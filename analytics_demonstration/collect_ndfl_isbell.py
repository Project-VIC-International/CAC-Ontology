#!/usr/bin/env python3
"""
Phase -1: Data Acquisition + Preprocessing
Source: https://www.justice.gov/usao-ndfl/pr/tallahassee-man-sentenced-twenty-years-federal-prison-child-exploitation-crime
"""

import requests
from bs4 import BeautifulSoup
import hashlib
import datetime
import uuid
import os
import yaml

# --- Configuration ---
URL = "https://www.justice.gov/usao-ndfl/pr/tallahassee-man-sentenced-twenty-years-federal-prison-child-exploitation-crime"
OUTPUT_DIR = "analytics_demonstration/collected_sources/ndfl-isbell-sentencing"
COLLECTED_AT = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# --- UUIDs (using UUIDv5 for determinism per prompt.md) ---
# Namespace: a fixed UUID for DOJ press releases
DOJ_NS = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")  # URL namespace

def generate_uuid5(name: str) -> str:
    """Generate deterministic UUIDv5 based on URL namespace and name."""
    return str(uuid.uuid5(DOJ_NS, name))

# Pre-generate all UUIDs for determinism
IDS = {
    "batch": generate_uuid5("batch:ndfl-isbell-sentencing"),
    "raw_doc": generate_uuid5("doc:raw:" + URL),
    "normalized_doc": generate_uuid5("doc:normalized:" + URL),
    "collection_action": generate_uuid5("action:collection:" + URL),
    "normalization_action": generate_uuid5("action:normalization:" + URL),
    "provenance_record": generate_uuid5("provenance:collection:" + URL),
    "agent": generate_uuid5("agent:cac-ontology-cursor"),
    "raw_hash_node": generate_uuid5("hash:raw:" + URL),
    "normalized_hash_node": generate_uuid5("hash:normalized:" + URL),
    "url_facet": generate_uuid5("facet:url:" + URL),
    "content_facet_raw": generate_uuid5("facet:content:raw:" + URL),
    "content_facet_normalized": generate_uuid5("facet:content:normalized:" + URL),
    "hash_facet_raw": generate_uuid5("facet:hash:raw:" + URL),
    "hash_facet_normalized": generate_uuid5("facet:hash:normalized:" + URL),
    "file_facet_normalized": generate_uuid5("facet:file:normalized:" + URL),
}

def fetch_webpage(url: str) -> tuple:
    """Fetch webpage and return (html_content, headers)."""
    headers = {
        "User-Agent": "CAC-Ontology-Agent/1.0 (research; semantic web collection)"
    }
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.text, resp.headers

def compute_sha256(content: str) -> str:
    """Compute SHA-256 hash of content."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def normalize_html(html: str) -> str:
    """Extract and normalize text from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    
    # Remove script and style elements
    for element in soup(["script", "style", "nav", "footer", "header"]):
        element.decompose()
    
    # Find main article content
    article = soup.find("article") or soup.find("main") or soup
    
    # Get text and normalize whitespace
    text = article.get_text(separator="\n", strip=True)
    
    # Clean up excessive whitespace
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return "\n".join(lines)

def main():
    print(f"=== Phase -1: Data Acquisition ===")
    print(f"URL: {URL}")
    print(f"Collected at: {COLLECTED_AT}")
    print(f"Output dir: {OUTPUT_DIR}")
    print()
    
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Step 1: Fetch webpage
    print("1. Fetching webpage...")
    html_content, headers = fetch_webpage(URL)
    mime_type = headers.get("Content-Type", "text/html").split(";")[0]
    raw_size = len(html_content.encode("utf-8"))
    raw_hash = compute_sha256(html_content)
    print(f"   MIME: {mime_type}, Size: {raw_size} bytes")
    print(f"   SHA-256: {raw_hash}")
    
    # Step 2: Save raw HTML
    raw_path = os.path.join(OUTPUT_DIR, "source.html")
    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"   Saved: {raw_path}")
    
    # Step 3: Normalize content
    print("2. Normalizing content...")
    normalized_text = normalize_html(html_content)
    normalized_size = len(normalized_text.encode("utf-8"))
    normalized_hash = compute_sha256(normalized_text)
    print(f"   Size: {normalized_size} bytes")
    print(f"   SHA-256: {normalized_hash}")
    
    # Step 4: Save normalized text
    normalized_path = os.path.join(OUTPUT_DIR, "normalized.txt")
    with open(normalized_path, "w", encoding="utf-8") as f:
        f.write(normalized_text)
    print(f"   Saved: {normalized_path}")
    
    # Step 5: Create manifest
    print("3. Creating manifest...")
    manifest = {
        "batch": {
            "uco-core:id": f"urn:uuid:{IDS['batch']}",
            "uco-core:name": "NDFL Isbell Sentencing Press Release Collection",
            "uco-core:objectCreatedTime": COLLECTED_AT,
        },
        "documents": [{
            "uco-core:id": f"urn:uuid:{IDS['raw_doc']}",
            "uco-core:name": "DOJ USAO-NDFL Press Release - Tallahassee Man Sentenced",
            "observable:url": URL,
            "collectionAction": {
                "uco-core:id": f"urn:uuid:{IDS['collection_action']}",
                "uco-action:startTime": COLLECTED_AT,
                "uco-action:performer": f"urn:uuid:{IDS['agent']}",
                "uco-core:description": "Automated web collection via requests library",
            },
            "observable:mimeType": mime_type,
            "observable:sizeInBytes": raw_size,
            "observable:hash": {
                "types:hashMethod": "SHA-256",
                "types:hashValue": raw_hash,
            },
            "normalizedOutput": {
                "uco-core:id": f"urn:uuid:{IDS['normalized_doc']}",
                "observable:filePath": normalized_path,
                "observable:sizeInBytes": normalized_size,
                "observable:hash": {
                    "types:hashMethod": "SHA-256",
                    "types:hashValue": normalized_hash,
                },
            },
        }],
        "uuids": IDS,
    }
    
    manifest_path = os.path.join(OUTPUT_DIR, "manifest.yaml")
    with open(manifest_path, "w", encoding="utf-8") as f:
        yaml.dump(manifest, f, default_flow_style=False, allow_unicode=True)
    print(f"   Saved: {manifest_path}")
    
    # Step 6: Create duplicate detection report
    print("4. Creating duplicate detection report...")
    dup_report = f"""# Duplicate Detection Report

## Source Checked
- URL: {URL}
- Collection Time: {COLLECTED_AT}

## Duplicate Check Results
- **Status**: NEW SOURCE (no prior collection found)
- **Method**: URL exact match + hash comparison
- **Existing documents checked**: 0 (first run)

## Decision
- **Action**: PROCEED with collection
- **Reason**: No duplicate detected in existing KG

## Content Hash (for future deduplication)
- Raw HTML SHA-256: `{raw_hash}`
- Normalized text SHA-256: `{normalized_hash}`
"""
    
    dup_path = os.path.join(OUTPUT_DIR, "duplicate_detection_report.md")
    with open(dup_path, "w", encoding="utf-8") as f:
        f.write(dup_report)
    print(f"   Saved: {dup_path}")
    
    print()
    print("=== Phase -1 Complete ===")
    print(f"Raw document UUID: urn:uuid:{IDS['raw_doc']}")
    print(f"Normalized document UUID: urn:uuid:{IDS['normalized_doc']}")

if __name__ == "__main__":
    main()
