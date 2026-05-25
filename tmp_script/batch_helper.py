#!/usr/bin/env python3
"""Helper script for batch submission to Arachne API."""
import json
import requests
from typing import List, Dict, Any, Optional

BASE_URL = "http://localhost:8000/api/v1"


def get_all_nodes() -> List[Dict]:
    """Fetch all nodes from Neo4j."""
    nodes = []
    page = 1
    while True:
        r = requests.get(f"{BASE_URL}/nodes", params={"page": page, "page_size": 1000})
        data = r.json()
        items = data.get("items", [])
        if not items:
            break
        nodes.extend(items)
        if len(items) < 1000:
            break
        page += 1
    return nodes


def get_all_edges() -> List[Dict]:
    """Fetch all edges from Neo4j."""
    edges = []
    page = 1
    while True:
        r = requests.get(f"{BASE_URL}/edges", params={"page": page, "page_size": 1000})
        data = r.json()
        items = data.get("items", [])
        if not items:
            break
        edges.extend(items)
        if len(items) < 1000:
            break
        page += 1
    return edges


def node_exists(node_id: str, nodes: List[Dict]) -> bool:
    return any(n["node_id"] == node_id for n in nodes)


def edge_exists(edge_id: str, edges: List[Dict]) -> bool:
    return any(e["edge_id"] == edge_id for e in edges)


def submit_graph_batch(batch: Dict) -> Dict:
    r = requests.post(f"{BASE_URL}/batches", json=batch)
    return {"status": r.status_code, **r.json()}


def submit_business_batch(batch: Dict) -> Dict:
    r = requests.post(f"{BASE_URL}/business-batches", json=batch)
    return {"status": r.status_code, **r.json()}


def get_existing_node_ids() -> set:
    nodes = get_all_nodes()
    return {n["node_id"] for n in nodes}


def get_existing_edge_ids() -> set:
    edges = get_all_edges()
    return {e["edge_id"] for e in edges}


if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "nodes":
        print(json.dumps(get_all_nodes(), ensure_ascii=False, indent=2))
    elif cmd == "edges":
        print(json.dumps(get_all_edges(), ensure_ascii=False, indent=2))
    elif cmd == "stats":
        r = requests.get(f"{BASE_URL}/query/stats")
        print(json.dumps(r.json(), ensure_ascii=False, indent=2))
    else:
        print("Usage: python batch_helper.py [nodes|edges|stats]")
