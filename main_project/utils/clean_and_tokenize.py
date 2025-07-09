import re

def clean_and_tokenize(text):
    # Lowercase, remove punctuation, and split
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text.split()
