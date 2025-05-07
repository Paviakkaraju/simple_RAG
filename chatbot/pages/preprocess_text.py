import re
from sentence_transformers import SentenceTransformer
import nltk
import uuid

nltk.download('punkt')

UNWANTED_LINES = {"Free Consulting", "Discover More", "Read More"}

def preprocess_text(text):
    lines = text.splitlines()
    cleaned = [line.strip() for line in lines if line.strip() and line.strip() not in UNWANTED_LINES]
    
    deduped = list(dict.fromkeys(cleaned))  # Preserve order while removing duplicates
    return "\n".join(deduped)
