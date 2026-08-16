#!/usr/bin/env python3
"""Regression controls for REM-014 strict-profile decomposition."""

from __future__ import annotations

import unittest

import decompose_owl2dl_profile as decomposition
from rdflib import Graph, OWL, RDF, RDFS, URIRef


class Rem014DecompositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = decomposition.build()

    def test_multiline_annotation_text_is_not_counted_as_a_violation(self):
        for name in ("C3", "C5"):
            configuration = self.report["configurations"][name]
            self.assertEqual(
                configuration["violation_count"],
                sum(configuration["by_category"].values()),
            )
            self.assertLessEqual(
                configuration["violation_count"],
                decomposition.REM014_BASELINE[name]["violation_count"],
            )

    def test_compatibility_layer_adds_no_strict_profile_findings(self):
        c3 = self.report["configurations"]["C3"]
        c5 = self.report["configurations"]["C5"]
        self.assertEqual(0, c5["violation_count"] - c3["violation_count"])
        self.assertNotIn(
            "reserved-owl-vocabulary-as-domain-or-range",
            c5["by_root_cause"],
        )

    def test_completed_high_confidence_roots_leave_the_priority_queue(self):
        roots = self.report["configurations"]["C3"]["by_root_cause"]
        self.assertNotIn(
            "single-operand-equivalence",
            roots,
        )
        self.assertEqual(2, roots.get("property-kind-punning", 0))
        self.assertNotIn("class-used-as-datatype", roots)
        self.assertNotIn("missing-local-declaration", roots)

    def test_no_first_party_profile_findings_remain(self):
        c3 = self.report["configurations"]["C3"]
        self.assertEqual(0, c3["by_owner"].get("cac", 0))
        self.assertNotIn("cac", c3["by_owner_and_root_cause"])
        self.assertNotIn("invalid-or-version-mismatched-external-reference", c3["by_root_cause"])
        self.assertNotIn("unsupported-xsd-datatype-policy", c3["by_root_cause"])
        self.assertNotIn("unimported-shared-vocabulary", c3["by_root_cause"])

    def test_priority_queue_puts_cac_work_before_external_findings(self):
        units = self.report["priority_units"]
        first_external = next(
            (index for index, unit in enumerate(units) if unit["scope"] == "external"),
            len(units),
        )
        self.assertTrue(all(unit["scope"] == "cac-actionable" for unit in units[:first_external]))
        self.assertTrue(all(unit["scope"] == "external" for unit in units[first_external:]))
        self.assertEqual(0, next(unit for unit in units if unit["root_cause"] == "property-kind-punning")["priority_score"])

    def test_remediation_reduces_only_cac_owned_findings(self):
        c3 = self.report["configurations"]["C3"]
        self.assertEqual(-831, self.report["delta_from_baseline"]["C3"])
        self.assertEqual(
            self.report["delta_from_baseline"]["C3"],
            (
                c3["by_owner"].get("cac", 0)
                - decomposition.REM014_BASELINE["C3"]["cac_owned_count"]
            )
            + (
                c3["by_owner"].get("shared-or-unattributed", 0)
                - decomposition.REM014_BASELINE["C3"]["shared_or_unattributed_count"]
            ),
        )
        self.assertEqual(
            decomposition.REM014_BASELINE["C3"]["upstream_owned_count"],
            c3["by_owner"]["upstream"],
        )
        self.assertEqual(
            0,
            c3["by_owner"].get("shared-or-unattributed", 0),
        )

    def test_object_property_targets_have_explicit_class_declarations(self):
        educational = Graph().parse(
            decomposition.REPO / "ontology" / "cacontology-educational-exploitation.ttl",
            format="turtle",
        )
        taskforce = Graph().parse(
            decomposition.REPO / "ontology" / "cacontology-taskforce.ttl",
            format="turtle",
        )
        targets = {
            educational: (
                "https://cacontology.projectvic.org/educational#PhysicalContactPattern",
                "https://cacontology.projectvic.org/educational#VictimDisclosureToStaff",
                "https://cacontology.projectvic.org/educational#PrincipalNotification",
                "https://cacontology.projectvic.org/educational#PoliceNotification",
                "https://cacontology.projectvic.org/educational#AgeDeception",
                "https://cacontology.projectvic.org/educational#MultipleAccountDeception",
            ),
            taskforce: (
                "https://cacontology.projectvic.org/taskforce#TaskForceTraining",
            ),
        }
        for graph, iris in targets.items():
            for iri in iris:
                self.assertIn((URIRef(iri), RDF.type, OWL.Class), graph)

    def test_integration_pattern_metamodeling_is_dl_safe(self):
        graph = Graph().parse(
            decomposition.REPO / "ontology" / "cacontology-integration-patterns.ttl",
            format="turtle",
        )
        base = "https://cacontology.projectvic.org/integration-patterns#"
        integration_pattern = URIRef(base + "IntegrationPattern")
        properties = tuple(
            URIRef(base + name)
            for name in (
                "hasIntegrationPattern",
                "requiresValidation",
                "dependsOnPattern",
                "extendsPattern",
            )
        )
        self.assertIn((integration_pattern, RDF.type, OWL.Class), graph)
        for property_iri in properties:
            self.assertNotIn((property_iri, RDFS.domain, OWL.Class), graph)
            self.assertNotIn((property_iri, RDFS.range, OWL.Class), graph)

        pattern_nodes = set(graph.objects(None, properties[0]))
        for property_iri in properties[1:]:
            pattern_nodes.update(graph.subjects(property_iri, None))
            if property_iri != properties[1]:
                pattern_nodes.update(graph.objects(None, property_iri))
        self.assertTrue(pattern_nodes)
        for node in pattern_nodes:
            self.assertIn((node, RDF.type, OWL.Class), graph)
            self.assertIn((node, RDF.type, integration_pattern), graph)

    def test_no_class_is_declared_equivalent_only_to_itself(self):
        graph = Graph().parse(
            decomposition.REPO / "ontology" / "cacontology-usa-federal-law.ttl",
            format="turtle",
        )
        self.assertEqual([], sorted(str(subject) for subject, _, value in graph.triples((None, OWL.equivalentClass, None)) if subject == value))


if __name__ == "__main__":
    unittest.main()
