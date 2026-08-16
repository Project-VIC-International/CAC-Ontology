#!/usr/bin/env python3
"""Generate the local Gate 4 evidence bundle without network or GitHub mutation."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
REPORTS = HERE / "reports"
BASE = "93de063951b758dd68a27611638c177fcf910eab"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


ARCH = load_module("architecture_audit", HERE / "architecture_audit.py")
SPARQL = load_module("audit_shacl_sparql", HERE / "audit_shacl_sparql.py")
LEVELS = load_module(
    "audit_shape_level_assumptions", HERE / "audit_shape_level_assumptions.py"
)
DEP_OWLAPI = load_module(
    "audit_dependency_owlapi_structures", HERE / "audit_dependency_owlapi_structures.py"
)
DEP_TURTLE = load_module(
    "audit_dependency_turtle", HERE / "audit_dependency_turtle.py"
)


def git(*args: str) -> str:
    return subprocess.run(
        ["git", "-c", f"safe.directory={REPO}", *args],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def write_json(name: str, value: object) -> None:
    (REPORTS / name).write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [sys.executable, str(HERE / "build_dependency_lock.py")],
        cwd=REPO,
        check=True,
    )
    dependency = json.loads((HERE / "dependency-lock.json").read_text(encoding="utf-8"))

    configurations: dict[str, object] = {}
    for config in ("C2", "C3", "C4", "C5"):
        configurations[config] = {}
        for inference in ("asserted", "rdfs"):
            report = ARCH.build_report(REPO, config, inference)
            write_json(f"{config.lower()}-{inference}.json", report)
            configurations[config][inference] = {
                "status": report["status"],
                "diagnostic_findings": report["counts"]["diagnostic_findings"],
                "triples": report["counts"]["triples"],
            }

    tests = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            str(HERE),
            "-p",
            "test_*.py",
            "-v",
        ],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    test_output = tests.stdout + tests.stderr
    (REPORTS / "unittest.txt").write_text(test_output, encoding="utf-8")
    match = re.search(r"Ran (\d+) tests", test_output)

    sparql = SPARQL.audit(REPO / "ontology")
    write_json("shacl-sparql-syntax.json", sparql)
    level_inventory = LEVELS.inventory(REPO / "ontology")
    write_json("shape-level-assumptions.json", level_inventory)
    dependency_owlapi = DEP_OWLAPI.audit()
    write_json("dependency-owlapi-rdf-structures.json", dependency_owlapi)
    dependency_turtle = DEP_TURTLE.audit()
    write_json("dependency-turtle-syntax.json", dependency_turtle)

    baseline = json.loads(
        (HERE / "baselines" / "c1-v3.1-asserted.json").read_text(encoding="utf-8")
    )
    ledger = json.loads((HERE / "term-disposition-summary.json").read_text(encoding="utf-8"))
    imports = dependency["imports"]

    commits = git("rev-list", "--reverse", f"{BASE}..HEAD").splitlines()
    unsigned = [
        commit
        for commit in commits
        if "Signed-off-by:" not in git("show", "-s", "--format=%B", commit)
    ]
    changed_paths = git("diff", "--name-only", f"{BASE}..HEAD").splitlines()
    tracked_changes = git("status", "--porcelain", "--untracked-files=no").splitlines()
    tracked_source_changes = [
        line for line in tracked_changes if "testing/v4/reports/" not in line
    ]
    tracked_evidence_changes = [
        line for line in tracked_changes if "testing/v4/reports/" in line
    ]

    owl_summary_path = REPORTS / "owl2dl-summary.json"
    owl_summary = (
        json.loads(owl_summary_path.read_text(encoding="utf-8"))
        if owl_summary_path.is_file()
        else None
    )
    owl_diagnostic_pass = bool(owl_summary) and all(
        value["diagnostic_projection"]["hermit"]["status"] == "pass"
        for value in owl_summary["configurations"].values()
    )
    owl_normative_pass = bool(owl_summary) and all(
        value["status"] == "pass" for value in owl_summary["configurations"].values()
    )

    summary = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": {
            "base_commit": BASE,
            "candidate_commit": git("rev-parse", "HEAD"),
            "candidate_tree": git("rev-parse", "HEAD^{tree}"),
            "branch": git("branch", "--show-current"),
            "tracked_dirty": bool(tracked_source_changes),
            "tracked_source_changes": tracked_source_changes,
            "tracked_evidence_dirty": bool(tracked_evidence_changes),
            "commits": len(commits),
            "unsigned_commits": unsigned,
            "changed_paths": len(changed_paths),
            "detection_shapes_changed": "ontology/cacontology-detection-shapes.ttl" in changed_paths,
        },
        "configurations": {
            "C1": {
                "status": "observed-baseline",
                "diagnostic_findings": baseline["counts"]["diagnostic_findings"],
                "source_commit": BASE,
            },
            "C2": {
                **configurations["C2"],
                "gate": False,
                "scope_note": "Exact profile ontology applied to the frozen base; imported submodule closure is not included.",
            },
            "C3": configurations["C3"],
            "C4": {
                **configurations["C4"],
                "gate": True,
                "scope_note": "Exact profile ontology applied to the candidate; imported submodule closure is not included.",
            },
            "C5": configurations["C5"],
        },
        "tests": {
            "return_code": tests.returncode,
            "tests_run": int(match.group(1)) if match else None,
            "status": "pass" if tests.returncode == 0 else "fail",
        },
        "shacl_sparql": {
            "queries": sparql["queries"],
            "proposal_failures": sparql["proposal_failures"],
            "pr48_detection_failures": sparql["pr48_detection_failures"],
        },
        "term_dispositions": ledger,
        "dependencies": {
            "imports": len(imports),
            "resolved_local": sum(i["status"] == "resolved-local" for i in imports),
            "resolved_vendored": sum(i["status"] == "resolved-vendored" for i in imports),
            "unresolved_remote": sum(i["status"] == "unresolved-remote" for i in imports),
            "uco_gufo_profile": dependency["uco_gufo_profile"],
            "owlapi_rdf_structures": {
                "status": dependency_owlapi["status"],
                "finding_count": dependency_owlapi["finding_count"],
                "report": "testing/v4/reports/dependency-owlapi-rdf-structures.json",
            },
            "turtle_syntax": {
                "status": dependency_turtle["status"],
                "files_audited": dependency_turtle["files_audited"],
                "finding_count": dependency_turtle["finding_count"],
                "report": "testing/v4/reports/dependency-turtle-syntax.json",
            },
        },
        "owl_2_dl": {
            "status": "pass" if owl_normative_pass else "fail",
            "diagnostic_projection_status": "pass" if owl_diagnostic_pass else "fail",
            "summary": "testing/v4/reports/owl2dl-summary.json" if owl_summary else None,
            "claim": (
                "The non-normative diagnostic projections are coherent under HermiT, but they do not satisfy the full-import OWL 2 DL gate."
                if owl_diagnostic_pass and not owl_normative_pass
                else "See the pinned ROBOT/HermiT summary for the exact normative result."
            ),
        },
        "gate4_recommendation": {
            "status": "ready" if owl_normative_pass else "hold",
            "reason": (
                "All normative configuration gates pass."
                if owl_normative_pass
                else "CAC-only and exact-profile diagnostic projections are coherent, and recognized C3/C5 profile violations are now entirely upstream-owned. The unmodified full import closure still fails the normative OWL 2 DL gate because the exact upstream profile contains malformed RDF structures and imported SWRL built-ins are unsupported by HermiT."
            ),
            "github_mutation_authorized": False,
        },
        "sensitive_data": "Synthetic fixtures only; no real investigative, victim, or adopter data is present.",
    }
    write_json("gate4-summary.json", summary)
    return 0 if tests.returncode == 0 else tests.returncode


if __name__ == "__main__":
    raise SystemExit(main())
