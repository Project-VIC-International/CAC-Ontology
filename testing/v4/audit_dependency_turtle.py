#!/usr/bin/env python3
"""Audit exact vendored dependency snapshots for Turtle syntax without modifying them."""

from __future__ import annotations

import json
from pathlib import Path

from rdflib import Graph

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
LOCK = HERE / "dependency-lock.json"


def audit() -> dict:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    files = sorted(
        REPO / record["path"]
        for record in lock["dependency_files"]
        if record["path"].endswith(".ttl")
    )
    findings = []
    for path in files:
        try:
            Graph().parse(path, format="turtle")
        except Exception as exc:
            findings.append(
                {
                    "path": path.relative_to(REPO).as_posix(),
                    "error": str(exc),
                    "ownership": "pinned-upstream-snapshot",
                }
            )
    return {
        "schema_version": 1,
        "status": "pass" if not findings else "fail-upstream",
        "files_audited": len(files),
        "finding_count": len(findings),
        "findings": findings,
        "claim_limit": "This report audits the content-addressed .ttl files registered in dependency-lock.json; unregistered upstream source examples are outside the vendored runtime closure.",
    }


def main() -> int:
    print(json.dumps(audit(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
