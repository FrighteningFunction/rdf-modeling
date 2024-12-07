import logging
from flask import Flask, render_template, request
from modules.rdf_xml import triples_to_rdf
from modules.triple_generator import generate_triples
import configparser
from rdflib.plugins.sparql.processor import SPARQLResult
from urllib.parse import unquote
from rdflib import URIRef, Literal

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def load_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    input_file = config.get('Files', 'input_file', fallback='input_text.txt')
    output_file = config.get('Files', 'output_file', fallback='hf2.rdf')
    return input_file, output_file

# Generate RDF graph at startup
config_file = "config.ini"
input_file, output_file = load_config(config_file)
triples = generate_triples(input_file)
rdf_graph = triples_to_rdf(triples, output_file)

@app.route('/', methods=['GET', 'POST'])
def query():
    results = None
    if request.method == 'POST':
        # Get user input and map to SPARQL query
        subject = request.form.get('subject')
        predicate = request.form.get('predicate')
        obj = request.form.get('object')

        logging.info(f"Received input - Subject: {subject}, Predicate: {predicate}, Object: {obj}")

        # Build SPARQL query based on user input
        query_parts = []
        if subject:
            query_parts.append(f"?s = <http://hf2.org/{subject}>")
        if predicate:
            # Change the predicate to use full URI instead of namespace prefix
            query_parts.append(f"?p = <http://hf2.org/{predicate}>")
        if obj:
            query_parts.append(f'?o = "{obj}"@hu')

        # Construct the FILTER clause if there are query parts
        query_filter = f"FILTER ({' && '.join(query_parts)})" if query_parts else ''

        # Build the SPARQL query without the PREFIX declaration
        sparql_query = f"""
        SELECT ?s ?p ?o WHERE {{
            ?s ?p ?o .
            {query_filter}
        }}
        """
        logging.debug(f"Constructed SPARQL query:\n{sparql_query}")

        try:
            qres = rdf_graph.query(sparql_query)
            if isinstance(qres, SPARQLResult):
                results = []
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
                results = [{'error': 'No results found.'}]
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
            if isinstance(qres, SPARQLResult):
                results = []
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
                results = [{'error': 'No results found.'}]
        except Exception as e:
            logging.error(f"SPARQL query error: {e}")
            results = [{'error': str(e)}]

    return render_template('query.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)