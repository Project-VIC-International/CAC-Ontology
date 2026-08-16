#!/usr/bin/env python3
"""SHACL and axiom tests for the v4 core role/phase split."""

from pathlib import Path
import unittest

from pyshacl import validate
from rdflib import Graph, Namespace, RDFS

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CORE = Namespace("https://cacontology.projectvic.org/core#")
GUFO = Namespace("http://purl.org/nemo/gufo#")


def shapes() -> Graph:
    graph = Graph()
    graph.parse(REPO / "ontology" / "cacontology-core-spine-shapes.ttl", format="turtle")
    graph.parse(REPO / "ontology" / "cacontology-v4-foundation-shapes.ttl", format="turtle")
    return graph


def conforms(*names: str) -> bool:
    data = Graph()
    for name in names:
        data.parse(HERE / "fixtures" / name, format="turtle")
    result, _, _ = validate(
        data,
        shacl_graph=shapes(),
        inference="none",
        abort_on_first=False,
        allow_infos=True,
        allow_warnings=True,
    )
    return result


class CoreAxiomTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = Graph().parse(REPO / "ontology" / "cacontology-core-spine.ttl", format="turtle")

    def test_operational_role_is_not_a_gufo_classifier_subclass(self):
        self.assertNotIn((CORE.Role, RDFS.subClassOf, GUFO.Role), self.graph)

    def test_operational_phase_is_a_situation_not_gufo_phase_subclass(self):
        self.assertIn((CORE.Phase, RDFS.subClassOf, CORE.Situation), self.graph)
        self.assertNotIn((CORE.Phase, RDFS.subClassOf, GUFO.Phase), self.graph)

    def test_role_assignment_uses_temporary_instantiation_situation(self):
        self.assertIn((CORE.RoleAssignment, RDFS.subClassOf, GUFO.TemporaryInstantiationSituation), self.graph)
        self.assertNotIn((CORE.roleBearer, RDFS.subPropertyOf, GUFO.concernsTemporaryWhole), self.graph)
        self.assertIn((CORE.roleClassifier, RDFS.subPropertyOf, GUFO.concernsNonRigidType), self.graph)


class CoreProfileTests(unittest.TestCase):
    def test_positive_role_assignment_conforms(self):
        self.assertTrue(conforms("positive-role-assignment.ttl"))

    def test_invalid_assignment_classifier_mixing_fails(self):
        self.assertFalse(conforms("negative-role-level-mixing.ttl"))

    def test_positive_revisited_phase_occurrences_conform(self):
        self.assertTrue(conforms("positive-phase-occurrences.ttl"))

    def test_invalid_phase_classifier_mixing_fails(self):
        self.assertFalse(conforms("negative-phase-level-mixing.ttl"))

    def test_invalid_phase_precedence_cycle_fails(self):
        self.assertFalse(conforms("negative-phase-cycle.ttl"))


if __name__ == "__main__":
    unittest.main()
