import unittest
import os
from rdflib import Graph, Literal, URIRef
from modules.rdf_xml import triples_to_rdf

class TestTriplesToRdf(unittest.TestCase):

    def setUp(self):
        self.triples = [
            ("subject1", "predicate1", "object1"),
            ("subject2", "predicate2", "42"),
            ("subject3", "predicate3", "object3")
        ]
        self.output_file = "test_output.rdf"

    def tearDown(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_rdf_file_creation(self):
        triples_to_rdf(self.triples, self.output_file)
        self.assertTrue(os.path.exists(self.output_file))

    def test_rdf_content(self):
        triples_to_rdf(self.triples, self.output_file)
        g = Graph()
        g.parse(self.output_file, format="xml")
        self.assertEqual(len(g), 3)
        for subj, pred, obj in self.triples:
            subj_uri = f"http://hf2.org/{subj}"
            pred_uri = f"http://hf2.org/{pred}"
            if obj.isnumeric():
                obj_node = Literal(float(obj))
            else:
                obj_node = URIRef(f"http://hf2.org/{obj}")
            self.assertTrue((URIRef(subj_uri), URIRef(pred_uri), obj_node) in g)

if __name__ == "__main__":
    unittest.main()