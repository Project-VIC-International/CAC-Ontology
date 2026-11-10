#!/usr/bin/env python3
"""Unit tests for legal compliance capability shapes in the platforms module."""

import os
import unittest

os.chdir(os.path.join(os.path.dirname(__file__), ".."))

from pyshacl import validate
import rdflib
from rdflib.namespace import SH

REPO = os.getcwd()
PLATFORMS = rdflib.Namespace("https://cacontology.projectvic.org/platforms#")
PLATFORMS_SHAPES = os.path.join(REPO, "ontology", "cacontology-platforms-shapes.ttl")
NOTICE = (
    "Legal-process contact details change. Check them against the provider's "
    "current law-enforcement guide before use."
)

PREFIXES = """
@prefix kb: <https://projectvic.org/kb/> .
@prefix uco-core: <https://ontology.unifiedcyberontology.org/uco/core/> .
@prefix cacontology-platforms: <https://cacontology.projectvic.org/platforms#> .
"""


def results(data: str):
    data_graph = rdflib.Graph().parse(data=PREFIXES + data, format="turtle")
    shapes_graph = rdflib.Graph().parse(PLATFORMS_SHAPES, format="turtle")
    _, report, _ = validate(
        data_graph, shacl_graph=shapes_graph, inference="none", abort_on_first=False
    )
    out = []
    for r in report.subjects(rdflib.RDF.type, SH.ValidationResult):
        out.append(
            (
                report.value(r, SH.resultPath),
                report.value(r, SH.resultSeverity),
                str(report.value(r, SH.resultMessage)),
            )
        )
    return out


class TestProviderMisplacementWarning(unittest.TestCase):
    def test_properties_on_provider_give_warnings_not_violations(self):
        res = results(
            """
            kb:organization-7c2a9e14-5b3f-4d8e-a1c6-0f9b2d4e6a37
                a cacontology-platforms:ElectronicServiceProvider ;
                cacontology-platforms:acceptsLegalProcess true ;
                cacontology-platforms:legalProcessContactInfo "Portal https://lawenforcement.example.com/" ;
                cacontology-platforms:responseTimeFrame 30 .
            """
        )
        misplaced = {
            PLATFORMS.acceptsLegalProcess,
            PLATFORMS.legalProcessContactInfo,
            PLATFORMS.responseTimeFrame,
        }
        hits = [r for r in res if r[0] in misplaced]
        self.assertEqual({r[0] for r in hits}, misplaced)
        for _, severity, message in hits:
            self.assertEqual(severity, SH.Warning)
            self.assertIn("LegalComplianceCapability", message)
            self.assertIn(NOTICE, message)

    def test_properties_on_capability_give_no_warning(self):
        res = results(
            """
            kb:legal-compliance-capability-1d5f7a93-2c8e-4b6a-9f1d-7e3c5a0b8d26
                a cacontology-platforms:LegalComplianceCapability ;
                cacontology-platforms:acceptsLegalProcess true ;
                cacontology-platforms:legalProcessContactInfo "subpoena-compliance@example.com" ;
                cacontology-platforms:responseTimeFrame 30 .
            """
        )
        self.assertEqual(res, [])


class TestResponseTimeFrameOnCapability(unittest.TestCase):
    def test_out_of_range_on_capability_is_violation(self):
        res = results(
            """
            kb:legal-compliance-capability-4e8b2c61-9a3d-4f7e-b5c0-2d6a1e9f3b48
                a cacontology-platforms:LegalComplianceCapability ;
                cacontology-platforms:responseTimeFrame 400 .
            """
        )
        self.assertIn(
            (PLATFORMS.responseTimeFrame, SH.Violation,
             "Response time frame must be between 1 and 365 days."),
            res,
        )

    def test_not_checked_on_disclosure_action(self):
        res = results(
            """
            kb:legal-data-disclosure-action-8b3e6f20-4a1d-4c9b-a7e5-3f0d2c6b9a14
                a cacontology-platforms:LegalDataDisclosureAction ;
                cacontology-platforms:responseTimeFrame 400 .
            """
        )
        self.assertFalse(
            any(r[0] == PLATFORMS.responseTimeFrame and r[1] == SH.Violation for r in res)
        )


if __name__ == "__main__":
    unittest.main()
