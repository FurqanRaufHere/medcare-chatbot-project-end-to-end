from flask import Flask, render_template, jsonify, request
from src.helpers import download_huggingface_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY


embeddings = download_huggingface_embeddings()

indexname = "medcare-medchatbot"
#Embed each chunk and upsert the embeddings into your pinecone index
docsearch = PineconeVectorStore.from_existing_index(
    index_name=indexname,
    embedding=embeddings
 )

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

llm = ChatGroq(
    temperature=0.4,
    model_name="llama3-70b-8192",  # or "llama3-8b-8192"
    groq_api_key=os.environ["GROQ_API_KEY"]
)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get', methods=["GET", "POST"])
def chat():
    msg = request.args.get("msg")
    input = msg
    print(input)
    response = rag_chain.invoke({"input": msg})
    print("Response:", response["answer"])
    return str(response["answer"])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug=True)