#!/usr/bin/env python3
"""Executable controls for v4 JSON-LD and SPARQL consumer contracts."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from rdflib import Graph
from rdflib.plugins.sparql.processor import prepareQuery


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CONTEXT = REPO / "contexts" / "cacontology-v4-foundation.jsonld"
QUERIES = REPO / "example_SPARQL_queries"


class JsonLdContextControls(unittest.TestCase):
    def test_v4_context_exposes_level_separated_contract(self):
        context = json.loads(CONTEXT.read_text(encoding="utf-8"))["@context"]
        required = {
            "RoleRecord",
            "RoleAssignment",
            "describesRoleAssignment",
            "roleBearer",
            "roleClassifier",
            "roleContext",
            "Phase",
            "isPhaseOf",
            "realizesPhaseClassifier",
            "precedes",
            "CustodyState",
            "hasCustodyState",
            "currentCustodyState",
            "custodyStateOf",
            "MembershipTier",
            "hasMembershipTier",
        }
        self.assertEqual(set(), required - set(context))
        for term in required - {"RoleRecord", "RoleAssignment", "Phase", "CustodyState", "MembershipTier"}:
            self.assertEqual("@id", context[term]["@type"])


class SparqlConsumerControls(unittest.TestCase):
    CASES = {
        "v4-role-assignment.rq": ("positive-role-assignment.ttl", 1),
        "v4-phase-history.rq": ("positive-phase-occurrences.ttl", 3),
        "v4-custody-state-history.rq": ("positive-custody-history.ttl", 2),
        "v4-membership-tier.rq": ("positive-membership-tier.ttl", 1),
    }

    def test_v4_queries_parse_and_return_expected_fixture_rows(self):
        for query_name, (fixture_name, expected_rows) in self.CASES.items():
            with self.subTest(query=query_name):
                query_text = (QUERIES / query_name).read_text(encoding="utf-8")
                prepareQuery(query_text)
                graph = Graph().parse(HERE / "fixtures" / fixture_name, format="turtle")
                self.assertEqual(expected_rows, len(list(graph.query(query_text))))


if __name__ == "__main__":
    unittest.main()
