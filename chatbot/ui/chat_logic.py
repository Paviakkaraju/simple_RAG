import chromadb
import os 

base_dir = os.path.dirname(os.path.dirname(__file__))  # one level up from ui/
persist_path = os.path.join(base_dir, "chroma_db")

client = chromadb.PersistentClient(path=persist_path)
collection = client.get_collection("codework_chunks")

# Fetch up to 5 items (just the IDs)
# items = collection.peek(5)
# print("Stored IDs:", items)

query = "What are the services provided at codework?"
results = collection.query(
    query_texts=[query],
    n_results=3
)

# Display the results
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(f"From section: {meta['section']} ({meta['url']})")
    print(doc[:200], "\n---\n")