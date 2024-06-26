import requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import quote

# Configure logging
logging.basicConfig(level=logging.INFO)

GOOGLE_SEARCH_URL = "https://www.google.com/search?q="

def fetch_urls_from_google(focus_keyword):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    search_url = GOOGLE_SEARCH_URL + quote(focus_keyword)
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        links = []
        for g in soup.find_all('div', class_='g'):
            a_tag = g.find('a')
            if a_tag:
                url = a_tag.get('href')
                if url.startswith("http"):
                    links.append(url)
                    
        logging.info(f"Found URLs: {links}")
        return links
    except Exception as e:
        logging.error(f"Error fetching URLs from Google: {e}")
        return []

# Test function
if __name__ == "__main__":
    focus_keyword = "teething child crying at night"
    urls = fetch_urls_from_google(focus_keyword)
    print("Found URLs:", urls)
