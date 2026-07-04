"""
File-based storage layer for PROV statements.

PROV assertions are persisted as human-editable PROV-N documents under
`data/prov_statements/{node_id}.provn`. The file content is the source of truth
and is preserved exactly as written. Statement-level APIs read from and append
to these documents, but they never rewrite a document from scratch, so manual
edits (extra declarations, attributes, comments, formatting) are kept intact.

The only expected link to the industrial graph is that `entity(...)` identifiers
should reuse existing `node_id`s when possible; the parser does not enforce this
and will happily load PROV-N documents that reference entities not yet in the
graph.
"""

from __future__ import annotations

import json
import os
import re
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple

from app.models.prov_schema import ProvStatement, ProvRole, ProvRelation
from app.services.prov_n import parse_provn, serialize_provn, PROV_PREFIX


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


def _default_document(node_id: str) -> str:
    """Return an empty PROV-N document for a node."""
    return serialize_provn([], node_id)


def get_provn_text(node_id: str) -> Optional[str]:
    """Return the raw PROV-N text for a node."""
    path = _node_file(node_id)
    if path.exists():
        try:
            return path.read_text(encoding="utf-8")
        except OSError:
            return None
    legacy_path = _legacy_node_file(node_id)
    if legacy_path.exists():
        # One-time migration: convert legacy JSON to PROV-N and remove JSON.
        try:
            with legacy_path.open("r", encoding="utf-8") as f:
                raw = json.load(f)
            statements: List[ProvStatement] = []
            if isinstance(raw, list):
                for item in raw:
                    try:
                        statements.append(ProvStatement(**item))
                    except Exception:
                        continue
            text = serialize_provn(statements, node_id)
            _save_text(node_id, text)
            legacy_path.unlink()
            return text
        except (json.JSONDecodeError, OSError):
            pass
    return _default_document(node_id)


def set_provn_text(node_id: str, text: str) -> None:
    """Validate and save raw PROV-N text for a node."""
    # Validate by parsing.
    parse_provn(text)
    _save_text(node_id, text)


def _save_text(node_id: str, text: str) -> None:
    path = _node_file(node_id)
    legacy_path = _legacy_node_file(node_id)

    if not text.strip():
        if path.exists():
            path.unlink()
        if legacy_path.exists():
            legacy_path.unlink()
        return

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

    if legacy_path.exists():
        try:
            legacy_path.unlink()
        except OSError:
            pass


def _load_statements(node_id: str) -> List[ProvStatement]:
    text = get_provn_text(node_id)
    if text is None:
        return []
    _, statements = parse_provn(text)
    return statements


def _all_node_ids() -> List[str]:
    _ensure_dir()
    return sorted(p.stem.replace(".prov", "") for p in PROV_DIR.glob("*.provn"))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _relation_signature(relation: ProvRelation) -> Tuple[ProvRole, ProvRole]:
    from app.services.prov_n import RELATION_SIGNATURES
    return RELATION_SIGNATURES[relation.value][1], RELATION_SIGNATURES[relation.value][2]


def _ensure_declaration(text: str, node_id: str, role: ProvRole) -> str:
    """Add a declaration line if not already present."""
    pattern = re.compile(rf"^\s*{role.value}\s*\(\s*{PROV_PREFIX}:{re.escape(node_id)}\s*\)", re.MULTILINE)
    if pattern.search(text):
        return text
    decl = f"  {role.value}(ex:{node_id})"
    if "endDocument" in text:
        return text.replace("endDocument", f"{decl}\n\nendDocument", 1)
    return text.rstrip() + "\n" + decl + "\n"


def _find_statement_file(statement_id: str) -> Optional[str]:
    """Scan all PROV-N files for a statement with the given ID/UUID."""
    for nid in _all_node_ids():
        for s in _load_statements(nid):
            if s.statement_id == statement_id or str(s.statement_uuid) == statement_id:
                return nid
    return None


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------

async def create_statement(data: ProvStatement) -> ProvStatement:
    data = data.model_copy(update={"statement_id": data.statement_id or str(data.statement_uuid)})

    text = get_provn_text(data.node_id) or _default_document(data.node_id)
    _, existing = parse_provn(text)
    if any(
        s.node_id == data.node_id
        and s.prov_relation == data.prov_relation
        and s.target_node_id == data.target_node_id
        for s in existing
    ):
        raise ValueError(
            f"PROV statement already exists: {data.node_id} {data.prov_relation.value} {data.target_node_id}"
        )

    text = _ensure_declaration(text, data.node_id, data.node_role)
    text = _ensure_declaration(text, data.target_node_id, data.target_role)

    rel_name = data.prov_relation.value
    rel_line = f"  {rel_name}(ex:{data.node_id}, ex:{data.target_node_id})"
    if "endDocument" in text:
        text = text.replace("endDocument", f"{rel_line}\n\nendDocument", 1)
    else:
        text = text.rstrip() + "\n" + rel_line + "\n"
    _save_text(data.node_id, text)
    return data


async def get_statement(statement_id: str) -> Optional[ProvStatement]:
    nid = _find_statement_file(statement_id)
    if nid is None:
        return None
    for s in _load_statements(nid):
        if s.statement_id == statement_id or str(s.statement_uuid) == statement_id:
            return s
    return None


async def update_statement(statement_id: str, data: dict) -> Optional[ProvStatement]:
    """Metadata-only update. PROV-N files do not currently store evidence/confidence."""
    return await get_statement(statement_id)


async def delete_statement(statement_id: str) -> bool:
    nid = _find_statement_file(statement_id)
    if nid is None:
        return False

    target: Optional[ProvStatement] = None
    for s in _load_statements(nid):
        if s.statement_id == statement_id or str(s.statement_uuid) == statement_id:
            target = s
            break
    if target is None:
        return False

    text = get_provn_text(nid)
    if text is None:
        return False

    rel_name = target.prov_relation.value
    escaped_rel = re.escape(rel_name)
    escaped_node = re.escape(target.node_id)
    escaped_target = re.escape(target.target_node_id)
    pattern = re.compile(
        rf"^\s*{escaped_rel}\s*\(\s*{PROV_PREFIX}:{escaped_node}\s*,\s*{PROV_PREFIX}:{escaped_target}\s*\)\s*;?\s*$",
        re.MULTILINE,
    )
    new_text = pattern.sub("", text)
    if new_text == text:
        return False

    new_text = re.sub(r"\n{3,}", "\n\n", new_text)
    _save_text(nid, new_text)
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
