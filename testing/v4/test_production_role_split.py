#!/usr/bin/env python3
"""Regression tests for the mixed-use production role split."""

from pathlib import Path
import unittest

from rdflib import Graph, Namespace, RDF, RDFS

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PRODUCTION = Namespace("https://cacontology.projectvic.org/production#")
CORE = Namespace("https://cacontology.projectvic.org/core#")
GUFO = Namespace("http://purl.org/nemo/gufo#")


class ProductionRoleSplitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ontology = Graph().parse(REPO / "ontology" / "cacontology-production.ttl", format="turtle")
        cls.rhode_island = Graph().parse(REPO / "examples_knowledge_graphs" / "rhode-island-production-case.ttl", format="turtle")
        cls.vermont = Graph().parse(REPO / "examples_knowledge_graphs" / "vermont-case-example.ttl", format="turtle")
        cls.hartford = Graph().parse(REPO / "examples_knowledge_graphs" / "hartford-vermont-case-example.ttl", format="turtle")

    def test_record_classes_remain_operational_and_not_gufo_classifiers(self):
        for term in (PRODUCTION.Producer, PRODUCTION.ProductionVictim):
            self.assertIn((term, RDFS.subClassOf, CORE.Role), self.ontology)
            self.assertNotIn((term, RDF.type, GUFO.Role), self.ontology)

    def test_new_classifier_classes_use_person_bearer_branch(self):
        for term in (PRODUCTION.ProducerClassifier, PRODUCTION.ProductionVictimClassifier):
            self.assertIn((term, RDFS.subClassOf, CORE.PersonLikeEntity), self.ontology)
            self.assertIn((term, RDF.type, GUFO.Role), self.ontology)

    def test_rhode_island_role_nodes_remain_records(self):
        ex = Namespace("http://example.org/rhode-island-case#")
        self.assertIn((ex.ProducerRole, RDF.type, PRODUCTION.Producer), self.rhode_island)
        self.assertIn((ex.ProductionVictimRole001, RDF.type, PRODUCTION.ProductionVictim), self.rhode_island)
        self.assertIn((ex.ProductionVictimRole002, RDF.type, PRODUCTION.ProductionVictim), self.rhode_island)

    def test_enduring_bearer_nodes_use_classifiers(self):
        vermont = Namespace("http://example.org/vermont-case#")
        self.assertIn((vermont.BrianBluto, RDF.type, PRODUCTION.ProducerClassifier), self.vermont)
        self.assertIn((vermont.PrimaryVictim, RDF.type, PRODUCTION.ProductionVictimClassifier), self.vermont)
        self.assertIn((Namespace("https://example.org/persons/")["matthew-isaacs"], RDF.type, PRODUCTION.ProducerClassifier), self.hartford)
        self.assertIn((Namespace("https://example.org/persons/")["child-victim"], RDF.type, PRODUCTION.ProductionVictimClassifier), self.hartford)


if __name__ == "__main__":
    unittest.main()
