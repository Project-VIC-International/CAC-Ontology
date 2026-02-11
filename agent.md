# CAC Ontology Enhancement Agent Prompt (v3)

## Context

You are enhancing the CAC Ontology (Crimes Against Children Ontology): a semantic framework for modeling child sexual exploitation and abuse (CSEA) investigations, law enforcement operations, digital forensics, legal process, civil society rescue actions, offender tradecraft, and victim/survivor terminology.

- **Repository root**: `D:\Project VIC\CAC-Ontology\CAC-Ontology\`
- **Ontology modules**: `ontology/*.ttl`
- **SHACL shapes**: `ontology/*-shapes.ttl`
- **Examples**: `examples_knowledge_graphs/*.ttl`
- **SPARQL queries**: `example_SPARQL_queries/*.rq`
- **Current version**: read `CHANGELOG.md`

### Strategic Goals

The CAC Ontology exists to support explainable, evidence-backed analytics that:

- Identify **recurring offender tradecraft** patterns across cases.
- Analyze **law enforcement investigation and operations responses** to understand what works.
- Model **legal process tradecraft** to find improvements.
- Enable discovery of methods to **find and rescue children** from exploitation and abuse.
- Support **offender identification** and **recidivism reduction**.
- Make everything in this domain **explainable** with full provenance.

---

## Automation Mode (Single vs Batch)

This prompt supports two modes:

### Single-Document Mode

Use when manually analyzing one press release or document. Paste the document in the Input Document section and proceed through all phases.

### Batch Mode (Automation Default)

Use when processing multiple documents, press releases, or tool exports at scale. Requires a **batch manifest** as input.

#### Batch Manifest (Required Fields - UCO Aligned)

All batch manifest fields map to UCO (Unified Cyber Ontology) terms for interoperability:

```yaml
# Batch-level metadata
batch:
  uco-core:id: "urn:uuid:<uuid>"           # Unique batch identifier (types:Identifier)
  uco-core:name: "<batch name>"            # Human-readable batch name
  uco-core:objectCreatedTime: "<ISO 8601>" # When batch was created
  
  # Agent Orchestration (for automated pipelines)
  agentOrchestration:
    enabled: true                          # Enable LLM-orchestrated acquisition
    fetchMethod: "<api | scrape | manual | export>"  # Primary acquisition method
    preprocessingPipeline:                 # Ordered list of preprocessing steps
      - "pdf_to_text"
      - "html_clean"
      - "chunk_by_paragraph"
    scopeScreeningModel: "<model identifier>"  # Model for semantic scope filtering
    deconflictionEnabled: true             # Enable cross-document entity resolution

# Per-document metadata
documents:
  - # Document identity (uco-observable:ObservableObject)
    uco-core:id: "urn:uuid:<uuid>"         # Unique document identifier (types:Identifier)
    uco-core:name: "<document name>"       # Human-readable document name
    
    # Source location (observable:URLFacet or observable:FileFacet)
    observable:url: "<URL>"                # Source URL (for web sources)
    observable:filePath: "<path>"          # File path (for local sources)
    
    # Collection action (uco-action:Action or investigation:InvestigativeAction)
    collectionAction:
      uco-action:startTime: "<ISO 8601>"   # When collection occurred
      uco-action:performer: "urn:uuid:<uuid>"  # Who/what collected (Identity)
      uco-core:description: "<api | scrape | manual | export>"  # Collection method
    
    # Content metadata (observable:ContentDataFacet)
    observable:mimeType: "<MIME type>"     # e.g., "text/html", "application/pdf"
    observable:sizeInBytes: <integer>      # Size of raw content in bytes
    
    # Hash verification (observable:HashFacet via types:Hash)
    observable:hash:
      types:hashMethod: "SHA-256"          # Hash algorithm used
      types:hashValue: "<hash value>"      # The computed hash
    
    # Preprocessing (uco-action:Action for normalization)
    normalizationAction:
      uco-core:description: "<preprocessing steps applied>"
      uco-action:startTime: "<ISO 8601>"
      uco-action:result: "urn:uuid:<uuid>" # Reference to normalized output
```

#### UCO Property Reference

| Manifest Field | UCO Term | UCO Namespace |
|----------------|----------|---------------|
| Batch/Document ID | `uco-core:id` | `https://ontology.unifiedcyberontology.org/uco/core#` |
| Name | `uco-core:name` | `uco-core:` |
| Creation time | `uco-core:objectCreatedTime` | `uco-core:` |
| URL source | `observable:url` | `https://ontology.unifiedcyberontology.org/uco/observable#` |
| File path | `observable:filePath` | `observable:` |
| MIME type | `observable:mimeType` | `observable:` |
| Size | `observable:sizeInBytes` | `observable:` |
| Hash method | `types:hashMethod` | `https://ontology.unifiedcyberontology.org/uco/types#` |
| Hash value | `types:hashValue` | `types:` |
| Action start | `uco-action:startTime` | `https://ontology.unifiedcyberontology.org/uco/action#` |
| Performer | `uco-action:performer` | `uco-action:` |
| Action result | `uco-action:result` | `uco-action:` |
| Description | `uco-core:description` | `uco-core:` |

#### Batch Mode Requirements

- Process each document through the full phase pipeline.
- Maintain deterministic outputs (same input → same output).
- Produce per-document artifacts (skeleton TTL, provenance, mappings).
- Merge KGs while preserving UUID uniqueness across documents.

---

## Scope Definition (In-Scope Topics Only)

The CAC Ontology models ONLY the following topics. **Do not model out-of-scope content as domain triples.**

### In-Scope Topics

- Child sexual exploitation and abuse (CSEA)
- Law enforcement operations and investigations targeting CSEA crimes
- Digital investigations and forensics related to CSEA
- Legal process surrounding CSEA investigations and operations
- Civil society actions that help rescue children from sexual exploitation
- Offender tradecraft (methods, tools, behaviors)
- Victim/survivor terminology and support concepts

### Out-of-Scope Handling (Strict)

- **Do NOT create domain triples** for content unrelated to the above topics.
- **DO retain minimal provenance**: record that the document was collected using UCO terms (`observable:URLFacet`/`FileFacet`, `observable:HashFacet`, collection action with `uco-action:startTime` + `uco-action:performer`) even if content is out-of-scope.
- **DO produce an "excluded topics" summary** in the run report listing what was screened out and why.

---

## Foundational Ontologies (MUST follow)

- **UCO Action**: `https://ontology.unifiedcyberontology.org/uco/action/`
  - Use `uco-action:Action` to model actions generally.
- **CASE Investigation**: `https://ontology.caseontology.org/case/investigation/`
  - Use for investigative actions, provenance, authorizations, exhibits, and lifecycle semantics:
    - `investigation:InvestigativeAction`
    - `investigation:ProvenanceRecord`
    - `investigation:Authorization`
- **UCO Core**: `https://ontology.unifiedcyberontology.org/uco/core/`
  - Use `uco-core:UcoObject` for **physical** (non-digital) things.
  - Use `uco-core:hasFacet` to attach multiple perspective-based facets to objects.
- **UCO Observable**: `https://ontology.unifiedcyberontology.org/uco/observable/`
  - Use `uco-observable:ObservableObject` for **digital** artifacts only.
  - Attach facets like `observable:FileFacet`, `observable:ContentDataFacet` for metadata and analysis perspectives.

---

## Non-negotiables (Follow Exactly)

### Search-First / No Duplicates

Before creating any class/property, search the codebase for existing terms and document what you found.

### Scope Gate (Strict)

Out-of-scope content MUST NOT become domain triples. Only model content relevant to CSEA, investigations, operations, legal process, civil society rescue, offender tradecraft, and victim/survivor terminology.

### UUID-Only Instances

Every instance IRI MUST be `urn:uuid:<uuid>` format. This includes:

- All domain instances (persons, actions, evidence, etc.)
- All facet instances
- All provenance nodes

#### UUID Generation Policy

**UUIDv4** (random): Use for interactive/non-repeatable extraction where determinism is not required.

**UUIDv5** (deterministic): Use for **example KG generation** and **derived artifacts** where repeatability is required.

**Determinism requirement**: Same input + same normalized text → same UUID IRIs for example outputs.

#### UUIDv5 Naming Conventions

Use **document UUID as namespace** and structured name strings:

```python
import uuid

# Document namespace (the source document's UUID)
DOC_NAMESPACE = uuid.UUID("82588a71-7176-4cd0-aaee-56cffc467f86")

# Derived UUIDs for entities extracted from document
affiliate_uuid = uuid.uuid5(DOC_NAMESPACE, "affiliate:Ogden Police Department")
action_uuid = uuid.uuid5(DOC_NAMESPACE, "action:affiliates_listed")
facet_uuid = uuid.uuid5(DOC_NAMESPACE, "facet:content_data:raw_html")
provenance_uuid = uuid.uuid5(DOC_NAMESPACE, "provenance:collection")
```

**Name string patterns**:
- `"affiliate:<org_label>"` — for list items (organizations, contacts)
- `"action:<action_type>"` — for actions (affiliates_listed, funding_stated)
- `"facet:<facet_type>:<context>"` — for facets
- `"provenance:<record_type>"` — for provenance records
- `"crime:<crime_label>"` — for crime categories

**Benefits of UUIDv5 for examples**:
1. Regenerating the example KG produces identical output
2. Diffs show only semantic changes, not UUID churn
3. Testing and validation are reproducible
4. Cross-references between example files remain stable

Never reuse UUIDs across unrelated objects. UUIDs are globally unique within the CAC ecosystem.

### Facet-Based Modeling

Multi-perspective descriptions MUST use facets attached via `uco-core:hasFacet`. Use facets to represent:

- Different tool perspectives (e.g., Autopsy analysis vs EnCase analysis)
- Different analyst interpretations
- Different temporal snapshots

Do NOT create excessive subclasses when facets are more appropriate.

### Duck Typing (UCO/CASE Pattern)

Follow the UCO/CASE duck typing principle for flexible, facet-based modeling:

- **Prefer facets over subclasses** for adding capabilities or perspectives to objects
- An object's behavior is defined by its facets, not just its class
- Use `uco-core:hasFacet` to attach multiple perspectives without rigid hierarchies
- Create new subclasses ONLY when:
  - The concept has intrinsic identity properties (not just perspectives/views)
  - Facet attachment cannot capture the semantics
  - The class represents a fundamentally different kind of thing
- **Validate extensions against UCO/CASE SHACL shapes**
- Import UCO/CASE modules verbatim; extend via subclasses/facets only

**Duck Typing Examples**:
- A file that's also evidence: `uco-observable:ObservableObject` + `investigation:ExhibitFacet` (NOT a new EvidenceFile subclass)
- A person who's a suspect: `uco-identity:Person` + role facet (NOT a Suspect subclass)
- An image with analysis: `uco-observable:ObservableObject` + `observable:ContentDataFacet` + `cacontology:AnalysisFacet`

### Graph Connectivity (No Isolated Nodes)

Every node in the KG MUST be connected to at least one other node:

- **Minimum degree = 1**: All instance nodes must have at least one incoming or outgoing edge (excluding `rdf:type`)
- **Evidence-based edges only**: Do NOT invent relationships to satisfy connectivity
- **Relationship-centric extraction**: Extract triples (subject-predicate-object), not standalone entities
- **Ontology-guided connections**: Use UCO/CASE patterns for required relationships:
  - Actions: `uco-action:performer`, `uco-action:object`, `uco-action:instrument`, `uco-action:result`
  - Provenance: `investigation:ProvenanceRecord` links via `investigation:provenanceRecordAction`
  - Evidence: `investigation:exhibitNumber`, `uco-core:hasFacet`, `uco-core:object`

**Provenance-Anchoring Pattern (Connectivity Fallback)**:

When a concept has no explicit relationship in the source text, anchor it to the source document via a **statement/listing action**:

```turtle
# Statement action pattern: "Webpage lists X"
ex:statement-action-uuid a uco-action:Action ;
    rdfs:label "Webpage lists affiliate organizations"@en ;
    uco-action:startTime "<collection-timestamp>"^^xsd:dateTime ;
    uco-action:performer ex:source-org-uuid ;          # Who/what made the statement
    uco-action:object ex:source-document-uuid ,        # The source document
                      ex:entity-uuid-1 ,               # Entities mentioned in statement
                      ex:entity-uuid-2 ;
    uco-core:description "Grounded in <file> lines X-Y: '<quote>'"@en .
```

This pattern ensures:
1. The entity is connected via `uco-action:object` to a grounded action
2. The action links back to the source document (provenance chain)
3. The `uco-core:description` contains evidence pointer (file + lines + quote)

**Isolated node handling (CRITICAL)**:
  - If no valid edge exists in source text AND no provenance-anchoring is possible: **Do NOT create the node**
  - Mark as **REVIEW REQUIRED** if the concept seems important but cannot be grounded
  - Do NOT hallucinate relationships to force connectivity
  - Truly isolated entities indicate extraction error—remove them

**Low-degree warning (degree = 1)**:
  - Nodes with only one edge (excluding `rdf:type`) should be flagged for human review
  - Consider: Can additional grounded relationships be found? Is the single edge sufficient?
  - Target: <10% of nodes should have degree = 1

- **Provenance for all edges**: Every relationship must have an evidence pointer or confidence level recorded in an `investigation:ProvenanceRecord` or via `uco-core:description`

### Provenance Completeness

Every collected source MUST have the following represented in the KG using UCO terms:

- Source URI/path → `observable:url` or `observable:filePath` (via `observable:URLFacet` or `observable:FileFacet`)
- Collection date/time → `uco-action:startTime` (on collection action)
- Collection method → `uco-core:description` (on collection action)
- Collector identity → `uco-action:performer` (pointing to `uco-identity:Identity`)
- Content hash → `types:hashMethod` + `types:hashValue` (via `observable:HashFacet`)

Downstream artifacts and claims MUST trace back to their source via `investigation:ProvenanceRecord`.

### Evidence Pointers + Confidence (UCO/CASE-Native)

Every extracted assertion MUST include grounded evidence and confidence using **existing UCO/CASE patterns** (no new CAC terms required):

**Evidence Pointer** — Use `investigation:ProvenanceRecord` with structured description:

```turtle
ex:provenance-record-uuid a investigation:ProvenanceRecord ;
    rdfs:label "Provenance: <what was extracted>"@en ;
    uco-core:object ex:source-document-uuid ;           # The source artifact
    investigation:provenanceRecordAction ex:action-uuid ; # Action that produced/extracted the claim
    uco-core:description "Evidence pointer: <file> lines X-Y. Quote: '<verbatim text>'"@en .
```

**Confidence Level** — Use one of these approaches (in order of preference):

1. **UCO ConfidenceFacet** (when available in tooling):
   ```turtle
   ex:claim-uuid uco-core:hasFacet ex:confidence-facet-uuid .
   ex:confidence-facet-uuid a uco-core:ConfidenceFacet ;
       uco-core:confidence 0.95 .  # numeric 0.0-1.0
   ```

2. **Structured description fallback** (always available):
   ```turtle
   ex:action-uuid uco-core:description 
       "Confidence: high. Justification: direct quote, unambiguous. Evidence: lines 45-47."@en .
   ```

**Confidence levels**:
- **high** (0.85-1.0): Direct quote, unambiguous meaning, well-defined term
- **medium** (0.6-0.84): Paraphrased, some interpretation required, likely correct
- **low** (0.0-0.59): Inferred, ambiguous, or requires domain expertise to confirm

**Allowed Grounding Patterns** (copy/paste-ready templates):

1. **Statement action** (webpage/document says X):
   ```turtle
   ex:statement-action-uuid a uco-action:Action ;
       rdfs:label "Webpage states funding source"@en ;
       uco-action:startTime "<timestamp>"^^xsd:dateTime ;
       uco-action:performer ex:source-org-uuid ;
       uco-action:object ex:source-doc-uuid, ex:claim-subject-uuid ;
       uco-core:description "Grounded in normalized.txt lines 37-40. Confidence: high."@en .
   ```

2. **List publication** (source lists items):
   ```turtle
   ex:listing-action-uuid a uco-action:Action ;
       rdfs:label "Webpage lists affiliate organizations"@en ;
       uco-action:startTime "<timestamp>"^^xsd:dateTime ;
       uco-action:performer ex:source-org-uuid ;
       uco-action:object ex:source-doc-uuid, ex:item-1-uuid, ex:item-2-uuid ;
       uco-core:description "Grounded in normalized.txt lines 64-128. Confidence: high."@en .
   ```

3. **Normalization/derivation** (raw→normalized):
   ```turtle
   ex:normalization-action-uuid a uco-action:Action ;
       rdfs:label "Normalization: HTML to text"@en ;
       uco-action:performer ex:agent-uuid ;
       uco-action:object ex:raw-doc-uuid ;
       uco-action:result ex:normalized-doc-uuid ;
       uco-core:description "html_clean + whitespace normalization. Confidence: high (deterministic)."@en .
   ```

### Privacy / Harm Minimization

- Minimize victim/survivor PII; avoid storing sensitive raw content.
- Store hashes/metadata where possible instead of raw sensitive data.
- **NEVER store CSAM content**; store only references/hashes/metadata.
- Require a redaction decision for any sensitive snippet used as evidence.

### Human Review Gates

The following MUST be flagged as **REVIEW REQUIRED** before implementation:

- New CAC terms (classes/properties)
- SKOS mappings to external ontologies
- Sensitive entity modeling (victims, minors)

### Deconfliction Rules

- Never merge instances by label alone.
- Require explicit evidence-based linking decisions.
- When linking instances across documents, document the evidence supporting the link.

### Term Citations (Required)

Every new/updated CAC class or property MUST have:

- `dcterms:source` with a referenceable citation (string or URL)
- `rdfs:seeAlso` with a URL (when available)

### Equivalence Mappings

When a CAC concept aligns with an external term:

- Use `skos:exactMatch` for exact semantic equivalence
- Use `skos:closeMatch` for near equivalence
- Reserve `owl:equivalentClass` / `owl:equivalentProperty` for strict logical equivalence only (rare)

### Actions

Investigative workflow actions MUST be `investigation:InvestigativeAction` (or a CAC subclass). Use `uco-action:Action` when it's not investigative workflow.

### Authorizations

Warrants/consents MUST be `investigation:Authorization` (or a CAC subclass).

### Provenance Records

Chain-of-custody records MUST be `investigation:ProvenanceRecord` (or a CAC subclass).

### Physical vs Digital

- Physical items (devices, condoms, buildings, vehicles, paper documents): `uco-core:UcoObject`
- Digital artifacts (messages, files, images, recordings as files): `uco-observable:ObservableObject`

### SHACL Validation Assumes NO Reasoning

Do not rely on RDFS/OWL inference to satisfy SHACL. Example graphs MUST include explicit parent `rdf:type` assertions needed for shapes.

### `dcterms:modified` Policy

Update `dcterms:modified` ONLY on ontology/shapes files where **classes or properties were added/updated** (not for purely version-string or formatting-only changes).

---

## Namespace/Module Governance

### Namespace Discovery (Required Before Modeling)

Before proposing new terms, the AI Agent MUST search the following authoritative sources for existing namespaces and terms:

#### 1. CAC Ontology Namespaces
- **Base**: `https://cacontology.projectvic.org#`
- **Discovery**: Search the `ontology/` directory for all `*.ttl` files to find available CAC modules
- **Pattern**: `https://cacontology.projectvic.org/<module>#`

Example CAC namespaces (non-exhaustive, always verify against repo):

```turtle
@prefix cacontology: <https://cacontology.projectvic.org#> .
@prefix cacontology-undercover: <https://cacontology.projectvic.org/undercover#> .
@prefix cacontology-physical: <https://cacontology.projectvic.org/physical#> .
@prefix cacontology-tactical: <https://cacontology.projectvic.org/tactical#> .
@prefix cacontology-sentencing: <https://cacontology.projectvic.org/sentencing#> .
# ... discover additional modules from ontology/ directory
```

#### 2. CASE/UCO Namespaces
- **CASE**: `https://ontology.caseontology.org/`
- **UCO**: `https://ontology.unifiedcyberontology.org/`
- **Discovery**: Reference the CASE/UCO documentation and ontology files

Key UCO/CASE namespaces:

```turtle
@prefix case-investigation: <https://ontology.caseontology.org/case/investigation/> .
@prefix uco-action: <https://ontology.unifiedcyberontology.org/uco/action/> .
@prefix uco-core: <https://ontology.unifiedcyberontology.org/uco/core/> .
@prefix uco-identity: <https://ontology.unifiedcyberontology.org/uco/identity/> .
@prefix uco-location: <https://ontology.unifiedcyberontology.org/uco/location/> .
@prefix uco-observable: <https://ontology.unifiedcyberontology.org/uco/observable/> .
@prefix uco-tool: <https://ontology.unifiedcyberontology.org/uco/tool/> .
@prefix uco-types: <https://ontology.unifiedcyberontology.org/uco/types/> .
@prefix uco-vocabulary: <https://ontology.unifiedcyberontology.org/uco/vocabulary/> .
```

#### 3. gUFO (Foundational Ontology)
- **Base**: `http://purl.org/nemo/gufo#`
- **Purpose**: Lightweight implementation of the Unified Foundational Ontology (UFO)
- **Use cases**: When modeling needs foundational distinctions (e.g., `gufo:Object`, `gufo:Event`, `gufo:Relator`, `gufo:Quality`)

```turtle
@prefix gufo: <http://purl.org/nemo/gufo#> .
```

Key gUFO classes for CAC modeling:
- `gufo:Object` - Independent endurants (persons, organizations, physical items)
- `gufo:Event` - Occurrences in time (actions, incidents)
- `gufo:Relator` - Reified relationships (marriages, contracts, memberships)
- `gufo:Quality` - Measurable aspects (weight, age, duration)
- `gufo:Role` - Anti-rigid sortals (Student, Victim, Offender)
- `gufo:Phase` - Intrinsic contingent types (Child, Deceased)

#### 4. Standard Vocabularies

```turtle
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
```

### Creating New Modules

If no good alignment exists for new concepts, propose a **new CAC module namespace**:

1. Define a clear **scope statement** for the new module.
2. Create `ontology/<module>.ttl` with the ontology definitions.
3. Create `ontology/<module>-shapes.ttl` with SHACL shapes.
4. Add the new prefix to all relevant files.
5. Update imports in dependent modules.
6. Add Term Citation & Mapping Ledger entries for all new terms.

Example new namespaces (if needed):

- `cacontology-survivor:` for victim/survivor terminology
- `cacontology-civilsociety:` for civil society rescue organizations/actions

---

## Naming Conventions (Use Consistently)

- **caseId**: short, kebab-case (e.g., `miami-icac-felipe-lopez`)
- **batchId**: `urn:uuid:<uuid>`
- **documentId**: `urn:uuid:<uuid>`
- **branch**: `release/vX.Y.Z-[caseId]`
- **example KG**: `examples_knowledge_graphs/[caseId]-example.ttl`
- **SPARQL queries**: `example_SPARQL_queries/[caseId]-analytics.rq`
- **classes**: PascalCase
- **properties** (datatype/object): camelCase

---

## Input Document

### Single-Document Mode

Analyze the following press release/document and enhance the CAC Ontology to model its unique concepts.

---
[PASTE YOUR PRESS RELEASE OR DOCUMENT HERE]
---

### Batch Mode

Provide a batch manifest (YAML format as specified above) and ensure all source documents are accessible.

---

## Required Workflow (Do All Phases in Order)

---

## Phase -1: Data Acquisition + Preprocessing

**Purpose**: Automate collection, normalization, and provenance scaffolding before modeling.

### Phase -1 Steps

1. **Duplicate Detection (REQUIRED - Before Collection)**
   
   Before fetching any document, the AI Agent MUST query the Graph DB to check if the source has already been collected and processed.
   
   **For URL sources**, run this SPARQL query:
   ```sparql
   # Check if URL was already collected
   PREFIX observable: <https://ontology.unifiedcyberontology.org/uco/observable/>
   PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
   
   SELECT ?doc ?collectedAt ?hash WHERE {
     ?doc uco-core:hasFacet ?urlFacet .
     ?urlFacet a observable:URLFacet ;
               observable:url ?url .
     FILTER(STR(?url) = "<CANDIDATE_URL>")
     
     OPTIONAL {
       ?doc uco-core:hasFacet ?hashFacet .
       ?hashFacet a observable:HashFacet ;
                  observable:hash ?hashNode .
       ?hashNode types:hashValue ?hash .
     }
     OPTIONAL {
       ?action uco-action:object ?doc ;
               uco-action:startTime ?collectedAt .
     }
   }
   ```
   
   **For file path sources**, query by file path:
   ```sparql
   # Check if file path was already collected
   PREFIX observable: <https://ontology.unifiedcyberontology.org/uco/observable/>
   PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
   
   SELECT ?doc ?collectedAt ?hash WHERE {
     ?doc uco-core:hasFacet ?fileFacet .
     ?fileFacet a observable:FileFacet ;
                observable:filePath ?path .
     FILTER(STR(?path) = "<CANDIDATE_PATH>")
     
     OPTIONAL {
       ?doc uco-core:hasFacet ?hashFacet .
       ?hashFacet a observable:HashFacet ;
                  observable:hash ?hashNode .
       ?hashNode types:hashValue ?hash .
     }
   }
   ```
   
   **Decision logic**:
   - If **URL/path already exists** in Graph DB:
     - Compare content hash (if available) with current source hash
     - If hash matches: **SKIP** - document already processed, log as "already collected"
     - If hash differs: **FLAG for re-collection** - source content has changed, create new version
   - If **URL/path not found**: Proceed with collection
   
   **Deliverable**: Duplicate detection report listing:
   - Candidate sources checked
   - Already-collected sources (skipped)
   - Changed sources (flagged for re-collection with reason)
   - New sources (proceeding to collection)

2. **Entity Resolution for Near-Duplicates (REQUIRED - After Hash Check)**
   
   After exact URL/path matching and hash comparison, run similarity-based entity resolution to catch near-duplicates that exact matching misses (URL variations, dynamic content, reformatted documents).
   
   **Step 1: URL Similarity Check**
   - Normalize URLs: remove query parameters, trailing slashes, convert to lowercase
   - Compute Levenshtein distance or Jaccard similarity against existing URLs
   - If similarity > 0.9: **FLAG as potential duplicate** for review
   
   **SPARQL for fuzzy URL matching**:
   ```sparql
   # Near-duplicate URL detection (domain-based approximation)
   PREFIX observable: <https://ontology.unifiedcyberontology.org/uco/observable/>
   PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
   
   SELECT ?doc ?existingUrl WHERE {
     ?doc uco-core:hasFacet ?urlFacet .
     ?urlFacet a observable:URLFacet ;
               observable:url ?existingUrl .
     FILTER(CONTAINS(LCASE(STR(?existingUrl)), "<normalized_domain_or_path_segment>"))
   }
   ```
   
   **Step 2: Content Similarity Check**
   - Generate embedding for document content (using configured model)
   - Compare against embeddings of existing documents in vector index
   - If cosine similarity > 0.85: **FLAG for review** as potential duplicate
   
   **Step 3: Title/Label Fuzzy Matching**
   - Extract document title/headline
   - Compute similarity against existing document labels
   - If similarity > 0.8: **FLAG for review**
   
   **Decision logic for flagged pairs**:
   | Scenario | Action |
   |----------|--------|
   | URL similarity > 0.95 + content similarity > 0.9 | HIGH confidence duplicate - SKIP |
   | URL similarity > 0.9 + same domain | MEDIUM confidence - review hash difference |
   | Content similarity > 0.85 only | MEDIUM confidence - may be repost/syndication |
   | Title match only | LOW confidence - FLAG for human review |
   | All similarities < thresholds | PROCEED with collection |
   
   **Entity Resolution Tool Configuration** (add to batch manifest):
   ```yaml
   batch:
     entityResolution:
       enabled: true                    # Enable ER for near-duplicate detection
       tool: "dedupe | splink | embeddings"  # ER tool/method to use
       similarityThreshold: 0.85        # Minimum similarity to flag
       embeddingModel: "text-embedding-3-small"  # Model for content embeddings
       urlNormalization: true           # Normalize URLs before comparison
       reportNearDuplicates: true       # Include near-duplicates in report
   ```
   
   **Entity Resolution Deliverable** (add to duplicate detection report):
   - Near-duplicate candidates identified (with similarity scores)
   - ER tool/method used and configuration
   - Pairs flagged for human review (with similarity breakdown)
   - Resolution decisions (skip/proceed/merge) with justification

### Agent Orchestration (Batch Mode - When Enabled)

When `agentOrchestration.enabled: true` in the batch manifest, the following automated pipeline executes:

1. **Dispatch fetch agents**: Deploy appropriate agents per source type
   - API agents for structured data sources (justice.gov, court dockets)
   - Scraping agents for web pages (with rate limiting and robots.txt compliance)
   - Export agents for tool outputs (Autopsy, EnCase, Cellebrite reports)

2. **Run preprocessing pipeline**: Execute steps defined in `preprocessingPipeline`:
   - `pdf_to_text`: Extract text from PDFs preserving structure markers
   - `html_clean`: Strip HTML tags, preserve semantic structure
   - `chunk_by_paragraph`: Split into manageable chunks for processing
   - `ocr_images`: Extract text from images if present

3. **Semantic scope screening**: Use embeddings to filter content
   - Compute embedding for each chunk
   - Compare against CAC scope embeddings
   - Classify as in-scope (proceed) or out-of-scope (minimal provenance only)
   - Use model specified in `scopeScreeningModel`

4. **Parallel skeleton generation**: Generate UUID nodes + facets in parallel
   - Each agent produces skeleton TTL independently
   - Provenance records agent identity as `uco-action:performer`
   - Hash computed and stored in `observable:HashFacet`

5. **Agent provenance tracking**: Record all agent actions
   ```turtle
   ex:agent-run-uuid a uco-tool:Tool ;
       rdfs:label "CAC Ontology Batch Agent" ;
       uco-core:description "Automated acquisition and preprocessing agent" ;
       uco-tool:version "1.0" .
   
   ex:collection-action-uuid a investigation:InvestigativeAction ;
       uco-action:performer ex:agent-run-uuid ;
       uco-action:startTime "2024-01-15T10:30:00Z"^^xsd:dateTime ;
       uco-action:endTime "2024-01-15T10:31:45Z"^^xsd:dateTime .
   ```

2. **Fetch/Ingest Sources**
   - Retrieve documents from URLs, file paths, or tool exports.
   - Preserve raw artifacts alongside normalized versions.
   - **SKIP sources identified as duplicates in step 1** (unless flagged for re-collection).
   - When agent orchestration is enabled, this step is handled by dispatch agents above.

3. **Normalize Content**
   - Convert to plain text while preserving structure markers.
   - Record normalization steps in the manifest.

4. **Run Strict Scope Screen**
   - Classify each document/section as in-scope or out-of-scope.
   - Only proceed with in-scope content for domain modeling.
   - Record excluded topics with justification.

5. **Generate Per-Document KG Skeleton**
   - Create UUID nodes (`urn:uuid:<uuid>`) for:
     - Source artifact (the collected document)
     - Collection action (`investigation:InvestigativeAction`)
     - Provenance record (`investigation:ProvenanceRecord`)
   - Link collection action to source artifact and provenance record.
   - For **re-collected sources** (content changed), link to prior version via `uco-core:previousVersion` or similar provenance chain.

6. **Establish Evidence Indexing**
   - Create stable evidence pointers (documentId + span/offset scheme).
   - These will be referenced by assertions in later phases.

7. **Run Early Verification Checks**
   - SPARQL sanity queries to verify:
     - All collection actions have `uco-action:startTime` and `uco-action:performer`
     - All documents have `observable:HashFacet` with `types:hashMethod` and `types:hashValue`
     - All documents have source location (`observable:URLFacet` or `observable:FileFacet`)
     - All `uco-core:hasFacet` links point to typed facet nodes
     - All document nodes have required metadata
     - No duplicate URLs/paths were collected (deduplication verified)

### KG Deconfliction (Cross-Document Merge - Batch Mode)

When processing multiple documents, run deconfliction before merging KGs:

**Step 1: Query for potentially duplicate entities**

```sparql
# Find entities with similar labels across documents
SELECT ?ent1 ?ent2 ?label1 ?label2 ?doc1 ?doc2 WHERE {
  GRAPH ?doc1 { ?ent1 rdfs:label ?label1 . }
  GRAPH ?doc2 { ?ent2 rdfs:label ?label2 . }
  FILTER(?doc1 != ?doc2 && ?ent1 != ?ent2)
  FILTER(LCASE(STR(?label1)) = LCASE(STR(?label2)))
}
```

```sparql
# Find entities with matching identifiers (names, case numbers, etc.)
SELECT ?ent1 ?ent2 ?identifier WHERE {
  ?ent1 cacontology:hasIdentifier ?identifier .
  ?ent2 cacontology:hasIdentifier ?identifier .
  FILTER(?ent1 != ?ent2)
}
```

**Step 2: Decision logic for each candidate pair**

| Scenario | Action |
|----------|--------|
| Same UUID | Already linked, no action needed |
| Different UUID + same identifier | HIGH confidence match - link with `owl:sameAs` |
| Different UUID + same label + corroborating evidence | MEDIUM confidence - link with provenance |
| Different UUID + similar label only | FLAG for human review |
| Confidence < medium | Do NOT merge, flag for review |

**Step 3: Link with provenance (if approved)**

```turtle
# Linking two entities identified as the same
ex:entity-from-doc1 owl:sameAs ex:entity-from-doc2 .

# Provenance for the linking decision
ex:linking-decision-uuid a investigation:ProvenanceRecord ;
    rdfs:label "Entity Deconfliction Decision" ;
    uco-core:description "Linked based on matching case number and name" ;
    investigation:provenanceRecordAction ex:deconfliction-action-uuid ;
    cacontology:confidence "high" ;
    cacontology:evidencePointer "doc1:line45, doc2:line23" .
```

**Step 4: Never merge by label alone**
- Require at least one corroborating identifier or evidence pointer
- Document all linking decisions for auditability
- Flag uncertain cases for human review

**Deconfliction Deliverable**: Report listing:
- Candidate entity pairs found
- Pairs linked (with confidence and evidence)
- Pairs flagged for human review
- Pairs rejected (with reason)

### Phase -1 Deliverables (Must Output)

- **Duplicate detection report**:
  - Total candidate sources checked
  - Sources skipped (already collected, hash unchanged)
  - Sources flagged for re-collection (content changed, with prior version reference)
  - New sources collected
  - **Entity Resolution results** (when ER enabled):
    - Near-duplicate candidates identified (with similarity scores)
    - ER tool/method used and configuration
    - Pairs flagged for human review
    - Resolution decisions with justification
- **Agent orchestration report** (if enabled):
  - Agents dispatched and their status
  - Preprocessing pipeline execution results
  - Scope screening decisions per chunk
- **Batch manifest** (completed with all required fields, excluding skipped duplicates)
- **In-scope decision per document** + excluded-topics summary
- **Per-document skeleton TTL** (UUID-only, minimal nodes)
- **Provenance completeness report** (UCO properties present per document):
  - `observable:URLFacet` or `observable:FileFacet` (source location)
  - `uco-action:startTime` (collection time on action)
  - `uco-action:performer` (collector identity)
  - `observable:HashFacet` with `types:Hash` (content verification)
- **KG deconfliction report** (for batch mode):
  - Candidate entity pairs identified
  - Pairs linked with provenance
  - Pairs flagged for human review
  - Linking decisions with confidence levels
- **Early verification results** (SPARQL checks pass/fail, including deduplication verification)

---

## Phase 0: Setup + Guardrails

### Phase 0 Steps

- Determine a **caseId** (for single-doc) or confirm **batchId** (for batch).
- Identify the likely CAC modules involved (e.g., undercover, physical evidence, tactical, sentencing).
- Confirm which foundational ontology patterns apply (UCO Action, CASE Investigation, UCO Core/Observable).
- Run a **search-first sweep** in the repo for likely existing terms (classes + properties) to avoid duplication.
- Confirm scope categories: all content must relate to CSEA, investigations, operations, legal process, civil society rescue, offender tradecraft, or victim/survivor terminology.

### Phase 0 Deliverables (Must Output)

- A 5–15 bullet "Working assumptions" list (only what you need).
- A short list of candidate modules/files to change.
- A list of existing terms found that you plan to reuse.
- **Scope confirmation**: list of documents in-scope vs out-of-scope (out-of-scope stops at minimal provenance).

---

## Phase 1: Concept Extraction + Mapping

Extract concepts from the document and map them to:

- Existing CAC terms (preferred), or
- Existing UCO/CASE terms, or
- Proposed new CAC terms (only when needed).

### Phase 1 Requirements

For each concept/assertion:

- Assign a **UUID** for involved instances
- Identify **facets** required per perspective (tool vs analyst vs legal)
- Create an **evidence pointer** (documentId + span/quote)
- Assign a **confidence level** (high/medium/low) with justification

### Phase 1 Reasoning Procedure (Chain-of-Thought - Follow Step-by-Step)

For each sentence/paragraph in the document, follow this 12-step reasoning chain:

1. **Parse**: Identify candidate entities, actions, and relationships in the text
2. **Extract**: Name each concept and assign its category (Entity/Action/Evidence/Legal/Location/Org/Other)
3. **Search**: Check existing CAC/UCO/CASE/gUFO terms for a match before proposing new terms
4. **Map**: Assign to existing term OR propose new term with explicit rationale
5. **UUID**: Generate `urn:uuid:` identifier for each instance
   - Use `uuid.uuid4()` for interactive/non-repeatable extraction
   - Use `uuid.uuid5(doc_namespace, "type:label")` for deterministic example generation (see UUID policy)
6. **Facets**: Identify required facets per perspective:
   - Tool perspective (e.g., `observable:ContentDataFacet` for forensic tool output)
   - Analyst perspective (e.g., custom analysis facet for investigator interpretation)
   - Legal perspective (e.g., facets for evidentiary status)
7. **Relationships**: List candidate relationships with their expected domain/range
8. **Verify**: Run mock SPARQL to check domain/range compliance:
   ```sparql
   # Verify relationship domain/range
   ASK WHERE {
     ?subject a <ExpectedDomainClass> .
     ?object a <ExpectedRangeClass> .
   }
   ```
9. **Confidence**: Assign high/medium/low with explicit justification:
   - **High**: Direct quote, unambiguous meaning, well-defined term
   - **Medium**: Paraphrased, some interpretation required, likely correct
   - **Low**: Inferred, ambiguous, or requires domain expertise to confirm
10. **Evidence**: Record documentId + span/quote for full traceability

11. **Hallucination Check**: Before finalizing extraction:
    - Re-read the source text for the specific span being modeled
    - Verify: "Is every extracted detail directly stated or clearly implied in the source?"
    - Check for invented details:
      - Names/identifiers not explicitly in text
      - Dates/times not mentioned
      - Relationships not explicitly stated or strongly implied
      - Quantities or specifics not in source
    - If any detail cannot be traced to source:
      - **REMOVE** the unsupported detail entirely, OR
      - Mark confidence as **LOW** with note: "inferred, not explicit in source"
    - Document: "Hallucination check: [PASS/ADJUSTED] - [brief note if adjusted]"

12. **Connectivity Check (MANDATORY GATE)**: Before finalizing any node:
    - Verify: "Does this node have at least one relationship to another node (excluding `rdf:type`)?"
    - For each extracted entity:
      - List all outgoing edges (predicates where entity is subject)
      - List all incoming edges (predicates where entity is object)
      - If total edges = 0: **MUST resolve before proceeding**
    
    **Resolution order (try in sequence)**:
    1. **Find grounded relationship in text**: Re-read source for explicit or strongly implied connections
    2. **Apply provenance-anchoring pattern**: Create a statement/listing action linking the entity to the source document via `uco-action:object` with evidence pointer in `uco-core:description`
    3. **Do NOT create the node**: If neither option works, the entity cannot be grounded—omit it and flag as **REVIEW REQUIRED**
    
    **Never**: Invent relationships not supported by text. "Patch-connecting" is hallucination.
    
    - Relationship requirements:
      - Every entity MUST connect via at least one of: `uco-action:object`, `uco-core:hasFacet`, `uco-action:result`, `investigation:provenanceRecordAction`
      - Every action MUST have `uco-action:performer`, `uco-action:object`, or `uco-action:instrument`
      - Every evidence item MUST link to an action or provenance record
    
    - **Low-degree warning**: If degree = 1 (excluding `rdf:type`), flag for review—weakly connected
    
    - Document: "Connectivity check: [PASS/ANCHORED/FLAGGED/REMOVED] - [resolution used if any]"

**Example CoT Walkthrough**:
```
Sentence: "The suspect used a hypnosis script during the online chat."

1. Parse: Entity="suspect", Action="used", Object="hypnosis script", Context="online chat"
2. Extract: 
   - Concept: "HypnosisScript" (Category: Evidence)
   - Concept: "OnlineChatSession" (Category: Action)
3. Search: No existing CAC term for "HypnosisScript"; found cacontology:ChatSession
4. Map: 
   - HypnosisScript → NEW: cacontology-evidence:HypnosisScript (rationale: specific tradecraft artifact)
   - OnlineChatSession → REUSE: cacontology:ChatSession
5. UUID: urn:uuid:7f3a2b1c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
6. Facets: observable:ContentDataFacet (script text), cacontology:TradecraftFacet (method)
7. Relationships: cacontology:usedInAction (domain: Evidence, range: Action)
8. Verify: CHECK - HypnosisScript is Evidence, ChatSession is Action ✓
9. Confidence: HIGH - direct quote "used a hypnosis script"
10. Evidence: docId=urn:uuid:abc..., span="lines 42-42", quote="used a hypnosis script"
11. Hallucination Check:
    - Re-read: "The suspect used a hypnosis script during the online chat."
    - Verify: "hypnosis script" ✓ explicit, "online chat" ✓ explicit, "suspect" ✓ explicit
    - NOT in text: specific script name, chat platform name, script content
    - Decision: Do NOT invent platform name or script details; keep as stated
    - Result: PASS (no hallucination - all extracted details are in source)
12. Connectivity Check (MANDATORY GATE):
    - Entity: "HypnosisScript" (urn:uuid:7f3a...)
      - Outgoing: usedInAction → ChatSession ✓
      - Incoming: wasUsedBy ← Suspect (implied from context) ✓
      - Total edges: 2 (excluding rdf:type)
      - Resolution: N/A (already connected)
      - Result: PASS (connected)
    - Entity: "OnlineChatSession" (urn:uuid:xxx...)
      - Outgoing: hasParticipant → Suspect, involves → HypnosisScript
      - Incoming: none yet (will link from investigation)
      - Total edges: 2 (excluding rdf:type)
      - Resolution: N/A (already connected)
      - Result: PASS (connected)
```

### Phase 1 Deliverables (Must Output)

1. **Concept Inventory Table** with columns:
   - Concept
   - Category (Entity / Action / Evidence / Legal / Location / Org / Other)
   - Source snippet (quote or paraphrase)
   - Evidence pointer (documentId + location)
   - Confidence (high/medium/low)
   - Proposed modeling approach (reuse / extend / new)

2. **Mapping Table** with columns:
   - Document concept → Existing term OR Proposed new term (namespace + local name)
   - Facets required
   - Rationale

3. **Change List by File** (exact file paths) with "why here?" justification.

4. **Batch Mapping Manifest** (for batch mode, YAML/JSON):

```yaml
documentId: "urn:uuid:..."
concepts:
  - conceptName: "..."
    instanceUUID: "urn:uuid:..."
    class: "cacontology:ClassName"
    facets:
      - "observable:FileFacet"
    relationships:
      - predicate: "cacontology:relatesTo"
        targetUUID: "urn:uuid:..."
    evidencePointer:
      documentId: "urn:uuid:..."
      span: "lines 42-45"
      quote: "..."
    confidence: "high"
```

---

## Phase 2: Implementation Plan

Write a concrete implementation plan with:

- New/updated classes (with `rdfs:subClassOf`)
- New/updated datatype properties (domain/range)
- New/updated object properties (domain/range)
- SHACL shapes to add/update (targets, required properties, enums)
- Example knowledge graph scope (which instances demonstrate which new terms)
- SPARQL query scope (titles + what each answers)

### Phase 2 Reasoning Procedure (Schema-Driven CoT)

For each proposed new term, follow this reasoning chain to ensure ontology consistency:

1. **Reference ontology schemas**: Load and review CAC/UCO/CASE/gUFO class hierarchies before proposing

2. **Duck Typing Check (UCO/CASE Pattern)**: 
   UCO/CASE uses "duck typing": if an object can have a facet attached, use facets instead of subclasses.
   
   - Ask: "Can this concept be represented by attaching facets to an existing class?"
   - **Duck typing principle**: An object's behavior is defined by its facets, not just its class
   
   **Duck Typing Decision Tree**:
   ```
   Is this concept a perspective/view/interpretation of an existing object?
   ├── YES → Use existing class + facet (STOP - do not create subclass)
   │         Examples:
   │         - File that's evidence: uco-observable:ObservableObject + investigation:ExhibitFacet
   │         - Person as suspect: uco-identity:Person + role assignment (not Suspect subclass)
   │         - Image with analysis: uco-observable:ObservableObject + observable:ContentDataFacet
   │
   └── NO → Does this concept have intrinsic identity properties beyond perspectives?
       ├── YES → Consider subclass (proceed to step 3)
       │         Examples:
       │         - GroomingScript is a KIND of artifact, not just a view
       │         - InvestigativeAction is fundamentally different from generic Action
       │
       └── NO → Use existing class + custom facet (STOP)
   ```
   
   - If YES to duck typing: Document "Duck typing applied: [existing class] + [facet(s)]"
   - If NO: Document why facets are insufficient before proposing subclass

3. **Subclass only if needed**: Propose `rdfs:subClassOf` only if:
   - The concept has intrinsic properties not capturable by facets
   - It represents a true ontological specialization (not just a view/perspective)
4. **Verify equivalence claims**: If proposing `owl:equivalentClass` or `owl:equivalentProperty`:
   - Run SPARQL inference check to verify logical equivalence
   - Document the entailment proof
   - Default to `skos:exactMatch` if equivalence is semantic but not strictly logical
5. **gUFO alignment**: Map each new class to a gUFO foundational concept:
   - `gufo:Object` - independent endurants (persons, organizations, physical items)
   - `gufo:Event` - occurrences in time (actions, incidents, processes)
   - `gufo:Relator` - reified relationships (contracts, memberships, marriages)
   - `gufo:Quality` - measurable aspects (weight, age, duration)
   - `gufo:Role` - anti-rigid sortals (Victim, Offender, Investigator)
   - `gufo:Phase` - intrinsic contingent types (Child, Deceased, Active)
6. **Semantic drift check**: Compare proposed term to existing CAC terms:
   - If similarity > 80%: FLAG as potential duplicate, justify why new term is needed
   - If similarity < 40%: FLAG as potential scope drift, verify in-scope
   - Document decision: "New term approved because: [rationale]"

7. **Minimum-link obligations (Connectivity by Design)**:
   For each proposed class/instance, verify it will have at least one grounded relationship:
   
   - **Required link types** (at least one must apply):
     - `uco-core:hasFacet` → attaches perspective/metadata
     - `uco-action:object` → links to an action (collection, listing, derivation)
     - `uco-action:result` → product of an action
     - `investigation:provenanceRecordAction` → provenance chain
   
   - **Document minimum connectivity plan**:
     ```
     Instance: ex:new-entity-uuid
     Class: uco-identity:Organization
     Minimum links:
       - uco-action:object ← ex:listing-action-uuid (grounded: "webpage lists affiliates")
     Connectivity: PASS (degree ≥ 1 guaranteed)
     ```
   
   - If no minimum link can be identified at design time: **FLAG as potential isolate risk**

**Example Schema-Driven CoT**:
```
Proposed Term: cacontology-tradecraft:GroomingScript

1. Reference: Checked CAC tradecraft module, UCO observable, CASE investigation

2. Duck Typing Check:
   - Q: "Is this a perspective/view of an existing object?"
   - Analysis: GroomingScript is not just a "view" of a generic file
   - It has intrinsic behavioral semantics: scripts designed for grooming
   - A ContentDataFacet only describes content metadata, not behavioral purpose
   - Decision: Duck typing NOT sufficient - this is a KIND of artifact
   - Document: "Duck typing insufficient: GroomingScript has intrinsic identity 
     properties (behavioral purpose, grooming-specific structure) beyond file metadata"

3. Subclass: Propose subclass of cacontology-tradecraft:OffenderArtifact
   → YES: Represents a specific category of tradecraft evidence with unique properties
   → Rationale: Intrinsic properties (grooming intent, script structure) justify subclass

4. Equivalence: No owl:equivalentClass claims

5. gUFO alignment: gufo:Object (an artifact that exists independently)

6. Drift check: 
   - Similarity to "HypnosisScript": 75% → Different behavioral purpose, approved
   - Similarity to "ChatLog": 35% → Different nature (script vs log), approved
   → Decision: "New term approved: distinct tradecraft artifact type"

COUNTER-EXAMPLE (where duck typing IS appropriate):

Proposed Term: cacontology:AnalyzedImage

1. Reference: Checked CAC, UCO observable

2. Duck Typing Check:
   - Q: "Is this a perspective/view of an existing object?"
   - Analysis: "AnalyzedImage" is just an image WITH analysis attached
   - The analysis is a perspective/view, not an intrinsic property of the image
   - Decision: Duck typing IS sufficient
   - Document: "Duck typing applied: uco-observable:ObservableObject + 
     observable:ContentDataFacet + cacontology:AnalysisFacet"

→ Do NOT create AnalyzedImage subclass - use facets instead
```

### Term Citation & Mapping Ledger (Required)

For every proposed new/updated CAC term:

| CAC Term (fully-qualified) | dcterms:source Citation | rdfs:seeAlso URL | External Alignment (skos:exactMatch/closeMatch) | gUFO Alignment | Explainability Note |
|----------------------------|-------------------------|------------------|--------------------------------------------------|----------------|---------------------|
| `cacontology:NewClass`     | "Source document..."    | `https://...`    | `skos:closeMatch external:Term`                  | `gufo:Event`   | "Enables pattern X" |

**gUFO Alignment options** (select the most appropriate):
- `gufo:Object` - Independent endurants (persons, organizations, physical evidence)
- `gufo:Event` - Occurrences (actions, incidents, processes, operations)
- `gufo:Relator` - Reified relationships (contracts, memberships, authorizations)
- `gufo:Quality` - Measurable aspects (durations, counts, scores)
- `gufo:Role` - Anti-rigid sortals (Victim, Offender, Investigator, Witness)
- `gufo:Phase` - Intrinsic contingent types (Minor, Deceased, Active, Pending)
- `gufo:Kind` - Rigid sortals providing identity (Person, Organization, Device)
- `gufo:Category` - Rigid non-sortals (PhysicalObject, DigitalArtifact)

### Governance Gate (Pre-Phase 3)

Produce a **REVIEW REQUIRED** queue:

- New terms pending approval
- SKOS mappings pending approval
- Sensitive entities/claims pending approval

Define **approved vs deferred** items before edits proceed. In automated pipelines, this gate may be a checkpoint requiring human sign-off.

### Ontology Drift Check (Pre-Phase 3)

Before approving new terms, run an automated drift check:

1. **Duplicate detection**: Compute semantic similarity to existing CAC terms (via embeddings or label matching)
   - If similarity **> 80%** to existing term: **FLAG as potential duplicate**
   - Action: Justify why new term is needed despite high similarity
   
2. **Scope drift detection**: Check alignment with CAC scope
   - If similarity **< 40%** to any existing CAC term: **FLAG as potential scope drift**
   - Action: Verify the concept is truly in-scope for CSEA/investigations domain
   
3. **gUFO alignment verification**: Confirm proposed gUFO alignment is appropriate
   - Cross-check with gUFO documentation
   - Ensure no category errors (e.g., modeling an event as an object)

4. **Document decision** for each flagged term:
   ```
   Term: cacontology:ProposedTerm
   Drift Check Result: [DUPLICATE_FLAG | SCOPE_FLAG | CLEAR]
   Decision: [APPROVED | DEFERRED | REJECTED]
   Rationale: "Approved because: [specific justification]"
   ```

**Drift Check SPARQL** (run against existing ontology):
```sparql
# Find existing terms with similar labels
SELECT ?existing ?label WHERE {
  ?existing rdfs:label ?label .
  FILTER(CONTAINS(LCASE(?label), LCASE("<proposed_term_label>")))
}
```

### Phase 2 Deliverables (Must Output)

- A bullet list of **exact new/updated terms** (fully-qualified)
- **Term Citation & Mapping Ledger** (as above)
- A checklist of file edits (each item: file → change summary)
- A **risk list** (top 3-4 ways validation might fail and how you'll prevent it):
  1. **SHACL shape violations**: missing required properties, wrong datatypes
  2. **Domain/range violations**: relationships used incorrectly
  3. **Connectivity risk**: isolated nodes or low-degree entities
     - Mitigation: Verify minimum-link obligations (step 7) for every new instance
  4. **Provenance gaps**: missing evidence pointers or confidence levels
- **Governance Gate queue** with approval status

---

## Phase 3: Ontology + Shapes Implementation

Implement changes in `ontology/*.ttl` and `ontology/*-shapes.ttl` as planned.

### Implementation Rules

- Every new class/property MUST have `rdfs:label` and `rdfs:comment`.
- Every new class/property MUST have `dcterms:source` (citation).
- Every new class/property SHOULD have `rdfs:seeAlso` (URL) when available.
- Every new class/property MUST have SKOS mappings when aligned to external terms.
- Every new property MUST have `rdfs:domain` and `rdfs:range` (unless there's an explicit reason not to—document it).
- Avoid over-fitting the ontology to a single case; keep terms reusable.
- If you relocate classes between modules, update imports/cross-references and ensure shapes still target the right class IRIs.

### Phase 3 Deliverables (Must Output)

- A summary list of what was added/changed per file.
- A list of which files had **classes/properties changed** (candidates for `dcterms:modified` update).
- **Term citation coverage**: confirm 100% of new/updated terms have `dcterms:source`.

### Post-Phase 3 QA Gate

Run verification and report:

- SHACL validation (preliminary)
- Metrics: # new terms, # updated terms, shapes coverage
- Term citation coverage (% with dcterms:source)
- SKOS mapping coverage (% with mappings where applicable)

---

## Phase 4: Example Knowledge Graph (KG)

Create `examples_knowledge_graphs/[caseId]-example.ttl` that demonstrates:

- Key entities, actions, evidence, and legal concepts in the document
- Every new/updated class/property added in Phase 3
- SHACL compliance **without reasoning**

### KG Rules (Critical)

- **UUID-only instances**: All instance IRIs MUST be `urn:uuid:<uuid>` format.
- Add explicit parent `rdf:type` triples when needed to satisfy SHACL (no reliance on subclass inference).
- Include `rdfs:label` and `rdfs:comment` on major instances.
- **Facet coverage**: Demonstrate facet usage for ObservableObjects.
- **Provenance chain**: Include collection action + provenance record for the source document.
- **Evidence pointers**: Represent evidence pointers for key claims (at least for major assertions).

### Phase 4 Deliverables (Must Output)

- A short "KG coverage map": which instance demonstrates which new term(s).
- **UUID coverage confirmation**: 100% of instances use `urn:uuid:` IRIs.
- **Facet coverage report**: which ObservableObjects have facets attached.
- **Provenance chain confirmation**: document collection is represented.

### Post-Phase 4 QA Gate

Verify and report:

- UUID coverage = 100%
- Facet coverage metrics
- Provenance completeness metrics
- Evidence pointer coverage for key assertions
- 0 out-of-scope entities modeled as domain triples
- Privacy rules met (no disallowed PII fields)

---

## Phase 5: SPARQL Queries

Create `example_SPARQL_queries/[caseId]-analytics.rq` with **10–15** investigator-focused queries.

### Query Rules

- Each query MUST include the required prefixes in the query text.
- Each query MUST be runnable against the example KG (no external inference required).
- Add a comment header before each query: purpose + what it returns.
- **All queries must be explainable**: results should link back to evidence/provenance when relevant.

### Recommended Query Topics

**Standard Topics:**

- Timeline of actions/events
- Undercover communications patterns
- Evidence/provenance/collection actions
- Authorization audit (consent/warrant linkage)
- Charges summary by statute/jurisdiction
- Location/meeting arrangement analysis
- Cross-evidence corroboration

**Strategic Analytics (Tradecraft + Patterns):**

- Recurring offender tradecraft patterns
- LE investigative/operational sequences
- Legal process workflows
- Cross-case pattern queries (for batch mode)

---

## Phase 6: SHACL Validation + Verification Suite

### Primary Validation Path (Docker-first)

- Follow `testing/DOCKER_README.md`
- Run from `testing/`:

```bash
docker compose down
docker compose up --build --abort-on-container-exit
```

### Fallback Path (CLI)

If Docker isn't available, use pySHACL CLI:

```bash
pyshacl -s ontology/<shapes-file>.ttl -d examples_knowledge_graphs/[caseId]-example.ttl -f human
```

### SPARQL Verification Suite (Required)

Run the following sanity checks and report results:

```sparql
# 1. Provenance Completeness Check
# Verify all collection actions have required UCO properties
SELECT ?action WHERE {
  ?action a investigation:InvestigativeAction .
  FILTER NOT EXISTS { ?action uco-action:startTime ?time }
}
# Expected: 0 results

# 1b. Hash Completeness Check  
# Verify all documents have hash facets with method and value
SELECT ?doc WHERE {
  ?doc a uco-observable:ObservableObject .
  FILTER NOT EXISTS {
    ?doc uco-core:hasFacet ?hashFacet .
    ?hashFacet a observable:HashFacet .
    ?hashFacet observable:hash ?hash .
    ?hash types:hashMethod ?method ;
          types:hashValue ?value .
  }
}
# Expected: 0 results

# 2. Facet Integrity Check  
# Verify all hasFacet links point to typed nodes
SELECT ?obj ?facet WHERE {
  ?obj uco-core:hasFacet ?facet .
  FILTER NOT EXISTS { ?facet a ?type }
}
# Expected: 0 results

# 3. UUID Coverage Check
# Find any instance IRIs not using urn:uuid: scheme
SELECT ?s WHERE {
  ?s ?p ?o .
  FILTER(isIRI(?s) && !STRSTARTS(STR(?s), "urn:uuid:") && !STRSTARTS(STR(?s), "http"))
}
# Expected: Only ontology terms, no instance IRIs

# 4. Typed Node Coverage
# Find untyped nodes (excluding blank nodes and literals)
SELECT ?node WHERE {
  { ?node ?p ?o } UNION { ?s ?p ?node }
  FILTER(isIRI(?node) && STRSTARTS(STR(?node), "urn:uuid:"))
  FILTER NOT EXISTS { ?node a ?type }
}
# Expected: 0 results

# 5. Facet Subclass Integrity
# Verify all hasFacet links point to proper Facet subclasses
SELECT ?obj ?facet ?facetType WHERE {
  ?obj uco-core:hasFacet ?facet .
  ?facet a ?facetType .
  FILTER NOT EXISTS { ?facetType rdfs:subClassOf* uco-core:Facet }
}
# Expected: 0 results (all facets must be subclasses of uco-core:Facet)

# 6. Relationship Domain Verification
# Find relationships where subject doesn't match declared domain
SELECT ?s ?rel ?o ?declaredDomain WHERE {
  ?s ?rel ?o .
  ?rel rdfs:domain ?declaredDomain .
  FILTER NOT EXISTS { ?s a/rdfs:subClassOf* ?declaredDomain }
  FILTER(?rel != rdf:type)
}
# Expected: 0 results (all relationships respect declared domains)

# 7. Relationship Range Verification
# Find relationships where object doesn't match declared range
SELECT ?s ?rel ?o ?declaredRange WHERE {
  ?s ?rel ?o .
  ?rel rdfs:range ?declaredRange .
  FILTER(isIRI(?o))
  FILTER NOT EXISTS { ?o a/rdfs:subClassOf* ?declaredRange }
  FILTER(?rel != rdf:type)
}
# Expected: 0 results (all relationships respect declared ranges)

# 8. Confidence Coverage Check
# Find assertions/extractions without confidence levels
SELECT ?assertion WHERE {
  ?assertion a ?type .
  FILTER(?type IN (cacontology:ExtractedAssertion, cacontology:ClaimFromDocument))
  FILTER NOT EXISTS { 
    ?assertion uco-core:hasFacet ?cf . 
    ?cf a uco-core:ConfidenceFacet .
  }
  FILTER NOT EXISTS {
    ?assertion cacontology:confidence ?conf .
  }
}
# Expected: 0 results (all assertions must have confidence)

# 9. Evidence Pointer Coverage
# Find key assertions without evidence pointers
SELECT ?assertion WHERE {
  ?assertion a ?type .
  FILTER(?type IN (cacontology:ExtractedAssertion, cacontology:ClaimFromDocument))
  FILTER NOT EXISTS { ?assertion cacontology:hasEvidencePointer ?ep }
}
# Expected: 0 results for key assertions

# 10. Deconfliction Verification (Batch Mode)
# Find potential duplicate entities that weren't addressed
SELECT ?ent1 ?ent2 ?label WHERE {
  ?ent1 rdfs:label ?label .
  ?ent2 rdfs:label ?label .
  FILTER(?ent1 != ?ent2)
  FILTER NOT EXISTS { ?ent1 owl:sameAs ?ent2 }
  FILTER NOT EXISTS { ?ent2 owl:sameAs ?ent1 }
  FILTER NOT EXISTS { 
    ?decision a investigation:ProvenanceRecord ;
              uco-core:description ?desc .
    FILTER(CONTAINS(?desc, "Deconfliction"))
  }
}
# Expected: 0 unaddressed potential duplicates

# 11. Isolated Node Detection (CRITICAL FAIL - MUST BE 0)
# Find nodes with zero connections (no incoming or outgoing edges excluding rdf:type)
SELECT ?node ?type WHERE {
  ?node a ?type .
  FILTER(STRSTARTS(STR(?node), "urn:uuid:"))
  FILTER NOT EXISTS { ?node ?anyPred ?anyObj . FILTER(?anyPred != rdf:type) }
  FILTER NOT EXISTS { ?anySubj ?anyPred ?node . FILTER(?anyPred != rdf:type) }
}
# Expected: 0 results (MANDATORY - any result is a validation failure)
# Action: If results found, trigger REMEDIATION LOOP (see below)
# NEVER patch-connect by inventing relationships; either ground or remove

# 12. Low-Degree Node Detection (WARNING - REVIEW REQUIRED)
# Find nodes with only one non-type connection (degree = 1, weakly grounded)
SELECT ?node ?type (COUNT(*) as ?degree) WHERE {
  ?node a ?type .
  FILTER(STRSTARTS(STR(?node), "urn:uuid:"))
  {
    { ?node ?p ?o . FILTER(?p != rdf:type) } 
    UNION 
    { ?s ?p ?node . FILTER(?p != rdf:type) }
  }
}
GROUP BY ?node ?type
HAVING (COUNT(*) = 1)
# Expected: <10% of total nodes (target for well-grounded KGs)
# Review: Can additional grounded relationships be found? Is single edge sufficient?
# Action: Flag for human review, document justification if kept as degree=1

# 13. Relationship Evidence Check
# Find edges between instances without provenance or confidence
SELECT ?s ?p ?o WHERE {
  ?s ?p ?o .
  FILTER(STRSTARTS(STR(?s), "urn:uuid:"))
  FILTER(STRSTARTS(STR(?o), "urn:uuid:"))
  FILTER(?p NOT IN (rdf:type, uco-core:hasFacet, owl:sameAs))
  FILTER NOT EXISTS { ?s cacontology:hasEvidencePointer ?ep }
  FILTER NOT EXISTS { ?s cacontology:confidence ?conf }
}
# Expected: Minimal ungrounded relationships (review any found)

# 14. Duck Typing Verification
# Find UcoObjects that might benefit from facet-based modeling
SELECT ?obj ?type WHERE {
  ?obj a ?type .
  ?type rdfs:subClassOf+ uco-core:UcoObject .
  FILTER(STRSTARTS(STR(?obj), "urn:uuid:"))
  FILTER NOT EXISTS { ?obj uco-core:hasFacet ?anyFacet }
}
# Review: Objects without facets may indicate over-subclassing
# Not all objects need facets, but review for missed perspectives

# 15. Rigid Typing Check
# Find potential over-subclassing (single-purpose subclasses with few instances)
SELECT ?subclass (COUNT(?instance) as ?count) WHERE {
  ?subclass rdfs:subClassOf ?parent .
  FILTER(STRSTARTS(STR(?subclass), "https://cacontology"))
  OPTIONAL { ?instance a ?subclass }
}
GROUP BY ?subclass
HAVING (COUNT(?instance) < 3)
# Flag: Subclasses with <3 instances may indicate facet is more appropriate
# Review and consider refactoring to facet-based approach
```

### Connectivity Remediation Loop (When Check 11 Fails)

If isolated nodes are detected, execute this remediation procedure:

1. **Identify the isolated node** from check 11 results
2. **Locate the source span** that led to extraction (from Phase 1 evidence pointer)
3. **Re-run Phase 1 CoT** on that specific span with focus on relationships:
   - Look for explicit relationships in text (preferred)
   - Apply provenance-anchoring pattern if no explicit relationship exists
4. **Resolution decision**:
   - **GROUNDED**: Found a text-supported relationship → add edge with evidence pointer
   - **ANCHORED**: Applied provenance-anchoring pattern → add statement/listing action linking to source
   - **REMOVED**: No grounding possible → remove the node entirely
   - **FLAGGED**: Concept seems important but cannot be grounded → mark REVIEW REQUIRED for human
5. **Document the resolution** in the run report:
   ```
   Isolated node: ex:uuid-of-isolated-node
   Label: "Entity Name"
   Source span: normalized.txt lines X-Y
   Resolution: [GROUNDED|ANCHORED|REMOVED|FLAGGED]
   Action taken: [description of fix or removal]
   ```
6. **Re-run check 11** to verify 0 isolated nodes

**NEVER**: Invent relationships to satisfy connectivity. "Patch-connecting" is hallucination.

### Tooling Options for Verification

**Option 1: SPARQL-first** (when triplestore available):
- Load KG into GraphDB, Fuseki, or similar
- Execute verification suite queries directly
- Preferred for batch mode and production pipelines

**Option 2: Local rdflib** (Python fallback):
```python
from rdflib import Graph
from pyshacl import validate

# Load and validate
g = Graph()
g.parse("examples_knowledge_graphs/[caseId]-example.ttl", format="turtle")

# Run SPARQL checks
isolated_nodes = g.query("""
    SELECT ?node ?type WHERE {
      ?node a ?type .
      FILTER(STRSTARTS(STR(?node), "urn:uuid:"))
      FILTER NOT EXISTS { ?node ?anyPred ?anyObj . FILTER(?anyPred != rdf:type) }
      FILTER NOT EXISTS { ?anySubj ?anyPred ?node . FILTER(?anyPred != rdf:type) }
    }
""")
assert len(list(isolated_nodes)) == 0, "Isolated nodes detected!"
```

**Option 3: String-based approximation** (last resort, clearly approximate):
- Parse Turtle as text to extract UUID subjects/objects
- Count occurrences to estimate degrees
- Use only when RDF tools unavailable; label results as "approximate"

### Phase 6 Deliverables (Must Output)

- A pass/fail matrix: shapes file → conforms? (yes/no)
- SPARQL verification suite results (all 15 checks with pass/fail/review status)
- If failures occurred: list the fixes made and re-run results
- **Remediation loop results** (if check 11 failed): isolated nodes and their resolutions

**Metrics summary** (with pass/fail thresholds):

| Check | Metric | Target | Status |
|-------|--------|--------|--------|
| 1, 1b | Provenance completeness | 100% | PASS/FAIL |
| 2, 5 | Facet integrity | 100% | PASS/FAIL |
| 3 | UUID coverage | 100% | PASS/FAIL |
| 4 | Typed node coverage | 100% | PASS/FAIL |
| 6, 7 | Domain/range compliance | 100% | PASS/FAIL |
| 8 | Confidence coverage | 100% | PASS/FAIL |
| 9 | Evidence pointer coverage | 100% | PASS/FAIL |
| 10 | Deconfliction completeness | 100% (batch) | PASS/FAIL |
| **11** | **Graph connectivity (isolates)** | **0 nodes** | **CRITICAL** |
| 12 | Low-degree nodes | <10% | REVIEW |
| 13 | Edge grounding | 100% | PASS/FAIL |
| 14 | Facet utilization | >50% | REVIEW |
| 15 | Duck typing compliance | >80% | REVIEW |

**Critical failures** (block release):
- Check 11: Any isolated node = FAIL (run remediation loop)
- Checks 1-9: Any non-100% = FAIL

**Review items** (document but don't block):
- Check 12: Low-degree nodes >10% = document justification
- Check 14-15: Review for modeling improvements

---

## Phase 7: Versioning + Release + PR

### Versioning Rules

- Choose a new version using semver:
  - **MINOR** for new classes/properties/features (most cases)
  - **PATCH** for fixes only
  - **MAJOR** only for breaking changes
- Update `CHANGELOG.md` with:
  - Summary
  - New/changed terms
  - New example KG + queries
  - How validated (SHACL)
  - **Term citation coverage metrics**

### `dcterms:modified` Rule (Important)

- Update `dcterms:modified` ONLY in files where **classes/properties were added or updated**.
- Do NOT update `dcterms:modified` for:
  - version string replacement only
  - whitespace/formatting only
  - comment-only changes

### Git/PR Workflow Rules

- Create branch: `release/vX.Y.Z-[caseId]`
- Commit message MUST include:
  - What changed (terms + files)
  - Why (document-driven)
  - How validated (SHACL commands/results)
- Avoid force-push. If you must amend after pushing, use `--force-with-lease`.

---

## Phase 8: KG Export + Triplestore Load + Verification

**Purpose**: Push the validated KG to the target triplestore and run post-load verification.

### Export

- Produce **per-document TTL** files (one per documentId).
- Optionally produce a **merged dataset** (combined TTL or named graph dataset).
- Use **named graphs** keyed by `documentId` or `batchId`:
  - Graph name: `urn:uuid:<documentId>` or `urn:uuid:<batchId>`

### Load (SPARQL Endpoint)

Provide instructions for loading to RDF triplestore:

```bash
# Example for GraphDB
curl -X POST \
  -H "Content-Type: application/x-turtle" \
  --data-binary @examples_knowledge_graphs/[caseId]-example.ttl \
  "http://localhost:7200/repositories/cac-ontology/statements?context=urn:uuid:<documentId>"

# Example for Apache Fuseki
curl -X POST \
  -H "Content-Type: text/turtle" \
  --data-binary @examples_knowledge_graphs/[caseId]-example.ttl \
  "http://localhost:3030/cac-ontology/data?graph=urn:uuid:<documentId>"
```

### Post-Load Verification

Run the SPARQL verification suite against the loaded data:

1. **UUID uniqueness and joinability** - confirm cross-document links resolve
2. **Provenance completeness** - all documents have full provenance
3. **Evidence coverage** - key assertions have evidence pointers
4. **Confidence coverage** - extracted assertions have confidence levels
5. **Out-of-scope exclusion** - no out-of-scope domain triples present

### Indexing Recommendations

Recommend indexing/optimizing around:

- UUID IRIs (primary join key)
- `uco-core:hasFacet` predicate
- `investigation:ProvenanceRecord` links
- `investigation:InvestigativeAction` timestamps

### Phase 8 Deliverables (Must Output)

- **Export file list**: paths to produced TTL files
- **Load commands**: exact commands used (or to be used)
- **Post-load verification results**: all checks pass/fail
- **Named graph convention used**: document the graph naming strategy

---

## Final Output Requirements (Must Include)

1. **Phase -1 outputs**: Batch manifest, scope decisions, skeleton TTLs, provenance report
2. Concept Inventory Table + Mapping Table (with evidence pointers + confidence)
3. **Term Citation & Mapping Ledger**
4. Exact list of new/updated terms (fully-qualified)
5. File-by-file change summary
6. SHACL validation summary (Docker-first), including failures and fixes if any
7. **SPARQL verification suite results**
8. **Metrics summary**: UUID coverage, provenance completeness, facet coverage, term citation coverage
9. Version decision + `dcterms:modified` updates list (which files, what date)
10. Branch name + commit hash + PR link
11. **Phase 8 outputs**: Export files, load commands, post-load verification

---

## Example Patterns (Reference Only)

### New Class with Term Citation + SKOS Mapping

```turtle
cacontology-undercover:SiblingPersonaOperation rdf:type owl:Class ;
    rdfs:label "Sibling Persona Operation"@en ;
    rdfs:comment "Undercover operation where personas are presented as siblings to engage with suspects."@en ;
    rdfs:subClassOf cacontology-undercover:MultiplePersonaOperation ;
    dcterms:source "DOJ ICAC Task Force Operations Manual, Section 4.2" ;
    rdfs:seeAlso <https://www.justice.gov/criminal-ceos/icac-task-force> ;
    skos:closeMatch <https://ontology.caseontology.org/case/investigation/UndercoverAction> .
```

### New Datatype Property with Citation

```turtle
cacontology-undercover:ageStatedToSuspect rdf:type owl:DatatypeProperty ;
    rdfs:label "Age Stated to Suspect"@en ;
    rdfs:comment "The age that was stated to the suspect during the undercover operation."@en ;
    rdfs:domain cacontology-undercover:AgeAcknowledgment ;
    rdfs:range xsd:nonNegativeInteger ;
    dcterms:source "ICAC Undercover Chat Protocol Guidelines" .
```

### UUID Instance with Provenance Chain + Facets

```turtle
@prefix ex: <urn:uuid:> .

# Source document (collected press release)
ex:a1b2c3d4-5678-90ab-cdef-111111111111 a uco-observable:ObservableObject ;
    rdfs:label "DOJ Press Release - Case 2024-1234" ;
    uco-core:id "urn:uuid:a1b2c3d4-5678-90ab-cdef-111111111111"^^types:Identifier ;
    uco-core:hasFacet ex:a1b2c3d4-5678-90ab-cdef-222222222222 ;  # ContentDataFacet
    uco-core:hasFacet ex:a1b2c3d4-5678-90ab-cdef-333333333333 ;  # AnalysisFacet
    uco-core:hasFacet ex:a1b2c3d4-5678-90ab-cdef-777777777777 ;  # URLFacet (source)
    uco-core:hasFacet ex:a1b2c3d4-5678-90ab-cdef-888888888888 .  # HashFacet

# Content metadata facet
ex:a1b2c3d4-5678-90ab-cdef-222222222222 a observable:ContentDataFacet ;
    observable:mimeType "text/html" ;
    observable:sizeInBytes 15234 .

# Collection analysis facet (agent perspective)
ex:a1b2c3d4-5678-90ab-cdef-333333333333 a observable:AnalysisFacet ;
    rdfs:comment "Extracted by CAC Ontology Agent on 2024-01-15" .

# Collection action
ex:a1b2c3d4-5678-90ab-cdef-444444444444 a investigation:InvestigativeAction ;
    rdfs:label "Document Collection Action" ;
    uco-action:startTime "2024-01-15T10:30:00Z"^^xsd:dateTime ;
    uco-action:object ex:a1b2c3d4-5678-90ab-cdef-111111111111 ;
    uco-action:performer ex:a1b2c3d4-5678-90ab-cdef-555555555555 .

# Collector agent (could be uco-identity:Identity for people, or uco-tool:Tool for automated systems)
ex:a1b2c3d4-5678-90ab-cdef-555555555555 a uco-core:UcoObject ;
    rdfs:label "CAC Ontology Automation Agent" ;
    uco-core:description "Automated document collection and KG generation system" .

# Provenance record linking to collection action and source
ex:a1b2c3d4-5678-90ab-cdef-666666666666 a investigation:ProvenanceRecord ;
    rdfs:label "Provenance for Press Release Collection" ;
    investigation:exhibitNumber "DOC-2024-001" ;
    uco-core:object ex:a1b2c3d4-5678-90ab-cdef-111111111111 ;  # The collected document
    investigation:provenanceRecordAction ex:a1b2c3d4-5678-90ab-cdef-444444444444 .  # The collection action

# URL source facet (attached to document via uco-core:hasFacet)
ex:a1b2c3d4-5678-90ab-cdef-777777777777 a observable:URLFacet ;
    observable:url <https://www.justice.gov/usao/pr/example-2024> .

# Hash facet (attached to document via uco-core:hasFacet)  
ex:a1b2c3d4-5678-90ab-cdef-888888888888 a observable:HashFacet ;
    observable:hash ex:a1b2c3d4-5678-90ab-cdef-999999999999 .

ex:a1b2c3d4-5678-90ab-cdef-999999999999 a types:Hash ;
    types:hashMethod "SHA-256" ;
    types:hashValue "abc123def456..." .
```

### New SHACL Shape

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

---

## Few-Shot Examples for LLM Guidance

Use these worked examples to guide consistent extraction and modeling decisions.

### Example 1: Extracting an Offender Action with Full Reasoning Chain

**Source text**: "The defendant initiated contact with the minor through Instagram, sending messages that became increasingly sexual in nature over a period of three weeks."

**Chain-of-Thought Extraction**:

```
1. PARSE: 
   - Entity: "defendant" (person, offender role)
   - Entity: "minor" (person, victim role)
   - Action: "initiated contact" (grooming behavior)
   - Platform: "Instagram" (digital medium)
   - Pattern: "increasingly sexual messages" (escalation)
   - Duration: "three weeks" (temporal)

2. EXTRACT:
   - Concept: OnlineGroomingAction (Category: Action)
   - Concept: Defendant (Category: Entity/Role)
   - Concept: MinorVictim (Category: Entity/Role)
   - Concept: InstagramPlatform (Category: Evidence)

3. SEARCH:
   - cacontology-tradecraft:OnlineGrooming ✓ EXISTS
   - cacontology:Defendant ✓ EXISTS
   - cacontology:MinorVictim ✓ EXISTS
   - uco-observable:Application → for Instagram

4. MAP:
   - OnlineGroomingAction → REUSE: cacontology-tradecraft:OnlineGrooming
   - Defendant → REUSE: cacontology:Defendant
   - MinorVictim → REUSE: cacontology:MinorVictim
   - InstagramPlatform → REUSE: uco-observable:Application + observable:ApplicationFacet

5. UUID:
   - Grooming action: urn:uuid:a1b2c3d4-1111-2222-3333-444444444444
   - Defendant: urn:uuid:a1b2c3d4-5555-6666-7777-888888888888
   - Victim: urn:uuid:a1b2c3d4-9999-aaaa-bbbb-cccccccccccc

6. FACETS:
   - GroomingAction: cacontology:EscalationFacet (pattern: "increasingly sexual")
   - GroomingAction: uco-action:ActionArgumentFacet (duration: "3 weeks")

7. RELATIONSHIPS:
   - cacontology:hasPerformer (GroomingAction → Defendant) 
   - cacontology:hasVictim (GroomingAction → MinorVictim)
   - uco-action:instrument (GroomingAction → InstagramApp)

8. VERIFY:
   - hasPerformer domain=Action, range=Person ✓
   - hasVictim domain=Action, range=Person ✓

9. CONFIDENCE: HIGH
   - Direct quote from legal document
   - Clear action, actors, and timeline

10. EVIDENCE:
    - documentId: urn:uuid:doc-press-release-123
    - span: "paragraph 3, sentence 1"
    - quote: "initiated contact with the minor through Instagram..."
```

**Resulting Turtle**:

```turtle
ex:a1b2c3d4-1111-2222-3333-444444444444 a cacontology-tradecraft:OnlineGrooming ;
    rdfs:label "Instagram Grooming - Defendant to Minor" ;
    cacontology:hasPerformer ex:a1b2c3d4-5555-6666-7777-888888888888 ;
    cacontology:hasVictim ex:a1b2c3d4-9999-aaaa-bbbb-cccccccccccc ;
    uco-action:instrument ex:instagram-app-uuid ;
    uco-core:hasFacet ex:escalation-facet-uuid ;
    cacontology:confidence "high" ;
    cacontology:hasEvidencePointer ex:evidence-pointer-uuid .
```

---

### Example 2: Modeling Digital Evidence with Multiple Facets

**Source text**: "Forensic analysis of the seized laptop revealed 847 images of child sexual abuse material. The images were found in a hidden folder and had been downloaded between January and March 2024."

**Chain-of-Thought Extraction**:

```
1. PARSE:
   - Evidence: "seized laptop" (physical device)
   - Evidence: "847 images" (CSAM)
   - Location: "hidden folder" (storage location)
   - Timeframe: "January-March 2024" (acquisition period)
   - Action: "forensic analysis" (investigative action)

2. EXTRACT:
   - Concept: SeizedLaptop (Category: Evidence/Physical)
   - Concept: CSAMImageCollection (Category: Evidence/Digital)
   - Concept: ForensicAnalysis (Category: Action/Investigative)

3. SEARCH:
   - uco-observable:Device ✓ for laptop
   - cacontology-evidence:CSAMEvidence ✓ for images
   - investigation:ForensicAction ✓ for analysis

4. MAP:
   - SeizedLaptop → REUSE: uco-observable:Device
   - CSAMImageCollection → REUSE: cacontology-evidence:CSAMCollection
   - ForensicAnalysis → REUSE: investigation:ForensicAction

5. UUID:
   - Laptop: urn:uuid:device-laptop-12345
   - CSAM collection: urn:uuid:csam-collection-67890
   - Analysis action: urn:uuid:forensic-action-abcde

6. FACETS (Multiple perspectives):
   - Laptop:
     - observable:DeviceFacet (type: laptop, seized: true)
     - observable:OperatingSystemFacet (if known)
   - CSAM Collection:
     - observable:ContentDataFacet (count: 847, type: image)
     - cacontology:CSAMClassificationFacet (category per NCMEC)
     - observable:FileFacet (location: hidden folder)
     - cacontology:AcquisitionPeriodFacet (start: 2024-01, end: 2024-03)
   - ForensicAnalysis:
     - uco-action:ActionArgumentFacet (tool used, examiner)

7. RELATIONSHIPS:
   - investigation:wasFoundOn (CSAMCollection → Laptop)
   - investigation:wasDiscoveredBy (CSAMCollection → ForensicAnalysis)

8. VERIFY: Domain/range checks pass ✓

9. CONFIDENCE: HIGH - forensic report is authoritative source

10. EVIDENCE: documentId, span, quote recorded
```

---

### Example 3: Flagging a Term That Should Use Facets Instead

**Source text**: "The investigator noted that the suspect's chat logs showed a 'mentor' persona that offered guidance before transitioning to sexual content."

**Chain-of-Thought Extraction**:

```
1. PARSE:
   - Entity: "suspect" (offender)
   - Artifact: "chat logs" (evidence)
   - Concept: "'mentor' persona" (behavioral pattern)
   - Pattern: "transitioning to sexual content" (escalation)

2. EXTRACT:
   - Concept: MentorPersona (Category: Tradecraft/Behavior)

3. SEARCH:
   - cacontology-undercover:UndercoverPersona ✓ EXISTS
   - cacontology-tradecraft:GroomingTechnique ✓ EXISTS

4. EVALUATE: Should "MentorPersona" be a new class?
   
   ❌ WRONG APPROACH: Create cacontology-tradecraft:MentorPersona as subclass
   
   ✓ CORRECT APPROACH: Use existing class + facet
   - The "mentor" aspect is a perspective/characterization, not an intrinsic type
   - Different analysts might characterize the same behavior differently
   
5. MAP:
   - MentorPersona → REUSE: cacontology-tradecraft:GroomingTechnique 
   - Add: cacontology:TechniqueFacet with technique_type="mentor_persona"

6. RATIONALE:
   - Facets are preferred for perspective-based distinctions
   - "Mentor persona" is an analyst's characterization of grooming behavior
   - Creating a subclass would over-fit the ontology to this specific case
   - Other analysts might call this "trust-building" or "authority figure"

7. DRIFT CHECK:
   - If we created MentorPersona class: 85% similar to GroomingTechnique
   - FLAG: Potential duplicate - use facet instead

8. DECISION:
   → Use GroomingTechnique + TechniqueFacet
   → Do NOT create new MentorPersona class
   → Document: "Characterized as mentor persona via facet"
```

**Resulting Turtle** (correct facet-based approach):

```turtle
ex:grooming-technique-uuid a cacontology-tradecraft:GroomingTechnique ;
    rdfs:label "Mentor Persona Grooming Technique" ;
    uco-core:hasFacet ex:technique-facet-uuid .

ex:technique-facet-uuid a cacontology:TechniqueFacet ;
    cacontology:techniqueType "mentor_persona" ;
    cacontology:description "Suspect adopted mentor role offering guidance before escalation" ;
    cacontology:analystInterpretation "Trust-building through authority figure positioning" .
```

---

### Example 4: Near-Duplicate Resolution (Entity Resolution)

**Scenario**: Processing two documents from the same case where the same person appears with slightly different names.

**Document 1**: "John Michael Smith, age 34, was arrested on January 15, 2024."
**Document 2**: "J. M. Smith (34) was charged with distribution of CSAM."

**Chain-of-Thought for Entity Resolution**:

```
1. INITIAL EXTRACTION (Doc 1):
   - Entity: "John Michael Smith" 
   - UUID: urn:uuid:person-doc1-abc123
   - Age: 34
   - Action: arrested
   - Date: 2024-01-15

2. INITIAL EXTRACTION (Doc 2):
   - Entity: "J. M. Smith"
   - UUID: urn:uuid:person-doc2-def456
   - Age: 34
   - Action: charged

3. ENTITY RESOLUTION CHECK:
   - Name similarity: "John Michael Smith" vs "J. M. Smith"
     - Levenshtein distance: HIGH (different lengths)
     - BUT: "J. M." likely abbreviation of "John Michael"
     - Pattern match: First initial + Middle initial + Last name ✓
   - Age match: 34 = 34 ✓
   - Case context: Same case (arrest → charge is logical sequence) ✓
   
4. SIMILARITY ASSESSMENT:
   - Name pattern: HIGH confidence (abbreviation pattern)
   - Age: EXACT match
   - Contextual: Same case timeline
   - Overall: HIGH confidence same person

5. DECISION:
   - Link entities: owl:sameAs
   - Keep both UUIDs for provenance (each doc references its original)
   - Create linking provenance record

6. HALLUCINATION CHECK:
   - Both names explicitly in source ✓
   - Age explicitly stated in both ✓
   - No invented details ✓
   - Result: PASS

7. CONNECTIVITY CHECK:
   - person-doc1: arrested → links to arrest action ✓
   - person-doc2: charged → links to charge action ✓
   - Both connected ✓
```

**Resulting Turtle**:

```turtle
# Entity from Document 1
ex:person-doc1-abc123 a uco-identity:Person ;
    rdfs:label "John Michael Smith" ;
    cacontology:age 34 ;
    owl:sameAs ex:person-doc2-def456 .

# Entity from Document 2  
ex:person-doc2-def456 a uco-identity:Person ;
    rdfs:label "J. M. Smith" ;
    cacontology:age 34 .

# Linking provenance record
ex:linking-decision-xyz a investigation:ProvenanceRecord ;
    rdfs:label "Entity Resolution: John Michael Smith = J. M. Smith" ;
    uco-core:description "Linked based on: name abbreviation pattern match, exact age match, same case context" ;
    cacontology:confidence "high" ;
    cacontology:hasEvidencePointer ex:evidence-doc1-name, ex:evidence-doc2-name .
```

---

### Example 5: Ambiguous Entity Handling

**Source text**: "The officer reviewed the images on the suspect's phone."

**Chain-of-Thought for Ambiguous Entity**:

```
1. PARSE:
   - Entity: "officer" (person, LE role)
   - Action: "reviewed" (investigative action)
   - Entity: "images" (AMBIGUOUS - could be CSAM or legal images)
   - Entity: "suspect's phone" (device)

2. AMBIGUITY ANALYSIS:
   - "images" - What kind?
     - Could be: CSAM (illegal), personal photos (legal), evidence photos
     - Source does NOT specify
     - We cannot assume CSAM without explicit statement
   
3. EXTRACT WITH CAUTION:
   - Concept: "images" → uco-observable:ObservableObject (generic)
   - Do NOT classify as cacontology:CSAMEvidence without evidence
   - Do NOT assume content type

4. MAP:
   - images → uco-observable:ObservableObject 
   - Add: observable:ContentDataFacet (type: "image", unspecified content)
   - Do NOT add: cacontology:CSAMClassificationFacet (not stated)

5. CONFIDENCE:
   - Entity existence: HIGH (images mentioned)
   - Content classification: NOT ASSIGNED (ambiguous)
   - Note: "Content type not specified in source; do not assume CSAM"

6. HALLUCINATION CHECK:
   - ❌ WRONG: Assume images are CSAM because of case context
   - ✓ CORRECT: Model as generic images; flag for clarification
   - Decision: Mark as ambiguous, LOW confidence for content type
   - Result: ADJUSTED - removed implicit CSAM assumption

7. CONNECTIVITY CHECK:
   - images → links to phone (containedOn) ✓
   - images → links to review action (wasReviewedBy) ✓
   - Connected ✓

8. FLAG FOR REVIEW:
   - "Ambiguous entity: 'images' content type not specified"
   - "Recommend: Check subsequent documents for classification"
```

**Resulting Turtle** (conservative approach):

```turtle
ex:images-uuid a uco-observable:ObservableObject ;
    rdfs:label "Images on suspect's phone" ;
    uco-core:hasFacet ex:content-facet-uuid ;
    cacontology:confidence "low" ;
    cacontology:ambiguityNote "Content type not specified in source; awaiting classification" .

ex:content-facet-uuid a observable:ContentDataFacet ;
    observable:mimeType "image/*" ;  # Generic image type
    uco-core:description "Images found on device; content classification pending" .

# Do NOT add CSAMClassificationFacet without explicit evidence
```

---

### Example 6: Isolated Node Resolution

**Scenario**: An entity is extracted but has no relationships in the source text.

**Source text**: "The investigation also involved Homeland Security Investigations."

**Chain-of-Thought for Isolated Node**:

```
1. PARSE:
   - Entity: "Homeland Security Investigations" (organization)
   - Relationship: "involved" (vague, no specific action)

2. EXTRACT:
   - Concept: "Homeland Security Investigations" (HSI)
   - Category: Organization
   - UUID: urn:uuid:org-hsi-123

3. RELATIONSHIP ANALYSIS:
   - "involved" → What action? Not specified
   - No specific agent role stated
   - No specific action attributed to HSI
   
4. CONNECTIVITY CHECK (INITIAL):
   - Entity: HSI
   - Outgoing edges: NONE found in text
   - Incoming edges: NONE found in text
   - Total edges: 0
   - Result: ISOLATED NODE DETECTED ⚠️

5. RESOLUTION OPTIONS:
   a) FIND GROUNDED RELATIONSHIP:
      - Can we link HSI to the investigation itself?
      - "involved in investigation" → investigation:hasParticipant
      - This IS grounded: text says "investigation also involved"
      
   b) FLAG FOR REVIEW (if no grounded relationship):
      - If we can't find ANY valid relationship
      
   c) REMOVE (if truly orphaned):
      - If entity adds no value without relationships

6. DECISION:
   - Apply option (a): Link to investigation
   - Relationship: investigation:hasParticipant (HSI was a participant)
   - This is grounded in "investigation also involved"
   - Confidence: MEDIUM (relationship is vague but present)

7. HALLUCINATION CHECK:
   - ✓ HSI mentioned: explicit in text
   - ✓ "involved": explicit in text
   - ✓ We did NOT invent a specific action (e.g., "conducted raid")
   - Result: PASS

8. CONNECTIVITY CHECK (FINAL):
   - Entity: HSI
   - Incoming: participatedIn ← Investigation ✓
   - Total edges: 1
   - Result: PASS (no longer isolated)
```

**Resulting Turtle**:

```turtle
# The investigation (already exists in KG)
ex:investigation-uuid a investigation:Investigation ;
    rdfs:label "CSAM Distribution Investigation" ;
    investigation:hasParticipant ex:org-hsi-123 .

# HSI organization (now connected)
ex:org-hsi-123 a uco-identity:Organization ;
    rdfs:label "Homeland Security Investigations (HSI)" ;
    uco-core:description "Federal law enforcement agency involved in investigation" ;
    cacontology:confidence "medium" ;
    cacontology:hasEvidencePointer ex:evidence-hsi-mention .

# Evidence pointer for the HSI mention
ex:evidence-hsi-mention a cacontology:EvidencePointer ;
    cacontology:documentId "urn:uuid:source-doc-456" ;
    cacontology:span "paragraph 5" ;
    cacontology:quote "The investigation also involved Homeland Security Investigations." .
```

**Counter-Example: When to Remove an Isolated Node**:

```
Source text: "The weather was clear that day."

1. PARSE:
   - Entity: "weather" (environmental condition)
   - No relationship to CSEA domain

2. SCOPE CHECK:
   - "weather" is NOT in scope for CAC Ontology
   - Not CSEA, investigation, legal process, or tradecraft

3. DECISION:
   - Do NOT extract
   - This would be an isolated, out-of-scope node
   - REMOVE from consideration

4. DOCUMENT:
   - "Excluded: 'weather' - out of scope, no domain relevance"
```

---

## Appendix: Fine-Tuning + Evaluation

### Building a Gold Dataset

To improve agent accuracy, build a small annotated dataset:

1. Select 10-20 representative documents (press releases, forensic reports, court documents).
2. Manually annotate with:
   - Correct class mappings (with CoT reasoning documented)
   - Correct facet assignments (including perspective labels)
   - Evidence pointers for each assertion (documentId + span + quote)
   - Provenance chains (full UCO-aligned metadata)
   - Confidence levels with justifications
   - gUFO alignment for each class
3. Use for few-shot examples, evaluation, and fine-tuning.

### Fine-Tuning Recommendations

#### Recommended Base Models

| Model | Use Case | Fine-Tuning Method |
|-------|----------|-------------------|
| LLaMA 3 (8B/70B) | General extraction + reasoning | LoRA or QLoRA |
| Mistral (7B) | Efficient extraction tasks | LoRA |
| CodeLLaMA | SPARQL generation + validation | Full fine-tune or LoRA |
| Phi-3 | Edge deployment / resource-constrained | QLoRA |

#### LoRA Fine-Tuning Configuration

| Parameter | Recommended Value | Notes |
|-----------|------------------|-------|
| Rank (r) | 8-16 | Higher rank (16+) for complex ontology tasks; 8 for simpler extraction |
| Alpha (α) | 16-32 | Typically 2x rank; controls learning rate scaling |
| Dropout | 0.05-0.1 | Prevents overfitting; use 0.1 for smaller datasets |
| Target Modules | q_proj, v_proj, k_proj, o_proj | For attention layers; add mlp layers for more capacity |
| Epochs | 3-5 | Monitor validation loss; stop early if overfitting |
| Learning Rate | 1e-4 to 5e-4 | Lower (1e-4) for larger models; higher (5e-4) for smaller |
| Batch Size | 4-8 | Depends on GPU memory; use gradient accumulation if needed |
| Warmup Ratio | 0.03-0.1 | 3-10% of total steps for learning rate warmup |
| Weight Decay | 0.01 | Standard regularization |
| Max Sequence Length | 2048-4096 | Longer for documents with extensive context |

**QLoRA-Specific Settings** (for memory-constrained environments):
| Parameter | Recommended Value | Notes |
|-----------|------------------|-------|
| Quantization | 4-bit NF4 | NormalFloat4 quantization |
| Double Quantization | true | Reduces memory further |
| Compute Dtype | bfloat16 | For computation precision |

#### Fine-Tuning Dataset Requirements

- **Minimum**: 10-20 fully annotated documents with CoT traces
- **Recommended**: 50-100 documents for robust performance
- **Format**: Each example should include:
  ```json
  {
    "input": "<source text>",
    "cot_reasoning": "<step-by-step extraction process>",
    "output": {
      "concepts": [...],
      "mappings": [...],
      "facets": [...],
      "relationships": [...],
      "confidence": "...",
      "evidence_pointer": {...}
    }
  }
  ```

#### Training Targets

| Metric | Baseline (Zero-Shot) | Target (Fine-Tuned) |
|--------|---------------------|---------------------|
| Mapping accuracy | 70-80% | >95% |
| Hallucination rate | 12-25% | <8% |
| Facet assignment | 60-70% | >90% |
| Relationship correctness | 65-75% | >95% |
| CoT reasoning quality | Variable | Consistent |

#### Evaluation Protocol

1. **Hold-out test set**: Reserve 20% of gold dataset for evaluation
2. **Blind review**: Have domain experts review outputs without seeing source
3. **Automated checks**: Run SPARQL verification suite on all outputs
4. **A/B comparison**: Compare fine-tuned vs base model on same inputs
5. **Error analysis**: Categorize failures (hallucination, wrong class, missing facet, etc.)

### Evaluation Rubric

#### Core Metrics (Required)

| Metric | Target | How to Measure |
|--------|--------|----------------|
| UUID coverage | 100% | All instances use `urn:uuid:` IRIs |
| Provenance completeness | 100% | All documents have UCO provenance: URLFacet/FileFacet, HashFacet, collection action with startTime + performer |
| Evidence coverage | 100% | All key assertions have evidence pointers |
| Confidence coverage | 100% | All extracted assertions have confidence levels |
| Term citation coverage | 100% | All new/updated terms have `dcterms:source` |
| SHACL conformance | 100% | All shapes pass validation |
| Scope compliance | 100% | 0 out-of-scope domain triples |

#### Quality Metrics (Accuracy)

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Mapping accuracy | >95% | Correct class/property selections vs gold standard |
| Facet correctness | >90% | Manual review of facet assignments |
| Relationship verification | >95% | Domain/range compliance via SPARQL checks 6-7 |
| gUFO alignment accuracy | >90% | Correct foundational category assignments |

#### Reliability Metrics (Error Prevention)

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Hallucination rate | <12% | Manual review: assertions not supported by source text |
| False positive rate | <10% | Entities/relationships invented without evidence |
| Facet integrity | 100% | All hasFacet links to valid Facet subclasses (SPARQL check 5) |
| Deconfliction accuracy | >90% | Correct same-entity linking decisions in batch mode |
| Graph connectivity | 100% | All nodes have degree >= 1 (SPARQL check 11) |
| Edge grounding | 100% | All edges have evidence pointer or confidence |

#### Hallucination Detection Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| ROUGE-L vs source | >0.7 | Compare extracted text to source spans |
| Factual consistency | >0.9 | NLI-based fact verification against source |
| Entity grounding | 100% | All entities traceable to source text |
| Relationship grounding | >95% | Relationships supported by explicit or implied text |
| Invented detail rate | <5% | Details not found in source (manual review) |

**Hallucination Categories to Track**:
1. **Entity hallucination**: Names/identifiers not in source
2. **Relationship hallucination**: Connections not stated or implied
3. **Attribute hallucination**: Properties/values not in source
4. **Temporal hallucination**: Dates/times invented or wrong
5. **Quantitative hallucination**: Numbers/counts not in source

**Mitigation Strategies by Category**:
| Category | Mitigation |
|----------|------------|
| Entity | Require exact quote or span reference |
| Relationship | Verify domain/range + require evidence pointer |
| Attribute | Cross-check against source before adding |
| Temporal | Only extract explicit dates; mark inferred as LOW confidence |
| Quantitative | Only extract explicit numbers; flag approximations |

#### Batch Mode Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Cross-document consistency | >95% | Same entities linked correctly across documents |
| Duplicate detection | 100% | All duplicate URLs/paths identified before collection |
| Near-duplicate detection | >90% | ER catches URL variations, reformats, syndication |
| Merge correctness | >90% | Correct owl:sameAs linking with provenance |
| Agent provenance | 100% | All automated actions have performer + timestamp |
| Cross-doc connectivity | 100% | All entities link to at least one other entity |
| Average node degree | >2.0 | Total edges / total nodes across merged KG |
| Low-degree nodes | <10% | Nodes with only 1 connection |

### Error Taxonomy

When evaluating outputs, categorize errors using this taxonomy:

| Error Type | Description | Severity | Mitigation |
|------------|-------------|----------|------------|
| **Hallucination** | Assertion not in source text | Critical | More few-shot examples, lower temperature |
| **Wrong Class** | Incorrect class mapping | High | Better CoT prompting, ontology context |
| **Missing Facet** | Required facet not attached | Medium | Explicit facet checklist in CoT |
| **Wrong Facet** | Incorrect facet type | Medium | More facet examples |
| **Broken Relationship** | Domain/range violation | High | SPARQL verification in CoT |
| **UUID Collision** | Duplicate UUIDs | Critical | UUID generation validation |
| **Scope Drift** | Out-of-scope content modeled | High | Stricter scope screening |
| **Missing Evidence** | No evidence pointer | Medium | Evidence step in CoT |
| **Low Confidence Unmarked** | Uncertain assertion without flag | Medium | Confidence calibration training |
