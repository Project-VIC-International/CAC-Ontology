#!/usr/bin/env python3
"""Freeze exact reviewed lists for unchanged operational Role/Phase terms."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from rdflib import Graph, Namespace, OWL, RDF, RDFS, URIRef

CORE = Namespace("https://cacontology.projectvic.org/core#")
GUFO = Namespace("http://purl.org/nemo/gufo#")


def ancestors(graph: Graph) -> dict[URIRef, set[URIRef]]:
    values: dict[URIRef, set[URIRef]] = defaultdict(set)
    for child, parent in graph.subject_objects(RDFS.subClassOf):
        if isinstance(child, URIRef) and isinstance(parent, URIRef):
            values[child].add(parent)
    changed = True
    while changed:
        changed = False
        for child in list(values):
            inherited = set().union(*(values.get(parent, set()) for parent in values[child]))
            if not inherited.issubset(values[child]):
                values[child].update(inherited)
                changed = True
    return values


def main() -> int:
    here = Path(__file__).resolve().parent
    repo = here.parents[1]
    graph = Graph()
    for path in sorted((repo / "ontology").glob("*.ttl")):
        if "-shapes" not in path.name:
            graph.parse(path, format="turtle")
    parents = ancestors(graph)
    classes = {term for term in graph.subjects(RDF.type, OWL.Class) if isinstance(term, URIRef)}
    groups = json.loads((here / "reviewed-term-groups.json").read_text(encoding="utf-8"))["groups"]
    overrides = json.loads((here / "term-disposition-overrides.json").read_text(encoding="utf-8"))
    already_reviewed = set(overrides)
    for group in groups:
        already_reviewed.update(group["exact_iris"])

    role_terms = {
        term for term in classes
        if term == CORE.Role or CORE.Role in parents.get(term, set())
    }
    phase_terms = {
        term for term in classes
        if term == CORE.Phase or CORE.Phase in parents.get(term, set())
    }
    event_terms = {
        term for term in classes
        if term == CORE.Event or CORE.Event in parents.get(term, set())
    }
    enduring_terms = {
        term for term in classes
        if term == CORE.EnduringEntity or CORE.EnduringEntity in parents.get(term, set())
    }

    remaining_role = {term for term in role_terms if str(term) not in already_reviewed}
    remaining_phase = {term for term in phase_terms if str(term) not in already_reviewed}
    invalid = set()
    invalid.update(term for term in remaining_role if (term, RDF.type, GUFO.Role) in graph)
    invalid.update(term for term in remaining_phase if (term, RDF.type, GUFO.Phase) in graph)
    invalid.update(remaining_role & (phase_terms | enduring_terms | event_terms))
    invalid.update(remaining_phase & (role_terms | enduring_terms | event_terms))
    if invalid:
        raise ValueError("Unchanged disposition preconditions failed: " + ", ".join(sorted(map(str, invalid))))

    result = {
        "schema_version": 1,
        "review_rule": "Exact current descendants with no gUFO metaclass typing and no Role/Phase/Event/Enduring cross-branch overlap.",
        "role_record_iris": sorted(map(str, remaining_role)),
        "phase_occurrence_iris": sorted(map(str, remaining_phase)),
    }
    (here / "reviewed-unchanged-terms.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
