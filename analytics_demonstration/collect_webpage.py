#!/usr/bin/env python3
"""
Utility helpers for collecting and preprocessing web pages for CAC Ontology ingestion.

This is intentionally dependency-free (stdlib only) so it runs in constrained environments.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from html.parser import HTMLParser
from pathlib import Path


class _HTMLTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []

    def handle_data(self, data: str) -> None:  # noqa: D401
        # Collapse internal whitespace, keep only meaningful text nodes.
        cleaned = re.sub(r"\s+", " ", data).strip()
        if cleaned:
            self._chunks.append(cleaned)

    @property
    def text_lines(self) -> list[str]:
        # De-dupe consecutive identical lines (common in nav menus / repeated labels).
        out: list[str] = []
        for ln in self._chunks:
            if not out or out[-1] != ln:
                out.append(ln)
        return out


def sha256_hex(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest()


def normalize_html_to_text(source_html: Path) -> str:
    parser = _HTMLTextExtractor()
    parser.feed(source_html.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(parser.text_lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-html", required=True, help="Path to downloaded HTML file")
    ap.add_argument(
        "--out-normalized",
        required=True,
        help="Path to write normalized text output",
    )
    ap.add_argument(
        "--print-hash",
        action="store_true",
        help="Print SHA-256 of source HTML (hex)",
    )
    args = ap.parse_args()

    source_html = Path(args.source_html)
    out_normalized = Path(args.out_normalized)

    out_normalized.parent.mkdir(parents=True, exist_ok=True)
    out_normalized.write_text(normalize_html_to_text(source_html), encoding="utf-8")

    if args.print_hash:
        print(sha256_hex(source_html))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

