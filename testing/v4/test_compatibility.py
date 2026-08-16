#!/usr/bin/env python3
"""Safety controls for the bounded v3-to-v4 compatibility proposal."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

from owlrl import DeductiveClosure, OWLRL_Semantics
from rdflib import Graph, Namespace, OWL, RDFS


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
COMPAT = REPO / "ontology" / "cacontology-v3-compatibility.ttl"
SPEC = importlib.util.spec_from_file_location(
    "architecture_audit", HERE / "architecture_audit.py"
)
AUDIT = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(AUDIT)

CAC_CUSTODY = Namespace("https://cacontology.projectvic.org/custodial#")


class CompatibilitySafetyControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.compat = Graph().parse(COMPAT, format="turtle")

    def test_only_one_way_safe_property_bridges_are_present(self):
        self.assertIn(
            (CAC_CUSTODY.inCustodyPhase, RDFS.subPropertyOf, CAC_CUSTODY.currentCustodyState),
            self.compat,
        )
        self.assertIn(
            (CAC_CUSTODY.hasCustodyPhase, RDFS.subPropertyOf, CAC_CUSTODY.hasCustodyState),
            self.compat,
        )
        self.assertEqual([], list(self.compat.triples((None, OWL.equivalentClass, None))))
        self.assertEqual([], list(self.compat.triples((None, OWL.equivalentProperty, None))))
        self.assertEqual([], list(self.compat.triples((None, RDFS.subClassOf, None))))

    def test_compatibility_closure_does_not_restore_architecture_conflicts(self):
        graph = Graph()
        for name in (
            "cacontology-core-spine.ttl",
            "cacontology-custodial.ttl",
            "cacontology-extremist-enterprises.ttl",
            "cacontology-v3-compatibility.ttl",
        ):
            graph.parse(REPO / "ontology" / name, format="turtle")
        DeductiveClosure(OWLRL_Semantics).expand(graph)
        findings = AUDIT.audit_graph(graph)["diagnostics"]
        self.assertTrue(all(not values for values in findings.values()))


if __name__ == "__main__":
    unittest.main()
