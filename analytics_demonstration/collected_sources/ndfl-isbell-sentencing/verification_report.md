# Verification Report: NDFL Isbell Sentencing

## Summary
- **Target KG**: `examples_knowledge_graphs/ndfl-isbell-sentencing-example.ttl`
- **Total Nodes**: 38
- **Total Edges**: 171
- **Average Degree**: 4.50

## SPARQL Verification Suite Results

| Check | Metric | Result | Status |
|-------|--------|--------|--------|
| 1 | Provenance completeness | 0 missing | PASS |
| 2 | Facet integrity | 0 untyped | PASS |
| 4 | Typed node coverage | 0 untyped | PASS |
| 11 | Isolated nodes (CRITICAL) | 0 isolated | **PASS** |
| 12 | Low-degree nodes | 0 (0.0%) | PASS |

## Overall Status
**ALL CRITICAL CHECKS PASS**

## SHACL Validation

| Shapes File | Conforms |
|-------------|----------|
| `cacontology-sentencing-shapes.ttl` | **True** |

## Metrics Summary
- UUID Coverage: 100% (all instance IRIs use urn:uuid:)
- Graph Connectivity: 38/38 nodes connected (100%)
- Provenance Completeness: 100%
- Average Node Degree: 4.50 (well above minimum of 1)
- Low-Degree Nodes: 0% (target: <10%)
- SHACL Conformance: **True**

## Files Generated
- `examples_knowledge_graphs/ndfl-isbell-sentencing-example.ttl` (38 nodes, 171 edges)
- `examples_knowledge_graphs/ndfl-isbell-sentencing-skeleton.ttl` (provenance skeleton)
- `example_SPARQL_queries/ndfl-isbell-sentencing-analytics.rq` (15 queries)
- `analytics_demonstration/collected_sources/ndfl-isbell-sentencing/` (collection artifacts)
