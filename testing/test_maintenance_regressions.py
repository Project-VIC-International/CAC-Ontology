#!/usr/bin/env python3
"""Regression tests for post-v3.1 ontology maintenance fixes."""

from pathlib import Path
import unittest

import rdflib
from rdflib.plugins.sparql.parser import parseQuery


REPO = Path(__file__).resolve().parent.parent
SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")


class TestDetectionSparqlSyntax(unittest.TestCase):
    def test_all_detection_select_queries_parse(self):
        shapes = rdflib.Graph().parse(
            REPO / "ontology" / "cacontology-detection-shapes.ttl",
            format="turtle",
        )
        queries = list(shapes.objects(None, SH.select))

        self.assertEqual(14, len(queries))
        for query in queries:
            with self.subTest(query=str(query)[:80]):
                parseQuery(str(query))
if __name__ == "__main__":
    unittest.main()
