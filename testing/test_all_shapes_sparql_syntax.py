#!/usr/bin/env python3
"""Parse every SHACL sh:select in every *-shapes.ttl file.

Turtle parse of a shapes file does not evaluate embedded SPARQL. This test
closes that gap for the whole ontology tree (see #57).

``cacontology-detection-shapes.ttl`` is excluded only while #47 / PR #48 is
open. After that PR merges, delete ``EXCLUDED_UNTIL_PR48`` so this file is the
single repo-wide guard and supersedes PR #48's detection-only test.
"""

from __future__ import annotations

from pathlib import Path
import unittest

import rdflib
from rdflib.plugins.sparql.parser import parseQuery


REPO = Path(__file__).resolve().parent.parent
SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")

# Remove this set when https://github.com/Project-VIC-International/CAC-Ontology/pull/48 merges.
EXCLUDED_UNTIL_PR48 = frozenset({"cacontology-detection-shapes.ttl"})


class TestAllShapesSparqlSyntax(unittest.TestCase):
    def test_every_shape_select_query_parses(self):
        shape_files = sorted((REPO / "ontology").glob("*-shapes.ttl"))
        self.assertGreater(len(shape_files), 0)

        total = 0
        scanned = 0
        for path in shape_files:
            if path.name in EXCLUDED_UNTIL_PR48:
                continue
            scanned += 1
            graph = rdflib.Graph().parse(path, format="turtle")
            queries = list(graph.objects(None, SH.select))
            total += len(queries)
            for index, query in enumerate(queries, 1):
                with self.subTest(file=path.name, query_index=index):
                    parseQuery(str(query))

        self.assertGreater(scanned, 0)
        self.assertGreater(total, 0)
        # Detection must remain the only temporary exclusion.
        self.assertEqual(EXCLUDED_UNTIL_PR48, frozenset({"cacontology-detection-shapes.ttl"}))


if __name__ == "__main__":
    unittest.main()
