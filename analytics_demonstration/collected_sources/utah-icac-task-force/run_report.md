## Utah ICAC Task Force Webpage Ingestion Run Report

- **Source**: [Utah Attorney General – ICAC Task Force](https://attorneygeneral.utah.gov/icac/)
- **DocumentId (UUID)**: `urn:uuid:82588a71-7176-4cd0-aaee-56cffc467f86`
- **Collected (UTC)**: 2026-01-07T02:59:19Z
- **Scope decision**: **IN-SCOPE** (law enforcement task force context for CSEA investigations + reporting contacts + focus crime categories)

### Phase -1: Data Acquisition + Preprocessing (completed)

- **Duplicate detection**: `duplicate_detection_report.md` (repo-local grep in lieu of triplestore query)
- **Raw artifact**: `source.html`
  - **MIME**: `text/html`
  - **Bytes**: 35953
  - **SHA-256**: `6ec7cea6c9da98611f732bfe65039531dd032678ebb6fe3b4e961a5f7fe076c2`
- **Normalized artifact**: `normalized.txt`
  - **MIME**: `text/plain`
  - **Bytes**: 17554
  - **SHA-256**: `0555fc5ae78a4fb7db4e617c31e3dcacd5ee3a5813317b889b6f23ad3ac2f1f7`
- **Manifest**: `manifest.yaml`

### Phase 0: Setup + Guardrails (completed)

#### Working assumptions

- The page is treated as a **public informational source** (not a case record).
- We model **only** in-scope operational facts: task force identity, reporting contacts, stated focus crime categories, affiliate-agency list, and high-level funding/admin statement.
- We avoid modeling generic public-safety advice content as domain triples unless it directly supports in-scope prevention concepts (kept out here).
- Where the page provides counts (e.g., “65 affiliates”), we do **not** fabricate missing rows; we preserve what is actually extracted in `normalized.txt`.
- All instances use **`urn:uuid:`** IRIs; no blank nodes.

#### Reuse-first summary (no new ontology terms added)

- **UCO Observable facets**: `uco-observable:URLFacet`, `uco-observable:HashFacet`, `uco-observable:FileFacet`, `uco-observable:ContentDataFacet`
- **UCO Action**: `uco-action:Action` (for webpage statements and list publication)
- **CASE Investigation**: `investigation:InvestigativeAction`, `investigation:ProvenanceRecord` (for collection provenance and statement provenance)
- **UCO Identity**: `uco-identity:Organization` (task force, affiliates, agencies)

#### Files changed / added (this run)

- `analytics_demonstration/collect_webpage.py` (stdlib-only HTML→text normalization)
- `analytics_demonstration/generate_utah_icac_webpage_example.py` (deterministic UUIDv5 generator)
- `analytics_demonstration/collected_sources/utah-icac-task-force/*` (raw+normalized+manifest+reports)
- `examples_knowledge_graphs/utah-icac-task-force-webpage-skeleton.ttl` (provenance skeleton)
- `examples_knowledge_graphs/utah-icac-task-force-webpage-example.ttl` (extended example KG)
- `example_SPARQL_queries/utah-icac-task-force-webpage-analytics.rq` (12 queries)

### Phase 1: Concept Inventory + Mapping (completed)

#### Concept inventory (in-scope)

| Concept | Category | Source snippet | Evidence pointer | Confidence | Modeling |
|---|---|---|---|---|---|
| Utah AG ICAC Task Force | Org | “The Internet Crimes Against Children Task Force (ICAC)… Utah Attorney General ICAC Task Force…” | `normalized.txt` lines 35-45 | high | `uco-identity:Organization` |
| Reporting contacts | Evidence/Other | “ICAC Tip Line… ICAC Email…” | `normalized.txt` lines 41-42 | high | `uco-observable:ObservableObject` values + `uco-action:Action` |
| Crimes investigated (3) | Other | “Crimes We Investigate …” | `normalized.txt` lines 49-52 | high | 3× `uco-core:UcoObject` + listing `uco-action:Action` |
| Funding/admin statement | Other | “funded by a grant… OJJDP… administered through…” | `normalized.txt` lines 37-40 | high | `uco-action:Action` + `investigation:ProvenanceRecord` |
| Digital Respons-Ability program | Other | “sponsors the Digital Respons-Ability program…” | `normalized.txt` lines 46-48 | high | `uco-core:UcoObject` + `uco-action:Action` |
| Affiliate agencies list | Org | “Utah Attorney General ICAC Affiliates … [list] …” | `normalized.txt` lines 64-128 | high | 64× `uco-identity:Organization` + listing `uco-action:Action` |

#### Mapping manifest

- `mapping_manifest.yaml` (UCO-aligned per `prompt.md`)

### Governance gate (REVIEW REQUIRED queue)

- **New ontology terms**: none (✅ not required)
- **SKOS mappings**: none (✅ not required)
- **Sensitive entity modeling**: none (✅ no victims/minors modeled)

### Phase 4–5: Example KG + SPARQL Queries (completed)

- **Example KG**: `examples_knowledge_graphs/utah-icac-task-force-webpage-example.ttl`
- **Queries**: `example_SPARQL_queries/utah-icac-task-force-webpage-analytics.rq`

### Phase 6: Validation (pending results)

#### SHACL validation

- **Shapes**: `ontology/cacontology-core-shapes.ttl`
- **Data**: `examples_knowledge_graphs/utah-icac-task-force-webpage-example.ttl`
- **Result**: **Conforms: True**
- **Report**: `shacl_validation_core.txt`

#### SPARQL verification suite (subset)

- **Report**: `sparql_verification_report.md`
- **Summary**: all checks PASS (0 failures / 0 isolated nodes)

