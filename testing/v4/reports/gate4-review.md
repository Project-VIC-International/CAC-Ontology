# CAC v4 Foundational Proposal — Gate 4.4 Reproducibility Review

**Recommendation:** **Publish the corrected candidate to the existing draft PR #49, while retaining HOLD on maintainer-review readiness until PR #48 is integrated and HOLD on every v4.0.0 release claim.**

Gate 4.4 repairs the clean-checkout reproducibility and contributor-guideline defects found by independent verification. All accepted first-party semantic, datatype, and vocabulary policies remain implemented and regression-controlled. The unmodified full-import closure still does not satisfy the normative OWL 2 DL gate, but the recognized C3/C5 remainder remains entirely attributable to pinned upstream dependencies. This is a reviewable foundational proposal, not a release artifact.

No GitHub mutation occurred during Gate 4.4 evidence generation.

## Source identity

| Item | Value |
|---|---|
| Frozen base | `93de063951b758dd68a27611638c177fcf910eab` (`v3.1.0`) |
| Sealed source candidate | `41cc0049cf0304681801582d0e5ae1e2755ada12` |
| Candidate tree | `473a15f5b9e1c453ecc1d8c5cbb7ab731561616d` |
| Branch | `proposal/issue-44-v4-foundational-architecture` |
| DCO status | All 35 local commits from the frozen base contain sign-off trailers |
| Pre-existing unsigned commits reported by the manifest | 0 |
| Tracked source dirty during final evidence run | No |
| Commit convention | All 35 subjects satisfy the repository's Conventional Commits convention |
| GitHub publication | Existing draft PR #49; corrected history not yet pushed at evidence time |

## Gate 4.1 acceptance outcome

| Control | Result |
|---|---|
| C3 architecture, asserted/RDFS | Pass/pass; 0 findings |
| C4 architecture, asserted/RDFS | Pass/pass; 0 findings |
| C5 architecture, asserted/RDFS | Pass/pass; 0 findings |
| Executable tests | Pass; 94/94 |
| Import closure | Pass; 75/75 resolved, 0 remote gaps |
| Locked Turtle dependencies | Pass; 28/28 parse |
| Proposal-owned SHACL SPARQL syntax | Pass; 0 failures |
| Diagnostic HermiT projections | Pass for C3, C4, and C5 |
| C3 strict profile | 6,116 findings: 0 CAC, 0 shared, 6,116 upstream |
| C5 strict profile | 6,116 findings: 0 CAC, 0 shared, 6,116 upstream |
| C4 strict ingestion | Upstream failure before classification due to malformed exact-profile RDF structures |
| Normative full-import OWL 2 DL | HOLD; upstream/tool-route blockers remain |

## Implemented policy surface

1. Applied all twenty reviewed semantic mapping families, including event/role direction, qualified participation, lifecycle, record/classifier, service/device/call, norm/artifact, planning-artifact, phone-account/facet, and temporal-ordering corrections.
2. Replaced unsupported normative `xsd:duration` and `xsd:gYear` usage with the approved lexical-string and integer-year policies while preserving all fourteen existing duration values exactly.
3. Added positive and negative SHACL fixtures for datatype behavior and structured phone-account traces.
4. Added bounded SKOS/DCMI declarations with content-addressed authoritative snapshots; no uncontrolled full standards import was introduced.
5. Centralized the six CAC design-note predicates as annotation properties and removed literal-valued `skos:exactMatch` assertions.
6. Regenerated the dependency lock, architecture reports, strict-profile reports, REM-014 decomposition, and complete regression transcript.
7. Canonicalized first-party text hashing so Git-equivalent LF and CRLF checkouts produce identical dependency identities.
8. Restored the exact locked DCMI reference and gUFO-profile exemplar, canonicalized vendored RDF text identities without altering committed bytes, and added clean-checkout presence/hash regression controls.
9. Added the required unreleased changelog, README, user-documentation, glossary, and dependency-policy guidance.
10. Replayed eleven historical subjects into Conventional Commit form while preserving all 33 pre-correction commit trees and DCO trailers.
11. Enforced LF checkout for first-party ontology files and canonicalized reasoner-input identities, with an executable regression proving the Git attribute contract on every ontology module.

## Measured REM-014 result

- C3 moved from 6,947 to 6,116 recognized findings: **831 removed**.
- C5 moved from 6,949 to 6,116 recognized findings: **833 removed**.
- C3 CAC-owned findings moved from 812 to **0**.
- C3 shared/header findings moved from 19 to **0**.
- The 6,116 upstream-owned findings did not change.
- C3 and C5 now have exact parity; the compatibility artifact adds no strict-profile finding.

## Preserved boundaries and residual risks

- The exact pinned dependency bytes were not edited.
- C3/C5 HermiT strict reasoning still encounters imported SWRL built-ins unsupported by the pinned route.
- The exact profile still contains malformed OWL/RDF structures that block C4 OWLAPI ingestion.
- Diagnostic projections demonstrate bounded CAC coherence but are not represented as normative full-import conformance.
- PR #48 remains unchanged and is a merge-readiness dependency for the seven known detection-shape SPARQL syntax failures.
- Issue/PR #46 remains an independent v3.x path and is unchanged; this v4 proposal contains the equivalent systemic platform-range correction and discloses that overlap.
- The exhaustive post-v4 remediation charter remains active for upstream coordination, tooling alternatives, documentation, and future findings.

## Publication boundary

Gate 4.4 authorizes a lease-protected update only to the dedicated issue-44 branch and accurate edits only to existing draft PR #49 after clean-room controls pass. It does not authorize a release claim, merge, tag, modification of PR #48 or issue/PR #46, or representation of diagnostic projections as normative OWL 2 DL conformance.
