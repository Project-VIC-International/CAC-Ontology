#!/usr/bin/env python3
"""Regression controls for the approved Gate 4.1 datatype policy."""

from collections import Counter
from pathlib import Path
import unittest

from pyshacl import validate
from rdflib import Graph, Namespace, RDFS, SH, URIRef, XSD


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
ONTOLOGY = REPO / "ontology"
EXAMPLES = REPO / "examples_knowledge_graphs"
POLICY = Namespace("https://cacontology.projectvic.org/datatype-policy#")
INTEGRATION = Namespace("https://cacontology.projectvic.org/integration-patterns#")


class Gate41DatatypePolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ontology = Graph()
        for path in sorted(ONTOLOGY.glob("*.ttl")):
            cls.ontology.parse(path, format="turtle")
        cls.shapes = Graph().parse(
            ONTOLOGY / "cacontology-datatype-policy-shapes.ttl", format="turtle"
        )

    def test_unsupported_duration_and_gyear_terms_are_absent(self):
        for directory in (ONTOLOGY, EXAMPLES):
            for path in directory.glob("*.ttl"):
                text = path.read_text(encoding="utf-8")
                with self.subTest(path=path.name):
                    self.assertNotIn("xsd:duration", text)
                    self.assertNotIn("xsd:gYear", text)

    def test_every_duration_property_is_a_string_and_is_targeted_once(self):
        duration_shape = POLICY.CanonicalDurationLexicalShape
        targets = set(self.shapes.objects(duration_shape, SH.targetObjectsOf))
        self.assertEqual(50, len(targets))
        for property_iri in targets:
            with self.subTest(property=property_iri):
                self.assertIn((property_iri, RDFS.range, XSD.string), self.ontology)

    def test_all_four_year_properties_are_integer_and_bounded(self):
        year_shape = POLICY.FourDigitCivilYearShape
        targets = set(self.shapes.objects(year_shape, SH.targetObjectsOf))
        self.assertEqual(4, len(targets))
        for property_iri in targets:
            with self.subTest(property=property_iri):
                self.assertIn((property_iri, RDFS.range, XSD.integer), self.ontology)

    def test_integration_duration_lexical_values_are_preserved(self):
        values = Counter(
            str(value)
            for value in self.ontology.objects(
                None, INTEGRATION.hasIntegrationTimeline
            )
        )
        self.assertEqual(
            Counter(
                {
                    "P30D": 6,
                    "P45D": 4,
                    "P90D": 1,
                    "P120D": 1,
                    "P135D": 1,
                    "P345D": 1,
                }
            ),
            values,
        )
        for value in self.ontology.objects(None, INTEGRATION.hasIntegrationTimeline):
            self.assertIn(value.datatype, (None, XSD.string))

    def test_reusable_shapes_accept_canonical_values_and_reject_bad_values(self):
        positive = Graph().parse(HERE / "fixtures" / "positive-datatype-policy.ttl", format="turtle")
        negative = Graph().parse(HERE / "fixtures" / "negative-datatype-policy.ttl", format="turtle")
        positive_conforms, _, positive_report = validate(
            data_graph=positive, shacl_graph=self.shapes, inference="none", advanced=True
        )
        negative_conforms, _, _ = validate(
            data_graph=negative, shacl_graph=self.shapes, inference="none", advanced=True
        )
        self.assertTrue(positive_conforms, str(positive_report))
        self.assertFalse(negative_conforms)


if __name__ == "__main__":
    unittest.main()
