#!/usr/bin/env python3
"""
Comprehensive SHACL validation for CAC Ontology v3.0.0.
Validates every ontology module against its corresponding shapes file,
and validates example knowledge graphs against relevant shapes.
"""

import glob, os, sys, time

os.chdir(os.path.join(os.path.dirname(__file__), '..'))

try:
    import rdflib
    from pyshacl import validate
except ImportError:
    print("ERROR: rdflib and pyshacl required. Run: pip install rdflib pyshacl")
    sys.exit(1)

print("=" * 70)
print("  CAC Ontology v3.0.0 — Comprehensive SHACL Validation")
print("=" * 70)

start_time = time.time()
passed = 0
failed = 0
errors = []

# ============================================================
# Stage 1: Validate each ontology module against its shapes
# ============================================================
print("\n[Stage 1] Validating ontology modules against shapes files...\n")

ontology_files = sorted(glob.glob(os.path.join('ontology', '*.ttl')))
shapes_files = {os.path.basename(f) for f in ontology_files if '-shapes' in f}

for f in ontology_files:
    bn = os.path.basename(f)
    if '-shapes' in bn or 'bridge' in bn or 'spine' in bn or 'integration' in bn:
        continue
    
    shapes_name = bn.replace('.ttl', '-shapes.ttl')
    shapes_path = os.path.join('ontology', shapes_name)
    
    if shapes_name not in shapes_files:
        continue
    
    try:
        data_graph = rdflib.Graph()
        data_graph.parse(f, format='turtle')
        
        shapes_graph = rdflib.Graph()
        shapes_graph.parse(shapes_path, format='turtle')
        
        conforms, results_graph, results_text = validate(
            data_graph,
            shacl_graph=shapes_graph,
            inference='none',
            abort_on_first=False,
            allow_infos=True,
            allow_warnings=True,
        )
        
        if conforms:
            print(f"  PASS: {bn} (shapes: {shapes_name})")
            passed += 1
        else:
            violation_count = 0
            warning_count = 0
            info_count = 0
            for s, p, o in results_graph.triples((None, rdflib.URIRef('http://www.w3.org/ns/shacl#resultSeverity'), None)):
                sev = str(o)
                if 'Violation' in sev:
                    violation_count += 1
                elif 'Warning' in sev:
                    warning_count += 1
                elif 'Info' in sev:
                    info_count += 1
            
            if violation_count > 0:
                print(f"  FAIL: {bn} — {violation_count} violations, {warning_count} warnings")
                failed += 1
                for line in results_text.strip().split('\n')[:10]:
                    errors.append(f"  {bn}: {line}")
            else:
                print(f"  PASS: {bn} (warnings: {warning_count}, info: {info_count})")
                passed += 1
    except Exception as e:
        err_msg = str(e).split('\n')[0][:100]
        print(f"  ERROR: {bn} — {err_msg}")
        failed += 1
        errors.append(f"  {bn}: {err_msg}")

# ============================================================
# Stage 2: Validate shapes files parse correctly
# ============================================================
print(f"\n[Stage 2] Validating all shapes files parse correctly...\n")

shapes_parsed = 0
shapes_failed = 0
for f in sorted(glob.glob(os.path.join('ontology', '*-shapes.ttl'))):
    bn = os.path.basename(f)
    try:
        g = rdflib.Graph()
        g.parse(f, format='turtle')
        
        shapes_count = 0
        for s, p, o in g.triples((None, rdflib.RDF.type, rdflib.URIRef('http://www.w3.org/ns/shacl#NodeShape'))):
            shapes_count += 1
        for s, p, o in g.triples((None, rdflib.RDF.type, rdflib.URIRef('http://www.w3.org/ns/shacl#PropertyShape'))):
            shapes_count += 1
        
        print(f"  OK: {bn} ({shapes_count} shapes)")
        shapes_parsed += 1
    except Exception as e:
        print(f"  FAIL: {bn} — {str(e).split(chr(10))[0][:80]}")
        shapes_failed += 1
        errors.append(f"  {bn}: parse error")

# ============================================================
# Stage 3: Validate example KGs against core shapes
# ============================================================
print(f"\n[Stage 3] Validating example knowledge graphs against core shapes...\n")

known_parse_exceptions = {
    'utah-dominic-christensen-Autopsy-report.ttl',
}

core_shapes = rdflib.Graph()
core_shapes.parse(os.path.join('ontology', 'cacontology-core-shapes.ttl'), format='turtle')

example_passed = 0
example_failed = 0
example_skipped = 0

for f in sorted(glob.glob(os.path.join('examples_knowledge_graphs', '*.ttl'))):
    bn = os.path.basename(f)
    if bn in known_parse_exceptions:
        example_skipped += 1
        continue
    
    try:
        data_graph = rdflib.Graph()
        data_graph.parse(f, format='turtle')
        
        conforms, results_graph, results_text = validate(
            data_graph,
            shacl_graph=core_shapes,
            inference='none',
            abort_on_first=False,
            allow_infos=True,
            allow_warnings=True,
        )
        
        if conforms:
            print(f"  PASS: {bn}")
            example_passed += 1
        else:
            violation_count = 0
            for s, p, o in results_graph.triples((None, rdflib.URIRef('http://www.w3.org/ns/shacl#resultSeverity'), None)):
                if 'Violation' in str(o):
                    violation_count += 1
            
            if violation_count > 0:
                print(f"  FAIL: {bn} — {violation_count} violations")
                example_failed += 1
                for line in results_text.strip().split('\n')[:5]:
                    errors.append(f"  {bn}: {line}")
            else:
                print(f"  PASS: {bn} (warnings only)")
                example_passed += 1
    except Exception as e:
        print(f"  ERROR: {bn} — {str(e).split(chr(10))[0][:80]}")
        example_failed += 1

# ============================================================
# Stage 4: Cross-validate domain examples against domain shapes
# ============================================================
print(f"\n[Stage 4] Cross-validating examples against domain-specific shapes...\n")

domain_validations = [
    ('examples_knowledge_graphs/hotline-lifecycle.ttl', 'ontology/cacontology-hotlines-shapes.ttl'),
    ('examples_knowledge_graphs/miami-icac-felipe-lopez-example.ttl', 'ontology/cacontology-undercover-shapes.ttl'),
    ('examples_knowledge_graphs/miami-icac-felipe-lopez-example.ttl', 'ontology/cacontology-tactical-shapes.ttl'),
    ('examples_knowledge_graphs/miami-icac-felipe-lopez-example.ttl', 'ontology/cacontology-legal-outcomes-shapes.ttl'),
    ('examples_knowledge_graphs/k2p-soe-information-example.ttl', 'ontology/cacontology-sadistic-online-exploitation-shapes.ttl'),
    ('examples_knowledge_graphs/k2p-soe-information-example.ttl', 'ontology/cacontology-sextortion-shapes.ttl'),
]

domain_passed = 0
domain_failed = 0

for data_path, shapes_path in domain_validations:
    if not os.path.exists(data_path) or not os.path.exists(shapes_path):
        continue
    
    data_bn = os.path.basename(data_path)
    shapes_bn = os.path.basename(shapes_path)
    
    try:
        data_graph = rdflib.Graph()
        data_graph.parse(data_path, format='turtle')
        
        shapes_graph = rdflib.Graph()
        shapes_graph.parse(shapes_path, format='turtle')
        
        conforms, results_graph, results_text = validate(
            data_graph,
            shacl_graph=shapes_graph,
            inference='none',
            abort_on_first=False,
            allow_infos=True,
            allow_warnings=True,
        )
        
        if conforms:
            print(f"  PASS: {data_bn} vs {shapes_bn}")
            domain_passed += 1
        else:
            violation_count = 0
            for s, p, o in results_graph.triples((None, rdflib.URIRef('http://www.w3.org/ns/shacl#resultSeverity'), None)):
                if 'Violation' in str(o):
                    violation_count += 1
            
            if violation_count > 0:
                print(f"  FAIL: {data_bn} vs {shapes_bn} — {violation_count} violations")
                domain_failed += 1
            else:
                print(f"  PASS: {data_bn} vs {shapes_bn} (warnings only)")
                domain_passed += 1
    except Exception as e:
        print(f"  ERROR: {data_bn} vs {shapes_bn} — {str(e).split(chr(10))[0][:80]}")
        domain_failed += 1

# ============================================================
# SUMMARY
# ============================================================
elapsed = time.time() - start_time
total_fail = failed + shapes_failed + example_failed + domain_failed
total_pass = passed + shapes_parsed + example_passed + domain_passed

print("\n" + "=" * 70)
print("  SHACL VALIDATION SUMMARY")
print("=" * 70)
print(f"  Ontology vs Shapes:   {passed} pass / {failed} fail")
print(f"  Shapes parsing:       {shapes_parsed} pass / {shapes_failed} fail")
print(f"  Example KGs (core):   {example_passed} pass / {example_failed} fail / {example_skipped} skipped")
print(f"  Domain cross-checks:  {domain_passed} pass / {domain_failed} fail")
print(f"  Total:                {total_pass} pass / {total_fail} fail")
print(f"  Time:                 {elapsed:.1f}s")
print()

if errors:
    print("  DETAILED ERRORS:")
    for e in errors[:30]:
        print(f"    {e}")
    if len(errors) > 30:
        print(f"    ... and {len(errors) - 30} more")
    print()

if total_fail == 0:
    print("  >>> ALL SHACL VALIDATIONS PASS <<<")
else:
    print(f"  >>> {total_fail} FAILURES <<<")

sys.exit(0 if total_fail == 0 else 1)
