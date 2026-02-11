## Duplicate detection report

- **Candidate source URL**: `https://www.linkedin.com/pulse/when-development-interrupted-childhood-sexual-abuse-maranville-phd-wlrje/`
- **Method**: repo-local string search (in lieu of a triplestore SPARQL lookup)
- **Searched locations**:
  - `analytics_demonstration/`
  - `examples_knowledge_graphs/`
  - `example_SPARQL_queries/`
  - `ontology/`
- **Result**: **NOT FOUND** (treat as new source; proceed with collection)

### Notes

- LinkedIn pages often require authentication for raw HTML retrieval; this ingestion run uses the article text as captured in `source.txt` and normalized in `normalized.txt`.

