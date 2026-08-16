#!/usr/bin/env python3
"""Prevent UCO hash values from crossing into the disjoint UcoObject branch."""

from pathlib import Path
import unittest

from rdflib import Graph, Namespace, RDFS

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CORE = Namespace("https://cacontology.projectvic.org/core#")
DETECTION = Namespace("https://cacontology.projectvic.org/detection#")
UCO_TYPES = Namespace("https://ontology.unifiedcyberontology.org/uco/types/")


class DetectionHashConsistencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = Graph().parse(
            REPO / "ontology" / "cacontology-detection.ttl", format="turtle"
        )

    def test_hash_classes_remain_on_uco_hash_branch_only(self):
        for term in (DETECTION.PhotoDNAHash, DETECTION.PerceptualHash):
            with self.subTest(term=term):
                self.assertIn((term, RDFS.subClassOf, UCO_TYPES.Hash), self.graph)
                self.assertNotIn((term, RDFS.subClassOf, CORE.Artifact), self.graph)


if __name__ == "__main__":
    unittest.main()
