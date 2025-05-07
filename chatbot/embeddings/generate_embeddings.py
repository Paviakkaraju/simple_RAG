from sentence_transformers import SentenceTransformer
import nltk
import uuid

# nltk.download('punkt')

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # or another open-source model

def num_tokens(text):
    from nltk.tokenize import word_tokenize
    return len(word_tokenize(text))

def embed_chunks(chunks):
    embedded_chunks = []
    for chunk in chunks:
        text = chunk['text']
        if num_tokens(text) > 2000:
            continue

        embedding = embedding_model.encode(text, convert_to_numpy=True).tolist()
        chunk['embedding'] = embedding

        if 'id' not in chunk['metadata']:
            chunk['metadata']['id'] = str(uuid.uuid4())

        embedded_chunks.append(chunk)
    return embedded_chunks
