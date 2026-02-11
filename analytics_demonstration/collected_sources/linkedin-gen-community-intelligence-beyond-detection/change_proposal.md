## CAC Ontology Change Proposal: “Community & Intelligence Beyond Detection” (GEN) — target release v2.6.0

- **Source document**: LinkedIn article “Community & Intelligence Beyond Detection” (Global Emancipation Network)
- **Source URL**: `https://www.linkedin.com/pulse/community-intelligence-beyond-detection-global-emancipation-network-xvemc/`
- **Captured source text**: `analytics_demonstration/collected_sources/linkedin-gen-community-intelligence-beyond-detection/source.txt`
- **Normalized evidence**: `analytics_demonstration/collected_sources/linkedin-gen-community-intelligence-beyond-detection/normalized.txt`
- **DocumentId (deterministic)**: `urn:uuid:7c162f90-5339-5427-b43a-0a1446025780` (UUIDv5 using URL)
- **Proposal scope** (in-scope only):
  - **A**: Nudification tools / “nudifying functionalities” as an AI-enabled CSEA-adjacent generation pattern
  - **B**: Risk-stratified intelligence outputs (beyond raw detection flags) for prioritization/triage
  - **C**: Compliance intelligence frameworks, safe-harbor linkage, and “knowing paradox” incentive conflict
  - **D**: Trust & Safety operations at scale: moderation queues, backlogs, throughput/latency metrics
  - **E**: Analyst exposure minimization + occupational harm concepts (vicarious trauma / secondary traumatic stress) for content review workflows

This document follows Phase 0–2 requirements in `agent.md` (scope gate + reuse-first sweep + concept inventory + mapping + implementation plan + term ledger + governance gate queue).

---

### Phase 0: Setup + guardrails

#### Working assumptions (needed for this proposal)

- The article is **in-scope** when it discusses CSAM detection-to-action pipelines, NCMEC/platform/law-enforcement coordination, evidentiary readiness, and analyst exposure minimization.
- The article is **out-of-scope** for ontology domain triples when it discusses GEN staffing announcements, marketing, general organizational growth, and unrelated corporate topics (retain provenance only in acquisition artifacts).
- “Risk-stratified intelligence” should be modeled as **a process + result artifact** that can attach to either:
  - platform detection outputs (`cacontology-detection:*`), and/or
  - NCMEC CyberTip analysis / prioritization (`cacontology-us-ncmec:*`),
  without duplicating existing “case management triage” semantics.
- Compliance and policy concepts should **extend** `cacontology-legal-harmonization` (which already contains `ComplianceProcess`, `AuditProcess`, and legal instrument classes), rather than introducing a parallel compliance namespace.

#### Candidate modules/files to change

- `ontology/cacontology-ai-generated-content.ttl` (+ `ontology/cacontology-ai-generated-content-shapes.ttl`)
- `ontology/cacontology-detection.ttl` (+ `ontology/cacontology-detection-shapes.ttl`)
- `ontology/cacontology-platforms.ttl` (+ `ontology/cacontology-platforms-shapes.ttl`)
- `ontology/cacontology-legal-harmonization.ttl` (+ `ontology/cacontology-legal-harmonization-shapes.ttl`)
- **New module (recommended)**: `ontology/cacontology-analyst-wellbeing.ttl` (+ `ontology/cacontology-analyst-wellbeing-shapes.ttl`)
- `CHANGELOG.md` (add `v2.6.0` section; see “Versioning plan” below)

#### Reuse-first / search-first summary (required)

Repo-local searches over `ontology/*.ttl` show **reuse candidates** already present:

- **CSAM detection pipeline + analyst roles**: `cacontology-detection:*` (e.g., `DetectionResult`, `ManualClassificationAction`, `ContentAnalystRole`, reporting phase)
- **Platform content moderation + ESP compliance capability (high-level)**: `cacontology-platforms:*` (e.g., `ContentModerationCapability`, `ContentModerationAction`, `LegalComplianceCapability`)
- **NCMEC clearinghouse and tip processing**: `cacontology-us-ncmec:*` (e.g., `TipPrioritization`, `TipProcessing`, `PlatformCooperation`)
- **Legal compliance processes and legal instruments**: `cacontology-legal:*` in `cacontology-legal-harmonization.ttl` (e.g., `ComplianceProcess`, `AuditProcess`, `CertificationProcess`, `Statute`, `LegislativeInstrument`, `PlatformAccountabilityLaw`)
- **Evidence quality / admissibility / chain-of-custody**: `cacontology-forensics:*`, `cacontology-physical-evidence:*`
- **AI-generated / deepfake CSAM**: `cacontology-ai:*` in `cacontology-ai-generated-content.ttl`

Repo-local searches indicate **gaps (not found as modeled terms)** for:

- “nudifying tools / nudifying functionalities” (nudification as a specific AI action/tool/output category)
- “risk-stratified” modeling (risk tiers/scores/rationales as first-class outputs linked to detection/tips)
- “safe harbor” and “knowing paradox” as modeled legal-policy incentive concepts linked to statutes/frameworks
- moderation “queue/backlog/throughput/latency” as first-class operational objects/situations/metrics for Trust & Safety workflows
- analyst occupational impacts (vicarious trauma / secondary traumatic stress) and “exposure minimization measures” linked to review actions

#### Scope confirmation

- **In-scope**: `normalized.txt` lines 1–15 (detection-to-action pipeline, NCMEC/platform coordination, evidence readiness, analyst exposure minimization, nudification ban, safe harbors/knowing paradox, risk stratification)
- **Out-of-scope** (do not model as domain triples): general org announcements, hiring, sales, non-CSEA corporate due diligence claims (captured only in `source.txt` for provenance)

---

## Phase 1: Concept inventory + mapping (proposal-focused subset)

### Concept inventory table

| Concept | Category | Source snippet | Evidence pointer | Confidence | Proposed modeling approach |
|---|---|---|---|---|---|
| Detection is not the hard part; “what comes next” is coordination | Other | “The hard part… isn't detection… The challenge is what comes next…” | `normalized.txt` line 1 | high | **reuse** existing detection/platform coordination terms; **extend** with queue/backlog and risk strat outputs |
| Massive flagged volume requiring operational review + distribution | Other | “flags… 100,000… in just one month…” | `normalized.txt` line 3 | high | **extend** platforms/detection with moderation queue + throughput/latency metrics |
| Documentation trail proving good faith to regulators | Legal/Other | “What documentation proves to regulators…” | `normalized.txt` line 4 | high | **extend** legal-harmonization with compliance documentation/audit trail concepts (aligned to existing `ComplianceProcess`) |
| Turn raw flags into courtroom-ready evidence while protecting analysts | Other | “turn raw flags into courtroom-ready evidence… protecting… analysts…” | `normalized.txt` line 5 | high | **reuse** forensics/admissibility; **extend** with exposure mitigation + analyst wellbeing module |
| Ethical obligation to minimize analyst exposure | Other | “minimize their exposure…” | `normalized.txt` line 6 | high | **new** exposure mitigation measure + occupational harm concepts (analyst wellbeing module) |
| Nudifying apps / nudifying functionalities | Other | “nudifying apps… illegal… global ban…” | `normalized.txt` lines 7–9 | high | **extend** AI-generated-content module with nudification-specific action/tool/output terms |
| “Knowing paradox” incentive conflict (SESTA-FOSTA) | Legal/Other | “knowing paradox… liability both for detecting… and for failing…” | `normalized.txt` line 10 | high | **extend** legal-harmonization with incentive-conflict concept linked to statute(s) |
| Safe harbors based on verified compliance intelligence frameworks | Legal/Other | “Create safe harbors… verified compliance intelligence frameworks… good faith vs negligence” | `normalized.txt` line 11 | high | **extend** legal-harmonization with `SafeHarbor` + `ComplianceIntelligenceFramework` linkage |
| Preserve evidence quality + protect investigator capacity | Other | “preserve evidence quality… protect investigator capacity…” | `normalized.txt` line 12 | high | **reuse** forensics/evidence quality; **extend** with analyst wellbeing/exposure mitigation connections |
| Verification standards for compliance documentation | Legal/Other | “verification standards for compliance documentation…” | `normalized.txt` line 13 | high | **extend** legal-harmonization compliance processes with documentation verification artifact/result |
| Risk-stratified intelligence / action | Other | “Risk-Stratified Intelligence… risk-stratified action” | `normalized.txt` lines 14–15 | high | **extend** detection module with risk stratification action + result artifact |

### Mapping table (document concept → existing term OR proposed new term)

| Document concept | Existing term(s) to reuse | Proposed new term(s) | Rationale |
|---|---|---|---|
| Nudifying tools / functionalities | `cacontology-ai:AIContentGeneration` (process pattern) | `cacontology-ai:Nudification` (process), `cacontology-ai:NudificationTool`, `cacontology-ai:NudifiedCSAM` | “Nudification” is a named, policy-targeted functionality distinct from generic deepfake/face swapping; needs a dedicated pattern for cross-document analytics. |
| Risk-stratified analysis of flags | `cacontology-detection:DetectionResult` and phases/roles | `cacontology-detection:RiskStratificationAction`, `cacontology-detection:RiskStratificationResult`, `cacontology-detection:riskScore/riskTier/riskRationale` | Article’s key claim is operational prioritization beyond detection; representing risk outputs as first-class artifacts enables explainable triage analytics. |
| Safe harbors & “good faith vs negligence” compliance framing | `cacontology-legal:ComplianceProcess`, `cacontology-legal:AuditProcess`, `cacontology-legal:CertificationProcess` | `cacontology-legal:SafeHarbor`, `cacontology-legal:ComplianceIntelligenceFramework` | Legal-harmonization already models compliance processes; this extends it with the specific safe-harbor + verified-framework linkage. |
| “Knowing paradox” incentive conflict | `cacontology-legal:Statute` / `LegislativeInstrument` | `cacontology-legal:KnowingParadox` + link property from statute | This is explicitly named in the article and central to policy incentive analytics; should be queryable as a modeled situation/outcome of a statute. |
| Documentation trails for regulators | `cacontology-case:CaseDocumentation` (general), `cacontology-legal:AuditProcess` | `cacontology-legal:ComplianceDocumentationArtifact` (or `ComplianceDocumentationRecord`) + verification status | Current ontology has compliance processes, but not an explicit documentation artifact node optimized for “good faith” evidence trails. |
| Moderation queues/backlogs/throughput | `cacontology-platforms:ContentModerationAction` | `cacontology-platforms:ContentModerationQueue`, `cacontology-platforms:ReviewBacklogSituation`, moderation metrics properties | Needed to represent bottlenecks and operational scale described (100k flags/month). |
| Analyst exposure minimization + occupational harm | `cacontology-detection:ContentAnalystRole`, `cacontology-detection:ManualReviewTool` | New module: `cacontology-analyst:ExposureMitigationMeasure`, `cacontology-analyst:OccupationalHarm`, `cacontology-analyst:VicariousTrauma` | Victim trauma is modeled, but analyst occupational impacts and mitigation measures are not; article makes this a first-class design constraint. |

---

## Phase 2: Implementation plan (schema-driven; proposal only) — target release v2.6.0

### 2.1 New / updated terms (fully-qualified)

#### File: `ontology/cacontology-ai-generated-content.ttl`

**Add classes:**

- `cacontology-ai:Nudification` (subClassOf `cacontology-ai:AIContentGeneration`, `uco-action:Action`, `gufo:Event`)
- `cacontology-ai:NudificationTool` (subClassOf `uco-tool:Tool`, `gufo:Object`)
- `cacontology-ai:NudifiedCSAM` (subClassOf `cacontology-ai:AIGeneratedCSAM`, `gufo:Object`)

**Add object properties:**

- `cacontology-ai:usesNudificationTool` (domain `Nudification`, range `NudificationTool`)
- `cacontology-ai:producesNudifiedContent` (domain `Nudification`, range `NudifiedCSAM`)
- `cacontology-ai:nudifiedFrom` (domain `NudifiedCSAM`, range `uco-observable:ObservableObject`) — links output to source media

**Add datatype properties (minimal):**

- `cacontology-ai:nudificationTechnique` (domain `Nudification`, range `xsd:string`) — e.g., “nudify”, “clothing_removal”, “synthetic_nudity”

**Duck-typing note:** do **not** subclass generic “image” types for “analyzed nudified image”; attach analysis facets to `uco-observable:ObservableObject` as needed.

#### File: `ontology/cacontology-detection.ttl`

**Add classes:**

- `cacontology-detection:RiskStratificationAction` (subClassOf `uco-action:Action`, `gufo:Event`)
- `cacontology-detection:RiskStratificationResult` (subClassOf `uco-observable:ObservableObject`, `gufo:Object`)

**Add object properties:**

- `cacontology-detection:stratifiesResult` (domain `RiskStratificationAction`, range `cacontology-detection:DetectionResult`)
- `cacontology-detection:producesRiskStratificationResult` (domain `RiskStratificationAction`, range `RiskStratificationResult`)
- `cacontology-detection:riskResultFor` (domain `RiskStratificationResult`, range `uco-observable:ObservableObject`) — allows linking risk results to tips/content/artifacts beyond `DetectionResult` if needed

**Add datatype properties:**

- `cacontology-detection:riskScore` (domain `RiskStratificationResult`, range `xsd:decimal`)
- `cacontology-detection:riskTier` (domain `RiskStratificationResult`, range `xsd:string`) — recommend controlled values via SHACL
- `cacontology-detection:riskRationale` (domain `RiskStratificationResult`, range `xsd:string`) — explainability payload

#### File: `ontology/cacontology-platforms.ttl`

**Add classes:**

- `cacontology-platforms:ContentModerationQueue` (subClassOf `uco-core:UcoObject`, `gufo:Object`)
- `cacontology-platforms:ReviewBacklogSituation` (subClassOf `gufo:Situation`)
- `cacontology-platforms:ModerationThroughputMetrics` (subClassOf `uco-core:UcoObject`, `gufo:Object`)

**Add object properties:**

- `cacontology-platforms:enqueuedForModeration` (domain `uco-observable:ObservableObject`, range `ContentModerationQueue`)
- `cacontology-platforms:queueOperatedBy` (domain `ContentModerationQueue`, range `cacontology-platforms:ElectronicServiceProvider`)
- `cacontology-platforms:hasBacklogSituation` (domain `ContentModerationQueue`, range `ReviewBacklogSituation`)
- `cacontology-platforms:reportsThroughputMetrics` (domain `ContentModerationQueue`, range `ModerationThroughputMetrics`)

**Add datatype properties:**

- `cacontology-platforms:queueSize` (domain `ContentModerationQueue`, range `xsd:nonNegativeInteger`)
- `cacontology-platforms:reviewLatencyHours` (domain `ModerationThroughputMetrics`, range `xsd:decimal`)
- `cacontology-platforms:throughputPerDay` (domain `ModerationThroughputMetrics`, range `xsd:nonNegativeInteger`)
- `cacontology-platforms:flagVolumePerMonth` (domain `ModerationThroughputMetrics`, range `xsd:nonNegativeInteger`)

#### File: `ontology/cacontology-legal-harmonization.ttl`

**Add classes:**

- `cacontology-legal:ComplianceIntelligenceFramework` (subClassOf `uco-core:UcoObject`, `gufo:Object`; `gufo:Kind`)
- `cacontology-legal:SafeHarbor` (subClassOf `uco-core:UcoObject`, `gufo:Object`; `gufo:Kind`)
- `cacontology-legal:KnowingParadox` (subClassOf `gufo:Situation`)
- `cacontology-legal:ComplianceDocumentationArtifact` (subClassOf `uco-core:UcoObject`, `gufo:Object`; `gufo:Kind`)

**Add object properties:**

- `cacontology-legal:hasSafeHarbor` (domain `cacontology-legal:Statute`, range `SafeHarbor`)
- `cacontology-legal:supportedByFramework` (domain `SafeHarbor`, range `ComplianceIntelligenceFramework`)
- `cacontology-legal:producesComplianceDocumentation` (domain `cacontology-legal:ComplianceProcess`, range `ComplianceDocumentationArtifact`)
- `cacontology-legal:documentsGoodFaithEffort` (domain `ComplianceDocumentationArtifact`, range `uco-identity:Organization`)
- `cacontology-legal:createsIncentiveConflict` (domain `cacontology-legal:Statute`, range `KnowingParadox`)

**Add datatype properties (minimal):**

- `cacontology-legal:goodFaithCriteria` (domain `SafeHarbor`, range `xsd:string`)
- `cacontology-legal:verificationStatus` (domain `ComplianceDocumentationArtifact`, range `xsd:string`) — controlled values via SHACL (“verified”, “unverified”, “contested”)

**Optional named individuals (policy artifacts)**:

- `cacontology-legal:SESTA_FOSTA_2018` a `cacontology-legal:Statute`
- `cacontology-legal:DEFIANCE_Act` a `cacontology-legal:LegislativeInstrument`

> Note: keep these individuals optional for v2.6.0 if you prefer schema-only releases; the core gap is the *pattern* (safe harbor + compliance intelligence + knowing paradox), not the population of specific laws.

#### New module (recommended): `ontology/cacontology-analyst-wellbeing.ttl`

**New namespace:**

- `@prefix cacontology-analyst: <https://cacontology.projectvic.org/analyst-wellbeing#> .`

**Add classes:**

- `cacontology-analyst:ExposureMitigationMeasure` (subClassOf `uco-core:UcoObject`, `gufo:Object`)
- `cacontology-analyst:OccupationalHarm` (subClassOf `gufo:Situation`)
- `cacontology-analyst:VicariousTrauma` (subClassOf `OccupationalHarm`)
- `cacontology-analyst:SecondaryTraumaticStress` (subClassOf `OccupationalHarm`)

**Add object properties:**

- `cacontology-analyst:usesExposureMitigation` (domain `cacontology-detection:ManualClassificationAction`, range `ExposureMitigationMeasure`)
- `cacontology-analyst:experiencesOccupationalHarm` (domain `uco-identity:Person`, range `OccupationalHarm`)

**Add datatype properties:**

- `cacontology-analyst:mitigationType` (domain `ExposureMitigationMeasure`, range `xsd:string`) — controlled values via SHACL (“hash_only_review”, “blurred_preview”, “progressive_reveal”, “audio_removed”, “frame_sampling”)
- `cacontology-analyst:harmSeverity` (domain `OccupationalHarm`, range `xsd:string`) — e.g., “low/medium/high”

### 2.1a Ontology drift check (label-match pre-screen; required before approval)

Pre-screen result (repo-local label/keyphrase searches conducted during analysis):

- No existing CAC term labels found for: **nudification**, **nudifying**, **risk stratified / risk-stratified**, **safe harbor**, **knowing paradox**, **moderation queue / backlog**, **vicarious trauma** (as analyst occupational harm).
- **Decision**: proposed new terms are **CLEAR** for duplication by label-match; proceed to governance review.

### 2.1b Minimum-link obligations (connectivity-by-design plan)

| New class | Example instance must be connected by | Grounding |
|---|---|---|
| `cacontology-ai:Nudification` | `uco-action:result` → `NudifiedCSAM` and/or `usesNudificationTool` | `normalized.txt` lines 7–9 |
| `cacontology-detection:RiskStratificationAction` | `stratifiesResult` → `DetectionResult` and `producesRiskStratificationResult` → result | `normalized.txt` lines 14–15 |
| `cacontology-legal:SafeHarbor` | `hasSafeHarbor` ← `Statute` and `supportedByFramework` → framework | `normalized.txt` lines 10–13 |
| `cacontology-platforms:ContentModerationQueue` | `enqueuedForModeration` ← content/detection output and `queueOperatedBy` → ESP | `normalized.txt` line 3 |
| `cacontology-analyst:ExposureMitigationMeasure` | `usesExposureMitigation` ← manual review action | `normalized.txt` lines 5–6 |

### 2.2 SHACL shapes to add/update (targets + minimal constraints)

**Principle:** keep constraints minimal; enforce connectivity + controlled enums where they provide analytic value.

- `ontology/cacontology-ai-generated-content-shapes.ttl`
  - NodeShapes for `Nudification`, `NudificationTool`, `NudifiedCSAM`
  - Require: `usesNudificationTool` (min 0/1) and `producesNudifiedContent` (min 1 for `Nudification`)
  - Require: `nudifiedFrom` (min 0/1) for `NudifiedCSAM` (optional when source not known)

- `ontology/cacontology-detection-shapes.ttl`
  - `RiskStratificationActionShape`: require `producesRiskStratificationResult` minCount 1
  - `RiskStratificationResultShape`: require at least one of `riskTier` or `riskScore`; optionally require `riskRationale` when `riskTier` present (explainability)

- `ontology/cacontology-platforms-shapes.ttl`
  - `ContentModerationQueueShape`: require `queueOperatedBy` exactly 1; `queueSize` optional
  - `ModerationThroughputMetricsShape`: require `throughputPerDay` (optional), `reviewLatencyHours` (optional), `flagVolumePerMonth` (optional)

- `ontology/cacontology-legal-harmonization-shapes.ttl`
  - `SafeHarborShape`: require `goodFaithCriteria` min 1 (string) **or** allow empty if unknown
  - `ComplianceDocumentationArtifactShape`: require `verificationStatus` in (“verified”, “unverified”, “contested”)

- `ontology/cacontology-analyst-wellbeing-shapes.ttl` (new)
  - `ExposureMitigationMeasureShape`: require `mitigationType` in controlled list
  - `OccupationalHarmShape`: optional `harmSeverity` in (“low”, “medium”, “high”)

### 2.3 Example KG scope (what instances demonstrate which new terms)

Proposed example file (new):

- `examples_knowledge_graphs/linkedin-gen-community-intelligence-beyond-detection-example.ttl`

Must demonstrate:

- Nudification pattern: one `Nudification` action, one `NudificationTool`, one `NudifiedCSAM`, and `nudifiedFrom` link
- Risk stratification pattern: `RiskStratificationAction` over a `DetectionResult` producing a `RiskStratificationResult` with `riskTier` and `riskRationale`
- Moderation queue pattern: content/detection output enqueued into a `ContentModerationQueue` with throughput metrics
- Legal policy pattern: a `Statute` with `hasSafeHarbor` and `createsIncentiveConflict` (KnowingParadox), plus a `ComplianceIntelligenceFramework` and `ComplianceDocumentationArtifact`
- Analyst wellbeing pattern: a `ManualClassificationAction` using an `ExposureMitigationMeasure`, plus an example `OccupationalHarm` linked to an analyst identity

### 2.4 SPARQL query scope (titles + intent)

Proposed query file (new):

- `example_SPARQL_queries/linkedin-gen-community-intelligence-beyond-detection-analytics.rq`

Planned queries:

- “List risk-stratification results and rationale for detection results”
- “Find moderation queues with backlog situations and high review latency”
- “Find nudification actions and resulting nudified content”
- “List statutes with safe harbors supported by compliance intelligence frameworks”
- “Find review actions that used exposure mitigation measures”

### 2.5 Versioning plan for v2.6.0

- Update **all** ontology and shape files version references **2.5.0 → 2.6.0** (consistent with prior release practice in `CHANGELOG.md`).
- Add a `CHANGELOG.md` entry:
  - `## v2.6.0 - 11 February 2026`
  - Summarize: nudification modeling, risk stratification outputs, compliance intelligence + safe harbors + knowing paradox, moderation queue/backlog metrics, analyst wellbeing.

---

## Term Citation & Mapping Ledger (Required)

Citation for all new terms (uniform):

- **dcterms:source**: “Community & Intelligence Beyond Detection” (Global Emancipation Network), published 2026-02-10
- **rdfs:seeAlso**: `https://www.linkedin.com/pulse/community-intelligence-beyond-detection-global-emancipation-network-xvemc/`

| CAC Term (fully-qualified) | dcterms:source citation | rdfs:seeAlso | External alignment | gUFO alignment | Explainability note |
|---|---|---|---|---|---|
| `cacontology-ai:Nudification` | GEN article, `normalized.txt` lines 7–9 | URL above | (none proposed) | `gufo:Event` | Distinguishes nudification from generic deepfake/face swap; supports analytics on “nudify” tool usage. |
| `cacontology-ai:NudificationTool` | GEN article, `normalized.txt` lines 7–9 | URL above | (none proposed) | `gufo:Object` | Represents a class of tools called out for policy prohibition. |
| `cacontology-ai:NudifiedCSAM` | GEN article, `normalized.txt` lines 7–9 | URL above | (none proposed) | `gufo:Object` | Represents the resulting synthetic nudity output relevant to child protection. |
| `cacontology-detection:RiskStratificationAction` | GEN article, `normalized.txt` lines 14–15 | URL above | (none proposed) | `gufo:Event` | Encodes the “what comes next” step beyond detection: prioritization. |
| `cacontology-detection:RiskStratificationResult` | GEN article, `normalized.txt` lines 14–15 | URL above | (none proposed) | `gufo:Object` | Enables explainable triage analytics with risk score/tier + rationale. |
| `cacontology-platforms:ContentModerationQueue` | GEN article, `normalized.txt` line 3 | URL above | (none proposed) | `gufo:Object` | Models moderation bottlenecks described in scaled detection environments. |
| `cacontology-platforms:ReviewBacklogSituation` | GEN article, `normalized.txt` line 3 | URL above | (none proposed) | `gufo:Situation` | Enables analytics on backlog presence and operational risk. |
| `cacontology-legal:ComplianceIntelligenceFramework` | GEN article, `normalized.txt` line 11 | URL above | (none proposed) | `gufo:Kind` | Represents the “verified compliance intelligence framework” concept tied to safe harbors. |
| `cacontology-legal:SafeHarbor` | GEN article, `normalized.txt` line 11 | URL above | (none proposed) | `gufo:Kind` | Enables modeling of safe-harbor policy mechanisms for good-faith efforts. |
| `cacontology-legal:KnowingParadox` | GEN article, `normalized.txt` line 10 | URL above | (none proposed) | `gufo:Situation` | Captures the incentive conflict: liability for knowledge vs liability for failing to detect. |
| `cacontology-analyst:ExposureMitigationMeasure` | GEN article, `normalized.txt` lines 5–6 | URL above | (none proposed) | `gufo:Object` | Enables modeling of measures that reduce traumatic exposure while maintaining review effectiveness. |
| `cacontology-analyst:VicariousTrauma` | GEN article, `normalized.txt` lines 5–6 | URL above | (none proposed) | `gufo:Situation` | Models occupational harm relevant to sustaining investigative capacity. |

---

## Checklist of file edits (proposal; “why here?”)

- `ontology/cacontology-ai-generated-content.ttl`
  - Add nudification process/tool/output terms (fits existing AI content generation/detection patterns).
- `ontology/cacontology-ai-generated-content-shapes.ttl`
  - Add shapes validating nudification connectivity and minimal required properties.
- `ontology/cacontology-detection.ttl`
  - Add risk stratification action + result artifacts for “beyond detection” prioritization.
- `ontology/cacontology-detection-shapes.ttl`
  - Validate risk score/tier/rationale (explainability) and connectivity.
- `ontology/cacontology-platforms.ttl`
  - Add moderation queue/backlog/throughput concepts to represent scaled review operations.
- `ontology/cacontology-platforms-shapes.ttl`
  - Minimal constraints ensuring queues are associated with an ESP and optionally metrics.
- `ontology/cacontology-legal-harmonization.ttl`
  - Extend existing compliance/legal instrument modeling with safe harbor + knowing paradox + framework/doc artifact terms.
- `ontology/cacontology-legal-harmonization-shapes.ttl`
  - Add shapes for new legal-policy nodes and documentation verification status.
- `ontology/cacontology-analyst-wellbeing.ttl` (**new**)
  - Add exposure mitigation + occupational harm concepts for content review workflows.
- `ontology/cacontology-analyst-wellbeing-shapes.ttl` (**new**)
  - Validate controlled vocabularies for mitigation types and severity.
- `CHANGELOG.md`
  - Add `v2.6.0` entry summarizing this release (and update version references across files).

---

## Risk list (top validation failure modes + mitigations)

1. **SHACL shape violations (over-constrained enums / required fields)**
   - Mitigation: keep new shapes minimal; enforce only connectivity + small controlled lists where essential.
2. **Domain/range violations across modules**
   - Mitigation: keep risk stratification anchored in `cacontology-detection` and connect via explicit properties; avoid reusing ambiguous generic predicates.
3. **Connectivity risk (isolated policy/metric nodes)**
   - Mitigation: ensure example KG ties every new node to at least one action/object relationship (`uco-action:object/result`, `uco-core:hasFacet`) per `agent.md`.
4. **Scope drift (general compliance/industry concepts)**
   - Mitigation: restrict to CSEA-relevant compliance intelligence (platform reporting/detection/capacity/evidence readiness), not generic corporate compliance.

---

## Governance gate queue (REVIEW REQUIRED)

- **New terms pending approval** (schema additions for v2.6.0):
  - `cacontology-ai:Nudification`
  - `cacontology-ai:NudificationTool`
  - `cacontology-ai:NudifiedCSAM`
  - `cacontology-detection:RiskStratificationAction`
  - `cacontology-detection:RiskStratificationResult`
  - `cacontology-platforms:ContentModerationQueue`
  - `cacontology-platforms:ReviewBacklogSituation`
  - `cacontology-legal:ComplianceIntelligenceFramework`
  - `cacontology-legal:SafeHarbor`
  - `cacontology-legal:KnowingParadox`
  - `cacontology-legal:ComplianceDocumentationArtifact`
  - `cacontology-analyst:ExposureMitigationMeasure`
  - `cacontology-analyst:OccupationalHarm`
  - `cacontology-analyst:VicariousTrauma`
  - `cacontology-analyst:SecondaryTraumaticStress`

- **SKOS mappings pending approval**:
  - None proposed yet (recommend adding only when a stable external vocabulary is selected).

- **Sensitive entities/claims pending approval**:
  - None required for schema-level release (avoid modeling any real victim identities from this article).
