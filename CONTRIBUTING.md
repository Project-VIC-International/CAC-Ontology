# Contributing to CAC Ontology Family

This document provides guidelines for contributing to the CAC ontology family. Please read it carefully before submitting any changes.

## Project Structure

The CAC ontology family is organized into several modules:

- `cacontology-core.ttl`: Core investigation classes and properties
- `cacontology-core-shapes.ttl`: SHACL validation for core
- `hotlines-core.ttl`: Hotline reporting classes and properties
- `hotlines-core-shapes.ttl`: SHACL validation for hotlines
- `cacontology-us-ncmec.ttl`: NCMEC-specific extensions
- `contexts/`: JSON-LD context files
- `examples/`: Example data files
- `queries/`: SPARQL query examples

## Development Process

1. Create a new branch for your changes
2. Make your changes
3. Add tests
4. Run validation checks
5. Submit a pull request

## Style Guide

Follow the UCO Style Guide:

- Use Turtle format for ontologies
- Use proper prefixes
- Document all changes
- Follow naming conventions
- Include examples

## Testing

Before merging, changes must pass:

```bash
# Validate ontology structure
robot validate --input your-file.ttl

# Validate SHACL constraints
pyshacl -s shapes-file.ttl -d your-file.ttl

# Validate examples
pyshacl -s shapes-file.ttl -d examples/your-example.ttl
```

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
- Update SHACL validation rules
- Add example usage
```

## Sign-off

All commits must be signed off to indicate agreement with the [Developer Certificate of Origin](https://developercertificate.org/).

## Documentation

Update:
- CHANGELOG.md
- README.md
- Example files
- SPARQL queries

## JSON-LD Contexts

### Context Files
JSON-LD context files are stored in the `contexts/` directory:
- `hotlines-core.jsonld`: Context for hotline reporting
- `cacontology-core.jsonld`: Context for CAC investigations

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
    "@vocab": "https://cacontology.projectvic.org/hotlines/2025/core#",
    "HotlineReport": {
      "@type": "@id"
    },
    "reportedBy": {
      "@type": "@id"
    }
  }
}
```

## Pull Requests

1. Reference related issues
2. Include tests
3. Update documentation
4. Follow style guide
5. Sign off commits

## Code Review

Changes are reviewed for:
- Style compliance
- Test coverage
- Documentation updates
- Performance impact
- Security considerations

## Questions?

Contact the UCO Ontology Team:
- GitHub issues
- Mailing list
- Documentation

## License

This project is licensed under the [Apache License 2.0](LICENSE). 