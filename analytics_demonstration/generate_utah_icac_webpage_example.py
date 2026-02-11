#!/usr/bin/env python3
"""
Generate a UUID-only example KG for the Utah AG ICAC Task Force webpage collection.

This script is intentionally stdlib-only and writes:
  - examples_knowledge_graphs/utah-icac-task-force-webpage-example.ttl

It starts from the existing skeleton TTL and appends additional in-scope modeling:
  - affiliates list (as Organizations, connected via one listing Action)
  - crimes investigated (as UcoObjects, connected via one Action)
  - funding/admin context (OJJDP + Utah AG Office, connected via one Action)
  - Digital Respons-Ability program statement (as UcoObject + Action)

Evidence pointers are recorded as human-readable descriptions referencing
`normalized.txt` line numbers (no new ontology terms introduced).
"""

from __future__ import annotations

import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

NORMALIZED = (
    ROOT
    / "analytics_demonstration/collected_sources/utah-icac-task-force/normalized.txt"
)
SKELETON = ROOT / "examples_knowledge_graphs/utah-icac-task-force-webpage-skeleton.ttl"
OUT = ROOT / "examples_knowledge_graphs/utah-icac-task-force-webpage-example.ttl"


# Fixed IDs already established in the skeleton/manifest (do not change).
DOC_ID = "82588a71-7176-4cd0-aaee-56cffc467f86"
TASK_FORCE_ORG_ID = "af3aaac8-c561-4223-bcb3-0787f90c14b9"
COLLECTED_AT = "2026-01-07T02:59:19Z"


def _uuid_ns() -> uuid.UUID:
    """
    Deterministic namespace for this document.
    Using the document UUID ensures stable IDs across re-runs.
    """
    return uuid.UUID(DOC_ID)


def uuid5(name: str) -> str:
    """Deterministic UUIDv5 (document-scoped)."""
    return str(uuid.uuid5(_uuid_ns(), name))


def find_line(lines: list[str], target: str) -> int | None:
    for i, ln in enumerate(lines, start=1):
        if ln.strip() == target:
            return i
    return None


def main() -> int:
    lines = NORMALIZED.read_text(encoding="utf-8", errors="ignore").splitlines()

    start_aff = find_line(lines, "Utah Attorney General ICAC Affiliates")
    end_aff = find_line(lines, "Follow Us")
    if not start_aff or not end_aff or end_aff <= start_aff:
        raise SystemExit("Could not locate affiliates section bounds in normalized.txt")

    affiliates: list[str] = []
    for ln in lines[start_aff : end_aff - 1]:
        ln = ln.strip()
        if not ln or ln == "Utah Attorney General ICAC Affiliates":
            continue
        affiliates.append(ln)

    ids = {
        "affiliation_action": uuid5("action:affiliates_listed"),
        "affiliation_prov": uuid5("prov:affiliates_listed"),
        "crimes_action": uuid5("action:crimes_investigated_listed"),
        "crimes_prov": uuid5("prov:crimes_investigated_listed"),
        "funding_action": uuid5("action:funding_admin_context"),
        "funding_prov": uuid5("prov:funding_admin_context"),
        "ojjdp_org": uuid5("org:ojjdp"),
        "utag_org": uuid5("org:utah_ag_office"),
        "digital_program": uuid5("obj:digital_respons_ability"),
        "digital_program_action": uuid5("action:digital_respons_ability_statement"),
        "digital_program_prov": uuid5("prov:digital_respons_ability_statement"),
        "crime1": uuid5("obj:crime:sexual_exploitation_minor"),
        "crime2": uuid5("obj:crime:enticement_minor_internet"),
        "crime3": uuid5("obj:crime:material_harmful_minor"),
    }

    append: list[str] = []
    append.append(
        "\n# =============================================================================\n"
        "# Extended example modeling (affiliates, crime focus, funding, education program)\n"
        "# Source evidence: analytics_demonstration/collected_sources/utah-icac-task-force/normalized.txt\n"
        "# =============================================================================\n\n"
    )

    append.append(
        f"ex:{ids['utag_org']} a uco-identity:Organization ;\n"
        '    rdfs:label "Utah Attorney General\'s Office"@en .\n\n'
    )
    append.append(
        f"ex:{ids['ojjdp_org']} a uco-identity:Organization ;\n"
        '    rdfs:label "Office of Juvenile Justice and Delinquency Prevention"@en .\n\n'
    )

    append.append(
        f"ex:{ids['funding_action']} a uco-action:Action ;\n"
        '    rdfs:label "Webpage states ICAC Task Force funding/admin context"@en ;\n'
        f'    uco-action:startTime "{COLLECTED_AT}"^^xsd:dateTime ;\n'
        f"    uco-action:performer ex:{TASK_FORCE_ORG_ID} ;\n"
        f"    uco-action:object ex:{DOC_ID}, ex:{ids['ojjdp_org']}, ex:{ids['utag_org']} ;\n"
        "    uco-core:description \"Grounded in normalized.txt lines 37-40: funded by a grant from OJJDP and administered through the Utah Attorney General's Office.\"@en .\n\n"
    )
    append.append(
        f"ex:{ids['funding_prov']} a investigation:ProvenanceRecord ;\n"
        '    rdfs:label "Provenance: funding/admin statements"@en ;\n'
        f"    uco-core:object ex:{DOC_ID} ;\n"
        f"    investigation:provenanceRecordAction ex:{ids['funding_action']} ;\n"
        '    uco-core:description "Evidence pointer: normalized.txt lines 37-40."@en .\n\n'
    )

    append.append(
        f"ex:{ids['crime1']} a uco-core:UcoObject ;\n"
        '    rdfs:label "Sexual Exploitation of a Minor"@en ;\n'
        '    uco-core:description "(possessing, distributing and manufacturing child pornography)"@en .\n\n'
    )
    append.append(
        f"ex:{ids['crime2']} a uco-core:UcoObject ;\n"
        '    rdfs:label "Enticing a Minor over the Internet"@en ;\n'
        '    uco-core:description "(with the intent of committing sexual acts to the child)"@en .\n\n'
    )
    append.append(
        f"ex:{ids['crime3']} a uco-core:UcoObject ;\n"
        '    rdfs:label "Dealing in Material Harmful to a Minor"@en ;\n'
        '    uco-core:description "(sending pornography to a minor and/or sexting)"@en .\n\n'
    )
    append.append(
        f"ex:{ids['crimes_action']} a uco-action:Action ;\n"
        '    rdfs:label "Webpage lists crimes investigated by the task force"@en ;\n'
        f'    uco-action:startTime "{COLLECTED_AT}"^^xsd:dateTime ;\n'
        f"    uco-action:performer ex:{TASK_FORCE_ORG_ID} ;\n"
        f"    uco-action:object ex:{DOC_ID}, ex:{ids['crime1']}, ex:{ids['crime2']}, ex:{ids['crime3']} ;\n"
        '    uco-core:description "Grounded in normalized.txt lines 49-52 (Crimes We Investigate)."@en .\n\n'
    )
    append.append(
        f"ex:{ids['crimes_prov']} a investigation:ProvenanceRecord ;\n"
        '    rdfs:label "Provenance: crimes investigated list"@en ;\n'
        f"    uco-core:object ex:{DOC_ID} ;\n"
        f"    investigation:provenanceRecordAction ex:{ids['crimes_action']} ;\n"
        '    uco-core:description "Evidence pointer: normalized.txt lines 49-52."@en .\n\n'
    )

    append.append(
        f"ex:{ids['digital_program']} a uco-core:UcoObject ;\n"
        '    rdfs:label "Digital Respons-Ability program"@en ;\n'
        '    uco-core:description "Program described on the webpage; sponsored to educate children, parents, and the community on Internet safety presentations."@en .\n\n'
    )
    append.append(
        f"ex:{ids['digital_program_action']} a uco-action:Action ;\n"
        '    rdfs:label "Webpage states sponsorship of Digital Respons-Ability program"@en ;\n'
        f'    uco-action:startTime "{COLLECTED_AT}"^^xsd:dateTime ;\n'
        f"    uco-action:performer ex:{ids['utag_org']} ;\n"
        f"    uco-action:object ex:{DOC_ID}, ex:{ids['digital_program']} ;\n"
        '    uco-core:description "Grounded in normalized.txt lines 46-48."@en .\n\n'
    )
    append.append(
        f"ex:{ids['digital_program_prov']} a investigation:ProvenanceRecord ;\n"
        '    rdfs:label "Provenance: Digital Respons-Ability program statement"@en ;\n'
        f"    uco-core:object ex:{DOC_ID} ;\n"
        f"    investigation:provenanceRecordAction ex:{ids['digital_program_action']} ;\n"
        '    uco-core:description "Evidence pointer: normalized.txt lines 46-48."@en .\n\n'
    )

    append.append("# -- Affiliates listed on webpage (each connected via one listing action)\n\n")
    affiliate_ids: list[str] = []
    for name in affiliates:
        u = uuid5(f"affiliate:{name}")
        affiliate_ids.append(u)
        safe = name.replace('"', '\\"')
        append.append(
            f"ex:{u} a uco-identity:Organization ;\n"
            f'    rdfs:label "{safe}"@en .\n\n'
        )

    append.append(
        f"ex:{ids['affiliation_action']} a uco-action:Action ;\n"
        '    rdfs:label "Webpage lists Utah ICAC affiliates"@en ;\n'
        f'    uco-action:startTime "{COLLECTED_AT}"^^xsd:dateTime ;\n'
        f"    uco-action:performer ex:{TASK_FORCE_ORG_ID} ;\n"
        f"    uco-action:object ex:{DOC_ID},\n"
    )
    for i, u in enumerate(affiliate_ids):
        sep = "," if i < len(affiliate_ids) - 1 else " ;"
        append.append(f"                    ex:{u}{sep}\n")
    append.append(
        f'    uco-core:description "Grounded in normalized.txt lines {start_aff}-{end_aff - 1} (affiliate agency list)."@en .\n\n'
    )
    append.append(
        f"ex:{ids['affiliation_prov']} a investigation:ProvenanceRecord ;\n"
        '    rdfs:label "Provenance: affiliates list"@en ;\n'
        f"    uco-core:object ex:{DOC_ID} ;\n"
        f"    investigation:provenanceRecordAction ex:{ids['affiliation_action']} ;\n"
        f'    uco-core:description "Evidence pointer: normalized.txt lines {start_aff}-{end_aff - 1}."@en .\n\n'
    )

    base = SKELETON.read_text(encoding="utf-8", errors="ignore")
    OUT.write_text(base + "".join(append), encoding="utf-8")
    print(f"Wrote {OUT} (affiliates={len(affiliates)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

