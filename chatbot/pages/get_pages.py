import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_internal_links(url):
    '''
    This function takes a URL as input and returns a set of all the internal links found on the page.
    Args:
        url (str): The URL of the page to get the links.
        
    Returns:
        set: A set of all the internal links found on the page.
    '''
    
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    # Finding all <a> tags. 
    links = soup.find_all('a', href=True)
    
    internal_links = set()
    
    for link in links:
        href = link.get("href")
        
        # Joining relative links with base URL
        full_url = urljoin(url, href)
        
        # Keeping only internal links (that belong to the same domain)
        if urlparse(full_url).netloc == urlparse(url).netloc:
            internal_links.add(full_url)
           
            
    return internal_links