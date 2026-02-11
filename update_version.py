## This script is used to update the version of the CAC Ontology prior to publishing a new release.

import argparse
import os
from pathlib import Path

OLD_VERSION = "2.4.0"
NEW_VERSION = "2.5.0"

TTL_EXTENSION = ".ttl"
SKIP_DIRS = {".git", ".idea", ".vscode", "__pycache__", "node_modules"}


def update_versions(root: Path, dry_run: bool = False) -> int:
    total_replacements = 0

    for dirpath, dirnames, filenames in os.walk(root):
        # Skip unwanted directories
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for filename in filenames:
            file_path = Path(dirpath) / filename

            # Only process .ttl files
            if file_path.suffix.lower() != TTL_EXTENSION:
                continue

            try:
                content = file_path.read_text(encoding="utf-8")
            except Exception:
                # If we can't read it as UTF-8, skip
                continue

            if OLD_VERSION not in content:
                continue

            new_content = content.replace(OLD_VERSION, NEW_VERSION)
            replacements = content.count(OLD_VERSION)

            print(f"{'[DRY-RUN] ' if dry_run else ''}Updating {file_path} "
                  f"({replacements} replacement{'s' if replacements != 1 else ''})")

            if not dry_run:
                file_path.write_text(new_content, encoding="utf-8")

            total_replacements += replacements

    return total_replacements


def main():
    parser = argparse.ArgumentParser(
        description=f"Replace ontology version {OLD_VERSION} with {NEW_VERSION} in all .ttl files."
    )
    parser.add_argument(
        "--root",
        type=str,
        default=".",
        help="Root directory to scan (default: current directory).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Scan and report changes without modifying any files.",
    )

    args = parser.parse_args()
    root = Path(args.root).resolve()

    print(f"Scanning under: {root}")
    print(f"Replacing '{OLD_VERSION}' -> '{NEW_VERSION}' in .ttl files only")
    print(f"Dry run: {args.dry_run}")
    print("-" * 60)

    total = update_versions(root, dry_run=args.dry_run)

    print("-" * 60)
    print(f"Total replacements: {total}")
    if args.dry_run:
        print("No files were modified (dry run).")


if __name__ == "__main__":
    main()