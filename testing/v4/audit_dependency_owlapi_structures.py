#!/usr/bin/env python3
"""Audit pinned dependency RDF structures that OWLAPI must translate."""

from __future__ import annotations

import json
from pathlib import Path

from rdflib import Graph, OWL, RDF

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def audit() -> dict:
    lock = json.loads((HERE / "dependency-lock.json").read_text(encoding="utf-8"))
    findings = []
    files_scanned = 0
    for record in lock["dependency_files"]:
        path = REPO / record["path"]
        if path.suffix.lower() not in {".ttl", ".owl", ".rdf", ".xml"}:
            continue
        graph = Graph()
        graph.parse(path, format="xml" if path.suffix.lower() in {".owl", ".rdf", ".xml"} else "turtle")
        files_scanned += 1
        for node in graph.subjects(RDF.type, OWL.Axiom):
            missing = [
                str(predicate)
                for predicate in (OWL.annotatedSource, OWL.annotatedProperty, OWL.annotatedTarget)
                if not list(graph.objects(node, predicate))
            ]
            if missing:
                findings.append(
                    {
                        "kind": "incomplete-owl-axiom",
                        "node": str(node),
                        "path": record["path"],
                        "source": record["source"],
                        "missing": missing,
                        "predicates_present": sorted({str(predicate) for predicate in graph.predicates(node)}),
                    }
                )
        for node in graph.subjects(RDF.type, OWL.NegativePropertyAssertion):
            missing = []
            if not list(graph.objects(node, OWL.sourceIndividual)):
                missing.append(str(OWL.sourceIndividual))
            if not list(graph.objects(node, OWL.assertionProperty)):
                missing.append(str(OWL.assertionProperty))
            if not (
                list(graph.objects(node, OWL.targetIndividual))
                or list(graph.objects(node, OWL.targetValue))
            ):
                missing.append("owl:targetIndividual|owl:targetValue")
            if missing:
                findings.append(
                    {
                        "kind": "incomplete-negative-property-assertion",
                        "node": str(node),
                        "path": record["path"],
                        "source": record["source"],
                        "missing": missing,
                        "predicates_present": sorted({str(predicate) for predicate in graph.predicates(node)}),
                    }
                )
    return {
        "schema_version": 1,
        "scope": "Every RDF dependency file in the content-addressed Gate 4 dependency lock.",
        "files_scanned": files_scanned,
        "finding_count": len(findings),
        "status": "pass" if not findings else "fail-upstream",
        "findings": sorted(findings, key=lambda item: (item["path"], item["kind"], item["node"])),
    }


def main() -> int:
    output = HERE / "reports" / "dependency-owlapi-rdf-structures.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(audit(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
