"""Export temporary reasoning graphs to JSON files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


REASONING_EXPORT_DIR = Path(__file__).resolve().parents[3] / "data" / "reasoning"


def export_temp_graph(reasoning_id: str, temp_graph: Dict[str, Any]) -> Path:
    """Serialize a temporary graph to a JSON file and return its path."""
    REASONING_EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REASONING_EXPORT_DIR / f"temp_graph_{reasoning_id}.json"
    path.write_text(
        json.dumps(temp_graph, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path
