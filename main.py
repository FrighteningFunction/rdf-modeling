# main.py
from modules.rdf_xml import triples_to_rdf
from modules.triple_generator import generate_triples

def main():
    input_file = "input_text.txt"
    output_file = "hf2.rdf"

    # Generate triples from the input text
    triples = generate_triples(input_file)
    print("Generated Triples:", triples)

    # Convert triples to RDF/XML and save to a file
    triples_to_rdf(triples, output_file)

if __name__ == "__main__":
    main()