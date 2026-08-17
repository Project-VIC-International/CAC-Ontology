#!/usr/bin/env python3
"""Unit tests for CaseLinker state machine extension classes."""

import os
import unittest

from pyshacl import validate
import rdflib

os.chdir(os.path.join(os.path.dirname(__file__), ".."))

REPO = os.getcwd()

CAC_SEXTORTION = rdflib.Namespace("https://cacontology.projectvic.org/sextortion#")
CAC_PLATFORMS = rdflib.Namespace("https://cacontology.projectvic.org/platforms#")
CAC_GROOMING = rdflib.Namespace("https://cacontology.projectvic.org/grooming#")


def shacl_validate(data_graph: rdflib.Graph, shapes_path: str) -> bool:
    shapes_graph = rdflib.Graph()
    shapes_graph.parse(shapes_path, format="turtle")
    conforms, _, _ = validate(
        data_graph,
        shacl_graph=shapes_graph,
        inference="none",
        abort_on_first=False,
        allow_infos=True,
        allow_warnings=True,
    )
    return conforms


class TestCoercionCycle(unittest.TestCase):
    shapes = os.path.join(REPO, "ontology", "cacontology-sextortion-shapes.ttl")

    def test_valid_instance_passes_shacl(self):
        g = rdflib.Graph()
        g.parse(
            data="""
            @prefix cac-core: <https://cacontology.projectvic.org/core#> .
            @prefix cac-sextortion: <https://cacontology.projectvic.org/sextortion#> .
            <urn:uuid:test-artifact-001> a cac-core:Artifact .
            <urn:uuid:test-extortion-phase> a cac-core:Phase .
            <urn:uuid:test-image-phase> a cac-core:Phase .
            <urn:uuid:test-coercion-cycle-valid> a cac-sextortion:CoercionCycle ;
                cac-sextortion:sustainedBy <urn:uuid:test-artifact-001> ;
                cac-sextortion:cyclesBetween <urn:uuid:test-extortion-phase> ,
                                           <urn:uuid:test-image-phase> ;
                cac-sextortion:coercionCycleDemandType "imagery_quota" ;
                cac-sextortion:terminationCondition "unknown" .
            """,
            format="turtle",
        )
        self.assertTrue(shacl_validate(g, self.shapes))
        cycle = rdflib.URIRef("urn:uuid:test-coercion-cycle-valid")
        self.assertIn((cycle, rdflib.RDF.type, CAC_SEXTORTION.CoercionCycle), g)
        self.assertIn(
            (cycle, CAC_SEXTORTION.coercionCycleDemandType, rdflib.Literal("imagery_quota")),
            g,
        )

    def test_missing_sustained_by_fails_shacl(self):
        g = rdflib.Graph()
        g.parse(
            data="""
            @prefix cac-sextortion: <https://cacontology.projectvic.org/sextortion#> .
            <urn:uuid:test-coercion-cycle-invalid> a cac-sextortion:CoercionCycle ;
                cac-sextortion:coercionCycleDemandType "imagery_quota" ;
                cac-sextortion:cyclesBetween <urn:uuid:phase-a>, <urn:uuid:phase-b> .
            """,
            format="turtle",
        )
        self.assertFalse(shacl_validate(g, self.shapes))


class TestChannelMigrationEvent(unittest.TestCase):
    shapes = os.path.join(REPO, "ontology", "cacontology-platforms-shapes.ttl")

    def test_valid_instance_passes_shacl(self):
        g = rdflib.Graph()
        g.parse(
            data="""
            @prefix uco-observable: <https://ontology.unifiedcyberontology.org/uco/observable/> .
            @prefix cac-core: <https://cacontology.projectvic.org/core#> .
            @prefix cac-platforms: <https://cacontology.projectvic.org/platforms#> .
            <urn:uuid:platform-instagram> a uco-observable:OnlineService .
            <urn:uuid:platform-messenger> a uco-observable:OnlineService .
            <urn:uuid:phase-trust> a cac-core:Phase .
            <urn:uuid:phase-image> a cac-core:Phase .
            <urn:uuid:test-channel-migration-valid> a cac-platforms:ChannelMigrationEvent ;
                cac-platforms:fromPlatform <urn:uuid:platform-instagram> ;
                cac-platforms:toPlatform <urn:uuid:platform-messenger> ;
                cac-platforms:migrationRationale "capability_upgrade" ;
                cac-platforms:occursBetween <urn:uuid:phase-trust> , <urn:uuid:phase-image> .
            """,
            format="turtle",
        )
        self.assertTrue(shacl_validate(g, self.shapes))
        event = rdflib.URIRef("urn:uuid:test-channel-migration-valid")
        self.assertIn(
            (event, CAC_PLATFORMS.migrationRationale, rdflib.Literal("capability_upgrade")),
            g,
        )

    def test_invalid_rationale_fails_shacl(self):
        g = rdflib.Graph()
        g.parse(
            data="""
            @prefix cac-platforms: <https://cacontology.projectvic.org/platforms#> .
            <urn:uuid:test-channel-migration-invalid> a cac-platforms:ChannelMigrationEvent ;
                cac-platforms:fromPlatform <urn:uuid:platform-a> ;
                cac-platforms:toPlatform <urn:uuid:platform-b> ;
                cac-platforms:migrationRationale "invalid_value" ;
                cac-platforms:occursBetween <urn:uuid:phase-a>, <urn:uuid:phase-b> .
            """,
            format="turtle",
        )
        self.assertFalse(shacl_validate(g, self.shapes))


class TestAffordanceMisuse(unittest.TestCase):
    shapes = os.path.join(REPO, "ontology", "cacontology-platforms-shapes.ttl")

    def test_valid_instance_passes_shacl(self):
        g = rdflib.Graph()
        g.parse(
            data="""
            @prefix cac-core: <https://cacontology.projectvic.org/core#> .
            @prefix cac-platforms: <https://cacontology.projectvic.org/platforms#> .
            @prefix uco-observable: <https://ontology.unifiedcyberontology.org/uco/observable/> .
            <urn:uuid:affordance-ephemerality> a cac-platforms:PlatformAffordance .
            <urn:uuid:phase-trust> a cac-core:Phase .
            <urn:uuid:phase-image> a cac-core:Phase .
            <urn:uuid:platform-snapchat> a uco-observable:OnlineService .
            <urn:uuid:test-affordance-misuse-valid> a cac-platforms:AffordanceMisuse ;
                cac-platforms:affordanceClass <urn:uuid:affordance-ephemerality> ;
                cac-platforms:enablesTransitionFrom <urn:uuid:phase-trust> ;
                cac-platforms:enablesTransitionTo <urn:uuid:phase-image> ;
                cac-platforms:platform <urn:uuid:platform-snapchat> ;
                cac-platforms:misuseDescription "Disappearing messages normalized image sharing before extortion." .
            """,
            format="turtle",
        )
        self.assertTrue(shacl_validate(g, self.shapes))
        misuse = rdflib.URIRef("urn:uuid:test-affordance-misuse-valid")
        self.assertIn(
            (misuse, CAC_PLATFORMS.misuseDescription, rdflib.Literal(
                "Disappearing messages normalized image sharing before extortion."
            )),
            g,
        )

    def test_missing_description_fails_shacl(self):
        g = rdflib.Graph()
        g.parse(
            data="""
            @prefix cac-platforms: <https://cacontology.projectvic.org/platforms#> .
            <urn:uuid:test-affordance-misuse-invalid> a cac-platforms:AffordanceMisuse ;
                cac-platforms:affordanceClass <urn:uuid:affordance-anonymity> ;
                cac-platforms:enablesTransitionFrom <urn:uuid:phase-a> ;
                cac-platforms:enablesTransitionTo <urn:uuid:phase-b> .
            """,
            format="turtle",
        )
        self.assertFalse(shacl_validate(g, self.shapes))


class TestAccountReplacementEvent(unittest.TestCase):
    shapes = os.path.join(REPO, "ontology", "cacontology-grooming-shapes.ttl")

    def test_valid_instance_passes_shacl(self):
        g = rdflib.Graph()
        g.parse(
            data="""
            @prefix cac-core: <https://cacontology.projectvic.org/core#> .
            @prefix cac-grooming: <https://cacontology.projectvic.org/grooming#> .
            @prefix uco-observable: <https://ontology.unifiedcyberontology.org/uco/observable/> .
            <urn:uuid:account-banned> a uco-observable:Account .
            <urn:uuid:account-new> a uco-observable:Account .
            <urn:uuid:phase-initial-contact> a cac-grooming:InitialContactPhase , cac-core:Phase .
            <urn:uuid:test-account-replacement-valid> a cac-grooming:AccountReplacementEvent ;
                cac-grooming:triggeredBy "platform_ban" ;
                cac-grooming:resumesAt <urn:uuid:phase-initial-contact> ;
                cac-grooming:originalAccountId <urn:uuid:account-banned> ;
                cac-grooming:replacementAccountId <urn:uuid:account-new> .
            """,
            format="turtle",
        )
        self.assertTrue(shacl_validate(g, self.shapes))
        event = rdflib.URIRef("urn:uuid:test-account-replacement-valid")
        self.assertIn(
            (event, CAC_GROOMING.triggeredBy, rdflib.Literal("platform_ban")),
            g,
        )

    def test_invalid_trigger_fails_shacl(self):
        g = rdflib.Graph()
        g.parse(
            data="""
            @prefix cac-grooming: <https://cacontology.projectvic.org/grooming#> .
            <urn:uuid:test-account-replacement-invalid> a cac-grooming:AccountReplacementEvent ;
                cac-grooming:triggeredBy "account_hack" ;
                cac-grooming:resumesAt <urn:uuid:phase-initial-contact> .
            """,
            format="turtle",
        )
        self.assertFalse(shacl_validate(g, self.shapes))


if __name__ == "__main__":
    unittest.main()
