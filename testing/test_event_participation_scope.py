"""Regression checks for the domain participation targets in issue #58.

These focused tests use the shipped local class hierarchy with RDFS
inference and the participation shape's complete blank-node closure. They do
not download owl:imports or stand in for the repository-wide validation run.
"""
from itertools import combinations
from pathlib import Path
import unittest
from uuid import UUID

from pyshacl import validate
from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDF, RDFS, OWL


ROOT = Path(__file__).resolve().parents[1]
CORE = Namespace("https://cacontology.projectvic.org/core#")
FORENSICS = Namespace("https://cacontology.projectvic.org/forensics#")
FEDERAL = Namespace("https://cacontology.projectvic.org/usa-federal-law#")
GROOMING = Namespace("https://cacontology.projectvic.org/grooming#")
STREET = Namespace("https://cacontology.projectvic.org/street#")
IMPACT = Namespace("https://cacontology.projectvic.org/victim-impact#")
IDENTITY = Namespace("https://ontology.unifiedcyberontology.org/uco/identity/")
SH = Namespace("http://www.w3.org/ns/shacl#")
EX = Namespace("urn:example:participation:")
GROOMING_EVENT_ROOTS = (
    GROOMING.GroomingBehavior,
    GROOMING.VictimTargeting,
    GROOMING.AccountReplacementEvent,
)
GROOMING_PARTICIPANTS = (
    GROOMING.targetsVictim, GROOMING.performedBy,
    GROOMING.witnessedBy, GROOMING.facilitatedBy,
)


def undeclared_cac_vocabulary(data, declarations):
    """Return missing CAC property/class declarations for asserted RDF roles."""
    properties = {
        term for kind in (RDF.Property, OWL.ObjectProperty,
                          OWL.DatatypeProperty, OWL.AnnotationProperty)
        for term in declarations.subjects(RDF.type, kind)
    }
    classes = {
        term for kind in (OWL.Class, RDFS.Class)
        for term in declarations.subjects(RDF.type, kind)
    }
    is_cac = lambda term: str(term).startswith("https://cacontology.projectvic.org/")
    return (
        {str(p) for p in data.predicates() if is_cac(p) and p not in properties},
        {str(c) for c in data.objects(None, RDF.type) if is_cac(c) and c not in classes},
    )


class EventParticipationScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ontology = Graph()
        for filename in (
            "cacontology-core-spine.ttl",
            "cacontology-forensics.ttl",
            "cacontology-usa-federal-law.ttl",
            "cacontology-victim-impact.ttl",
            "cacontology-grooming.ttl",
            "cacontology-street-recruitment.ttl",
        ):
            cls.ontology.parse(ROOT / "ontology" / filename, format="turtle")
        cls.hierarchy = Graph()
        for triple in cls.ontology.triples((None, RDFS.subClassOf, None)):
            cls.hierarchy.add(triple)
        cls.shapes = {}
        for filename, shape in (
            ("cacontology-forensics-shapes.ttl", FORENSICS.ForensicEventParticipationShape),
            ("cacontology-usa-federal-law-shapes.ttl", FEDERAL.EventParticipationValidationShape),
            ("cacontology-grooming-shapes.ttl", GROOMING.GroomingEventParticipationShape),
        ):
            graph = Graph().parse(ROOT / "ontology" / filename, format="turtle")
            cls.shapes[shape] = graph.cbd(shape)
            if shape == GROOMING.GroomingEventParticipationShape:
                cls.grooming_shapes = graph

    def validate_data(self, data, shapes, *, inference="rdfs", include_hierarchy=True):
        return validate(
            data_graph=data,
            shacl_graph=shapes,
            ont_graph=self.hierarchy if include_hierarchy else None,
            inference=inference,
            do_owl_imports=False,
        )

    def conforms(self, shape, event_type, participant=None):
        data = Graph()
        data.add((EX.event, RDF.type, event_type))
        if participant is not None:
            data.add((EX.event, participant, EX.actor))
        conforms, _, report = self.validate_data(data, self.shapes[shape])
        return conforms, report

    def domain_event_classes(self, namespace):
        return {
            term for term in self.ontology.subjects(RDF.type, OWL.Class)
            if str(term).startswith(str(namespace))
            and CORE.Event in self.ontology.transitive_objects(term, RDFS.subClassOf)
        }

    def test_unrelated_events_do_not_require_domain_participants(self):
        # SupportEvent is the actual spine parent of victim-support activity.
        for shape in self.shapes:
            for event_type in (CORE.Event, CORE.SupportEvent, CORE.InvestigativeAction,
                               IMPACT.VictimSupport):
                with self.subTest(shape=shape, event_type=event_type):
                    conforms, report = self.conforms(shape, event_type)
                    self.assertTrue(conforms, report)

    def test_forensic_events_still_require_participation(self):
        for event_type in self.domain_event_classes(FORENSICS):
            with self.subTest(event_type=event_type):
                conforms, report = self.conforms(FORENSICS.ForensicEventParticipationShape, event_type)
                self.assertFalse(conforms, report)

    def test_federal_events_still_require_participation(self):
        # Federal legal phases also inherit FederalProsecution and Event.
        for event_type in self.domain_event_classes(FEDERAL):
            with self.subTest(event_type=event_type):
                conforms, report = self.conforms(FEDERAL.EventParticipationValidationShape, event_type)
                self.assertFalse(conforms, report)

    def test_grooming_events_still_require_participation(self):
        events = self.domain_event_classes(GROOMING)
        self.assertTrue(events)
        for event_type in events:
            with self.subTest(event_type=event_type):
                conforms, report = self.conforms(
                    GROOMING.GroomingEventParticipationShape, event_type,
                )
                self.assertFalse(conforms, report)

    def test_each_grooming_participant_path_satisfies_each_event_branch(self):
        for event_type in GROOMING_EVENT_ROOTS:
            for prop in GROOMING_PARTICIPANTS:
                with self.subTest(event_type=event_type, prop=prop):
                    conforms, report = self.conforms(
                        GROOMING.GroomingEventParticipationShape, event_type, prop,
                    )
                    self.assertTrue(conforms, report)

    def test_grooming_subclasses_declared_in_another_module_keep_participation(self):
        # These street-recruitment events inherit grooming:SexualExploitation.
        event_types = (
            STREET.DirectTraffickingProposition, STREET.ExplicitCommercialOffer,
            STREET.StrippingProposition, STREET.ProstitutionProposition,
            STREET.BodySellingProposition, STREET.EconomicIncentivePresentation,
            STREET.ImmediateExploitationAttempt,
        )
        for event_type in event_types:
            for prop in (None, GROOMING.performedBy):
                with self.subTest(event_type=event_type, prop=prop):
                    conforms, report = self.conforms(
                        GROOMING.GroomingEventParticipationShape, event_type, prop,
                    )
                    self.assertEqual(prop is not None, conforms, report)

    def test_new_subclasses_of_each_grooming_branch_keep_participation(self):
        for root in GROOMING_EVENT_ROOTS:
            for with_participant in (False, True):
                data = Graph()
                data.add((EX.SpecializedEvent, RDFS.subClassOf, root))
                data.add((EX.event, RDF.type, EX.SpecializedEvent))
                if with_participant:
                    data.add((EX.event, GROOMING.performedBy, EX.actor))
                with self.subTest(root=root, with_participant=with_participant):
                    conforms, _, report = self.validate_data(
                        data, self.shapes[GROOMING.GroomingEventParticipationShape],
                    )
                    self.assertEqual(with_participant, conforms, report)

    def test_each_forensic_participant_path_satisfies_the_rule(self):
        for prop in (FORENSICS.examinedBy, FORENSICS.performedBy,
                     FORENSICS.witnessedBy, FORENSICS.authorizedBy):
            with self.subTest(prop=prop):
                conforms, report = self.conforms(
                    FORENSICS.ForensicEventParticipationShape,
                    FORENSICS.ForensicAcquisitionAction, prop,
                )
                self.assertTrue(conforms, report)

    def test_each_federal_participant_path_satisfies_the_rule(self):
        for prop in (FEDERAL.prosecutedBy, FEDERAL.investigatedBy,
                     FEDERAL.defendedBy, FEDERAL.victimizedBy):
            with self.subTest(prop=prop):
                conforms, report = self.conforms(
                    FEDERAL.EventParticipationValidationShape,
                    FEDERAL.ChildPornographyPossession, prop,
                )
                self.assertTrue(conforms, report)

    def test_forensic_event_does_not_require_federal_participation(self):
        conforms, report = self.conforms(
            FEDERAL.EventParticipationValidationShape, FORENSICS.ForensicAcquisitionAction,
        )
        self.assertTrue(conforms, report)

    def test_federal_event_does_not_require_forensic_participation(self):
        conforms, report = self.conforms(
            FORENSICS.ForensicEventParticipationShape, FEDERAL.ChildPornographyPossession,
        )
        self.assertTrue(conforms, report)

    def test_grooming_and_other_domains_do_not_require_each_others_participants(self):
        for other_shape, other_event in (
            (FORENSICS.ForensicEventParticipationShape, FORENSICS.ForensicAcquisitionAction),
            (FEDERAL.EventParticipationValidationShape, FEDERAL.ChildPornographyPossession),
        ):
            for shape, event_type in (
                (GROOMING.GroomingEventParticipationShape, other_event),
                (other_shape, GROOMING.GroomingBehavior),
            ):
                with self.subTest(shape=shape, event_type=event_type):
                    conforms, report = self.conforms(shape, event_type)
                    self.assertTrue(conforms, report)

    def test_wrong_domain_participant_does_not_satisfy_the_rule(self):
        for shape, event_type, prop in (
            (FORENSICS.ForensicEventParticipationShape,
             FORENSICS.ForensicAcquisitionAction, FEDERAL.prosecutedBy),
            (FEDERAL.EventParticipationValidationShape,
             FEDERAL.ChildPornographyPossession, FORENSICS.examinedBy),
            (GROOMING.GroomingEventParticipationShape,
             GROOMING.GroomingBehavior, FORENSICS.examinedBy),
            (GROOMING.GroomingEventParticipationShape,
             GROOMING.GroomingBehavior, FEDERAL.prosecutedBy),
            (FORENSICS.ForensicEventParticipationShape,
             FORENSICS.ForensicAcquisitionAction, GROOMING.performedBy),
            (FEDERAL.EventParticipationValidationShape,
             FEDERAL.ChildPornographyPossession, GROOMING.performedBy),
        ):
            with self.subTest(shape=shape):
                conforms, report = self.conforms(shape, event_type, prop)
                self.assertFalse(conforms, report)

    def test_phase_inheriting_a_targeted_process_keeps_existing_requirement(self):
        for event_type in (
            FEDERAL.PreTrialPhase, FEDERAL.TrialPhase,
            FEDERAL.SentencingPhase, FEDERAL.PostConvictionPhase,
        ):
            with self.subTest(event_type=event_type):
                conforms, report = self.conforms(
                    FEDERAL.EventParticipationValidationShape, event_type,
                )
                self.assertFalse(conforms, report)

    def test_multi_domain_events_keep_each_domains_participation_requirement(self):
        domains = (
            (FORENSICS.ForensicEventParticipationShape,
             FORENSICS.ForensicAcquisitionAction, FORENSICS.examinedBy),
            (FEDERAL.EventParticipationValidationShape,
             FEDERAL.ChildPornographyPossession, FEDERAL.prosecutedBy),
            (GROOMING.GroomingEventParticipationShape,
             GROOMING.GroomingBehavior, GROOMING.performedBy),
        )
        for first, second in combinations(domains, 2):
            shapes = self.shapes[first[0]] + self.shapes[second[0]]
            owners = {
                prop: shape for shape in (first[0], second[0])
                for prop in shapes.objects(shape, SH.property)
            }
            for supplied in ((), (first,), (second,), (first, second)):
                data = Graph()
                for _, event_type, _ in (first, second):
                    data.add((EX.event, RDF.type, event_type))
                for _, _, participant in supplied:
                    data.add((EX.event, participant, EX.actor))
                expected = {first[0], second[0]} - {domain[0] for domain in supplied}
                with self.subTest(first=first[0], second=second[0], supplied=supplied):
                    conforms, report, text = self.validate_data(data, shapes)
                    results = list(report.subjects(RDF.type, SH.ValidationResult))
                    actual = {owners[report.value(result, SH.sourceShape)] for result in results}
                    self.assertEqual(expected, actual, text)
                    self.assertEqual(len(expected), len(results), text)
                    self.assertEqual(not expected, conforms, text)

    def test_grooming_phases_do_not_require_event_participation(self):
        phases = {
            term for term in self.ontology.subjects(RDF.type, OWL.Class)
            if str(term).startswith(str(GROOMING))
            and CORE.Phase in self.ontology.transitive_objects(term, RDFS.subClassOf)
        }
        self.assertIn(GROOMING.ConditioningPhase, phases)
        for phase in phases:
            with self.subTest(phase=phase):
                conforms, report = self.conforms(GROOMING.GroomingEventParticipationShape, phase)
                self.assertTrue(conforms, report)

    def test_grooming_process_composition_still_requires_event_behavior(self):
        # GroomingProcess has a shipped shape but no declared Event ancestry.
        shapes = self.grooming_shapes.cbd(GROOMING.GroomingProcessCompositionShape)
        for behavior_type, expected in (
            (None, False), (GROOMING.GroomingBehavior, True),
            (GROOMING.ConditioningPhase, False),
        ):
            data = Graph()
            data.add((EX.process, RDF.type, GROOMING.GroomingProcess))
            if behavior_type is not None:
                data.add((EX.process, GROOMING.hasGroomingBehavior, EX.behavior))
                data.add((EX.behavior, RDF.type, behavior_type))
            with self.subTest(behavior_type=behavior_type):
                conforms, _, report = self.validate_data(data, shapes)
                self.assertEqual(expected, conforms, report)

    def test_conditioning_phase_requirements_are_preserved(self):
        shapes = self.grooming_shapes.cbd(GROOMING.ConditioningPhaseShape)
        for dual_type, label, mode, expected in (
            (True, True, "deception", True),
            (False, True, "deception", False),
            (True, False, "deception", False),
            (True, True, "invalid_mode", False),
        ):
            data = Graph()
            data.add((EX.phase, RDF.type, GROOMING.ConditioningPhase))
            if dual_type:
                data.add((EX.phase, RDF.type, CORE.Phase))
            if label:
                data.add((EX.phase, RDFS.label, Literal("Synthetic phase")))
            data.add((EX.phase, CORE.conditioningMode, Literal(mode)))
            with self.subTest(dual_type=dual_type, label=label, mode=mode):
                conforms, _, report = self.validate_data(
                    data, shapes, inference="none", include_hierarchy=False,
                )
                self.assertEqual(expected, conforms, report)

    def test_full_grooming_shapes_allow_unrelated_support_events(self):
        for event_types, inference, include_hierarchy in (
            ((CORE.SupportEvent, CORE.Event), "none", False),
            ((IMPACT.VictimSupport,), "rdfs", True),
        ):
            data = Graph()
            for event_type in event_types:
                data.add((EX.event, RDF.type, event_type))
            with self.subTest(event_types=event_types):
                conforms, _, report = self.validate_data(
                    data, self.grooming_shapes, inference=inference,
                    include_hierarchy=include_hierarchy,
                )
                self.assertTrue(conforms, report)

    def test_account_replacement_example_uses_declared_cac_vocabulary(self):
        # A SHACL path reference does not declare an RDF property. Check the
        # published example's CAC predicates and class roles against the shipped
        # ontology, independently of inference and participation cardinality.
        declarations = Graph()
        for filename in ("cacontology-core-spine.ttl", "cacontology-grooming.ttl"):
            declarations.parse(ROOT / "ontology" / filename, format="turtle")
        data = Graph().parse(
            ROOT / "examples_knowledge_graphs" / "caselinker-account-replacement-example.ttl",
            format="turtle",
        )
        missing_properties, missing_classes = undeclared_cac_vocabulary(data, declarations)
        self.assertEqual(set(), missing_properties, "Undeclared CAC example predicates")
        self.assertEqual(set(), missing_classes, "Undeclared CAC example classes")

    def test_cac_vocabulary_check_rejects_wrong_roles_and_path_only_terms(self):
        declarations = Graph()
        declarations.add((GROOMING.GroomingBehavior, RDF.type, OWL.Class))
        declarations.add((GROOMING.targetsVictim, RDF.type, OWL.ObjectProperty))
        # A path reference must never satisfy a property declaration check.
        declarations.add((EX.shape, SH.path, GROOMING.undeclaredParticipant))
        valid = Graph()
        valid.add((EX.event, RDF.type, GROOMING.GroomingBehavior))
        valid.add((EX.event, GROOMING.targetsVictim, EX.actor))
        self.assertEqual((set(), set()), undeclared_cac_vocabulary(valid, declarations))
        invalid = Graph()
        invalid.add((EX.event, GROOMING.GroomingBehavior, EX.actor))
        invalid.add((EX.event, GROOMING.undeclaredParticipant, EX.actor))
        invalid.add((EX.event, RDF.type, GROOMING.targetsVictim))
        self.assertEqual(
            ({str(GROOMING.GroomingBehavior), str(GROOMING.undeclaredParticipant)},
             {str(GROOMING.targetsVictim)}),
            undeclared_cac_vocabulary(invalid, declarations),
        )

    def test_account_replacement_example_keeps_participation_requirement(self):
        data = Graph().parse(
            ROOT / "examples_knowledge_graphs" / "caselinker-account-replacement-example.ttl",
            format="turtle",
        )
        events = list(data.subjects(RDF.type, GROOMING.AccountReplacementEvent))
        self.assertEqual(1, len(events))
        event = events[0]
        performers = list(data.objects(event, GROOMING.performedBy))
        self.assertEqual(1, len(performers))
        performer = performers[0]
        self.assertTrue(str(performer).startswith("urn:uuid:"))
        self.assertEqual(5, UUID(str(performer).removeprefix("urn:uuid:")).version)
        self.assertIn((performer, RDF.type, IDENTITY.Person), data)
        self.assertTrue(any("fictional" in str(label).lower()
                            for label in data.objects(performer, RDFS.label)))

        conforms, _, text = self.validate_data(
            data, self.grooming_shapes, inference="none", include_hierarchy=False,
        )
        self.assertTrue(conforms, text)

        # Remove participation only: the otherwise-valid example must fail
        # specifically on the retained participation cardinality constraint.
        for prop in GROOMING_PARTICIPANTS:
            data.remove((event, prop, None))
        conforms, report, text = self.validate_data(
            data, self.grooming_shapes, inference="none", include_hierarchy=False,
        )
        self.assertFalse(conforms, text)
        results = list(report.subjects(RDF.type, SH.ValidationResult))
        self.assertEqual(1, len(results), text)
        result = results[0]
        self.assertEqual(event, report.value(result, SH.focusNode), text)
        self.assertEqual(SH.MinCountConstraintComponent,
                         report.value(result, SH.sourceConstraintComponent), text)
        self.assertIn(
            (GROOMING.GroomingEventParticipationShape, SH.property,
             report.value(result, SH.sourceShape)),
            self.grooming_shapes,
        )


if __name__ == "__main__":
    unittest.main()
