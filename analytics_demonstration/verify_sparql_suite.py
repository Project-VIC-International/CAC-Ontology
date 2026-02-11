#!/usr/bin/env python3
"""
Run a SPARQL verification suite (subset aligned to prompt.md Phase 6) over a TTL dataset.

Outputs a simple markdown report with pass/fail/review.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import rdflib


PREFIXES = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

PREFIX uco-action: <https://ontology.unifiedcyberontology.org/uco/action/>
PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
PREFIX uco-observable: <https://ontology.unifiedcyberontology.org/uco/observable/>
PREFIX investigation: <https://ontology.caseontology.org/case/investigation/>
"""


@dataclass(frozen=True)
class Check:
    id: str
    title: str
    query: str
    expected_zero: bool = True
    note: str | None = None


CHECKS: list[Check] = [
    Check(
        id="1",
        title="Collection actions have startTime",
        query="""
SELECT ?action WHERE {
  ?action a investigation:InvestigativeAction .
  FILTER NOT EXISTS { ?action uco-action:startTime ?t }
}
""",
    ),
    Check(
        id="1a",
        title="Collection actions have performer",
        query="""
SELECT ?action WHERE {
  ?action a investigation:InvestigativeAction .
  FILTER NOT EXISTS { ?action uco-action:performer ?p }
}
""",
    ),
    Check(
        id="2",
        title="Facet integrity: every hasFacet target is typed",
        query="""
SELECT ?obj ?facet WHERE {
  ?obj uco-core:hasFacet ?facet .
  FILTER NOT EXISTS { ?facet a ?type }
}
""",
    ),
    Check(
        id="3",
        title="UUID coverage: instance IRIs should be urn:uuid:",
        query="""
SELECT DISTINCT ?s WHERE {
  ?s ?p ?o .
  FILTER(isIRI(?s) && STRSTARTS(STR(?s), "urn:uuid:") = false && STRSTARTS(STR(?s), "http") = false)
}
""",
        note="Expected: 0 results (only ontology IRIs should be http(s)).",
    ),
    Check(
        id="4",
        title="Typed node coverage: all urn:uuid nodes have rdf:type",
        query="""
SELECT DISTINCT ?node WHERE {
  { ?node ?p ?o } UNION { ?s ?p ?node }
  FILTER(isIRI(?node) && STRSTARTS(STR(?node), "urn:uuid:"))
  FILTER NOT EXISTS { ?node a ?type }
}
""",
    ),
    Check(
        id="11",
        title="Isolated nodes: urn:uuid nodes must have degree >= 1 (excluding rdf:type)",
        query="""
SELECT ?node ?type WHERE {
  ?node a ?type .
  FILTER(STRSTARTS(STR(?node), "urn:uuid:"))
  FILTER NOT EXISTS { ?node ?p ?o . FILTER(?p != rdf:type) }
  FILTER NOT EXISTS { ?s ?p ?node . FILTER(?p != rdf:type) }
}
""",
    ),
]


def run_check(g: rdflib.Graph, c: Check) -> tuple[str, int]:
    q = PREFIXES + c.query
    res = list(g.query(q))
    return ("PASS" if (len(res) == 0) == c.expected_zero else "FAIL", len(res))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="Path to TTL dataset to verify")
    ap.add_argument("--out", required=True, help="Path to write markdown report")
    args = ap.parse_args()

    data_path = Path(args.data)
    out_path = Path(args.out)

    g = rdflib.Graph()
    g.parse(str(data_path), format="turtle")

    lines: list[str] = []
    lines.append("## SPARQL Verification Suite (subset)\n")
    lines.append(f"- **Dataset**: `{data_path.as_posix()}`\n")
    lines.append(f"- **Triples**: {len(g):,}\n\n")
    lines.append("| Check | Result | Count | Notes |\n")
    lines.append("|---|---|---:|---|\n")
    for c in CHECKS:
        status, count = run_check(g, c)
        note = c.note or ""
        lines.append(f"| {c.id} {c.title} | **{status}** | {count} | {note} |\n")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

