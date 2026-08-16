# Glossary

This glossary applies to **CAC Ontology v3.1.0**. The semantic spine entries identify their v3.0.0 introduction as historical release context. See [Namespaces and prefixes](namespaces-and-prefixes.md) for canonical IRIs.

Draft v4 terminology is defined normatively for proposal review in [the v4 foundational architecture](v4-foundational-architecture.md) and [v3-to-v4 migration notes](v3-to-v4-migration.md). In that proposal, `RoleAssignment` is an operational bearer/classifier/context record, `Phase` is an operational occurrence linked to a separate phase classifier, `CustodyState` records time-varying custody, and `MembershipTier` is a controlled concept. These meanings do not change the published v3.1.0 release.

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

### Semantic Spine (v3.0.0)
The stable top-level class hierarchy introduced in v3.0.0 (`cac-core:` namespace, `https://cacontology.projectvic.org/core#`). The spine organizes CAC domain classes by ontological kind and provides enduring anchor types that every module inherits from.

- **cac-core:Entity**: The most general class in the CAC semantic spine. All other spine classes are subclasses of `cac-core:Entity`.
- **cac-core:EnduringEntity**: A thing that persists through time (persons, organizations, devices, artifacts). Corresponds to gUFO endurant concepts.
- **cac-core:Occurrent**: Organizing superclass for things that happen. Parent of `cac-core:Event` and related temporal classes.
- **cac-core:Event**: Something that happens or unfolds in time (e.g., a search-warrant execution, a synchronization event). Domain event classes inherit from this spine type rather than asserting `gufo:Event` directly.
- **cac-core:Situation**: A context or state that holds at a time (e.g., an active investigation situation, a multi-jurisdiction coordination). Domain situation classes inherit from this spine type rather than asserting `gufo:Situation` directly.
- **cac-core:Role**: A non-rigid role borne by an enduring entity. Investigation roles (`InvestigatorRole`, `VictimRole`, etc.) subclass this type.
- **cac-core:Phase**: A temporal stage of some entity, process, or situation. Investigation phases (`InitialPhase`, `AnalysisPhase`, etc.) subclass this type.
- **cac-core:AssessmentResult**: An output of an evaluative or classification process (e.g., triage outcomes, severity scores, detection results).
- **cac-core:Artifact**: An inspectable, storable, or evidentiary enduring entity (e.g., forensic images, hash values, digital evidence).

### Core Classes
- **HotlineReport**: A report of potential child exploitation material
- **EvidenceItem**: Digital evidence associated with a report
- **HotlineAction**: An action taken in processing a report
- **CACInvestigation**: An investigation into child exploitation
- **AutomatedReporterAgent**: Software system that automatically generates reports
- **HashFeedbackAction**: Action recording feedback on hash matches
- **URLReference**: Reference to a URL containing potential CSAM

### Core Investigation Classes (semantic spine)
- **Investigation** (`cacontology:CACInvestigation`): Core investigation class; subclass of `cac-core:EnduringEntity` in the semantic spine.
- **InitialPhase** (`cacontology:InitialPhase`): Initial investigation phase; subclass of `cac-core:Phase`
- **AnalysisPhase** (`cacontology:AnalysisPhase`): Evidence analysis phase with temporal dependencies; subclass of `cac-core:Phase`
- **LegalProcessPhase** (`cacontology:LegalProcessPhase`): Legal proceedings phase with court coordination; subclass of `cac-core:Phase`
- **EvidencePhase** (`cacontology:EvidencePhase`): Evidence collection and processing phase; subclass of `cac-core:Phase`
- **ResolutionPhase** (`cacontology:ResolutionPhase`): Investigation resolution and case closure phase; subclass of `cac-core:Phase`
- **InvestigatorRole** (`cacontology:InvestigatorRole`): Investigation role with anti-rigid properties and temporal boundaries; subclass of `cac-core:Role`
- **VictimRole** (`cacontology:VictimRole`): Victim role with conflict prevention mechanisms; subclass of `cac-core:Role`
- **OffenderRole** (`cacontology:OffenderRole`): Offender role with exclusive constraints; subclass of `cac-core:Role`
- **WitnessRole** (`cacontology:WitnessRole`): Witness role allowing multiple assignments; subclass of `cac-core:Role`
- **InformantRole** (`cacontology:InformantRole`): Informant role with confidentiality constraints; subclass of `cac-core:Role`
- **RescuerRole** (`cacontology:RescuerRole`): Rescue operation role with temporal dynamics; subclass of `cac-core:Role`

### Criminal Activity Classes
- **ProductionOffense**: Child sexual abuse material production activity
- **CustodialRelationship**: Trust relationship involving authority over children
- **GroomingSolicitation**: Grooming or solicitation of children for sexual purposes
- **AccountReplacementEvent** (`cacontology-grooming:AccountReplacementEvent`): Offender creates a new account after ban or block and resumes at an earlier grooming phase (typically `InitialContactPhase`); lifecycle reset, not a coercion loop
- **SexualConsequenceGameGrooming**: Physical-space, multi-victim grooming pattern where a perpetrator uses structured “games with sexual consequences” involving several juveniles
- **Sextortion**: Sexual extortion incidents involving children
- **CoercionCycle** (`cacontology-sextortion:CoercionCycle`): Self-sustaining sextortion loop where retained imagery is redeployed as perpetual leverage; distinct from linear `progressionStage` or single `ExtortionDemand` events
- **LiveStreamingCSA**: Live streaming of child sexual abuse
- **DigitallyGeneratedCSAMIncident**: AI-generated or manipulated CSAM

### Offense-trajectory state machine (ConditioningPhase)

Spine-level `cac-core:ConditioningPhase` models the macro preparatory phase between initial contact and exploitation in ICAC offense-trajectory state machines (contact → conditioning → exploitation → maintenance). Grooming-module instances use `cacontology-grooming:ConditioningPhase` as the canonical instance type.

| Macro phase | Canonical instance type | Notes |
|-------------|-------------------------|-------|
| Initial contact | `cacontology-grooming:InitialContactPhase` | First documented approach |
| Conditioning | `cacontology-grooming:ConditioningPhase` + `cac-core:Phase` | Macro preparatory phase; `cac-core:conditioningMode` attaches here |
| Exploitation | `cacontology-grooming:ExploitationPhase` | Primary harm act |
| Maintenance | `cacontology-grooming:MaintenancePhase` | Ongoing control / retention |

- **ConditioningPhase** (`cac-core:ConditioningPhase` / `cacontology-grooming:ConditioningPhase`): Spine-level and grooming-module class for the macro preparatory phase between initial contact and exploitation. This structure supports cross-case offense-trajectory analysis.
- **Dual typing:** Every macro conditioning node carries both `cacontology-grooming:ConditioningPhase` and `cac-core:Phase`. Spine and grooming SHACL shapes require the `cac-core:Phase` type (`sh:hasValue` with `sh:minCount 1`); instances that omit it fail validation.
- **`conditioningMode`:** The dominant preparatory mechanism (`trust_rapport`, `deception`, `isolation`, `normalization`, `desensitization`, `compliance_shaping`, `dependency_creation`, `fear_priming`, `platform_confidence`) is recorded on the macro ConditioningPhase node, not on variant sub-stage nodes. The `platform_confidence` value denotes preparatory conduct in which the offender models and develops operational confidence in a platform's affordances, detection characteristics, and community norms prior to exploitation — applicable to mainstream platforms, encrypted messaging apps, dark web forums, and generative AI tools; it is offender- and platform-directed, not victim-directed rapport or trust building.
- **Subclass vs. macro node:** `SexualizationPhase` and `IsolationPhase` are subclasses of `ConditioningPhase` because they are conditioning mechanisms — that is the correct taxonomic relationship, not a modeling workaround. In state-machine graphs, conditioning is represented as a single macro node with `conditioningMode` by default; `SexualizationPhase` or `IsolationPhase` appear as their own sequential nodes only when a case documents that sub-stage as a distinct, separate step.
- **Deprecated label:** `TrustBuildingPhase` in the grooming and sextortion modules subclasses `ConditioningPhase`. Legacy instances remain valid; new graphs express rapport-heavy cases as `ConditioningPhase` with `conditioningMode: trust_rapport`.
- **Behavior axis vs phase axis:** `groomingStage` on `GroomingBehavior` tags behavior records separately from phase typing. Legacy values `trust_building` and `sexual_introduction` remain in SHACL for older behavior graphs; `conditioning` and `sexualization` are the preferred values for new behavior tagging.
- **Sextortion deception distinction:** For sextortion cases, note that InitialDeceptionPhase (identity fabrication at first contact) is distinct from ConditioningPhase + conditioningMode: deception (preparatory deception after contact is established); see cacontology-sextortion.ttl.

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
- **ChannelMigrationEvent** (`cacontology-platforms:ChannelMigrationEvent`): Deliberate move of contact from one platform to another before escalation (capability upgrade and/or evidence trail severance)
- **PlatformAffordance** (`cacontology-platforms:PlatformAffordance`): Platform capability taxonomy (Anonymity, Ephemerality, UnmonitoredCommunication, etc.) usable for transition-level annotation
- **AffordanceMisuse** (`cacontology-platforms:AffordanceMisuse`): Links a platform affordance to the phase transition it enabled (affordances on offense edges, not platform nodes alone)
- **ContentModerationCapability**: Platform's ability to detect and remove illegal content

### Athletic Coaching Roles
- **AthleticCoachRole**: Athletic coaching role with authority over team members and training activities
- **TravelTeamCoachRole**: Coaching role for travel or club sports teams with enhanced authority and access
- **SchoolAthleticCoachRole**: Coaching role within school-based athletic programs with institutional authority
- **HeadCoachRole**: Head coaching role with primary authority over team and training decisions
- **AssistantCoachRole**: Assistant coaching role with delegated authority over specific training aspects

### Properties
- **reportedBy**: Links a report to its reporter
- **cac-core:precedes**: Spine-level temporal ordering property linking one `cac-core:Phase` instance to the next in a documented offense lifecycle (`ontology/cacontology-core-spine.ttl`). Introduced in the CaseLinker state machine extensions release. Related but distinct from `cacontology:transitionsTo` (investigation phases in `cacontology-core.ttl`), `cacontology-temporal:temporallyPrecedes` (subPropertyOf `gufo:precedes`), and `cacontology-usa-federal:precedesPhase` (federal legal phases). Not defined in UCO or CASE.
- **conditioningMode** (`cac-core:conditioningMode`): Dominant conditioning mechanism on a ConditioningPhase instance or `ConditioningBehavior` instance; see [Offense-trajectory state machine (ConditioningPhase)](#offense-trajectory-state-machine-conditioningphase)
- **sustainedBy** (`cacontology-sextortion:sustainedBy`): Links a coercion cycle to retained leverage material
- **cyclesBetween** (`cacontology-sextortion:cyclesBetween`): Links a coercion cycle to the phase instances forming the loop
- **fromPlatform** / **toPlatform** (`cacontology-platforms:`): Originating and destination platforms for a channel migration event
- **occursBetween** (`cacontology-platforms:occursBetween`): Phase instances separated by a channel migration or similar transition event
- **affordanceClass** (`cacontology-platforms:affordanceClass`): Platform affordance category misused to enable a phase transition
- **enablesTransitionFrom** / **enablesTransitionTo** (`cacontology-platforms:`): Source and target phases for affordance misuse
- **resumesAt** (`cacontology-grooming:resumesAt`): Grooming phase the offender returns to after account replacement
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
