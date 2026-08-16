#!/usr/bin/env python3
"""Reject RDF structures that OWLAPI cannot translate into OWL axioms."""

from pathlib import Path
import unittest

from rdflib import Graph, OWL, RDF

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


class OwlApiRdfStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = Graph()
        for path in sorted((REPO / "ontology").glob("*.ttl")):
            cls.graph.parse(path, format="turtle")

    def test_reified_axioms_have_all_required_components(self):
        required = (OWL.annotatedSource, OWL.annotatedProperty, OWL.annotatedTarget)
        incomplete = {
            str(node): [str(predicate) for predicate in required if not list(self.graph.objects(node, predicate))]
            for node in self.graph.subjects(RDF.type, OWL.Axiom)
        }
        incomplete = {node: missing for node, missing in incomplete.items() if missing}
        self.assertEqual({}, incomplete)

    def test_negative_property_assertions_have_all_required_components(self):
        incomplete = {}
        for node in self.graph.subjects(RDF.type, OWL.NegativePropertyAssertion):
            missing = []
            if not list(self.graph.objects(node, OWL.sourceIndividual)):
                missing.append(str(OWL.sourceIndividual))
            if not list(self.graph.objects(node, OWL.assertionProperty)):
                missing.append(str(OWL.assertionProperty))
            if not (
                list(self.graph.objects(node, OWL.targetIndividual))
                or list(self.graph.objects(node, OWL.targetValue))
            ):
                missing.append("owl:targetIndividual|owl:targetValue")
            if missing:
                incomplete[str(node)] = missing
        self.assertEqual({}, incomplete)


if __name__ == "__main__":
    unittest.main()
