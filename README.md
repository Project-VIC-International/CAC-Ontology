# CAC Ontology

The CAC (Crimes Against Children) Ontology Family is a comprehensive semantic framework for modeling child exploitation investigations, operations, legal processes, reporting, offender tradecraft, and digital forensics activities. This ontology family extends the Unified Cyber Ontology (UCO) and the Cyber-investigation Analysis Standard Expression (CASE) Ontology.

## Overview

The CAC Ontology Family consists of **30+ specialized modules** organized into six domain areas, enhanced with comprehensive gUFO (Unified Foundational Ontology) integration for improved semantic precision, temporal modeling, and validation capabilities. The ontology family is designed to support law enforcement agencies, hotline organizations, digital forensics teams, prosecutors, and researchers in modeling and analyzing crimes against children investigations.

**Namespace**: `https://cacontology.projectvic.org`

**Documentation**: [cacontology.projectvic.org](https://cacontology.projectvic.org)

## Key Features

- **30+ Specialized Modules**: Comprehensive coverage of child exploitation investigation domains
- **gUFO Integration**: Enhanced semantic precision with foundational ontology patterns
- **SHACL Validation**: 20+ validation modules with comprehensive business rules
- **UCO/CASE Compatibility**: Seamless integration with Unified Cyber Ontology and CASE frameworks
- **Real-World Examples**: 30+ example files based on actual law enforcement cases
- **International Support**: Global coordination frameworks for 120+ countries
- **Namespace Standardization**: Consistent `cacontology` prefix and namespace structure

## Ontology Modules

### Core Framework (3 modules)
- `cacontology-core.ttl` - Base investigation framework and lifecycles
- `cacontology-hotlines-core.ttl` - Hotline operations and report management
- `cacontology-us-ncmec.ttl` - Enhanced NCMEC integration and tip analysis

### International Coordination & Global Frameworks (4 modules)
- `cacontology-international.ttl` - Global coordination & cross-border operations
- `cacontology-training.ttl` - Professional development & capacity building
- `cacontology-prevention.ttl` - Prevention programs & education
- `cacontology-legal-harmonization.ttl` - International legal framework

### High-Priority Criminal Activities (5+ modules)
- `cacontology-production.ttl` - CSAM production operations
- `cacontology-custodial.ttl` - Custodial relationships & positions of trust
- `cacontology-grooming.ttl` - Online grooming & enticement
- `cacontology-sextortion.ttl` - Sexual extortion incidents
- `cacontology-athletic-exploitation.ttl` - Athletic coaching exploitation

### Specialized Investigation (5+ modules)
- `cacontology-undercover.ttl` - Undercover operations
- `cacontology-physical-evidence.ttl` - Physical evidence & procurement
- `cacontology-tactical.ttl` - Tactical law enforcement operations
- `cacontology-multi-jurisdiction.ttl` - Multi-jurisdictional operations
- `cacontology-stranger-abduction.ttl` - Stranger abduction patterns

### Technical Support (4+ modules)
- `cacontology-forensics.ttl` - Digital forensics
- `cacontology-detection.ttl` - Content detection & classification
- `cacontology-platforms.ttl` - Technology platforms & service providers
- `cacontology-street-recruitment.ttl` - Street-based recruitment patterns

### Victim Services & Task Force Management (5+ modules)
- `cacontology-victim-impact.ttl` - Victim impact assessment & recovery
- `cacontology-taskforce.ttl` - CAC task force organization
- `cacontology-sentencing.ttl` - Legal outcomes & sentencing
- `cacontology-specialized-units.ttl` - Specialized units & advanced capabilities
- `cacontology-sex-offender-registry.ttl` - Sex offender registry management

### Validation Components (20+ modules)
- Comprehensive SHACL validation shapes for all major modules
- Cross-reference validation and business rule enforcement

## Quick Start

### Installation

```bash
git clone https://github.com/Project-VIC-International/CAC-Ontology.git
cd CAC-Ontology
pip install -r requirements.txt
```

### Using the Ontology

```turtle
@prefix cacontology: <https://cacontology.projectvic.org#> .
@prefix cacontology-core: <https://cacontology.projectvic.org/core#> .

# Example: Create a CAC investigation
:investigation-001 a cacontology-core:CACInvestigation ;
    cacontology-core:hasReport :report-001 ;
    cacontology-core:status "active" .
```

### Validation

The project includes comprehensive SHACL validation:

```bash
docker compose -f testing/docker-compose.yaml up -d
# Validation runs automatically on all ontology files
```

## Documentation

Comprehensive documentation is available:

- **Architecture**: `docs/architecture.md` - Complete system architecture and module relationships
- **Design**: `docs/design.md` - Design principles and technical specifications
- **User Guide**: `docs/user_doc.md` - User documentation and examples
- **Product Requirements**: `docs/PRD.md` - Product requirements and specifications
- **Glossary**: `docs/glossary.md` - Terminology and acronyms

## Examples

The repository includes 30+ real-world example files based on actual law enforcement cases:

- `examples/brooklyn-morton-october-2024-example.ttl` - Athletic coaching exploitation
- `examples/arkansas-operation-cyber-highway-safety-check-example.ttl` - Large-scale operations
- `examples/operation-restore-justice-example.ttl` - Nationwide coordination
- And many more...

See the `examples/` directory for complete list.

## Repository Structure

```
.
├── ontology/                     # All ontology modules (30+ files)
│   ├── cacontology-core.ttl
│   ├── cacontology-*.ttl        # Specialized domain modules
│   └── cacontology-*-shapes.ttl # SHACL validation modules
├── examples/                     # Real-world example files (30+ files)
├── example_SPARQL_queries/       # Analytics and query examples
├── docs/                         # Documentation files
├── testing/                      # Testing and validation infrastructure
├── contexts/                     # JSON-LD context files
├── CHANGELOG.md                  # Version history
└── README.md                     # This file
```

## Namespace and Prefixes

All ontology modules use the standardized namespace structure:

- **Base Namespace**: `https://cacontology.projectvic.org`
- **Module Namespaces**: `https://cacontology.projectvic.org/{module-name}#`
- **Prefix Pattern**: `cacontology-{module-name}:`

Example:
```turtle
@prefix cacontology: <https://cacontology.projectvic.org#> .
@prefix cacontology-core: <https://cacontology.projectvic.org/core#> .
@prefix cacontology-taskforce: <https://cacontology.projectvic.org/taskforce#> .
```

## Contributing

See `CONTRIBUTING.md` for contribution guidelines. The project follows semantic versioning and maintains comprehensive documentation.

## License

This project is licensed under the Apache License 2.0. See `license.md` for details.
