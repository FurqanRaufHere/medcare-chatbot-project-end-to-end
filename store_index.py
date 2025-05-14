from src.helpers import load_pdf_file, text_split, download_huggingface_embeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv  
import os

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY


extracted_data = load_pdf_file("Data/")
text_chunks = text_split(extracted_data)
embeddings = download_huggingface_embeddings()



# pc = Pinecone(api_key=PINECONE_API_KEY)
# index_name = "MedChat chatbot"

# pc.create_index(
#     name=index_name,
#     dimension=384,  # The dimension of the embeddings
#     metric="cosine",
#     spec=ServerlessSpec(
#         cloud="aws",
#         region="us-east-1",
#     )
# )


# # embed each chunk and upsert the embeddings into your pinecone index
# docsearch = PineconeVectorStore.from_documents(
#     documents=text_chunks,
#     index_name=index_name,
#     embedding=embeddings
# )



# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "ChatMED"

# List all indexes to check if the desired index already exists
existing_indexes = pc.list_indexes().names()

# Only create the index if it doesn't already exist
if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=384,  # The dimension of the embeddings
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1",
        )
    )
else:
    print(f"Index '{index_name}' already exists. Skipping creation.")
