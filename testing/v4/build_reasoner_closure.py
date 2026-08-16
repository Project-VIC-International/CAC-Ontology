#!/usr/bin/env python3
"""Build deterministic offline OWL reasoner inputs for Gate 4."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from rdflib import BNode, Graph, Namespace, OWL, RDF, RDFS, URIRef
import architecture_audit as architecture

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SWRL = Namespace("http://www.w3.org/2003/11/swrl#")
UCO_ACTION = Namespace("https://ontology.unifiedcyberontology.org/uco/action/")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def input_set_digest(configuration: str, cac_inputs: list[dict], dependency_inputs: list[dict]) -> str:
    identity = {
        "configuration": configuration,
        "cac_inputs": sorted((item["path"], item["sha256"]) for item in cac_inputs),
        "dependency_inputs": sorted(
            (item["path"], item["sha256"]) for item in dependency_inputs
        ),
    }
    return hashlib.sha256(
        json.dumps(identity, separators=(",", ":"), sort_keys=True).encode("utf-8")
    ).hexdigest()


def remove_node_closure(graph: Graph, roots: set) -> int:
    nodes = set(roots)
    queue = list(roots)
    while queue:
        node = queue.pop()
        for _, value in graph.predicate_objects(node):
            if isinstance(value, BNode) or (
                isinstance(value, URIRef) and str(value).startswith("urn:swrl#")
            ):
                if value not in nodes:
                    nodes.add(value)
                    queue.append(value)
    triples = {
        triple
        for node in nodes
        for triple in (*graph.triples((node, None, None)), *graph.triples((None, None, node)))
    }
    for triple in triples:
        graph.remove(triple)
    return len(triples)


def apply_diagnostic_projection(graph: Graph) -> dict:
    swrl_rules = set(graph.subjects(RDF.type, SWRL.Imp))
    swrl_triples = remove_node_closure(graph, swrl_rules)

    invalid_axioms = {
        node
        for node in graph.subjects(RDF.type, OWL.Axiom)
        if any(
            not list(graph.objects(node, predicate))
            for predicate in (OWL.annotatedSource, OWL.annotatedProperty, OWL.annotatedTarget)
        )
    }
    invalid_negative_assertions = set()
    for node in graph.subjects(RDF.type, OWL.NegativePropertyAssertion):
        if (
            not list(graph.objects(node, OWL.sourceIndividual))
            or not list(graph.objects(node, OWL.assertionProperty))
            or not (
                list(graph.objects(node, OWL.targetIndividual))
                or list(graph.objects(node, OWL.targetValue))
            )
        ):
            invalid_negative_assertions.add(node)
    invalid_roots = invalid_axioms | invalid_negative_assertions
    invalid_triples = remove_node_closure(graph, invalid_roots)

    # UCO 1.5.0 declares action:phase as a subproperty of action:subaction,
    # while their ranges are respectively ArrayOfAction (an inherent
    # characterization thing) and Action (a UcoObject). Those branches are
    # disjoint, so the exact upstream axiom makes action:phase bottom. Keep the
    # full closure normative and remove only this exact, pinned upstream axiom
    # in the explicitly non-normative CAC diagnostic projection.
    upstream_bottom_property_axioms = {
        (UCO_ACTION.phase, RDFS.subPropertyOf, UCO_ACTION.subaction)
    }
    removed_upstream_bottom_property_axioms = []
    for triple in sorted(upstream_bottom_property_axioms, key=lambda item: tuple(map(str, item))):
        if triple in graph:
            graph.remove(triple)
            removed_upstream_bottom_property_axioms.append(tuple(map(str, triple)))
    return {
        "status": "non-normative-diagnostic-only",
        "removed_swrl_rules": len(swrl_rules),
        "removed_swrl_rule_triples": swrl_triples,
        "removed_incomplete_axioms": len(invalid_axioms),
        "removed_incomplete_negative_property_assertions": len(invalid_negative_assertions),
        "removed_invalid_structure_triples": invalid_triples,
        "removed_upstream_bottom_property_axioms": removed_upstream_bottom_property_axioms,
        "claim_limit": "A passing projection does not satisfy the full-import OWL 2 DL gate.",
    }


def build(configuration: str, output: Path, *, diagnostic_projection: bool = False) -> dict:
    if configuration not in {"C3", "C4", "C5"}:
        raise ValueError("OWL 2 DL release gates are C3, C4, and C5")
    lock = json.loads((HERE / "dependency-lock.json").read_text(encoding="utf-8"))
    graph, cac_inputs = architecture.load_configuration_graph(REPO, configuration)
    catalog = {record["requested_iri"]: record for record in lock["imports"]}
    loaded_paths = {record["path"] for record in cac_inputs}
    dependency_inputs = []
    queue = [str(iri) for iri in graph.objects(None, OWL.imports)]
    visited_iris: set[str] = set()
    while queue:
        iri = queue.pop(0)
        if iri in visited_iris:
            continue
        visited_iris.add(iri)
        record = catalog.get(iri)
        if record is None or record["status"] == "unresolved-remote":
            raise RuntimeError(f"Import is not locked: {iri}")
        if record["path"] in loaded_paths:
            continue
        loaded_paths.add(record["path"])
        path = REPO / record["path"]
        rdf_format = "xml" if path.suffix.lower() == ".owl" else "turtle"
        imported = Graph().parse(path, format=rdf_format)
        queue.extend(str(value) for value in imported.objects(None, OWL.imports))
        graph += imported
        dependency_inputs.append(record)

    import_triples = list(graph.triples((None, OWL.imports, None)))
    for triple in import_triples:
        graph.remove(triple)

    projection = apply_diagnostic_projection(graph) if diagnostic_projection else None

    output.parent.mkdir(parents=True, exist_ok=True)
    graph.serialize(destination=output, format="xml")
    return {
        "schema_version": 1,
        "configuration": configuration,
        "scope": "Offline transitive semantic closure with owl:imports declarations removed only after all locked imported graphs are materialized.",
        "diagnostic_projection": projection,
        "triples": len(graph),
        "imports_materialized": len(import_triples),
        "input_set_sha256": input_set_digest(configuration, cac_inputs, dependency_inputs),
        "serialized_path": output.relative_to(REPO).as_posix(),
        "serialized_bytes": output.stat().st_size,
        "serialized_sha256": sha256(output),
        "cac_inputs": cac_inputs,
        "dependency_inputs": dependency_inputs,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--configuration", choices=("C3", "C4", "C5"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--diagnostic-projection", action="store_true")
    args = parser.parse_args()
    report = build(
        args.configuration,
        args.output,
        diagnostic_projection=args.diagnostic_projection,
    )
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
