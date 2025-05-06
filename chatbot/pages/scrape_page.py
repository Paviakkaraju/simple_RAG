import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    
    # Removing unwanted elements
    for tag in soup(["script", "style", "nav", "footer", "header", "form"]):
        tag.decompose()
        
    # Extracting visible text
    text = soup.get_text(separator="\n")
    
    UNWANTED_LINES = {
    "AI Solutions",
    "Industries",
    "Company",
    "AI Community",
    "Get In Touch",
    "×",}
    
    # Cleaning whitespace
    lines = text.split("\n")
    cleaned = [line.strip() for line in lines if line.strip() and line.strip() not in UNWANTED_LINES]
    text = "\n".join(cleaned)
    return text