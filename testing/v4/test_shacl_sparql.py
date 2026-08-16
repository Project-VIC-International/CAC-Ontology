#!/usr/bin/env python3
"""Controls for the repository-wide embedded SHACL SPARQL syntax audit."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SPEC = importlib.util.spec_from_file_location(
    "audit_shacl_sparql", HERE / "audit_shacl_sparql.py"
)
AUDIT = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(AUDIT)

LEVEL_SPEC = importlib.util.spec_from_file_location(
    "audit_shape_level_assumptions", HERE / "audit_shape_level_assumptions.py"
)
LEVEL_AUDIT = importlib.util.module_from_spec(LEVEL_SPEC)
assert LEVEL_SPEC.loader is not None
LEVEL_SPEC.loader.exec_module(LEVEL_AUDIT)


class RepositoryShaclSparqlControls(unittest.TestCase):
    def test_all_non_detection_queries_parse(self):
        result = AUDIT.audit(REPO / "ontology")
        self.assertEqual(0, result["proposal_failures"])
        self.assertTrue(
            all(
                item["file"] == "cacontology-detection-shapes.ttl"
                for item in result["results"]
            )
        )

    def test_audit_detects_a_malformed_query(self):
        malformed = """
            @prefix sh: <http://www.w3.org/ns/shacl#> .
            @prefix ex: <https://example.invalid/> .
            ex:Shape a sh:NodeShape ;
                sh:sparql [ sh:select "SELECT ?this WHERE { ?this ex:p ?o ; ?o ex:q ?v . }" ] .
        """
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "control-shapes.ttl"
            path.write_text(malformed, encoding="utf-8")
            result = AUDIT.audit(path.parent)
        self.assertEqual(1, result["proposal_failures"])

    def test_role_and_phase_mentions_do_not_reintroduce_level_conflation(self):
        results = LEVEL_AUDIT.inventory(REPO / "ontology")
        exceptions = {
            (
                "cacontology-core-shapes.ttl",
                "https://cacontology.projectvic.org#FoundationalTypeConsistencyShape",
            )
        }
        failures = []
        for item in results:
            if item["file"] == "cacontology-detection-shapes.ttl":
                continue
            if (item["file"], item["shape"]) in exceptions:
                continue
            if not any("must not" in message.lower() for message in item["messages"]):
                failures.append(item)
        self.assertEqual([], failures)


if __name__ == "__main__":
    unittest.main()
