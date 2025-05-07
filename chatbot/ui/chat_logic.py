import chromadb
import os 
import sys
import requests
from config.config import GROQ_API_KEY 

base_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_dir)

base_dir = os.path.dirname(os.path.dirname(__file__))  # one level up from ui/
persist_path = os.path.join(base_dir, "chroma_db")

client = chromadb.PersistentClient(path=persist_path)
collection = client.get_collection("codework_chunks")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "meta-llama/llama-4-maverick-17b-128e-instruct"

# Fetch up to 5 items (just the IDs)
# items = collection.peek(5)
# print("Stored IDs:", items)

# query = "What are the services provided at codework?"
# results = collection.query(
#     query_texts=[query],
#     n_results=3
# )

# # Display the results
# for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
#     print(f"From section: {meta['section']} ({meta['url']})")
#     print(doc[:200], "\n---\n")
# === Groq Model Wrapper ===
class GroqLLaMAModel:
    def __init__(self, api_key, model_name):
        self.api_key = api_key
        self.model_name = model_name

    def generate_content(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2
        }
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    # Optional: make it callable like a function
    def __call__(self, prompt):
        return self.generate_content(prompt)
    
model = GroqLLaMAModel(GROQ_API_KEY, MODEL_NAME)
def get_relevant_chunks(query, emb_model, top_k=3):
    """
    Generate the query embedding, query the ChromaDB collection, and return the top matching documents.
    """
    query_embedding = emb_model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )
    return results

def generate_response(query, llm_generator, context):
    """
    Combine the query with the retrieved context and feed to the LLM to generate an answer.
    """
    # You can format the context as needed, e.g.:
    flat_context = [item for sublist in context for item in (sublist if isinstance(sublist, list) else [sublist])]
    context_text = "\n".join(map(str, flat_context))
    prompt = f"Context:\n{context_text}\n\nQuestion: {query}\nAnswer: "
    response = llm_generator.generate_content(prompt)
    return response