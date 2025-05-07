import chromadb
from chromadb.config import Settings
import os

def get_chroma_collection(collection_name="codework_chunks", persist_dir="./chroma_db"):
    base_dir = os.path.dirname(os.path.dirname(__file__))  # one level up from ui/
    persist_path = os.path.join(base_dir, "chroma_db")

    client = chromadb.PersistentClient(path=persist_path)
    collection = client.get_collection("codework_chunks")
    return collection, client

def store_embedded_chunks(chunks, collection):
    for chunk in chunks:
        collection.add(
            documents=[chunk["text"]],
            embeddings=[chunk["embedding"]],
            metadatas=[chunk["metadata"]],
            ids=[chunk["metadata"]["id"]]
        )
