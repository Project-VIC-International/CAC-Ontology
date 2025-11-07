# Contributing to CAC Ontology Family

This document provides guidelines for contributing to the CAC ontology family. Please read it carefully before submitting any changes.

## Project Structure

The CAC ontology family consists of **30+ specialized modules** organized into six domain areas:

### Core Framework (3 modules)
- `cacontology-core.ttl`: Core investigation classes and properties
- `cacontology-core-shapes.ttl`: SHACL validation for core
- `cacontology-hotlines-core.ttl`: Hotline reporting classes and properties
- `cacontology-hotlines-core-shapes.ttl`: SHACL validation for hotlines
- `cacontology-us-ncmec.ttl`: NCMEC-specific extensions

### Domain Modules (25+ modules)
- **International & Global**: `cacontology-international.ttl`, `cacontology-training.ttl`, `cacontology-prevention.ttl`, `cacontology-legal-harmonization.ttl`
- **Criminal Activities**: `cacontology-production.ttl`, `cacontology-custodial.ttl`, `cacontology-grooming.ttl`, `cacontology-sextortion.ttl`, `cacontology-athletic-exploitation.ttl`
- **Investigation**: `cacontology-undercover.ttl`, `cacontology-physical-evidence.ttl`, `cacontology-tactical.ttl`, `cacontology-multi-jurisdiction.ttl`, `cacontology-stranger-abduction.ttl`
- **Technical**: `cacontology-forensics.ttl`, `cacontology-detection.ttl`, `cacontology-platforms.ttl`, `cacontology-street-recruitment.ttl`
- **Victim Services**: `cacontology-victim-impact.ttl`, `cacontology-taskforce.ttl`, `cacontology-sentencing.ttl`, `cacontology-specialized-units.ttl`, `cacontology-sex-offender-registry.ttl`

### Supporting Files
- `ontology/`: All ontology module files (30+ `.ttl` files)
- `ontology/*-shapes.ttl`: SHACL validation modules (20+ files)
- `contexts/`: JSON-LD context files
- `examples/`: Example data files (30+ real-world examples)
- `example_SPARQL_queries/`: SPARQL query examples
- `testing/`: Docker-based validation infrastructure
- `docs/`: Comprehensive documentation

## Development Process

1. Create a new branch for your changes
2. Make your changes
3. Add tests
4. Run validation checks
5. Submit a pull request

## Style Guide

Follow the UCO Style Guide and CAC Ontology conventions:

- Use Turtle format (`.ttl`) for all ontology files
- Use standardized namespace: `https://cacontology.projectvic.org`
- Follow prefix pattern: `cacontology-{module-name}:`
- File naming: `cacontology-{module-name}.ttl` and `cacontology-{module-name}-shapes.ttl`
- Document all changes with `rdfs:comment` and `rdfs:label`
- Include comprehensive examples in `examples/` directory
- Follow gUFO integration patterns where applicable
- Maintain UCO/CASE compatibility

## Testing

Before merging, changes must pass all validation checks. The project uses Docker-based validation:

```bash
# Start validation environment
cd testing
docker compose up -d

# Validate ontology structure
robot validate --input ontology/your-file.ttl

# Validate SHACL constraints
pyshacl -s ontology/your-file-shapes.ttl -d ontology/your-file.ttl

# Validate examples against shapes
pyshacl -s ontology/your-file-shapes.ttl -d examples/your-example.ttl

# Run full validation suite
docker compose exec validation python validate_shapes.py
```

### Validation Requirements

- All ontology files must validate syntactically (ROBOT)
- All modules with SHACL shapes must pass validation
- All example files must validate against their corresponding shapes
- Cross-reference validation must pass
- Namespace consistency must be maintained

## Commit Convention

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `style:` for formatting
- `refactor:` for code changes
- `test:` for tests
- `chore:` for maintenance

Example:
```
feat: add AutomatedReporterAgent class

- Add new class for software-based reporting
- Update SHACL validation rules in cacontology-core-shapes.ttl
- Add example usage in examples/automated-reporting-example.ttl
- Update CHANGELOG.md with new feature
```

### Namespace Changes

For namespace or prefix changes:
```
refactor: realign namespace from ICAC to CAC ontology

- Update all namespace URIs to https://cacontology.projectvic.org
- Change prefixes from icac-* to cacontology-*
- Update all file references and imports
- Maintain backward compatibility where possible
```

## Sign-off

All commits must be signed off to indicate agreement with the [Developer Certificate of Origin](https://developercertificate.org/).

## Documentation

When contributing, update relevant documentation:

- **CHANGELOG.md**: Add entry under [Unreleased] or new version section
- **README.md**: Update module list, examples, or features if applicable
- **docs/architecture.md**: Update architecture diagrams if structure changes
- **docs/design.md**: Update design document if patterns change
- **docs/user_doc.md**: Add usage examples for new features
- **docs/glossary.md**: Add new terms and acronyms
- **Example files**: Add real-world examples demonstrating new features
- **SPARQL queries**: Add analytics queries for new capabilities

## JSON-LD Contexts

### Context Files
JSON-LD context files are stored in the `contexts/` directory:
- `hotlines-core.jsonld`: Context for hotline reporting
- `cacontology-core.jsonld`: Context for CAC investigations (planned)

All contexts should use the standardized namespace: `https://cacontology.projectvic.org`

### Generating Contexts
Use rdf-toolkit to generate contexts:

```bash
# Install rdf-toolkit
npm install -g rdf-toolkit

# Generate context from TTL
rdf-toolkit format --from turtle --to jsonld --context your-file.ttl > contexts/your-file.jsonld
```

### Context Structure
Contexts should include:
- All prefixes used in the ontology
- Type coercion rules
- Property mappings
- Value object definitions

Example:
```json
{
  "@context": {
    "@vocab": "https://cacontology.projectvic.org/hotlines/core#",
    "cacontology": "https://cacontology.projectvic.org#",
    "cacontology-hotlines": "https://cacontology.projectvic.org/hotlines/core#",
    "HotlineReport": {
      "@type": "@id"
    },
    "reportedBy": {
      "@type": "@id"
    }
  }
}
```

### Namespace Conventions

- **Base namespace**: `https://cacontology.projectvic.org`
- **Module namespaces**: `https://cacontology.projectvic.org/{module-name}#`
- **Shapes namespaces**: `https://cacontology.projectvic.org/{module-name}/shapes#`
- **Prefix pattern**: `cacontology-{module-name}:`

## Pull Requests

When submitting a pull request:

1. **Reference related issues**: Link to GitHub issues or discussions
2. **Include validation**: All changes must pass validation tests
3. **Update documentation**: Update relevant docs (CHANGELOG, README, etc.)
4. **Follow style guide**: Adhere to namespace, naming, and formatting conventions
5. **Sign off commits**: All commits must be signed off (DCO)
6. **Add examples**: Include example files demonstrating new features
7. **Update SHACL shapes**: Add or update validation shapes for new classes/properties
8. **Test compatibility**: Ensure UCO/CASE compatibility is maintained

## Code Review

Changes are reviewed for:
- **Style compliance**: Namespace, naming, and formatting conventions
- **Validation coverage**: SHACL shapes for new classes and properties
- **Documentation updates**: CHANGELOG, README, and relevant docs
- **Example quality**: Real-world examples demonstrating usage
- **UCO/CASE compatibility**: Maintains interoperability
- **gUFO integration**: Proper foundational ontology patterns where applicable
- **Namespace consistency**: Adherence to `cacontology.projectvic.org` namespace
- **Security considerations**: TLP classification and data protection

## Questions?

For questions or support:
- **GitHub Issues**: Open an issue for bugs, features, or questions
- **Documentation**: See `docs/` directory for comprehensive guides
- **Project VIC**: Contact through Project VIC International channels

## Additional Resources

- **Architecture**: See `docs/architecture.md` for system architecture
- **Design Principles**: See `docs/design.md` for design guidelines
- **User Guide**: See `docs/user_doc.md` for usage examples
- **Glossary**: See `docs/glossary.md` for terminology

## License

This project is licensed under the [Apache License 2.0](LICENSE). 