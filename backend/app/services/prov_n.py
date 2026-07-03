"""
PROV-N parser and serializer.

Supports a subset of the W3C PROV-N notation sufficient for Arachne's
type-level provenance assertions. Each node's statements are stored as a
self-contained PROV-N document under `data/prov_statements/{node_id}.provn`.

Supported grammar subset:

    document
      prefix ex <http://arachne.graph/>

      entity(ex:node_id)
      activity(ex:node_id)
      agent(ex:node_id)

      used(ex:activity, ex:entity)
      wasGeneratedBy(ex:entity, ex:activity)
      wasDerivedFrom(ex:entity, ex:entity)
      wasAttributedTo(ex:entity, ex:agent)
      wasAssociatedWith(ex:activity, ex:agent)
      actedOnBehalfOf(ex:agent, ex:agent)

    endDocument

Attributes, bundles and extra positional arguments are intentionally ignored
for now to keep the storage format simple and human-editable.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Tuple

from app.models.prov_schema import ProvRole, ProvRelation, ProvStatement


PROV_NAMESPACE = "http://arachne.graph/"
PROV_PREFIX = "ex"

QUALIFIED_NAME_RE = re.compile(r"^([a-zA-Z_][a-zA-Z0-9_]*):([a-zA-Z_][a-zA-Z0-9_]*)$")


@dataclass
class ProvDeclaration:
    """A PROV element declaration: entity/activity/agent."""

    role: ProvRole
    node_id: str


RELATION_SIGNATURES = {
    "used": (ProvRelation.USED, ProvRole.ACTIVITY, ProvRole.ENTITY),
    "wasGeneratedBy": (ProvRelation.WAS_GENERATED_BY, ProvRole.ENTITY, ProvRole.ACTIVITY),
    "wasDerivedFrom": (ProvRelation.WAS_DERIVED_FROM, ProvRole.ENTITY, ProvRole.ENTITY),
    "wasAttributedTo": (ProvRelation.WAS_ATTRIBUTED_TO, ProvRole.ENTITY, ProvRole.AGENT),
    "wasAssociatedWith": (ProvRelation.WAS_ASSOCIATED_WITH, ProvRole.ACTIVITY, ProvRole.AGENT),
    "actedOnBehalfOf": (ProvRelation.ACTED_ON_BEHALF_OF, ProvRole.AGENT, ProvRole.AGENT),
}


def _strip_attributes(args_str: str) -> str:
    """Remove an optional PROV attribute list `[...]` from the tail of args."""
    # Find the first unquoted '[' that is not inside a qualified name.
    depth = 0
    in_string = False
    for i, ch in enumerate(args_str):
        if ch == '"' and (i == 0 or args_str[i - 1] != "\\"):
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "[":
            if depth == 0:
                return args_str[:i].rstrip(", ")
            depth += 1
        elif ch == "]":
            depth -= 1
    return args_str


def _split_args(args_str: str) -> List[str]:
    """Split comma-separated args, ignoring commas inside strings."""
    parts: List[str] = []
    current: List[str] = []
    in_string = False
    for ch in args_str:
        if ch == '"' and (not current or current[-1] != "\\"):
            in_string = not in_string
            current.append(ch)
        elif ch == "," and not in_string:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
    if current:
        parts.append("".join(current).strip())
    return [p for p in parts if p]


def _parse_qname(qname: str, prefixes: dict[str, str]) -> str:
    """Convert a PROV qualified name to a local node_id."""
    qname = qname.strip()
    if not qname:
        raise ValueError("empty qualified name")
    # Literal string (not expected for identifiers, but tolerated)
    if qname.startswith('"') and qname.endswith('"'):
        return qname[1:-1]
    match = QUALIFIED_NAME_RE.match(qname)
    if match:
        prefix, local = match.groups()
        # Accept the configured prefix; unknown prefixes keep their full qname.
        if prefix == PROV_PREFIX:
            return local
        return f"{prefix}:{local}"
    # Bare identifier: assume it belongs to the default namespace.
    return qname


def parse_provn(text: str) -> Tuple[List[ProvDeclaration], List[ProvStatement]]:
    """Parse a PROV-N document and return declarations and relation statements."""
    declarations: List[ProvDeclaration] = []
    statements: List[ProvStatement] = []
    prefixes: dict[str, str] = {}

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("//"):
            continue
        if line in ("document", "endDocument"):
            continue

        if line.startswith("prefix "):
            match = re.match(r'prefix\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+<([^>]+)>', line)
            if match:
                prefixes[match.group(1)] = match.group(2)
            continue

        if line.startswith("default "):
            continue

        match = re.match(r"(\w+)\s*\((.*)\)\s*;?\s*$", line)
        if not match:
            continue

        name = match.group(1)
        args_str = _strip_attributes(match.group(2))
        args = _split_args(args_str)

        if name in ("entity", "activity", "agent"):
            if not args:
                continue
            try:
                role = ProvRole(name)
                node_id = _parse_qname(args[0], prefixes)
                declarations.append(ProvDeclaration(role=role, node_id=node_id))
            except Exception:
                continue
            continue

        if name not in RELATION_SIGNATURES:
            continue
        if len(args) < 2:
            continue

        rel, node_role, target_role = RELATION_SIGNATURES[name]
        try:
            node_id = _parse_qname(args[0], prefixes)
            target_node_id = _parse_qname(args[1], prefixes)
        except Exception:
            continue

        statements.append(
            ProvStatement(
                node_id=node_id,
                node_role=node_role,
                prov_relation=rel,
                target_node_id=target_node_id,
                target_role=target_role,
            )
        )

    return declarations, statements


def serialize_provn(
    statements: List[ProvStatement],
    node_id: str,
    declarations: List[ProvDeclaration] | None = None,
) -> str:
    """Serialize a list of ProvStatement objects to a PROV-N document."""
    # Build declaration map from explicit declarations and relation signatures.
    decl_map: dict[str, ProvRole] = {}
    if declarations:
        for d in declarations:
            decl_map[d.node_id] = d.role

    for s in statements:
        decl_map.setdefault(s.node_id, s.node_role)
        decl_map.setdefault(s.target_node_id, s.target_role)

    # If the node has no statements and no declaration, default to entity.
    if not decl_map and node_id:
        decl_map[node_id] = ProvRole.ENTITY

    lines: List[str] = [
        "document",
        f"  prefix {PROV_PREFIX} <{PROV_NAMESPACE}>",
        "",
    ]

    for nid, role in sorted(decl_map.items()):
        lines.append(f"  {role.value}(ex:{nid})")

    if statements:
        lines.append("")
        for s in statements:
            rel_name = s.prov_relation.value
            lines.append(f"  {rel_name}(ex:{s.node_id}, ex:{s.target_node_id})")

    lines.append("")
    lines.append("endDocument")
    return "\n".join(lines)
