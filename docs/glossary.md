# Glossary

## Acronyms

- **CAID**: Child Abuse Image Database
- **CADF**: Cloud Auditing Data Federation
- **CASE**: Cyber-investigation Analysis Standard Expression
- **CSAM**: Child Sexual Abuse Material
- **ESP**: Electronic Service Provider
- **gUFO**: Unified Foundational Ontology
- **CAC**: Crimes Against Children
- **ICAC**: Internet Crimes Against Children
- **ICMEC**: International Centre for Missing & Exploited Children
- **ICCAM**: International Child Sexual Exploitation Image Database
- **INHOPE**: International Association of Internet Hotlines
- **JSON-LD**: JavaScript Object Notation for Linked Data
- **LEA**: Law Enforcement Agency
- **MLAT**: Mutual Legal Assistance Treaty
- **NCMEC**: National Center for Missing & Exploited Children
- **NSRL**: National Software Reference Library
- **PII**: Personally Identifiable Information
- **RDF**: Resource Description Framework
- **SHACL**: Shapes Constraint Language
- **SPARQL**: SPARQL Protocol and RDF Query Language
- **TLP**: Traffic Light Protocol
- **TURTLE**: Terse RDF Triple Language
- **UCO**: Unified Cyber Ontology

## Key Terms

### Core Classes
- **HotlineReport**: A report of potential child exploitation material
- **EvidenceItem**: Digital evidence associated with a report
- **HotlineAction**: An action taken in processing a report
- **CACInvestigation**: An investigation into child exploitation
- **AutomatedReporterAgent**: Software system that automatically generates reports
- **HashFeedbackAction**: Action recording feedback on hash matches
- **URLReference**: Reference to a URL containing potential CSAM

### gUFO-Enhanced Core Classes
- **Investigation** (`cacontology-gufo:Investigation`): gUFO-enhanced investigation with phase modeling and temporal constraints
- **InitialPhase** (`cacontology-gufo:InitialPhase`): Initial investigation phase modeled as anti-rigid `gufo:Phase`
- **AnalysisPhase** (`cacontology-gufo:AnalysisPhase`): Evidence analysis phase with temporal dependencies
- **LegalProcessPhase** (`cacontology-gufo:LegalProcessPhase`): Legal proceedings phase with court coordination
- **EvidencePhase** (`cacontology-gufo:EvidencePhase`): Evidence collection and processing phase
- **ResolutionPhase** (`cacontology-gufo:ResolutionPhase`): Investigation resolution and case closure phase
- **InvestigatorRole** (`cacontology-gufo:InvestigatorRole`): Investigation role with anti-rigid properties and temporal boundaries
- **VictimRole** (`cacontology-gufo:VictimRole`): Victim role with conflict prevention mechanisms
- **OffenderRole** (`cacontology-gufo:OffenderRole`): Offender role with exclusive constraints
- **WitnessRole** (`cacontology-gufo:WitnessRole`): Witness role allowing multiple assignments
- **InformantRole** (`cacontology-gufo:InformantRole`): Informant role with confidentiality constraints
- **RescuerRole** (`cacontology-gufo:RescuerRole`): Rescue operation role with temporal dynamics

### Criminal Activity Classes
- **ProductionOffense**: Child sexual abuse material production activity
- **CustodialRelationship**: Trust relationship involving authority over children
- **GroomingSolicitation**: Grooming or solicitation of children for sexual purposes
- **SexualConsequenceGameGrooming**: Physical-space, multi-victim grooming pattern where a perpetrator uses structured “games with sexual consequences” involving several juveniles
- **Sextortion**: Sexual extortion incidents involving children
- **LiveStreamingCSA**: Live streaming of child sexual abuse
- **DigitallyGeneratedCSAMIncident**: AI-generated or manipulated CSAM

### Athletic Coaching Exploitation Classes
- **AthleticCoachingExploitation**: Child sexual exploitation by athletic coaches using sports authority and team dynamics
- **TravelTeamExploitation**: Exploitation within travel or club sports teams with enhanced coach authority
- **SchoolAthleticExploitation**: Exploitation within school-based athletic programs leveraging institutional authority
- **DualCoachingRoleExploitation**: Exploitation leveraging multiple coaching positions across teams/institutions
- **PhysicalTrainingCoercion**: Use of physical training, conditioning, and exercise as coercion mechanism
- **ConditioningCoercion**: Use of physical conditioning exercises as coercion for sexual compliance
- **TeamMembershipCoercion**: Threats to team membership and participation as coercion
- **MaterialBenefitCoercion**: Athletic equipment, benefits, or opportunities as coercion
- **AthleticFacilityExploitation**: Exploitation occurring in athletic facilities and sports venues
- **SexualEducationExploitation**: Use of sexual topics and education as exploitation method within athletic context
- **PhysicalContactEscalation**: Escalation of physical contact within athletic training context
- **ParentNetworkDiscovery**: Discovery through parent community networks and team family communications

### Investigation Classes
- **UnderCoverOperation**: Covert investigation activities
- **TacticalOperation**: High-risk law enforcement operations
- **MultiJurisdictionalOperation**: Cross-jurisdictional investigations
- **ForensicAcquisitionAction**: Digital evidence collection and imaging
- **ContentDetectionAction**: Automated CSAM detection and classification
- **LegalProcessAction**: Initiation of legal processes (warrants, subpoenas)
- **VictimRescueAction**: Operations to rescue and protect victims

### Victim Services Classes
- **VictimImpactAssessment**: Comprehensive trauma and harm evaluation
- **TaskForceOperation**: Multi-agency coordinated operations
- **TherapeuticIntervention**: Treatment and support services for victims
- **ComplexTrauma**: Severe psychological harm from abuse
- **VictimRecoveryProgram**: Long-term support and rehabilitation services

### Registry & Compliance Classes
- **RegisteredOffender**: Individual in sex offender registry system
- **ComplianceMonitoringOperation**: Registry compliance verification activities
- **RegistrationRecord**: Official registry documentation
- **ComplianceViolation**: Failure to meet registry requirements
- **NotificationRequirement**: Community notification obligations

### International Classes
- **CrossBorderInvestigation**: International coordination activities
- **TrainingProgram**: Professional development and capacity building
- **PreventionProgram**: Education and awareness initiatives
- **LegalHarmonization**: International legal framework alignment
- **MutualLegalAssistance**: International legal cooperation mechanisms

### Technical Classes
- **ForensicImage**: Bit-for-bit copy of digital storage device
- **PhotoDNAHash**: Microsoft PhotoDNA hash value for image matching
- **DetectionResult**: Outcome of automated content analysis
- **SocialMediaPlatform**: Online platform used for communication or content sharing
- **ContentModerationCapability**: Platform's ability to detect and remove illegal content

### Athletic Coaching Roles
- **AthleticCoachRole**: Athletic coaching role with authority over team members and training activities
- **TravelTeamCoachRole**: Coaching role for travel or club sports teams with enhanced authority and access
- **SchoolAthleticCoachRole**: Coaching role within school-based athletic programs with institutional authority
- **HeadCoachRole**: Head coaching role with primary authority over team and training decisions
- **AssistantCoachRole**: Assistant coaching role with delegated authority over specific training aspects

### Properties
- **reportedBy**: Links a report to its reporter
- **hasEvidence**: Links a report to its evidence
- **triggersAction**: Links a report to actions taken
- **performedBy**: Links an action to its performer
- **depictsChild**: Links digital artifact to depicted child (TLP-RED by default)
- **producesArtifact**: Links an event to digital artifacts created
- **involvesVictim**: Links an event to victim roles
- **involvesOffender**: Links an event to offender roles
- **hasStep**: Links investigation to lifecycle steps
- **nextStep**: Chronological sequence in workflows
- **previousStep**: Reverse chronological sequence
- **severityLevel**: Severity rating (0-3 scale)

### Athletic Exploitation Properties
- **coachesTeam**: Links coach to team they coach
- **playsOnTeam**: Links player to team they participate in
- **holdsCoachingRole**: Links person to coaching role they hold
- **exploitsAthleticAuthority**: Links exploitation to athletic authority being exploited
- **usesPhysicalTraining**: Links exploitation to physical training coercion methods used
- **occursInFacility**: Links exploitation to athletic facility where it occurs
- **threatensMembership**: Links coercion to team membership threats made
- **escalatesPhysicalContact**: Links exploitation to physical contact escalation patterns
- **discoveredByParents**: Links exploitation to parent network discovery
- **sportType**: Type of sport (baseball, basketball, soccer, football, tennis, etc.)
- **teamType**: Type of team (travel, school, club, recreational, competitive)
- **conditioningType**: Type of conditioning exercise used for coercion
- **exhaustionLevel**: Level of physical exhaustion induced
- **materialBenefitType**: Type of material benefit offered
- **contactEscalationPattern**: Pattern of physical contact escalation

### Status Values
- **status-new**: Report is newly received
- **status-in-progress**: Report is being processed
- **status-in-review**: Report is under review
- **status-forwarded**: Report has been forwarded to LEA
- **status-closed**: Report processing is complete
- **status-reopened**: Report has been reopened for additional review

### Classification Values
- **classification-confirmed**: Material confirmed as CSAM
- **classification-false-positive**: Material not CSAM
- **classification-uncertain**: Requires further review
- **classification-legal**: Material is legal but concerning
- **classification-other**: Other classification

### Registry Tier Classifications
- **Tier I**: Low-risk offenders (10-15 year registration)
- **Tier II**: Moderate-risk offenders (25 year registration)
- **Tier III**: High-risk offenders (lifetime registration)

### Traffic Light Protocol (TLP) Classifications
- **TLP-RED**: Critical sensitivity, no sharing (default for depictsChild)
- **TLP-AMBER**: Limited sharing within organization
- **TLP-GREEN**: Community sharing allowed
- **TLP-WHITE**: Public information, unrestricted sharing

### Operation Types
- **Named Operations**: Coordinated multi-agency operations (e.g., "Operation Cyber Highway Safety Check")
- **Seasonal Operations**: Operations timed to seasonal patterns (e.g., spring break)
- **Compliance Operations**: Large-scale registry verification activities
- **Rescue Operations**: Emergency response to save children from ongoing abuse
- **Prevention Campaigns**: Educational and awareness programs
- **Athletic Coaching Operations**: Investigations targeting sports-based exploitation and coaching abuse

### Investigative Techniques
- **Undercover Infiltration**: Covert penetration of criminal networks
- **Digital Forensics**: Technical analysis of digital evidence
- **Hash Matching**: Automated comparison of known CSAM signatures
- **Behavioral Analysis**: Pattern recognition in grooming and exploitation
- **Cross-Platform Analysis**: Investigation across multiple digital services
- **Athletic Authority Analysis**: Investigation of sports-based authority exploitation
- **Team Dynamics Investigation**: Analysis of group-based exploitation patterns
- **Physical Training Coercion Analysis**: Investigation of exercise-based compliance mechanisms

### International Frameworks
- **ICMEC Global Partnership**: Cooperation with 120+ countries
- **CSAM Model Law**: Template legislation for international harmonization
- **Cross-Border Information Sharing**: Secure international data exchange
- **Capacity Building**: Training and technical assistance programs
- **Policy Harmonization**: Alignment of legal frameworks across jurisdictions

### Performance Metrics
- **Arrest Rate**: Arrests per search warrant executed
- **Rescue Rate**: Children rescued per operation
- **Compliance Rate**: Registry offenders in compliance with requirements
- **Training Reach**: Number of professionals trained globally
- **Prevention Effectiveness**: Impact measurement of education programs
- **Athletic Investigation Success**: Effectiveness of sports-based exploitation investigations
- **Parent Network Response**: Speed and effectiveness of community-based discovery

### Technology Integration
- **UCO Compatibility**: Native integration with Unified Cyber Ontology
- **CASE Export**: Seamless export to CASE investigation format
- **JSON-LD Context**: Developer-friendly API integration
- **SHACL Validation**: Automated data quality verification
- **SPARQL Analytics**: Query-based operational intelligence

See the individual ontology modules and their SKOS concept schemes for complete term definitions and relationships.

## License

This project is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). 