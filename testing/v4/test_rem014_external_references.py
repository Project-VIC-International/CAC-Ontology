#!/usr/bin/env python3
"""Regression controls for pinned-vocabulary repairs in REM-014."""

from __future__ import annotations

from pathlib import Path
import re
import unittest

from rdflib import Graph, Namespace, OWL, RDF


REPOSITORY = Path(__file__).resolve().parents[2]
ONTOLOGY = REPOSITORY / "ontology"
GUFO = Namespace("http://purl.org/nemo/gufo#")
UCO_OBSERVABLE = Namespace("https://ontology.unifiedcyberontology.org/uco/observable/")
UCO_ROLE = Namespace("https://ontology.unifiedcyberontology.org/uco/role/")
UCO_TYPES = Namespace("https://ontology.unifiedcyberontology.org/uco/types/")
PINNED_UCO = (
    REPOSITORY
    / "testing"
    / "v4"
    / "dependencies"
    / "uco-gufo-profile"
    / "4b98b9881aa29ed80f39b589d15725fa696c921a"
    / "dependencies"
    / "UCO"
    / "ontology"
    / "uco"
)
PINNED_GUFO = (
    REPOSITORY
    / "testing"
    / "v4"
    / "dependencies"
    / "uco-gufo-profile"
    / "4b98b9881aa29ed80f39b589d15725fa696c921a"
    / "dependencies"
    / "CDO-Shapes-gufo"
    / "dependencies"
    / "formatted-gufo.ttl"
)

QUALITY_REFERENCE_FILES = (
    "cacontology-extremist-enterprises-shapes.ttl",
    "cacontology-investigation-coordination.ttl",
    "cacontology-law-enforcement-corruption.ttl",
    "cacontology-legal-harmonization.ttl",
)


class Rem014ExternalReferenceTests(unittest.TestCase):
    def test_quality_properties_use_the_pinned_gufo_term(self):
        obsolete = re.compile(r"\bgufo:hasQuality\b")
        successor = re.compile(r"\bgufo:hasQualityValue\b")
        successor_count = 0

        for filename in QUALITY_REFERENCE_FILES:
            with self.subTest(filename=filename):
                text = (ONTOLOGY / filename).read_text(encoding="utf-8")
                self.assertIsNone(obsolete.search(text))
                successor_count += len(successor.findall(text))

        self.assertEqual(52, successor_count)

    def test_quality_value_superproperty_exists_in_pinned_gufo(self):
        graph = Graph().parse(PINNED_GUFO, format="turtle")
        self.assertIn((GUFO.hasQualityValue, RDF.type, OWL.DatatypeProperty), graph)
        self.assertNotIn((GUFO.hasQuality, RDF.type, OWL.DatatypeProperty), graph)

    def test_relocated_uco_classes_exist_in_their_pinned_modules(self):
        modules = {
            PINNED_UCO / "observable" / "observable.ttl": {
                UCO_OBSERVABLE.Observable,
                UCO_OBSERVABLE.Software,
            },
            PINNED_UCO / "role" / "role.ttl": {UCO_ROLE.Role},
            PINNED_UCO / "types" / "types.ttl": {UCO_TYPES.Hash},
        }
        for path, expected_classes in modules.items():
            with self.subTest(path=path):
                graph = Graph().parse(path, format="turtle")
                for class_iri in expected_classes:
                    self.assertIn((class_iri, RDF.type, OWL.Class), graph)

    def test_obsolete_uco_namespaces_are_absent_from_first_party_turtle(self):
        obsolete_terms = {
            "uco-core:Observable",
            "uco-core:Role",
            "uco-identity:Software",
            "uco-observable:Hash",
        }
        for path in ONTOLOGY.glob("*.ttl"):
            text = path.read_text(encoding="utf-8")
            for term in obsolete_terms:
                with self.subTest(path=path.name, term=term):
                    self.assertNotIn(term, text)


if __name__ == "__main__":
    unittest.main()
