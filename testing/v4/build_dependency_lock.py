#!/usr/bin/env python3
"""Generate the content-addressed local import catalog without network access."""

from __future__ import annotations

import hashlib
import json
from importlib.metadata import version
from pathlib import Path

from rdflib import Graph, OWL, RDF, URIRef

PACKAGES = ("rdflib", "pyshacl", "owlrl", "html5rdf", "packaging", "prettytable", "pyparsing", "wcwidth")
OVERLAY_REVISION = "4b98b9881aa29ed80f39b589d15725fa696c921a"
OVERLAY_ARCHIVE_SHA256 = "e8298fa86e24432947901c8b574378bee4b3d3d8cf946a25f37d912908d0c8d6"
UCO_REVISION = "7ebb3957e9e9a2e1bb9c66cd1ede8c912a726344"
CDO_SHAPES_GUFO_REVISION = "1b13dd56308261f451db3e304ce7a5e044ed0297"
COLLECTIONS_REVISION = "619e7b02646321174635fd04be658e338bf7d1d7"
SPAR_ERROR_REVISION = "101aca952ef854505f49725d852de00e6e192344"
CASE_REVISION = "8073d5a0a4f8741799adfe0c494d58fd6472acaa"


def canonical_lf_bytes(path: Path) -> bytes:
    """Return text bytes with Git-equivalent CRLF normalized to LF."""
    return path.read_bytes().replace(b"\r\n", b"\n")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_record(
    repo: Path,
    path: Path,
    *,
    status: str,
    source: str,
    license_id: str,
    canonical_text: bool = False,
) -> dict:
    data = canonical_lf_bytes(path) if canonical_text else path.read_bytes()
    record = {
        "path": path.relative_to(repo).as_posix(),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "status": status,
        "source": source,
        "license": license_id,
    }
    if canonical_text:
        record["canonicalization"] = "utf-8-lf"
    return record


def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    overlay_root = (
        repo
        / "testing"
        / "v4"
        / "dependencies"
        / "uco-gufo-profile"
        / OVERLAY_REVISION
    )
    overlay_ontology = overlay_root / "ontology" / "uco-gufo.ttl"
    overlay_shapes = overlay_root / "shapes" / "sh-uco-gufo.ttl"
    overlay_license = overlay_root / "LICENSE"
    uco_root = overlay_root / "dependencies" / "UCO"
    cdo_root = overlay_root / "dependencies" / "CDO-Shapes-gufo"
    collections = uco_root / "dependencies" / "collections-ontology" / "collections.owl"
    spar_error = uco_root / "dependencies" / "error" / "docs" / "current" / "error.ttl"
    gufo = cdo_root / "dependencies" / "formatted-gufo.ttl"
    gufo_shapes = cdo_root / "shapes" / "sh-gufo.ttl"
    case_root = repo / "testing" / "v4" / "dependencies" / "case" / CASE_REVISION
    shacl = repo / "testing" / "v4" / "dependencies" / "w3c" / "shacl-2026-08-15.ttl"
    standards_root = repo / "testing" / "v4" / "dependencies" / "standards"
    skos = standards_root / "skos-2009-08-18.rdf"
    dcterms = standards_root / "dublin-core-terms-2012-06-14.ttl"

    dependency_specs: list[tuple[Path, str, str, str]] = [
        (overlay_ontology, "turtle", f"ucoProject/UCO-Profile-gufo@{OVERLAY_REVISION}", "Apache-2.0"),
        (overlay_shapes, "turtle", f"ucoProject/UCO-Profile-gufo@{OVERLAY_REVISION}", "Apache-2.0"),
        (gufo, "turtle", f"Cyber-Domain-Ontology/CDO-Shapes-gufo@{CDO_SHAPES_GUFO_REVISION}", "CC-BY-4.0"),
        (gufo_shapes, "turtle", f"Cyber-Domain-Ontology/CDO-Shapes-gufo@{CDO_SHAPES_GUFO_REVISION}", "Apache-2.0"),
        (collections, "xml", f"collections-ontology/collections-ontology@{COLLECTIONS_REVISION}", "see-vendored-source"),
        (spar_error, "turtle", f"SPAROntologies/error@{SPAR_ERROR_REVISION}", "CC-BY-4.0"),
        (shacl, "turtle", "https://www.w3.org/ns/shacl.ttl retrieved 2026-08-15", "W3C-Document-License"),
        (skos, "xml", "W3C SKOS Recommendation 2009-08-18", "W3C-Document-License"),
        (dcterms, "turtle", "DCMI Metadata Terms 2012-06-14", "CC-BY-4.0"),
    ]
    dependency_specs.extend(
        (path, "turtle", f"ucoProject/UCO@{UCO_REVISION}", "Apache-2.0")
        for path in sorted((uco_root / "ontology").rglob("*.ttl"))
    )
    dependency_specs.extend(
        (path, "turtle", f"casework/CASE@{CASE_REVISION}", "Apache-2.0")
        for path in sorted((case_root / "ontology").rglob("*.ttl"))
    )
    missing = [str(path) for path, _, _, _ in dependency_specs if not path.is_file()]
    if not overlay_license.is_file():
        missing.append(str(overlay_license))
    if missing:
        raise FileNotFoundError(f"Pinned dependency closure is incomplete: {missing}")

    declarations: dict[str, dict] = {}
    imports: set[str] = set()
    local_files = []
    for path in sorted((repo / "ontology").glob("*.ttl")):
        graph = Graph().parse(path, format="turtle")
        record = file_record(
            repo,
            path,
            status="resolved-local",
            source="CAC proposal worktree",
            license_id="Apache-2.0",
            canonical_text=True,
        )
        for ontology in graph.subjects(RDF.type, OWL.Ontology):
            if isinstance(ontology, URIRef):
                declarations[str(ontology)] = record
            for iri in graph.objects(ontology, OWL.versionIRI):
                if isinstance(iri, URIRef):
                    declarations[str(iri)] = record
        imports.update(str(value) for value in graph.objects(None, OWL.imports))
        local_files.append(record)

    dependency_files = []
    seen_paths: set[Path] = set()
    for path, rdf_format, source, license_id in dependency_specs:
        if path in seen_paths:
            continue
        seen_paths.add(path)
        graph = Graph().parse(path, format=rdf_format)
        record = file_record(
            repo,
            path,
            status="resolved-vendored",
            source=source,
            license_id=license_id,
            canonical_text=True,
        )
        dependency_files.append(record)
        for ontology in graph.subjects(RDF.type, OWL.Ontology):
            if isinstance(ontology, URIRef):
                declarations.setdefault(str(ontology), record)
            for iri in graph.objects(ontology, OWL.versionIRI):
                if isinstance(iri, URIRef):
                    declarations.setdefault(str(iri), record)
        imports.update(str(value) for value in graph.objects(None, OWL.imports))

    # Stable aliases explicitly present in the upstream XML catalogs.
    alias_paths = {
        "http://purl.org/co/": collections,
        "http://purl.org/nemo/gufo#": gufo,
        "http://purl.org/nemo/gufo#/1.0.0": gufo,
        "http://purl.org/spar/error": spar_error,
        "http://www.w3.org/ns/shacl#": shacl,
    }
    records_by_path = {repo / record["path"]: record for record in dependency_files}
    for iri, path in alias_paths.items():
        declarations.setdefault(iri, records_by_path[path])

    catalog = []
    for iri in sorted(imports):
        resolved = declarations.get(iri)
        if resolved:
            catalog.append({"requested_iri": iri, **resolved})
        else:
            catalog.append(
                {
                    "requested_iri": iri,
                    "status": "unresolved-remote",
                    "path": None,
                    "bytes": None,
                    "sha256": None,
                }
            )

    result = {
        "schema_version": 2,
        "policy": "All direct and transitive imports are resolved to locally vendored, content-addressed bytes; no evidence run retrieves mutable remote content.",
        "first_party_text_hash_policy": "Hash UTF-8 first-party Turtle after CRLF-to-LF normalization so Git-equivalent checkouts have stable identities.",
        "vendored_text_hash_policy": "Hash vendored RDF text after CRLF-to-LF normalization so Git-equivalent checkouts retain stable identities while the committed snapshots remain unmodified.",
        "runtime": {package: version(package) for package in PACKAGES},
        "uco_gufo_profile": {
            "revision_prefix": OVERLAY_REVISION[:8],
            "status": "resolved-local-with-runtime-closure",
            "commit": OVERLAY_REVISION,
            "source_archive_sha256": OVERLAY_ARCHIVE_SHA256,
            "source_archive_note": "User-provided GitHub source ZIP; Git submodule working trees are not embedded in source archives.",
            "license": "Apache-2.0",
            "license_path": overlay_license.relative_to(repo).as_posix(),
            "path": overlay_ontology.relative_to(repo).as_posix(),
            "sha256": sha256(overlay_ontology),
            "shapes_path": overlay_shapes.relative_to(repo).as_posix(),
            "shapes_sha256": sha256(overlay_shapes),
            "snapshot_files": [
                {
                    "path": path.relative_to(repo).as_posix(),
                    "bytes": path.stat().st_size,
                    "sha256": sha256(path),
                }
                for path in sorted(overlay_root.rglob("*"))
                if path.is_file()
                and "__pycache__" not in path.parts
                and path.suffix != ".pyc"
                and not any(
                    parent in path.parents
                    for parent in (uco_root, cdo_root)
                )
            ],
            "submodule_closure": {
                "status": "resolved-runtime",
                "UCO": UCO_REVISION,
                "CDO-Shapes-gufo": CDO_SHAPES_GUFO_REVISION,
                "collections-ontology": COLLECTIONS_REVISION,
                "SPAR-error": SPAR_ERROR_REVISION,
                "note": "Runtime ontology and shape closure is reconstructed. Build-only nested submodules not referenced by the vendored catalogs are intentionally omitted.",
            },
        },
        "imports": catalog,
        "ontology_files": local_files,
        "dependency_files": dependency_files,
    }
    output = Path(__file__).with_name("dependency-lock.json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
