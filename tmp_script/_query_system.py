import json
import urllib.request

BASE = "http://localhost:8000/api/v1"

def get_json(path):
    try:
        with urllib.request.urlopen(f"{BASE}{path}", timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"Error fetching {path}: {e}")
        return None

# Query all nodes
print("=== NODES (first 500) ===")
nodes = get_json("/nodes?page=1&page_size=500")
if nodes:
    for item in nodes.get("items", []):
        print(f"  {item['node_id']} | {item['canonical_name_zh']} | {item['entity_type']}")
    print(f"Total nodes: {nodes.get('total', 0)}")

# Query all companies
print("\n=== COMPANIES (first 500) ===")
companies = get_json("/companies?page=1&page_size=500")
if companies:
    for item in companies.get("items", []):
        print(f"  {item['company_id']} | {item['name_zh']}")
    print(f"Total companies: {companies.get('total', 0)}")

# Query stats
print("\n=== STATS ===")
stats = get_json("/query/stats")
if stats:
    print(json.dumps(stats, ensure_ascii=False, indent=2))
