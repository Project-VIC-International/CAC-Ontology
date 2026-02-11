# Run Report: NDFL Isbell Sentencing Press Release

## Phase 0: Setup + Guardrails

### Working Assumptions

1. **caseId**: `ndfl-isbell-sentencing`
2. **Document type**: Federal sentencing press release (DOJ USAO-NDFL)
3. **Scope**: IN-SCOPE (federal prosecution, sentencing, CSAM production, child exploitation)
4. **Primary modules to use**:
   - `cacontology-sentencing` - sentencing terms (prison, supervised release, etc.)
   - `cacontology-multi` - multi-jurisdictional investigation (TPD + HSI)
   - `cacontology-registry` - sex offender registration
   - `cacontology-core` - roles (offender, victim)
   - UCO/CASE foundation - persons, organizations, actions
5. **No new CAC terms required** - all concepts map to existing terms
6. **Privacy note**: Victim is referred to only as "minor victim" - no identifying information
7. **Defendant fully named** in public press release (Ryan Isbell)

### Existing Terms Found (Search-First Sweep)

| Existing Term | Namespace | Will Use For |
|---------------|-----------|--------------|
| `uco-identity:Person` | UCO | Defendant, victim, prosecutors, agents |
| `cacontology:OffenderRole` | Core | Defendant's role |
| `cacontology:VictimRole` | Core | Minor victim's role |
| `cacontology-sentencing:PrisonSentence` | Sentencing | 20-year prison term |
| `cacontology-sentencing:SupervisedRelease` | Sentencing | 15-year supervised release |
| `cacontology-sentencing:MonetaryPenalty` | Sentencing | Restitution order |
| `cacontology-sentencing:ProsecutorRole` | Sentencing | AUSA Stephen Kunz |
| `cacontology-sentencing:DefendantRole` | Sentencing | Ryan Isbell |
| `cacontology-sentencing:SentencingHearing` | Sentencing | Sentencing event |
| `cacontology-multi:LocalAgency` | Multi-Jurisdiction | Tallahassee PD |
| `cacontology-multi:FederalAgency` | Multi-Jurisdiction | HSI |
| `cacontology-registry:RegistrationRequirement` | Registry | Sex offender registration |
| `investigation:Authorization` | CASE | Arrest warrant |
| `investigation:InvestigativeAction` | CASE | Investigation actions |

---

## Phase 1: Concept Extraction + Mapping

### Concept Inventory Table

| Concept | Category | Source Quote (lines) | Evidence Pointer | Confidence | Modeling Approach |
|---------|----------|---------------------|------------------|------------|-------------------|
| Ryan Isbell | Person/Offender | "Ryan Isbell, 36, of Tallahassee, Florida" (line 7) | normalized.txt:7 | HIGH | REUSE: uco-identity:Person + cacontology:OffenderRole |
| 20-year prison sentence | Sentence | "sentenced to 20 years in federal prison" (line 7) | normalized.txt:7 | HIGH | REUSE: cacontology-sentencing:PrisonSentence |
| 15-year supervised release | Sentence | "15-year term of supervised release" (line 15) | normalized.txt:15 | HIGH | REUSE: cacontology-sentencing:SupervisedRelease |
| CSAM production charge | Charge | "pleading guilty to producing child pornography" (line 7) | normalized.txt:7 | HIGH | REUSE: cacontology-sentencing:FederalCharge (18 USC 2251) |
| Tallahassee Police Department | Organization | "Tallahassee Police Department received reports" (line 11) | normalized.txt:11 | HIGH | REUSE: cacontology-multi:LocalAgency |
| HSI Tallahassee | Organization | "Homeland Security Investigations" (line 13, 17) | normalized.txt:13,17 | HIGH | REUSE: cacontology-multi:FederalAgency |
| USAO Northern District of Florida | Organization | "U.S. Attorney's Office" (line 4) | normalized.txt:4 | HIGH | REUSE: uco-identity:Organization |
| U.S. Attorney Jason R. Heekin | Person | "announced by U.S. Attorney Jason R. Heekin" (line 7) | normalized.txt:7 | HIGH | REUSE: uco-identity:Person + cacontology-sentencing:ProsecutorRole |
| AUSA Stephen Kunz | Person | "prosecuted by Assistant United States Attorney Stephen Kunz" (line 17) | normalized.txt:17 | HIGH | REUSE: uco-identity:Person + cacontology-sentencing:ProsecutorRole |
| ASAC David Pezzutti | Person | "Assistant Special Agent in Charge David Pezzutti" (line 13) | normalized.txt:13 | HIGH | REUSE: uco-identity:Person |
| Minor victim | Person/Victim | "depicting a minor victim" (line 11) | normalized.txt:11 | HIGH | REUSE: uco-identity:Person + cacontology:VictimRole (anonymized) |
| Electronic devices seized | Evidence | "seized multiple electronic devices" (line 11) | normalized.txt:11 | HIGH | REUSE: uco-observable:Device |
| Social media account | Evidence | "defendant's social media account" (line 11) | normalized.txt:11 | HIGH | REUSE: uco-observable:Account |
| November 2020 arrest warrant | Authorization | "execution of a November 2020 arrest warrant" (line 11) | normalized.txt:11 | HIGH | REUSE: investigation:Authorization |
| Restitution order | Sentence | "ordered to pay restitution to the victim" (line 15) | normalized.txt:15 | HIGH | REUSE: cacontology-sentencing:MonetaryPenalty |
| Sex offender registration | Requirement | "required to register as a sex offender" (line 15) | normalized.txt:15 | HIGH | REUSE: cacontology-registry:RegistrationRequirement |
| Project Safe Childhood | Initiative | "part of Project Safe Childhood" (line 19) | normalized.txt:19 | HIGH | REUSE: uco-identity:Organization |
| Forensic examination | Action | "forensic examination of the devices" (line 11) | normalized.txt:11 | HIGH | REUSE: investigation:ForensicAction |

### Mapping Table

| Document Concept | Ontology Term | Facets Required | Rationale |
|------------------|---------------|-----------------|-----------|
| Ryan Isbell (defendant) | `uco-identity:Person` + `cacontology-sentencing:DefendantRole` | BirthInformationFacet (age 36) | Existing person + role pattern |
| 20-year prison sentence | `cacontology-sentencing:PrisonSentence` | None (use properties) | Exact match in sentencing module |
| 15-year supervised release | `cacontology-sentencing:SupervisedRelease` | None | Exact match in sentencing module |
| CSAM production | `cacontology-sentencing:FederalCSAMProduction` | None | Federal charge class exists |
| TPD | `cacontology-multi:LocalAgency` | None | Local law enforcement |
| HSI | `cacontology-multi:FederalAgency` | None | Federal law enforcement |
| Electronic devices | `uco-observable:Device` | DeviceFacet | UCO pattern for devices |
| Arrest warrant | `investigation:Authorization` | None | CASE authorization pattern |
| Forensic exam | `investigation:ForensicAction` | None | CASE investigative action |

---

## Phase 2: Implementation Plan

### New/Updated Terms Required
**NONE** - All concepts map to existing CAC/UCO/CASE terms.

### Risk List
1. **SHACL shape violations**: Minimal risk - using well-tested existing classes
2. **Domain/range violations**: Minimal risk - following established patterns
3. **Connectivity risk**: MITIGATED - using statement/listing actions to ground all entities
4. **Provenance gaps**: MITIGATED - all entities traced to normalized.txt lines

### Governance Gate Queue
- **No new terms** pending approval
- **No SKOS mappings** required
- **Sensitive entities**: Minor victim modeled anonymously (no PII)

---

## File Changes Summary

| File | Change | Status |
|------|--------|--------|
| `collected_sources/ndfl-isbell-sentencing/normalized.txt` | Created | Complete |
| `collected_sources/ndfl-isbell-sentencing/manifest.yaml` | Created | Complete |
| `collected_sources/ndfl-isbell-sentencing/duplicate_detection_report.md` | Created | Complete |
| `examples_knowledge_graphs/ndfl-isbell-sentencing-skeleton.ttl` | Created | Complete |
| `examples_knowledge_graphs/ndfl-isbell-sentencing-example.ttl` | Created | Pending |
| `example_SPARQL_queries/ndfl-isbell-sentencing-analytics.rq` | Created | Pending |

---

## Metrics Summary (Pre-Validation)

| Metric | Target | Expected |
|--------|--------|----------|
| UUID coverage | 100% | 100% (all UUIDv5) |
| Provenance completeness | 100% | 100% |
| Facet coverage | >50% | ~60% |
| Graph connectivity | 0 isolates | 0 (all entities grounded via actions) |
| Term citation coverage | N/A | No new terms |

