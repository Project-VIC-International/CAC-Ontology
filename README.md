# CAC Ontology Documentation Site

This repository contains the automation for generating and deploying the CAC Ontology documentation site at [cacontology.projectvic.org](https://cacontology.projectvic.org).

## Overview

The documentation is automatically generated using [Ontospy](https://github.com/lambdamusic/Ontospy) from the ontology files in the main [CAC-Ontology repository](https://github.com/Project-VIC-International/CAC-Ontology). The documentation mirrors the structure and style of the [CASE Ontology documentation site](https://ontology.caseontology.org/documentation/index.html).

## Features

- **Automated Generation**: Documentation regenerates automatically on every push to the main ontology repository
- **Comprehensive Coverage**: Documents all ontology modules, classes, properties, and SHACL shapes
- **CASE Ontology Style**: Matches the visual style and navigation structure of the CASE Ontology documentation
- **GitHub Pages Hosting**: Automatically deployed to GitHub Pages with custom domain support

## Documentation Structure

The generated documentation includes:

- **Entities A-Z**: Alphabetical listing of all ontology entities
- **Classes**: Complete list of all ontology classes
- **Properties**: All object and datatype properties
- **Shapes**: All SHACL validation shapes
- **Statistics**: Ontology metrics and statistics

## How It Works

1. **GitHub Actions Workflow**: The `.github/workflows/deploy_docs.yml` workflow triggers on:
   - Push to main branch (for script/config changes)
   - Scheduled checks (to detect ontology changes)
   - Manual workflow dispatch

2. **Documentation Generation**: The `scripts/generate_docs.py` script:
   - Fetches the latest ontology files from the main CAC-Ontology repository
   - Merges all ontology modules into a unified ontology
   - Generates comprehensive documentation using Ontospy
   - Outputs HTML files to the `docs/` directory

3. **Deployment**: Generated documentation is automatically deployed to the `gh-pages` branch and served via GitHub Pages.

## Local Development

### Prerequisites

- Python 3.9+
- Git

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/Project-VIC-International/cacontology.projectvic.org.git
   cd cacontology.projectvic.org
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Generate documentation locally:
   ```bash
   python scripts/generate_docs.py
   ```

4. View the generated documentation:
   ```bash
   # Open docs/index.html in a web browser
   ```

## Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── deploy_docs.yml      # GitHub Actions workflow
├── scripts/
│   └── generate_docs.py         # Documentation generation script
├── config/                       # Configuration files (optional)
├── docs/                         # Generated documentation (gitignored)
├── CNAME                         # Custom domain configuration
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Custom Domain

The documentation is configured to be served at `cacontology.projectvic.org`. The `CNAME` file ensures GitHub Pages serves the content on this custom domain.

To configure the custom domain:
1. Add the `CNAME` file to the repository (already included)
2. Configure DNS settings at projectvic.org to point to GitHub Pages
3. Enable custom domain in GitHub Pages settings

## Dependencies

- **Ontospy**: Ontology documentation generator
- **ROBOT**: Ontology processing and merging tool
- **rdflib**: RDF processing library

See `requirements.txt` for complete dependency list.

## Contributing

To update the documentation generation process:

1. Make changes to the scripts or configuration
2. Test locally using `python scripts/generate_docs.py`
3. Commit and push to the main branch
4. GitHub Actions will automatically regenerate and deploy the documentation

## License

This documentation automation is part of the CAC Ontology project. See the main [CAC-Ontology repository](https://github.com/Project-VIC-International/CAC-Ontology) for license information.
