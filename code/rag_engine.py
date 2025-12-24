import os
import faiss
import pickle
import numpy as np
import ollama
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from docx import Document as DocxDocument

# Constants
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'
EMBEDDING_DIM = 384
INDEX_FILE = "vector_index.faiss"
METADATA_FILE = "metadata.pkl"

class RAGEngine:
    def __init__(self, storage_path: str = "storage"):
        self.storage_path = storage_path
        os.makedirs(self.storage_path, exist_ok=True)
        
        self.index_path = os.path.join(self.storage_path, INDEX_FILE)
        self.metadata_path = os.path.join(self.storage_path, METADATA_FILE)
        
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        
        self.index = None
        self.chunks_metadata = [] # List of {"text": str, "source": str}
        
        self._load_index()

    def _load_index(self):
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            try:
                self.index = faiss.read_index(self.index_path)
                with open(self.metadata_path, "rb") as f:
                    self.chunks_metadata = pickle.load(f)
                print(f"Loaded index with {self.index.ntotal} vectors.")
            except Exception as e:
                print(f"Error loading index: {e}. Starting fresh.")
                self._init_new_index()
        else:
            self._init_new_index()

    def _init_new_index(self):
        self.index = faiss.IndexFlatL2(EMBEDDING_DIM)
        self.chunks_metadata = []

    def _save_index(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, "wb") as f:
            pickle.dump(self.chunks_metadata, f)

    def process_file(self, file_path: str, filename: str) -> int:
        text = ""
        ext = os.path.splitext(filename)[1].lower()
        
        try:
            if ext == '.pdf':
                reader = PdfReader(file_path)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            elif ext == '.docx':
                doc = DocxDocument(file_path)
                for para in doc.paragraphs:
                    text += para.text + "\n"
            elif ext == '.txt':
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
            else:
                return 0
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            return 0
            
        if not text.strip():
            return 0
            
        # Chunking
        chunks = self.text_splitter.split_text(text)
        if not chunks:
            return 0
            
        # Embedding
        embeddings = self.embedding_model.encode(chunks)
        
        # Add to Index
        self.index.add(np.array(embeddings).astype('float32'))
        
        # Add Metadata
        for chunk in chunks:
            self.chunks_metadata.append({
                "text": chunk,
                "source": filename
            })
            
        self._save_index()
        return len(chunks)

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        if self.index.ntotal == 0:
            return []
            
        query_vector = self.embedding_model.encode([query]).astype('float32')
        distances, indices = self.index.search(query_vector, top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.chunks_metadata):
                item = self.chunks_metadata[idx]
                results.append({
                    "text": item['text'],
                    "source": item['source'],
                    "score": float(distances[0][i])
                })
        return results

    def generate_response(self, query: str, history: List[dict], strict_mode: bool = True) -> Dict:
        # Retrieve context
        retrieved = self.search(query, top_k=5)
        
        context_text = "\n\n".join([f"Source ({r['source']}): {r['text']}" for r in retrieved])
        
        system_prompt = "You are a helpful AI assistant. Answer the user's question based ONLY on the provided context."
        if not strict_mode:
            system_prompt = "You are a creative AI assistant. Use the provided context to answer the user's question, but you can also add your own insights."
            
        if not retrieved and strict_mode:
             return {
                "response": "I couldn't find any relevant information in your documents to answer this question.",
                "sources": []
            }

        prompt = f"""Context:
{context_text}

User Question: {query}
"""

        messages = [{"role": "system", "content": system_prompt}]
        # Add history (limit last 5 messages to avoid blowing up context)
        for msg in history[-5:]: 
             messages.append(msg)
        
        messages.append({"role": "user", "content": prompt})

        # Ask Ollama
        try:
            response = ollama.chat(model='qwen2.5', messages=messages)
            return {
                "response": response['message']['content'],
                "sources": retrieved
            }
        except Exception as e:
            return {
                "response": f"Error communicating with local LLM: {str(e)}",
                "sources": []
            }


