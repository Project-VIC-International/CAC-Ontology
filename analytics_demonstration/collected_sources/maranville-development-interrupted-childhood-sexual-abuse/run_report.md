## Maranville (LinkedIn Pulse) article ingestion run report

- **Source**: `https://www.linkedin.com/pulse/when-development-interrupted-childhood-sexual-abuse-maranville-phd-wlrje/`
- **Title**: *When Development Is Interrupted by Childhood Sexual Abuse*
- **Author (as stated)**: Melissa Maranville, PhD
- **Published (as stated)**: 2026-02-05
- **DocumentId (UUID)**: `urn:uuid:582ed787-34e0-5fbd-b457-ffb11e94c3af`
- **Collected (UTC)**: 2026-02-11T00:00:00Z
- **Scope decision**: **IN-SCOPE** (victim/survivor terminology; developmental/complex trauma impacts of childhood sexual abuse)

### Phase -1: Data acquisition + preprocessing (completed)

- **Duplicate detection**: `duplicate_detection_report.md` (repo-local string search in lieu of triplestore query)
- **Raw artifact**: `source.txt`
  - **MIME**: `text/plain` (manual text capture)
  - **Bytes**: 4651
  - **SHA-256**: `611b43884049f6ef55e8516f28888b25aaa964e5b2a63b57b54ce653aef11d4e`
- **Normalized artifact**: `normalized.txt`
  - **MIME**: `text/plain`
  - **Bytes**: 4254
  - **SHA-256**: `d92d4f4360ff4febf259fdb7eb6eab8fba9a1ecf5e547c7dd501d9949186fea8`
- **Manifest**: `manifest.yaml`

### Phase 0: setup + guardrails (completed)

#### Working assumptions

- The article is treated as a **public informational source** (not a case record).
- We model **only** in-scope conceptual claims related to CSA’s developmental impact (trauma framing, attachment stability, language/labeling implications).
- We do **not** model a victim/survivor individual for the author’s narrative example; we only model that the article states generalizable claims.
- All instances use **`urn:uuid:`** IRIs; no blank nodes.

#### Reuse-first summary (no new ontology terms added)

- **UCO Observable facets**: `uco-observable:ContentDataFacet`, `uco-observable:URLFacet`, `uco-observable:FileFacet`, `uco-observable:HashFacet`
- **UCO Action**: `uco-action:Action` (statement actions); `investigation:InvestigativeAction` (collection action)
- **CASE Investigation**: `investigation:ProvenanceRecord`
- **UCO Identity**: `uco-identity:Person`, `uco-identity:Organization`
- **CAC victim impact module (reuse)**: `cacontology-impact:ComplexTrauma`, `cacontology-impact:DevelopmentalImpact`

### Phase 1: concept inventory + mapping (completed)

| Concept / claim | Category | Evidence pointer | Confidence | Modeling |
|---|---|---:|---:|---|
| Early CSA shapes development while “still forming” (not disruption of a finished system) | Claim | `normalized.txt` lines 6-8 | high | statement `uco-action:Action` → `cacontology-impact:DevelopmentalImpact` |
| “Developmental trauma or complex trauma” framing for early CSA | Claim | `normalized.txt` line 12 | high | statement `uco-action:Action` → `cacontology-impact:ComplexTrauma` |
| “Instead of learning safety… learns threat/vigilance… closeness brings danger” | Claim | `normalized.txt` line 11 | high | statement `uco-action:Action` → concept objects (UCO `UcoObject`) |
| Attachment patterns formed early are relatively stable across lifespan | Claim | `normalized.txt` line 15 | high | statement `uco-action:Action` → concept object (UCO `UcoObject`) |
| “Language of healing” framing can be misleading for survivors (no baseline to restore) | Claim | `normalized.txt` line 16 | high | statement `uco-action:Action` → concept object (UCO `UcoObject`) |
| Naming/terminology can distance responsibility (“child prostitute”, “young woman”) | Claim | `normalized.txt` lines 17-18 | high | statement `uco-action:Action` → concept object (UCO `UcoObject`) |

### Governance gate (REVIEW REQUIRED queue)

- **New ontology terms**: none (✅ not required for this ingestion)
- **SKOS mappings**: none (✅ not required for this ingestion)
- **Sensitive entity modeling**: **minimal** (✅ no child victim identities modeled; author represented only as article author)

### Phase 4–5: example KG + SPARQL queries (completed)

- **Skeleton KG**: `examples_knowledge_graphs/maranville-development-interrupted-childhood-sexual-abuse-skeleton.ttl`
- **Example KG**: `examples_knowledge_graphs/maranville-development-interrupted-childhood-sexual-abuse-example.ttl`
- **Queries**: `example_SPARQL_queries/maranville-development-interrupted-childhood-sexual-abuse-analytics.rq`

