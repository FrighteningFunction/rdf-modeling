# modules/triple_generator.py
import spacy
import huspacy
import re

def preprocess_text(text):
    """
    Preprocesses the input text by removing specific patterns and normalizing spaces.

    :param text: Raw input text.
    :return: Cleaned and preprocessed text.
    """
    text = re.sub(r'[a-f]\)', '', text)  # Remove subsection markers a), b)
    text = re.sub(r'\(\d+\)', '', text)  # Remove (1), (2)
    text = re.sub(r'\*|\"', '', text)  # Remove asterisks and quotes
    text = re.sub(r'\s+', ' ', text)  # Normalize spaces
    return text.strip()

def extract_triples(token, triples):
    """
    Extracts triples from a given token in the text.

    :param token: Token from the NLP model.
    :param triples: List to append the extracted triples.
    """
    subject = None
    predicate = None
    obj = None

    if token.dep_ == "nsubj":  # Subject
        subject = " ".join([
            child.lemma_ for child in token.subtree
            if child.dep_ in ["det", "amod", "compound", "appos", "acl", "relcl"]  # All possible modifiers
        ]) + " " + token.lemma_

        subject = re.sub(r'\b(a|az)\b', '', subject).strip() 

        predicate = token.head.lemma_  # Predicate
        obj = " ".join(set([
            child.lemma_ for child in token.head.subtree
            if child.dep_ in ["attr", "obj"] and len(child.lemma_) > 2
        ]))
        triples.append((subject.strip(), predicate, obj.strip()))

def generate_triples(file_path):
    """
    Generates triples from the input text file.

    :param file_path: Path to the input text file.
    :return: List of extracted triples.
    """
    with open(file_path, "r", encoding='utf-8') as f:
        text = f.read()

    text = preprocess_text(text)

    nlp = huspacy.load()
    doc = nlp(text)

    stopwords = ["azt", "az", "a", "és", "vagy", "is", "nem", "nincs", "van", "volt", "lesz", "ha", "de", "már"]

    triples = []

    # Process sentences and tokens
    for sent in doc.sents:
        filtered_tokens = [token for token in sent if token.lemma_.lower() not in stopwords and token.is_alpha]
        for token in filtered_tokens:
            extract_triples(token, triples)

    # Post-process triples
    triples = [(nsubj, pred, obj) for nsubj, pred, obj in triples if nsubj and pred and obj]
    triples = list(set(triples))  # Remove duplicates

    return triples

if __name__ == "__main__":
    file_path = "./input_text.txt"
    triples = generate_triples(file_path)
    print(triples)
