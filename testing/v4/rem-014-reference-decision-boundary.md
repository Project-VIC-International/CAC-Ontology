# REM-014 External Reference Decision Boundary

This ledger records the 64 CAC-owned external-reference findings that remain
after all non-interpretive pinned-vocabulary repairs. These findings are not
safe mechanical edits: each candidate replacement changes abstraction level,
property direction, or domain meaning and therefore requires an explicit
ontology design decision.

| Decision family | Findings | Retired or invalid IRIs | Decision required |
|---|---:|---|---|
| gUFO abstraction migration | 20 | `AbstractArtifact`, `IntrinsicMoment`, `Norm`, `ParticipationSituation`, `Plan`, `Process` | Choose the intended current gUFO category per CAC class; do not collapse all terms into `AbstractIndividual`, `IntrinsicAspect`, `Participation`, or `Event` without class-level review. |
| gUFO participation direction | 7 | `participantIn`, `participatesIn` | Confirm whether each CAC property is entity-to-event before specializing current `participatedIn`; reverse-direction properties require a CAC inverse or a different alignment. |
| gUFO temporal relation | 1 | `precedes` | The pinned gUFO vocabulary has no direct `precedes` property; retain the CAC property without a gUFO superproperty or approve a separately justified temporal alignment. |
| UCO action and observable migration | 25 | `action:Crime`, `channel:DigitalService`, `observable:DigitalArtifact`, `DigitalDevice`, `DigitalService`, `DigitalServiceFeature`, `PhoneCall`, `PhoneNumber` | Select current UCO classes from the modeled referent, not lexical similarity alone (for example `Action`, `OnlineService`, `Observable`, `Device`, `OnlineServiceFacet`, `Call`, or a phone-account/contact pattern). |
| UCO role migration | 11 | `OffenderRole`, `SubjectRole`, `VictimRole` | Apply the v4 classifier/record separation: decide among `role:Role`, `MaliciousRole`, `NeutralRole`, `victim:Victim`, or a CAC classifier for each use. |

## Repairs already proven safe

- `gufo:hasQuality` was replaced by the pinned datatype property
  `gufo:hasQualityValue` in 51 ontology axioms and the matching SHACL path.
- Same-name UCO relocations were applied only where the pinned module declares
  the exact class: `core:Observable` to `observable:Observable`, `core:Role` to
  `role:Role`, `identity:Software` to `observable:Software`, and
  `observable:Hash` to `types:Hash`.

## Acceptance rule

A future change may leave this boundary only when its commit identifies the
source and target IRI, states whether the relationship direction is preserved,
adds a pinned-vocabulary regression, and demonstrates no new C3/C4/C5
architecture finding. Validator-count reduction alone is not sufficient.
