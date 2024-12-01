# modules/rdf_xml.py
from rdflib import Graph, URIRef, Literal, Namespace
from urllib.parse import quote

def triples_to_rdf(triples, output_file="output.rdf"):
    """
    Converts Python triples to RDF/XML format and saves to a file.
    
    :param triples: List of triples (subject, predicate, object)
    :param output_file: Path to save the RDF/XML file
    """
    EX = Namespace("http://hf2.org/")

    # Initialize RDF graph
    g = Graph()

    for subject, predicate, obj in triples:
        # Encode spaces in URIs
        subj_uri = URIRef(EX + quote(subject))
        pred_uri = URIRef(EX + quote(predicate))
        if obj.isnumeric():
            obj_node = Literal(float(obj))
        else:
            obj_node = URIRef(EX + quote(obj))

        # Add triple to graph
        g.add((subj_uri, pred_uri, obj_node))

    # Serialize graph to RDF/XML
    g.serialize(destination=output_file, format="xml")
    print(f"RDF/XML file saved to: {output_file}")
