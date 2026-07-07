"""
File-based storage layer for PROV statements.

PROV statements are persisted as plain JSON files under `data/prov_statements/`.
Each file is named `{node_id}.prov.json` and contains an array of PROV statements
whose `node_id` equals the file name. This makes the data transparent, diffable,
and easy for humans to inspect or edit directly.

Note on PROV-N:
    The project previously experimented with W3C PROV-N documents stored as
    `{node_id}.provn`. That dependency has been deprecated: the parser module
    `app.services.prov_n` is kept in the repository for reference and potential
    future export use, but the main storage layer no longer imports or uses it.
    The commented-out blocks below document the former PROV-N interface.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple

from app.models.prov_schema import ProvStatement, ProvRelation, ProvRole


# ---------------------------------------------------------------------------
# Storage layout
# ---------------------------------------------------------------------------

PROV_DIR = Path(__file__).resolve().parents[3] / "data" / "prov_statements"


def _ensure_dir() -> None:
    PROV_DIR.mkdir(parents=True, exist_ok=True)


def _node_file(node_id: str) -> Path:
    _ensure_dir()
    return PROV_DIR / f"{node_id}.prov.json"


def _load_statements(node_id: str) -> List[ProvStatement]:
    path = _node_file(node_id)
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(raw, list):
        return []
    statements: List[ProvStatement] = []
    for item in raw:
        try:
            statements.append(ProvStatement(**item))
        except Exception:
            # Skip malformed entries; could be logged in the future
            continue
    return statements


def _save_statements(node_id: str, statements: List[ProvStatement]) -> None:
    path = _node_file(node_id)
    if not statements:
        if path.exists():
            path.unlink()
        return

    payload = [s.model_dump(mode="json") for s in statements]
    # Atomic write: write to temp file in the same directory, then rename
    fd, tmp_path = tempfile.mkstemp(
        suffix=".tmp", prefix=f"{node_id}_", dir=str(PROV_DIR)
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.unlink(tmp_path)
        except FileNotFoundError:
            pass
        raise


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


def _normalize_statement(statement: ProvStatement) -> ProvStatement:
    """Ensure the statement carries a stable composite statement_id."""
    composite_id = _statement_id(
        statement.node_id,
        statement.prov_relation.value,
        statement.target_node_id,
    )
    if statement.statement_id != composite_id:
        return statement.model_copy(update={"statement_id": composite_id})
    return statement


# ---------------------------------------------------------------------------
# Deprecated PROV-N helpers (kept for reference; not used by hot path)
# ---------------------------------------------------------------------------

# The following functions used to read and write raw PROV-N text. They are
# preserved in comments so the PROV-N experiment remains documented and can
# be revived as an *export* format in the future.

# from app.services.prov_n import parse_provn, serialize_provn, PROV_PREFIX
#
# def _node_provn_file(node_id: str) -> Path:
#     _ensure_dir()
#     return PROV_DIR / f"{node_id}.provn"
#
# def get_provn_text(node_id: str) -> Optional[str]:
#     """Return the raw PROV-N text for a node."""
#     path = _node_provn_file(node_id)
#     if path.exists():
#         try:
#             return path.read_text(encoding="utf-8")
#         except OSError:
#             return None
#     return None
#
# def set_provn_text(node_id: str, text: str) -> None:
#     """Validate and save raw PROV-N text for a node."""
#     parse_provn(text)
#     path = _node_provn_file(node_id)
#     path.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------

async def create_statement(data: ProvStatement) -> ProvStatement:
    composite_id = _statement_id(
        data.node_id, data.prov_relation.value, data.target_node_id
    )
    data = data.model_copy(update={"statement_id": composite_id})

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

    statements.append(_normalize_statement(data))
    _save_statements(data.node_id, statements)
    return data


async def get_statement(statement_id: str) -> Optional[ProvStatement]:
    try:
        node_id, relation, target_node_id = _parse_statement_id(statement_id)
    except ValueError:
        return None

    statements = _load_statements(node_id)
    for s in statements:
        if (
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
        if (
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
            statements[idx] = _normalize_statement(updated)
            _save_statements(node_id, statements)
            return statements[idx]
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
        files = sorted(PROV_DIR.glob("*.prov.json"))

    all_statements: List[ProvStatement] = []
    for path in files:
        if not path.exists():
            continue
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
