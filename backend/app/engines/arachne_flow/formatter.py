"""Format arachne-flow YAML documents for readability."""

from __future__ import annotations

from typing import Any

import yaml

from app.engines.arachne_flow.parser import FlowParseError


def format_flow_yaml(content: str) -> str:
    """Re-serialize a flow YAML document with edges in compact triple form.

    The output keeps all top-level keys in block style, but each edge is written
    as a single-line ``[source, predicate, target]`` triple.
    """
    try:
        raw = yaml.safe_load(content)
    except Exception as exc:
        raise FlowParseError(f"invalid YAML: {exc}") from exc

    if raw is None:
        raw = {}
    if not isinstance(raw, dict):
        raise FlowParseError("flow document must be a mapping")

    edges = raw.get("edges", [])
    doc = {k: v for k, v in raw.items() if k != "edges"}

    text = yaml.safe_dump(
        doc,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
    )

    lines = [text.rstrip("\n"), "edges:"]
    for edge in edges:
        if isinstance(edge, (list, tuple)) and len(edge) == 3:
            lines.append(f"- [{', '.join(str(x) for x in edge)}]")
        else:
            lines.append(f"- {edge}")
    return "\n".join(lines) + "\n"
