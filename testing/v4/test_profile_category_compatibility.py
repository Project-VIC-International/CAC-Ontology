#!/usr/bin/env python3
"""Prevent exact-profile Endurant/Event/Situation category collisions."""

from pathlib import Path
import unittest

from rdflib import Graph, Namespace, RDF, RDFS

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CORE = Namespace("https://cacontology.projectvic.org/core#")
GUFO = Namespace("http://purl.org/nemo/gufo#")
UCO_OBSERVABLE = Namespace("https://ontology.unifiedcyberontology.org/uco/observable/")
HOTLINES = Namespace("https://cacontology.projectvic.org/hotlines#")
INSTITUTIONAL = Namespace("https://cacontology.projectvic.org/institutional-exploitation#")
PRODUCTION = Namespace("https://cacontology.projectvic.org/production#")
TASKFORCE = Namespace("https://cacontology.projectvic.org/taskforce#")
IMPACT = Namespace("https://cacontology.projectvic.org/victim-impact#")


class ProfileCategoryCompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = Graph()
        for name in (
            "cacontology-hotlines.ttl",
            "cacontology-institutional-exploitation.ttl",
            "cacontology-production.ttl",
            "cacontology-taskforce.ttl",
            "cacontology-victim-impact.ttl",
        ):
            cls.graph.parse(REPO / "ontology" / name, format="turtle")

    def test_report_and_evidence_concepts_are_artifacts(self):
        for term in (
            HOTLINES.HotlineReport,
            INSTITUTIONAL.MultipleVictimTestimony,
            INSTITUTIONAL.InstitutionalAbuseEvidence,
        ):
            with self.subTest(term=term):
                self.assertIn((term, RDFS.subClassOf, CORE.Artifact), self.graph)
                self.assertNotIn((term, RDFS.subClassOf, CORE.Situation), self.graph)
        self.assertNotIn(
            (HOTLINES.HotlineReport, RDFS.subClassOf, UCO_OBSERVABLE.Observation),
            self.graph,
        )

    def test_situations_do_not_also_specialize_observable_object(self):
        for term in (
            INSTITUTIONAL.ForeignCommerceOffense,
            PRODUCTION.ProductionSession,
            PRODUCTION.ExtendedProductionPeriod,
            TASKFORCE.ResourceSharing,
            TASKFORCE.CoordinationMechanism,
            IMPACT.RecoveryProcess,
            IMPACT.LongTermEffect,
        ):
            with self.subTest(term=term):
                self.assertIn((term, RDFS.subClassOf, CORE.Situation), self.graph)
                self.assertNotIn(
                    (term, RDFS.subClassOf, UCO_OBSERVABLE.ObservableObject),
                    self.graph,
                )

    def test_artifact_stereotypes_are_not_situation_types(self):
        for term in (
            INSTITUTIONAL.MultipleVictimTestimony,
            INSTITUTIONAL.AdultVictimTestimony,
            INSTITUTIONAL.InstitutionalAbuseEvidence,
            INSTITUTIONAL.LongTermAbusePattern,
        ):
            with self.subTest(term=term):
                self.assertIn((term, RDF.type, GUFO.Kind), self.graph)
                self.assertNotIn((term, RDF.type, GUFO.SituationType), self.graph)


if __name__ == "__main__":
    unittest.main()
