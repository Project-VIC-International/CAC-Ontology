## CAC Ontology Change Proposal (A+B+C): Know2Protect SOE brochure (k2p-soe-information)

- **Source document**: `K2P SOE Information.pdf`
- **Normalized evidence**: `analytics_demonstration/collected_sources/k2p-soe-information/normalized.txt`
- **DocumentId**: `urn:uuid:1d896431-835d-585d-929b-f51fafce1fe2`
- **Proposal scope**: add reusable ontology terms for:
  - **A**: *Sadistic sextortion*
  - **B**: *Sadistic Online Exploitation (SOE) network taxonomy*
  - **C**: *Doxxing/swatting intimidation tactics + livestream “watch party / cut show” coercion events*

This document follows the Phase 1–2 requirements in `agent.md` (concept inventory + mapping + implementation plan + term ledger + governance gate queue).

---

### Reuse-first / search-first summary (required)

Repo-local searches over `ontology/*.ttl` show:

- **Found (reuse)**:
  - `cacontology-sextortion:ThreatMechanism` (and sharing/screenshot threat subtypes) in `ontology/cacontology-sextortion.ttl`
  - Enterprise coercion modeling such as `cacontology-enterprises:SelfHarmCoercion` and `NameCuttingCoercion` in `ontology/cacontology-extremist-enterprises.ttl`
  - Enterprise/network operations modeling such as:
    - `cacontology-enterprises:CrossPlatformCoordination`
    - `cacontology-enterprises:PrivateGroupManagement`
    - `cacontology-enterprises:PlatformMigrationStrategy`
    - `cacontology-enterprises:EncryptedChannelNetwork`
  - Live-streaming-related concepts in other modules (e.g., `cacontology:LiveStreamingCSA`, `cacontology-production:LiveStreamContent`, `cacontology-sentencing:LiveStreamingOffense`)
- **Not found (gap / propose new CAC terms)**:
  - “Sadistic Sextortion” (as a modeled sextortion subtype)
  - “Sadistic Online Exploitation (SOE)” and “SOE network” (as modeled network taxonomy)
  - “doxxing / swatting” (as intimidation/threat mechanism/tactic)
  - “watch parties / cut shows / cut stages / stages” (as a modeled livestream coercion event pattern)

---

### Impact analysis: `extremist-enterprises` module overlap (required before proposing `cacontology-soe`)

The `extremist-enterprises` module already covers many behaviors that appear in SOE descriptions (network/enterprise structure, cross-platform coordination, platform migration, coercion event taxonomies, vulnerability targeting, and private group management). See the namespace index at:

- `https://cacontology.projectvic.org/extremist-enterprises#`

#### Overlap areas (and the “do not duplicate” rule)

- **Network/enterprise structure**: `cacontology-enterprises:NihilisticViolentExtremismNetwork`, `ChildExploitationEnterprise`, hierarchy/cells/roles
- **Cross-platform + private channels**: `CrossPlatformCoordination`, `EncryptedChannelNetwork`, `PrivateGroupManagement`, `PlatformMigrationStrategy`
- **Coercion event types**: `SelfHarmCoercion`, `ExtremeDegradationCoercion`, `NameCuttingCoercion`, etc.
- **Targeting / social engineering**: `VulnerablePopulationTargeting`, `MentalHealthVulnerabilityTargeting`, `SocialEngineeringCampaign`, `TrustBuildingProcess`

#### Why `cacontology-soe` is still justified (boundary decision)

The Know2Protect brochure defines **SOE networks** as a broader DHS category (“online groups…”) that can include:

- ideologically framed extremist enterprises (e.g., neo-Nazi networks; 764-adjacent ecosystems), **and**
- other sadistic exploitation communities that may not cleanly fit the “extremist” ideological framing.

Creating `cacontology-soe` is justified **only if** we keep it narrowly scoped to:

- the *DHS definitional taxonomy* for SOE networks (to support cross-document aggregation), and
- a small number of *SOE-specific lexical/ritual patterns* not already modeled elsewhere (e.g., “cut show / watch party” naming and its event-type).

Everything else should **reuse** `cacontology-enterprises:*` (and existing CAC modules) rather than re-inventing parallel classes/properties.

#### Recommended classification decision rule (prevents drift/conflict)

- If evidence supports *ideological/enterprise* framing and the richer 764/NVE-style structure is needed:
  - Type the network as `cacontology-enterprises:NihilisticViolentExtremismNetwork` (or related `cacontology-enterprises:*`) and reuse enterprise properties/shapes.
- If evidence only supports the DHS “SOE network” definitional frame (without extremist ideological commitments):
  - Type it as `cacontology-soe:SadisticOnlineExploitationNetwork`.
- A single real-world network MAY be dual-typed **only with explicit justification** (avoid over-typing).

---

## Phase 1: Concept inventory + mapping (proposal-focused subset)

### Concept inventory table

| Concept | Category | Source snippet | Evidence pointer | Confidence | Proposed modeling approach |
|---|---|---|---|---|---|
| Sadistic Online Exploitation (SOE) networks definition | Other | “SOE networks are online groups…” | `normalized.txt` lines **5–9** | high | **new** (SOE taxonomy module), while **reusing** `cacontology-enterprises:*` when extremist-enterprise modeling applies |
| “the com” (community slang) + hierarchy/cross-border operations | Other | “referred to as … ‘the com’ … leadership roles and hierarchy … across international borders” | `normalized.txt` line **8** | high | **new** (datatype property on SOE network) |
| Sadistic sextortion (definition) | Legal/Other | “Sadistic Sextortion: … violence, self-harm or destruction … coordinated through organized SOE networks.” | `normalized.txt` line **46** | high | **new** (sextortion subtype) + **extend** (new threat mechanism subclasses) |
| Doxxing + swatting as intimidation/violence tactics | Action/Other | “Threats… such as self-harm, swatting, or doxxing.” | `normalized.txt` line **40** | high | **extend** (new threat mechanism subclasses) |
| “watch parties / cut shows / cut stages / stages” livestreamed coercion events | Action/Other | “Host online ‘watch parties’ or ‘cut shows’… via livestream… ‘cut stages’ or ‘stages’.” | `normalized.txt` line **32** | high | **new** (SOE livestream coercion event class + controlled vocabulary/alt labels) |

### Mapping table (document concept → existing term OR proposed new term)

| Document concept | Existing term (if any) | Proposed new term | Rationale |
|---|---|---|---|
| Sadistic sextortion | `cacontology-sextortion:SextortionIncident` | `cacontology-sextortion:SadisticSextortion` | Distinct subtype where coercion includes violence/self-harm/destruction (beyond sharing threats) and is SOE-coordinated. |
| Doxxing intimidation | `cacontology-sextortion:ThreatMechanism` | `cacontology-sextortion:DoxxingThreat` | Fits existing sextortion threat mechanism taxonomy and supports cross-case threat analytics. |
| Swatting intimidation | `cacontology-sextortion:ThreatMechanism` | `cacontology-sextortion:SwattingThreat` | Same as above; captures swatting as a coercive/terrorizing threat mechanism. |
| SOE network taxonomy | (none) | `cacontology-soe:SadisticOnlineExploitationNetwork` | Needed to represent DHS-defined SOE networks without forcing an “extremist” ideological classification. |
| “the com” slang term | (none) | `cacontology-soe:communitySlangTerm` (datatype property) | Supports consistent query/label matching for SOE community slang without creating brittle per-case strings. |
| Watch party / cut show coercion livestream | (none) | `cacontology-soe:LivestreamedCoercionShow` (+ `cacontology-soe:coercionShowType`) | Reusable class for a recurring SOE tradecraft behavior referenced in 764/SOE contexts. |

---

## Phase 2: Implementation plan (schema-driven; proposal only)

### 2.1 New / updated terms (fully-qualified)

### 2.1a Ontology drift check (label-match pre-screen; required before approval)

Planned drift check method (per `agent.md`):

- For each proposed term label, search existing `ontology/*.ttl` for similar `rdfs:label` strings.

Pre-screen result (repo-local label searches):

- No existing CAC term labels found for: **SOE**, **Sadistic Online Exploitation**, **Sadistic Sextortion**, **doxxing**, **swatting**, **cut show**, **watch party**.
- **Decision**: all proposed terms are **CLEAR** for duplication by label-match; proceed to governance review (semantic similarity/embeddings check can be added later).

#### File: `ontology/cacontology-sextortion.ttl`

- **Add classes**:
  - `cacontology-sextortion:SadisticSextortion` (subClassOf `cacontology-sextortion:SextortionIncident`)
  - `cacontology-sextortion:DoxxingThreat` (subClassOf `cacontology-sextortion:ThreatMechanism`)
  - `cacontology-sextortion:SwattingThreat` (subClassOf `cacontology-sextortion:ThreatMechanism`)
  - `cacontology-sextortion:ViolenceThreat` (subClassOf `cacontology-sextortion:ThreatMechanism`)
  - `cacontology-sextortion:SelfHarmThreat` (subClassOf `cacontology-sextortion:ThreatMechanism`)
  - `cacontology-sextortion:PropertyDestructionThreat` (subClassOf `cacontology-sextortion:ThreatMechanism`)

- **Add/extend controlled vocabulary guidance** (no new property required):
  - Allow `cacontology-sextortion:threatType` values such as `"doxxing"`, `"swatting"`, `"self_harm"`, `"violence"`, `"property_destruction"` (shape-level enforcement recommended).

#### File: `ontology/cacontology-sextortion-shapes.ttl`

- **Add NodeShapes** (or extend existing threat shapes pattern):
  - `cacontology-sextortion:DoxxingThreatShape`
  - `cacontology-sextortion:SwattingThreatShape`
  - `cacontology-sextortion:SelfHarmThreatShape`
  - `cacontology-sextortion:ViolenceThreatShape`
  - `cacontology-sextortion:PropertyDestructionThreatShape`
  - `cacontology-sextortion:SadisticSextortionShape`

Suggested minimal constraints (to avoid overfitting):

- Threat shapes:
  - `sh:targetClass` each new threat class
  - Require at least one of:
    - `cacontology-sextortion:threatSpecificity` (1–1; in existing allowed list)
    - `cacontology-sextortion:threatFollowThrough` (0–1; boolean)
  - Optional: `cacontology-sextortion:threatType` must be one of the values above (if you choose to enforce by enumeration)

- `SadisticSextortionShape`:
  - `sh:targetClass cacontology-sextortion:SadisticSextortion`
  - Require `cacontology-sextortion:employsThreat` minCount 1
  - Require that at least one `employsThreat` is instance of:
    - `SelfHarmThreat` OR `ViolenceThreat` OR `PropertyDestructionThreat` OR `DoxxingThreat` OR `SwattingThreat`

#### New module (recommended): `ontology/cacontology-soe.ttl` + `ontology/cacontology-soe-shapes.ttl`

**Rationale**: avoid scope/label drift by *not* forcing SOE (DHS-defined) into the “extremist-enterprises” module’s ideological framing; keep SOE taxonomy reusable across cases while **reusing** `cacontology-enterprises:*` for structure/coercion/coordination modeling when appropriate.

- **New namespace**:
  - `@prefix cacontology-soe: <https://cacontology.projectvic.org/soe#> .`

- **Add classes**:
  - `cacontology-soe:SadisticOnlineExploitationNetwork`
    - `rdfs:subClassOf uco-identity:Organization , gufo:FunctionalComplex`
    - `rdfs:comment`: DHS-defined SOE network as an online group coordinating sadistic exploitation/coercion of minors; not inherently ideological “extremist” by definition.
  - `cacontology-soe:LivestreamedCoercionShow`
    - `rdfs:subClassOf uco-action:Action , gufo:Event`
    - `rdfs:comment`: livestreamed/coordinated coercion event (“watch party”, “cut show”, etc.)

- **Add datatype properties**:
  - `cacontology-soe:communitySlangTerm` (domain `SadisticOnlineExploitationNetwork`, range `xsd:string`)
  - `cacontology-soe:coercionShowType` (domain `LivestreamedCoercionShow`, range `xsd:string`)

- **Add object properties**:
  - `cacontology-soe:hostsCoercionShow` (domain `SadisticOnlineExploitationNetwork`, range `LivestreamedCoercionShow`)

- **Non-duplication note (implementation constraint)**:
  - Do **not** create SOE duplicates of existing extremist-enterprises classes such as `CrossPlatformCoordination`, `PlatformMigrationStrategy`, `PrivateGroupManagement`, `SelfHarmCoercion`.
  - In SOE scenarios where those concepts are evidenced, reuse `cacontology-enterprises:*` directly in the KG (and optionally relate them to the SOE network via existing UCO/CASE action-object patterns).

- **SHACL (in `cacontology-soe-shapes.ttl`)**:
  - `SadisticOnlineExploitationNetworkShape`: require `rdfs:label` and allow optional `communitySlangTerm`
  - `LivestreamedCoercionShowShape`: require `coercionShowType` with `sh:in ( "watch_party" "cut_show" "cut_stage" "stage" )`

### 2.1b Minimum-link obligations (connectivity-by-design plan)

| New class | Example instance must be connected by | Grounding |
|---|---|---|
| `cacontology-sextortion:SadisticSextortion` | `cacontology-sextortion:employsThreat` → at least 1 threat + `uco-action:object` (link to normalized doc) | `normalized.txt` line 46 |
| `cacontology-sextortion:DoxxingThreat` | `uco-action:object` (link to normalized doc) or link via `employsThreat` from a sextortion incident | `normalized.txt` line 40 |
| `cacontology-sextortion:SwattingThreat` | same as above | `normalized.txt` line 40 |
| `cacontology-soe:SadisticOnlineExploitationNetwork` | `cacontology-soe:hostsCoercionShow` OR `uco-action:object` via a statement action + optional `communitySlangTerm` | `normalized.txt` lines 5–9 (and line 8) |
| `cacontology-soe:LivestreamedCoercionShow` | linked from SOE network via `hostsCoercionShow` + `uco-action:object` statement action | `normalized.txt` line 32 |

### 2.2 Example KG update plan (what will demonstrate which new terms)

Target example KG to update:

- `examples_knowledge_graphs/k2p-soe-information-example.ttl`

Add (or re-type) instances to demonstrate:

- `cacontology-sextortion:SadisticSextortion` (grounded to `normalized.txt` line 46)
- At least one each of:
  - `cacontology-sextortion:DoxxingThreat` (grounded to `normalized.txt` line 40 and/or line 6)
  - `cacontology-sextortion:SwattingThreat` (grounded to `normalized.txt` line 40 and/or line 6)
- `cacontology-soe:SadisticOnlineExploitationNetwork` (grounded to `normalized.txt` lines 5–9)
  - with `cacontology-soe:communitySlangTerm "the com"` (grounded to `normalized.txt` line 8)
- `cacontology-soe:LivestreamedCoercionShow` with `coercionShowType "cut_show"` (and/or `"watch_party"`) grounded to `normalized.txt` line 32

### 2.3 SPARQL query update plan (titles only)

Target query suite to update:

- `example_SPARQL_queries/k2p-soe-information-analytics.rq`

Add/extend queries:

- “Find all SadisticSextortion incidents and their threat mechanisms”
- “List all ThreatMechanism instances typed as DoxxingThreat/SwattingThreat”
- “List SOE networks and their slang terms (communitySlangTerm)”
- “List livestream coercion shows and their coercionShowType”

---

## Term Citation & Mapping Ledger (Required)

| CAC Term (fully-qualified) | dcterms:source citation | rdfs:seeAlso | External alignment | gUFO alignment | Explainability note |
|---|---|---|---|---|---|
| `cacontology-sextortion:SadisticSextortion` | Know2Protect SOE brochure, `normalized.txt` line 46 | `https://know2protect.gov` | (none proposed) | `gufo:Event` | Enables analytics on violence/self-harm/destruction-based sextortion threats vs classic sharing threats. |
| `cacontology-sextortion:DoxxingThreat` | Know2Protect SOE brochure, `normalized.txt` line 40 | `https://know2protect.gov` | (none proposed) | `gufo:Event` | Enables consistent modeling of doxxing as an intimidation threat mechanism in sextortion/SOE contexts. |
| `cacontology-sextortion:SwattingThreat` | Know2Protect SOE brochure, `normalized.txt` line 40 | `https://know2protect.gov` | (none proposed) | `gufo:Event` | Enables consistent modeling of swatting as an intimidation threat mechanism. |
| `cacontology-sextortion:ViolenceThreat` | Know2Protect SOE brochure, `normalized.txt` line 46 | `https://know2protect.gov` | (none proposed) | `gufo:Event` | Captures explicit threats of violence used to extort/coerce. |
| `cacontology-sextortion:SelfHarmThreat` | Know2Protect SOE brochure, `normalized.txt` lines 40–46 | `https://know2protect.gov` | (none proposed) | `gufo:Event` | Supports modeling threats compelling self-harm as coercion leverage. |
| `cacontology-sextortion:PropertyDestructionThreat` | Know2Protect SOE brochure, `normalized.txt` line 46 | `https://know2protect.gov` | (none proposed) | `gufo:Event` | Covers destruction-based coercion distinct from image-sharing threats. |
| `cacontology-soe:SadisticOnlineExploitationNetwork` | Know2Protect SOE brochure, `normalized.txt` lines 5–9 | `https://know2protect.gov` | `skos:closeMatch cacontology-enterprises:CyberExtremistNetwork` (**conditional**: only when ideology/enterprise evidence supports extremist-enterprises typing) | `gufo:FunctionalComplex` | Provides a first-class node for DHS-defined SOE networks to support cross-document aggregation without ideological over-commitment. |
| `cacontology-soe:LivestreamedCoercionShow` | Know2Protect SOE brochure, `normalized.txt` line 32 | `https://know2protect.gov` | `skos:closeMatch` to `cacontology-production:LiveStreamContent` (content vs event distinction) | `gufo:Event` | Enables pattern queries on livestreamed coercion rituals (“cut shows”, “watch parties”). |
| `cacontology-soe:communitySlangTerm` | Know2Protect SOE brochure, `normalized.txt` line 8 | `https://know2protect.gov` | (none proposed) | `gufo:Quality` (string attribute) | Standardizes slang-term capture for SOE communities. |
| `cacontology-soe:coercionShowType` | Know2Protect SOE brochure, `normalized.txt` line 32 | `https://know2protect.gov` | (none proposed) | `gufo:Quality` (string attribute) | Enables controlled vocabulary for “watch party / cut show / cut stage / stage”. |
| `cacontology-soe:hostsCoercionShow` | Know2Protect SOE brochure, `normalized.txt` line 32 | `https://know2protect.gov` | (none proposed) | (relational) | Links networks to the coercion shows they host/coordinate. |

---

## Checklist of file edits (proposal; “why here?”)

- `ontology/cacontology-sextortion.ttl`
  - Add `SadisticSextortion` and new threat mechanism subclasses (fits existing sextortion threat taxonomy).
- `ontology/cacontology-sextortion-shapes.ttl`
  - Add shapes for new threats + sadistic sextortion (validation + consistent data constraints).
- `ontology/cacontology-soe.ttl` (**new**)
  - Add SOE definitional taxonomy + SOE-specific livestream coercion show pattern **without duplicating** extremist-enterprises concepts.
- `ontology/cacontology-soe-shapes.ttl` (**new**)
  - Validate SOE network + coercion show instances.
- `examples_knowledge_graphs/k2p-soe-information-example.ttl`
  - Demonstrate each new term with grounded evidence pointers.
- `example_SPARQL_queries/k2p-soe-information-analytics.rq`
  - Add investigator queries for sadistic sextortion, doxxing/swatting threats, and livestream coercion shows.

---

## Risk list (top validation failure modes + mitigations)

1. **SHACL violations**
   - Mitigation: keep new shapes minimal (focus on required links + bounded enums where needed).
2. **Domain/range misuse**
   - Mitigation: place doxxing/swatting under `cacontology-sextortion:ThreatMechanism` (already a `uco-action:Action`) to avoid inventing ad-hoc relationships.
3. **Connectivity risk (isolated nodes)**
   - Mitigation: ensure each new instance is linked via at least one of: `uco-action:object`, `uco-core:hasFacet`, `investigation:provenanceRecordAction`.
4. **Scope drift**
   - Mitigation: keep SOE module focused on CSEA coercion networks; avoid modeling unrelated violent-content categories as domain nodes unless tied to CSEA exploitation/coercion.

---

## Governance gate queue (REVIEW REQUIRED)

- **New terms pending approval**:
  - `cacontology-sextortion:SadisticSextortion` (**REVIEW REQUIRED**)
  - `cacontology-sextortion:DoxxingThreat` (**REVIEW REQUIRED**)
  - `cacontology-sextortion:SwattingThreat` (**REVIEW REQUIRED**)
  - `cacontology-sextortion:ViolenceThreat` (**REVIEW REQUIRED**)
  - `cacontology-sextortion:SelfHarmThreat` (**REVIEW REQUIRED**)
  - `cacontology-sextortion:PropertyDestructionThreat` (**REVIEW REQUIRED**)
  - `cacontology-soe:SadisticOnlineExploitationNetwork` (**REVIEW REQUIRED**)
  - `cacontology-soe:LivestreamedCoercionShow` (**REVIEW REQUIRED**)
  - `cacontology-soe:communitySlangTerm` (**REVIEW REQUIRED**)
  - `cacontology-soe:coercionShowType` (**REVIEW REQUIRED**)
  - `cacontology-soe:hostsCoercionShow` (**REVIEW REQUIRED**)

- **SKOS mappings pending approval**:
  - (Optional) `cacontology-soe:LivestreamedCoercionShow skos:closeMatch cacontology-production:LiveStreamContent` (**REVIEW REQUIRED**; content-vs-event semantics need review)

- **Sensitive entities/claims pending approval**:
  - None in the proposed terms themselves (no victims/minors modeled as identities).
