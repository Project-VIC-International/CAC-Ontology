# CAC Ontology Family - Product Requirements Document

## Overview
Current Crimes Against Children community language and data sets are siloed in organizations and law enforcement jurisdictions. This language is presented in many venues including courts of law, in the press, in non governmental organization reporting, and by survivors. We present a unified Crimes Against Children (CAC) family of ontologies that unifies the language used in the CAC community into a standardized, interoperable framework for representing and sharing data about child exploitation investigations and operations, and analysis. This document outlines the requirements for the 30+ module ontology family and its supporting technologies. This family of ontologies was assembled using various language models and human analysis of law enforcement and prosecutor's press releases that describe the results of investigations and legal process for crimes against children and trafficking. This family of ontologies extends the Unified Cyber Ontology (UCO), the Cyber-investigation Analysis Standard Expression (CASE) Ontology, and the Unified Foundational Ontology (gUFO) to ensure that key communities of interest can easily access the semantic modeling in the CAC Ontology. This make it possible to model all aspects of an child sexual abuse or child sex trafficking investigation, including the digital forensics examination, operations planning tradecraft, and legal process. This document presents the requirements for the CAC Ontology.

**NEW**: The ontology family now includes comprehensive gUFO (Unified Foundational Ontology) integration, providing enhanced semantic precision, temporal modeling, and validation capabilities for law enforcement investigations.

## Target Users
1. Law Enforcement Agencies
2. Hotline Organizations
3. Electronic Service Providers
4. Digital Forensics Teams
5. Research Organizations
6. Software Developers
7. Athletic Organizations and Schools
8. Child Protection Services
9. **NEW**: Ontology Engineers and Semantic Web Developers
10. **NEW**: AI/ML Researchers and Data Scientists

## Core Requirements

### 1. Ontology Structure
- Must support modular design with clear separation of concerns across 30+ specialized modules
- Must maintain compatibility with UCO (Unified Cyber Ontology)
- Must support versioning and backward compatibility
- Must include comprehensive SHACL validation rules
- Must provide JSON-LD context for developer integration
- Must support athletic coaching exploitation and sports authority abuse patterns
- **NEW**: Must implement gUFO foundational ontology patterns for enhanced semantics
- **NEW**: Must provide anti-rigid modeling for phases and roles
- **NEW**: Must distinguish between Events (actions) and Situations (states)
- **NEW**: Must support temporal constraints and validation

### 2. Data Representation
- Must support representation of:
  - Hotline reports and their lifecycle
  - Evidence items (images, videos, URLs)
  - Investigation workflows
  - Cross-border information sharing
  - Automated reporting systems
  - Classification schemes
  - Status tracking
  - Athletic coaching exploitation patterns
  - Physical training coercion mechanisms
  - Team dynamics and authority abuse
  - Educational institution vulnerabilities
  - Parent network discovery patterns
  - **NEW**: Investigation phases as anti-rigid sortals with temporal constraints
  - **NEW**: Role assignments with conflict prevention and temporal boundaries
  - **NEW**: Investigation lifecycle with suspension/resumption patterns
  - **NEW**: Multi-jurisdiction coordination scenarios
  - **NEW**: Performance metrics and efficiency tracking

### 3. Interoperability
- Must support export to CASE (Cyber-investigation Analysis Standard Expression)
- Must provide clear mapping to existing standards
- Must support multiple serialization formats (Turtle, JSON-LD, RDF/XML)
- Must include validation tools for data quality
- Must integrate with educational and athletic institution systems
- **NEW**: Must maintain backward compatibility with existing CAC ontologies
- **NEW**: Must provide equivalence mappings between original and gUFO-enhanced classes
- **NEW**: Must support parallel operation of original and enhanced models

### 4. Security & Privacy
- Must support anonymous reporting
- Must include data minimization principles
- Must encode confidentiality tier (TLP-*) so middleware can block export of TLP-RED nodes
- All triples containing depictsChild must default to TLP-RED; leakage is a critical-severity bug
- Must maintain audit trails
- Must protect sensitive information
- Must support institutional investigation confidentiality

### 5. Developer Experience
- Must provide clear documentation
- Must include example data
- Must offer testing tools
- Must support common development environments
- Must provide validation tools
- Must include athletic exploitation usage examples
- **NEW**: Must provide comprehensive gUFO integration examples
- **NEW**: Must include AI/ML integration frameworks
- **NEW**: Must support advanced analytics and pattern recognition

## Technical Requirements

### 1. Ontology Components
- Core CAC ontology
- Hotline operations ontology
- Investigation workflow ontology
- Athletic exploitation ontology
- Regional extensions (e.g., NCMEC)
- Validation shapes
- Example data sets
- **NEW**: gUFO-enhanced core investigation modeling (`cacontology-core-gufo.ttl`)
- **NEW**: Temporal framework for investigation lifecycle (`cacontology-temporal-gufo.ttl`)
- **NEW**: Integration strategy across all modules (`cacontology-gufo-integration-strategy.ttl`)
- **NEW**: Advanced analytics query library (`queries/gufo-enhanced-analytics.rq`)
- **NEW**: AI integration framework (`ai-integration-framework.py`)

### 2. Supporting Technologies
- SHACL validation engine
- JSON-LD context processor
- Testing framework
- Documentation generator
- Example data generator
- Docker compose (Fuseki + pySHACL + ROBOT) MUST validate every PR (see /devops)
- **NEW**: gUFO validation engine for anti-rigidity and temporal constraints
- **NEW**: Machine learning frameworks (scikit-learn, networkx)
- **NEW**: Advanced analytics and visualization tools

### 3. Integration Requirements
- Must support SPARQL queries
- Must provide REST API endpoints
- Must support bulk data operations
- Must include error handling
- Must support logging and monitoring
- Must integrate with educational institution systems
- **NEW**: Must support gUFO-enhanced SPARQL queries for advanced analytics
- **NEW**: Must provide AI/ML model integration capabilities
- **NEW**: Must support investigation efficiency prediction and risk assessment

## Quality Requirements

### 1. Validation
- Must validate ontology structure
- Must validate instance data
- Must check for consistency
- Must verify cross-references
- Must ensure proper typing
- Must validate athletic exploitation patterns
- **NEW**: Must validate gUFO anti-rigidity constraints
- **NEW**: Must detect role conflicts automatically
- **NEW**: Must validate temporal constraints and phase dependencies
- **NEW**: Must ensure investigation lifecycle consistency

### 2. Performance
- SPARQL query Q1 (find all open HotlineReports) on 5 M triples MUST return in ≤ 500 ms on 16 GB heap Fuseki
  - See `/queries/Q1.rq` for the exact query
- Must support large datasets (up to 100 M triples)
- Must handle 10 k new reports per day
- Must provide efficient querying
- Must handle concurrent operations
- Must support batch processing
- Must maintain reasonable response times
- Must efficiently process athletic coaching cases with complex team dynamics
- **NEW**: gUFO-enhanced queries MUST complete within 2x baseline performance
- **NEW**: Role conflict detection MUST complete in ≤ 100 ms for 1000 persons
- **NEW**: Phase validation MUST complete in ≤ 50 ms per investigation
- **NEW**: AI model inference MUST complete in ≤ 200 ms per investigation

### 3. Reliability
- Must maintain data integrity
- Must support backup and recovery
- Must handle errors gracefully
- Must provide status monitoring
- Must support audit logging
- **NEW**: Must prevent data corruption from role conflicts
- **NEW**: Must maintain temporal consistency across investigation lifecycle
- **NEW**: Must provide rollback capabilities for failed gUFO validations

## Future Requirements

### 1. Extensibility
- Must support new evidence types
- Must accommodate new workflows
- Must allow for regional variations
- Must support new classification schemes
- Must enable custom extensions
- Must support emerging athletic exploitation patterns
- **NEW**: Must support additional gUFO patterns (Quality, Mode, etc.)
- **NEW**: Must enable custom temporal patterns and constraints
- **NEW**: Must support domain-specific role hierarchies

### 2. Integration
- Must support new data sources
- Must enable new analysis tools
- Must accommodate new reporting systems
- Must support new visualization tools
- Must enable new export formats
- Must integrate with athletic organization systems
- **NEW**: Must support federated gUFO reasoning across jurisdictions
- **NEW**: Must enable real-time investigation analytics
- **NEW**: Must support predictive modeling and risk assessment

## Success Criteria
1. Successful integration with existing systems
2. Positive feedback from user community
3. Successful validation of example data
4. Clear documentation and examples
5. Efficient processing of large datasets
6. Successful cross-border data sharing
7. Effective support for investigations
8. Reliable operation in production
9. At least three external tools (Autopsy, Griffeye, PhotoDNA Service) ingest JSON-LD without modification
   - Note: Adapters allowed so long as no ontology changes required
10. Successful modeling of athletic coaching exploitation cases
11. Effective parent network discovery and institutional coordination
12. **NEW**: gUFO integration achieves >60% improvement in semantic precision
13. **NEW**: Role conflict prevention prevents >95% of modeling errors
14. **NEW**: Temporal framework reduces investigation duration by >20%
15. **NEW**: AI analytics provide actionable insights in >80% of cases

## Timeline
- Developer Preview (0.4): May 2025
  - Core functionality complete
  - Basic validation
  - Internal testing
- Public Beta (0.5): Q4 2025
  - Beta with INHOPE pilot
  - Enhanced validation
  - Public documentation
- First Update (0.6): Q2 2026
  - Additional examples
  - Performance improvements
  - Extended tool support
- Major Version (1.0): Q4 2026
  - Full feature set
  - Production ready
  - Complete documentation
- Athletic Enhancement (1.7): Q1 2025
  - Athletic coaching exploitation framework
  - Physical training coercion modeling
  - Team dynamics analysis
  - Parent network discovery
- **NEW**: gUFO Integration (2.0): **✅ COMPLETED July 2025**
  - **Phase 1 (✅ COMPLETE)**: Core investigation modeling with anti-rigid phases and roles
  - **Phase 2 (✅ COMPLETE)**: Temporal framework for investigation lifecycle management
  - **Phase 3 (✅ COMPLETE)**: Integration strategy across all 26 modules
  - Enhanced semantic precision and validation capabilities
  - AI-powered analytics and pattern recognition
  - Advanced temporal modeling and performance tracking

## Support Requirements
- Documentation updates
- User support
- Bug fixes
- Feature requests
- Training materials
- Example updates
- Validation rule updates
- Athletic exploitation case studies
- **NEW**: gUFO integration training and workshops
- **NEW**: AI/ML model maintenance and updates
- **NEW**: Advanced analytics query optimization
- **NEW**: Cross-jurisdictional deployment support

## License

This project is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
