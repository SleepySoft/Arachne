#!/usr/bin/env python3
"""Arachne CLI Tool - Full API Client for Graph, Industry, and Company management."""

import argparse
import json
import sys
from pathlib import Path

import httpx

BASE_URL = "http://localhost:8005/api/v1"


# ========================================================================
# Helpers
# ========================================================================

def _load_json(path_str: str) -> dict:
    path = Path(path_str)
    if not path.exists():
        print(f"Error: File not found: {path_str}", file=sys.stderr)
        sys.exit(1)
    return json.loads(path.read_text(encoding="utf-8"))


def _request(method: str, path: str, **kwargs) -> dict:
    url = f"{BASE_URL}{path}"
    try:
        resp = httpx.request(method, url, timeout=60.0, **kwargs)
        resp.raise_for_status()
        return resp.json() if resp.content else {}
    except httpx.HTTPStatusError as e:
        print(f"HTTP Error {e.response.status_code}: {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def _print(data: dict | list):
    print(json.dumps(data, ensure_ascii=False, indent=2))


# ========================================================================
# Batch Commands
# ========================================================================

def cmd_submit_graph_batch(json_path: str):
    data = _load_json(json_path)
    result = _request("POST", "/batches", json=data)
    _print(result)
    if result.get("errors"):
        print(f"\n⚠️  {len(result['errors'])} errors occurred", file=sys.stderr)
        sys.exit(1)
    print("\n[OK] Graph batch submitted successfully")


def cmd_submit_business_batch(json_path: str):
    data = _load_json(json_path)
    result = _request("POST", "/business-batches", json=data)
    _print(result)
    if result.get("errors"):
        print(f"\n⚠️  {len(result['errors'])} errors occurred", file=sys.stderr)
        sys.exit(1)
    print("\n[OK] Business batch submitted successfully")


# ========================================================================
# Industry Commands
# ========================================================================

def cmd_industry_list(search: str = None, industry_type: str = None, status: str = None,
                      page: int = 1, page_size: int = 20):
    params = {"page": page, "page_size": page_size}
    if search:
        params["search"] = search
    if industry_type:
        params["industry_type"] = industry_type
    if status:
        params["status"] = status
    result = _request("GET", "/industries", params=params)
    _print(result)


def cmd_industry_get(industry_id: str):
    result = _request("GET", f"/industries/{industry_id}")
    _print(result)


def cmd_industry_create(json_path: str):
    data = _load_json(json_path)
    result = _request("POST", "/industries", json=data)
    _print(result)
    print("\n[OK] Industry created")


def cmd_industry_update(industry_id: str, json_path: str):
    data = _load_json(json_path)
    result = _request("PUT", f"/industries/{industry_id}", json=data)
    _print(result)
    print("\n[OK] Industry updated")


def cmd_industry_delete(industry_id: str):
    _request("DELETE", f"/industries/{industry_id}")
    print(f"[OK] Industry '{industry_id}' deleted")


def cmd_industry_subgraph(industry_id: str):
    result = _request("GET", f"/industries/{industry_id}/subgraph")
    _print(result)


def cmd_industry_mappings(industry_id: str, page: int = 1, page_size: int = 20):
    params = {"page": page, "page_size": page_size}
    result = _request("GET", f"/industries/{industry_id}/mappings", params=params)
    _print(result)


def cmd_industry_add_mapping(industry_id: str, json_path: str):
    data = _load_json(json_path)
    result = _request("POST", f"/industries/{industry_id}/mappings", json=data)
    _print(result)
    print("\n[OK] Mapping created")


def cmd_industry_update_mapping(industry_id: str, mapping_id: str, json_path: str):
    data = _load_json(json_path)
    result = _request("PUT", f"/industries/{industry_id}/mappings/{mapping_id}", json=data)
    _print(result)
    print("\n[OK] Mapping updated")


def cmd_industry_del_mapping(industry_id: str, mapping_id: str):
    _request("DELETE", f"/industries/{industry_id}/mappings/{mapping_id}")
    print(f"[OK] Mapping '{mapping_id}' deleted")


# ========================================================================
# Company Commands
# ========================================================================

def cmd_company_list(search: str = None, company_type: str = None, status: str = None,
                     country: str = None, page: int = 1, page_size: int = 20):
    params = {"page": page, "page_size": page_size}
    if search:
        params["search"] = search
    if company_type:
        params["company_type"] = company_type
    if status:
        params["status"] = status
    if country:
        params["country"] = country
    result = _request("GET", "/companies", params=params)
    _print(result)


def cmd_company_get(company_id: str):
    result = _request("GET", f"/companies/{company_id}")
    _print(result)


def cmd_company_create(json_path: str):
    data = _load_json(json_path)
    result = _request("POST", "/companies", json=data)
    _print(result)
    print("\n[OK] Company created")


def cmd_company_update(company_id: str, json_path: str):
    data = _load_json(json_path)
    result = _request("PUT", f"/companies/{company_id}", json=data)
    _print(result)
    print("\n[OK] Company updated")


def cmd_company_delete(company_id: str):
    _request("DELETE", f"/companies/{company_id}")
    print(f"[OK] Company '{company_id}' deleted")


def cmd_company_subgraph(company_id: str):
    result = _request("GET", f"/companies/{company_id}/subgraph")
    _print(result)


def cmd_company_exposures(company_id: str, page: int = 1, page_size: int = 20):
    params = {"page": page, "page_size": page_size}
    result = _request("GET", f"/companies/{company_id}/exposures", params=params)
    _print(result)


def cmd_company_add_exposure(company_id: str, json_path: str):
    data = _load_json(json_path)
    result = _request("POST", f"/companies/{company_id}/exposures", json=data)
    _print(result)
    print("\n[OK] Exposure created")


def cmd_company_del_exposure(company_id: str, exposure_id: str):
    _request("DELETE", f"/companies/{company_id}/exposures/{exposure_id}")
    print(f"[OK] Exposure '{exposure_id}' deleted")


# ========================================================================
# Query Commands
# ========================================================================

def cmd_query_subgraph(node_id: str, depth: int = 2):
    result = _request("GET", f"/query/subgraph/{node_id}", params={"depth": depth})
    _print(result)


def cmd_query_neighbors(node_id: str):
    result = _request("GET", f"/query/neighbors/{node_id}")
    _print(result)


def cmd_query_stats():
    result = _request("GET", "/query/stats")
    _print(result)


def cmd_query_list_nodes(search: str = None, page: int = 1, page_size: int = 20, draft_only: bool = False):
    params = {"page": page, "page_size": page_size}
    if search:
        params["search"] = search
    if draft_only:
        params["draft_only"] = True
    result = _request("GET", "/nodes", params=params)
    _print(result)


def cmd_query_fuzzy_search(query: str, limit: int = 10):
    result = _request("GET", "/nodes/fuzzy-search", params={"query": query, "limit": limit})
    _print(result)


def cmd_query_incomplete_items(limit: int = 100):
    result = _request("GET", "/query/incomplete-items", params={"limit": limit})
    _print(result)


def cmd_quick_node(name_zh: str = None, name_en: str = None, entity_type: str = "unknown", notes: str = None):
    data = {
        "canonical_name_zh": name_zh,
        "canonical_name_en": name_en,
        "entity_type": entity_type,
        "notes": notes,
    }
    result = _request("POST", "/nodes/quick-create", json=data)
    _print(result)
    print("\n[OK] Draft node created")


def cmd_quick_edge(from_node: str, to_node: str, edge_type: str = "material_flow", description: str = None, notes: str = None):
    data = {
        "from_node": from_node,
        "to_node": to_node,
        "edge_type": edge_type,
        "description": description,
        "notes": notes,
    }
    result = _request("POST", "/edges/quick-create", json=data)
    _print(result)
    print("\n[OK] Draft edge created")


# ========================================================================
# CLI Parser
# ========================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Arachne CLI - Graph, Industry & Company Management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s submit batch.json
  %(prog)s business-batch business_batch.json
  %(prog)s industry list --search 机器人
  %(prog)s industry get intelligent_driving
  %(prog)s industry create --json industry.json
  %(prog)s industry subgraph intelligent_driving
  %(prog)s company list --type public --country CN
  %(prog)s company get hesai_technology
  %(prog)s company create --json company.json
  %(prog)s query --stats
  %(prog)s query --search 激光雷达
  %(prog)s query --fuzzy-search "激光雷达" --limit 5
  %(prog)s query --incomplete-items --limit 50
  %(prog)s quick-node --name-zh "六氟化铀" --entity-type material
  %(prog)s quick-edge --from lithium_metal --to battery_cell --edge-type material_flow
        """
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # submit
    p_submit = subparsers.add_parser("submit", help="Submit a GraphRegistrationBatch JSON file")
    p_submit.add_argument("json_file", help="Path to JSON file")

    # business-batch
    p_bbatch = subparsers.add_parser("business-batch", help="Submit a BusinessRegistrationBatch JSON file")
    p_bbatch.add_argument("json_file", help="Path to JSON file")

    # industry
    p_ind = subparsers.add_parser("industry", help="Manage industries")
    ind_sub = p_ind.add_subparsers(dest="subcommand", required=True)

    p_ind_list = ind_sub.add_parser("list", help="List industries")
    p_ind_list.add_argument("--search", help="Search by name/id")
    p_ind_list.add_argument("--type", dest="industry_type", choices=["formal_industry", "curated_view", "theme_view"], help="Filter by type")
    p_ind_list.add_argument("--status", choices=["ACTIVE", "PENDING", "REJECTED", "ARCHIVED"], help="Filter by status")
    p_ind_list.add_argument("--page", type=int, default=1, help="Page number (default: 1)")
    p_ind_list.add_argument("--page-size", type=int, default=20, help="Page size (default: 20)")

    p_ind_get = ind_sub.add_parser("get", help="Get industry details")
    p_ind_get.add_argument("industry_id", help="Industry ID")

    p_ind_create = ind_sub.add_parser("create", help="Create industry from JSON")
    p_ind_create.add_argument("--json", required=True, dest="json_file", help="Path to JSON file")

    p_ind_update = ind_sub.add_parser("update", help="Update industry from JSON")
    p_ind_update.add_argument("industry_id", help="Industry ID")
    p_ind_update.add_argument("--json", required=True, dest="json_file", help="Path to JSON file")

    p_ind_delete = ind_sub.add_parser("delete", help="Delete industry")
    p_ind_delete.add_argument("industry_id", help="Industry ID")

    p_ind_subgraph = ind_sub.add_parser("subgraph", help="Get industry subgraph")
    p_ind_subgraph.add_argument("industry_id", help="Industry ID")

    p_ind_mappings = ind_sub.add_parser("mappings", help="List industry node mappings")
    p_ind_mappings.add_argument("industry_id", help="Industry ID")
    p_ind_mappings.add_argument("--page", type=int, default=1)
    p_ind_mappings.add_argument("--page-size", type=int, default=20)

    p_ind_add_map = ind_sub.add_parser("add-mapping", help="Add node mapping to industry")
    p_ind_add_map.add_argument("industry_id", help="Industry ID")
    p_ind_add_map.add_argument("--json", required=True, dest="json_file", help="Path to JSON file")

    p_ind_update_map = ind_sub.add_parser("update-mapping", help="Update node mapping in industry")
    p_ind_update_map.add_argument("industry_id", help="Industry ID")
    p_ind_update_map.add_argument("mapping_id", help="Mapping ID")
    p_ind_update_map.add_argument("--json", required=True, dest="json_file", help="Path to JSON file")

    p_ind_del_map = ind_sub.add_parser("del-mapping", help="Delete node mapping from industry")
    p_ind_del_map.add_argument("industry_id", help="Industry ID")
    p_ind_del_map.add_argument("mapping_id", help="Mapping ID")

    # company
    p_co = subparsers.add_parser("company", help="Manage companies")
    co_sub = p_co.add_subparsers(dest="subcommand", required=True)

    p_co_list = co_sub.add_parser("list", help="List companies")
    p_co_list.add_argument("--search", help="Search by name/id")
    p_co_list.add_argument("--type", dest="company_type", choices=["public", "private", "state_owned", "startup", "unknown"], help="Filter by type")
    p_co_list.add_argument("--status", choices=["ACTIVE", "PENDING", "REJECTED", "ARCHIVED"], help="Filter by status")
    p_co_list.add_argument("--country", help="Filter by country")
    p_co_list.add_argument("--page", type=int, default=1)
    p_co_list.add_argument("--page-size", type=int, default=20)

    p_co_get = co_sub.add_parser("get", help="Get company details")
    p_co_get.add_argument("company_id", help="Company ID")

    p_co_create = co_sub.add_parser("create", help="Create company from JSON")
    p_co_create.add_argument("--json", required=True, dest="json_file", help="Path to JSON file")

    p_co_update = co_sub.add_parser("update", help="Update company from JSON")
    p_co_update.add_argument("company_id", help="Company ID")
    p_co_update.add_argument("--json", required=True, dest="json_file", help="Path to JSON file")

    p_co_delete = co_sub.add_parser("delete", help="Delete company")
    p_co_delete.add_argument("company_id", help="Company ID")

    p_co_subgraph = co_sub.add_parser("subgraph", help="Get company temporary subgraph")
    p_co_subgraph.add_argument("company_id", help="Company ID")

    p_co_exposures = co_sub.add_parser("exposures", help="List company node exposures")
    p_co_exposures.add_argument("company_id", help="Company ID")
    p_co_exposures.add_argument("--page", type=int, default=1)
    p_co_exposures.add_argument("--page-size", type=int, default=20)

    p_co_add_exp = co_sub.add_parser("add-exposure", help="Add node exposure to company")
    p_co_add_exp.add_argument("company_id", help="Company ID")
    p_co_add_exp.add_argument("--json", required=True, dest="json_file", help="Path to JSON file")

    p_co_del_exp = co_sub.add_parser("del-exposure", help="Delete node exposure from company")
    p_co_del_exp.add_argument("company_id", help="Company ID")
    p_co_del_exp.add_argument("exposure_id", help="Exposure ID")

    # query
    p_query = subparsers.add_parser("query", help="Query the graph")
    p_query.add_argument("--subgraph", metavar="NODE_ID", help="Get subgraph centered on node")
    p_query.add_argument("--depth", type=int, default=2, help="Subgraph depth (default: 2)")
    p_query.add_argument("--neighbors", metavar="NODE_ID", help="Get neighbors of node")
    p_query.add_argument("--stats", action="store_true", help="Get graph statistics")
    p_query.add_argument("--list-nodes", action="store_true", help="List all nodes")
    p_query.add_argument("--search", help="Search nodes by name/alias")
    p_query.add_argument("--fuzzy-search", metavar="QUERY", help="Fuzzy search similar node names")
    p_query.add_argument("--incomplete-items", action="store_true", help="List all incomplete/draft nodes and edges")
    p_query.add_argument("--limit", type=int, default=10, help="Limit for fuzzy/incomplete search (default: 10)")
    p_query.add_argument("--draft-only", action="store_true", help="List only draft/incomplete nodes")

    # quick-node
    p_quick = subparsers.add_parser("quick-node", help="Quickly create a draft node with minimal fields")
    p_quick.add_argument("--name-zh", help="Chinese name")
    p_quick.add_argument("--name-en", help="English name")
    p_quick.add_argument("--entity-type", default="unknown", choices=[
        "material", "component", "device", "module", "subsystem", "system",
        "platform", "infrastructure", "application_system", "service", "technology_capability", "unknown"
    ], help="Entity type (default: unknown)")
    p_quick.add_argument("--notes", help="Notes, e.g. '待 AI 补全'")

    # quick-edge
    p_qedge = subparsers.add_parser("quick-edge", help="Quickly create a draft industrial flow edge with minimal fields")
    p_qedge.add_argument("--from", required=True, dest="from_node", help="Source node ID")
    p_qedge.add_argument("--to", required=True, dest="to_node", help="Target node ID")
    p_qedge.add_argument("--edge-type", default="material_flow", choices=[
        "material_flow", "composition", "energy_flow", "information_flow", "capability_supply", "service_flow"
    ], help="Edge type (default: material_flow)")
    p_qedge.add_argument("--description", help="Optional description; auto-generated if omitted")
    p_qedge.add_argument("--notes", help="Notes, e.g. '待 AI 补全'")

    args = parser.parse_args()

    if args.command == "submit":
        cmd_submit_graph_batch(args.json_file)
    elif args.command == "business-batch":
        cmd_submit_business_batch(args.json_file)
    elif args.command == "industry":
        if args.subcommand == "list":
            cmd_industry_list(args.search, args.industry_type, args.status, args.page, args.page_size)
        elif args.subcommand == "get":
            cmd_industry_get(args.industry_id)
        elif args.subcommand == "create":
            cmd_industry_create(args.json_file)
        elif args.subcommand == "update":
            cmd_industry_update(args.industry_id, args.json_file)
        elif args.subcommand == "delete":
            cmd_industry_delete(args.industry_id)
        elif args.subcommand == "subgraph":
            cmd_industry_subgraph(args.industry_id)
        elif args.subcommand == "mappings":
            cmd_industry_mappings(args.industry_id, args.page, args.page_size)
        elif args.subcommand == "add-mapping":
            cmd_industry_add_mapping(args.industry_id, args.json_file)
        elif args.subcommand == "update-mapping":
            cmd_industry_update_mapping(args.industry_id, args.mapping_id, args.json_file)
        elif args.subcommand == "del-mapping":
            cmd_industry_del_mapping(args.industry_id, args.mapping_id)
    elif args.command == "company":
        if args.subcommand == "list":
            cmd_company_list(args.search, args.company_type, args.status, args.country, args.page, args.page_size)
        elif args.subcommand == "get":
            cmd_company_get(args.company_id)
        elif args.subcommand == "create":
            cmd_company_create(args.json_file)
        elif args.subcommand == "update":
            cmd_company_update(args.company_id, args.json_file)
        elif args.subcommand == "delete":
            cmd_company_delete(args.company_id)
        elif args.subcommand == "subgraph":
            cmd_company_subgraph(args.company_id)
        elif args.subcommand == "exposures":
            cmd_company_exposures(args.company_id, args.page, args.page_size)
        elif args.subcommand == "add-exposure":
            cmd_company_add_exposure(args.company_id, args.json_file)
        elif args.subcommand == "del-exposure":
            cmd_company_del_exposure(args.company_id, args.exposure_id)
    elif args.command == "query":
        if args.subgraph:
            cmd_query_subgraph(args.subgraph, args.depth)
        elif args.neighbors:
            cmd_query_neighbors(args.neighbors)
        elif args.stats:
            cmd_query_stats()
        elif args.fuzzy_search:
            cmd_query_fuzzy_search(args.fuzzy_search, args.limit)
        elif args.incomplete_items:
            cmd_query_incomplete_items(args.limit)
        elif args.list_nodes or args.search:
            cmd_query_list_nodes(args.search, draft_only=args.draft_only)
        elif args.draft_only:
            cmd_query_list_nodes(draft_only=True)
        else:
            p_query.print_help()
            sys.exit(1)
    elif args.command == "quick-node":
        cmd_quick_node(args.name_zh, args.name_en, args.entity_type, args.notes)
    elif args.command == "quick-edge":
        cmd_quick_edge(args.from_node, args.to_node, args.edge_type, args.description, args.notes)


if __name__ == "__main__":
    main()
