import requests
from bs4 import BeautifulSoup
import spacy
import logging
from collections import Counter
from .url_fetch import fetch_urls_from_google  # Correct relative import

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load the medium Spacy model
nlp = spacy.load('en_core_web_md')

def fetch_content_from_urls(urls):
    content = ""
    for url in urls:
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

def extract_lsi_keywords(text, focus_keyword):
    doc = nlp(text)
    focus_vec = nlp(focus_keyword).vector
    words = [token.lemma_.lower() for token in doc if token.is_alpha and not token.is_stop]
    word_freq = Counter(words)
    common_words = word_freq.most_common(200)

    lsi_keywords = set()  # Use a set to avoid repetitions
    for word, freq in common_words:
        word_vec = nlp(word).vector
        similarity = nlp(focus_keyword).similarity(nlp(word))
        if word != focus_keyword and word not in lsi_keywords and similarity > 0.5:
            lsi_keywords.add(word)
            if len(lsi_keywords) >= 10:
                break

    # Adding combinations of two words
    bigrams = list(nlp(text).noun_chunks)
    bigram_keywords = set()  # Use a set to avoid repetitions
    for bigram in bigrams:
        if 1 < len(bigram.text.split()) <= 2 and bigram.text.lower() not in lsi_keywords and bigram.text.lower() != focus_keyword:
            similarity = nlp(focus_keyword).similarity(nlp(bigram.text))
            if similarity > 0.5:
                bigram_keywords.add(bigram.text.lower())
                if len(bigram_keywords) + len(lsi_keywords) >= 20:
                    break

    return list(lsi_keywords) + list(bigram_keywords)

def get_keywords(focus_keyword):
    try:
        logging.info(f"Fetching URLs for keyword: {focus_keyword}")
        urls = fetch_urls_from_google(focus_keyword)
        
        if not urls:
            logging.error("No URLs found, using predefined content")
            return [], []

        content = fetch_content_from_urls(urls)
        logging.info(f"Extracting keywords from content of length: {len(content)}")
        keywords = extract_keywords_from_text(content)

        # Generate long tail keywords by appending the focus keyword
        long_tail_keywords = []
        for kw in keywords:
            long_tail = f"{focus_keyword} {kw}"
            if len(long_tail) <= 60:
                long_tail_keywords.append(long_tail)
                if len(long_tail_keywords) >= 5:
                    break

        # Generate LSI keywords
        lsi_keywords = extract_lsi_keywords(content, focus_keyword)

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
