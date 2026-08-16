#!/usr/bin/env python3
"""Run pinned ROBOT/HermiT OWL 2 DL gates and record complete evidence."""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import build_reasoner_closure as closure
from decompose_owl2dl_profile import parse_profile_lines

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
REPORTS = HERE / "reports"
WORK = HERE / "tmp" / "reasoner"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def execute(command: list[str], log: Path, timeout: int) -> dict:
    completed = subprocess.run(
        command,
        cwd=REPO,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    rendered = completed.stdout + completed.stderr
    log.write_text(rendered, encoding="utf-8")
    if "SWRL rule uses a built-in atom" in rendered:
        failure_kind = "reasoner-unsupported-imported-swrl-builtin"
    elif "value cannot be null at this stage" in rendered:
        failure_kind = "owlapi-invalid-rdf-structure"
    elif "unsatisfiable" in rendered:
        failure_kind = "logical-incoherence"
    elif completed.returncode:
        failure_kind = "tool-failure"
    else:
        failure_kind = None
    return {
        "return_code": completed.returncode,
        "status": "pass" if completed.returncode == 0 else "fail",
        "log": log.relative_to(REPO).as_posix(),
        "log_sha256": sha256(log),
        "failure_kind": failure_kind,
        "output_excerpt": rendered.strip()[-4000:],
    }


def summarize_profile_report(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    violations = parse_profile_lines(lines)
    categories = Counter(record["category"] for record in violations)
    return {
        "violation_count": len(violations),
        "cac_owned_count": sum(record["owner"] == "cac" for record in violations),
        "upstream_owned_count": sum(record["owner"] == "upstream" for record in violations),
        "categories": dict(sorted(categories.items())),
    }


def compress_report(path: Path) -> Path:
    compressed = path.with_suffix(path.suffix + ".gz")
    if compressed.exists():
        compressed.unlink()
    with path.open("rb") as source, compressed.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as target:
            target.write(source.read())
    path.unlink()
    return compressed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--java", type=Path, required=True)
    parser.add_argument("--robot-jar", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=1200)
    args = parser.parse_args()
    if not args.java.is_file() or not args.robot_jar.is_file():
        raise FileNotFoundError("Pinned Java or ROBOT artifact is unavailable")

    REPORTS.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    version = subprocess.run(
        [str(args.java), "-jar", str(args.robot_jar), "--version"],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    summary = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "runtime": {
            "robot": version,
            "robot_jar_sha256": sha256(args.robot_jar),
            "java": subprocess.run(
                [str(args.java), "-version"],
                capture_output=True,
                text=True,
                check=True,
            ).stderr.strip(),
        },
        "configurations": {},
    }
    overall = 0
    for configuration in ("C3", "C4", "C5"):
        stem = configuration.lower()
        source = WORK / f"{stem}-closure.owl"
        manifest_path = REPORTS / f"{stem}-owl-closure.json"
        manifest = closure.build(configuration, source)
        manifest_path.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

        profile_output = REPORTS / f"{stem}-owl2dl-profile.txt"
        if profile_output.exists():
            profile_output.unlink()
        profile = execute(
            [
                str(args.java),
                "-Xmx3g",
                "-jar",
                str(args.robot_jar),
                "validate-profile",
                "--profile",
                "DL",
                "--input",
                str(source),
                "--output",
                str(profile_output),
            ],
            REPORTS / f"{stem}-owl2dl-profile.log",
            args.timeout,
        )
        if profile_output.is_file():
            report_summary = summarize_profile_report(profile_output)
            compressed_report = compress_report(profile_output)
            if profile["status"] == "fail":
                profile["failure_kind"] = "owl2dl-profile-violations"
            profile.update(
                {
                    "report": compressed_report.relative_to(REPO).as_posix(),
                    "report_compression": "gzip-mtime-0",
                    "report_sha256": sha256(compressed_report),
                    "report_bytes": compressed_report.stat().st_size,
                    "summary": report_summary,
                }
            )

        reasoned = WORK / f"{stem}-reasoned.owl"
        if reasoned.exists():
            reasoned.unlink()
        reasoning = execute(
            [
                str(args.java),
                "-Xmx3g",
                "-jar",
                str(args.robot_jar),
                "reason",
                "--reasoner",
                "HermiT",
                "--equivalent-classes-allowed",
                "all",
                "--input",
                str(source),
                "--output",
                str(reasoned),
            ],
            REPORTS / f"{stem}-hermit.log",
            args.timeout,
        )
        if reasoned.is_file():
            reasoning.update(
                {
                    "reasoned_bytes": reasoned.stat().st_size,
                    "reasoned_sha256": sha256(reasoned),
                }
            )

        projection_source = WORK / f"{stem}-diagnostic-projection.owl"
        projection_manifest_path = REPORTS / f"{stem}-diagnostic-projection.json"
        projection_manifest = closure.build(
            configuration,
            projection_source,
            diagnostic_projection=True,
        )
        projection_manifest_path.write_text(
            json.dumps(projection_manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        projection_reasoned = WORK / f"{stem}-diagnostic-reasoned.owl"
        if projection_reasoned.exists():
            projection_reasoned.unlink()
        diagnostic_reasoning = execute(
            [
                str(args.java),
                "-Xmx3g",
                "-jar",
                str(args.robot_jar),
                "reason",
                "--reasoner",
                "HermiT",
                "--equivalent-classes-allowed",
                "all",
                "--input",
                str(projection_source),
                "--output",
                str(projection_reasoned),
            ],
            REPORTS / f"{stem}-diagnostic-hermit.log",
            args.timeout,
        )
        if projection_reasoned.is_file():
            diagnostic_reasoning.update(
                {
                    "reasoned_bytes": projection_reasoned.stat().st_size,
                    "reasoned_sha256": sha256(projection_reasoned),
                }
            )
        configuration_status = (
            "pass"
            if profile["status"] == "pass" and reasoning["status"] == "pass"
            else "fail"
        )
        summary["configurations"][configuration] = {
            "status": configuration_status,
            "closure_manifest": manifest_path.relative_to(REPO).as_posix(),
            "profile": profile,
            "hermit": reasoning,
            "diagnostic_projection": {
                "status": "non-normative-diagnostic-only",
                "manifest": projection_manifest_path.relative_to(REPO).as_posix(),
                "hermit": diagnostic_reasoning,
            },
        }
        if configuration_status != "pass":
            overall = 1

    output = REPORTS / "owl2dl-summary.json"
    output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return overall


if __name__ == "__main__":
    raise SystemExit(main())
