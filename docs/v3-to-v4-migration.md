# v3-to-v4 Migration Notes

> **Status:** Gate 3 proposal. Do not treat these notes as a published release migration guide until Gate 4 approval.

## Safe automatic rewrites

| v3 property | v4 property | Rewrite |
|---|---|---|
| `cacontology-custodial:inCustodyPhase` | `cacontology-custodial:currentCustodyState` | Rename predicate |
| `cacontology-custodial:hasCustodyPhase` | `cacontology-custodial:hasCustodyState` | Rename predicate |

The compatibility ontology exposes each legacy predicate as a deprecated subproperty of its replacement. This supports canonical reads without claiming equivalence.

## Migrations requiring data interpretation

### Operational roles

Do not replace an operational role record with a `gufo:Role` type assertion. Create a `cac-core:RoleAssignment`, link its bearer through `roleBearer`, link the source record through `describesRoleAssignment`, and add a distinct classifier through `roleClassifier` only when the source supports that interpretation.

### Operational phases

Do not replace a phase occurrence with a `gufo:Phase` class. Preserve each historical occurrence as its own node, connect it to its subject through `isPhaseOf`, and order occurrences with `precedes`. Use a distinct `gufo:Phase` OWL class through `realizesPhaseClassifier` only when classification is required.

### Custody history

Custodial relationships and temporary/emergency arrangements are not phase occurrences. Preserve the relationship as an enduring entity and represent its changing history with `CustodyState` nodes.

### Membership tiers

Treat `MembershipTier` as a controlled concept referenced through `hasMembershipTier`. Do not infer that the tier itself is an access-control system, hierarchy object, role, or phase.

## Forbidden compatibility axioms

The proposal intentionally does not publish:

- `owl:equivalentClass` between operational CAC role/phase classes and gUFO classifier classes;
- `rdfs:subClassOf gufo:Role` for `cac-core:Role`;
- `rdfs:subClassOf gufo:Phase` for `cac-core:Phase`;
- class equivalence between `CustodialRelationship` and `CustodyState`;
- class equivalence between `MembershipTier` and operational access-control classes.

Consumers that relied on these inferences need an explicit transformation reviewed against source meaning.
