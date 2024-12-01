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
    g.bind("ex", EX)

    for subject, predicate, obj in triples:
        # Encode spaces and special characters in URIs
        subj_uri = URIRef(EX + quote(subject, safe=''))
        # Use Namespace for predicates to ensure valid XML elements
        pred_uri = EX[predicate]
        if obj.isnumeric():
            obj_node = Literal(float(obj))
        elif obj.startswith("http://") or obj.startswith("https://"):
            obj_node = URIRef(obj)
        else:
            obj_node = Literal(obj, lang="hu")

        # Add triple to graph
        g.add((subj_uri, pred_uri, obj_node))

    # Serialize graph to RDF/XML with UTF-8 encoding
    g.serialize(destination=output_file, format="xml", encoding="utf-8")
    print(f"RDF/XML file saved to: {output_file}")
