#!/usr/bin/env python3
"""Executable contract for the approved Gate 4.1 semantic mapping policy."""

from pathlib import Path
import unittest

from rdflib import Graph, Namespace, OWL, RDF, RDFS, URIRef
from pyshacl import validate


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
ONTOLOGY = REPO / "ontology"

GUFO = Namespace("http://purl.org/nemo/gufo#")
CORE = Namespace("https://cacontology.projectvic.org/core#")
CAC = Namespace("https://cacontology.projectvic.org#")
TEMPORAL = Namespace("https://cacontology.projectvic.org/temporal#")
INTEGRATION = Namespace("https://cacontology.projectvic.org/integration-patterns#")
LEGAL = Namespace("https://cacontology.projectvic.org/legal-harmonization#")
GROOMING = Namespace("https://cacontology.projectvic.org/grooming#")
IMPACT = Namespace("https://cacontology.projectvic.org/victim-impact#")
COORDINATION = Namespace("https://cacontology.projectvic.org/investigation-coordination#")
CORRUPTION = Namespace("https://cacontology.projectvic.org/law-enforcement-corruption#")
FEDERAL = Namespace("https://cacontology.projectvic.org/usa-federal-law#")
ENTERPRISES = Namespace("https://cacontology.projectvic.org/extremist-enterprises#")
UCO_ACTION = Namespace("https://ontology.unifiedcyberontology.org/uco/action/")
UCO_OBSERVABLE = Namespace("https://ontology.unifiedcyberontology.org/uco/observable/")
UCO_ROLE = Namespace("https://ontology.unifiedcyberontology.org/uco/role/")
UCO_VICTIM = Namespace("https://ontology.unifiedcyberontology.org/uco/victim/")


class Gate41SemanticPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = Graph()
        for path in sorted(ONTOLOGY.glob("*.ttl")):
            cls.graph.parse(path, format="turtle")

    def test_removed_external_terms_are_absent_from_first_party_triples(self):
        stale = {
            URIRef("http://purl.org/nemo/gufo#participantIn"),
            URIRef("http://purl.org/nemo/gufo#ParticipationSituation"),
            URIRef("http://purl.org/nemo/gufo#Process"),
            URIRef("http://purl.org/nemo/gufo#participatesIn"),
            URIRef("http://purl.org/nemo/gufo#IntrinsicMoment"),
            URIRef("http://purl.org/nemo/gufo#AbstractArtifact"),
            URIRef("http://purl.org/nemo/gufo#Norm"),
            URIRef("http://purl.org/nemo/gufo#Plan"),
            URIRef("http://purl.org/nemo/gufo#precedes"),
            URIRef("https://ontology.unifiedcyberontology.org/uco/channel/DigitalService"),
            URIRef("https://ontology.unifiedcyberontology.org/uco/observable/DigitalService"),
            URIRef("https://ontology.unifiedcyberontology.org/uco/observable/DigitalServiceFeature"),
            URIRef("https://ontology.unifiedcyberontology.org/uco/action/Crime"),
            URIRef("https://ontology.unifiedcyberontology.org/uco/role/VictimRole"),
            URIRef("https://ontology.unifiedcyberontology.org/uco/role/SubjectRole"),
            URIRef("https://ontology.unifiedcyberontology.org/uco/role/OffenderRole"),
            URIRef("https://ontology.unifiedcyberontology.org/uco/observable/PhoneCall"),
            URIRef("https://ontology.unifiedcyberontology.org/uco/observable/DigitalDevice"),
            URIRef("https://ontology.unifiedcyberontology.org/uco/observable/PhoneNumber"),
            URIRef("https://ontology.unifiedcyberontology.org/uco/observable/DigitalArtifact"),
        }
        used = {value for triple in self.graph for value in triple if value in stale}
        self.assertEqual(set(), used)

    def test_qualified_participation_uses_the_local_situation(self):
        self.assertIn(
            (CORE.QualifiedParticipationSituation, RDFS.subClassOf, CORE.Situation),
            self.graph,
        )
        for property_iri, predicate in (
            (COORDINATION.standsInQualifiedParticipation, RDFS.range),
            (COORDINATION.concernsParticipant, RDFS.domain),
            (CORRUPTION.standsInQualifiedCorruption, RDFS.range),
            (CORRUPTION.concernsCorruptOfficer, RDFS.domain),
            (LEGAL.standsInQualifiedCompliance, RDFS.range),
            (LEGAL.concernsLegalFramework, RDFS.domain),
        ):
            with self.subTest(property=property_iri):
                self.assertIn(
                    (property_iri, predicate, CORE.QualifiedParticipationSituation),
                    self.graph,
                )

    def test_lifecycle_is_an_event_type_with_a_local_ownership_relation(self):
        self.assertIn((TEMPORAL.InvestigationLifecycle, RDF.type, GUFO.EventType), self.graph)
        self.assertNotIn((TEMPORAL.InvestigationLifecycle, RDF.type, GUFO.Kind), self.graph)
        self.assertIn(
            (TEMPORAL.InvestigationLifecycle, RDFS.subClassOf, CORE.Event), self.graph
        )
        restrictions = set(self.graph.objects(CAC.CACInvestigation, RDFS.subClassOf))
        matching = {
            node
            for node in restrictions
            if (node, OWL.onProperty, TEMPORAL.hasInvestigationLifecycle) in self.graph
            and (node, OWL.onClass, TEMPORAL.InvestigationLifecycle) in self.graph
        }
        self.assertEqual(1, len(matching))

    def test_descriptor_and_planning_levels_remain_separate(self):
        self.assertIn((INTEGRATION.PlanningArtifact, RDFS.subClassOf, CORE.Artifact), self.graph)
        for strategy in (INTEGRATION.ModuleIntegrationStrategy, INTEGRATION.ValidationStrategy):
            self.assertIn((strategy, RDFS.subClassOf, INTEGRATION.PlanningArtifact), self.graph)
        for descriptor in (
            INTEGRATION.ForensicsLifecyclePattern,
            INTEGRATION.EducationalPattern,
            INTEGRATION.AIGenerationPattern,
            INTEGRATION.CapabilityPattern,
            INTEGRATION.TreatyPattern,
            INTEGRATION.IdeologyPattern,
        ):
            self.assertIn((descriptor, RDF.type, INTEGRATION.IntegrationPattern), self.graph)

    def test_intrinsic_modes_have_bearer_paths_and_contexts_stay_separate(self):
        for mode in (
            GROOMING.VictimVulnerability,
            IMPACT.PsychologicalHarm,
            IMPACT.ResilienceDisposition,
        ):
            self.assertIn((mode, RDFS.subClassOf, GUFO.IntrinsicMode), self.graph)
            restrictions = set(self.graph.objects(mode, RDFS.subClassOf))
            self.assertTrue(
                any((node, OWL.onProperty, GUFO.inheresIn) in self.graph for node in restrictions)
            )
        for context in (GROOMING.VictimVulnerabilitySituation, IMPACT.ResilienceContext):
            self.assertIn((context, RDFS.subClassOf, CORE.Situation), self.graph)
        self.assertIn((IMPACT.ResilienceFactors, OWL.deprecated, None), self.graph)

    def test_offense_and_role_interoperability_targets_are_current(self):
        self.assertIn((CORE.OffenseEvent, RDFS.subClassOf, CORE.ExploitationEvent), self.graph)
        self.assertIn((CORE.OffenseEvent, RDFS.subClassOf, UCO_ACTION.Action), self.graph)
        for victim_role in (CAC.VictimRole, IMPACT.TraumatizedVictim, IMPACT.VictimInRecovery):
            self.assertIn((victim_role, RDFS.subClassOf, UCO_VICTIM.Victim), self.graph)
        for offender_role in (CAC.OffenderRole, CAC.ConspiracyRole):
            self.assertIn((offender_role, RDFS.subClassOf, UCO_ROLE.MaliciousRole), self.graph)

    def test_direction_sensitive_properties_follow_the_approved_contract(self):
        for property_iri in (
            FEDERAL.prosecutedBy,
            FEDERAL.investigatedBy,
            FEDERAL.defendedBy,
            FEDERAL.victimizedBy,
        ):
            self.assertNotIn((property_iri, RDFS.subPropertyOf, None), self.graph)
        for property_iri in (
            ENTERPRISES.participatesInCoercion,
            ENTERPRISES.participatesInRecruitment,
        ):
            self.assertIn((property_iri, RDFS.subPropertyOf, GUFO.participatedIn), self.graph)

    def test_current_uco_targets_exist_in_the_pinned_profile(self):
        pinned = REPO / "testing" / "v4" / "dependencies" / "uco-gufo-profile" / "4b98b9881aa29ed80f39b589d15725fa696c921a" / "dependencies" / "UCO" / "ontology" / "uco"
        graph = Graph()
        for relative in ("observable/observable.ttl", "role/role.ttl", "victim/victim.ttl"):
            graph.parse(pinned / relative, format="turtle")
        for class_iri in (
            UCO_OBSERVABLE.OnlineService,
            UCO_OBSERVABLE.OnlineServiceFacet,
            UCO_OBSERVABLE.Call,
            UCO_OBSERVABLE.Device,
            UCO_OBSERVABLE.PhoneAccount,
            UCO_OBSERVABLE.PhoneAccountFacet,
            UCO_ROLE.MaliciousRole,
            UCO_VICTIM.Victim,
        ):
            with self.subTest(class_iri=class_iri):
                self.assertIn((class_iri, RDF.type, OWL.Class), graph)

    def test_phone_account_pattern_accepts_structured_data_and_rejects_a_literal(self):
        shapes = Graph().parse(ONTOLOGY / "cacontology-us-ncmec-shapes.ttl", format="turtle")
        positive = Graph().parse(HERE / "fixtures" / "positive-phone-account-trace.ttl", format="turtle")
        negative = Graph().parse(HERE / "fixtures" / "negative-unstructured-phone-trace.ttl", format="turtle")
        positive_conforms, _, positive_report = validate(
            data_graph=positive, shacl_graph=shapes, inference="none", advanced=True
        )
        negative_conforms, _, _ = validate(
            data_graph=negative, shacl_graph=shapes, inference="none", advanced=True
        )
        self.assertTrue(positive_conforms, str(positive_report))
        self.assertFalse(negative_conforms)


if __name__ == "__main__":
    unittest.main()
