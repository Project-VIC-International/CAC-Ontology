# CAC v4 Architecture Conformance Harness

This directory contains the deterministic, synthetic-data-only harness for the
issue-44 foundational architecture proposal. It separates frozen v3.1 baseline
observations from v4 release gates.

## Configurations

- **C1** — CAC v3.1 asserted graph at the recorded proposal base.
- **C2** — C1 plus the pinned UCO gUFO Profile interoperability overlay.
- **C3** — proposed CAC v4 normative graph.
- **C4** — C3 plus the same profile overlay.
- **C5** — C3 plus the bounded v3 compatibility artifact.

C1 and C2 are evidence, not release gates. C3 and C4 must pass all applicable
checks. C5 must pass before compatibility support is claimed.

## Local execution

Use Python 3.12 with the exact packages in `requirements.lock`, then run:

```text
python testing/v4/architecture_audit.py --configuration C3 --output <report.json>
python testing/v4/architecture_audit.py --configuration C4 --inference rdfs --output <report.json>
python testing/v4/architecture_audit.py --configuration C5 --inference rdfs --output <report.json>
python -m unittest discover -s testing/v4 -p "test_*.py" -v
```

The C1 report is frozen in `baselines/c1-v3.1-asserted.json` at the recorded
base commit. C2 and C4 use the exact ontology bytes from UCO gUFO Profile
commit `4b98b9881aa29ed80f39b589d15725fa696c921a`. Its runtime submodule closure
is reconstructed from exact commits and pinned in `dependency-lock.json`; all
normative imports resolve locally.

The lock hashes first-party and vendored RDF text after CRLF-to-LF
normalization. This changes neither committed nor upstream snapshot bytes; it
ensures Git-equivalent Windows and Unix checkouts produce the same identities.
First-party ontology files are also checked out with LF endings, and the graph
loader canonicalizes those bytes defensively before parsing and recording
reasoner-input identities.
The executable reproducibility controls also require every locked dependency
and every recorded profile-snapshot member to exist and match in a clean
checkout.

Pinned OWL 2 DL execution uses the runtime artifacts recorded in
`reasoner-runtime.lock.json`:

```text
python testing/v4/run_owl2dl.py --java <pinned-java> --robot-jar <pinned-robot-jar>
```

`run_owl2dl.py` records both the unmodified full closure and a bounded
diagnostic projection. The full closure is normative. The projection exists
only to separate CAC logical coherence from known upstream parsing and
reasoner-coverage defects; a projection pass never satisfies the release gate.

The audit reports the source commit, dirty state, runtime versions, graph
counts, and stable diagnostic identifiers. Remote imports are never silently
retrieved by the Python harness; the dependency catalog controls imported
content for connected and offline conformance runs. Exact upstream snapshots
are not modified to make them pass: their syntax and OWL/RDF structure findings
are recorded separately.

All fixtures in this directory are invented examples and contain no real case
or victim data.
