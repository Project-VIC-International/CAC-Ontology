#!/usr/bin/env python3
"""Build the repository-wide Role/Phase term disposition evidence ledger."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

from rdflib import Graph, Namespace, OWL, RDF, RDFS, URIRef

CAC_CORE = Namespace("https://cacontology.projectvic.org/core#")
GUFO = Namespace("http://purl.org/nemo/gufo#")
FIELDS = (
    "iri", "source_file", "direct_parents", "explicit_gufo_type",
    "repository_instance_count", "adopter_instance_count_if_authorized",
    "observed_instance_predicates", "definition_evidence",
    "property_domain_range_evidence", "primary_level", "v4_action",
    "replacement_iri", "migration_mode", "asserted_delta", "inferred_delta",
    "fixture_ids", "reviewer_status",
)


def transitive_parents(graph: Graph) -> dict[URIRef, set[URIRef]]:
    parents: dict[URIRef, set[URIRef]] = defaultdict(set)
    for child, parent in graph.subject_objects(RDFS.subClassOf):
        if isinstance(child, URIRef) and isinstance(parent, URIRef):
            parents[child].add(parent)
    changed = True
    while changed:
        changed = False
        for child in list(parents):
            inherited = set().union(*(parents.get(parent, set()) for parent in parents[child]))
            if not inherited.issubset(parents[child]):
                parents[child].update(inherited)
                changed = True
    return parents


def main() -> int:
    here = Path(__file__).resolve().parent
    repo = here.parents[1]
    ontology = Graph()
    declared_in: dict[URIRef, list[str]] = defaultdict(list)
    for path in sorted((repo / "ontology").glob("*.ttl")):
        if "-shapes" in path.name:
            continue
        module = Graph().parse(path, format="turtle")
        ontology += module
        for term in module.subjects(RDF.type, OWL.Class):
            if isinstance(term, URIRef):
                declared_in[term].append(path.relative_to(repo).as_posix())

    examples = Graph()
    for path in sorted((repo / "examples_knowledge_graphs").glob("*.ttl")):
        try:
            examples.parse(path, format="turtle")
        except Exception:
            continue

    parents = transitive_parents(ontology)
    classes = {term for term in ontology.subjects(RDF.type, OWL.Class) if isinstance(term, URIRef)}
    overrides = json.loads((here / "term-disposition-overrides.json").read_text(encoding="utf-8"))
    reviewed_groups = json.loads((here / "reviewed-term-groups.json").read_text(encoding="utf-8"))["groups"]
    group_overrides = {}
    for group in reviewed_groups:
        values = {key: value for key, value in group.items() if key not in ("group_id", "exact_iris")}
        for iri in group["exact_iris"]:
            if iri in group_overrides:
                raise ValueError(f"Term appears in multiple reviewed groups: {iri}")
            group_overrides[iri] = values
    unchanged = json.loads((here / "reviewed-unchanged-terms.json").read_text(encoding="utf-8"))
    unchanged_overrides = {}
    for iri in unchanged["role_record_iris"]:
        unchanged_overrides[iri] = {
            "primary_level": "role-record",
            "v4_action": "unchanged",
            "migration_mode": "automatic",
            "asserted_delta": "none; verified operational role branch with no classifier or cross-branch overlap",
            "inferred_delta": "none intended",
            "fixture_ids": "RQ-07|RQ-08",
            "reviewer_status": "reviewed",
        }
    for iri in unchanged["phase_occurrence_iris"]:
        unchanged_overrides[iri] = {
            "primary_level": "phase-occurrence",
            "v4_action": "unchanged",
            "migration_mode": "automatic",
            "asserted_delta": "none; verified operational phase branch with no classifier or cross-branch overlap",
            "inferred_delta": "none intended",
            "fixture_ids": "PQ-01|PQ-05|PQ-08",
            "reviewer_status": "reviewed",
        }
    branch_candidates = {
        term for term in classes
        if term in (CAC_CORE.Role, CAC_CORE.Phase)
        or CAC_CORE.Role in parents.get(term, set())
        or CAC_CORE.Phase in parents.get(term, set())
    }
    # Preserve reviewed dispositions after a move removes the term from the
    # current branch; otherwise regeneration would erase the migration record.
    candidates = sorted(
        branch_candidates
        | {URIRef(iri) for iri in overrides}
        | {URIRef(iri) for iri in group_overrides}
        | {URIRef(iri) for iri in unchanged_overrides}
    )
    rows = []
    for term in candidates:
        instances = set(examples.subjects(RDF.type, term))
        predicates = sorted({str(predicate) for instance in instances for predicate in examples.predicates(instance, None)})
        domain_range = sorted(
            str(prop)
            for predicate in (RDFS.domain, RDFS.range)
            for prop in ontology.subjects(predicate, term)
        )
        comments = [str(value).replace("\n", " ") for value in ontology.objects(term, RDFS.comment)]
        row = {
            "iri": str(term),
            "source_file": "|".join(sorted(declared_in.get(term, []))),
            "direct_parents": "|".join(sorted(str(value) for value in ontology.objects(term, RDFS.subClassOf) if isinstance(value, URIRef))),
            "explicit_gufo_type": "|".join(sorted(str(value) for value in ontology.objects(term, RDF.type) if str(value).startswith(str(GUFO)))),
            "repository_instance_count": str(len(instances)),
            "adopter_instance_count_if_authorized": "not-authorized",
            "observed_instance_predicates": "|".join(predicates),
            "definition_evidence": " || ".join(comments),
            "property_domain_range_evidence": "|".join(domain_range),
            "primary_level": "ambiguous",
            "v4_action": "unchanged",
            "replacement_iri": "",
            "migration_mode": "manual",
            "asserted_delta": "none pending review",
            "inferred_delta": "not evaluated",
            "fixture_ids": "",
            "reviewer_status": "pending",
        }
        row.update(group_overrides.get(str(term), {}))
        row.update(unchanged_overrides.get(str(term), {}))
        row.update(overrides.get(str(term), {}))
        rows.append(row)

    output = here / "term-disposition-ledger.csv"
    with output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "schema_version": 1,
        "rows": len(rows),
        "reviewed": sum(row["reviewer_status"] == "reviewed" for row in rows),
        "pending": sum(row["reviewer_status"] != "reviewed" for row in rows),
        "policy": "A pending or ambiguous row is not authorized for semantic edit.",
    }
    (here / "term-disposition-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
