# 🩺MedCare Chatbot – RAG-based Medical Assistant

MedCare is a Retrieval-Augmented Generation (RAG) based medical chatbot that leverages Google’s Gemini 2.0 Flash model and Pinecone vector database to provide intelligent, personalized responses from custom medical datasets.

This project uses LangChain to manage document loading, chunking, semantic search, and LLM-based response generation.

---

## Features

- RAG architecture using LangChain and Gemini 2.0 Flash
- Semantic search over embedded medical documents using Pinecone
- Modular codebase structured across `src/`, `Data/`, and `research/` directories
- Streamlined PDF ingestion, vector storage, and question answering
- Custom prompts for precise and informative medical responses

---

## Tech Stack

- Python
- LangChain
- Pinecone (vector DB)
- Gemini 2.0 Flash (Google Generative AI)
- Streamlit (for UI)
- PyPDF2, tiktoken, python-dotenv

---

## How It Works

1. **Document Loading**  
   Medical PDFs are placed in the `Data/` directory and processed using PyPDF2.

2. **Text Chunking and Embedding**  
   The text is chunked and embedded via a transformer model and stored in Pinecone.

3. **Semantic Retrieval**  
   When a user asks a question, the system retrieves the most relevant text chunks from Pinecone based on vector similarity.

4. **LLM-based Generation**  
   The retrieved context is passed into Gemini 2.0 Flash via LangChain, which generates a customized, medically sound response.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/medcare-chatbot.git
cd medcare-chatbot

---
- If need some help, then email at: furqanrauf6@gmail.com
