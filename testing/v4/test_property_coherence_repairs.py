#!/usr/bin/env python3
"""Lock the Gate 4 repairs for properties made bottom by imported semantics."""

from pathlib import Path
import unittest

from rdflib import Graph, Namespace, OWL, RDF, RDFS

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
GUFO = Namespace("http://purl.org/nemo/gufo#")
CORE = Namespace("https://cacontology.projectvic.org/core#")
TEMPORAL = Namespace("https://cacontology.projectvic.org/temporal#")
LEGAL = Namespace("https://cacontology.projectvic.org/legal-harmonization#")
INSTITUTIONAL = Namespace("https://cacontology.projectvic.org/institutional-exploitation#")
CUSTODIAL = Namespace("https://cacontology.projectvic.org/custodial#")
CORRUPTION = Namespace("https://cacontology.projectvic.org/law-enforcement-corruption#")
COORDINATION = Namespace("https://cacontology.projectvic.org/investigation-coordination#")
FEDERAL = Namespace("https://cacontology.projectvic.org/usa-federal-law#")
ENTERPRISES = Namespace("https://cacontology.projectvic.org/extremist-enterprises#")


class PropertyCoherenceRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = Graph()
        for name in (
            "cacontology-legal-harmonization.ttl",
            "cacontology-institutional-exploitation.ttl",
            "cacontology-custodial.ttl",
            "cacontology-law-enforcement-corruption.ttl",
            "cacontology-investigation-coordination.ttl",
            "cacontology-usa-federal-law.ttl",
            "cacontology-temporal.ttl",
        ):
            cls.graph.parse(REPO / "ontology" / name, format="turtle")

    def test_non_participation_relations_do_not_specialize_participated_in(self):
        for term in (
            LEGAL.isAssessedBy,
            INSTITUTIONAL.participatesInInstitution,
            INSTITUTIONAL.experiencesExploitation,
            CUSTODIAL.occursInCustodialSituation,
            CORRUPTION.isDetectedBy,
        ):
            with self.subTest(term=term):
                self.assertNotIn((term, RDFS.subPropertyOf, GUFO.participatedIn), self.graph)

    def test_event_to_participant_uses_inverse_participation(self):
        inverse_nodes = set(self.graph.subjects(OWL.inverseOf, GUFO.participatedIn))
        self.assertTrue(
            any(
                (CUSTODIAL.perpetratedBy, RDFS.subPropertyOf, node) in self.graph
                for node in inverse_nodes
            )
        )

    def test_enduring_custodial_associations_are_not_event_participation(self):
        for term in (
            CUSTODIAL.involvesCustodian,
            CUSTODIAL.involvesChild,
            CUSTODIAL.involvesParent,
        ):
            with self.subTest(term=term):
                self.assertNotIn((term, RDFS.subPropertyOf, GUFO.participatedIn), self.graph)

    def test_enterprise_members_are_inverse_functional_components(self):
        graph = Graph().parse(
            REPO / "ontology" / "cacontology-extremist-enterprises.ttl",
            format="turtle",
        )
        inverse_nodes = set(graph.subjects(OWL.inverseOf, GUFO.isComponentOf))
        self.assertTrue(
            any(
                (ENTERPRISES.hasMember, RDFS.subPropertyOf, node) in graph
                for node in inverse_nodes
            )
        )
        self.assertNotIn(
            (ENTERPRISES.hasMember, RDFS.subPropertyOf, GUFO.isCollectionMemberOf),
            graph,
        )

    def test_coordination_legacy_component_name_has_participation_semantics(self):
        self.assertIn(
            (COORDINATION.isComponentOf, RDFS.subPropertyOf, GUFO.participatedIn),
            self.graph,
        )
        self.assertNotIn(
            (COORDINATION.isComponentOf, RDFS.subPropertyOf, GUFO.isComponentOf),
            self.graph,
        )

    def test_legal_phases_use_cac_lifecycle_relations(self):
        self.assertIn((FEDERAL.hasLegalPhase, RDFS.subPropertyOf, CORE.hasPhase), self.graph)
        self.assertIn((FEDERAL.isPhaseOf, RDFS.subPropertyOf, CORE.isPhaseOf), self.graph)
        self.assertNotIn(
            (FEDERAL.isPhaseOf, RDFS.subPropertyOf, GUFO.isObjectProperPartOf),
            self.graph,
        )

    def test_age_is_a_quality_type_not_the_property_value_class(self):
        self.assertIn((TEMPORAL.Age, RDF.type, GUFO.Kind), self.graph)
        self.assertIn(
            (TEMPORAL.concernsAgeQuality, RDFS.range, GUFO.EndurantType), self.graph
        )
        self.assertNotIn(
            (TEMPORAL.concernsAgeQuality, RDFS.range, TEMPORAL.Age), self.graph
        )


if __name__ == "__main__":
    unittest.main()
