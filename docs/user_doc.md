# CAC Ontology Family - User Documentation
One or more of these ontologies can be used to develop unique software applications for users that are then foundationally interoperable with other applications built on this family of ontologies.

This family of ontologies seeks to implement semantically clear information models that reflect the information, information relationships, workflows, and events that a Crimes Against Children Investigator uses or may use in the future. Each ontology represents a unique application domain within investigators'and prosecutors' discourse. This family of ontologies seeks to be universal and it is heavily informed by public documentation in the form of press releses from law enforcement agencies and prosecutor's offices. Finally, this family of ontologies seeks to use modern language as much as possible to reflect the unifying efforts of the CAC community, but there may be language in these ontologies that are more reflective of a certain country when that language is still professionally used.

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

4. **NEW**: Load gUFO-enhanced ontologies:
```bash
# Load core gUFO integration
curl -X POST http://localhost:3030/cac/data \
  --data-binary @cacontology-core-gufo.ttl \
  --header "Content-Type: text/turtle"

# Load temporal framework
curl -X POST http://localhost:3030/cac/data \
  --data-binary @cacontology-temporal-gufo.ttl \
  --header "Content-Type: text/turtle"

# Load integration strategy
curl -X POST http://localhost:3030/cac/data \
  --data-binary @cacontology-gufo-integration-strategy.ttl \
  --header "Content-Type: text/turtle"
```

## Core Concepts

> **Note on examples and namespaces:** Many of the examples in this document use legacy `icac-*` prefixes and `https://ontology.unifiedcyberontology.org/...` IRIs from the original ICAC ontology work. In CAC Ontology v2.x, the corresponding production modules use `cacontology-*` prefixes and `https://cacontology.projectvic.org/{module-name}#` IRIs; the ICAC-style examples are retained here to illustrate modeling patterns that are now realized in the CAC Ontology family.

### 1. Hotline Reports
We use hotline reports as a foundation of the ontology. They represent the initial reports of potential child exploitation material.

```turtle
@base <https://example.org/hotline/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix uco-core: <https://ontology.unifiedcyberontology.org/core#> .
@prefix uco-observable: <https://ontology.unifiedcyberontology.org/observable#> .
@prefix hotline: <https://ontology.unifiedcyberontology.org/hotlines/2025/core#> .

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
@prefix icac-gufo: <https://ontology.unifiedcyberontology.org/icac/gufo#> .
@prefix gufo: <http://purl.org/nemo/gufo#> .

# Investigation with gUFO phases
example:Investigation001 rdf:type icac-gufo:Investigation ;
    icac-gufo:inPhase example:ResolutionPhase001 ;
    icac-gufo:hasPhase example:InitialPhase001, example:AnalysisPhase001 .

# Initial phase with temporal constraints
example:InitialPhase001 rdf:type icac-gufo:InitialPhase ;
    icac-gufo:hasPhaseBeginPoint "2025-01-01T08:00:00Z"^^xsd:dateTimeStamp ;
    icac-gufo:hasPhaseEndPoint "2025-01-03T17:00:00Z"^^xsd:dateTimeStamp ;
    icac-temporal:phaseDuration "P2DT9H"^^xsd:duration ;
    icac-temporal:phaseEfficiency "1.2"^^xsd:decimal .

# Analysis phase with dependencies
example:AnalysisPhase001 rdf:type icac-gufo:AnalysisPhase ;
    icac-temporal:hasPrerequisitePhase example:InitialPhase001 ;
    icac-gufo:hasPhaseBeginPoint "2025-01-03T17:00:00Z"^^xsd:dateTimeStamp .
```

#### 4.2 Enhanced Role Modeling with Anti-Rigidity

```turtle
# Person with multiple roles (prevented conflicts)
example:Witness_Parent icac-gufo:playsRole example:WitnessRole001 ;
    icac-gufo:playsRole example:InformantRole001 .

# Investigation role with temporal boundaries
example:InvestigatorRole001 rdf:type icac-gufo:InvestigatorRole ;
    icac-gufo:hasRoleBeginPoint "2025-01-01T08:00:00Z"^^xsd:dateTimeStamp ;
    icac-gufo:participatesInInvestigation example:Investigation001 .

# Role conflict prevention (automatic validation)
# This would be INVALID and caught by gUFO validation:
# example:Person001 icac-gufo:playsRole example:VictimRole001 ;
#                   icac-gufo:playsRole example:OffenderRole001 .  # CONFLICT!
```

#### 4.3 Event vs Situation Distinction

```turtle
# Concrete investigation actions as Events
example:SearchWarrantExecution001 rdf:type icac-gufo:InvestigationEvent ;
    rdf:type gufo:Event ;
    gufo:hasBeginPointInXSDDateTimeStamp "2025-01-05T06:00:00Z"^^xsd:dateTimeStamp ;
    gufo:hasEndPointInXSDDateTimeStamp "2025-01-05T08:30:00Z"^^xsd:dateTimeStamp .

# Ongoing investigation state as Situation
example:ActiveInvestigationSituation001 rdf:type icac-gufo:ActiveInvestigationSituation ;
    rdf:type gufo:Situation ;
    gufo:hasBeginPointInXSDDateTimeStamp "2025-01-01T08:00:00Z"^^xsd:dateTimeStamp .
```

#### 4.4 Temporal Investigation Lifecycle

```turtle
@prefix icac-temporal: <https://ontology.unifiedcyberontology.org/icac/temporal#> .

# Investigation with suspension/resumption
example:Investigation002 rdf:type icac-gufo:Investigation ;
    icac-temporal:hasTimeToResolution "P45D"^^xsd:duration ;
    icac-temporal:hasActiveDuration "P38D"^^xsd:duration ;
    icac-temporal:hasSuspendedDuration "P7D"^^xsd:duration ;
    icac-temporal:urgencyLevel "4"^^xsd:nonNegativeInteger .

# Suspension event
example:Suspension001 rdf:type icac-temporal:SuspensionEvent ;
    icac-temporal:suspends example:Investigation002 ;
    icac-temporal:suspensionReason "pending_court_order" ;
    gufo:hasBeginPointInXSDDateTimeStamp "2025-01-15T16:00:00Z"^^xsd:dateTimeStamp .

# Resumption event  
example:Resumption001 rdf:type icac-temporal:ResumptionEvent ;
    icac-temporal:resumes example:Investigation002 ;
    icac-temporal:resumptionTrigger "court_order_received" ;
    gufo:hasBeginPointInXSDDateTimeStamp "2025-01-22T09:00:00Z"^^xsd:dateTimeStamp .
```

#### 4.5 Multi-Jurisdiction Coordination

```turtle
# Complex multi-jurisdiction scenario
example:MultiJurisdictionCoordination001 rdf:type icac-temporal:MultiJurisdictionCoordinationSituation ;
    rdf:type gufo:Situation ;
    icac-temporal:coordinatesInvestigations example:Investigation001, example:Investigation003 ;
    icac-temporal:involvesJurisdictions "US-CA", "US-TX", "CA-ON" ;
    gufo:hasBeginPointInXSDDateTimeStamp "2025-01-10T14:00:00Z"^^xsd:dateTimeStamp .

# Synchronization event
example:JurisdictionSync001 rdf:type icac-temporal:JurisdictionSynchronizationEvent ;
    icac-temporal:synchronizes example:MultiJurisdictionCoordination001 ;
    icac-temporal:syncType "evidence_sharing" ;
    gufo:hasBeginPointInXSDDateTimeStamp "2025-01-12T10:00:00Z"^^xsd:dateTimeStamp .
```

### 5. Athletic Coaching Exploitation
The ontology includes comprehensive modeling of athletic coaching exploitation patterns.

```turtle
@prefix icac-athletic: <https://ontology.unifiedcyberontology.org/icac/athletic#> .
@prefix uco-identity: <https://ontology.unifiedcyberontology.org/identity#> .

# Athletic coaching exploitation case
<https://example.org/exploitation/coach-case> a icac-athletic:DualCoachingRoleExploitation ;
    icac-athletic:sportType "baseball" ;
    icac-athletic:teamType "travel" ;
    icac-athletic:practiceFrequency "3"^^xsd:decimal ;
    icac-athletic:teamSize "7"^^xsd:nonNegativeInteger ;
    icac-athletic:multipleRoles "2"^^xsd:nonNegativeInteger ;
    uco-core:startTime "2023-01-01T00:00:00Z"^^xsd:dateTime ;
    uco-core:endTime "2024-08-01T00:00:00Z"^^xsd:dateTime .

# Coach with dual roles
<https://example.org/person/coach> a uco-identity:Person ;
    uco-core:name "Athletic Coach" ;
    icac-athletic:holdsCoachingRole <https://example.org/role/travel-coach> ;
    icac-athletic:holdsCoachingRole <https://example.org/role/school-coach> .

# Travel team coaching role
<https://example.org/role/travel-coach> a icac-athletic:TravelTeamCoachRole ;
    icac-athletic:coachingExperience "5"^^xsd:decimal ;
    icac-athletic:ageGroupCoached "12-14" ;
    icac-athletic:teamSize "15"^^xsd:nonNegativeInteger .

# Physical training coercion
<https://example.org/coercion/conditioning> a icac-athletic:ConditioningCoercion ;
    icac-athletic:conditioningType "running_drills" ;
    icac-athletic:exhaustionLevel "severe" .

# Link exploitation to coercion methods
<https://example.org/exploitation/coach-case> icac-athletic:usesPhysicalTraining <https://example.org/coercion/conditioning> .
```

## API Reference

### 1. JSON-LD Context
Context files live in `/contexts/`, versioned alongside ontology:

```json
{
  "@context": "https://ontology.unifiedcyberontology.org/hotlines/2025/core/contexts/hotlines-core.jsonld",
  "@type": "HotlineReport",
  "reportedBy": {
    "@type": "ReporterRole",
    "isAnonymous": true
  }
}
```

#### 1.1 **NEW: gUFO-Enhanced JSON-LD Context**

```json
{
  "@context": [
    "contexts/icac-core.jsonld",
    "contexts/icac-gufo.jsonld"
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
    "contexts/icac-core.jsonld",
    "contexts/icac-athletic-exploitation.jsonld"
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
  "@context": "contexts/hotlines-core.jsonld",
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
PREFIX icac-athletic: <https://ontology.unifiedcyberontology.org/icac/athletic#>
SELECT ?exploitation ?sportType ?teamSize
WHERE {
    ?exploitation a icac-athletic:AthleticCoachingExploitation ;
                  icac-athletic:sportType ?sportType ;
                  icac-athletic:teamSize ?teamSize .
}

# Find Coaches with Multiple Roles
PREFIX icac-athletic: <https://ontology.unifiedcyberontology.org/icac/athletic#>
SELECT ?coach ?roleCount
WHERE {
    ?coach icac-athletic:holdsCoachingRole ?role .
    {
        SELECT ?coach (COUNT(?role) AS ?roleCount)
        WHERE {
            ?coach icac-athletic:holdsCoachingRole ?role .
        }
        GROUP BY ?coach
        HAVING (?roleCount > 1)
    }
}
```

#### 2.2 **NEW: gUFO-Enhanced SPARQL Queries**

```sparql
# Investigation Phase Performance Analytics
PREFIX icac-gufo: <https://ontology.unifiedcyberontology.org/icac/gufo#>
PREFIX icac-temporal: <https://ontology.unifiedcyberontology.org/icac/temporal#>
PREFIX gufo: <http://purl.org/nemo/gufo#>

SELECT ?phase_type ?avg_duration ?efficiency_score ?case_count WHERE {
  {
    SELECT ?phase_type 
           (AVG(?duration_hours) as ?avg_duration)
           (AVG(?efficiency) as ?efficiency_score)
           (COUNT(?phase) as ?case_count) WHERE {
      ?phase rdf:type ?phase_type ;
             icac-gufo:phaseDuration ?duration ;
             icac-temporal:phaseEfficiency ?efficiency .
      
      # Convert duration to hours for analysis
      BIND(
        IF(CONTAINS(STR(?duration), "PT"), 
           xsd:decimal(REPLACE(REPLACE(STR(?duration), "PT", ""), "H.*", "")),
           xsd:decimal(REPLACE(REPLACE(STR(?duration), "P", ""), "D.*", "")) * 24
        ) as ?duration_hours
      )
      
      FILTER(?phase_type IN (
        icac-gufo:InitialPhase, icac-gufo:AnalysisPhase, 
        icac-gufo:LegalProcessPhase, icac-gufo:EvidencePhase,
        icac-gufo:ResolutionPhase
      ))
    }
    GROUP BY ?phase_type
  }
}
ORDER BY ?avg_duration

# Role Conflict Detection
SELECT ?person ?conflicting_roles ?investigation ?conflict_severity WHERE {
  ?person icac-gufo:playsRole ?role1 ;
          icac-gufo:playsRole ?role2 .
  
  ?role1 icac-gufo:participatesInInvestigation ?investigation .
  ?role2 icac-gufo:participatesInInvestigation ?investigation .
  
  # Detect conflicting role combinations
  FILTER(
    (?role1 = icac-gufo:VictimRole && ?role2 = icac-gufo:OffenderRole) ||
    (?role1 = icac-gufo:OffenderRole && ?role2 = icac-gufo:VictimRole) ||
    (?role1 = icac-gufo:InvestigatorRole && ?role2 = icac-gufo:OffenderRole)
  )
  
  BIND(CONCAT(STR(?role1), " + ", STR(?role2)) as ?conflicting_roles)
  BIND("CRITICAL" as ?conflict_severity)
}

# Temporal Investigation Pattern Analysis
SELECT ?pattern_type ?frequency ?avg_success_rate WHERE {
  {
    SELECT ?pattern_type 
           (COUNT(?inv) as ?frequency)
           (AVG(?completion_rate) as ?avg_success_rate) WHERE {
      
      ?inv rdf:type icac-gufo:Investigation ;
           icac-temporal:hasTimeToResolution ?resolution_time ;
           icac-gufo:hasPhase ?phase .
      
      ?phase icac-temporal:phaseCompletionRate ?completion_rate .
      
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
SELECT ?coordination_type ?jurisdiction_count ?avg_duration ?success_rate WHERE {
  {
    SELECT ?coordination_type 
           (AVG(?jurisdiction_count) as ?jurisdiction_count)
           (AVG(?duration_days) as ?avg_duration)
           (AVG(?completion_rate) as ?success_rate) WHERE {
      
      ?situation rdf:type icac-temporal:MultiJurisdictionCoordinationSituation ;
                 gufo:hasBeginPointInXSDDateTimeStamp ?begin ;
                 gufo:hasEndPointInXSDDateTimeStamp ?end .
      
      ?investigation icac-temporal:hasTimeToResolution ?total_time ;
                     icac-gufo:hasPhase ?phase .
      
      ?phase icac-temporal:phaseCompletionRate ?completion_rate .
      
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
@prefix icac-athletic: <https://ontology.unifiedcyberontology.org/icac/athletic#> .
@prefix uco-identity: <https://ontology.unifiedcyberontology.org/identity#> .
@prefix uco-location: <https://ontology.unifiedcyberontology.org/location#> .

# Main exploitation case
<https://example.org/case/athletic-001> a icac-athletic:DualCoachingRoleExploitation ;
    rdfs:label "Travel Team and School Coach Exploitation"@en ;
    icac-athletic:sportType "baseball" ;
    icac-athletic:teamType "travel" ;
    icac-athletic:practiceFrequency "3"^^xsd:decimal ;
    icac-athletic:seasonDuration "18"^^xsd:decimal ;
    icac-athletic:teamSize "7"^^xsd:nonNegativeInteger ;
    icac-athletic:multipleRoles "2"^^xsd:nonNegativeInteger ;
    uco-core:startTime "2023-01-01T00:00:00Z"^^xsd:dateTime ;
    uco-core:endTime "2024-08-01T00:00:00Z"^^xsd:dateTime .

# Perpetrator with coaching roles
<https://example.org/person/coach-001> a uco-identity:Person ;
    uco-core:name "Athletic Coach" ;
    uco-observable:age "31"^^xsd:nonNegativeInteger ;
    icac-athletic:holdsCoachingRole <https://example.org/role/travel-coach> ;
    icac-athletic:holdsCoachingRole <https://example.org/role/school-coach> .

# Travel team coaching role
<https://example.org/role/travel-coach> a icac-athletic:TravelTeamCoachRole ;
    uco-core:name "Travel Team Coach" ;
    icac-athletic:coachingExperience "5"^^xsd:decimal ;
    icac-athletic:ageGroupCoached "12-14" ;
    icac-athletic:teamSize "15"^^xsd:nonNegativeInteger .

# School coaching role
<https://example.org/role/school-coach> a icac-athletic:SchoolAthleticCoachRole ;
    uco-core:name "School Head Coach" ;
    icac-athletic:coachingExperience "5"^^xsd:decimal ;
    icac-athletic:institutionalAffiliation "School Athletic Program" ;
    icac-athletic:ageGroupCoached "12-18" .

# Physical training coercion
<https://example.org/coercion/conditioning-001> a icac-athletic:ConditioningCoercion ;
    rdfs:label "Conditioning Exercise Exposure Coercion"@en ;
    icac-athletic:conditioningType "running_drills" ;
    icac-athletic:exhaustionLevel "severe" .

# Team membership threats
<https://example.org/coercion/membership-001> a icac-athletic:TeamMembershipCoercion ;
    rdfs:label "Team Membership Threat Coercion"@en ;
    icac-athletic:threatSpecificity "specific" .

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
<https://example.org/facility/gym-exploitation> a icac-athletic:GymExploitation ;
    rdfs:label "Gymnasium Exploitation"@en ;
    icac-athletic:facilityType "gym" .

<https://example.org/facility/field-exploitation> a icac-athletic:AthleticFieldExploitation ;
    rdfs:label "Baseball Field Exploitation"@en ;
    icac-athletic:facilityType "field" .

# Discovery through parent network
<https://example.org/discovery/parent-rumors> a icac-athletic:RumorCirculationDiscovery ;
    rdfs:label "Parent Network Rumor Circulation"@en ;
    uco-core:startTime "2024-07-01T00:00:00Z"^^xsd:dateTime ;
    icac-athletic:parentNetworkSize "10"^^xsd:nonNegativeInteger ;
    icac-athletic:rumorCirculationDuration "30"^^xsd:decimal .

# Link relationships
<https://example.org/case/athletic-001> icac-athletic:exploitsAthleticAuthority <https://example.org/role/travel-coach> ;
    icac-athletic:exploitsAthleticAuthority <https://example.org/role/school-coach> ;
    icac-athletic:usesPhysicalTraining <https://example.org/coercion/conditioning-001> ;
    icac-athletic:employsConditioningCoercion <https://example.org/coercion/membership-001> ;
    icac-athletic:occursInFacility <https://example.org/location/gym-001> ;
    icac-athletic:occursInFacility <https://example.org/location/field-001> ;
    icac-athletic:discoveredByParents <https://example.org/discovery/parent-rumors> .
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
@prefix icac: <https://ontology.unifiedcyberontology.org/icac#> .

icac:investigation-001 a icac:ICACInvestigation ;
    icac:hasStep icac:receive-tip-001, icac:review-tip-001, icac:legal-process-001 ;
    icac:hasReport hotline:report-004 .

icac:receive-tip-001 a icac:ReceiveCybertipAction ;
    icac:nextStep icac:review-tip-001 ;
    uco-action:startTime "2024-03-20T13:00:00Z"^^xsd:dateTime .

icac:review-tip-001 a icac:ReviewCybertipAction ;
    icac:previousStep icac:receive-tip-001 ;
    icac:nextStep icac:legal-process-001 ;
    uco-action:performer icac:analyst-001 .

icac:legal-process-001 a icac:LegalProcessAction ;
    icac:previousStep icac:review-tip-001 ;
    icac:targetsService icac:social-platform-001 ;
    icac:legalInstrument icac:search-warrant-001 .
```

### 6. Production Case Investigation

#### 6.1 CSAM Production Offense
```turtle
@prefix icac-production: <https://ontology.unifiedcyberontology.org/icac/production#> .

icac-production:offense-001 a icac-production:ProductionOffense ;
    icac-production:productionMethod "direct_recording" ;
    icac-production:sessionCount 15 ;
    icac-production:victimCount 2 ;
    icac-production:producedAt icac-production:location-001 ;
    icac-production:usesEquipment icac-production:device-001 .

icac-production:producer-001 a icac-production:Producer ;
    icac-production:holdsPositionOf icac-production:babysitter-role ;
    icac-production:violatesPosition icac-production:trust-violation-001 .
```

### 7. Victim Impact Assessment

#### 7.1 Comprehensive Impact Assessment
```turtle
@prefix icac-impact: <https://ontology.unifiedcyberontology.org/icac/victim-impact#> .

icac-impact:assessment-001 a icac-impact:ComprehensiveImpactAssessment ;
    icac-impact:severityLevel "severe" ;
    icac-impact:assessesVictim icac-impact:victim-001 ;
    icac-impact:identifiesHarm icac-impact:complex-trauma-001 .

icac-impact:complex-trauma-001 a icac-impact:ComplexTrauma ;
    icac-impact:traumaType "complex" ;
    icac-impact:severity "severe" ;
    icac-impact:manifestsAs icac-impact:behavioral-indicator-001, icac-impact:emotional-indicator-001 .

icac-impact:therapeutic-intervention-001 a icac-impact:TraumaTherapy ;
    icac-impact:treatmentModality "CBT" ;
    icac-impact:addressesHarm icac-impact:complex-trauma-001 ;
    icac-impact:treatmentOutcome "partially_successful" .
```

### 8. Task Force Operations

#### 8.1 Multi-Agency Operation
```turtle
@prefix icac-taskforce: <https://ontology.unifiedcyberontology.org/icac/taskforce#> .

icac-taskforce:operation-001 a icac-taskforce:TaskForceOperation ;
    icac-taskforce:operationName "Operation Cyber Highway Safety Check" ;
    icac-taskforce:leadAgency icac-taskforce:arkansas-dps ;
    icac-taskforce:participatingAgency icac-taskforce:local-sheriff-001, icac-taskforce:fbi-field-office-001 ;
    icac-taskforce:arrestCount 42 ;
    icac-taskforce:searchWarrantCount 178 ;
    icac-taskforce:childrenRescued 5 .
```

### 9. Sex Offender Registry Integration

#### 9.1 Registry Compliance Monitoring
```turtle
@prefix icac-registry: <https://ontology.unifiedcyberontology.org/icac/sex-offender-registry#> .

icac-registry:compliance-operation-001 a icac-registry:ComplianceMonitoringOperation ;
    icac-registry:visitCount 1600 ;
    icac-registry:complianceRate 0.95 ;
    icac-registry:violationCount 80 ;
    icac-registry:newArrestCount 12 .

icac-registry:offender-001 a icac-registry:RegisteredOffender ;
    icac-registry:registrationTier "Tier II" ;
    icac-registry:hasRegistrationRecord icac-registry:record-001 ;
    icac-registry:subjectToRestriction icac-registry:internet-restriction-001 .
```

### 10. International Coordination

#### 10.1 Cross-Border Investigation
```turtle
@prefix icac-international: <https://ontology.unifiedcyberontology.org/icac/international#> .

icac-international:cross-border-001 a icac-international:CrossBorderInvestigation ;
    icac-international:originCountry "US" ;
    icac-international:targetCountry "UK" ;
    icac-international:coordinationMechanism icac-international:mutual-legal-assistance ;
    icac-international:informationShared icac-international:evidence-package-001 .
```

### 11. Forensic Analysis

#### 11.1 Digital Forensics Workflow
```turtle
@prefix icac-forensics: <https://ontology.unifiedcyberontology.org/icac/forensics#> .

icac-forensics:acquisition-001 a icac-forensics:ForensicAcquisitionAction ;
    icac-forensics:acquisitionMethod "physical_imaging" ;
    icac-forensics:writeBlockingUsed true ;
    icac-forensics:evidenceSeized icac-forensics:mobile-device-001 ;
    icac-forensics:producesImage icac-forensics:forensic-image-001 .

icac-forensics:analysis-001 a icac-forensics:ForensicAnalysisAction ;
    icac-forensics:analyzesImage icac-forensics:forensic-image-001 ;
    icac-forensics:usesTool icac-forensics:cellebrite-tool ;
    icac-forensics:recoversFiles icac-forensics:recovered-images-001 .
```

## Advanced Query Examples

### 1. Cross-Ontology Analytics
```sparql
# Find investigations with production offenses and victim impact assessments
PREFIX icac: <https://ontology.unifiedcyberontology.org/icac#>
PREFIX icac-production: <https://ontology.unifiedcyberontology.org/icac/production#>
PREFIX icac-impact: <https://ontology.unifiedcyberontology.org/icac/victim-impact#>

SELECT ?investigation ?offense ?assessment ?severity
WHERE {
    ?investigation a icac:ICACInvestigation ;
                  icac:hasStep ?step .
    ?step a icac-production:ProductionOffense .
    ?offense a icac-production:ProductionOffense .
    ?assessment a icac-impact:VictimImpactAssessment ;
               icac-impact:severityLevel ?severity .
}
```

### 2. Task Force Performance Metrics
```sparql
# Calculate task force operation effectiveness
PREFIX icac-taskforce: <https://ontology.unifiedcyberontology.org/icac/taskforce#>

SELECT ?operation ?arrestRate ?rescueRate
WHERE {
    ?operation a icac-taskforce:TaskForceOperation ;
              icac-taskforce:arrestCount ?arrests ;
              icac-taskforce:searchWarrantCount ?warrants ;
              icac-taskforce:childrenRescued ?rescued .
    BIND(?arrests / ?warrants AS ?arrestRate)
    BIND(?rescued / ?arrests AS ?rescueRate)
}
ORDER BY DESC(?arrestRate)
```

### 3. Registry Compliance Analysis
```sparql
# Find compliance violations by registry tier
PREFIX icac-registry: <https://ontology.unifiedcyberontology.org/icac/sex-offender-registry#>

SELECT ?tier (COUNT(?violation) AS ?violationCount)
WHERE {
    ?offender a icac-registry:RegisteredOffender ;
             icac-registry:registrationTier ?tier ;
             icac-registry:hasViolation ?violation .
}
GROUP BY ?tier
ORDER BY DESC(?violationCount)
```

## Validation and Quality Assurance

### 1. Using pySHACL ✅ **COMPREHENSIVE COVERAGE COMPLETED**
**23 SHACL shapes files** provide comprehensive validation across all critical modules:

```bash
# Core validation
pyshacl -s ontology/icac/hotlines-core-shapes.ttl -d your-hotline-data.ttl
pyshacl -s ontology/icac/icac-core-shapes.ttl -d your-investigation-data.ttl
pyshacl -s ontology/icac/icac-forensics-shapes.ttl -d your-forensic-data.ttl

# Advanced validation (NEW)
pyshacl -s ontology/icac/icac-us-ncmec-shapes.ttl -d your-ncmec-data.ttl
pyshacl -s ontology/icac/icac-international-shapes.ttl -d your-international-data.ttl
pyshacl -s ontology/icac/icac-legal-harmonization-shapes.ttl -d your-legal-data.ttl
pyshacl -s ontology/icac/icac-training-shapes.ttl -d your-training-data.ttl
pyshacl -s ontology/icac/icac-prevention-shapes.ttl -d your-prevention-data.ttl
pyshacl -s ontology/icac/icac-ai-generated-content-shapes.ttl -d your-ai-content-data.ttl
pyshacl -s ontology/icac/icac-platform-infrastructure-shapes.ttl -d your-platform-data.ttl
pyshacl -s ontology/icac/icac-specialized-units-shapes.ttl -d your-specialized-units-data.ttl
pyshacl -s ontology/icac/icac-platforms-shapes.ttl -d your-platforms-data.ttl
pyshacl -s ontology/icac/icac-detection-shapes.ttl -d your-detection-data.ttl
pyshacl -s ontology/icac/icac-sex-offender-registry-shapes.ttl -d your-registry-data.ttl

# Educational and trafficking validation
pyshacl -s ontology/icac/icac-educational-shapes.ttl -d your-educational-data.ttl
pyshacl -s ontology/icac/icac-trafficking-shapes.ttl -d your-trafficking-data.ttl
pyshacl -s ontology/icac/icac-athletic-exploitation-shapes.ttl -d your-athletic-data.ttl
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
time sparql --query queries/find_open_reports.rq --data your-5m-triple-dataset.ttl
```

## Development Workflow

### 1. Local Development Setup
```bash
# Start complete development environment (from repository root)
docker compose -f testing/docker-compose.yaml up -d

# Validate all ontologies
docker exec icac-robot robot validate *.ttl

# Run SHACL validation
docker exec icac-pyshacl pyshacl -s *-shapes.ttl -d examples/*.ttl
```

### 2. Contributing New Examples
1. Create your example in `examples/` directory
2. Ensure it validates against relevant SHACL shapes
3. Add corresponding SPARQL queries in `queries/` directory
4. Update documentation with usage examples
5. Submit pull request with automated CI validation

### 3. Adding New Ontology Modules
1. Follow naming convention: `icac-[domain].ttl`
2. Create corresponding SHACL shapes: `icac-[domain]-shapes.ttl`
3. Add JSON-LD context if needed: `contexts/icac-[domain].jsonld`
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
@prefix uco-core: <https://ontology.unifiedcyberontology.org/core#> .
@prefix case-investigation: <https://ontology.caseontology.org/case/investigation#> .

# CAC investigation extends CASE investigation
icac:investigation-001 a icac:ICACInvestigation, case-investigation:Investigation ;
    uco-core:hasFacet [
        a uco-core:TimestampFacet ;
        uco-core:timestamp "2024-03-20T10:00:00Z"^^xsd:dateTime
    ] .
```

### 2. Multi-System Data Exchange
```turtle
# Support for multiple data formats and systems
icac:investigation-001 icac:exportFormat "CASE-JSON", "UCO-Turtle", "STIX-JSON" ;
                      icac:compatibleWith "Autopsy", "Griffeye", "PhotoDNA-Service" .
```

## License and Support

### 1. Versioning
- Current Version: 2.2.0 (23 November 2025)
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
- [Example Files](../examples/) - Real-world usage demonstrations
- [Analytics Queries](../queries/) - Operational intelligence examples
