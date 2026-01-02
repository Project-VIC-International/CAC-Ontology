# CAC Ontology Enhancement Agent Prompt (v2)

## Context

You are enhancing the CAC Ontology (Crimes Against Children Ontology): a semantic framework for modeling child exploitation investigations, operations, legal process, and offender/victim behaviors.

- **Repository root**: `D:\Project VIC\CAC-Ontology\CAC-Ontology\`
- **Ontology modules**: `ontology/*.ttl`
- **SHACL shapes**: `ontology/*-shapes.ttl`
- **Examples**: `examples_knowledge_graphs/*.ttl`
- **SPARQL queries**: `example_SPARQL_queries/*.rq`
- **Current version**: read `CHANGELOG.md`

### Foundational Ontologies (MUST follow)

- **UCO Action**: `https://ontology.unifiedcyberontology.org/uco/action/`
  - Use `uco-action:Action` to model actions generally.
- **CASE Investigation**: `https://ontology.caseontology.org/case/investigation/`
  - Use for investigative actions, provenance, authorizations, exhibits, and lifecycle semantics:
    - `investigation:InvestigativeAction`
    - `investigation:ProvenanceRecord`
    - `investigation:Authorization`
- **UCO Core**: `https://ontology.unifiedcyberontology.org/uco/core/`
  - Use `uco-core:UcoObject` for **physical** (non-digital) things.
- **UCO Observable**: `https://ontology.unifiedcyberontology.org/uco/observable/`
  - Use `uco-observable:ObservableObject` for **digital** artifacts only.

### Non‑negotiables (Follow Exactly)

- **Search-first / no duplicates**: before creating any class/property, search the codebase for existing terms and document what you found.
- **Actions**: investigative workflow actions MUST be `investigation:InvestigativeAction` (or a CAC subclass of it). Use `uco-action:Action` when it’s not investigative workflow.
- **Authorizations**: warrants/consents MUST be `investigation:Authorization` (or a CAC subclass of it).
- **Provenance**: chain-of-custody records MUST be `investigation:ProvenanceRecord` (or a CAC subclass of it).
- **Physical vs digital**:
  - Physical items (vape, condoms, buildings, vehicles, paper documents): `uco-core:UcoObject`
  - Digital artifacts (messages, files, images, recordings as files): `uco-observable:ObservableObject`
- **SHACL validation assumes NO reasoning**: do not rely on RDFS/OWL inference to satisfy SHACL. Example graphs MUST include explicit parent `rdf:type` assertions needed for shapes.
- **`dcterms:modified` policy**: update `dcterms:modified` ONLY on ontology/shapes files where **classes or properties were added/updated** (not for purely version-string or formatting-only changes).

### Naming conventions (Use consistently)

- **caseId**: short, kebab-case (e.g., `miami-icac-felipe-lopez`)
- **branch**: `release/vX.Y.Z-[caseId]`
- **example KG**: `examples_knowledge_graphs/[caseId]-example.ttl`
- **SPARQL queries**: `example_SPARQL_queries/[caseId]-analytics.rq`
- **example base IRI**: `https://example.org/cac/[caseId]/`
- **classes**: PascalCase
- **properties** (datatype/object): camelCase

### CAC namespace reminders (examples)

```turtle
@prefix cacontology: <https://cacontology.projectvic.org#> .
@prefix cacontology-undercover: <https://cacontology.projectvic.org/undercover#> .
@prefix cacontology-physical: <https://cacontology.projectvic.org/physical#> .
@prefix cacontology-tactical: <https://cacontology.projectvic.org/tactical#> .
@prefix cacontology-sentencing: <https://cacontology.projectvic.org/sentencing#> .
# ... additional modules - see ontology/ directory for complete list
```

---

## Input Document

Analyze the following press release/document and enhance the CAC Ontology to model its unique concepts.

---
[PASTE YOUR PRESS RELEASE OR DOCUMENT HERE]
---

---

## Required Workflow (Do all phases in order)

## Phase 0: Setup + Guardrails (before you propose changes)

- Determine a **caseId**.
- Identify the likely CAC modules involved (e.g., undercover, physical evidence, tactical, sentencing).
- Confirm which foundational ontology patterns apply (UCO Action, CASE Investigation, UCO Core/Observable).
- Run a **search-first sweep** in the repo for likely existing terms (classes + properties) to avoid duplication.

### Phase 0 Deliverables (must output)

- A 5–15 bullet “Working assumptions” list (only what you need).
- A short list of candidate modules/files to change.
- A list of existing terms found that you plan to reuse.

---

## Phase 1: Concept Extraction + Mapping

Extract concepts from the document and map them to:

- Existing CAC terms (preferred), or
- Existing UCO/CASE terms, or
- Proposed new CAC terms (only when needed).

### Phase 1 Deliverables (must output)

1. **Concept Inventory Table** with columns:
   - Concept
   - Category (Entity / Action / Evidence / Legal / Location / Org / Other)
   - Source snippet (quote or paraphrase)
   - Proposed modeling approach (reuse / extend / new)
2. **Mapping Table** with columns:
   - Document concept → Existing term OR Proposed new term (namespace + local name)
   - Rationale
3. **Change List by File** (exact file paths) with “why here?” justification.

---

## Phase 2: Implementation Plan (must happen before edits)

Write a concrete implementation plan with:

- New/updated classes (with `rdfs:subClassOf`)
- New/updated datatype properties (domain/range)
- New/updated object properties (domain/range)
- SHACL shapes to add/update (targets, required properties, enums)
- Example knowledge graph scope (which instances demonstrate which new terms)
- SPARQL query scope (titles + what each answers)

### Phase 2 Deliverables (must output)

- A bullet list of **exact new/updated terms** (fully-qualified)
- A checklist of file edits (each item: file → change summary)
- A “risk list” (top 3 ways SHACL might fail and how you’ll prevent it)

---

## Phase 3: Ontology + Shapes Implementation

Implement changes in `ontology/*.ttl` and `ontology/*-shapes.ttl` as planned.

### Implementation rules

- Every new class/property MUST have `rdfs:label` and `rdfs:comment`.
- Every new property MUST have `rdfs:domain` and `rdfs:range` (unless there’s an explicit reason not to—document it).
- Avoid over-fitting the ontology to a single case; keep terms reusable.
- If you relocate classes between modules, update imports/cross-references and ensure shapes still target the right class IRIs.

### Phase 3 Deliverables (must output)

- A summary list of what was added/changed per file.
- A list of which files had **classes/properties changed** (these are candidates for `dcterms:modified` update later).

---

## Phase 4: Example Knowledge Graph (KG)

Create `examples_knowledge_graphs/[caseId]-example.ttl` that demonstrates:

- Key entities, actions, evidence, and legal concepts in the document
- Every new/updated class/property added in Phase 3
- SHACL compliance **without reasoning**

### KG rules (critical)

- Use base prefix:

```turtle
@prefix ex: <https://example.org/cac/[caseId]/> .
```

- Add explicit parent `rdf:type` triples when needed to satisfy SHACL (no reliance on subclass inference).
- Include `rdfs:label` and `rdfs:comment` on major instances (suspect/persona/operation/charges/evidence).

### Phase 4 Deliverables (must output)

- A short “KG coverage map”: which instance demonstrates which new term(s).

---

## Phase 5: SPARQL Queries

Create `example_SPARQL_queries/[caseId]-analytics.rq` with **10–15** investigator-focused queries.

### Query rules

- Each query MUST include the required prefixes in the query text.
- Each query MUST be runnable against the example KG (no external inference required).
- Add a comment header before each query: purpose + what it returns.

### Recommended query topics

- Timeline of actions/events
- Undercover communications patterns
- Evidence/provenance/collection actions
- Authorization audit (consent/warrant linkage)
- Charges summary by statute/jurisdiction
- Location/meeting arrangement analysis
- Cross-evidence corroboration (e.g., recording matches self-identification)

---

## Phase 6: SHACL Validation (Docker-first)

### Primary path (preferred)

- Follow `testing/DOCKER_README.md`
- Run from `testing/`:

```bash
docker compose down
docker compose up --build --abort-on-container-exit
```

### Fallback path (CLI)

If Docker isn’t available, use pySHACL CLI (avoid fragile `python -c` quoting on Windows):

```bash
pyshacl -s ontology/<shapes-file>.ttl -d examples_knowledge_graphs/[caseId]-example.ttl -f human
```

### Phase 6 Deliverables (must output)

- A pass/fail matrix: shapes file → conforms? (yes/no)
- If failures occurred: list the fixes made and re-run results.

---

## Phase 7: Versioning + Release + PR

### Versioning rules

- Choose a new version using semver:
  - **MINOR** for new classes/properties/features (most cases)
  - **PATCH** for fixes only
  - **MAJOR** only for breaking changes
- Update `CHANGELOG.md` with:
  - Summary
  - New/changed terms
  - New example KG + queries
  - How validated (SHACL)
- Update version metadata in ontology files as required by CAC conventions (e.g., version IRI/info).

### `dcterms:modified` rule (IMPORTANT)

- Update `dcterms:modified` ONLY in files where **classes/properties were added or updated**.
- Do NOT update `dcterms:modified` for changes like:
  - version string replacement only
  - whitespace/formatting only
  - comment-only changes (unless you treat those as semantic—if so, document it)

### Git/PR workflow rules

- Create branch: `release/vX.Y.Z-[caseId]`
- Commit message MUST include:
  - What changed (terms + files)
  - Why (document-driven)
  - How validated (SHACL commands/results)
- Avoid force-push. If you must amend after pushing, use `--force-with-lease`.

---

## Final Output Requirements (must include)

1. Concept Inventory Table + Mapping Table
2. Exact list of new/updated terms (fully-qualified)
3. File-by-file change summary
4. SHACL validation summary (Docker-first), including failures and fixes if any
5. Version decision + `dcterms:modified` updates list (which files, what date)
6. Branch name + commit hash + PR link

---

## Example patterns (reference only)

### New class

```turtle
cacontology-undercover:SiblingPersonaOperation rdf:type owl:Class ;
    rdfs:label "Sibling Persona Operation"@en ;
    rdfs:comment "Undercover operation where personas are presented as siblings to engage with suspects."@en ;
    rdfs:subClassOf cacontology-undercover:MultiplePersonaOperation .
```

### New datatype property

```turtle
cacontology-undercover:ageStatedToSuspect rdf:type owl:DatatypeProperty ;
    rdfs:label "Age Stated to Suspect"@en ;
    rdfs:comment "The age that was stated to the suspect during the undercover operation."@en ;
    rdfs:domain cacontology-undercover:AgeAcknowledgment ;
    rdfs:range xsd:nonNegativeInteger .
```

### New SHACL shape

```turtle
cacontology-undercover:AgeAcknowledgmentShape rdf:type sh:NodeShape ;
    sh:targetClass cacontology-undercover:AgeAcknowledgment ;
    rdfs:label "Age Acknowledgment Shape"@en ;
    sh:property [
        sh:path cacontology-undercover:ageStatedToSuspect ;
        sh:datatype xsd:nonNegativeInteger ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:minInclusive 0 ;
        sh:maxInclusive 17 ;
        sh:message "Age acknowledgment must specify the age stated (0-17)."@en
    ] .
```
