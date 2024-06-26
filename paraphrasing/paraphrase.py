import random
from nltk.corpus import wordnet
from textblob import TextBlob

# Download necessary NLTK data
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('punkt')

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonym = lemma.name().replace('_', ' ').lower()
            if synonym != word:
                synonyms.add(synonym)
    return list(synonyms)

def paraphrase_sentence(sentence):
    words = nltk.word_tokenize(sentence)
    tagged_words = nltk.pos_tag(words)
    
    new_sentence = []
    for word, tag in tagged_words:
        if tag.startswith('NN') or tag.startswith('VB') or tag.startswith('JJ'):
            synonyms = get_synonyms(word)
            if synonyms:
                new_word = random.choice(synonyms)
                new_sentence.append(new_word)
            else:
                new_sentence.append(word)
        else:
            new_sentence.append(word)
    
    return ' '.join(new_sentence)

def paraphrase_text(text, variation=3):
    blob = TextBlob(text)
    sentences = blob.sentences
    paraphrased_sentences = [paraphrase_sentence(str(sentence)) for sentence in sentences]

    for _ in range(variation - 1):
        additional_sentences = [paraphrase_sentence(str(sentence)) for sentence in sentences]
        paraphrased_sentences.extend(additional_sentences)
    
    return ' '.join(paraphrased_sentences)
