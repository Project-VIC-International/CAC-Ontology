# CAC Ontology Semantic Spine Refactoring Proposal for CAC Ontology v3.0.0

## Status

This is a revised proposal that incorporates follow-on review feedback, including explicit treatment of:

* `uco-core:UcoObject`
* `gufo:Object`
* existing `owl:equivalentClass` axioms
* the current `cacontology-gufo:` namespace
* the `cacontology-temporal:` layer
* `AICSAMInvestigation`
* backward compatibility for existing instance data and queries
* versioning of the semantic spine
* more explicit guidance on what should **not** be modeled as an OWL class

---

# Purpose

This document proposes a concrete refactoring approach for CAC Ontology so that:

1. the subclassing hierarchy better reflects the real world,
2. adoption is easier for new implementers,
3. CAC remains aligned with gUFO, CASE Ontology, and Unified Cyber Ontology where appropriate,
4. AI-assisted application builders can more reliably discover the right namespaces, classes, properties, relationships, and SHACL shapes from the published documentation,
5. independently built applications are more likely to be semantically interoperable with each other.

This proposal does **not** narrow CAC Ontology to one stakeholder group. The goal is to support the full Crimes Against Children domain of discourse, including but not limited to:

* investigators
* forensic examiners
* prosecutors
* victim advocates and support organizations
* hotline and intake personnel
* platform trust and safety teams
* educators and researchers
* NGOs and nonprofits
* intelligence and analysis teams
* policy and compliance teams
* software vendors and integrators
* AI agent development tools

---

# Executive Summary

CAC Ontology should adopt a **semantic spine** that is organized first by **ontological kind** rather than by stakeholder workflow or module-local convenience.

The semantic spine should preserve and strengthen alignment with:

* **gUFO** for foundational distinctions such as object, event, situation, role, phase, relator, and type hierarchy semantics
* **CASE Ontology** for investigation-specific concepts, especially `case-investigation:InvestigativeAction` and related structures
* **Unified Cyber Ontology (UCO)** for cross-domain cyber and digital evidence concepts such as identities, observables, actions, tools, locations, relationships, and common semantic infrastructure

The key modeling principle is:

> Every class should have one clear ontological home, one clear identity story, and one intended modeling pattern.

That means:

* if it is something that happens, it should live under an event/action branch
* if it is a context or condition that holds, it should live under a situation branch
* if it is a temporary capacity or social function borne by an entity, it should live under a role branch
* if it is a lifecycle stage, it should live under a phase branch
* if it is a person, organization, device, account, file, document, image, place, or platform object, it should live under an enduring-entity branch
* if it is an analytic conclusion, score, classification, decision, or assessment outcome, it should live under an assessment/result branch

This document recommends retaining subclassing from gUFO, CASE, and UCO **where appropriate**, but in a more disciplined, documented, and predictable way.

---

# Design Goals

## Primary goals

1. **Reflect reality better**

   * the top-level hierarchy should mirror the actual kinds of things in the CAC domain
   * avoid making phases look like investigations, results look like artifacts, or roles look like people

2. **Improve adoption**

   * new users should be able to start with a small number of stable, documented classes
   * implementers should not need to understand the full ontology to build semantically valid applications

3. **Improve semantic interoperability**

   * independent applications built from CAC documentation should converge on the same modeling patterns
   * the ontology should make it easier for different applications to exchange data without semantic drift

4. **Support AI-assisted implementation**

   * the public documentation should be understandable not just to experts but also to LLM-based coding and ontology agents
   * class pages should be structured to reduce ambiguity about what to use and why

5. **Retain foundational alignment**

   * continue subclassing from gUFO, CASE, and UCO where each is actually the right semantic fit

6. **Protect existing adopters**

   * existing graphs, examples, SPARQL queries, and integrations should have a documented migration path
   * the refactor should improve the ontology without causing avoidable semantic breakage

## Non-goals

This proposal is not trying to:

* replace gUFO, CASE, or UCO
* collapse all modules into one flat namespace
* remove domain richness
* eliminate multiple inheritance entirely
* overfit the ontology to investigator workflows only
* convert every operational concept into a heavyweight OWL pattern

---

# Core Problem Statement

The current CAC Ontology is rich and ambitious, but some parts of the subclassing structure make it harder for both people and AI agents to infer the intended modeling pattern.

## Current issues this proposal addresses

### 1. Mixed ontological categories

Some classes currently appear to mix categories such as:

* event vs action
* investigation vs phase
* artifact vs analytic result
* generated content vs altered content vs subtype of deepfake
* role vs person vs participant identity

### 2. Signal leakage through inheritance

Because the published documentation shows inherited properties and SHACL constraints on class pages, superclassing choices directly affect what users and AI agents think a class is supposed to do.

If a class is placed under the wrong parent, it may inherit:

* irrelevant properties
* misleading SHACL constraints
* confusing domain/range implications
* an overly broad or incorrect application contract

### 3. Inconsistent entry points for implementers

New adopters need a stable semantic starting point. Without it, different implementers may choose different branches for the same concept and create semantically incompatible applications.

### 4. Overuse of subclassing for concepts better represented as results, classifications, or controlled values

Not every category should become a new OWL class. Some concepts are better represented as:

* assessment results
* SKOS concepts
* controlled individuals
* property values
* mapping layer concepts

### 5. UCO core alignment is currently under-specified in the earlier draft

A very large portion of CAC’s current class structure sits in or near the UCO class lattice, especially through `uco-core:UcoObject`, `uco-observable:ObservableObject`, and related branches. The semantic spine must preserve that continuity rather than accidentally bypass it.

---

# Proposed Semantic Spine

The semantic spine is the stable, top-level CAC-facing class hierarchy that all modules should anchor to.

It should be designed to reflect the world first, while still aligning to gUFO, CASE, and UCO.

## Top-level semantic spine

```text
cac-core:Entity
  cac-core:EnduringEntity
    cac-core:PersonLikeEntity
    cac-core:OrganizationLikeEntity
    cac-core:DigitalSystemEntity
    cac-core:Artifact
    cac-core:PlaceLikeEntity
    cac-core:AssessmentResult

  cac-core:Occurrent
    cac-core:Event
      cac-core:ExploitationEvent
      cac-core:DetectionEvent
      cac-core:CoordinationEvent
      cac-core:SupportEvent
      cac-core:LegalEvent
      cac-core:InvestigativeAction

  cac-core:Situation
  cac-core:Role
  cac-core:Phase
```

## Intended semantics of each branch

### `cac-core:EnduringEntity`

A thing that persists through time while potentially changing state.

Examples:

* person
* child
* offender
* organization
* task force
* nonprofit
* online platform account
* digital device
* image file
* video file
* report
* hotline tip document

### `cac-core:PersonLikeEntity`

An enduring entity that is person-like in the domain model.

Use for:

* natural persons
* person abstractions or person-profile entities where appropriate

Do not use for:

* temporary capacities such as victim, offender, moderator, guardian, or advocate
* those belong under `cac-core:Role`

### `cac-core:OrganizationLikeEntity`

An enduring entity that represents an organization, institution, team, agency, or other collectively organized actor.

Use for:

* NGOs
* task forces
* police departments
* courts
* companies
* platforms treated as organizations

### `cac-core:DigitalSystemEntity`

An enduring entity representing a software or system-level resource.

Use for:

* online service platforms
* moderation systems
* application services
* digital environments
* platform subsystems

This class should not replace more specific UCO observable/device/software classes where those are already the right fit. It is a stable CAC-facing anchor.

### `cac-core:Artifact`

An enduring entity that is inspectable, storable, transferable, or evidentiary.

Examples:

* file
* image
* video
* report document
* extracted transcript
* cybertip message
* account export

### `cac-core:PlaceLikeEntity`

An enduring entity used to represent places, venues, virtual environments treated as locatable contexts, or place-like reference points.

### `cac-core:Occurrent`

A CAC organizing superclass for things that happen or unfold in time.

Important note:

* `cac-core:Occurrent` is intentionally a CAC-layer abstraction
* it is **not** directly mapped to a gUFO superclass in the base spine because the practical implementation emphasis in gUFO is on `gufo:Event` and `gufo:Situation`
* if the project later chooses to import or define a suitable perdurant-like abstraction, that can be added in a bridge layer

### `cac-core:Event`

Something that happens or unfolds in time.

Examples:

* grooming interaction
* abuse incident
* evidence review
* content classification event
* information sharing event
* victim rescue action
* judicial hearing

### `cac-core:Situation`

A context, state, or configuration that holds at a time and may involve multiple participants.

Examples:

* high-risk victim situation
* active multi-agency coordination situation
* child under coercive control situation
* ongoing online exploitation exposure situation
* custody transfer situation
* age-at-time situation

### `cac-core:Role`

A non-rigid role borne by an enduring entity in a certain relational or contextual setting.

Examples:

* victim role
* offender role
* guardian role
* moderator role
* examiner role
* reporter role
* investigator role
* advocate role

### `cac-core:Phase`

A temporal stage of some enduring entity, process, or situation.

Examples:

* grooming phase
* escalation phase
* active investigation phase
* victim identification phase
* victim support phase
* prosecution phase

### `cac-core:AssessmentResult`

An output or conclusion of some evaluative, analytic, classification, or decision-making process.

Examples:

* content classification result
* risk assessment result
* age estimation result
* grooming indicator result
* victim impact assessment result
* moderation decision
* authenticity assessment result

---

# Alignment Strategy with gUFO, CASE, and UCO

## Principle

CAC should subclass from gUFO, CASE, and UCO **where each is actually the best semantic fit**.

The semantic spine is a CAC-facing organizational layer, not a replacement for foundational or interoperable external ontologies.

## Recommended alignment pattern

### Use gUFO for foundational category semantics

Use gUFO for classes whose core meaning is ontological in nature.

Recommended direct or indirect alignment:

* `cac-core:EnduringEntity` subclass of `gufo:Object`
* `cac-core:Event` subclass of `gufo:Event`
* `cac-core:Situation` subclass of `gufo:Situation`
* `cac-core:Role` subclass of `gufo:Role`
* `cac-core:Phase` subclass of `gufo:Phase`
* relator-like constructs aligned to `gufo:Relator` when warranted
* event types aligned to `gufo:EventType` if a true type-level classification is intended

### Use CASE for investigation semantics

Use CASE where the class specifically participates in investigation modeling.

Recommended direct alignment:

* `cac-core:InvestigativeAction` subclass of `case-investigation:InvestigativeAction`
* investigation-specific objects aligned to CASE investigation classes when appropriate
* provenance of investigative steps aligned with CASE/UCO action patterns

### Use UCO for shared cyber, digital, and evidence semantics

Use UCO for common cross-domain digital constructs.

Recommended direct or indirect alignment:

* `cac-core:EnduringEntity` subclass of `uco-core:UcoObject`
* artifact classes aligned to `uco-observable:ObservableObject` where appropriate
* people and organizations aligned with UCO identity concepts where appropriate
* actions aligned with `uco-action:Action` when the action-oriented semantics are relevant
* devices, files, accounts, locations, tools, relationships, and identifiers aligned with the proper UCO branches

## Important modeling constraint

Do **not** use CASE or UCO merely because a term is operational. Use them because they provide the correct semantic abstraction.

Examples:

* `EvidenceReviewAction` should align to CASE and UCO action semantics
* `VictimRole` should align primarily to gUFO role semantics and secondarily to UCO role semantics if appropriate
* `ClassificationResult` should not be modeled primarily as an observable object simply because it is digitally represented
* `VictimSupportPhase` should not subclass investigation just because it participates in an investigation lifecycle

---

# Explicit Treatment of `uco-core:UcoObject`

This proposal now makes the UCO alignment explicit.

## Decision

`cac-core:EnduringEntity` should absorb the semantic role of a CAC-facing enduring root **while remaining explicitly aligned to** `uco-core:UcoObject`.

## Rationale

* many existing CAC classes already inherit from `uco-core:UcoObject`
* many inherited UCO properties and SHACL expectations are organized through that branch
* omitting the UCO root alignment would make the semantic spine feel detached from a large body of existing CAC content

## Rule

Use this explicit alignment in the core spine:

```turtle
cac-core:EnduringEntity a owl:Class ;
  rdfs:subClassOf cac-core:Entity , gufo:Object , uco-core:UcoObject .
```

This preserves continuity with current UCO-based modeling and makes the foundational identity of enduring entities explicit.

---

# Proposed Core Namespace Structure and Versioning

## Versioning policy

This refactor should be released as **v3.0.0**.

Rationale:

* the semantic spine introduces a new top-level structural layer
* several hierarchy corrections are materially breaking or semantically significant
* the AI content branch includes a documented hierarchy inversion
* phase classes currently mis-modeled as investigations are being corrected
* bridge-layer treatment of some existing equivalence axioms changes the reasoning surface

The semantic spine should be versioned consistently with the main ontology release train.

Recommended pattern:

* stable namespace for human-friendly use and imports
* version IRI for released snapshots

Example:

```text
Stable namespace:
https://cacontology.projectvic.org/core#

Version IRI example:
https://cacontology.projectvic.org/core/2.13.0
```

If the existing project convention prefers release-root versioning such as `https://cacontology.projectvic.org/2.12.0`, the semantic spine should still publish a stable namespace and an explicit version IRI tied to the release.

## Core namespaces

```text
https://cacontology.projectvic.org/core#
https://cacontology.projectvic.org/bridge/gufo#
https://cacontology.projectvic.org/bridge/case#
https://cacontology.projectvic.org/bridge/uco#
https://cacontology.projectvic.org/profile/core#
https://cacontology.projectvic.org/profile/investigation#
https://cacontology.projectvic.org/profile/advanced#
```

## Domain namespaces remain modular

Existing and future domain modules should remain distinct, such as:

* grooming
* detection
* coordination
* prosecution
* victim support
* sentencing
* trafficking
* AI-generated content
* hotline/reporting
* platform safety
* education/training
* temporal

Each domain namespace should anchor its classes into the shared semantic spine.

---

# Relationship to Existing `cacontology-gufo:` Namespace

There is already a `cacontology-gufo:` namespace with custom classes and properties related to gUFO-aligned modeling.

## Decision

The existing `cacontology-gufo:` namespace should **not** be abruptly removed.

## Recommended migration path

### Short term

* keep `cacontology-gufo:` in place
* treat it as the legacy gUFO alignment layer
* document how its classes map into the new semantic spine and new bridge modules

### Medium term

* introduce `bridge/gufo#` as the preferred place for new bridge axioms and alignment statements
* retain legacy IRIs where practical
* add deprecation notices only where there is clear replacement guidance

### Long term

* either:

  * merge the semantic role of `cacontology-gufo:` into the new bridge layer while preserving old IRIs, or
  * keep both namespaces but document one as authoritative for new development

## Practical guidance

* existing classes like `cacontology-gufo:CriminalEvent`, `cacontology-gufo:VictimRole`, and `cacontology-gufo:OffenderRole` should be reviewed individually
* where they are stable and useful, they can remain as bridge or mapping resources
* where they duplicate the new semantic-spine branches, they should be documented as legacy-alignment constructs rather than new primary modeling entry points

---

# Proposed Core Class Definitions

Below is a recommended starting point for the semantic spine with subclassing from gUFO, CASE, and UCO where appropriate.

```turtle
@prefix cac-core: <https://cacontology.projectvic.org/core#> .
@prefix gufo: <http://purl.org/nemo/gufo#> .
@prefix case-investigation: <https://ontology.caseontology.org/case/investigation/> .
@prefix uco-core: <https://ontology.unifiedcyberontology.org/uco/core/> .
@prefix uco-action: <https://ontology.unifiedcyberontology.org/uco/action/> .
@prefix uco-observable: <https://ontology.unifiedcyberontology.org/uco/observable/> .
@prefix uco-role: <https://ontology.unifiedcyberontology.org/uco/role/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

cac-core:Entity a owl:Class .

cac-core:EnduringEntity a owl:Class ;
  rdfs:subClassOf cac-core:Entity , gufo:Object , uco-core:UcoObject .

cac-core:PersonLikeEntity a owl:Class ;
  rdfs:subClassOf cac-core:EnduringEntity .

cac-core:OrganizationLikeEntity a owl:Class ;
  rdfs:subClassOf cac-core:EnduringEntity .

cac-core:DigitalSystemEntity a owl:Class ;
  rdfs:subClassOf cac-core:EnduringEntity .

cac-core:PlaceLikeEntity a owl:Class ;
  rdfs:subClassOf cac-core:EnduringEntity .

cac-core:Occurrent a owl:Class ;
  rdfs:subClassOf cac-core:Entity .

cac-core:Event a owl:Class ;
  rdfs:subClassOf cac-core:Occurrent , gufo:Event .

cac-core:Situation a owl:Class ;
  rdfs:subClassOf cac-core:Entity , gufo:Situation .

cac-core:Role a owl:Class ;
  rdfs:subClassOf cac-core:Entity , gufo:Role , uco-role:Role .

cac-core:Phase a owl:Class ;
  rdfs:subClassOf cac-core:Entity , gufo:Phase .

cac-core:Artifact a owl:Class ;
  rdfs:subClassOf cac-core:EnduringEntity , uco-observable:ObservableObject .

cac-core:AssessmentResult a owl:Class ;
  rdfs:subClassOf cac-core:EnduringEntity .

cac-core:InvestigativeAction a owl:Class ;
  rdfs:subClassOf cac-core:Event , case-investigation:InvestigativeAction , uco-action:Action .

cac-core:ExploitationEvent a owl:Class ;
  rdfs:subClassOf cac-core:Event .

cac-core:DetectionEvent a owl:Class ;
  rdfs:subClassOf cac-core:Event .

cac-core:CoordinationEvent a owl:Class ;
  rdfs:subClassOf cac-core:Event .

cac-core:SupportEvent a owl:Class ;
  rdfs:subClassOf cac-core:Event .

cac-core:LegalEvent a owl:Class ;
  rdfs:subClassOf cac-core:Event .
```

## Note on `AssessmentResult`

`AssessmentResult` is intentionally *not* subclassed from `uco-observable:ObservableObject` by default.

Reason:

* many results are represented in files or database rows, but their semantic identity is not the same as the artifact that stores them
* some results may later be materialized as documents, reports, or digital messages, but the result itself is the assessment outcome

If needed, a separate class can model a result-bearing document or artifact.

---

# Treatment of `owl:equivalentClass` Axioms

The earlier draft said these should be reviewed. This revision makes the policy explicit.

## Decision

Existing `owl:equivalentClass` axioms should be classified into three buckets:

### Bucket A: Keep in the reference layer

Use only when the equivalence is truly identity-level, stable, and unlikely to surprise downstream users.

### Bucket B: Move to bridge or advanced profile modules

Use when the equivalence is semantically defensible but operationally strong enough to create unwanted inference propagation in general-purpose consuming applications.

### Bucket C: Deprecate or replace with weaker alignment

Use when the equivalence collapses distinct concepts or creates more confusion than value.

## Recommended default posture

For most CAC-facing public documentation and starter profiles, prefer:

* `rdfs:subClassOf`
* `skos:exactMatch`
* `skos:closeMatch`
* bridge-layer axioms

rather than aggressive use of `owl:equivalentClass`.

## Example policy

* `ReceiveCybertipAction ≡ CriminalEvent` should be reviewed as a likely candidate for bridge-only treatment or weakening
* `VictimRole ≡ cacontology-gufo:VictimRole` may be acceptable if both classes really are intended as the same role-level class, but it should still be reviewed for redundancy and inference scope

## Migration guidance

Every current `owl:equivalentClass` axiom should receive a disposition annotation:

* `retainInReferenceLayer`
* `moveToBridgeLayer`
* `deprecateAndReplace`

---

# Modeling Rules for Subclassing

These rules should be part of contributor guidance and PR review.

## Rule 1: Every class must declare its ontological category

Every new class must explicitly declare whether it is primarily an:

* enduring entity
* event
* situation
* role
* phase
* assessment result

## Rule 2: Every class must have one primary direct parent in the CAC semantic spine

Even if a class also subclasses from gUFO, CASE, or UCO, it should still have one primary CAC semantic-spine parent.

## Rule 3: Multiple inheritance should be disciplined

Allowed when it truly adds meaning, but avoid letting a class inherit from multiple top-level conceptual branches that express conflicting identity stories.

Examples of problematic multiple inheritance:

* phase + investigation
* assessment result + artifact as primary identities
* role + person
* investigation + action when the class is actually intended as an enduring inquiry context rather than a single occurrence

Examples of acceptable multiple inheritance:

* `cac-core:InvestigativeAction` subclassing from `cac-core:Event`, `case-investigation:InvestigativeAction`, and `uco-action:Action`
* `cac:VictimRole` subclassing from `cac-core:Role` and a more specific UCO role class

## Rule 4: Use subclassing only when identity or inference depends on it

A new class should be created when the concept has stable semantic importance.

Do **not** create a new class when the concept is better represented as:

* a result value
* a status
* a confidence score
* a categorical label
* a SKOS concept
* a controlled individual

## Rule 5: Use SKOS or controlled individuals for operational taxonomies

Use SKOS for:

* triage labels
* severity levels
* reporting classifications
* moderation action categories
* sharing mechanism types
* analyst shorthand
* configurable application categories

## Rule 6: Preserve bridge-layer semantics separately when needed

If a stronger alignment to gUFO, CASE, or UCO is useful for advanced reasoning, place some of those axioms in bridge or advanced profile modules rather than overloading the public reference layer.

## Rule 7: Check for existing SKOS overlap

Before adding a new OWL class, contributors must answer:

* does this class duplicate or overlap with an existing SKOS concept scheme?
* would a concept scheme or controlled value preserve more agility while avoiding class explosion?

---

# Recommended Modeling Patterns

## Pattern A: Event

Use when something happens or unfolds in time.

Questions to ask:

* did something occur?
* can it have a start/end time?
* does it involve participants, inputs, outputs, or instruments?

Examples:

* `InformationSharing`
* `VictimRescueAction`
* `EvidenceReviewAction`
* `GroomingInteraction`
* `JudicialHearing`

## Pattern B: Situation

Use when representing a context or condition that holds.

Questions to ask:

* is this a state rather than an occurrence?
* does it hold over some interval?
* does it contextualize participants or events?

Examples:

* `HighRiskVictimSituation`
* `CrossPlatformExposureSituation`
* `CustodialControlSituation`
* `ActiveCaseCoordinationSituation`
* `AgeAtTimeSituation`

## Pattern C: Role

Use when an entity plays a context-dependent function.

Questions to ask:

* can the bearer gain or lose this without ceasing to exist?
* does the role depend on a relation, context, or institution?

Examples:

* `VictimRole`
* `OffenderRole`
* `GuardianRole`
* `ModeratorRole`
* `ReporterRole`

## Pattern D: Phase

Use for lifecycle stages of a thing, process, or condition.

Questions to ask:

* is this a stage in the history of something else?
* does the bearer remain the same entity while changing phase?

Examples:

* `VictimIdentificationPhase`
* `EscalationPhase`
* `RecoveryPhase`
* `ActiveInvestigationPhase`

## Pattern E: AssessmentResult

Use for outputs of analysis, classification, scoring, decision, or evaluation.

Questions to ask:

* is this the result of assessing something?
* can the assessed thing remain the same even if the result changes?
* would it be misleading to model this as the object assessed?

Examples:

* `ClassificationResult`
* `RiskAssessmentResult`
* `AuthenticityAssessmentResult`
* `VictimImpactAssessmentResult`
* `ModerationDecision`

## Pattern F: Artifact

Use for digital or physical objects that endure through time and may be observed, stored, transferred, or examined.

Examples:

* image file
* video file
* cybertip report document
* chat transcript
* phone image
* hash set export
* moderation report PDF

---

# Proposed High-Level Domain Mapping into the Semantic Spine

## People and institutions

* child -> person-like entity
* caregiver -> person-like entity
* offender -> person-like entity
* nonprofit -> organization-like entity
* task force -> organization-like entity
* platform -> digital system entity or organization-like entity depending on intent
* hotline -> organization-like entity or service system entity depending on modeling choice

## Roles

* victim role -> role
* offender role -> role
* guardian role -> role
* examiner role -> role
* moderator role -> role
* reporter role -> role
* advocate role -> role
* rescuer role -> role

## Events and actions

* grooming interaction -> exploitation event
* abuse incident -> exploitation event
* trafficking transfer event -> exploitation event
* evidence review action -> investigative action
* cybertip intake action -> investigative action or coordination event depending on design intent
* information sharing -> coordination event
* victim rescue action -> support event or investigative action depending on intended framing
* judicial hearing -> legal event
* training session -> support event or coordination event

## Situations

* child under coercive control -> situation
* high-risk victim situation -> situation
* multi-agency case coordination in progress -> situation
* platform exposure situation -> situation
* age-at-time situation -> situation

## Phases

* grooming phase -> phase
* escalation phase -> phase
* active investigation phase -> phase
* victim identification phase -> phase
* victim support phase -> phase
* prosecution phase -> phase

## Results and decisions

* classification result -> assessment result
* age estimate -> assessment result
* confidence score -> datatype on an assessment result, unless explicitly reified
* moderation decision -> assessment result
* victim impact assessment -> assessment result

## Artifacts

* CSAM image file -> artifact
* AIGeneratedCSAM media item -> artifact
* AIAlteredCSAM media item -> artifact
* cybertip PDF -> artifact
* extracted chat log -> artifact
* forensic report -> artifact

---

# Concrete Refactoring Recommendations for Current CAC Areas

## 1. Phase classes should never subclass investigation classes

### Problem

A phase is a temporal stage, not an investigation itself.

### Recommendation

Refactor any phase-like class to subclass `cac-core:Phase` and `gufo:Phase`, not an investigation class.

### Proposed pattern

```turtle
@prefix cac: <https://cacontology.projectvic.org#> .
@prefix cac-core: <https://cacontology.projectvic.org/core#> .
@prefix gufo: <http://purl.org/nemo/gufo#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

cac:VictimSupportPhase
  rdfs:subClassOf cac-core:Phase , gufo:Phase .

cac:VictimIdentificationPhase
  rdfs:subClassOf cac:VictimSupportPhase .

cac:VictimRescuePhase
  rdfs:subClassOf cac:VictimSupportPhase .
```

### Supporting object properties

```turtle
@prefix owl: <http://www.w3.org/2002/07/owl#> .

cac-core:hasPhase a owl:ObjectProperty .
cac-core:isPhaseOf a owl:ObjectProperty .
```

## 2. Add a distinct assessment-result branch

### Problem

Many analytic outcomes are not themselves observable artifacts.

### Recommendation

Introduce `cac-core:AssessmentResult` and re-home current result-like classes under it.

### Proposed pattern

```turtle
@prefix cac-detection: <https://cacontology.projectvic.org/detection#> .

cac-detection:ClassificationResult
  rdfs:subClassOf cac-core:AssessmentResult .

cac-detection:RiskAssessmentResult
  rdfs:subClassOf cac-core:AssessmentResult .

cac-detection:AgeAssessmentResult
  rdfs:subClassOf cac-core:AssessmentResult .

cac-detection:AuthenticityAssessmentResult
  rdfs:subClassOf cac-core:AssessmentResult .
```

### Supporting properties

```turtle
cac-core:assesses a owl:ObjectProperty .
cac-core:generatedBy a owl:ObjectProperty .
cac-core:hasConfidence a owl:DatatypeProperty .
cac-core:usesMethod a owl:ObjectProperty .
cac-core:issuedAtTime a owl:DatatypeProperty .
```

## 3. Rework AI-generated and AI-altered content into a cleaner artifact taxonomy

### Problem

A class like `AIAlteredCSAM` should not carry an unclear primary identity story.

### Recommendation

Place AI-generated and AI-altered media under an artifact branch, then use subclassing and controlled properties carefully.

### Proposed pattern

```turtle
@prefix cac-ai: <https://cacontology.projectvic.org/ai#> .

cac-ai:CSAMMediaArtifact
  rdfs:subClassOf cac-core:Artifact .

cac-ai:AIGeneratedCSAM
  rdfs:subClassOf cac-ai:CSAMMediaArtifact .

cac-ai:AIAlteredCSAM
  rdfs:subClassOf cac-ai:CSAMMediaArtifact .

cac-ai:DeepfakeCSAM
  rdfs:subClassOf cac-ai:AIAlteredCSAM .

cac-ai:NudifiedCSAM
  rdfs:subClassOf cac-ai:AIAlteredCSAM .

cac-ai:SyntheticCompositeCSAM
  rdfs:subClassOf cac-ai:AIAlteredCSAM .
```

### Breaking-change note

This proposal intentionally inverts the current problematic implication that all AI-altered CSAM is a deepfake.

#### Current problematic direction

* `AIGeneratedCSAM`

  * `DeepfakeCSAM`

    * `AIAlteredCSAM`

      * `NudifiedCSAM`

#### Proposed direction

* `CSAMMediaArtifact`

  * `AIGeneratedCSAM`
  * `AIAlteredCSAM`

    * `DeepfakeCSAM`
    * `NudifiedCSAM`
    * `SyntheticCompositeCSAM`

### Migration guidance

* existing instances of `AIAlteredCSAM` should be reviewed and retyped under the new branch
* existing rules or SPARQL patterns assuming `AIAlteredCSAM -> DeepfakeCSAM` must be updated
* documentation should clearly flag this as a hierarchy inversion, not a silent cleanup

### Supporting properties

```turtle
cac-ai:hasGenerationMethod a owl:ObjectProperty .
cac-ai:hasAlterationMethod a owl:ObjectProperty .
cac-ai:hasRealVictimLinkage a owl:DatatypeProperty .
cac-ai:hasAuthenticityAssessment a owl:ObjectProperty .
```

## 4. Keep investigation-specific actions aligned to CASE

### Recommendation

Where a class is truly an investigative action, continue subclassing from CASE and UCO action semantics through the CAC semantic spine.

### Proposed pattern

```turtle
@prefix cac: <https://cacontology.projectvic.org#> .

cac:EvidenceReviewAction
  rdfs:subClassOf cac-core:InvestigativeAction .

cac:ReceiveCybertipAction
  rdfs:subClassOf cac-core:InvestigativeAction .

cac:SearchWarrantExecutionAction
  rdfs:subClassOf cac-core:InvestigativeAction .
```

## 5. Allow non-investigative events to stay broad

Not every coordination or support activity should be forced into an investigative action branch.

### Proposed pattern

```turtle
@prefix cac-coord: <https://cacontology.projectvic.org/coord#> .

cac-coord:InformationSharing
  rdfs:subClassOf cac-core:CoordinationEvent , gufo:Event .

cac-support:VictimReferralEvent
  rdfs:subClassOf cac-core:SupportEvent , gufo:Event .

cac-legal:SentencingHearing
  rdfs:subClassOf cac-core:LegalEvent , gufo:Event .
```

## 6. Address `AICSAMInvestigation` explicitly

### Problem

If `AICSAMInvestigation` is currently modeled as `uco-action:Action` and `gufo:Event`, then the class is being treated as a single action-like occurrence. That appears inconsistent with its practical role when it serves as a container for investigative sub-activities such as generation-source tracking, model identification, and training-data analysis.

### Recommendation

Treat `AICSAMInvestigation` as an enduring investigation container aligned to CASE investigation semantics.

### Chosen pattern

```turtle
@prefix cac-ai: <https://cacontology.projectvic.org/ai#> .
@prefix cac-core: <https://cacontology.projectvic.org/core#> .
@prefix case-investigation: <https://ontology.caseontology.org/case/investigation/> .

cac-ai:AICSAMInvestigation
  rdfs:subClassOf cac-core:EnduringEntity , case-investigation:Investigation .
```

### Sub-activity pattern

Its investigative components should be modeled as `cac-core:InvestigativeAction` subclasses.

Example candidates:

* `GenerationSourceTracking`
* `ModelIdentification`
* `TrainingDataAnalysis`

### Implementation note

Do **not** leave this class semantically ambiguous in v3.0.0. The current action/event pattern should be retired unless there is a separate class representing a discrete AICSAM investigative act.

---

# Temporal Modeling and the `cacontology-temporal:` Namespace

The temporal framework should be treated as a first-class part of the semantic spine strategy.

## Recommendation

Existing temporal content should be reviewed and anchored into the spine as follows:

* temporal situation-like constructs -> `cac-core:Situation`
* temporal phases -> `cac-core:Phase`
* temporal events -> `cac-core:Event`
* age-at-time and similar contextual temporal state representations -> `cac-core:Situation`

## Example

`AgeAtTimeSituation` should naturally anchor under:

```turtle
cac-temporal:AgeAtTimeSituation
  rdfs:subClassOf cac-core:Situation .
```

## Guidance

The temporal namespace should continue to exist as a domain module, but its top-level classes should be made legible through the shared spine so that implementers and AI agents can immediately see whether a temporal concept is:

* a situation
* a phase
* an event
* an assessment result

---

# Specific Guidance for Key Current Classes

## `VictimRole`

### Recommendation

Keep the current role-oriented direction and re-anchor it explicitly into the semantic spine.

```turtle
cac:VictimRole
  rdfs:subClassOf cac-core:Role .
```

If there is a specific UCO victim role superclass that is semantically appropriate, retain it as an additional parent.

## `VictimPhase`

### Recommendation

Deprecate or refactor into one or more real phase classes under `cac-core:Phase`.

Suggested replacements:

* `VictimIdentificationPhase`
* `VictimRescuePhase`
* `VictimSupportPhase`
* `VictimRecoveryPhase`

## `ClassificationResult`

### Recommendation

Move under `cac-core:AssessmentResult`.

## `InformationSharing`

### Recommendation

Treat as a `CoordinationEvent`, not necessarily an investigative action unless the class is explicitly intended only for investigative contexts.

## `EvidenceReviewAction`

### Recommendation

Keep as `cac-core:InvestigativeAction` and therefore aligned to CASE and UCO action semantics.

## `AIAlteredCSAM`

### Recommendation

Give it one clear primary home under an artifact branch and avoid collapsing it with generated-content semantics unless that is truly intended.

## `AICSAMInvestigation`

### Recommendation

Review and re-home based on intended identity. Do not let the current event/action pattern persist by default.

---

# SHACL Design Guidance

## Principle

SHACL shapes should reinforce the semantic spine rather than accidentally redefine it.

## Recommendations

### 1. Provide starter shapes for each spine branch

At minimum, define starter shapes for:

* artifact
* event
* investigative action
* situation
* role
* phase
* assessment result

### 2. Distinguish core vs extended shapes

For each major class:

* one minimal shape for interoperability
* one richer profile shape for advanced applications

### 3. Avoid overconstraining inherited behavior

Inherited SHACL constraints should be carefully reviewed when superclassing changes, because the public docs expose them prominently.

### 4. Publish shape intent annotations

Add annotations such as:

* intended use
* required fields
* optional but recommended fields
* example instance link

### 5. Document backward-compatible shape transitions

When a class is re-homed under a new spine branch, publish migration notes for:

* deprecated shapes
* replacement shapes
* temporary compatibility shapes

---

# Documentation Changes for Human and AI Consumers

Because implementers may point AI agents directly at the public documentation, the docs themselves should be treated as part of the semantic interoperability layer.

## Required documentation improvements

### 1. Separate direct from inherited items

Every class page should clearly separate:

* direct superclasses
* inferred or additional superclasses
* direct properties
* inherited properties
* direct shapes
* inherited shapes

### 2. Add usage guidance annotations

Each important class should expose short annotations such as:

* use when
* do not use when
* common confusion with
* minimal required properties
* example JSON-LD or Turtle instance
* related shapes

### 3. Add a semantic-spine landing page

The docs should contain a clear entry page titled something like:

* Semantic Spine
* Core Modeling Patterns
* How to Choose the Right Class

### 4. Publish machine-readable starter packs

Provide a lightweight starter package containing:

* top classes
* top properties
* starter SHACL shapes
* JSON-LD context
* canonical examples

This should be easy for agents to ingest.

### 5. Add explicit migration callouts for breaking hierarchy changes

When the semantic meaning of a branch is inverted or significantly changed, the documentation should prominently say so.

---

# Contributor Checklist

Every new class PR should answer these questions.

## Ontological classification

1. Is this class an enduring entity, event, situation, role, phase, or assessment result?
2. What is the primary direct parent in the CAC semantic spine?
3. Why is that parent correct?

## External alignment

4. Should it also subclass from gUFO, CASE, or UCO?
5. Is that external alignment part of the public reference layer or a bridge layer?

## Identity and modeling choice

6. Does this concept warrant a new OWL class, or would a SKOS concept or controlled value be better?
7. What distinguishes this class from its siblings?
8. What is one positive example?
9. What is one negative example?
10. Does this class duplicate or overlap with an existing SKOS concept scheme?

## Documentation readiness

11. What is the short “use when” annotation?
12. What is the short “do not use when” annotation?
13. What minimal shape should be published for it?

---

# Backward Compatibility Policy

This proposal now makes backward compatibility explicit.

## Core principle

The refactor should preserve as much existing data usefulness as possible while correcting ontologically incorrect hierarchies.

## Commitments

### 1. Preserve existing IRIs where possible

* do not rename or remove heavily used classes without deprecation windows
* prefer re-parenting, bridge mappings, and annotations before hard deletion

### 2. Publish migration mappings

For each materially changed class, publish:

* old class IRI
* new preferred class or classes
* whether the change is non-breaking, soft-breaking, or breaking
* sample migration SPARQL Update or transformation guidance

### 3. Support existing instance data during transition

Example:

* existing instances typed as `cacontology:VictimPhase` should not simply become invalid
* they should either:

  * remain temporarily supported through compatibility mappings, or
  * be migrated to new phase classes with clear replacement guidance

### 4. Review existing examples and SPARQL queries

The codebase’s example knowledge graphs and SPARQL examples should be re-run against the updated hierarchy.

### 5. Provide compatibility layers

Where necessary, publish compatibility ontologies or bridge modules that preserve old reasoning expectations during transition.

# Implementation Decisions for v3.0.0

This section resolves the remaining design questions so implementation can begin without further architectural ambiguity.

## Decision 1: `AICSAMInvestigation`

`AICSAMInvestigation` should be treated as an **investigation or enduring inquiry container**, not as a single action.

### Chosen pattern

Use a CASE-aligned investigation/container pattern.

```turtle
@prefix cac-ai: <https://cacontology.projectvic.org/ai#> .
@prefix cac-core: <https://cacontology.projectvic.org/core#> .
@prefix case-investigation: <https://ontology.caseontology.org/case/investigation/> .

cac-ai:AICSAMInvestigation
  rdfs:subClassOf cac-core:EnduringEntity , case-investigation:Investigation .
```

### Consequence

Its current or future investigative sub-activities should instead be modeled as subclasses of `cac-core:InvestigativeAction`.

Examples:

* `GenerationSourceTracking`
* `ModelIdentification`
* `TrainingDataAnalysis`

These should no longer inherit their semantics from `AICSAMInvestigation` as though it were an action-like event. Instead, they participate *within* an investigation context.

### Rationale

This better reflects the apparent role of `AICSAMInvestigation` as a container for investigative work rather than a single discrete occurrence.

## Decision 2: Scope of re-anchoring in v3.0.0

v3.0.0 should do more than introduce the spine and re-anchor a few showcase classes.

### Chosen scope

In v3.0.0:

* introduce the semantic spine
* re-anchor all existing classes that are clearly `Phase`, `Role`, or `Situation` classes across all domain modules to their corresponding semantic-spine parent
* re-anchor priority event/action/result classes identified in this proposal
* perform the explicitly breaking hierarchy corrections called out in this proposal

### Why

For most `Phase`, `Role`, and `Situation` classes, adding a new `rdfs:subClassOf` link to the correct spine parent is additive and clarifying rather than destructive. Deferring that work would weaken the usefulness of the spine in the initial major release.

### Breaking vs additive distinction

The following are expected to be structurally or semantically breaking in v3.0.0:

* phase classes currently modeled as investigations and then corrected
* the AI content hierarchy inversion
* selected equivalence-axiom migrations to bridge layers

The following are primarily additive and should be done in v3.0.0 broadly:

* adding `cac-core:Phase` to phase classes
* adding `cac-core:Role` to role classes
* adding `cac-core:Situation` to situation classes

## Decision 3: `owl:equivalentClass` handling in v3.0.0

The v3.0.0 release should not postpone all equivalence handling, and it also should not require exhaustive manual redesign of all axioms before release.

### Chosen policy

For v3.0.0:

* move the most structurally impactful `cacontology-gufo:*` equivalence axioms into bridge modules immediately
* keep stable cross-namespace equivalences that are acting as identity mappings where they are well-justified
* annotate all reviewed equivalences with disposition metadata
* leave remaining non-critical equivalence axioms in place temporarily if they are not yet fully reviewed, but mark them for follow-up classification

### Practical guidance

The most likely immediate bridge candidates are equivalences involving:

* `cacontology-gufo:CriminalEvent`
* `cacontology-gufo:VictimRole`
* `cacontology-gufo:OffenderRole`
* similar `cacontology-gufo:*` alignment classes that strongly affect reasoning across the top of the lattice

### Disposition metadata

Each reviewed axiom should get one of:

* `retainInReferenceLayer`
* `moveToBridgeLayer`
* `deprecateAndReplace`
* `pendingReview`

## Decision 4: File organization

The semantic spine should be introduced as **new files**, not merged invisibly into the existing `cacontology-core.ttl`.

### Chosen structure

```text
ontology/
  cacontology-core-spine.ttl
  cacontology-core-spine-shapes.ttl
  cacontology-bridge-gufo.ttl
  cacontology-bridge-case.ttl
  cacontology-bridge-uco.ttl
```

### Rationale

Keeping the semantic spine separate makes it:

* easier to review
* easier to version and reference
* easier for AI agents and human contributors to identify as the canonical top-level semantic layer
* easier to import selectively in the future

### Implementation note

The existing `cacontology-core.ttl` should remain, but it should import or align to the spine explicitly rather than silently absorbing it. That preserves continuity while making the new architecture visible.

## Decision 5: Mechanical release updates

As part of the v3.0.0 work:

* update version references from `2.12.0` to `3.0.0`
* update any version automation or helper scripts accordingly
* ensure the new spine and bridge files are part of the release manifest and documentation generation

## Example migration note

If an existing graph contains:

```turtle
ex:vp1 a cacontology:VictimPhase .
```

Possible migration options include:

* retyping to `cac:VictimSupportPhase`
* asserting replacement hierarchy mappings
* keeping `cacontology:VictimPhase` as deprecated but still linked to the new phase branch during transition

---

# What Not to Model as a Class

This appendix is intentionally concrete.

## Use SKOS or controlled values instead of OWL classes when the concept is primarily:

* a configurable workflow label
* a local severity bucket
* a UI-facing filter category
* a confidence band
* a mechanism or method label that changes often
* a rapidly evolving analyst specialization label

## Candidate current examples to review

The following kinds of concepts should be reviewed for possible conversion from OWL classes to SKOS concepts or controlled values if they do not need identity-level semantics:

* highly fine-grained analyst specialization labels such as:

  * `DeepfakeDetectionSpecialist`
  * `SyntheticMediaExaminer`
  * `AIModelAnalyst`
* local triage categories
* rapidly changing operational status classes
* application-specific moderation labels
* mechanism-specific sharing categories

## Decision rule

If the ontology gains little inferential value from making something a class, and the concept is primarily there to support filtering, UI choice lists, reporting, or operational variation, prefer SKOS.

---

# Migration Plan

## Phase 1: Introduce the semantic spine without breaking existing IRIs

* add `cac-core` classes
* add new bridge modules
* add starter SHACL shapes
* keep existing classes in place

## Phase 2: Re-anchor existing classes broadly in v3.0.0

* add `rdfs:subClassOf` links from current classes to the appropriate semantic-spine parents
* re-anchor all identifiable `Phase`, `Role`, and `Situation` classes across domain modules to the spine in v3.0.0
* re-anchor priority event, action, result, and artifact classes called out in this proposal
* deprecate clearly problematic classes or patterns
* add replacement guidance in annotations

## Phase 3: Rationalize bridge content

* inventory current `cacontology-gufo:` classes and properties
* classify each one as retained, migrated, bridge-only, or deprecated
* review all existing `owl:equivalentClass` axioms and assign a disposition

## Phase 4: Refactor documentation

* show semantic spine prominently
* separate direct vs inherited content
* annotate high-use classes with guidance
* clearly mark breaking hierarchy changes

## Phase 5: Publish profiles

* core profile
* investigation profile
* advanced profile

## Phase 6: Clean up and stabilize

* review strong equivalence axioms
* review overly broad inherited properties
* move operational taxonomies to SKOS where appropriate
* re-run example graphs and query packs

---

# Recommended Initial Implementation Backlog

## Priority 1

1. Create `cac-core` semantic spine classes.
2. Add explicit `gufo:Object` and `uco-core:UcoObject` alignment to `cac-core:EnduringEntity`.
3. Add bridge modules for gUFO, CASE, and UCO alignment.
4. Introduce `cac-core:AssessmentResult`.
5. Re-anchor all identifiable `Phase`, `Role`, and `Situation` classes across domain modules to the spine.
6. Refactor phase classes so they no longer subclass investigation classes.

## Priority 2

7. Re-home `ClassificationResult` and similar result-like classes.
8. Re-home AI-generated and AI-altered media classes under a cleaner artifact structure.
9. Re-anchor investigation-specific actions through `cac-core:InvestigativeAction`.
10. Re-anchor coordination and support events under broader event branches where appropriate.
11. Re-home `AICSAMInvestigation` as a CASE-aligned investigation container and reclassify its sub-activities as `cac-core:InvestigativeAction` subclasses.

## Priority 3

11. Review and classify all current `owl:equivalentClass` axioms.
12. Inventory the current `cacontology-gufo:` namespace and document the migration path.
13. Anchor temporal namespace classes into the spine.
14. Add starter SHACL shapes for each semantic-spine branch.
15. Update docs to separate direct and inherited semantics.
16. Add class-level implementation guidance annotations.
17. Publish starter examples and machine-readable starter packs.

---

# Acceptance Criteria

This refactor should be considered successful when:

1. a new implementer can identify the correct modeling pattern for a new concept using the semantic spine
2. class pages clearly show the difference between direct and inherited semantics
3. phases are not modeled as investigations
4. results are not routinely modeled as artifacts
5. role classes consistently represent anti-rigid context-dependent capacities
6. investigation actions align cleanly to CASE where appropriate
7. `cac-core:EnduringEntity` preserves continuity with both gUFO object semantics and UCO core object semantics
8. the migration path for existing `owl:equivalentClass` axioms is explicitly documented
9. the existing `cacontology-gufo:` and temporal content have a clear path into the new architecture
10. independent app builders using the docs are more likely to choose the same classes and shapes for the same domain concepts
11. the ontology remains broad enough for the full CAC domain, not just one workflow community

---

# Suggested Work Items for Cursor AI Agent

## Task 1: Inventory and classify current classes

* review current top-level and high-use classes
* assign each one to an ontological category: enduring entity, event, situation, role, phase, assessment result
* flag classes with ambiguous or conflicting identity stories
* explicitly flag classes still relying on `uco-core:UcoObject` inheritance only

## Task 2: Draft the `cac-core` spine

* create new `cac-core` namespace
* implement it in `ontology/cacontology-core-spine.ttl`
* define the core classes in Turtle
* add labels, comments, and annotations for intended usage
* include explicit `gufo:Object` and `uco-core:UcoObject` alignment on `cac-core:EnduringEntity`

## Task 3: Build bridge modules

* create `ontology/cacontology-bridge-gufo.ttl`
* create `ontology/cacontology-bridge-case.ttl`
* create `ontology/cacontology-bridge-uco.ttl`
* decide how legacy `cacontology-gufo:` content maps into them
* move stronger or optional alignments into bridges when appropriate

## Task 4: Re-anchor classes

Start with priority classes while also broadening v3.0.0 coverage to all identifiable `Phase`, `Role`, and `Situation` classes across modules.

Priority classes:

* `VictimRole`
* `VictimPhase`
* `ClassificationResult`
* `InformationSharing`
* `EvidenceReviewAction`
* `ReceiveCybertipAction`
* `AIAlteredCSAM`
* `AICSAMInvestigation`
* `AgeAtTimeSituation`

## Task 5: Review `owl:equivalentClass` axioms

* inventory all of them
* immediately move the most structurally impactful `cacontology-gufo:*` equivalences into bridge modules in v3.0.0
* assign each reviewed axiom a disposition: keep, move to bridge, deprecate, or pending review
* retain stable cross-namespace identity mappings where justified
* update documentation accordingly

## Task 6: Refactor SHACL starter shapes

* create minimal shapes for each semantic-spine branch
* create richer profile shapes for advanced use
* provide temporary compatibility shapes where needed

## Task 7: Improve documentation generation and annotations

* distinguish direct vs inherited content in docs templates if possible
* add class annotations for use guidance
* create a semantic spine landing page
* add migration banners for breaking hierarchy changes

## Task 8: Publish starter examples and migration examples

Create canonical example instances for:

* victim role participation
* information sharing event
* evidence review action
* victim support phase
* classification result assessing an artifact
* AI-altered media artifact with authenticity assessment
* age-at-time situation
* before/after migration examples for deprecated classes

---

# Canonical Example Patterns

## Example 1: Classification result assessing an artifact

```turtle
@prefix ex: <https://example.org/> .
@prefix cac-core: <https://cacontology.projectvic.org/core#> .
@prefix cac-ai: <https://cacontology.projectvic.org/ai#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:item123 a cac-ai:AIAlteredCSAM .

ex:result456 a cac-core:AssessmentResult ;
  cac-core:assesses ex:item123 ;
  cac-core:hasConfidence "0.91"^^xsd:decimal .
```

## Example 2: Victim role in a participation situation

```turtle
@prefix ex: <https://example.org/> .
@prefix cac-core: <https://cacontology.projectvic.org/core#> .
@prefix cac: <https://cacontology.projectvic.org#> .
@prefix uco-identity: <https://ontology.unifiedcyberontology.org/uco/identity/> .

ex:person789 a uco-identity:Person .
ex:victimRole1 a cac:VictimRole .
ex:situation999 a cac-core:Situation .
```

## Example 3: Investigation-specific action

```turtle
@prefix ex: <https://example.org/> .
@prefix cac: <https://cacontology.projectvic.org#> .

ex:review1 a cac:EvidenceReviewAction .
```

## Example 4: Coordination event

```turtle
@prefix ex: <https://example.org/> .
@prefix cac-coord: <https://cacontology.projectvic.org/coord#> .

ex:shareEvent1 a cac-coord:InformationSharing .
```

## Example 5: Temporal situation

```turtle
@prefix ex: <https://example.org/> .
@prefix cac-temporal: <https://cacontology.projectvic.org/temporal#> .

ex:ageSituation1 a cac-temporal:AgeAtTimeSituation .
```

---

# Final Recommendation

Adopt the semantic spine as the stable CAC-facing top hierarchy, retain subclassing from gUFO, CASE, and UCO where appropriate, and make the public documentation explicitly guide both human implementers and AI agents toward the same modeling choices.

The ontology should be broad enough to model the entire CAC domain while still providing a disciplined, understandable, and interoperable starting point for application builders.

That balance is the best path toward large-scale semantic interoperability across independently built systems.
