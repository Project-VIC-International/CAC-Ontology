#!/usr/bin/env python3
"""Regression controls for bounded vocabulary closure in Gate 4.1."""

import hashlib
import json
from pathlib import Path
import unittest

from rdflib import Graph, Literal, Namespace, OWL, RDF


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
ONTOLOGY = REPO / "ontology"
STANDARDS_FILE = ONTOLOGY / "cacontology-standards-profile.ttl"
ANNOTATION_FILE = ONTOLOGY / "cacontology-gufo-annotation-vocabulary.ttl"
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DCTERMS = Namespace("http://purl.org/dc/terms/")
CAC_GUFO = Namespace("https://cacontology.projectvic.org/gufo#")
COMPAT = Namespace("https://cacontology.projectvic.org/compatibility#")


class Gate41VocabularyPolicyTests(unittest.TestCase):
    def test_bounded_external_term_kinds_are_exact(self):
        graph = Graph().parse(STANDARDS_FILE, format="turtle")
        for term in (SKOS.Concept, SKOS.ConceptScheme):
            self.assertIn((term, RDF.type, OWL.Class), graph)
        for term in (
            SKOS.altLabel,
            SKOS.definition,
            SKOS.editorialNote,
            SKOS.prefLabel,
            SKOS.scopeNote,
            DCTERMS.creator,
            DCTERMS.description,
            DCTERMS.isReplacedBy,
            DCTERMS.issued,
            DCTERMS.source,
            DCTERMS.title,
        ):
            with self.subTest(term=term):
                self.assertIn((term, RDF.type, OWL.AnnotationProperty), graph)
        for term in (SKOS.exactMatch, SKOS.inScheme):
            self.assertIn((term, RDF.type, OWL.ObjectProperty), graph)

    def test_first_party_annotation_properties_have_one_owner(self):
        expected = {
            CAC_GUFO.hasAntiRigidityConstraint,
            CAC_GUFO.hasRelationshipConstraint,
            CAC_GUFO.hasTemporalProperty,
            CAC_GUFO.hasValidationConstraint,
            CAC_GUFO.involvesSituation,
            CAC_GUFO.temporalConstraint,
        }
        owner = Graph().parse(ANNOTATION_FILE, format="turtle")
        self.assertEqual(expected, set(owner.subjects(RDF.type, OWL.AnnotationProperty)))
        for term in expected:
            declaring_files = []
            for path in ONTOLOGY.glob("*.ttl"):
                graph = Graph().parse(path, format="turtle")
                if (term, RDF.type, OWL.AnnotationProperty) in graph:
                    declaring_files.append(path.name)
            self.assertEqual([ANNOTATION_FILE.name], declaring_files)

    def test_skos_object_properties_never_receive_literals(self):
        graph = Graph()
        for path in ONTOLOGY.glob("*.ttl"):
            graph.parse(path, format="turtle")
        exact_matches = list(graph.triples((None, SKOS.exactMatch, None)))
        self.assertEqual(3, len(exact_matches))
        self.assertTrue(all(not isinstance(value, Literal) for _, _, value in exact_matches))
        self.assertTrue(
            all(not isinstance(value, Literal) for value in graph.objects(None, SKOS.inScheme))
        )

    def test_compatibility_notices_are_named_individuals(self):
        graph = Graph().parse(ONTOLOGY / "cacontology-v3-compatibility.ttl", format="turtle")
        for notice in (COMPAT.CustodyPropertyMigration, COMPAT.RolePhaseMigration):
            self.assertIn((notice, RDF.type, OWL.NamedIndividual), graph)

    def test_authoritative_reference_bytes_are_hash_locked(self):
        expected = {
            "testing/v4/dependencies/standards/skos-2009-08-18.rdf":
                "e79633b8d0564816cee8a99f5c9acf9a0e6fc7257c7209acd684ecad53a89dd6",
            "testing/v4/dependencies/standards/dublin-core-terms-2012-06-14.ttl":
                "13df401072dd7015bf9d75162f3e41c8138075304b7b9cc1aa1e9c16db976797",
        }
        lock = json.loads((HERE / "dependency-lock.json").read_text(encoding="utf-8"))
        records = {record["path"]: record for record in lock["dependency_files"]}
        for relative, digest in expected.items():
            path = REPO / relative
            with self.subTest(path=relative):
                self.assertEqual(digest, hashlib.sha256(path.read_bytes()).hexdigest())
                self.assertEqual(digest, records[relative]["sha256"])
                self.assertEqual("resolved-vendored", records[relative]["status"])


if __name__ == "__main__":
    unittest.main()
