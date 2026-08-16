#!/usr/bin/env python3
"""Tests for relationship/state separation in the custodial module."""

from pathlib import Path
import unittest

from owlrl import DeductiveClosure, RDFS_Semantics
from pyshacl import validate
from rdflib import Graph, Namespace, RDF, RDFS

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CUSTODY = Namespace("https://cacontology.projectvic.org/custodial#")
CORE = Namespace("https://cacontology.projectvic.org/core#")
GUFO = Namespace("http://purl.org/nemo/gufo#")


class CustodyAxiomTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ontology = Graph().parse(REPO / "ontology" / "cacontology-custodial.ttl", format="turtle")

    def test_relationship_and_arrangement_classes_are_not_phases(self):
        for term in (CUSTODY.TemporaryCustody, CUSTODY.EmergencyCustody):
            self.assertNotIn((term, RDFS.subClassOf, CORE.Phase), self.ontology)
            self.assertNotIn((term, RDF.type, GUFO.Phase), self.ontology)

    def test_state_classes_have_only_the_state_root(self):
        for term in (
            CUSTODY.ActiveCustodyPhase, CUSTODY.SuspendedCustodyPhase,
            CUSTODY.TerminatedCustodyPhase, CUSTODY.ProbationaryCustodyPhase,
        ):
            self.assertIn((term, RDFS.subClassOf, CUSTODY.CustodyState), self.ontology)
            self.assertNotIn((term, RDFS.subClassOf, CUSTODY.CustodialRelationship), self.ontology)
            self.assertNotIn((term, RDF.type, GUFO.Phase), self.ontology)

    def test_rhode_island_temporary_custody_nodes_do_not_infer_phase(self):
        graph = Graph()
        graph.parse(REPO / "ontology" / "cacontology-core-spine.ttl", format="turtle")
        graph.parse(REPO / "ontology" / "cacontology-custodial.ttl", format="turtle")
        graph.parse(REPO / "examples_knowledge_graphs" / "rhode-island-production-case.ttl", format="turtle")
        DeductiveClosure(RDFS_Semantics).expand(graph)
        example = Namespace("http://example.org/rhode-island-case#")
        for node in (
            example.CustodialRelationship001,
            example.CustodialRelationship002,
        ):
            self.assertIn((node, RDF.type, CUSTODY.TemporaryCustody), graph)
            self.assertNotIn((node, RDF.type, CORE.Phase), graph)


class CustodyShapeTests(unittest.TestCase):
    def validate_fixture(self, name: str) -> bool:
        data = Graph().parse(HERE / "fixtures" / name, format="turtle")
        shapes = Graph().parse(REPO / "ontology" / "cacontology-custodial-shapes.ttl", format="turtle")
        conforms, _, _ = validate(data, shacl_graph=shapes, inference="none", allow_warnings=True)
        return conforms

    def test_positive_history_conforms(self):
        self.assertTrue(self.validate_fixture("positive-custody-history.ttl"))

    def test_relationship_state_overlap_fails(self):
        self.assertFalse(self.validate_fixture("negative-custody-overlap.ttl"))


if __name__ == "__main__":
    unittest.main()
