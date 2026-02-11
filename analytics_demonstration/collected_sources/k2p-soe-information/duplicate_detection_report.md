## Duplicate Detection Report (k2p-soe-information)

- **Candidate source**: `K2P SOE Information.pdf`
- **Observed SHA-256**: `7e76dd7ab749bce560cb2c8ed8c75b3a6e7e725cb9795137d6e1c5bb78010742`
- **Observed bytes**: 23221236

### Method

This repo run does not have a triplestore/GraphDB endpoint configured, so duplicate detection was performed via repo-local text search over:

- `analytics_demonstration/`
- `examples_knowledge_graphs/`
- `example_SPARQL_queries/`
- `ontology/`

Search keys:

- the PDF SHA-256 value
- the candidate file path string (`K2P SOE Information.pdf`)

### Results

- **Exact matches found**: none
- **Decision**: **PROCEED** (treat as new source)

### Notes

- Near-duplicate/entity-resolution checks are **not** performed in this local run because no embedding index or document registry is configured.
