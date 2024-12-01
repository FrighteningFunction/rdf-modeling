import spacy
import huspacy

# Load Hungarian spaCy model
nlp = huspacy.load()

# Input sentence
text = "Magyarország területén csak olyan külföldi rendszámú gépjármű közlekedhet, amelyet a rendszámot kiadó állam jelzésével elláttak."

# Process the text
doc = nlp(text)

triples = []
for token in doc:
    if token.dep_ == "nsubj":  # Find subject
        # Expand subject with its modifiers
        subject = " ".join([
            child.text for child in token.subtree
            if child.dep_ in ["appos", "recl", "acl", "obl", "attr", "det", "amod", "compound", "nmod", "case"]
        ]) + " " + token.text

        # Extract predicate
        predicate = token.head.lemma_

        # Extract object with relative clauses and oblique modifiers
        obj_tokens = [
            child.text for child in token.head.subtree
            if child.dep_ in ["obj", "obl", "attr", "acl", "relcl", "appos"]
        ]
        obj = " ".join(sorted(obj_tokens, key=lambda x: doc.text.find(x)))  # Preserve original order

        # Add to triples
        triples.append((subject.strip(), predicate, obj.strip()))

print("Extracted Triples:", triples)

