## Know2Protect SOE Brochure (PDF) Ingestion Run Report

- **Source**: Know2Protect (DHS) brochure PDF: “Tips2Protect Against Sadistic Online Exploitation”
- **DocumentId (UUIDv5)**: `urn:uuid:1d896431-835d-585d-929b-f51fafce1fe2`
- **Collected (UTC)**: 2026-02-11T00:00:00Z
- **Scope decision**: **IN-SCOPE** (CSEA prevention + offender tradecraft patterns + reporting workflows; no case-specific victims modeled)

### Phase -1: Data Acquisition + Preprocessing (completed)

- **Duplicate detection**: `duplicate_detection_report.md` (repo-local search in lieu of triplestore query)
- **Raw artifact**: `K2P SOE Information.pdf`
  - **MIME**: `application/pdf`
  - **Bytes**: 23221236
  - **SHA-256**: `7e76dd7ab749bce560cb2c8ed8c75b3a6e7e725cb9795137d6e1c5bb78010742`
- **Extracted text (capture)**: `source.txt`
  - **MIME**: `text/plain`
  - **Bytes**: 12191
  - **SHA-256**: `579994b7b085d1b201985150a0dc20c422feba124c7727a304a5328bf613989a`
- **Normalized text (evidence-pointer stable)**: `normalized.txt`
  - **MIME**: `text/plain`
  - **Bytes**: 9552
  - **SHA-256**: `04a9e4a262e4410b3c6556e7e02bbd01581503ba20cfa9a4377961553688fc8a`
- **Manifest**: `manifest.yaml`

### Phase 0: Setup + Guardrails (completed)

#### Working assumptions

- The brochure is treated as a **public informational source** (not a case record).
- We model **only** in-scope concepts: SOE enterprise characteristics, coercion tactics, grooming/sextortion concepts, involvement indicators, and response/reporting guidance.
- We avoid modeling **victim identity** (the brochure includes a named minor death; this run preserves the claim only at a generalized level).
- All instances use **`urn:uuid:`** IRIs; no blank nodes.

#### Reuse-first summary (initially no new ontology terms added)

- **UCO Observable facets**: `uco-observable:FileFacet`, `uco-observable:URLFacet`, `uco-observable:HashFacet`, `uco-observable:ContentDataFacet`
- **UCO Action**: `uco-action:Action` (for brochure statements and list publication)
- **CASE Investigation**: `investigation:InvestigativeAction`, `investigation:ProvenanceRecord` (for collection and statement provenance)
- **CAC Extremist Enterprises**: `cacontology-enterprises:*` (enterprise + coercion + targeting patterns; includes 764-aligned modeling)
- **CAC Grooming & Sextortion modules**: referenced conceptually in the KG (definitions, tactics)

### Phase 1: Concept Inventory + Mapping (completed)

- **Mapping manifest**: `mapping_manifest.yaml`

### Phase 4–5: Example KG + SPARQL Queries (completed)

- **Example KG**: `examples_knowledge_graphs/k2p-soe-information-example.ttl`
- **Queries**: `example_SPARQL_queries/k2p-soe-information-analytics.rq`

### Phase 6: Validation (not run in this local report)

Validation was run locally (Docker not available on this workstation) using `python -m pyshacl` plus the SPARQL sanity suite subset.

- **SPARQL sanity suite (subset)**: `sparql_verification_report.md` (**PASS**)
- **SHACL validation results**:
  - `ontology/cacontology-soe-shapes.ttl` against `ontology/cacontology-soe.ttl`: **Conforms: True**
  - `ontology/cacontology-soe-shapes.ttl` against `examples_knowledge_graphs/k2p-soe-information-example.ttl`: **Conforms: True**
  - `ontology/cacontology-core-shapes.ttl` against `examples_knowledge_graphs/k2p-soe-information-example.ttl`: **Conforms: True**
  - `ontology/cacontology-sextortion-shapes.ttl` against `examples_knowledge_graphs/k2p-soe-information-example.ttl`: **Conforms: True**
