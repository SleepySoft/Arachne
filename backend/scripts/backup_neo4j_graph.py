#!/usr/bin/env python3
"""备份 Neo4j 中的全部节点与边到 JSON 文件。"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from neo4j import GraphDatabase
from neo4j.time import DateTime as Neo4jDateTime

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def serialize_value(v):
    if isinstance(v, Neo4jDateTime):
        return v.isoformat()
    if isinstance(v, list):
        return [serialize_value(x) for x in v]
    if isinstance(v, dict):
        return {k: serialize_value(vv) for k, vv in v.items()}
    return v


def serialize_props(props):
    return {k: serialize_value(v) for k, v in props.items()}
BACKUP_DIR = PROJECT_ROOT / "data" / "backups"
NEO4J_URI = "bolt://localhost:7687"
NEO4J_AUTH = ("neo4j", "arachne123")


def main():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_path = BACKUP_DIR / f"neo4j_backup_{timestamp}.json"

    with GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH) as driver:
        with driver.session() as session:
            node_records = list(session.run("MATCH (n) RETURN n LIMIT 10000"))
            edge_records = list(session.run("MATCH ()-[r]->() RETURN r LIMIT 20000"))

    nodes = [rec["n"] for rec in node_records]
    rels = [rec["r"] for rec in edge_records]

    backup = {
        "meta": {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "neo4j_uri": NEO4J_URI,
            "node_count": len(nodes),
            "edge_count": len(rels),
        },
        "nodes": [
            {
                "labels": list(n.labels),
                "properties": serialize_props(n),
            }
            for n in nodes
        ],
        "edges": [
            {
                "type": r.type,
                "properties": serialize_props(r),
                "start_node": serialize_props(r.nodes[0]),
                "end_node": serialize_props(r.nodes[1]),
            }
            for r in rels
        ],
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(backup, f, ensure_ascii=False, indent=2)

    print(f"Backup written to: {out_path}")
    print(f"Nodes: {backup['meta']['node_count']}, Edges: {backup['meta']['edge_count']}")


if __name__ == "__main__":
    main()
