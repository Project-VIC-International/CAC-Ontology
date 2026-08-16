# REM-014 OWL 2 DL Profile Decomposition

The earlier 7,287/7,289 figures were non-empty line counts. Multiline SPARQL annotation bodies inflated those totals. This decomposition counts only recognized ROBOT violation headers.

- C3 REM-014 baseline: **6,947**
- C5 REM-014 baseline: **6,949**
- C3 actual violations: **6,116**
- C5 actual violations: **6,116**
- C3 reduction from baseline: **-831**
- C5 reduction from baseline: **-833**
- C5 compatibility delta: **+0**

## Ownership

| Owner | C3 occurrences |
|---|---:|
| upstream | 6,116 |

## Prioritized remediation units

| Priority | Root cause | Scope | CAC occurrences | Total occurrences | Unique IRIs | Score |
|---:|---|---|---:|---:|---:|---:|
| 1 | embedded-shacl-vocabulary-not-declared-for-owlapi | external | 0 | 5,537 | 26 | 0 |
| 2 | missing-or-invalid-upstream-declaration | external | 0 | 577 | 6 | 0 |
| 3 | property-kind-punning | external | 0 | 2 | 1 | 0 |

## Interpretation boundary

Ownership is inferred from the violated IRI and the axiom actor before the merged OntologyID suffix. `cac` findings are candidates for local repair. `upstream` findings remain pinned external evidence. `shared-or-unattributed` findings require source-level provenance before assignment. The unmodified full-import report remains authoritative.
