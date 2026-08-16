#!/usr/bin/env python3
"""Deterministic asserted-graph diagnostics for the CAC v4 architecture."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import rdflib
from rdflib import OWL, RDF, RDFS, Graph, Namespace, URIRef
from owlrl import DeductiveClosure, RDFSClosure

CAC_CORE = Namespace("https://cacontology.projectvic.org/core#")
GUFO = Namespace("http://purl.org/nemo/gufo#")
BASE = "93de063951b758dd68a27611638c177fcf910eab"
PROFILE_REVISION = "4b98b9881aa29ed80f39b589d15725fa696c921a"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_lf_bytes(path: Path) -> bytes:
    """Return the repository-canonical bytes for first-party text inputs."""
    return path.read_bytes().replace(b"\r\n", b"\n")


def git_value(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-c", f"safe.directory={repo}", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def git_bytes(repo: Path, *args: str) -> bytes:
    return subprocess.run(
        ["git", "-c", f"safe.directory={repo}", *args],
        cwd=repo,
        check=True,
        capture_output=True,
    ).stdout


def ontology_files(repo: Path, configuration: str) -> list[Path]:
    return sorted(
        path
        for path in (repo / "ontology").glob("*.ttl")
        if "-shapes" not in path.name
        and (
            path.name != "cacontology-v3-compatibility.ttl"
            or configuration == "C5"
        )
    )


def overlay_path(repo: Path) -> Path:
    return (
        repo
        / "testing"
        / "v4"
        / "dependencies"
        / "uco-gufo-profile"
        / PROFILE_REVISION
        / "ontology"
        / "uco-gufo.ttl"
    )


def load_configuration_graph(repo: Path, configuration: str) -> tuple[Graph, list[dict]]:
    if configuration not in {"C2", "C3", "C4", "C5"}:
        raise ValueError(f"Unsupported configuration: {configuration}")

    graph = Graph()
    inputs: list[dict] = []
    if configuration == "C2":
        names = [
            name
            for name in git_value(repo, "ls-tree", "-r", "--name-only", BASE, "--", "ontology").splitlines()
            if name.endswith(".ttl") and "-shapes" not in Path(name).name
        ]
        for name in names:
            data = git_bytes(repo, "show", f"{BASE}:{name}")
            graph.parse(data=data.decode("utf-8"), format="turtle")
            inputs.append(
                {
                    "path": f"git:{BASE}:{name}",
                    "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                }
            )
    else:
        for path in ontology_files(repo, configuration):
            data = canonical_lf_bytes(path)
            graph.parse(data=data.decode("utf-8"), format="turtle")
            inputs.append(
                {
                    "path": path.relative_to(repo).as_posix(),
                    "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "canonicalization": "utf-8-lf",
                }
            )

    if configuration in {"C2", "C4"}:
        profile = overlay_path(repo)
        if not profile.is_file():
            raise FileNotFoundError(f"Pinned overlay is unavailable: {profile}")
        graph.parse(profile, format="turtle")
        inputs.append(
            {
                "path": profile.relative_to(repo).as_posix(),
                "bytes": profile.stat().st_size,
                "sha256": sha256(profile),
            }
        )
    return graph, inputs


def subclass_index(graph: Graph) -> dict[URIRef, set[URIRef]]:
    parents: dict[URIRef, set[URIRef]] = defaultdict(set)
    for child, parent in graph.subject_objects(RDFS.subClassOf):
        if isinstance(child, URIRef) and isinstance(parent, URIRef):
            parents[child].add(parent)
    changed = True
    while changed:
        changed = False
        for child in list(parents):
            inherited = set().union(*(parents.get(p, set()) for p in parents[child]))
            if not inherited.issubset(parents[child]):
                parents[child].update(inherited)
                changed = True
    return parents


def audit_graph(graph: Graph) -> dict:
    parents = subclass_index(graph)
    # OWL-RL closure entails that owl:Nothing is a subclass of every class.
    # It is the built-in bottom class, not a modeled CAC term or a conflict.
    classes = {
        s
        for s in graph.subjects(RDF.type, OWL.Class)
        if isinstance(s, URIRef) and s != OWL.Nothing
    }
    role_branch = {c for c in classes if c == CAC_CORE.Role or CAC_CORE.Role in parents.get(c, set())}
    phase_branch = {c for c in classes if c == CAC_CORE.Phase or CAC_CORE.Phase in parents.get(c, set())}
    enduring_branch = {
        c for c in classes if c == CAC_CORE.EnduringEntity or CAC_CORE.EnduringEntity in parents.get(c, set())
    }
    event_branch = {c for c in classes if c == CAC_CORE.Event or CAC_CORE.Event in parents.get(c, set())}

    diagnostics = {
        "META001_OPERATIONAL_ROLE_AS_GUFO_CLASSIFIER": sorted(
            str(c) for c in role_branch if (c, RDF.type, GUFO.Role) in graph
        ),
        "META002_OPERATIONAL_PHASE_AS_GUFO_CLASSIFIER": sorted(
            str(c) for c in phase_branch if (c, RDF.type, GUFO.Phase) in graph
        ),
        "META003_ENDURING_PHASE_OVERLAP": sorted(str(c) for c in enduring_branch & phase_branch),
        "META004_CORE_ROLE_SUBCLASSES_GUFO_ROLE": sorted(
            str(o) for o in graph.objects(CAC_CORE.Role, RDFS.subClassOf) if o == GUFO.Role
        ),
        "META005_CORE_PHASE_SUBCLASSES_GUFO_PHASE": sorted(
            str(o) for o in graph.objects(CAC_CORE.Phase, RDFS.subClassOf) if o == GUFO.Phase
        ),
        "META006_ROLE_ASSIGNMENT_INSTANCE_AS_GUFO_CLASSIFIER": sorted(
            str(node)
            for node in graph.subjects(RDF.type, CAC_CORE.RoleAssignment)
            if (node, RDF.type, GUFO.Role) in graph
        ),
        "META007_PHASE_OCCURRENCE_AS_GUFO_CLASSIFIER": sorted(
            str(node)
            for node in graph.subjects(RDF.type, CAC_CORE.Phase)
            if (node, RDF.type, GUFO.Phase) in graph and (node, RDF.type, OWL.Class) not in graph
        ),
        "META008_OPERATIONAL_ROLE_ENDURING_OVERLAP": sorted(str(c) for c in role_branch & enduring_branch),
        "META009_OPERATIONAL_ROLE_PHASE_OVERLAP": sorted(str(c) for c in role_branch & phase_branch),
        "META010_OPERATIONAL_PHASE_EVENT_OVERLAP": sorted(str(c) for c in phase_branch & event_branch),
        "META011_GUFO_ROLE_CLASSIFIER_WITHOUT_ENDURING_BEARER_BRANCH": sorted(
            str(c)
            for c in classes
            if str(c).startswith("https://cacontology.projectvic.org/")
            and (c, RDF.type, GUFO.Role) in graph
            and c not in enduring_branch
        ),
    }
    return {
        "counts": {
            "triples": len(graph),
            "owl_classes": len(classes),
            "role_branch_classes": len(role_branch),
            "phase_branch_classes": len(phase_branch),
            "enduring_branch_classes": len(enduring_branch),
            "diagnostic_findings": sum(len(values) for values in diagnostics.values()),
        },
        "diagnostics": diagnostics,
    }


def build_report(repo: Path, configuration: str, inference: str = "asserted") -> dict:
    graph, inputs = load_configuration_graph(repo, configuration)
    asserted_triples = len(graph)
    if inference == "rdfs":
        DeductiveClosure(RDFSClosure.RDFS_Semantics).expand(graph)
    result = audit_graph(graph)
    dirty = bool(git_value(repo, "status", "--porcelain", "--untracked-files=no"))
    dependency_lock = repo / "testing" / "v4" / "dependency-lock.json"
    result.update(
        {
            "schema_version": 1,
            "configuration": configuration,
            "inference": inference,
            "status": "pass" if result["counts"]["diagnostic_findings"] == 0 else "fail",
            "scope": "CAC architecture diagnostics with optional RDFS closure. C2/C4 include the exact pinned profile ontology but do not follow its imports; this is not an OWL 2 DL consistency result.",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source": {
                "commit": git_value(repo, "rev-parse", "HEAD"),
                "tree": git_value(repo, "rev-parse", "HEAD^{tree}"),
                "branch": git_value(repo, "branch", "--show-current"),
                "dirty": dirty,
            },
            "runtime": {
                "python": platform.python_version(),
                "rdflib": rdflib.__version__,
                "platform": platform.platform(),
            },
            "asserted_triples": asserted_triples,
            "dependency_lock_sha256": sha256(dependency_lock),
            "inputs": inputs,
            "sensitive_data": "Synthetic fixtures only; no real sensitive case data.",
        }
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--configuration", choices=("C2", "C3", "C4", "C5"), required=True)
    parser.add_argument("--inference", choices=("asserted", "rdfs"), default="asserted")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    report = build_report(repo, args.configuration, args.inference)
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
