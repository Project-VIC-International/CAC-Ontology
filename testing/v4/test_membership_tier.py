#!/usr/bin/env python3
"""Tests for controlled-concept MembershipTier semantics."""

from pathlib import Path
import unittest

from owlrl import DeductiveClosure, RDFS_Semantics
from pyshacl import validate
from rdflib import Graph, Namespace, RDF, RDFS

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
ENTERPRISES = Namespace("https://cacontology.projectvic.org/extremist-enterprises#")
CORE = Namespace("https://cacontology.projectvic.org/core#")
GUFO = Namespace("http://purl.org/nemo/gufo#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
EXAMPLE = Namespace("https://example.org/kb/")


class MembershipTierAxiomTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ontology = Graph().parse(REPO / "ontology" / "cacontology-extremist-enterprises.ttl", format="turtle")

    def test_membership_tier_is_only_a_controlled_concept(self):
        self.assertIn((ENTERPRISES.MembershipTier, RDFS.subClassOf, SKOS.Concept), self.ontology)
        self.assertNotIn((ENTERPRISES.MembershipTier, RDFS.subClassOf, ENTERPRISES.EnterpriseHierarchy), self.ontology)
        self.assertNotIn((ENTERPRISES.MembershipTier, RDFS.subClassOf, CORE.Phase), self.ontology)
        self.assertNotIn((ENTERPRISES.MembershipTier, RDF.type, GUFO.Phase), self.ontology)

    def test_access_level_does_not_force_tiers_to_be_access_control_systems(self):
        graph = Graph()
        graph += self.ontology
        graph.parse(REPO / "examples_knowledge_graphs" / "764-network-extremist-enterprise-example.ttl", format="turtle")
        DeductiveClosure(RDFS_Semantics).expand(graph)
        for tier in (EXAMPLE.membership_tier_leader, EXAMPLE.membership_tier_inner_core):
            self.assertIn((tier, RDF.type, ENTERPRISES.MembershipTier), graph)
            self.assertNotIn((tier, RDF.type, ENTERPRISES.AccessControlSystem), graph)
            self.assertNotIn((tier, RDF.type, ENTERPRISES.EnterpriseHierarchy), graph)
            self.assertNotIn((tier, RDF.type, CORE.Phase), graph)


class MembershipTierShapeTests(unittest.TestCase):
    def validate_fixture(self, name: str) -> bool:
        data = Graph().parse(HERE / "fixtures" / name, format="turtle")
        shapes = Graph().parse(REPO / "ontology" / "cacontology-extremist-enterprises-shapes.ttl", format="turtle")
        conforms, _, _ = validate(data, shacl_graph=shapes, inference="none", allow_warnings=True)
        return conforms

    def test_positive_tier_reference_conforms(self):
        self.assertTrue(self.validate_fixture("positive-membership-tier.ttl"))

    def test_level_mixing_fails(self):
        self.assertFalse(self.validate_fixture("negative-membership-tier-level-mixing.ttl"))


if __name__ == "__main__":
    unittest.main()
