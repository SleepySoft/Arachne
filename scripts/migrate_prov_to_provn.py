#!/usr/bin/env python3
"""
Migrate legacy PROV JSON files to PROV-N format.

Usage:
    python scripts/migrate_prov_to_provn.py

Scans data/prov_statements/*.prov.json, converts each to a PROV-N document,
writes it to *.provn, and removes the legacy JSON file.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Add backend dir to path so we can import app.*
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.models.prov_schema import ProvStatement
from app.services.prov_n import serialize_provn


PROV_DIR = Path(__file__).resolve().parent.parent / "data" / "prov_statements"


def main() -> None:
    if not PROV_DIR.exists():
        print(f"PROV directory does not exist: {PROV_DIR}")
        return

    files = sorted(PROV_DIR.glob("*.prov.json"))
    if not files:
        print("No legacy .prov.json files found.")
        return

    for json_path in files:
        node_id = json_path.stem.replace(".prov", "")
        provn_path = PROV_DIR / f"{node_id}.provn"

        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"  SKIP {json_path.name}: JSON decode error ({e})")
            continue

        if not isinstance(data, list):
            print(f"  SKIP {json_path.name}: expected a list of statements")
            continue

        statements: list[ProvStatement] = []
        for item in data:
            try:
                statements.append(ProvStatement(**item))
            except Exception as e:
                print(f"  WARN {json_path.name}: skipping malformed statement ({e})")
                continue

        text = serialize_provn(statements, node_id)
        provn_path.write_text(text, encoding="utf-8")
        json_path.unlink()
        print(f"  MIGRATED {json_path.name} -> {provn_path.name} ({len(statements)} statements)")

    print(f"\nMigration complete. {len(files)} file(s) converted to PROV-N.")


if __name__ == "__main__":
    main()
