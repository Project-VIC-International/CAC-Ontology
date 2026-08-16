# Gate 4 Evidence Bundle

The canonical final evidence files are:

- `gate4-summary.json` — machine-readable decision summary;
- `c2-asserted.json` and `c2-rdfs.json` — frozen-base overlay observations;
- `c3-asserted.json` and `c3-rdfs.json` — normative proposal diagnostics;
- `c4-asserted.json` and `c4-rdfs.json` — exact-profile overlay diagnostics;
- `c5-asserted.json` and `c5-rdfs.json` — compatibility-profile diagnostics;
- `owl2dl-summary.json` — pinned full-closure and diagnostic ROBOT/HermiT results;
- `rem-014-decomposition.json` and `rem-014-decomposition.md` — current strict-profile ownership, root-cause, priority, and baseline-delta summary;
- `rem-014-findings.jsonl.gz` — deterministic full finding-level REM-014 evidence;
- `c3-owl2dl-profile.txt.gz` and `c5-owl2dl-profile.txt.gz` — deterministic compressed strict-profile reports;
- `dependency-owlapi-rdf-structures.json` — malformed upstream OWL/RDF structures;
- `dependency-turtle-syntax.json` — syntax audit of every content-addressed Turtle file in the vendored runtime closure;
- `c4-unsatisfiable-class-paths.json` — asserted-path analysis for C4 diagnostic unsatisfiable classes;
- `shacl-sparql-syntax.json` — all embedded query parse results, with PR #48 isolated;
- `shape-level-assumptions.json` — review inventory of gUFO role/phase mentions;
- `unittest.txt` — complete executable test output;
- `gate4-review.md` — human review and handoff.

Files with `preview` or intermediate slice names are non-canonical working reports and may be regenerated or discarded. All fixtures are synthetic.

The strict full-import result is authoritative. Files labeled `diagnostic-projection` are root-cause isolation evidence only and must not be cited as OWL 2 DL release conformance.
