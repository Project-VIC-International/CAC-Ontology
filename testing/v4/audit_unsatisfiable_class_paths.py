#!/usr/bin/env python3
"""Trace HermiT-reported unsatisfiable classes to asserted category paths."""

from __future__ import annotations

from collections import deque
import json
import re
from pathlib import Path

from rdflib import Graph, RDFS, URIRef

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
REPORTS = HERE / "reports"
WORK = HERE / "tmp" / "reasoner"

MARKERS = {
    "gufo:Endurant": URIRef("http://purl.org/nemo/gufo#Endurant"),
    "gufo:Event": URIRef("http://purl.org/nemo/gufo#Event"),
    "gufo:Situation": URIRef("http://purl.org/nemo/gufo#Situation"),
    "gufo:Type": URIRef("http://purl.org/nemo/gufo#Type"),
    "gufo:Individual": URIRef("http://purl.org/nemo/gufo#Individual"),
    "gufo:AbstractIndividual": URIRef("http://purl.org/nemo/gufo#AbstractIndividual"),
    "drafting:Endurant": URIRef("http://example.org/ontology/drafting/Endurant"),
    "drafting:Perdurant": URIRef("http://example.org/ontology/drafting/Perdurant"),
    "uco-core:UcoObject": URIRef("https://ontology.unifiedcyberontology.org/uco/core/UcoObject"),
    "uco-core:UcoInherentCharacterizationThing": URIRef(
        "https://ontology.unifiedcyberontology.org/uco/core/UcoInherentCharacterizationThing"
    ),
}


def shortest_path(graph: Graph, start: URIRef, target: URIRef) -> list[str] | None:
    queue = deque([(start, [start])])
    seen = {start}
    while queue:
        current, path = queue.popleft()
        if current == target:
            return [str(node) for node in path]
        for parent in sorted(
            (value for value in graph.objects(current, RDFS.subClassOf) if isinstance(value, URIRef)),
            key=str,
        ):
            if parent not in seen:
                seen.add(parent)
                queue.append((parent, path + [parent]))
    return None


def main() -> int:
    log = (REPORTS / "c4-diagnostic-hermit.log").read_text(encoding="utf-8")
    classes = sorted(
        {
            URIRef(match)
            for match in re.findall(r"unsatisfiable: (https://cacontology\.projectvic\.org/\S+)", log)
        },
        key=str,
    )
    graph = Graph().parse(WORK / "c4-diagnostic-projection.owl", format="xml")
    records = []
    for term in classes:
        paths = {
            label: path
            for label, marker in MARKERS.items()
            if (path := shortest_path(graph, term, marker)) is not None
        }
        records.append(
            {
                "class": str(term),
                "direct_named_superclasses": sorted(
                    str(value)
                    for value in graph.objects(term, RDFS.subClassOf)
                    if isinstance(value, URIRef)
                ),
                "category_paths": paths,
            }
        )
    report = {
        "schema_version": 1,
        "configuration": "C4-diagnostic-projection",
        "status": "fail" if classes else "pass",
        "unsatisfiable_class_count": len(classes),
        "classes": records,
        "claim_limit": "Paths are asserted rdfs:subClassOf traces; HermiT is authoritative for unsatisfiability.",
    }
    output = REPORTS / "c4-unsatisfiable-class-paths.json"
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
