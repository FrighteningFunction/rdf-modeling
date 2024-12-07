import logging
from flask import Flask, render_template, request
from modules.rdf_xml import triples_to_rdf
from modules.triple_generator import generate_triples
import configparser
from rdflib.plugins.sparql.processor import SPARQLResult
from urllib.parse import unquote, quote
from rdflib import URIRef, Literal

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)


def load_config(config_file):
    """
    Loads configuration from the given config file.

    :param config_file: Path to the configuration file.
    :return: Tuple containing input_file and output_file paths.
    """
    config = configparser.ConfigParser()
    config.read(config_file)
    input_file = config.get('Files', 'input_file', fallback='input_text.txt')
    output_file = config.get('Files', 'output_file', fallback='hf2.rdf')
    return input_file, output_file


def load_rdf_graph(input_file, output_file):
    """
    Generates and loads the RDF graph from the given input file.

    :param input_file: Path to the input text file.
    :param output_file: Path to save the RDF/XML file.
    :return: RDF graph object.
    """
    triples = generate_triples(input_file)
    logging.info(f"Generated Triples: {triples}")
    rdf_graph = triples_to_rdf(triples, output_file)
    return rdf_graph


def build_sparql_query(subject, predicate, obj):
    """
    Constructs a SPARQL query based on provided subject, predicate, and object.

    :param subject: Subject input by the user.
    :param predicate: Predicate input by the user.
    :param obj: Object input by the user.
    :return: Constructed SPARQL query string.
    """
    query_parts = []
    if subject:
        encoded_subject = quote(subject, safe='')
        query_parts.append(f"?s = <http://hf2.org/{encoded_subject}>")
    if predicate:
        encoded_predicate = quote(predicate, safe='')
        query_parts.append(f"?p = <http://hf2.org/{encoded_predicate}>")
    if obj:
        # Create a Literal and serialize it to SPARQL format
        obj_literal = Literal(obj, lang="hu")
        serialized_obj = obj_literal.n3()
        query_parts.append(f'?o = {serialized_obj}')

    query_filter = f"FILTER ({' && '.join(query_parts)})" if query_parts else ''

    sparql_query = f"""
    SELECT ?s ?p ?o WHERE {{
        ?s ?p ?o .
        {query_filter}
    }}
    """
    logging.debug(f"Constructed SPARQL query:\n{sparql_query}")
    return sparql_query


def process_query_results(qres):
    """
    Processes the SPARQL query results, decoding URIs for display.

    :param qres: SPARQL query result.
    :return: List of dictionaries containing the results.
    """
    results = []
    if isinstance(qres, SPARQLResult):
        for row in qres:
            result = {}
            for var in qres.vars:
                value = row[var]
                if isinstance(value, URIRef):
                    # Extract local name from URI and decode it
                    local_name = value.split('/')[-1]
                    value = unquote(local_name)
                elif isinstance(value, Literal):
                    value = str(value)
                result[str(var)] = value
            results.append(result)
        logging.info(f"Query returned {len(results)} results.")
    else:
        logging.warning("No results found.")
        results = [{'error': 'No results found.'}]
    return results


@app.route('/', methods=['GET', 'POST'])
def query():
    """
    Handles the root route for querying the RDF graph.
    Supports both GET and POST methods.
    """
    results = None
    if request.method == 'POST':
        # Get user input and map to SPARQL query
        subject = request.form.get('subject')
        predicate = request.form.get('predicate')
        obj = request.form.get('object')

        logging.info(f"Received input - Subject: {subject}, Predicate: {predicate}, Object: {obj}")

        sparql_query = build_sparql_query(subject, predicate, obj)

        try:
            qres = rdf_graph.query(sparql_query)
            results = process_query_results(qres)
        except Exception as e:
            logging.error(f"SPARQL query error: {e}")
            results = [{'error': str(e)}]
    else:
        logging.warning("No input provided; displaying all triples.")
        sparql_query = """
        PREFIX ex: <http://hf2.org/>
        SELECT ?s ?p ?o WHERE {
            ?s ?p ?o .
        }
        """
        try:
            qres = rdf_graph.query(sparql_query)
            results = process_query_results(qres)
        except Exception as e:
            logging.error(f"SPARQL query error: {e}")
            results = [{'error': str(e)}]

    return render_template('query.html', results=results)


if __name__ == "__main__":
    input_file, output_file = load_config("config.ini")
    rdf_graph = load_rdf_graph(input_file, output_file)
    app.run(debug=True)