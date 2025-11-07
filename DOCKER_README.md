# CAC Ontology Docker Development Environment

This Docker Compose environment provides a comprehensive development and validation setup for the CAC Ontology Family with 23 specialized modules.

## Services Overview

### 1. Apache Jena Fuseki (`fuseki`)
- **Port**: 3030
- **Purpose**: SPARQL endpoint and triple store
- **Features**:
  - Loads all 23 core ontology modules automatically
  - 4GB heap size for handling large datasets
  - Web interface at http://localhost:3030
  - Dataset name: `/CAC`

### 2. pySHACL Validator (`pyshacl`)
- **Purpose**: Comprehensive SHACL validation
- **Features**:
  - Validates all core ontologies against their SHACL shapes
  - Validates 23+ example files across all domains
  - Organized validation by category (Athletic, Production, Multi-Jurisdictional, etc.)
  - Continuous validation monitoring

### 3. ROBOT Framework (`robot`)
- **Purpose**: Ontology processing and manipulation
- **Features**:
  - Ontology validation and reasoning
  - Merging and transformation capabilities
  - SPARQL query execution
  - Interactive command-line access

### 4. GraphDB (`graphdb`)
- **Port**: 7200
- **Purpose**: Advanced graph database with reasoning
- **Features**:
  - Web interface at http://localhost:7200
  - 4GB heap size for large-scale operations
  - Persistent data storage
  - Advanced reasoning capabilities

## Quick Start

### Start All Services
```bash
cd ontology/CAC
docker-compose up -d
```

### Check Service Status
```bash
docker-compose ps
```

### View Validation Results
```bash
docker-compose logs pyshacl
```

### Access Web Interfaces
- **Fuseki**: http://localhost:3030
- **GraphDB**: http://localhost:7200

## Validation Categories

The pySHACL service validates examples in organized categories:

### Core Ontology Validation
- `hotlines-core.ttl` against `hotlines-core-shapes.ttl`
- `cacontology-core.ttl` against `cacontology-core-shapes.ttl`
- `cacontology-forensics.ttl` against `cacontology-forensics-shapes.ttl`
- `cacontology-educational-exploitation.ttl` against `cacontology-educational-shapes.ttl`
- `cacontology-sex-trafficking.ttl` against `cacontology-trafficking-shapes.ttl`
- `cacontology-athletic-exploitation.ttl` against `cacontology-athletic-exploitation-shapes.ttl`
- `cacontology-production.ttl` against `cacontology-production-shapes.ttl`
- `cacontology-custodial.ttl` against `cacontology-custodial-shapes.ttl`
- `cacontology-grooming.ttl` against `cacontology-grooming-shapes.ttl`
- `cacontology-sextortion.ttl` against `cacontology-sextortion-shapes.ttl`
- `cacontology-victim-impact.ttl` against `cacontology-victim-impact-shapes.ttl`
- `cacontology-undercover.ttl` against `cacontology-undercover-shapes.ttl`

### Example Validation Categories
1. **Basic Examples**: Core lifecycle examples
2. **Athletic Exploitation**: Brooklyn Morton coaching case
3. **Production Cases**: Rhode Island HSI and Douglas cases
4. **Multi-Jurisdictional**: Arkansas, Illinois, international operations
5. **Registry Operations**: Sex offender registry integration
6. **Interstate Cases**: Buffalo-Vermont, Hartford-Vermont cases
7. **Sextortion**: Washington state sextortion case
8. **International Operations**: Cumberland, Europol, South Africa cases
9. **Recent Brooklyn Cases**: 2024-2025 Brooklyn DA cases

## Interactive Usage

### ROBOT Framework Commands
```bash
# Access ROBOT container
docker exec -it CAC_robot bash

# Validate ontologies
robot validate *.ttl

# Merge ontologies
robot merge --input cacontology-core.ttl --input hotlines-core.ttl --output merged.ttl

# Run reasoning
robot reason --input cacontology-core.ttl --reasoner hermit

# Execute SPARQL queries
robot query --input cacontology-core.ttl --query queries/find_open_reports.rq
```

### Fuseki SPARQL Queries
```bash
# Access Fuseki web interface
open http://localhost:3030

# Example SPARQL query for athletic coaching cases
PREFIX cacontology-athletic: <https://ontology.unifiedcyberontology.org/CAC/athletic#>
SELECT ?exploitation ?sportType ?teamSize
WHERE {
    ?exploitation a cacontology-athletic:AthleticCoachingExploitation ;
                  cacontology-athletic:sportType ?sportType ;
                  cacontology-athletic:teamSize ?teamSize .
}
```

### GraphDB Operations
```bash
# Access GraphDB web interface
open http://localhost:7200

# Import additional data
# Use the Import tab in GraphDB workbench
# Select files from /opt/graphdb/import/ directory
```

## Loaded Ontology Modules

The Fuseki service automatically loads all 23 core modules:

### Core Framework (3 modules)
- `cacontology-core.ttl`
- `hotlines-core.ttl`
- `cacontology-us-ncmec.ttl`

### International & Global (4 modules)
- `cacontology-international.ttl`
- `cacontology-training.ttl`
- `cacontology-prevention.ttl`
- `cacontology-legal-harmonization.ttl`

### Criminal Activities (5 modules)
- `cacontology-production.ttl`
- `cacontology-custodial.ttl`
- `cacontology-grooming.ttl`
- `cacontology-sextortion.ttl`
- `cacontology-athletic-exploitation.ttl`

### Investigation (5 modules)
- `cacontology-undercover.ttl`
- `cacontology-physical-evidence.ttl`
- `cacontology-tactical.ttl`
- `cacontology-multi-jurisdiction.ttl`
- `cacontology-stranger-abduction.ttl`

### Technical (4 modules)
- `cacontology-forensics.ttl`
- `cacontology-detection.ttl`
- `cacontology-platforms.ttl`
- `cacontology-street-recruitment.ttl`

### Victim Services & Legal (5 modules)
- `cacontology-victim-impact.ttl`
- `cacontology-taskforce.ttl`
- `cacontology-sentencing.ttl`
- `cacontology-specialized-units.ttl`
- `cacontology-sex-offender-registry.ttl`

### Additional Modules
- `cacontology-asset-forfeiture.ttl`
- `cacontology-educational-exploitation.ttl`
- `cacontology-ai-generated-content.ttl`
- `cacontology-platform-infrastructure.ttl`

## Development Workflow

### 1. Make Changes
Edit ontology files or add new examples

### 2. Validate Changes
```bash
# Restart validation
docker-compose restart pyshacl

# Check validation results
docker-compose logs pyshacl
```

### 3. Test SPARQL Queries
```bash
# Access Fuseki
open http://localhost:3030

# Test queries against updated data
```

### 4. Advanced Processing
```bash
# Use ROBOT for advanced operations
docker exec -it CAC_robot bash
robot validate your-new-ontology.ttl
```

## Troubleshooting

### Memory Issues
If you encounter memory issues with large datasets:
```bash
# Increase heap sizes in docker-compose.yaml
# Fuseki: FUSEKI_JVM_ARGS=-Xmx8g
# GraphDB: GDB_HEAP_SIZE=8g
```

### Validation Failures
```bash
# Check specific validation errors
docker-compose logs pyshacl | grep -A 10 "Validation Result"

# Validate individual files
docker exec CAC_pyshacl pyshacl -s /app/ontology/CAC/cacontology-core-shapes.ttl -d /app/ontology/CAC/your-file.ttl -f human
```

### Port Conflicts
If ports 3030 or 7200 are in use:
```bash
# Modify ports in docker-compose.yaml
# Change "3030:3030" to "3031:3030" for Fuseki
# Change "7200:7200" to "7201:7200" for GraphDB
```

## Performance Monitoring

### Resource Usage
```bash
# Monitor container resource usage
docker stats

# Check individual container logs
docker-compose logs fuseki
docker-compose logs graphdb
```

### Query Performance
- Fuseki provides query execution statistics in the web interface
- GraphDB offers detailed performance monitoring in the workbench
- Target: Q1 queries should complete in ≤ 500ms on 5M triples

## Data Persistence

- **GraphDB**: Data persists in the `graphdb_data` Docker volume
- **Fuseki**: Data is loaded fresh on each startup from ontology files
- **Validation Results**: Available in container logs

## Cleanup

### Stop Services
```bash
docker-compose down
```

### Remove All Data
```bash
docker-compose down -v
docker system prune -f
```

## Integration with CI/CD

This Docker environment is designed to support automated testing:

```bash
# Automated validation in CI
docker-compose up -d pyshacl
docker-compose logs pyshacl | grep -q "All ontologies and examples validated successfully!"
echo $? # Should return 0 for success
```

## Support

For issues with the Docker environment:
1. Check container logs: `docker-compose logs [service-name]`
2. Verify file permissions and paths
3. Ensure sufficient system resources (8GB+ RAM recommended)
4. Review the main project documentation in `README.md` 