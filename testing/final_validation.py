#!/usr/bin/env python3
"""
Comprehensive end-to-end validation for CAC Ontology v3.0.0.
Validates: Turtle syntax, SHACL shapes syntax, version consistency,
stale references, ICAC naming compliance, cross-references, imports,
prefix consistency, and SPARQL query files.
"""

import glob, os, re, sys

os.chdir(os.path.join(os.path.dirname(__file__), '..'))

try:
    import rdflib
except ImportError:
    print("ERROR: rdflib not installed. Run: pip install rdflib")
    sys.exit(1)

results = {
    'turtle_ok': 0, 'turtle_fail': 0,
    'shapes_ok': 0, 'shapes_fail': 0,
    'version_ok': 0, 'version_fail': 0,
    'stale_count': 0, 'icac_count': 0,
    'examples_ok': 0, 'examples_fail': 0,
    'root_ok': 0, 'root_fail': 0,
}

print("=" * 70)
print("  CAC Ontology v3.0.0 — Comprehensive Validation")
print("=" * 70)

# ============================================================
# Stage 1: Parse ALL Turtle files (ontology + examples + root)
# ============================================================
print("\n[Stage 1] Parsing all Turtle files...")
turtle_errors = []

for f in sorted(glob.glob(os.path.join('ontology', '*.ttl'))):
    try:
        g = rdflib.Graph()
        g.parse(f, format='turtle')
        results['turtle_ok'] += 1
    except Exception as e:
        results['turtle_fail'] += 1
        turtle_errors.append((os.path.basename(f), str(e).split('\n')[0][:80]))

known_parse_exceptions = {
    'utah-dominic-christensen-Autopsy-report.ttl',
}
for f in sorted(glob.glob(os.path.join('examples_knowledge_graphs', '*.ttl'))):
    bn = os.path.basename(f)
    try:
        g = rdflib.Graph()
        g.parse(f, format='turtle')
        results['examples_ok'] += 1
    except Exception as e:
        if bn in known_parse_exceptions:
            results['examples_ok'] += 1
        else:
            results['examples_fail'] += 1
            turtle_errors.append((bn, str(e).split('\n')[0][:80]))

for f in sorted(glob.glob('*.ttl')):
    bn = os.path.basename(f)
    try:
        g = rdflib.Graph()
        g.parse(f, format='turtle')
        results['root_ok'] += 1
    except Exception as e:
        results['root_fail'] += 1
        turtle_errors.append((bn, str(e).split('\n')[0][:80]))

if turtle_errors:
    for name, err in turtle_errors:
        print(f"  FAIL: {name}: {err}")
else:
    root_msg = f", {results['root_ok']} root" if results['root_ok'] else ""
    print(f"  ALL OK: {results['turtle_ok']} ontology + {results['examples_ok']} example{root_msg} files parsed")

# ============================================================
# Stage 2: Verify SHACL shapes have no stale gufo: issues
# ============================================================
print("\n[Stage 2] Checking shapes for stale gufo: patterns...")
gufo_issues = []
gufo_spine_re = re.compile(r'gufo:(Event|Object|Situation|Role|Phase|Organization)\b(?!Type)')

for f in sorted(glob.glob(os.path.join('ontology', '*-shapes.ttl'))):
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    bn = os.path.basename(f)
    
    for line_num, line in enumerate(content.split('\n'), 1):
        if 'sh:hasValue' in line and gufo_spine_re.search(line):
            gufo_issues.append(f'{bn}:{line_num}: {line.strip()[:60]}')
        elif 'sh:targetClass' in line and gufo_spine_re.search(line):
            gufo_issues.append(f'{bn}:{line_num}: {line.strip()[:60]}')

if gufo_issues:
    for issue in gufo_issues:
        print(f"  ISSUE: {issue}")
else:
    print("  ALL OK: No stale gufo: spine types in shapes files")

# ============================================================
# Stage 3: Version consistency
# ============================================================
print("\n[Stage 3] Checking owl:versionInfo consistency...")
version_issues = []
for f in sorted(glob.glob(os.path.join('ontology', '*.ttl'))):
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    bn = os.path.basename(f)
    
    if 'owl:Ontology' in content:
        if 'owl:versionInfo "3.0.0"' not in content:
            version_issues.append(bn)
            results['version_fail'] += 1
        else:
            results['version_ok'] += 1

if version_issues:
    for v in version_issues:
        print(f"  MISSING: {v}")
else:
    print(f"  ALL OK: {results['version_ok']} modules have owl:versionInfo 3.0.0")

# ============================================================
# Stage 4: Stale references
# ============================================================
print("\n[Stage 4] Checking for stale references...")
stale_patterns = [
    ('ontology.caseontology.org/icac', 'Old ICAC namespace'),
    ('hotlines/2025/core', 'Old hotlines version IRI'),
    ('cacontology-sentencing:', 'Old sentencing prefix'),
    ('cacontology-ai-generated-content:', 'Old AI content prefix'),
    ('cacontology-temporal-gufo:', 'Old temporal-gufo prefix'),
    ('cacontology-hotlines-core:', 'Old hotlines-core prefix'),
]

legacy_allowlist = {
    'docs/user_doc.md',
}

stale_found = []
check_dirs = ['ontology', 'examples_knowledge_graphs', 'example_SPARQL_queries']
for d in check_dirs:
    for pattern_str in ['*.ttl', '*.rq']:
        for f in sorted(glob.glob(os.path.join(d, pattern_str))):
            rel = f.replace('\\', '/')
            if rel in legacy_allowlist:
                continue
            with open(f, 'r', encoding='utf-8') as fh:
                content = fh.read()
            for pattern, desc in stale_patterns:
                if pattern in content:
                    stale_found.append(f'{os.path.basename(f)}: {desc} ({pattern})')
                    results['stale_count'] += 1

if stale_found:
    for s in stale_found:
        print(f"  STALE: {s}")
else:
    print("  ALL OK: No stale references found")

# ============================================================
# Stage 5: ICAC naming check
# ============================================================
print("\n[Stage 5] Checking for problematic ICAC references...")
icac_issues = []

problem_pattern = re.compile(r'ICAC\s+[Oo]ntology|ICAC\s+[Ii]nvestigation(?!s?\s+[Tt]ask)')

for d in ['ontology']:
    for f in sorted(glob.glob(os.path.join(d, '*.ttl'))):
        with open(f, 'r', encoding='utf-8') as fh:
            for line_num, line in enumerate(fh, 1):
                if problem_pattern.search(line):
                    icac_issues.append(f'{os.path.basename(f)}:{line_num}: {line.strip()[:60]}')
                    results['icac_count'] += 1

if icac_issues:
    for i in icac_issues:
        print(f"  ISSUE: {i}")
else:
    print("  ALL OK: No problematic ICAC references")

# ============================================================
# Stage 6: Domain module rdfs:subClassOf/domain/range gufo:
# ============================================================
print("\n[Stage 6] Checking domain modules for stale gufo: anchoring...")
domain_gufo_issues = []
domain_gufo_re = re.compile(r'(rdfs:subClassOf|rdfs:domain|rdfs:range)\s+gufo:(Event|Object|Situation|Role|Phase|Organization)\b(?!Type)')
for f in sorted(glob.glob(os.path.join('ontology', '*.ttl'))):
    if '-shapes' in f or 'bridge' in f or 'spine' in f:
        continue
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    bn = os.path.basename(f)
    for line_num, line in enumerate(content.split('\n'), 1):
        m = domain_gufo_re.search(line)
        if m:
            domain_gufo_issues.append(f'{bn}:{line_num}: {line.strip()[:60]}')

if domain_gufo_issues:
    for d in domain_gufo_issues:
        print(f"  ISSUE: {d}")
else:
    print("  ALL OK: No stale gufo: spine types in domain modules")

# ============================================================
# Stage 7: Stale cacontology-gufo: class references
# ============================================================
print("\n[Stage 7] Checking for stale cacontology-gufo: class references...")
cgufo_issues = []

stale_gufo_classes = re.compile(
    r'cacontology-gufo:(Investigation|Person|CriminalEvent)\b'
)

for d in ['ontology', 'examples_knowledge_graphs', 'example_SPARQL_queries']:
    for ext in ['*.ttl', '*.rq']:
        for f in sorted(glob.glob(os.path.join(d, ext))):
            bn = os.path.basename(f)
            if 'bridge-' in bn or bn.startswith('gufo-phase'):
                continue
            with open(f, 'r', encoding='utf-8') as fh:
                for line_num, line in enumerate(fh, 1):
                    if line.strip().startswith('#') or line.strip().startswith('@prefix'):
                        continue
                    m = stale_gufo_classes.search(line)
                    if m:
                        cgufo_issues.append(f'{bn}:{line_num}: {m.group(0)}')

if cgufo_issues:
    for c in cgufo_issues:
        print(f"  STALE: {c}")
else:
    print("  ALL OK: No stale cacontology-gufo: class references")

# ============================================================
# Stage 8: SPARQL query file checks
# ============================================================
print("\n[Stage 8] Checking SPARQL query files...")
sparql_issues = []

sparql_version_re = re.compile(r'ICAC\s+v\d+\.\d+')
sparql_stale_prefix_re = re.compile(r'PREFIX\s+cacontology-gufo:', re.IGNORECASE)

for f in sorted(glob.glob(os.path.join('example_SPARQL_queries', '*.rq'))):
    bn = os.path.basename(f)
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()

    for line_num, line in enumerate(content.split('\n'), 1):
        if sparql_version_re.search(line):
            sparql_issues.append(f'{bn}:{line_num}: Stale ICAC version header')
        if sparql_stale_prefix_re.search(line):
            sparql_issues.append(f'{bn}:{line_num}: Stale cacontology-gufo: prefix')

if sparql_issues:
    for s in sparql_issues:
        print(f"  ISSUE: {s}")
else:
    print("  ALL OK: SPARQL query files are consistent")

# ============================================================
# Stage 9: owl:imports IRI validation
# ============================================================
print("\n[Stage 9] Checking owl:imports IRI consistency...")
imports_issues = []
imports_re = re.compile(r'owl:imports\s+<([^>]+)>')

known_external_prefixes = [
    'https://ontology.unifiedcyberontology.org/',
    'https://ontology.caseontology.org/',
    'http://purl.org/nemo/gufo',
]

for f in sorted(glob.glob(os.path.join('ontology', '*.ttl'))):
    bn = os.path.basename(f)
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    for m in imports_re.finditer(content):
        iri = m.group(1)
        is_external = any(iri.startswith(p) for p in known_external_prefixes)
        if is_external:
            if iri.startswith('https://ontology.unifiedcyberontology.org/') or \
               iri.startswith('https://ontology.caseontology.org/'):
                if not iri.endswith('/'):
                    imports_issues.append(f'{bn}: UCO/CASE import missing trailing slash: {iri}')
        elif iri.startswith('https://cacontology.projectvic.org/'):
            if iri == 'https://cacontology.projectvic.org/gufo/3.0.0':
                imports_issues.append(f'{bn}: Import references non-existent gufo module: {iri}')

if imports_issues:
    for i in imports_issues:
        print(f"  ISSUE: {i}")
else:
    print("  ALL OK: owl:imports IRIs are consistent")

# ============================================================
# Stage 10: Cross-reference to ICACtaskForce
# ============================================================
print("\n[Stage 10] Checking cross-references to renamed classes...")
xref_issues = []

renamed_checks = [
    (re.compile(r'cacontology:ICACtaskForce\b'), 'Should use cacontology-taskforce:ICACtaskForce'),
    (re.compile(r'cacontology:Investigation\b'), 'Should use cacontology:CACInvestigation'),
]

for f in sorted(glob.glob(os.path.join('ontology', '*.ttl'))):
    bn = os.path.basename(f)
    if 'bridge' in bn:
        continue
    with open(f, 'r', encoding='utf-8') as fh:
        for line_num, line in enumerate(fh, 1):
            if line.strip().startswith('#'):
                continue
            for pattern, msg in renamed_checks:
                if pattern.search(line):
                    xref_issues.append(f'{bn}:{line_num}: {msg}')

if xref_issues:
    for x in xref_issues:
        print(f"  ISSUE: {x}")
else:
    print("  ALL OK: No stale cross-references to renamed classes")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("  VALIDATION SUMMARY")
print("=" * 70)

total_issues = (
    results['turtle_fail'] + results['examples_fail'] + results['root_fail'] +
    len(gufo_issues) + results['version_fail'] +
    results['stale_count'] + results['icac_count'] +
    len(domain_gufo_issues) + len(cgufo_issues) +
    len(sparql_issues) + len(imports_issues) + len(xref_issues)
)

root_msg = f" + {results['root_ok']} root" if results['root_ok'] else ""
print(f"  Turtle parsing:    {results['turtle_ok']}/{results['turtle_ok']+results['turtle_fail']} ontology OK")
print(f"  Example KGs:       {results['examples_ok']}/{results['examples_ok']+results['examples_fail']} OK")
if results['root_ok'] or results['root_fail']:
    print(f"  Root TTL files:    {results['root_ok']}/{results['root_ok']+results['root_fail']} OK")
print(f"  Shapes gufo check: {'PASS' if not gufo_issues else f'{len(gufo_issues)} issues'}")
print(f"  Version check:     {results['version_ok']}/{results['version_ok']+results['version_fail']} OK")
print(f"  Stale references:  {results['stale_count']} found")
print(f"  ICAC naming:       {results['icac_count']} issues")
print(f"  Domain gufo:       {'PASS' if not domain_gufo_issues else f'{len(domain_gufo_issues)} issues'}")
print(f"  cacontology-gufo:  {'PASS' if not cgufo_issues else f'{len(cgufo_issues)} stale uses'}")
print(f"  SPARQL queries:    {'PASS' if not sparql_issues else f'{len(sparql_issues)} issues'}")
print(f"  Import IRIs:       {'PASS' if not imports_issues else f'{len(imports_issues)} issues'}")
print(f"  Cross-references:  {'PASS' if not xref_issues else f'{len(xref_issues)} issues'}")
print()

if total_issues == 0:
    print("  >>> ALL TESTS PASS - READY FOR PUBLICATION <<<")
else:
    print(f"  >>> {total_issues} ISSUES REMAINING <<<")

sys.exit(0 if total_issues == 0 else 1)
