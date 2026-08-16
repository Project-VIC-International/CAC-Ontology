"""Inventory SHACL SPARQL constraints that mention gUFO role/phase classifiers.

The inventory is a review aid, not a verdict: classifier-oriented constraints
can be correct.  Each occurrence is surfaced with its enclosing node shape and
targets so operational-level assumptions can be dispositioned explicitly.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from rdflib import Graph, Namespace


SH = Namespace("http://www.w3.org/ns/shacl#")


def inventory(ontology_dir: Path) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for path in sorted(ontology_dir.glob("*-shapes.ttl")):
        graph = Graph().parse(path, format="turtle")
        queries = list(graph.subject_objects(SH.select))
        queries += list(graph.subject_objects(SH.ask))
        queries += list(graph.subject_objects(SH.construct))
        for sparql_node, query in queries:
            text = str(query)
            mentions = [term for term in ("gufo:Role", "gufo:Phase") if term in text]
            if not mentions:
                continue
            owners = list(graph.subjects(SH.sparql, sparql_node))
            owner = owners[0] if owners else sparql_node
            results.append(
                {
                    "file": path.name,
                    "shape": str(owner),
                    "targets": sorted(str(value) for value in graph.objects(owner, SH.targetClass)),
                    "mentions": mentions,
                    "messages": sorted(str(value) for value in graph.objects(sparql_node, SH.message)),
                }
            )
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ontology-dir", type=Path, default=Path("ontology"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = inventory(args.ontology_dir)
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
