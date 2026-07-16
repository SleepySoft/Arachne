"""
Compatibility shim: re-export legacy engine storage functions.

The original implementation has moved to app.engines.legacy.storage.
This module is kept for backward compatibility with existing imports.
"""

from __future__ import annotations

# Re-export all public functions from legacy storage
from app.engines.legacy.storage import (  # noqa: F401
    _evidence_from_db,
    _evidence_to_db,
    _to_datetime,
    create_industrial_flow_edge,
    create_node,
    create_ontology_edge,
    delete_edge,
    delete_node,
    get_async_driver,
    get_edge,
    get_neighbors,
    get_node,
    get_paths,
    get_stats,
    get_subgraph,
    list_edges,
    list_nodes,
    update_edge,
    update_node,
)
