## BBC “dark web agent brick clue rescue” ingestion run report

- **Source**: [BBC News – How dark web agent spotted bedroom wall clue to rescue girl from years of harm](https://www.bbc.com/news/articles/cx2gn239exlo)
- **DocumentId (UUID)**: `urn:uuid:c96f7e7d-8fbb-5c31-9734-8b1d0530a15f`
- **Collected (UTC)**: 2026-02-11T00:00:00Z
- **Scope decision**: **IN-SCOPE** (CSEA investigation tradecraft; rescue action; investigator occupational harm/wellbeing)

### Phase -1: Data acquisition + preprocessing (completed)

- **Duplicate detection**: `duplicate_detection_report.md` (repo-local string search in lieu of triplestore query)
- **Raw artifact**: `source.txt`
  - **MIME**: `text/plain` (manual text capture)
  - **Bytes**: 2871
  - **SHA-256**: `7c9065e03cee14512baa332592c67d0684b57075355ea08e86900bc5cbb52575`
- **Normalized artifact**: `normalized.txt`
  - **MIME**: `text/plain`
  - **Bytes**: 2482
  - **SHA-256**: `2a7b38c02bac66a57802a720cb5f34f7a946d4e6b17c5d3916b3644332992cd2`
- **Manifest**: `manifest.yaml`

### Phase 0: setup + guardrails (completed)

#### Working assumptions

- The article is treated as a **public informational source** (not a case file).
- We model **only** in-scope investigative tradecraft and occupational harm concepts described by the reporting.
- We avoid modeling real victim identity/location; “Lucy” is handled as a **pseudonym label** only.
- No CSAM content is stored; only narrative descriptions and provenance/evidence pointers.
- All instances use **`urn:uuid:`** IRIs; no blank nodes.

#### Reuse-first summary (no new ontology terms added)

- **UCO Observable facets**: `uco-observable:ContentDataFacet`, `uco-observable:URLFacet`, `uco-observable:FileFacet`, `uco-observable:HashFacet`
- **UCO Action / CASE Investigation**: `uco-action:Action`, `investigation:InvestigativeAction`, `investigation:ProvenanceRecord`
- **UCO Identity**: `uco-identity:Person`, `uco-identity:Organization`
- **CAC analyst wellbeing module (reuse)**: `cacontology-analyst:SecondaryTraumaticStress`, `cacontology-analyst:VicariousTrauma`, `cacontology-analyst:experiencesOccupationalHarm`

### Phase 1: concept inventory + mapping (completed)

| Concept / claim (high-level) | Evidence pointer | Confidence | Modeling |
|---|---:|---:|---|
| Infer broad region from electrical outlets | `normalized.txt` line 10 | high | investigative action (described) + concept object |
| Regional product constraint (sofa) narrows candidates | `normalized.txt` line 12 | high | investigative action + concept object |
| Brick identification + “bricks are heavy” geographic narrowing | `normalized.txt` lines 13-14 | high | investigative action + brick type object |
| Social media search produces lead (photo linkage) | `normalized.txt` line 15 | high | investigative action |
| Avoid tipping off suspect (avoid door-to-door) | `normalized.txt` line 16 | high | investigative action constraint concept |
| Occupational harm impacts on investigator | `normalized.txt` line 20 | high | `cacontology-analyst:SecondaryTraumaticStress` linked to person |

### Governance gate (REVIEW REQUIRED queue)

- **New ontology terms**: none (✅ not required for this ingestion)
- **SKOS mappings**: none (✅ not required for this ingestion)
- **Sensitive entity modeling**: **REVIEW REQUIRED** (✅ minimized; pseudonym only; no victim PII)

### Phase 4–5: example KG + SPARQL queries (completed)

- **Skeleton KG**: `examples_knowledge_graphs/bbc-dark-web-agent-brick-clue-rescue-girl-skeleton.ttl`
- **Example KG**: `examples_knowledge_graphs/bbc-dark-web-agent-brick-clue-rescue-girl-example.ttl`
- **Queries**: `example_SPARQL_queries/bbc-dark-web-agent-brick-clue-rescue-girl-analytics.rq`

### Phase 6: validation (completed)

- **SHACL (core shapes)**: Conforms: **True**
- **SHACL (analyst wellbeing shapes)**: Conforms: **True**

