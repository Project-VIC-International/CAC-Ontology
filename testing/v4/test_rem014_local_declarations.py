#!/usr/bin/env python3
"""Regression controls for CAC-owned local declaration repairs in REM-014."""

from __future__ import annotations

from pathlib import Path
import unittest

from rdflib import Graph, Namespace, OWL, RDF, RDFS, SH, SKOS


REPOSITORY = Path(__file__).resolve().parents[2]
ONTOLOGY = REPOSITORY / "ontology"

CAC = Namespace("https://cacontology.projectvic.org#")
DETECTION = Namespace("https://cacontology.projectvic.org/detection#")
EDUCATIONAL = Namespace("https://cacontology.projectvic.org/educational#")
HOTLINES = Namespace("https://cacontology.projectvic.org/hotlines#")
INTERNATIONAL = Namespace("https://cacontology.projectvic.org/international#")
PREVENTION = Namespace("https://cacontology.projectvic.org/prevention#")
TASKFORCE = Namespace("https://cacontology.projectvic.org/taskforce#")
TRAINING = Namespace("https://cacontology.projectvic.org/training#")
VICTIM_IMPACT = Namespace("https://cacontology.projectvic.org/victim-impact#")


EXPECTED_CLASSES = {
    "cacontology-core.ttl": {
        CAC.ChildSexualExploitation,
        CAC.ChildSexualExploitationCharge,
    },
    "cacontology-educational-exploitation.ttl": {
        EDUCATIONAL.AcademicPowerVulnerability,
        EDUCATIONAL.AgeSpecificTargeting,
        EDUCATIONAL.ClassroomIsolationVulnerability,
        EDUCATIONAL.DigitalImpersonation,
        EDUCATIONAL.EducationalInstitutionInvestigation,
        EDUCATIONAL.ForcibleTouching,
        EDUCATIONAL.InstitutionalVulnerability,
        EDUCATIONAL.OpportunisticTouching,
        EDUCATIONAL.SchoolStaffReporting,
        EDUCATIONAL.SexOffenderRegistration,
        EDUCATIONAL.StudentVictimTargeting,
        EDUCATIONAL.UseOfChildInSexualPerformance,
        EDUCATIONAL.VictimAccountEvidence,
        EDUCATIONAL.VulnerableStudentTargeting,
        EDUCATIONAL.WitnessTestimonyEvidence,
        EDUCATIONAL.WrittenHarassmentEvidence,
    },
    "cacontology-international.ttl": {INTERNATIONAL.USAustraliaCoordination},
    "cacontology-prevention.ttl": {
        PREVENTION.EducationalOutreach,
        PREVENTION.PreventionCampaign,
        PREVENTION.SafetyEducationEvent,
    },
    "cacontology-taskforce.ttl": {
        TASKFORCE.CertificationProgram,
        TASKFORCE.FederalLawEnforcementPartner,
        TASKFORCE.LocalLawEnforcementPartner,
    },
    "cacontology-training.ttl": {
        TRAINING.GlobalTrainingReach,
        TRAINING.K9ProgramMetrics,
        TRAINING.OperationalTrainingMetrics,
        TRAINING.OutreachEventMetrics,
        TRAINING.ProfessionalTrainingMetrics,
        TRAINING.TrainingEffectiveness,
    },
    "cacontology-victim-impact.ttl": {
        VICTIM_IMPACT.MentalHealthProfessional,
        VICTIM_IMPACT.RecoveryBarriers,
        VICTIM_IMPACT.VictimBehavior,
    },
}


class Rem014LocalDeclarationTests(unittest.TestCase):
    def test_referenced_cac_classes_are_explicitly_declared(self):
        for filename, expected_classes in EXPECTED_CLASSES.items():
            with self.subTest(filename=filename):
                graph = Graph().parse(ONTOLOGY / filename, format="turtle")
                declared = set(graph.subjects(RDF.type, OWL.Class))
                self.assertEqual(set(), expected_classes - declared)

    def test_hotline_property_chain_member_is_an_object_property(self):
        graph = Graph().parse(ONTOLOGY / "cacontology-hotlines.ttl", format="turtle")
        self.assertIn((HOTLINES.hasStep, RDF.type, OWL.ObjectProperty), graph)

    def test_skos_schemes_are_targeted_as_individuals_not_owl_classes(self):
        data = Graph().parse(ONTOLOGY / "cacontology-detection.ttl", format="turtle")
        shapes = Graph().parse(
            ONTOLOGY / "cacontology-detection-shapes.ttl", format="turtle"
        )
        schemes = {
            DETECTION.SARClassificationScheme,
            DETECTION.COPINEClassificationScheme,
            DETECTION.TannerScaleScheme,
        }

        for scheme in schemes:
            with self.subTest(scheme=scheme):
                self.assertIn((scheme, RDF.type, SKOS.ConceptScheme), data)
                self.assertNotIn((scheme, RDF.type, OWL.Class), data)
                self.assertIn(
                    (DETECTION.ClassificationSchemeGUFOShape, SH.targetNode, scheme),
                    shapes,
                )
                self.assertNotIn(
                    (DETECTION.ClassificationSchemeGUFOShape, SH.targetClass, scheme),
                    shapes,
                )

    def test_classification_properties_range_over_concepts_not_schemes(self):
        graph = Graph().parse(ONTOLOGY / "cacontology-detection.ttl", format="turtle")
        for property_iri in (
            DETECTION.sarClassification,
            DETECTION.copineClassification,
        ):
            with self.subTest(property=property_iri):
                self.assertIn((property_iri, RDFS.range, SKOS.Concept), graph)


if __name__ == "__main__":
    unittest.main()
