## SPARQL Verification Suite (subset)
- **Dataset**: `examples_knowledge_graphs/k2p-soe-information-example.ttl`
- **Triples**: 416

| Check | Result | Count | Notes |
|---|---|---:|---|
| 1 Collection actions have startTime | **PASS** | 0 |  |
| 1a Collection actions have performer | **PASS** | 0 |  |
| 2 Facet integrity: every hasFacet target is typed | **PASS** | 0 |  |
| 3 UUID coverage: instance IRIs should be urn:uuid: | **PASS** | 0 | Expected: 0 results (only ontology IRIs should be http(s)). |
| 4 Typed node coverage: all urn:uuid nodes have rdf:type | **PASS** | 0 |  |
| 11 Isolated nodes: urn:uuid nodes must have degree >= 1 (excluding rdf:type) | **PASS** | 0 |  |
