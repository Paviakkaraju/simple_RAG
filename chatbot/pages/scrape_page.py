import requests
from bs4 import BeautifulSoup
import uuid


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

def fetch_webpage(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_and_chunk(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    content_chunks = []

    current_heading = "Introduction"
    current_text = ""

    for tag in soup.find_all(['h1', 'h2', 'h3', 'p']):
        if tag.name in ['h1', 'h2', 'h3']:
            if current_text.strip():
                content_chunks.append({
                    "text": current_heading + "\n" + current_text.strip(),
                    "metadata": {
                        "url": url,
                        "section": current_heading,
                        "id": str(uuid.uuid4())
                    }
                })
            current_heading = tag.get_text().strip()
            current_text = ""
        elif tag.name == 'p':
            current_text += tag.get_text().strip() + "\n"
            
    if current_text.strip():
        content_chunks.append({
            "text": current_heading + "\n" + current_text.strip(),
            "metadata": {
                "url": url,
                "section": current_heading,
                "id": str(uuid.uuid4())
            }
        })

    return content_chunks