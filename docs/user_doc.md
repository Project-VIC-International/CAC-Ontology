# CAC Ontology Family - User Documentation
One or more of these ontologies can be used to develop unique software applications for users that are then foundationally interoperable with other applications built on this family of ontologies.

This family of ontologies seeks to implement semantically clear information models that reflect the information, information relationships, workflows, and events that a Crimes Against Children Investigator uses or may use in the future. Each ontology represents a unique application domain within investigators'and prosecutors' discourse. This family of ontologies seeks to be universal and it is heavily informed by public documentation in the form of press releases from law enforcement agencies and prosecutor's offices, and high-quality publications from nonprofits that are active in safeguarding children. Finally, this family of ontologies seeks to use modern language as much as possible to reflect the unifying efforts of the CAC community, but there may be language in these ontologies that are more reflective of a certain country when that language is still professionally used.

## Quick Start

### Prerequisites
- Basic understanding of RDF and ontologies
- Familiarity with Turtle syntax
- Understanding of UCO (Unified Cyber Ontology and CASE Ontology)
- Understanding of gUFO (Unified Foundational Ontology) concepts
- Python 3.9+ for validation tools

### Installation
1. Clone the repository:
```bash
git clone https://github.com/Project-VIC-International/CAC-Ontology.git
cd CAC-Ontology
```

2. Install dependencies:
```bash
pip install -r requirements.txt
# requirements.txt contents:
# rdflib>=6.3.2
# pyshacl>=0.20.0
# robotframework>=6.1.1
# robotframework-rdflib>=0.1.0
# scikit-learn>=1.3.0  # NEW: For AI integration
# networkx>=3.0        # NEW: For network analysis
```

3. Start the validation server:
```bash
docker compose -f testing/docker-compose.yaml up -d
```

4. Load gUFO-enhanced ontologies:
```bash
# Load core ontology with gUFO integration
curl -X POST http://localhost:3030/cac/data \
  --data-binary @ontology/cacontology-core.ttl \
  --header "Content-Type: text/turtle"

# Load temporal framework
curl -X POST http://localhost:3030/cac/data \
  --data-binary @ontology/cacontology-temporal.ttl \
  --header "Content-Type: text/turtle"

# Load integration patterns
curl -X POST http://localhost:3030/cac/data \
  --data-binary @ontology/cacontology-integration-patterns.ttl \
  --header "Content-Type: text/turtle"
```

## Semantic Spine (v3.0.0)

Version 3.0.0 introduces the **semantic spine** (`cac-core:` namespace, `https://cacontology.projectvic.org/core#`), a stable top-level class hierarchy organized by ontological kind. The spine provides enduring anchor classes—`cac-core:Entity`, `cac-core:EnduringEntity`, `cac-core:Event`, `cac-core:Situation`, `cac-core:Role`, `cac-core:Phase`, `cac-core:Artifact`, and `cac-core:AssessmentResult`—that every CAC domain module inherits from.

When creating new instances, use the CAC domain class (e.g., `cacontology:CACInvestigation`, `cacontology:InvestigatorRole`) rather than referencing gUFO types like `gufo:Event` or `gufo:Situation` directly. The domain classes already carry the correct spine (and foundational) superclass chain, so explicit `rdf:type gufo:Event` assertions are no longer needed.

## Core Concepts

> **Note on namespaces:** Examples in this document use `cacontology-*` prefixes and `https://cacontology.projectvic.org/{module-name}#` IRIs, matching the CAC Ontology v3.x namespace convention. The `cac-core:` prefix (`https://cacontology.projectvic.org/core#`) refers to the semantic spine. Core investigation classes use the `cacontology:` prefix (`https://cacontology.projectvic.org#`).

### 1. Hotline Reports
We use hotline reports as a foundation of the ontology. They represent the initial reports of potential child exploitation material.

```turtle
@base <https://example.org/hotline/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix uco-core: <https://ontology.unifiedcyberontology.org/uco/core/> .
@prefix uco-observable: <https://ontology.unifiedcyberontology.org/uco/observable/> .
@prefix hotline: <https://cacontology.projectvic.org/hotlines#> .

hotline:report-001 a hotline:PublicReport ;
    hotline:reportedBy hotline:reporter-001 ;
    hotline:receivedBy hotline:org-001 ;
    hotline:hasEvidence hotline:evidence-001 ;
    hotline:intakeChannel hotline:web-form ;
    hotline:status hotline:status-closed .
```

### 2. Evidence Items
Evidence items represent the material reported to hotlines.

```turtle
hotline:evidence-001 a hotline:ImageEvidence ;
    hotline:firstSeen "2024-03-20T10:00:00Z"^^xsd:dateTime ;
    hotline:foundAtURL hotline:url-001 .
```

### 3. Actions
Actions represent the steps taken in processing reports.

```turtle
hotline:action-001 a hotline:ReportReviewAction ;
    hotline:performedBy hotline:analyst-001 ;
    hotline:startTime "2024-03-20T10:05:00Z"^^xsd:dateTime ;
    hotline:endTime "2024-03-20T10:10:00Z"^^xsd:dateTime .
```

### 4. **NEW: gUFO-Enhanced Investigation Modeling**

The CAC ontology family now includes comprehensive gUFO integration for enhanced semantic precision and temporal modeling.

#### 4.1 Investigation Phases with gUFO

```turtle
@prefix cacontology: <https://cacontology.projectvic.org#> .
@prefix cac-core: <https://cacontology.projectvic.org/core#> .
@prefix cacontology-temporal: <https://cacontology.projectvic.org/temporal#> .

# Investigation with spine-backed phases
example:Investigation001 rdf:type cacontology:CACInvestigation ;
    cacontology:currentPhase example:ResolutionPhase001 ;
    cacontology:hasPhase example:InitialPhase001, example:AnalysisPhase001 .

# Initial phase (subclass of cac-core:Phase) with temporal constraints
example:InitialPhase001 rdf:type cacontology:InitialPhase ;
    cacontology:hasPhaseBeginPoint "2025-01-01T08:00:00Z"^^xsd:dateTimeStamp ;
    cacontology:hasPhaseEndPoint "2025-01-03T17:00:00Z"^^xsd:dateTimeStamp ;
    cacontology:phaseDuration "P2DT9H"^^xsd:duration ;
    cacontology-temporal:phaseEfficiency "1.2"^^xsd:decimal .

# Analysis phase with dependencies
example:AnalysisPhase001 rdf:type cacontology:AnalysisPhase ;
    cacontology-temporal:hasPrerequisitePhase example:InitialPhase001 ;
    cacontology:hasPhaseBeginPoint "2025-01-03T17:00:00Z"^^xsd:dateTimeStamp .
```

#### 4.2 Enhanced Role Modeling with Anti-Rigidity

```turtle
# Person with multiple roles (prevented conflicts)
example:Witness_Parent cacontology:playsRole example:WitnessRole001 ;
    cacontology:playsRole example:InformantRole001 .

# Investigation role (subclass of cac-core:Role) with temporal boundaries
example:InvestigatorRole001 rdf:type cacontology:InvestigatorRole ;
    cacontology:hasRoleBeginPoint "2025-01-01T08:00:00Z"^^xsd:dateTimeStamp ;
    cacontology:participatesInInvestigation example:Investigation001 .

# Role conflict prevention (automatic validation)
# This would be INVALID and caught by SHACL validation:
# example:Person001 cacontology:playsRole example:VictimRole001 ;
#                   cacontology:playsRole example:OffenderRole001 .  # CONFLICT!
```

#### 4.3 Event vs Situation Distinction

```turtle
@prefix cacontology: <https://cacontology.projectvic.org#> .
@prefix cac-core: <https://cacontology.projectvic.org/core#> .
@prefix gufo: <http://purl.org/nemo/gufo#> .

# Concrete investigation actions as Events (inherits cac-core:Event via spine)
example:SearchWarrantExecution001 rdf:type cac-core:InvestigativeAction ;
    gufo:hasBeginPointInXSDDateTimeStamp "2025-01-05T06:00:00Z"^^xsd:dateTimeStamp ;
    gufo:hasEndPointInXSDDateTimeStamp "2025-01-05T08:30:00Z"^^xsd:dateTimeStamp .

# Ongoing investigation state as Situation (inherits cac-core:Situation via spine)
example:ActiveInvestigationSituation001 rdf:type cacontology:InvestigationLifecycleSituation ;
    gufo:hasBeginPointInXSDDateTimeStamp "2025-01-01T08:00:00Z"^^xsd:dateTimeStamp .
```

#### 4.4 Temporal Investigation Lifecycle

```turtle
@prefix cacontology: <https://cacontology.projectvic.org#> .
@prefix cacontology-temporal: <https://cacontology.projectvic.org/temporal#> .

# Investigation with suspension/resumption
example:Investigation002 rdf:type cacontology:CACInvestigation ;
    cacontology-temporal:hasTimeToResolution "P45D"^^xsd:duration ;
    cacontology-temporal:hasActiveDuration "P38D"^^xsd:duration ;
    cacontology-temporal:hasSuspendedDuration "P7D"^^xsd:duration ;
    cacontology-temporal:urgencyLevel "4"^^xsd:nonNegativeInteger .

# Suspension event
example:Suspension001 rdf:type cacontology-temporal:SuspensionEvent ;
    cacontology-temporal:suspends example:Investigation002 ;
    cacontology-temporal:suspensionReason "pending_court_order" ;
    gufo:hasBeginPointInXSDDateTimeStamp "2025-01-15T16:00:00Z"^^xsd:dateTimeStamp .

# Resumption event  
example:Resumption001 rdf:type cacontology-temporal:ResumptionEvent ;
    cacontology-temporal:resumes example:Investigation002 ;
    cacontology-temporal:resumptionTrigger "court_order_received" ;
    gufo:hasBeginPointInXSDDateTimeStamp "2025-01-22T09:00:00Z"^^xsd:dateTimeStamp .
```

#### 4.5 Multi-Jurisdiction Coordination

```turtle
# Complex multi-jurisdiction scenario (inherits cac-core:Situation via spine)
example:MultiJurisdictionCoordination001 rdf:type cacontology-temporal:MultiJurisdictionCoordinationSituation ;
    cacontology-temporal:coordinatesInvestigations example:Investigation001, example:Investigation003 ;
    cacontology-temporal:involvesJurisdictions "US-CA", "US-TX", "CA-ON" ;
    gufo:hasBeginPointInXSDDateTimeStamp "2025-01-10T14:00:00Z"^^xsd:dateTimeStamp .

# Synchronization event
example:JurisdictionSync001 rdf:type cacontology-temporal:JurisdictionSynchronizationEvent ;
    cacontology-temporal:synchronizes example:MultiJurisdictionCoordination001 ;
    cacontology-temporal:syncType "evidence_sharing" ;
    gufo:hasBeginPointInXSDDateTimeStamp "2025-01-12T10:00:00Z"^^xsd:dateTimeStamp .
```

### 5. Athletic Coaching Exploitation
The ontology includes comprehensive modeling of athletic coaching exploitation patterns.

```turtle
@prefix cacontology-athletic: <https://cacontology.projectvic.org/athletic#> .
@prefix uco-identity: <https://ontology.unifiedcyberontology.org/uco/identity/> .

# Athletic coaching exploitation case
<https://example.org/exploitation/coach-case> a cacontology-athletic:DualCoachingRoleExploitation ;
    cacontology-athletic:sportType "baseball" ;
    cacontology-athletic:teamType "travel" ;
    cacontology-athletic:practiceFrequency "3"^^xsd:decimal ;
    cacontology-athletic:teamSize "7"^^xsd:nonNegativeInteger ;
    cacontology-athletic:multipleRoles "2"^^xsd:nonNegativeInteger ;
    uco-core:startTime "2023-01-01T00:00:00Z"^^xsd:dateTime ;
    uco-core:endTime "2024-08-01T00:00:00Z"^^xsd:dateTime .

# Coach with dual roles
<https://example.org/person/coach> a uco-identity:Person ;
    uco-core:name "Athletic Coach" ;
    cacontology-athletic:holdsCoachingRole <https://example.org/role/travel-coach> ;
    cacontology-athletic:holdsCoachingRole <https://example.org/role/school-coach> .

# Travel team coaching role
<https://example.org/role/travel-coach> a cacontology-athletic:TravelTeamCoachRole ;
    cacontology-athletic:coachingExperience "5"^^xsd:decimal ;
    cacontology-athletic:ageGroupCoached "12-14" ;
    cacontology-athletic:teamSize "15"^^xsd:nonNegativeInteger .

# Physical training coercion
<https://example.org/coercion/conditioning> a cacontology-athletic:ConditioningCoercion ;
    cacontology-athletic:conditioningType "running_drills" ;
    cacontology-athletic:exhaustionLevel "severe" .

# Link exploitation to coercion methods
<https://example.org/exploitation/coach-case> cacontology-athletic:usesPhysicalTraining <https://example.org/coercion/conditioning> .
```

## API Reference

### 1. JSON-LD Context
Context files live in `/contexts/`, versioned alongside ontology:

```json
{
  "@context": "contexts/cacontology-hotlines.jsonld",
  "@type": "HotlineReport",
  "reportedBy": {
    "@type": "ReporterRole",
    "isAnonymous": true
  }
}
```

> **Legacy note:** Earlier versions used `https://ontology.unifiedcyberontology.org/hotlines/2025/core/contexts/hotlines-core.jsonld` as the context URL. That URL is retained for backward compatibility but new implementations should use the local context file above.

#### 1.1 **NEW: gUFO-Enhanced JSON-LD Context**

```json
{
  "@context": [
    "contexts/cacontology-core.jsonld",
    "contexts/cac-core-spine.jsonld"
  ],
  "@type": "Investigation",
  "inPhase": {
    "@type": "InitialPhase",
    "hasPhaseBeginPoint": "2025-01-01T08:00:00Z",
    "phaseDuration": "P2DT9H"
  },
  "hasRole": [{
    "@type": "InvestigatorRole",
    "hasRoleBeginPoint": "2025-01-01T08:00:00Z"
  }]
}
```

For athletic exploitation cases:
```json
{
  "@context": [
    "contexts/cacontology-core.jsonld",
    "contexts/cacontology-athletic-exploitation.jsonld"
  ],
  "@type": "AthleticCoachingExploitation",
  "sportType": "baseball",
  "teamType": "travel",
  "practiceFrequency": 3,
  "teamSize": 7,
  "usesPhysicalTraining": {
    "@type": "ConditioningCoercion",
    "conditioningType": "running_drills",
    "exhaustionLevel": "severe"
  }
}
```

For local development:
```json
{
  "@context": "contexts/cacontology-hotlines.jsonld",
  "@type": "HotlineReport",
  "reportedBy": {
    "@type": "ReporterRole",
    "isAnonymous": true
  }
}
```

### 2. SPARQL Queries

#### 2.1 Read Operations
```sparql
# Find All Reports
SELECT ?report
WHERE {
    ?report a hotline:HotlineReport .
}

# Find Reports by Status
SELECT ?report
WHERE {
    ?report a hotline:HotlineReport ;
            hotline:status hotline:status-new .
}

# Find Athletic Coaching Exploitation Cases
PREFIX cacontology-athletic: <https://cacontology.projectvic.org/athletic#>
SELECT ?exploitation ?sportType ?teamSize
WHERE {
    ?exploitation a cacontology-athletic:AthleticCoachingExploitation ;
                  cacontology-athletic:sportType ?sportType ;
                  cacontology-athletic:teamSize ?teamSize .
}

# Find Coaches with Multiple Roles
PREFIX cacontology-athletic: <https://cacontology.projectvic.org/athletic#>
SELECT ?coach ?roleCount
WHERE {
    ?coach cacontology-athletic:holdsCoachingRole ?role .
    {
        SELECT ?coach (COUNT(?role) AS ?roleCount)
        WHERE {
            ?coach cacontology-athletic:holdsCoachingRole ?role .
        }
        GROUP BY ?coach
        HAVING (?roleCount > 1)
    }
}
```

#### 2.2 **NEW: gUFO-Enhanced SPARQL Queries**

```sparql
# Investigation Phase Performance Analytics
PREFIX cacontology: <https://cacontology.projectvic.org#>
PREFIX cacontology-temporal: <https://cacontology.projectvic.org/temporal#>
PREFIX gufo: <http://purl.org/nemo/gufo#>

SELECT ?phase_type ?avg_duration ?efficiency_score ?case_count WHERE {
  {
    SELECT ?phase_type 
           (AVG(?duration_hours) as ?avg_duration)
           (AVG(?efficiency) as ?efficiency_score)
           (COUNT(?phase) as ?case_count) WHERE {
      ?phase rdf:type ?phase_type ;
             cacontology:phaseDuration ?duration ;
             cacontology-temporal:phaseEfficiency ?efficiency .
      
      # Convert duration to hours for analysis
      BIND(
        IF(CONTAINS(STR(?duration), "PT"), 
           xsd:decimal(REPLACE(REPLACE(STR(?duration), "PT", ""), "H.*", "")),
           xsd:decimal(REPLACE(REPLACE(STR(?duration), "P", ""), "D.*", "")) * 24
        ) as ?duration_hours
      )
      
      FILTER(?phase_type IN (
        cacontology:InitialPhase, cacontology:AnalysisPhase, 
        cacontology:LegalProcessPhase, cacontology:EvidencePhase,
        cacontology:ConclusionPhase
      ))
    }
    GROUP BY ?phase_type
  }
}
ORDER BY ?avg_duration

# Role Conflict Detection
PREFIX cacontology: <https://cacontology.projectvic.org#>

SELECT ?person ?conflicting_roles ?investigation ?conflict_severity WHERE {
  ?person cacontology:playsRole ?role1 ;
          cacontology:playsRole ?role2 .
  
  ?role1 cacontology:participatesInInvestigation ?investigation .
  ?role2 cacontology:participatesInInvestigation ?investigation .
  
  # Detect conflicting role combinations
  FILTER(
    (?role1 = cacontology:VictimRole && ?role2 = cacontology:OffenderRole) ||
    (?role1 = cacontology:OffenderRole && ?role2 = cacontology:VictimRole) ||
    (?role1 = cacontology:InvestigatorRole && ?role2 = cacontology:OffenderRole)
  )
  
  BIND(CONCAT(STR(?role1), " + ", STR(?role2)) as ?conflicting_roles)
  BIND("CRITICAL" as ?conflict_severity)
}

# Temporal Investigation Pattern Analysis
PREFIX cacontology: <https://cacontology.projectvic.org#>
PREFIX cacontology-temporal: <https://cacontology.projectvic.org/temporal#>

SELECT ?pattern_type ?frequency ?avg_success_rate WHERE {
  {
    SELECT ?pattern_type 
           (COUNT(?inv) as ?frequency)
           (AVG(?completion_rate) as ?avg_success_rate) WHERE {
      
      ?inv rdf:type cacontology:CACInvestigation ;
           cacontology-temporal:hasTimeToResolution ?resolution_time ;
           cacontology:hasPhase ?phase .
      
      ?phase cacontology-temporal:phaseCompletionRate ?completion_rate .
      
      # Convert duration to days
      BIND(xsd:decimal(REPLACE(REPLACE(STR(?resolution_time), "P", ""), "D.*", "")) as ?total_duration)
      
      # Classify investigation patterns
      BIND(
        IF(?total_duration <= 30, "Fast Track (≤30 days)",
        IF(?total_duration <= 90, "Standard (31-90 days)",
        IF(?total_duration <= 180, "Extended (91-180 days)",
        "Complex (>180 days)"))) as ?pattern_type
      )
    }
    GROUP BY ?pattern_type
  }
}
ORDER BY ?avg_success_rate

# Advanced Multi-Jurisdiction Analytics
PREFIX cacontology: <https://cacontology.projectvic.org#>
PREFIX cacontology-temporal: <https://cacontology.projectvic.org/temporal#>
PREFIX gufo: <http://purl.org/nemo/gufo#>

SELECT ?coordination_type ?jurisdiction_count ?avg_duration ?success_rate WHERE {
  {
    SELECT ?coordination_type 
           (AVG(?jurisdiction_count) as ?jurisdiction_count)
           (AVG(?duration_days) as ?avg_duration)
           (AVG(?completion_rate) as ?success_rate) WHERE {
      
      ?situation rdf:type cacontology-temporal:MultiJurisdictionCoordinationSituation ;
                 gufo:hasBeginPointInXSDDateTimeStamp ?begin ;
                 gufo:hasEndPointInXSDDateTimeStamp ?end .
      
      ?investigation cacontology-temporal:hasTimeToResolution ?total_time ;
                     cacontology:hasPhase ?phase .
      
      ?phase cacontology-temporal:phaseCompletionRate ?completion_rate .
      
      # Calculate coordination duration
      BIND((xsd:dateTime(?end) - xsd:dateTime(?begin)) / xsd:dayTimeDuration("P1D") as ?duration_days)
      
      # Classify coordination type by complexity
      BIND(
        IF(?duration_days <= 7, "Bi-Jurisdictional",
        IF(?duration_days <= 21, "Multi-State",
        IF(?duration_days <= 45, "Regional",
        "National/International"))) as ?coordination_type
      )
    }
    GROUP BY ?coordination_type
  }
}
ORDER BY ?jurisdiction_count
```

## Comprehensive Usage Examples

### 1. Creating Reports

#### 1.1 Basic Report
```turtle
hotline:report-002 a hotline:PublicReport ;
    hotline:reportedBy [
        a hotline:ReporterRole ;
        hotline:isAnonymous true
    ] ;
    hotline:receivedBy hotline:org-001 ;
    hotline:hasEvidence hotline:evidence-002 ;
    hotline:intakeChannel hotline:web-form ;
    hotline:status hotline:status-new .
```

#### 1.2 ESP Report
```turtle
hotline:report-003 a hotline:ESPReport ;
    hotline:reportedBy hotline:automated-reporter-001 ;
    hotline:receivedBy hotline:org-001 ;
    hotline:hasEvidence hotline:evidence-003 ;
    hotline:intakeChannel hotline:api ;
    hotline:status hotline:status-new .
```

### 2. Managing Evidence

#### 2.1 Image Evidence
```turtle
hotline:evidence-002 a hotline:ImageEvidence ;
    hotline:firstSeen "2024-03-20T11:00:00Z"^^xsd:dateTime ;
    hotline:foundAtURL hotline:url-002 ;
    uco-observable:hash [
        a uco-observable:Hash ;
        uco-observable:hashValue "abc123"^^xsd:string ;
        uco-observable:hashMethod "SHA-256"
    ] .
```

#### 2.2 URL Evidence
```turtle
hotline:evidence-003 a hotline:URLReference ;
    hotline:firstSeen "2024-03-20T12:00:00Z"^^xsd:dateTime ;
    hotline:foundAtURL hotline:url-003 .
```

### 3. Athletic Coaching Exploitation Cases

#### 3.1 Complete Athletic Coaching Case
```turtle
@prefix cacontology-athletic: <https://cacontology.projectvic.org/athletic#> .
@prefix uco-identity: <https://ontology.unifiedcyberontology.org/uco/identity/> .
@prefix uco-location: <https://ontology.unifiedcyberontology.org/uco/location/> .

# Main exploitation case
<https://example.org/case/athletic-001> a cacontology-athletic:DualCoachingRoleExploitation ;
    rdfs:label "Travel Team and School Coach Exploitation"@en ;
    cacontology-athletic:sportType "baseball" ;
    cacontology-athletic:teamType "travel" ;
    cacontology-athletic:practiceFrequency "3"^^xsd:decimal ;
    cacontology-athletic:seasonDuration "18"^^xsd:decimal ;
    cacontology-athletic:teamSize "7"^^xsd:nonNegativeInteger ;
    cacontology-athletic:multipleRoles "2"^^xsd:nonNegativeInteger ;
    uco-core:startTime "2023-01-01T00:00:00Z"^^xsd:dateTime ;
    uco-core:endTime "2024-08-01T00:00:00Z"^^xsd:dateTime .

# Perpetrator with coaching roles
<https://example.org/person/coach-001> a uco-identity:Person ;
    uco-core:name "Athletic Coach" ;
    uco-observable:age "31"^^xsd:nonNegativeInteger ;
    cacontology-athletic:holdsCoachingRole <https://example.org/role/travel-coach> ;
    cacontology-athletic:holdsCoachingRole <https://example.org/role/school-coach> .

# Travel team coaching role
<https://example.org/role/travel-coach> a cacontology-athletic:TravelTeamCoachRole ;
    uco-core:name "Travel Team Coach" ;
    cacontology-athletic:coachingExperience "5"^^xsd:decimal ;
    cacontology-athletic:ageGroupCoached "12-14" ;
    cacontology-athletic:teamSize "15"^^xsd:nonNegativeInteger .

# School coaching role
<https://example.org/role/school-coach> a cacontology-athletic:SchoolAthleticCoachRole ;
    uco-core:name "School Head Coach" ;
    cacontology-athletic:coachingExperience "5"^^xsd:decimal ;
    cacontology-athletic:institutionalAffiliation "School Athletic Program" ;
    cacontology-athletic:ageGroupCoached "12-18" .

# Physical training coercion
<https://example.org/coercion/conditioning-001> a cacontology-athletic:ConditioningCoercion ;
    rdfs:label "Conditioning Exercise Exposure Coercion"@en ;
    cacontology-athletic:conditioningType "running_drills" ;
    cacontology-athletic:exhaustionLevel "severe" .

# Team membership threats
<https://example.org/coercion/membership-001> a cacontology-athletic:TeamMembershipCoercion ;
    rdfs:label "Team Membership Threat Coercion"@en ;
    cacontology-athletic:threatSpecificity "specific" .

# Athletic facilities
<https://example.org/location/gym-001> a uco-location:Location ;
    uco-core:name "School Gymnasium" ;
    uco-location:locality "Brooklyn" ;
    uco-location:region "New York" .

<https://example.org/location/field-001> a uco-location:Location ;
    uco-core:name "Baseball Fields" ;
    uco-location:locality "Brooklyn" ;
    uco-location:region "New York" .

# Facility exploitation
<https://example.org/facility/gym-exploitation> a cacontology-athletic:GymExploitation ;
    rdfs:label "Gymnasium Exploitation"@en ;
    cacontology-athletic:facilityType "gym" .

<https://example.org/facility/field-exploitation> a cacontology-athletic:AthleticFieldExploitation ;
    rdfs:label "Baseball Field Exploitation"@en ;
    cacontology-athletic:facilityType "field" .

# Discovery through parent network
<https://example.org/discovery/parent-rumors> a cacontology-athletic:RumorCirculationDiscovery ;
    rdfs:label "Parent Network Rumor Circulation"@en ;
    uco-core:startTime "2024-07-01T00:00:00Z"^^xsd:dateTime ;
    cacontology-athletic:parentNetworkSize "10"^^xsd:nonNegativeInteger ;
    cacontology-athletic:rumorCirculationDuration "30"^^xsd:decimal .

# Link relationships
<https://example.org/case/athletic-001> cacontology-athletic:exploitsAthleticAuthority <https://example.org/role/travel-coach> ;
    cacontology-athletic:exploitsAthleticAuthority <https://example.org/role/school-coach> ;
    cacontology-athletic:usesPhysicalTraining <https://example.org/coercion/conditioning-001> ;
    cacontology-athletic:employsConditioningCoercion <https://example.org/coercion/membership-001> ;
    cacontology-athletic:occursInFacility <https://example.org/location/gym-001> ;
    cacontology-athletic:occursInFacility <https://example.org/location/field-001> ;
    cacontology-athletic:discoveredByParents <https://example.org/discovery/parent-rumors> .
```

### 4. Cross-Border Scenarios

#### 4.1 Canadian Report to Spanish LEA
```turtle
hotline:report-004 a hotline:PublicReport ;
    hotline:reportedBy hotline:reporter-ca-001 ;
    hotline:receivedBy hotline:org-ca-001 ;
    hotline:hasEvidence hotline:evidence-004 ;
    hotline:triggersAction hotline:action-004 .

hotline:action-004 a hotline:ForwardToLEAction ;
    hotline:performedBy hotline:analyst-ca-001 ;
    hotline:forwardsTo hotline:org-es-001 ;
    hotline:startTime "2024-03-20T13:00:00Z"^^xsd:dateTime ;
    hotline:endTime "2024-03-20T13:05:00Z"^^xsd:dateTime .
```

### 5. CAC Investigation Lifecycle

#### 5.1 Complete Investigation
```turtle
@prefix cacontology: <https://cacontology.projectvic.org#> .

cacontology:investigation-001 a cacontology:CACInvestigation ;
    cacontology:hasStep cacontology:receive-tip-001, cacontology:review-tip-001, cacontology:legal-process-001 ;
    cacontology:hasReport hotline:report-004 .

cacontology:receive-tip-001 a cacontology:ReceiveCybertipAction ;
    cacontology:nextStep cacontology:review-tip-001 ;
    uco-action:startTime "2024-03-20T13:00:00Z"^^xsd:dateTime .

cacontology:review-tip-001 a cacontology:ReviewCybertipAction ;
    cacontology:previousStep cacontology:receive-tip-001 ;
    cacontology:nextStep cacontology:legal-process-001 ;
    uco-action:performer cacontology:analyst-001 .

cacontology:legal-process-001 a cacontology:LegalProcessAction ;
    cacontology:previousStep cacontology:review-tip-001 ;
    cacontology:targetsService cacontology:social-platform-001 ;
    cacontology:legalInstrument cacontology:search-warrant-001 .
```

### 6. Production Case Investigation

#### 6.1 CSAM Production Offense
```turtle
@prefix cacontology-production: <https://cacontology.projectvic.org/production#> .

cacontology-production:offense-001 a cacontology-production:ProductionOffense ;
    cacontology-production:productionMethod "direct_recording" ;
    cacontology-production:sessionCount 15 ;
    cacontology-production:victimCount 2 ;
    cacontology-production:producedAt cacontology-production:location-001 ;
    cacontology-production:usesEquipment cacontology-production:device-001 .

cacontology-production:producer-001 a cacontology-production:Producer ;
    cacontology-production:holdsPositionOf cacontology-production:babysitter-role ;
    cacontology-production:violatesPosition cacontology-production:trust-violation-001 .
```

### 7. Victim Impact Assessment

#### 7.1 Comprehensive Impact Assessment
```turtle
@prefix cacontology-impact: <https://cacontology.projectvic.org/victim-impact#> .

cacontology-impact:assessment-001 a cacontology-impact:ComprehensiveImpactAssessment ;
    cacontology-impact:severityLevel "severe" ;
    cacontology-impact:assessesVictim cacontology-impact:victim-001 ;
    cacontology-impact:identifiesHarm cacontology-impact:complex-trauma-001 .

cacontology-impact:complex-trauma-001 a cacontology-impact:ComplexTrauma ;
    cacontology-impact:traumaType "complex" ;
    cacontology-impact:severity "severe" ;
    cacontology-impact:manifestsAs cacontology-impact:behavioral-indicator-001, cacontology-impact:emotional-indicator-001 .

cacontology-impact:therapeutic-intervention-001 a cacontology-impact:TraumaTherapy ;
    cacontology-impact:treatmentModality "CBT" ;
    cacontology-impact:addressesHarm cacontology-impact:complex-trauma-001 ;
    cacontology-impact:treatmentOutcome "partially_successful" .
```

### 8. Task Force Operations

#### 8.1 Multi-Agency Operation
```turtle
@prefix cacontology-taskforce: <https://cacontology.projectvic.org/taskforce#> .

cacontology-taskforce:operation-001 a cacontology-taskforce:TaskForceOperation ;
    cacontology-taskforce:operationName "Operation Cyber Highway Safety Check" ;
    cacontology-taskforce:leadAgency cacontology-taskforce:arkansas-dps ;
    cacontology-taskforce:participatingAgency cacontology-taskforce:local-sheriff-001, cacontology-taskforce:fbi-field-office-001 ;
    cacontology-taskforce:arrestCount 42 ;
    cacontology-taskforce:searchWarrantCount 178 ;
    cacontology-taskforce:childrenRescued 5 .
```

### 9. Sex Offender Registry Integration

#### 9.1 Registry Compliance Monitoring
```turtle
@prefix cacontology-registry: <https://cacontology.projectvic.org/sex-offender-registry#> .

cacontology-registry:compliance-operation-001 a cacontology-registry:ComplianceMonitoringOperation ;
    cacontology-registry:visitCount 1600 ;
    cacontology-registry:complianceRate 0.95 ;
    cacontology-registry:violationCount 80 ;
    cacontology-registry:newArrestCount 12 .

cacontology-registry:offender-001 a cacontology-registry:RegisteredOffender ;
    cacontology-registry:registrationTier "Tier II" ;
    cacontology-registry:hasRegistrationRecord cacontology-registry:record-001 ;
    cacontology-registry:subjectToRestriction cacontology-registry:internet-restriction-001 .
```

### 10. International Coordination

#### 10.1 Cross-Border Investigation
```turtle
@prefix cacontology-international: <https://cacontology.projectvic.org/international#> .

cacontology-international:cross-border-001 a cacontology-international:CrossBorderInvestigation ;
    cacontology-international:originCountry "US" ;
    cacontology-international:targetCountry "UK" ;
    cacontology-international:coordinationMechanism cacontology-international:mutual-legal-assistance ;
    cacontology-international:informationShared cacontology-international:evidence-package-001 .
```

### 11. Forensic Analysis

#### 11.1 Digital Forensics Workflow
```turtle
@prefix cacontology-forensics: <https://cacontology.projectvic.org/forensics#> .

cacontology-forensics:acquisition-001 a cacontology-forensics:ForensicAcquisitionAction ;
    cacontology-forensics:acquisitionMethod "physical_imaging" ;
    cacontology-forensics:writeBlockingUsed true ;
    cacontology-forensics:evidenceSeized cacontology-forensics:mobile-device-001 ;
    cacontology-forensics:producesImage cacontology-forensics:forensic-image-001 .

cacontology-forensics:analysis-001 a cacontology-forensics:ForensicAnalysisAction ;
    cacontology-forensics:analyzesImage cacontology-forensics:forensic-image-001 ;
    cacontology-forensics:usesTool cacontology-forensics:cellebrite-tool ;
    cacontology-forensics:recoversFiles cacontology-forensics:recovered-images-001 .
```

## Advanced Query Examples

### 1. Cross-Ontology Analytics
```sparql
# Find investigations with production offenses and victim impact assessments
PREFIX cacontology: <https://cacontology.projectvic.org#>
PREFIX cacontology-production: <https://cacontology.projectvic.org/production#>
PREFIX cacontology-impact: <https://cacontology.projectvic.org/victim-impact#>

SELECT ?investigation ?offense ?assessment ?severity
WHERE {
    ?investigation a cacontology:CACInvestigation ;
                  cacontology:hasStep ?step .
    ?step a cacontology-production:ProductionOffense .
    ?offense a cacontology-production:ProductionOffense .
    ?assessment a cacontology-impact:VictimImpactAssessment ;
               cacontology-impact:severityLevel ?severity .
}
```

### 2. Task Force Performance Metrics
```sparql
# Calculate task force operation effectiveness
PREFIX cacontology-taskforce: <https://cacontology.projectvic.org/taskforce#>

SELECT ?operation ?arrestRate ?rescueRate
WHERE {
    ?operation a cacontology-taskforce:TaskForceOperation ;
              cacontology-taskforce:arrestCount ?arrests ;
              cacontology-taskforce:searchWarrantCount ?warrants ;
              cacontology-taskforce:childrenRescued ?rescued .
    BIND(?arrests / ?warrants AS ?arrestRate)
    BIND(?rescued / ?arrests AS ?rescueRate)
}
ORDER BY DESC(?arrestRate)
```

### 3. Registry Compliance Analysis
```sparql
# Find compliance violations by registry tier
PREFIX cacontology-registry: <https://cacontology.projectvic.org/sex-offender-registry#>

SELECT ?tier (COUNT(?violation) AS ?violationCount)
WHERE {
    ?offender a cacontology-registry:RegisteredOffender ;
             cacontology-registry:registrationTier ?tier ;
             cacontology-registry:hasViolation ?violation .
}
GROUP BY ?tier
ORDER BY DESC(?violationCount)
```

## Validation and Quality Assurance

### 1. Using pySHACL ✅ **COMPREHENSIVE COVERAGE COMPLETED**
**23 SHACL shapes files** provide comprehensive validation across all critical modules:

```bash
# Core validation
pyshacl -s ontology/cacontology-hotlines-shapes.ttl -d your-hotline-data.ttl
pyshacl -s ontology/cacontology-core-shapes.ttl -d your-investigation-data.ttl
pyshacl -s ontology/cacontology-forensics-shapes.ttl -d your-forensic-data.ttl

# Advanced validation
pyshacl -s ontology/cacontology-us-ncmec-shapes.ttl -d your-ncmec-data.ttl
pyshacl -s ontology/cacontology-international-shapes.ttl -d your-international-data.ttl
pyshacl -s ontology/cacontology-legal-harmonization-shapes.ttl -d your-legal-data.ttl
pyshacl -s ontology/cacontology-training-shapes.ttl -d your-training-data.ttl
pyshacl -s ontology/cacontology-prevention-shapes.ttl -d your-prevention-data.ttl
pyshacl -s ontology/cacontology-ai-csam-shapes.ttl -d your-ai-content-data.ttl
pyshacl -s ontology/cacontology-platform-infrastructure-shapes.ttl -d your-platform-data.ttl
pyshacl -s ontology/cacontology-specialized-units-shapes.ttl -d your-specialized-units-data.ttl
pyshacl -s ontology/cacontology-platforms-shapes.ttl -d your-platforms-data.ttl
pyshacl -s ontology/cacontology-detection-shapes.ttl -d your-detection-data.ttl
pyshacl -s ontology/cacontology-sex-offender-registry-shapes.ttl -d your-registry-data.ttl

# Educational and trafficking validation
pyshacl -s ontology/cacontology-educational-exploitation-shapes.ttl -d your-educational-data.ttl
pyshacl -s ontology/cacontology-sex-trafficking-shapes.ttl -d your-trafficking-data.ttl
pyshacl -s ontology/cacontology-athletic-exploitation-shapes.ttl -d your-athletic-data.ttl
```

**Coverage Statistics**: 71.88% (23 of 32 modules) - All critical modules covered with 10,000+ validation rules

### 2. Common Validation Rules
- Reports must have at least one evidence item
- Evidence items must have a firstSeen timestamp
- Actions must have a performer and timestamps
- Forward actions must specify a target organization
- Production offenses must specify victim count
- Impact assessments must link to specific victims
- Registry offenders must have valid tier classifications

### 3. Performance Testing
```bash
# Run performance test for Q1 query (must complete in ≤ 500ms on 5M triples)
time sparql --query example_SPARQL_queries/find_open_reports.rq --data your-5m-triple-dataset.ttl
```

## Development Workflow

### 1. Local Development Setup
```bash
# Start complete development environment (from repository root)
docker compose -f testing/docker-compose.yaml up -d

# Validate all ontologies
docker exec cac-robot robot validate *.ttl

# Run SHACL validation
docker exec cac-pyshacl pyshacl -s *-shapes.ttl -d examples_knowledge_graphs/*.ttl
```

### 2. Contributing New Examples
1. Create your example in `examples/` directory
2. Ensure it validates against relevant SHACL shapes
3. Add corresponding SPARQL queries in `example_SPARQL_queries/` directory
4. Update documentation with usage examples
5. Submit pull request with automated CI validation

### 3. Adding New Ontology Modules
1. Follow naming convention: `cacontology-[domain].ttl`
2. Create corresponding SHACL shapes: `cacontology-[domain]-shapes.ttl`
3. Add JSON-LD context if needed: `contexts/cacontology-[domain].jsonld`
4. Create comprehensive examples demonstrating usage
5. Update architecture diagrams and documentation

## Troubleshooting

### 1. Common Issues
- **Missing required properties**: Check SHACL validation output
- **Invalid data types**: Verify XSD type annotations
- **Broken action sequences**: Ensure nextStep/previousStep chains are valid
- **Cross-reference violations**: Validate relationships between ontology modules
- **Performance problems**: Check query patterns and dataset size

### 2. Solutions
- Use SHACL validation for data quality checking
- Verify property cardinality constraints
- Review action workflow sequences
- Monitor system resources during large dataset operations
- Check the build badge on README to confirm latest commit passes validation

### 3. Getting Help
- Check existing GitHub issues
- Review comprehensive examples in `examples/` directory
- Consult SPARQL queries in `queries/` directory for usage patterns
- Join community discussions and working groups

## Integration Patterns

### 1. UCO/CASE Integration
```turtle
# Seamless integration with UCO core concepts
@prefix uco-core: <https://ontology.unifiedcyberontology.org/uco/core/> .
@prefix case-investigation: <https://ontology.caseontology.org/case/investigation/> .

# CAC investigation extends CASE investigation
example:investigation-001 a cacontology:CACInvestigation, case-investigation:Investigation ;
    uco-core:hasFacet [
        a uco-core:TimestampFacet ;
        uco-core:timestamp "2024-03-20T10:00:00Z"^^xsd:dateTime
    ] .
```

### 2. Multi-System Data Exchange
```turtle
# Support for multiple data formats and systems
example:investigation-001 cacontology:exportFormat "CASE-JSON", "UCO-Turtle", "STIX-JSON" ;
                          cacontology:compatibleWith "Autopsy", "Griffeye", "PhotoDNA-Service" .
```

## License and Support

### 1. Versioning
- Current Version: 3.0.0 (16 March 2026)
- See CHANGELOG.md for complete version history
- Follows semantic versioning (MAJOR.MINOR.PATCH)
- Coordinated releases across all 30+ ontology modules

### 2. Support Channels
- GitHub issues for bug reports and feature requests
- Community mailing list for general discussion
- Working group meetings for stakeholder feedback
- Documentation updates and improvement suggestions

### 3. License
This project is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

## Additional Resources

- [Architecture Documentation](architecture.md) - Comprehensive system design
- [Design Document](design.md) - Technical design principles
- [Product Requirements](PRD.md) - Functional and technical requirements
- [Glossary](glossary.md) - Acronyms and key terminology
- [Contributing Guidelines](../CONTRIBUTING.md) - How to contribute to the project
- [Example Files](../examples_knowledge_graphs/) - Real-world usage demonstrations
- [Analytics Queries](../example_SPARQL_queries/) - Operational intelligence examples
