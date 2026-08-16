# CAC Ontology

The CAC Ontology is a family of RDF/OWL vocabularies for representing crimes-against-children investigations, reporting, legal process, offender behavior, victim services, and digital-forensics activity. Project VIC International stewards the project under the Apache License 2.0.

The current project release is **CAC v3.1.0**. The semantic spine was introduced in **v3.0.0** and remains the stable CAC-facing hierarchy in v3.1.0. CASE and UCO imports are pinned to **1.5.0**.

> **Draft v4 proposal:** A foundational v4 architecture is under review in issue #44 and is not a published release. See the [proposal architecture](docs/v4-foundational-architecture.md), [v3-to-v4 migration notes](docs/v3-to-v4-migration.md), and [reproducible Gate 4 harness](testing/v4/README.md). The unmodified full-import OWL 2 DL gate remains on HOLD for disclosed upstream/tool-route blockers.

## What ships in v3.1.0

The repository currently contains:

- 50 ontology, spine, bridge, and integration Turtle modules
- 47 SHACL shape files
- 61 Turtle example graphs
- 32 SPARQL query files
- six JSON-LD contexts (grooming, sextortion, platforms, legal outcomes, US-NCMEC, and state-machine extensions)

Counts describe this repository checkout, not a promise that every ontology module has a one-to-one shapes or JSON-LD context file.

Key architectural files:

- `ontology/cacontology-core-spine.ttl` — stable top-level hierarchy
- `ontology/cacontology-core-spine-shapes.ttl` — spine constraints
- `ontology/cacontology-bridge-gufo.ttl` — gUFO alignment
- `ontology/cacontology-bridge-case.ttl` — CASE alignment
- `ontology/cacontology-bridge-uco.ttl` — UCO alignment
- `ontology/cacontology-core.ttl` — core CAC investigation vocabulary

The shipped domain modules cover hotline intake, grooming, sextortion, trafficking, production, digital forensics, platforms, legal outcomes, victim impact, task forces, international cooperation, and other specialized areas. See [the module catalog](docs/CAC-Ontology-List) for the file-by-file inventory.

## Semantic spine

Domain classes anchor to the `cac-core:` hierarchy by ontological kind:

- `cac-core:EnduringEntity`
- `cac-core:Event`
- `cac-core:Situation`
- `cac-core:Role`
- `cac-core:Phase`
- `cac-core:Artifact`
- `cac-core:AssessmentResult`

Dedicated bridges align those branches to gUFO, CASE, and UCO. Applications should normally type data with the most specific CAC domain class; inherited spine and external semantics then follow from the ontology.

## Quick start

```bash
git clone https://github.com/Project-VIC-International/CAC-Ontology.git
cd CAC-Ontology
pip install rdflib pyshacl
```

Use repository-relative paths when loading ontology files:

```turtle
@prefix cac: <https://cacontology.projectvic.org#> .
@prefix cac-core: <https://cacontology.projectvic.org/core#> .
@prefix ex: <https://example.org/> .

ex:investigation-001 a cac:CACInvestigation .
ex:action-001 a cac:ReceiveCybertipAction .
```

Validate instance data against the relevant shapes:

```bash
pyshacl -s ontology/cacontology-core-shapes.ttl -d your-data.ttl
```

The Docker-based development environment is under `testing/`:

```bash
docker compose -f testing/docker-compose.yaml up -d
```

## Documentation

Start with the [documentation index](docs/README.md):

- [User guide](docs/user_doc.md)
- [Architecture](docs/architecture.md)
- [Design](docs/design.md)
- [Interoperability](docs/interoperability.md)
- [Namespaces and prefixes](docs/namespaces-and-prefixes.md)
- [Product requirements](docs/PRD.md)
- [Glossary](docs/glossary.md)
- [Draft v4 foundational architecture](docs/v4-foundational-architecture.md)
- [Draft v3-to-v4 migration notes](docs/v3-to-v4-migration.md)

For AI-assisted ontology work, read [agent.md](agent.md). It is the authoritative repository-specific agent workflow. Tool builders can also use the [CASE-UCO-SDK and its MCP server](https://github.com/vulnmaster/CASE-UCO-SDK); this README intentionally leaves detailed agent procedure to `agent.md`.

## Repository layout

```text
.
├── ontology/                  # Ontologies, bridges, spine, and SHACL shapes
├── contexts/                  # Shipped JSON-LD contexts (limited coverage)
├── examples_knowledge_graphs/ # Example Turtle graphs
├── example_SPARQL_queries/    # SPARQL query examples
├── docs/                      # Project documentation
├── testing/                   # Validation and test infrastructure
├── agent.md                   # Detailed agent workflow
└── README.md
```

## Namespace policy

- CAC base vocabulary: `https://cacontology.projectvic.org#`
- Semantic spine: `https://cacontology.projectvic.org/core#`
- Domain modules: generally `https://cacontology.projectvic.org/{module}#`
- CASE/UCO imports: versioned **1.5.0** IRIs
- gUFO imports: versioned **1.0.0** IRI

Do not infer a namespace from a filename alone; consult the module’s prefix declarations or [namespace reference](docs/namespaces-and-prefixes.md).

## Status and scope

Ontology and shapes files in `ontology/`, contexts in `contexts/`, examples, and queries are shipped artifacts. Statements in the PRD and design document marked “requirement,” “target,” or “planned” are not claims of completed implementation. Historical release proposals are retained for context and labeled accordingly.

## Contributing and license

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidance and [license.md](license.md) for the Apache License 2.0 text.
