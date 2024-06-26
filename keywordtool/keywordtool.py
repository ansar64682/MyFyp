import requests
from bs4 import BeautifulSoup
import spacy
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

nlp = spacy.load('en_core_web_sm')

# A predefined list of URLs to scrape for demonstration purposes
PREDEFINED_URLS = [
    "https://www.verywellfamily.com/teething-in-babies-4172172",
    "https://www.whattoexpect.com/first-year/teething.aspx",
    "https://www.webmd.com/parenting/baby/teething-pain-relief-tips",
    # Add more URLs as needed
]

def fetch_predefined_content():
    content = ""
    for url in PREDEFINED_URLS:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text()
            content += text + " "
        except Exception as e:
            logging.error(f"Error fetching or parsing content from {url}: {e}")
    return content

def extract_keywords_from_text(text):
    doc = nlp(text)
    keywords = [chunk.text.lower() for chunk in doc.noun_chunks if len(chunk.text.split()) > 1]
    return keywords

def get_keywords(focus_keyword):
    try:
        logging.info(f"Using predefined content for keyword: {focus_keyword}")
        content = fetch_predefined_content()
        logging.info(f"Extracting keywords from content of length: {len(content)}")
        keywords = extract_keywords_from_text(content)

        # Generate long tail keywords by appending the focus keyword
        long_tail_keywords = [f"{focus_keyword} {kw}" for kw in keywords[:5]]
        
        # LSI keywords are the next 20 most frequent phrases
        lsi_keywords = keywords[5:25]

        logging.info(f"Generated long tail keywords: {long_tail_keywords}")
        logging.info(f"Generated LSI keywords: {lsi_keywords}")

        return long_tail_keywords, lsi_keywords
    except Exception as e:
        logging.error(f"Error in get_keywords: {e}")
        return [], []

# Test function
if __name__ == "__main__":
    focus_keyword = "teething child crying at night"
    long_tail, lsi = get_keywords(focus_keyword)
    print("Long Tail Keywords:", long_tail)
    print("LSI Keywords:", lsi)
