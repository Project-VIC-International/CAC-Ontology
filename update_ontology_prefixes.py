#!/usr/bin/env python3
"""
Script to update ontology.unifiedcyberontology.org and ontology.caseontology.org prefixes
across all .ttl and .rq files in the codebase.

Transformation rules:
- UCO: Replace trailing # with / and ensure /uco/ path segment exists
- CASE: Replace trailing # with / at end of path
"""

import re
import os
from pathlib import Path
from typing import List, Tuple

# Directories to process
TARGET_DIRS = [
    "ontology",
    "example_SPARQL_queries",
    "examples_knowledge_graphs",
    "testing"
]

# File extensions to process
FILE_EXTENSIONS = [".ttl", ".rq"]


def update_uco_prefixes(content: str) -> Tuple[str, int]:
    """
    Update UCO ontology prefixes.
    Rules:
    1. <https://ontology.unifiedcyberontology.org/core#> -> <https://ontology.unifiedcyberontology.org/uco/core/>
    2. <https://ontology.unifiedcyberontology.org/uco/core#> -> <https://ontology.unifiedcyberontology.org/uco/core/>
    3. <http://unifiedcyberontology.org/uco/core#> -> <https://ontology.unifiedcyberontology.org/uco/core/>
    4. Also handles sh:namespace string literals
    
    Returns: (updated_content, replacement_count)
    """
    replacements = 0
    
    # Pattern 1: http://unifiedcyberontology.org (old format without ontology. and using http)
    # Match: <http://unifiedcyberontology.org/uco/{namespace}#>
    pattern1 = r'<http://unifiedcyberontology\.org/uco/([^>]+)#>'
    def replacer1(match):
        nonlocal replacements
        namespace = match.group(1)
        replacements += 1
        return f'<https://ontology.unifiedcyberontology.org/uco/{namespace}/>'
    
    content = re.sub(pattern1, replacer1, content)
    
    # Pattern 2: Without /uco/ segment - add it and replace # with /
    # Match: <https://ontology.unifiedcyberontology.org/{namespace}#>
    pattern2 = r'<https://ontology\.unifiedcyberontology\.org/([^/]+)#>'
    def replacer2(match):
        nonlocal replacements
        namespace = match.group(1)
        replacements += 1
        return f'<https://ontology.unifiedcyberontology.org/uco/{namespace}/>'
    
    content = re.sub(pattern2, replacer2, content)
    
    # Pattern 3: With /uco/ segment - just replace # with /
    # Match: <https://ontology.unifiedcyberontology.org/uco/{namespace}#>
    pattern3 = r'<https://ontology\.unifiedcyberontology\.org/uco/([^>]+)#>'
    def replacer3(match):
        nonlocal replacements
        namespace = match.group(1)
        replacements += 1
        return f'<https://ontology.unifiedcyberontology.org/uco/{namespace}/>'
    
    content = re.sub(pattern3, replacer3, content)
    
    # Pattern 4: String literals in sh:namespace (without angle brackets)
    # Match: "https://ontology.unifiedcyberontology.org/{namespace}#"
    pattern4 = r'"https://ontology\.unifiedcyberontology\.org/([^/]+)#"'
    def replacer4(match):
        nonlocal replacements
        namespace = match.group(1)
        replacements += 1
        return f'"https://ontology.unifiedcyberontology.org/uco/{namespace}/"'
    
    content = re.sub(pattern4, replacer4, content)
    
    # Pattern 5: String literals with /uco/ segment
    # Match: "https://ontology.unifiedcyberontology.org/uco/{namespace}#"
    pattern5 = r'"https://ontology\.unifiedcyberontology\.org/uco/([^"]+)#"'
    def replacer5(match):
        nonlocal replacements
        namespace = match.group(1)
        replacements += 1
        return f'"https://ontology.unifiedcyberontology.org/uco/{namespace}/"'
    
    content = re.sub(pattern5, replacer5, content)
    
    # Pattern 6: String literals for http://unifiedcyberontology.org (old format)
    # Match: "http://unifiedcyberontology.org/uco/{namespace}#"
    pattern6 = r'"http://unifiedcyberontology\.org/uco/([^"]+)#"'
    def replacer6(match):
        nonlocal replacements
        namespace = match.group(1)
        replacements += 1
        return f'"https://ontology.unifiedcyberontology.org/uco/{namespace}/"'
    
    content = re.sub(pattern6, replacer6, content)
    
    # Pattern 7: Handle owl:imports with https://ontology.unifiedcyberontology.org/core (no # or /)
    # Match: <https://ontology.unifiedcyberontology.org/core>
    pattern7 = r'<https://ontology\.unifiedcyberontology\.org/core>'
    def replacer7(match):
        nonlocal replacements
        replacements += 1
        return '<https://ontology.unifiedcyberontology.org/uco/core/>'
    
    content = re.sub(pattern7, replacer7, content)
    
    return content, replacements


def update_case_prefixes(content: str) -> Tuple[str, int]:
    """
    Update CASE ontology prefixes.
    Rules:
    1. <https://ontology.caseontology.org/case/investigation#> -> <https://ontology.caseontology.org/case/investigation/>
    2. <https://ontology.caseontology.org/case/vocabulary#> -> <https://ontology.caseontology.org/case/vocabulary/>
    3. Any other ontology.caseontology.org/*#> -> ontology.caseontology.org/*/>
    4. Also handles string literals in sh:namespace
    
    Returns: (updated_content, replacement_count)
    """
    replacements = 0
    
    # Pattern 1: Replace trailing # with / for all caseontology.org paths in angle brackets
    # Match: <https://ontology.caseontology.org/{path}#>
    pattern1 = r'<https://ontology\.caseontology\.org/([^>]+)#>'
    def replacer1(match):
        nonlocal replacements
        path = match.group(1)
        replacements += 1
        return f'<https://ontology.caseontology.org/{path}/>'
    
    content = re.sub(pattern1, replacer1, content)
    
    # Pattern 2: String literals in sh:namespace (without angle brackets)
    # Match: "https://ontology.caseontology.org/{path}#"
    pattern2 = r'"https://ontology\.caseontology\.org/([^"]+)#"'
    def replacer2(match):
        nonlocal replacements
        path = match.group(1)
        replacements += 1
        return f'"https://ontology.caseontology.org/{path}/"'
    
    content = re.sub(pattern2, replacer2, content)
    
    return content, replacements


def process_file(file_path: Path) -> Tuple[bool, int, int]:
    """
    Process a single file and update prefixes.
    Returns: (was_modified, uco_replacements, case_replacements)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False, 0, 0
    
    original_content = content
    
    # Update UCO prefixes
    content, uco_count = update_uco_prefixes(content)
    
    # Update CASE prefixes
    content, case_count = update_case_prefixes(content)
    
    # Write back if changes were made
    if content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, uco_count, case_count
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
            return False, 0, 0
    
    return False, uco_count, case_count


def find_files(base_dir: Path) -> List[Path]:
    """Find all .ttl and .rq files in target directories."""
    files = []
    for target_dir in TARGET_DIRS:
        dir_path = base_dir / target_dir
        if dir_path.exists() and dir_path.is_dir():
            for ext in FILE_EXTENSIONS:
                files.extend(dir_path.rglob(f"*{ext}"))
        else:
            print(f"Warning: Directory {dir_path} does not exist, skipping...")
    return sorted(files)


def main():
    """Main execution function."""
    # Get the script directory (should be CAC-Ontology/)
    script_dir = Path(__file__).parent
    base_dir = script_dir
    
    print("=" * 70)
    print("Ontology Prefix Updater")
    print("=" * 70)
    print(f"Base directory: {base_dir}")
    print(f"Target directories: {', '.join(TARGET_DIRS)}")
    print(f"File extensions: {', '.join(FILE_EXTENSIONS)}")
    print()
    
    # Find all files
    files = find_files(base_dir)
    print(f"Found {len(files)} files to process")
    print()
    
    # Process files
    stats = {
        'total_files': len(files),
        'modified_files': 0,
        'total_uco_replacements': 0,
        'total_case_replacements': 0,
        'errors': 0
    }
    
    modified_files = []
    
    for file_path in files:
        relative_path = file_path.relative_to(base_dir)
        was_modified, uco_count, case_count = process_file(file_path)
        
        if was_modified:
            stats['modified_files'] += 1
            stats['total_uco_replacements'] += uco_count
            stats['total_case_replacements'] += case_count
            modified_files.append((relative_path, uco_count, case_count))
            print(f"[MODIFIED] {relative_path} - UCO: {uco_count}, CASE: {case_count}")
        elif uco_count > 0 or case_count > 0:
            # This shouldn't happen, but just in case
            print(f"[WARNING] {relative_path} - Found patterns but file not modified")
    
    # Print summary
    print()
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"Total files processed: {stats['total_files']}")
    print(f"Files modified: {stats['modified_files']}")
    print(f"Total UCO replacements: {stats['total_uco_replacements']}")
    print(f"Total CASE replacements: {stats['total_case_replacements']}")
    print(f"Total replacements: {stats['total_uco_replacements'] + stats['total_case_replacements']}")
    
    if modified_files:
        print()
        print("Modified files:")
        for file_path, uco_count, case_count in modified_files:
            print(f"  - {file_path} (UCO: {uco_count}, CASE: {case_count})")
    
    print()
    print("Done!")


if __name__ == "__main__":
    main()

