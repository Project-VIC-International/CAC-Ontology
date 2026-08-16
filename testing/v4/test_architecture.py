#!/usr/bin/env python3
"""Unit controls proving that architecture diagnostics are not self-silencing."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

from rdflib import Graph, Namespace

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("architecture_audit", HERE / "architecture_audit.py")
AUDIT = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(AUDIT)


def graph(text: str) -> Graph:
    value = Graph()
    value.parse(data=text, format="turtle")
    return value


PREFIXES = """
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix gufo: <http://purl.org/nemo/gufo#> .
@prefix cac-core: <https://cacontology.projectvic.org/core#> .
@prefix ex: <https://example.invalid/v4-test#> .
"""


class DiagnosticControls(unittest.TestCase):
    def test_ignores_the_owl_bottom_class_in_closed_graphs(self):
        candidate = graph(PREFIXES + """
            owl:Nothing a owl:Class ;
                rdfs:subClassOf cac-core:Role, cac-core:Phase,
                    cac-core:EnduringEntity, cac-core:Event .
        """)
        findings = AUDIT.audit_graph(candidate)["diagnostics"]
        self.assertTrue(all(not values for values in findings.values()))

    def test_detects_operational_classifier_conflation_and_overlap(self):
        candidate = graph(PREFIXES + """
            cac-core:Role a owl:Class ; rdfs:subClassOf gufo:Role .
            cac-core:Phase a owl:Class ; rdfs:subClassOf gufo:Phase .
            cac-core:EnduringEntity a owl:Class .
            ex:BadRole a owl:Class, gufo:Role ;
                rdfs:subClassOf cac-core:Role, cac-core:EnduringEntity .
            ex:BadPhase a owl:Class, gufo:Phase ;
                rdfs:subClassOf cac-core:Phase, cac-core:EnduringEntity .
            cac-core:Event a owl:Class .
            ex:BadEventPhase a owl:Class ; rdfs:subClassOf cac-core:Phase, cac-core:Event .
        """)
        findings = AUDIT.audit_graph(candidate)["diagnostics"]
        self.assertEqual(1, len(findings["META001_OPERATIONAL_ROLE_AS_GUFO_CLASSIFIER"]))
        self.assertEqual(1, len(findings["META002_OPERATIONAL_PHASE_AS_GUFO_CLASSIFIER"]))
        self.assertEqual(1, len(findings["META003_ENDURING_PHASE_OVERLAP"]))
        self.assertEqual(1, len(findings["META004_CORE_ROLE_SUBCLASSES_GUFO_ROLE"]))
        self.assertEqual(1, len(findings["META005_CORE_PHASE_SUBCLASSES_GUFO_PHASE"]))
        self.assertEqual(1, len(findings["META008_OPERATIONAL_ROLE_ENDURING_OVERLAP"]))
        self.assertEqual(1, len(findings["META010_OPERATIONAL_PHASE_EVENT_OVERLAP"]))

    def test_accepts_separated_record_assignment_occurrence_classifier_pattern(self):
        candidate = graph(PREFIXES + """
            cac-core:Entity a owl:Class .
            cac-core:EnduringEntity a owl:Class ; rdfs:subClassOf cac-core:Entity .
            cac-core:Situation a owl:Class ; rdfs:subClassOf cac-core:Entity, gufo:Situation .
            cac-core:Role a owl:Class ; rdfs:subClassOf cac-core:Entity .
            cac-core:RoleRecord a owl:Class ; rdfs:subClassOf cac-core:Role .
            cac-core:RoleAssignment a owl:Class ; rdfs:subClassOf cac-core:Situation .
            cac-core:Phase a owl:Class ; rdfs:subClassOf cac-core:Situation .
            ex:VictimRoleClassifier a owl:Class, gufo:Role .
            ex:MinorPhaseClassifier a owl:Class, gufo:Phase ;
                rdfs:subClassOf cac-core:EnduringEntity .
        """)
        findings = AUDIT.audit_graph(candidate)["diagnostics"]
        self.assertTrue(all(not values for values in findings.values()))

    def test_detects_assignment_and_occurrence_level_mixing(self):
        candidate = graph(PREFIXES + """
            ex:badAssignment a cac-core:RoleAssignment, gufo:Role .
            ex:badOccurrence a cac-core:Phase, gufo:Phase .
        """)
        findings = AUDIT.audit_graph(candidate)["diagnostics"]
        self.assertEqual(1, len(findings["META006_ROLE_ASSIGNMENT_INSTANCE_AS_GUFO_CLASSIFIER"]))
        self.assertEqual(1, len(findings["META007_PHASE_OCCURRENCE_AS_GUFO_CLASSIFIER"]))


class CompetencyFixtureControls(unittest.TestCase):
    def test_role_record_reaches_one_bearer_and_classifier(self):
        fixture = Graph().parse(HERE / "fixtures" / "positive-role-assignment.ttl", format="turtle")
        query = """
            PREFIX cac-core: <https://cacontology.projectvic.org/core#>
            SELECT ?bearer ?classifier WHERE {
              <https://example.invalid/v4-test#record-1> cac-core:describesRoleAssignment ?assignment .
              ?assignment cac-core:roleBearer ?bearer ; cac-core:roleClassifier ?classifier .
            }
        """
        rows = list(fixture.query(query))
        self.assertEqual(1, len(rows))
        self.assertEqual("https://example.invalid/v4-test#person-1", str(rows[0].bearer))
        self.assertEqual("https://example.invalid/v4-test#VictimRoleClassifier", str(rows[0].classifier))

    def test_revisited_phase_occurrences_remain_distinct(self):
        fixture = Graph().parse(HERE / "fixtures" / "positive-phase-occurrences.ttl", format="turtle")
        core = Namespace("https://cacontology.projectvic.org/core#")
        occurrences = set(fixture.subjects(core.isPhaseOf, None))
        self.assertEqual(3, len(occurrences))
        self.assertEqual(3, len({str(value) for value in occurrences}))

    def test_negative_fixtures_trigger_level_diagnostics(self):
        fixture = Graph()
        fixture.parse(HERE / "fixtures" / "negative-role-level-mixing.ttl", format="turtle")
        fixture.parse(HERE / "fixtures" / "negative-phase-level-mixing.ttl", format="turtle")
        findings = AUDIT.audit_graph(fixture)["diagnostics"]
        self.assertEqual(1, len(findings["META006_ROLE_ASSIGNMENT_INSTANCE_AS_GUFO_CLASSIFIER"]))
        self.assertEqual(1, len(findings["META007_PHASE_OCCURRENCE_AS_GUFO_CLASSIFIER"]))


class RepositoryParseControls(unittest.TestCase):
    def test_every_first_party_turtle_document_parses(self):
        repo = HERE.parents[1]
        dependency_root = HERE / "dependencies"
        generated_roots = (repo / "tmp", HERE / "tmp")
        failures = []
        for path in sorted(repo.rglob("*.ttl")):
            if dependency_root in path.parents:
                continue
            if any(root in path.parents for root in generated_roots):
                continue
            try:
                Graph().parse(path, format="turtle")
            except Exception as exc:  # pragma: no cover - failure detail matters
                failures.append(f"{path.relative_to(repo)}: {exc}")
        self.assertEqual([], failures)


if __name__ == "__main__":
    unittest.main()
