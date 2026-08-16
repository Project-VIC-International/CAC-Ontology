# Gate 4 vendored dependencies

These files provide a deterministic, offline ontology and SHACL import closure for the v4 conformance configurations. They are test and evidence inputs, not CAC release artifacts.

| Dependency | Pinned identity | Purpose |
|---|---|---|
| UCO gUFO Profile | `4b98b9881aa29ed80f39b589d15725fa696c921a` | C2/C4 interoperability overlay and profile shapes |
| UCO | `7ebb3957e9e9a2e1bb9c66cd1ede8c912a726344` | Exact profile gitlink; UCO 1.5.0 ontology modules |
| CDO-Shapes-gufo | `1b13dd56308261f451db3e304ce7a5e044ed0297` | Generated gUFO 1.0.0 ontology and gUFO shapes |
| CASE | `8073d5a0a4f8741799adfe0c494d58fd6472acaa` (`1.5.0`) | CASE case and investigation imports used by CAC |
| Collections Ontology | `619e7b02646321174635fd04be658e338bf7d1d7` | UCO dependency |
| SPAR Error Ontology | `101aca952ef854505f49725d852de00e6e192344` | Collections Ontology dependency |
| W3C SHACL vocabulary | official bytes retrieved `2026-08-15` | Resolves `http://www.w3.org/ns/shacl#` |
| W3C SKOS reference | Recommendation bytes dated `2009-08-18` | Bounded standards-profile evidence |
| DCMI Metadata Terms | Vocabulary bytes modified `2012-06-14` | Bounded standards-profile evidence |

`testing/v4/dependency-lock.json` records every executed file's canonical text length and SHA-256 plus every direct and transitive `owl:imports` resolution. CRLF is normalized to LF for identity only, so Git-equivalent checkouts are stable while committed vendored snapshots remain untouched. The lock also inventories the exact UCO gUFO Profile source snapshot, including its exemplar. Validation scripts do not retrieve remote imports.
