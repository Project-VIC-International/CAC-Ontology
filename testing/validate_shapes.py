#!/usr/bin/env python3
"""
CAC Ontology SHACL Shapes Validation Script
Validates all SHACL shapes files for syntactic correctness and generates coverage report.
"""

import rdflib
import os
import glob

def main():
    print('CAC Ontology SHACL Shapes Validation Report')
    print('=' * 50)

    # Shapes live under ontology/ in this repo
    shapes_files = glob.glob(os.path.join('ontology', '*-shapes.ttl'))
    total_files = len(shapes_files)
    valid_files = 0
    total_triples = 0

    print(f'Total SHACL shapes files found: {total_files}')
    print()

    if total_files == 0:
        print("ERROR: No SHACL shapes files found under ontology/.")
        return

    for i, file in enumerate(sorted(shapes_files), 1):
        try:
            g = rdflib.Graph()
            g.parse(file, format='turtle')
            triples = len(g)
            total_triples += triples
            valid_files += 1
            print(f'OK  {i:2d}. {file:<45} ({triples:3d} triples)')
        except Exception as e:
            print(f'ERR {i:2d}. {file:<45} ERROR: {str(e)[:50]}...')

    print()
    print('VALIDATION SUMMARY')
    print('=' * 50)
    print(f'Valid files:     {valid_files}/{total_files} ({valid_files/total_files*100:.1f}%)')
    print(f'Total triples:   {total_triples:,}')
    print(f'Average triples: {total_triples/total_files:.0f} per file')
    print()

    if valid_files == total_files:
        print('SUCCESS: All SHACL shapes files are syntactically valid!')
        print('100% coverage: all shapes files parsed.')
    else:
        print(f'WARNING: {total_files - valid_files} files have syntax errors')

if __name__ == '__main__':
    main() 