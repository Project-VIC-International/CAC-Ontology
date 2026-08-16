"""Parse every embedded SHACL SPARQL query and report syntax failures.

The audit is intentionally repository-wide.  Detection-shape findings are
reported separately because their repair belongs to PR #48 and must not be
duplicated on the v4 proposal branch.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from rdflib import Graph, Namespace
from rdflib.plugins.sparql.processor import prepareQuery


SH = Namespace("http://www.w3.org/ns/shacl#")


def audit(ontology_dir: Path) -> dict[str, object]:
    failures: list[dict[str, object]] = []
    query_count = 0
    files = sorted(ontology_dir.glob("*-shapes.ttl"))

    for path in files:
        graph = Graph().parse(path, format="turtle")
        queries = [
            ("select", owner, query)
            for owner, query in graph.subject_objects(SH.select)
        ]
        queries += [
            ("ask", owner, query)
            for owner, query in graph.subject_objects(SH.ask)
        ]
        queries += [
            ("construct", owner, query)
            for owner, query in graph.subject_objects(SH.construct)
        ]
        query_count += len(queries)
        for ordinal, (query_type, owner, query) in enumerate(queries, start=1):
            try:
                prepareQuery(str(query), initNs=dict(graph.namespaces()))
            except Exception as exc:  # parser exception types vary by defect
                failures.append(
                    {
                        "file": path.name,
                        "ordinal": ordinal,
                        "query_type": query_type,
                        "owner": str(owner),
                        "error_type": type(exc).__name__,
                        "error": str(exc).splitlines()[0],
                    }
                )

    detection = [f for f in failures if f["file"] == "cacontology-detection-shapes.ttl"]
    proposal = [f for f in failures if f not in detection]
    return {
        "shape_files": len(files),
        "queries": query_count,
        "failures": len(failures),
        "proposal_failures": len(proposal),
        "pr48_detection_failures": len(detection),
        "results": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ontology-dir", type=Path, default=Path("ontology"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = audit(args.ontology_dir)
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 1 if result["proposal_failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
