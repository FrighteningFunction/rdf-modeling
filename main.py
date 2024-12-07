from modules.rdf_xml import triples_to_rdf
from modules.triple_generator import generate_triples
import configparser

def load_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    input_file = config.get('Files', 'input_file', fallback='input_text.txt')
    output_file = config.get('Files', 'output_file', fallback='hf2.rdf')
    return input_file, output_file

def run_cli(rdf_graph):
    print("\nEnter SPARQL queries below (type 'exit' to quit):")
    query_lines = []
    while True:
        line = input(">>> ")
        if line.strip().lower() == 'exit':
            break
        query_lines.append(line)
        if line.strip().endswith('}'):
            query = "\n".join(query_lines)
            query_lines = []
            try:
                results = rdf_graph.query(query)
                for result in results:
                    print(result)
            except Exception as e:
                print(f"Error: {e}")

def main():
    config_file = "config.ini"
    input_file, output_file = load_config(config_file)

    # Generate triples from the input text
    triples = generate_triples(input_file)
    print("Generated Triples:", triples)

    # Convert triples to RDF/XML, save to a file, and get the RDF graph
    rdf_graph = triples_to_rdf(triples, output_file)

    # Run the CLI for SPARQL queries
    run_cli(rdf_graph)

if __name__ == "__main__":
    main()