#!/usr/bin/env python3
"""Decompose strict ROBOT OWL 2 DL findings by ownership and root cause."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
REPORTS = HERE / "reports"

REM014_BASELINE = {
    "C3": {
        "violation_count": 6947,
        "cac_owned_count": 812,
        "upstream_owned_count": 6116,
        "shared_or_unattributed_count": 19,
    },
    "C5": {"violation_count": 6949},
}

VIOLATION_PREFIXES = (
    "Cannot pun between properties:",
    "Datatype IRI also used as Class IRI:",
    "Not enough operands; at least two needed:",
    "Use of defined datatype in datatype restriction",
    "Use of reserved vocabulary for class IRI:",
    "Use of undeclared annotation property:",
    "Use of undeclared class:",
    "Use of undeclared data property:",
    "Use of undeclared datatype:",
    "Use of undeclared object property:",
)

IRI_PATTERN = re.compile(r"<([^>]+)>|\b((?:https?|urn):[^\s\]\[()>,]+)")


def category(line: str) -> str:
    for prefix in VIOLATION_PREFIXES:
        if line.startswith(prefix):
            return prefix.rstrip(":")
    raise ValueError(f"Not a profile violation header: {line[:100]}")


def primary_iri(line: str) -> str | None:
    match = re.search(r":\s*<([^>]+)>", line)
    if match:
        return match.group(1)
    match = re.search(r"Class IRI:\s*(https?://\S+)", line)
    if match:
        return match.group(1)
    if line.startswith("Use of defined datatype") or line.startswith("Use of undeclared datatype"):
        match = re.search(r"\^\^(xsd:[A-Za-z0-9_-]+)|:\s*(xsd:[A-Za-z0-9_-]+)", line)
        if match:
            return match.group(1) or match.group(2)
    if line.startswith("Use of reserved vocabulary for class IRI:"):
        return line.split(":", 1)[1].split("[", 1)[0].strip()
    match = IRI_PATTERN.search(line)
    return (match.group(1) or match.group(2)) if match else None


def namespace_owner(iri: str | None) -> str:
    if not iri:
        return "unknown"
    if iri.startswith("https://cacontology.projectvic.org"):
        return "cac"
    if iri.startswith("https://ontology.unifiedcyberontology.org"):
        return "upstream-uco"
    if iri.startswith("http://purl.org/nemo/gufo#"):
        return "upstream-gufo"
    if iri.startswith("http://www.w3.org/ns/shacl#"):
        return "upstream-shacl"
    if iri.startswith(("http://purl.org/dc/", "http://www.w3.org/2004/02/skos/")):
        return "shared-vocabulary"
    if iri.startswith(("http://www.w3.org/", "owl:", "rdf:", "rdfs:", "xsd:")):
        return "standard"
    return "other-upstream-or-unknown"


def actor_owner(line: str, primary: str | None) -> str:
    axiom = line.split(" in OntologyID", 1)[0]
    iris = [left or right for left, right in IRI_PATTERN.findall(axiom)]
    for iri in iris:
        if iri == primary:
            continue
        owner = namespace_owner(iri)
        if owner == "cac":
            return owner
    for iri in iris:
        if iri == primary:
            continue
        owner = namespace_owner(iri)
        if owner.startswith("upstream-"):
            return owner
    return "unknown"


def effective_owner(line: str, primary: str | None) -> str:
    primary_owner = namespace_owner(primary)
    if line.startswith(("Cannot pun between properties:", "Datatype IRI also used as Class IRI:")):
        if primary_owner == "cac":
            return "cac"
        if primary_owner.startswith("upstream-"):
            return "upstream"
    actor = actor_owner(line, primary)
    if actor == "cac":
        return "cac"
    if actor.startswith("upstream-"):
        return "upstream"
    if primary_owner == "cac":
        return "cac"
    if primary_owner.startswith("upstream-"):
        return "upstream"
    if primary_owner in {"standard", "shared-vocabulary"}:
        return "shared-or-unattributed"
    return "unattributed"


def root_cause(line: str, owner: str, primary: str | None) -> str:
    value = category(line)
    if value == "Cannot pun between properties":
        return "property-kind-punning"
    if value == "Datatype IRI also used as Class IRI":
        return "class-used-as-datatype"
    if value == "Not enough operands; at least two needed":
        return "single-operand-equivalence"
    if value == "Use of reserved vocabulary for class IRI":
        return "reserved-owl-vocabulary-as-domain-or-range"
    if value == "Use of defined datatype in datatype restriction":
        return "unsupported-defined-datatype-literal"
    if value == "Use of undeclared annotation property":
        if primary and primary.startswith("http://www.w3.org/ns/shacl#"):
            return "embedded-shacl-vocabulary-not-declared-for-owlapi"
        return "annotation-vocabulary-not-declared-for-owlapi"
    if value.startswith("Use of undeclared"):
        if owner == "cac":
            primary_owner = namespace_owner(primary)
            if primary_owner == "cac":
                return "missing-local-declaration"
            if primary_owner == "standard":
                return "unsupported-xsd-datatype-policy"
            if primary_owner == "shared-vocabulary":
                return "unimported-shared-vocabulary"
            if primary_owner.startswith("upstream-"):
                return "invalid-or-version-mismatched-external-reference"
            return "unattributed-first-party-reference"
        if owner == "upstream":
            return "missing-or-invalid-upstream-declaration"
        return "unattributed-declaration-gap"
    return "unclassified"


def parse_profile_lines(lines: list[str]) -> list[dict]:
    records = []
    for line_number, line in enumerate(lines, start=1):
        if not line.startswith(VIOLATION_PREFIXES):
            continue
        primary = primary_iri(line)
        owner = effective_owner(line, primary)
        records.append(
            {
                "line": line_number,
                "category": category(line),
                "primary_iri": primary,
                "primary_namespace_owner": namespace_owner(primary),
                "actor_owner": actor_owner(line, primary),
                "owner": owner,
                "root_cause": root_cause(line, owner, primary),
                "text": line,
            }
        )
    return records


def parse_profile_path(path: Path) -> list[dict]:
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8") as stream:
            lines = stream.read().splitlines()
    else:
        lines = path.read_text(encoding="utf-8").splitlines()
    return parse_profile_lines(lines)


def aggregate(configuration: str, path: Path) -> dict:
    records = parse_profile_path(path)
    by_category = Counter(record["category"] for record in records)
    by_owner = Counter(record["owner"] for record in records)
    by_root = Counter(record["root_cause"] for record in records)
    by_owner_and_root: dict[str, Counter] = defaultdict(Counter)
    unique_by_root: dict[str, set[str]] = defaultdict(set)
    examples: dict[str, list[str]] = defaultdict(list)
    for record in records:
        by_owner_and_root[record["owner"]][record["root_cause"]] += 1
        if record["primary_iri"]:
            unique_by_root[record["root_cause"]].add(record["primary_iri"])
        if len(examples[record["root_cause"]]) < 3:
            examples[record["root_cause"]].append(record["text"])
    return {
        "configuration": configuration,
        "report": path.relative_to(REPO).as_posix(),
        "violation_count": len(records),
        "by_category": dict(sorted(by_category.items())),
        "by_owner": dict(sorted(by_owner.items())),
        "by_owner_and_root_cause": {
            owner: dict(sorted(counts.items()))
            for owner, counts in sorted(by_owner_and_root.items())
        },
        "by_root_cause": dict(sorted(by_root.items())),
        "unique_primary_iris_by_root_cause": {
            key: len(value) for key, value in sorted(unique_by_root.items())
        },
        "examples_by_root_cause": dict(sorted(examples.items())),
        "records": records,
    }


def priority_units(c3: dict) -> list[dict]:
    counts = c3["by_root_cause"]
    owner_counts = c3["by_owner_and_root_cause"]
    unique = c3["unique_primary_iris_by_root_cause"]
    definitions = [
        ("single-operand-equivalence", 5, 5, 1, "Remove or complete invalid one-member equivalent-class axioms."),
        ("property-kind-punning", 5, 5, 2, "Separate object and datatype property meanings; preserve compatibility explicitly."),
        ("class-used-as-datatype", 5, 5, 2, "Correct datatype ranges that name OWL classes."),
        ("reserved-owl-vocabulary-as-domain-or-range", 4, 4, 2, "Replace owl:Class domain/range metamodeling with a DL-safe contract."),
        ("missing-local-declaration", 5, 4, 2, "Declare intended CAC entities with the narrowest evidence-supported entity kind."),
        ("invalid-or-version-mismatched-external-reference", 5, 5, 3, "Replace obsolete or invalid external terms with verified pinned-version vocabulary."),
        ("unsupported-xsd-datatype-policy", 3, 4, 3, "Adopt a supported datatype representation without silently changing value meaning."),
        ("unimported-shared-vocabulary", 3, 3, 3, "Add a bounded SKOS vocabulary/import strategy for shared controlled concepts."),
        ("unsupported-defined-datatype-literal", 3, 4, 3, "Move planning durations out of the OWL DL semantic layer or adopt a supported representation."),
        ("annotation-vocabulary-not-declared-for-owlapi", 2, 3, 3, "Add a bounded annotation vocabulary/declaration strategy for first-party metadata."),
        ("embedded-shacl-vocabulary-not-declared-for-owlapi", 2, 3, 5, "Treat upstream embedded shapes separately or obtain an upstream/profile correction."),
        ("missing-or-invalid-upstream-declaration", 3, 4, 5, "Preserve as upstream evidence and avoid silently patching pinned bytes."),
    ]
    units = []
    for root, impact, risk, effort, remedy in definitions:
        count = counts.get(root, 0)
        if not count:
            continue
        cac_count = owner_counts.get("cac", {}).get(root, 0)
        scope = "cac-actionable" if cac_count else "external"
        units.append(
            {
                "root_cause": root,
                "occurrences": count,
                "cac_occurrences": cac_count,
                "scope": scope,
                "unique_primary_iris": unique.get(root, 0),
                "impact": impact,
                "risk": risk,
                "effort": effort,
                "priority_score": (impact + risk) * (6 - effort) if cac_count else 0,
                "remedy": remedy,
            }
        )
    return sorted(
        units,
        key=lambda value: (
            value["scope"] != "cac-actionable",
            -value["priority_score"],
            -value["cac_occurrences"],
            value["root_cause"],
        ),
    )


def markdown(report: dict) -> str:
    c3 = report["configurations"]["C3"]
    c5 = report["configurations"]["C5"]
    lines = [
        "# REM-014 OWL 2 DL Profile Decomposition",
        "",
        "The earlier 7,287/7,289 figures were non-empty line counts. Multiline SPARQL annotation bodies inflated those totals. This decomposition counts only recognized ROBOT violation headers.",
        "",
        f"- C3 REM-014 baseline: **{report['baseline']['C3']['violation_count']:,}**",
        f"- C5 REM-014 baseline: **{report['baseline']['C5']['violation_count']:,}**",
        f"- C3 actual violations: **{c3['violation_count']:,}**",
        f"- C5 actual violations: **{c5['violation_count']:,}**",
        f"- C3 reduction from baseline: **{report['delta_from_baseline']['C3']:+,}**",
        f"- C5 reduction from baseline: **{report['delta_from_baseline']['C5']:+,}**",
        f"- C5 compatibility delta: **{c5['violation_count'] - c3['violation_count']:+,}**",
        "",
        "## Ownership",
        "",
        "| Owner | C3 occurrences |",
        "|---|---:|",
    ]
    lines.extend(f"| {owner} | {count:,} |" for owner, count in c3["by_owner"].items())
    lines.extend(["", "## Prioritized remediation units", "", "| Priority | Root cause | Scope | CAC occurrences | Total occurrences | Unique IRIs | Score |", "|---:|---|---|---:|---:|---:|---:|"])
    for index, unit in enumerate(report["priority_units"], start=1):
        lines.append(
            f"| {index} | {unit['root_cause']} | {unit['scope']} | {unit['cac_occurrences']:,} | {unit['occurrences']:,} | {unit['unique_primary_iris']:,} | {unit['priority_score']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "Ownership is inferred from the violated IRI and the axiom actor before the merged OntologyID suffix. `cac` findings are candidates for local repair. `upstream` findings remain pinned external evidence. `shared-or-unattributed` findings require source-level provenance before assignment. The unmodified full-import report remains authoritative.",
            "",
        ]
    )
    return "\n".join(lines)


def build() -> dict:
    configurations = {
        name: aggregate(name, REPORTS / f"{name.lower()}-owl2dl-profile.txt.gz")
        for name in ("C3", "C5")
    }
    report = {
        "schema_version": 1,
        "mission": "REM-014",
        "method": "Count recognized ROBOT violation headers; classify primary IRI and axiom actor without treating multiline annotation text as separate violations.",
        "baseline": REM014_BASELINE,
        "configurations": configurations,
        "delta_from_baseline": {
            name: value["violation_count"] - REM014_BASELINE[name]["violation_count"]
            for name, value in configurations.items()
        },
        "priority_units": priority_units(configurations["C3"]),
    }
    return report


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summary_without_records(report: dict, details_path: Path) -> dict:
    configurations = {}
    for name, value in report["configurations"].items():
        configurations[name] = {key: item for key, item in value.items() if key != "records"}
    return {
        **{key: value for key, value in report.items() if key != "configurations"},
        "configurations": configurations,
        "details": {
            "path": details_path.relative_to(REPO).as_posix(),
            "format": "gzip-compressed JSON Lines; one record per recognized ROBOT violation header",
            "sha256": sha256(details_path),
            "bytes": details_path.stat().st_size,
        },
    }


def write_details(report: dict, path: Path) -> None:
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as target:
            for configuration, value in report["configurations"].items():
                for record in value["records"]:
                    row = {"configuration": configuration, **record}
                    target.write((json.dumps(row, sort_keys=True) + "\n").encode("utf-8"))


def refresh_owl_summary(report: dict) -> None:
    path = REPORTS / "owl2dl-summary.json"
    summary = json.loads(path.read_text(encoding="utf-8"))
    for name, value in report["configurations"].items():
        profile_summary = summary["configurations"][name]["profile"]["summary"]
        profile_summary.clear()
        profile_summary.update(
            {
                "violation_count": value["violation_count"],
                "cac_owned_count": value["by_owner"].get("cac", 0),
                "upstream_owned_count": value["by_owner"].get("upstream", 0),
                "shared_or_unattributed_count": value["by_owner"].get("shared-or-unattributed", 0),
                "categories": value["by_category"],
                "counting_method": "recognized-robot-violation-headers-v2",
            }
        )
    path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path, default=REPORTS / "rem-014-decomposition.json")
    parser.add_argument("--markdown", type=Path, default=REPORTS / "rem-014-decomposition.md")
    parser.add_argument("--details", type=Path, default=REPORTS / "rem-014-findings.jsonl.gz")
    args = parser.parse_args()
    report = build()
    write_details(report, args.details)
    summary = summary_without_records(report, args.details)
    args.json.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown.write_text(markdown(report), encoding="utf-8")
    refresh_owl_summary(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
