#!/usr/bin/env python3
"""Arachne CLI Tool - Submit and Query JSON batches"""

import argparse
import json
import sys
from pathlib import Path

import httpx

BASE_URL = "http://localhost:8000/api/v1"


def submit_batch(json_path: str):
    """Submit a GraphRegistrationBatch JSON file to the system."""
    path = Path(json_path)
    if not path.exists():
        print(f"Error: File not found: {json_path}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(path.read_text(encoding="utf-8"))
    url = f"{BASE_URL}/batches"

    try:
        resp = httpx.post(url, json=data, timeout=60.0)
        resp.raise_for_status()
        result = resp.json()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if result.get("errors"):
            print(f"\n⚠️  {len(result['errors'])} errors occurred", file=sys.stderr)
            sys.exit(1)
        print("\n[OK] Batch submitted successfully")
    except httpx.HTTPStatusError as e:
        print(f"HTTP Error {e.response.status_code}: {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def query_subgraph(node_id: str, depth: int = 2):
    """Query subgraph centered on a node."""
    url = f"{BASE_URL}/query/subgraph/{node_id}"
    try:
        resp = httpx.get(url, params={"depth": depth}, timeout=30.0)
        resp.raise_for_status()
        print(json.dumps(resp.json(), ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def query_neighbors(node_id: str):
    """Query neighbors of a node."""
    url = f"{BASE_URL}/query/neighbors/{node_id}"
    try:
        resp = httpx.get(url, timeout=30.0)
        resp.raise_for_status()
        print(json.dumps(resp.json(), ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def query_stats():
    """Query graph statistics."""
    url = f"{BASE_URL}/query/stats"
    try:
        resp = httpx.get(url, timeout=30.0)
        resp.raise_for_status()
        print(json.dumps(resp.json(), ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def list_nodes(search: str = None, page: int = 1, page_size: int = 20):
    """List nodes with optional search."""
    url = f"{BASE_URL}/nodes"
    params = {"page": page, "page_size": page_size}
    if search:
        params["search"] = search
    try:
        resp = httpx.get(url, params=params, timeout=30.0)
        resp.raise_for_status()
        print(json.dumps(resp.json(), ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Arachne CLI - Submit and Query")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # submit
    p_submit = subparsers.add_parser("submit", help="Submit a JSON batch file")
    p_submit.add_argument("json_file", help="Path to GraphRegistrationBatch JSON file")

    # query
    p_query = subparsers.add_parser("query", help="Query the graph")
    p_query.add_argument("--subgraph", metavar="NODE_ID", help="Get subgraph centered on node")
    p_query.add_argument("--depth", type=int, default=2, help="Subgraph depth (default: 2)")
    p_query.add_argument("--neighbors", metavar="NODE_ID", help="Get neighbors of node")
    p_query.add_argument("--stats", action="store_true", help="Get graph statistics")
    p_query.add_argument("--list-nodes", action="store_true", help="List all nodes")
    p_query.add_argument("--search", help="Search nodes by name/alias")

    args = parser.parse_args()

    if args.command == "submit":
        submit_batch(args.json_file)
    elif args.command == "query":
        if args.subgraph:
            query_subgraph(args.subgraph, args.depth)
        elif args.neighbors:
            query_neighbors(args.neighbors)
        elif args.stats:
            query_stats()
        elif args.list_nodes or args.search:
            list_nodes(search=args.search)
        else:
            p_query.print_help()
            sys.exit(1)


if __name__ == "__main__":
    main()
