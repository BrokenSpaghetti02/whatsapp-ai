import os
from typing import List, Dict
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
from pypdf import PdfReader
import requests
import re

load_dotenv()

class RecursiveCharacterTextSplitter:
    """Simple text splitter for chunking documents"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200, length_function=len):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.length_function = length_function
    
    def split_text(self, text: str) -> List[str]:
        """Split text into chunks"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence or paragraph
            if end < len(text):
                # Look for sentence boundaries
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > self.chunk_size // 2:
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - self.chunk_overlap
        
        return [c for c in chunks if c]

# Initialize ChromaDB
client = chromadb.Client(Settings(
    persist_directory="chroma_db",
    anonymized_telemetry=False
))

# Collection name
COLLECTION_NAME = "documents"

def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Get embeddings using Hugging Face Inference API
    Uses sentence-transformers model for better semantic search
    """
    api_key = os.getenv('HUGGINGFACE_API_KEY')
    if not api_key:
        raise ValueError("HUGGINGFACE_API_KEY not set in environment")
    
    # Using a good embedding model from Hugging Face
    api_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
    
    headers = {"Authorization": f"Bearer {api_key}"}
    
    embeddings = []
    for text in texts:
        response = requests.post(api_url, headers=headers, json={"inputs": text})
        if response.status_code == 200:
            # The model returns embeddings directly
            embedding = response.json()
            # Handle different response formats
            if isinstance(embedding, list) and len(embedding) > 0:
                if isinstance(embedding[0], list):
                    embeddings.append(embedding[0])
                else:
                    embeddings.append(embedding)
            else:
                # Fallback to zeros if something goes wrong
                embeddings.append([0.0] * 384)  # all-MiniLM-L6-v2 has 384 dimensions
        else:
            print(f"Error getting embedding: {response.text}")
            embeddings.append([0.0] * 384)
    
    return embeddings

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF file"""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def process_documents():
    """
    Process all PDF documents in the documents folder
    and store them in ChromaDB
    """
    documents_dir = "documents"
    
    if not os.path.exists(documents_dir):
        print("No documents directory found")
        return
    
    # Get or create collection
    try:
        collection = client.get_collection(COLLECTION_NAME)
        # Delete existing collection to reprocess
        client.delete_collection(COLLECTION_NAME)
    except:
        pass
    
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "Document embeddings for RAG"}
    )
    
    # Text splitter for chunking documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    # Process each PDF
    all_chunks = []
    all_metadatas = []
    all_ids = []
    
    pdf_files = [f for f in os.listdir(documents_dir) if f.endswith('.pdf')]
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(documents_dir, pdf_file)
        print(f"Processing {pdf_file}...")
        
        # Extract text
        text = extract_text_from_pdf(pdf_path)
        
        # Split into chunks
        chunks = text_splitter.split_text(text)
        
        # Create metadata and IDs for each chunk
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_metadatas.append({
                "source": pdf_file,
                "chunk_id": i
            })
            all_ids.append(f"{pdf_file}_{i}")
    
    if all_chunks:
        print(f"Getting embeddings for {len(all_chunks)} chunks...")
        embeddings = get_embeddings(all_chunks)
        
        print("Storing in ChromaDB...")
        collection.add(
            documents=all_chunks,
            embeddings=embeddings,
            metadatas=all_metadatas,
            ids=all_ids
        )
        
        print(f"✓ Processed {len(pdf_files)} documents with {len(all_chunks)} chunks")
    else:
        print("No text extracted from documents")

def query_documents(query: str, n_results: int = 3) -> List[Dict]:
    """
    Query the document collection and return relevant chunks
    """
    try:
        collection = client.get_collection(COLLECTION_NAME)
    except:
        return []
    
    # Get embedding for query
    query_embedding = get_embeddings([query])[0]
    
    # Query collection
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    # Format results
    documents = []
    if results['documents']:
        for i, doc in enumerate(results['documents'][0]):
            documents.append({
                "content": doc,
                "metadata": results['metadatas'][0][i] if results['metadatas'] else {}
            })
    
    return documents

def get_llm_response(prompt: str, context: str, history: List[Dict] = None) -> str:
    """
    Get response from Hugging Face LLM
    Uses the Inference API with a good open-source model
    """
    api_key = os.getenv('HUGGINGFACE_API_KEY')
    if not api_key:
        raise ValueError("HUGGINGFACE_API_KEY not set in environment")
    
    # Using Mistral-7B or similar open-source model
    # You can change this to other models available on HF
    api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # Build the prompt with context
    system_prompt = """You are a helpful AI assistant. Use the following context to answer the user's question. 
If the context doesn't contain relevant information, you can use your general knowledge, but mention that the information is not from the provided documents.

Context:
{context}

Answer the question based on the context above."""
    
    full_prompt = system_prompt.format(context=context) + f"\n\nUser: {prompt}\nAssistant:"
    
    # Add conversation history if available
    if history and len(history) > 1:
        history_text = "\n".join([
            f"{msg['role'].capitalize()}: {msg['content']}" 
            for msg in history[-4:]  # Last 4 messages
        ])
        full_prompt = system_prompt.format(context=context) + f"\n\nPrevious conversation:\n{history_text}\n\nUser: {prompt}\nAssistant:"
    
    payload = {
        "inputs": full_prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7,
            "top_p": 0.95,
            "return_full_text": False
        }
    }
    
    response = requests.post(api_url, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            return result[0].get('generated_text', 'Sorry, I could not generate a response.')
        return str(result)
    else:
        error_msg = f"Error from API: {response.status_code}"
        if response.text:
            error_msg += f" - {response.text}"
        return error_msg

def get_rag_response(user_query: str, history: List[Dict] = None) -> str:
    """
    Main RAG function that combines document retrieval and LLM generation
    
    Args:
        user_query: User's question
        history: Conversation history
    
    Returns:
        AI response
    """
    # Query relevant documents
    relevant_docs = query_documents(user_query, n_results=3)
    
    # Build context from retrieved documents
    if relevant_docs:
        context = "\n\n".join([
            f"Document: {doc['metadata'].get('source', 'Unknown')}\n{doc['content']}"
            for doc in relevant_docs
        ])
    else:
        context = "No relevant documents found in the knowledge base."
    
    # Get LLM response with context
    response = get_llm_response(user_query, context, history)
    
    return response

if __name__ == "__main__":
    # Test the RAG system
    print("Processing documents...")
    process_documents()
    
    print("\nTesting query...")
    response = get_rag_response("What is this document about?")
    print(f"Response: {response}")
