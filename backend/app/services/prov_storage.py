"""
File-based storage layer for PROV statements.

PROV statements are persisted as PROV-N documents under `data/prov_statements/`.
Each file is named `{node_id}.provn` and contains a self-contained PROV-N
document with declarations and the relation statements whose subject is
`node_id`. The format is human-readable, diffable, and standard PROV-N.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple
from uuid import UUID

from app.models.prov_schema import ProvStatement, ProvRelation, ProvRole
from app.services.prov_n import parse_provn, serialize_provn


# ---------------------------------------------------------------------------
# Storage layout
# ---------------------------------------------------------------------------

PROV_DIR = Path(__file__).resolve().parents[3] / "data" / "prov_statements"


def _ensure_dir() -> None:
    PROV_DIR.mkdir(parents=True, exist_ok=True)


def _node_file(node_id: str) -> Path:
    _ensure_dir()
    return PROV_DIR / f"{node_id}.provn"


def _legacy_node_file(node_id: str) -> Path:
    _ensure_dir()
    return PROV_DIR / f"{node_id}.prov.json"


def _load_statements(node_id: str) -> List[ProvStatement]:
    path = _node_file(node_id)
    legacy_path = _legacy_node_file(node_id)

    if not path.exists() and legacy_path.exists():
        # Fallback: load legacy JSON once, then caller can migrate if desired.
        try:
            with legacy_path.open("r", encoding="utf-8") as f:
                raw = json.load(f)
            if isinstance(raw, list):
                statements: List[ProvStatement] = []
                for item in raw:
                    try:
                        statements.append(ProvStatement(**item))
                    except Exception:
                        continue
                return statements
        except (json.JSONDecodeError, OSError):
            pass

    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return []

    _, statements = parse_provn(text)
    return statements


def _save_statements(node_id: str, statements: List[ProvStatement]) -> None:
    path = _node_file(node_id)
    legacy_path = _legacy_node_file(node_id)

    if not statements:
        if path.exists():
            path.unlink()
        if legacy_path.exists():
            legacy_path.unlink()
        return

    text = serialize_provn(statements, node_id)

    # Atomic write: write to temp file in the same directory, then rename.
    fd, tmp_path = tempfile.mkstemp(
        suffix=".tmp", prefix=f"{node_id}_", dir=str(PROV_DIR)
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.unlink(tmp_path)
        except FileNotFoundError:
            pass
        raise

    # Remove legacy JSON after successful PROV-N write.
    if legacy_path.exists():
        try:
            legacy_path.unlink()
        except OSError:
            pass


def get_provn_text(node_id: str) -> Optional[str]:
    """Return the raw PROV-N text for a node, or a default document if none."""
    path = _node_file(node_id)
    if path.exists():
        try:
            return path.read_text(encoding="utf-8")
        except OSError:
            return None
    legacy_path = _legacy_node_file(node_id)
    if legacy_path.exists():
        statements = _load_statements(node_id)
        return serialize_provn(statements, node_id)
    return serialize_provn([], node_id)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _statement_id(node_id: str, relation: str, target_node_id: str) -> str:
    return f"{node_id}__{relation}__{target_node_id}"


def _parse_statement_id(statement_id: str) -> Tuple[str, str, str]:
    parts = statement_id.split("__")
    if len(parts) != 3:
        raise ValueError(f"Invalid statement_id: {statement_id}")
    return parts[0], parts[1], parts[2]


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------

async def create_statement(data: ProvStatement) -> ProvStatement:
    data = data.model_copy(
        update={"statement_id": data.statement_id or _statement_id(data.node_id, data.prov_relation.value, data.target_node_id)}
    )

    statements = _load_statements(data.node_id)
    if any(
        s.node_id == data.node_id
        and s.prov_relation == data.prov_relation
        and s.target_node_id == data.target_node_id
        for s in statements
    ):
        raise ValueError(
            f"PROV statement already exists: {data.node_id} {data.prov_relation.value} {data.target_node_id}"
        )

    statements.append(data)
    _save_statements(data.node_id, statements)
    return data


async def get_statement(statement_id: str) -> Optional[ProvStatement]:
    try:
        node_id, relation, target_node_id = _parse_statement_id(statement_id)
    except ValueError:
        return None

    statements = _load_statements(node_id)
    for s in statements:
        if s.statement_id == statement_id or (
            s.node_id == node_id
            and s.prov_relation.value == relation
            and s.target_node_id == target_node_id
        ):
            return s
    return None


async def update_statement(statement_id: str, data: dict) -> Optional[ProvStatement]:
    try:
        node_id, relation, target_node_id = _parse_statement_id(statement_id)
    except ValueError:
        return None

    allowed = {
        "node_role",
        "target_role",
        "is_inferred",
        "evidence",
        "confidence",
        "status",
        "notes",
    }
    fields = {k: v for k, v in data.items() if k in allowed}
    if not fields:
        return await get_statement(statement_id)

    statements = _load_statements(node_id)
    for idx, s in enumerate(statements):
        if s.statement_id == statement_id or (
            s.node_id == node_id
            and s.prov_relation.value == relation
            and s.target_node_id == target_node_id
        ):
            update_dict = s.model_dump()
            update_dict.update(fields)
            # Normalize enum/string values
            if "node_role" in update_dict and hasattr(update_dict["node_role"], "value"):
                update_dict["node_role"] = update_dict["node_role"].value
            if "target_role" in update_dict and hasattr(update_dict["target_role"], "value"):
                update_dict["target_role"] = update_dict["target_role"].value
            if "prov_relation" in update_dict and hasattr(update_dict["prov_relation"], "value"):
                update_dict["prov_relation"] = update_dict["prov_relation"].value
            if "confidence" in update_dict and hasattr(update_dict["confidence"], "value"):
                update_dict["confidence"] = update_dict["confidence"].value
            if "status" in update_dict and hasattr(update_dict["status"], "value"):
                update_dict["status"] = update_dict["status"].value
            updated = ProvStatement(**update_dict)
            statements[idx] = updated
            _save_statements(node_id, statements)
            return updated
    return None


async def delete_statement(statement_id: str) -> bool:
    try:
        node_id, relation, target_node_id = _parse_statement_id(statement_id)
    except ValueError:
        return False

    statements = _load_statements(node_id)
    new_statements = [
        s
        for s in statements
        if not (
            s.node_id == node_id
            and s.prov_relation.value == relation
            and s.target_node_id == target_node_id
        )
    ]
    if len(new_statements) == len(statements):
        return False
    _save_statements(node_id, new_statements)
    return True


# ---------------------------------------------------------------------------
# Listing
# ---------------------------------------------------------------------------

async def list_statements(
    skip: int = 0,
    limit: int = 100,
    node_id: Optional[str] = None,
    target_node_id: Optional[str] = None,
    prov_relation: Optional[str] = None,
    status: Optional[str] = None,
) -> Tuple[List[ProvStatement], int]:
    _ensure_dir()

    files: List[Path] = []
    if node_id:
        files = [_node_file(node_id)]
    else:
        files = sorted(PROV_DIR.glob("*.provn"))

    all_statements: List[ProvStatement] = []
    for path in files:
        if not path.exists():
            continue
        # Derive node_id from file name
        nid = path.stem.replace(".prov", "")
        all_statements.extend(_load_statements(nid))

    if target_node_id:
        all_statements = [s for s in all_statements if s.target_node_id == target_node_id]
    if prov_relation:
        all_statements = [s for s in all_statements if s.prov_relation.value == prov_relation]
    if status:
        all_statements = [s for s in all_statements if s.status.value == status]

    total = len(all_statements)
    items = all_statements[skip : skip + limit]
    return items, total


async def list_statements_by_node(
    node_id: str,
    skip: int = 0,
    limit: int = 100,
) -> Tuple[List[ProvStatement], int]:
    statements = _load_statements(node_id)
    total = len(statements)
    return statements[skip : skip + limit], total
