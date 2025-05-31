# from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import HuggingFaceEmbeddings
import re



#Extract text from a PDF file
def load_pdf_file(data):
    loader = DirectoryLoader(data,
                             glob="*.pdf",
                             loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents

#Split the text into chunks
def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20,
    )
    texts_chunks = text_splitter.split_documents(extracted_data)
    return texts_chunks

# Download the Embeddings from HuggingFace
def download_huggingface_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings



# prompt template for the chatbot
def extract_topic(user_query):
    """
    Extract the main medical topic from user query
    
    Args:
        user_query (str): The user's question or message
        
    Returns:
        str: Identified medical topic or generic fallback
    """
    # List of common medical topics to check for
    common_topics = [
        "diabetes", "hypertension", "blood pressure", "heart disease", "cancer",
        "covid", "depression", "anxiety", "medication", "diet", "exercise",
        "nutrition", "sleep", "pain", "pregnancy", "vaccination", "headache",
        "migraine", "allergies", "asthma", "arthritis", "cholesterol",
        "atkins diet", "keto diet", "mediterranean diet", "vitamins", "supplements"
    ]
    
    # Check for exact topic matches
    for topic in common_topics:
        # Look for the topic as a whole word
        pattern = r'\b' + re.escape(topic) + r'\b'
        if re.search(pattern, user_query.lower()):
            # Capitalize first letter of each word for title format
            return ' '.join(word.capitalize() for word in topic.split())
    
    # Fall back to a generic topic if no match
    return "Your Medical Question"


def create_bullet_list(items):
    """
    Convert a list of items to a formatted bullet list
    
    Args:
        items (list): List of string items
        
    Returns:
        str: Formatted bullet list in markdown
    """
    if not items:
        return ""
    
    return "\n".join([f"- {item}" for item in items])


def create_numbered_list(items):
    """
    Convert a list of items to a formatted numbered list
    
    Args:
        items (list): List of string items
        
    Returns:
        str: Formatted numbered list in markdown
    """
    if not items:
        return ""
    
    return "\n".join([f"{i+1}. {item}" for i, item in enumerate(items)])


def extract_sections_from_llm_response(response):
    """
    Extract structured sections from LLM response
    
    Args:
        response (str): Raw LLM response text
        
    Returns:
        dict: Dictionary with extracted sections
    """
    # Initialize dictionary for sections
    sections = {
        "topic": "Medical Information",
        "greeting": "",
        "overview": "",
        "key_points": [],
        "details": "",
        "recommendations": [],
        "important_notes": "",
        "next_steps": [],
        "closing": ""
    }
    
    # Extract main topic (if present)
    topic_match = re.search(r'#\s+(.+?)(?=\n|$)', response)
    if topic_match:
        sections["topic"] = topic_match.group(1).strip()
    
    # Extract sections using regex
    section_pattern = r'##\s+([\w\s]+)(?:\n|\r\n?)(.*?)(?=##\s+[\w\s]+|\Z)'
    section_matches = re.finditer(section_pattern, response, re.DOTALL)
    
    for match in section_matches:
        section_name = match.group(1).strip().lower()
        section_content = match.group(2).strip()
        
        # Map section names to dictionary keys
        if "greeting" in section_name:
            sections["greeting"] = section_content
        elif "overview" in section_name:
            sections["overview"] = section_content
        elif "key information" in section_name:
            # Extract bullet points
            sections["key_points"] = [
                point.strip('- ').strip() 
                for point in re.findall(r'-\s+(.+?)(?=\n-|\n\n|\Z)', section_content + "\n\n")
            ]
        elif "detail" in section_name:
            sections["details"] = section_content
        elif "recommend" in section_name:
            # Extract bullet points
            sections["recommendations"] = [
                point.strip('- ').strip() 
                for point in re.findall(r'-\s+(.+?)(?=\n-|\n\n|\Z)', section_content + "\n\n")
            ]
        elif "important note" in section_name:
            sections["important_notes"] = section_content
        elif "next step" in section_name:
            # Extract numbered points
            sections["next_steps"] = [
                point.strip('0123456789. ').strip() 
                for point in re.findall(r'\d+\.\s+(.+?)(?=\n\d+\.|\n\n|\Z)', section_content + "\n\n")
            ]
        elif "closing" in section_name:
            sections["closing"] = section_content
    
    return sections


def markdown_to_html(markdown_text):
    """
    Basic conversion of markdown to HTML for frontend display
    
    Args:
        markdown_text (str): Markdown formatted text
        
    Returns:
        str: HTML formatted text
    """
    html = markdown_text
    
    # Convert headings
    html = re.sub(r'# (.*?)(?=\n|$)', r'<h1>\1</h1>', html)
    html = re.sub(r'## (.*?)(?=\n|$)', r'<h2>\1</h2>', html)
    html = re.sub(r'### (.*?)(?=\n|$)', r'<h3>\1</h3>', html)
    
    # Convert bullet lists
    bullet_pattern = r'- (.*?)(?=\n-|\n\n|\Z)'
    html = re.sub(bullet_pattern, r'<li>\1</li>', html)
    html = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', html, flags=re.DOTALL)
    
    # Convert numbered lists (basic)
    html = re.sub(r'\d+\.\s+(.*?)(?=\n\d+\.|\n\n|\Z)', r'<li>\1</li>', html)
    html = re.sub(r'(<li>.*?</li>)', r'<ol>\1</ol>', html, flags=re.DOTALL)
    
    # Convert bold text
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    
    # Convert italic text
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    
    # Convert paragraphs
    html = re.sub(r'\n\n', r'</p><p>', html)
    html = f'<p>{html}</p>'
    
    # Clean up any double tags that might have been created
    html = html.replace('<p><ul>', '<ul>').replace('</ul></p>', '</ul>')
    html = html.replace('<p><ol>', '<ol>').replace('</ol></p>', '</ol>')
    
    return html