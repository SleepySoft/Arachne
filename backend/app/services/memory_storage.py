"""In-memory graph storage fallback for development without Neo4j."""

from datetime import datetime
from typing import List, Optional

from app.engines.legacy.schemas import (
    GraphEdge,
    GraphStats,
    IndustrialFlowEdge,
    IndustrialNode,
    OntologyEdge,
)

# In-memory stores
_nodes: dict[str, IndustrialNode] = {}
_edges: dict[str, GraphEdge] = {}


def _evidence_to_db(evidence_list):
    return [
        {
            "source_title": e.source_title,
            "source_url": str(e.source_url) if e.source_url else None,
            "quote": e.quote,
        }
        for e in evidence_list
    ]


def _evidence_from_db(raw: list):
    from app.models.core import Evidence
    out = []
    for item in raw or []:
        if not item:
            continue
        url = item.get("source_url")
        out.append(
            Evidence(
                source_title=item.get("source_title", ""),
                source_url=url if url else None,
                quote=item.get("quote", ""),
            )
        )
    return out


def _node_to_dict(node: IndustrialNode) -> dict:
    return {
        "node_uuid": str(node.node_uuid),
        "node_id": node.node_id,
        "canonical_name_zh": node.canonical_name_zh,
        "canonical_name_en": node.canonical_name_en,
        "aliases": list(node.aliases),
        "definition": node.definition,
        "entity_type": node.entity_type.value if hasattr(node.entity_type, "value") else node.entity_type,
        "evidence": _evidence_to_db(node.evidence),
        "confidence": node.confidence.value if hasattr(node.confidence, "value") else node.confidence,
        "status": node.status.value if hasattr(node.status, "value") else node.status,
        "notes": node.notes,
        "created_at": node.created_at or datetime.utcnow(),
        "updated_at": node.updated_at or datetime.utcnow(),
    }


def _dict_to_node(data: dict) -> IndustrialNode:
    return IndustrialNode(
        node_uuid=data.get("node_uuid"),
        node_id=data["node_id"],
        canonical_name_zh=data["canonical_name_zh"],
        canonical_name_en=data.get("canonical_name_en"),
        aliases=list(data.get("aliases", [])),
        definition=data["definition"],
        entity_type=data["entity_type"],
        evidence=_evidence_from_db(data.get("evidence", [])),
        confidence=data["confidence"],
        status=data["status"],
        notes=data.get("notes"),
        created_at=data.get("created_at"),
        updated_at=data.get("updated_at"),
    )


def _edge_to_dict(edge: GraphEdge) -> dict:
    base = {
        "edge_uuid": str(edge.edge_uuid),
        "edge_id": edge.edge_id,
        "from_node": edge.from_node,
        "to_node": edge.to_node,
        "description": edge.description,
        "evidence": _evidence_to_db(edge.evidence),
        "confidence": edge.confidence.value if hasattr(edge.confidence, "value") else edge.confidence,
        "notes": edge.notes,
        "edge_namespace": edge.edge_namespace,
        "edge_type": edge.edge_type.value if hasattr(edge.edge_type, "value") else edge.edge_type,
        "created_at": edge.created_at or datetime.utcnow(),
        "updated_at": edge.updated_at or datetime.utcnow(),
    }
    return base


def _dict_to_edge(data: dict) -> GraphEdge:
    ns = data["edge_namespace"]
    common = {
        "edge_uuid": data.get("edge_uuid"),
        "edge_id": data["edge_id"],
        "from_node": data["from_node"],
        "to_node": data["to_node"],
        "description": data["description"],
        "evidence": _evidence_from_db(data.get("evidence", [])),
        "confidence": data["confidence"],
        "notes": data.get("notes"),
        "created_at": data.get("created_at"),
        "updated_at": data.get("updated_at"),
    }
    if ns == "industrial_flow":
        return IndustrialFlowEdge(
            edge_namespace="industrial_flow",
            edge_type=data["edge_type"],
            **common,
        )
    else:
        return OntologyEdge(
            edge_namespace="ontology",
            edge_type=data["edge_type"],
            **common,
        )


# ---------------------------------------------------------------------------
# Node Storage
# ---------------------------------------------------------------------------

async def create_node(node: IndustrialNode) -> IndustrialNode:
    _nodes[node.node_id] = _node_to_dict(node)
    return _dict_to_node(_nodes[node.node_id])


async def get_node(node_id: str) -> Optional[IndustrialNode]:
    data = _nodes.get(node_id)
    if data is None:
        return None
    return _dict_to_node(data)


async def update_node(node_id: str, data: dict) -> Optional[IndustrialNode]:
    existing = _nodes.get(node_id)
    if not existing:
        return None
    now = datetime.utcnow()
    for key, value in data.items():
        if value is not None:
            if key == "evidence":
                existing[key] = _evidence_to_db(value)
            elif key in ("confidence", "status", "entity_type"):
                existing[key] = value.value if hasattr(value, "value") else value
            else:
                existing[key] = value
    existing["updated_at"] = now
    return _dict_to_node(existing)


async def delete_node(node_id: str) -> bool:
    if node_id not in _nodes:
        return False
    del _nodes[node_id]
    # cascade delete edges
    global _edges
    _edges = {
        eid: edata
        for eid, edata in _edges.items()
        if edata["from_node"] != node_id and edata["to_node"] != node_id
    }
    return True


async def list_nodes(
    skip: int = 0,
    limit: int = 20,
    entity_type: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
) -> tuple[List[IndustrialNode], int]:
    items = []
    for data in _nodes.values():
        if entity_type and data.get("entity_type") != entity_type:
            continue
        if status and data.get("status") != status:
            continue
        if search:
            s = search.lower()
            name_zh = (data.get("canonical_name_zh") or "").lower()
            nid = (data.get("node_id") or "").lower()
            aliases = [a.lower() for a in data.get("aliases", [])]
            if s not in name_zh and s not in nid and not any(s in a for a in aliases):
                continue
        items.append(_dict_to_node(data))
    items.sort(key=lambda n: n.canonical_name_zh)
    total = len(items)
    return items[skip : skip + limit], total


# ---------------------------------------------------------------------------
# Edge Storage
# ---------------------------------------------------------------------------

async def create_industrial_flow_edge(edge: IndustrialFlowEdge) -> IndustrialFlowEdge:
    _edges[edge.edge_id] = _edge_to_dict(edge)
    return _dict_to_edge(_edges[edge.edge_id])


async def create_ontology_edge(edge: OntologyEdge) -> OntologyEdge:
    _edges[edge.edge_id] = _edge_to_dict(edge)
    return _dict_to_edge(_edges[edge.edge_id])


async def get_edge(edge_id: str) -> Optional[GraphEdge]:
    data = _edges.get(edge_id)
    if data is None:
        return None
    return _dict_to_edge(data)


async def update_edge(edge_id: str, data: dict, namespace: str) -> Optional[GraphEdge]:
    existing = _edges.get(edge_id)
    if not existing:
        return None
    now = datetime.utcnow()
    for key, value in data.items():
        if value is not None:
            if key == "evidence":
                existing[key] = _evidence_to_db(value)
            elif key in ("confidence",):
                existing[key] = value.value if hasattr(value, "value") else value
            else:
                existing[key] = value
    existing["updated_at"] = now
    return _dict_to_edge(existing)


async def delete_edge(edge_id: str, namespace: str) -> bool:
    if edge_id not in _edges:
        return False
    del _edges[edge_id]
    return True


async def list_edges(
    skip: int = 0,
    limit: int = 20,
    edge_namespace: Optional[str] = None,
    edge_type: Optional[str] = None,
    from_node: Optional[str] = None,
    to_node: Optional[str] = None,
) -> tuple[List[GraphEdge], int]:
    items = []
    for data in _edges.values():
        if edge_namespace and data.get("edge_namespace") != edge_namespace:
            continue
        if edge_type and data.get("edge_type") != edge_type:
            continue
        if from_node and data.get("from_node") != from_node:
            continue
        if to_node and data.get("to_node") != to_node:
            continue
        items.append(_dict_to_edge(data))
    items.sort(key=lambda e: e.edge_id)
    total = len(items)
    return items[skip : skip + limit], total


# ---------------------------------------------------------------------------
# Query Storage
# ---------------------------------------------------------------------------

async def get_subgraph(node_id: str, depth: int = 2) -> tuple[List[IndustrialNode], List[GraphEdge]]:
    visited_nodes = set()
    visited_edges = set()
    result_nodes = []
    result_edges = []

    def _bfs(current: str, d: int):
        if d <= 0 or current in visited_nodes:
            return
        visited_nodes.add(current)
        node_data = _nodes.get(current)
        if node_data:
            result_nodes.append(_dict_to_node(node_data))
        for eid, edata in _edges.items():
            if eid in visited_edges:
                continue
            if edata["from_node"] == current or edata["to_node"] == current:
                visited_edges.add(eid)
                result_edges.append(_dict_to_edge(edata))
                other = edata["to_node"] if edata["from_node"] == current else edata["from_node"]
                _bfs(other, d - 1)

    _bfs(node_id, depth)
    return result_nodes, result_edges


async def get_neighbors(node_id: str) -> tuple[List[IndustrialNode], List[GraphEdge]]:
    nodes = []
    edges = []
    neighbor_ids = set()
    for eid, edata in _edges.items():
        if edata["from_node"] == node_id or edata["to_node"] == node_id:
            edges.append(_dict_to_edge(edata))
            other = edata["to_node"] if edata["from_node"] == node_id else edata["from_node"]
            neighbor_ids.add(other)
    for nid in neighbor_ids:
        data = _nodes.get(nid)
        if data:
            nodes.append(_dict_to_node(data))
    return nodes, edges


async def get_paths(from_node: str, to_node: str, max_depth: int = 5) -> List[List[dict]]:
    # Simple DFS for paths
    paths = []

    def _dfs(current: str, target: str, path: list, visited: set, depth: int):
        if depth > max_depth:
            return
        if current == target and len(path) > 0:
            paths.append(path.copy())
            return
        for eid, edata in _edges.items():
            if edata["from_node"] == current and edata["to_node"] not in visited:
                visited.add(edata["to_node"])
                step = [{"type": "node", "node_id": current}]
                if len(path) == 0 or path[-1] != step[0]:
                    path.extend(step)
                path.append({
                    "type": "edge",
                    "edge_id": edata["edge_id"],
                    "edge_namespace": edata["edge_namespace"],
                    "edge_type": edata["edge_type"],
                    "from_node": edata["from_node"],
                    "to_node": edata["to_node"],
                })
                path.append({"type": "node", "node_id": edata["to_node"]})
                _dfs(edata["to_node"], target, path, visited, depth + 1)
                # backtrack
                path.pop()
                path.pop()
                if len(path) > 0 and path[-1]["type"] == "node" and path[-1]["node_id"] == current:
                    path.pop()
                visited.discard(edata["to_node"])

    _dfs(from_node, to_node, [], {from_node}, 0)
    return paths[:10]


async def get_stats() -> GraphStats:
    node_type_dist = {}
    status_dist = {}
    confidence_dist = {}
    for data in _nodes.values():
        et = data.get("entity_type", "unknown")
        node_type_dist[et] = node_type_dist.get(et, 0) + 1
        st = data.get("status", "PENDING")
        status_dist[st] = status_dist.get(st, 0) + 1
        cf = data.get("confidence", "LOW")
        confidence_dist[cf] = confidence_dist.get(cf, 0) + 1

    edge_ns_dist = {"industrial_flow": 0, "ontology": 0}
    edge_type_dist = {}
    for data in _edges.values():
        ns = data.get("edge_namespace", "industrial_flow")
        edge_ns_dist[ns] = edge_ns_dist.get(ns, 0) + 1
        et = data.get("edge_type", "")
        edge_type_dist[et] = edge_type_dist.get(et, 0) + 1

    return GraphStats(
        total_nodes=len(_nodes),
        total_edges=len(_edges),
        node_type_distribution=node_type_dist,
        edge_namespace_distribution=edge_ns_dist,
        edge_type_distribution=edge_type_dist,
        status_distribution=status_dist,
        confidence_distribution=confidence_dist,
    )
