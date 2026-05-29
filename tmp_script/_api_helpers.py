import httpx
import json

BASE_URL = "http://localhost:8005/api/v1"

def get_stats():
    r = httpx.get(f"{BASE_URL}/query/stats", timeout=10)
    return r.json()

def list_nodes(search=None, page_size=1000):
    params = {"page": 1, "page_size": page_size}
    if search:
        params["search"] = search
    r = httpx.get(f"{BASE_URL}/nodes", params=params, timeout=10)
    return r.json()

def get_node(node_id):
    r = httpx.get(f"{BASE_URL}/nodes/{node_id}", timeout=10)
    if r.status_code == 404:
        return None
    return r.json()

def list_companies(search=None, page_size=1000):
    params = {"page": 1, "page_size": page_size}
    if search:
        params["search"] = search
    r = httpx.get(f"{BASE_URL}/companies", params=params, timeout=10)
    return r.json()

def get_company(company_id):
    r = httpx.get(f"{BASE_URL}/companies/{company_id}", timeout=10)
    if r.status_code == 404:
        return None
    return r.json()

def submit_business_batch(data):
    r = httpx.post(f"{BASE_URL}/business-batches", json=data, timeout=60)
    return r.json()

def query_neighbors(node_id):
    r = httpx.get(f"{BASE_URL}/query/neighbors/{node_id}", timeout=10)
    return r.json()

def query_subgraph(node_id, depth=2):
    r = httpx.get(f"{BASE_URL}/query/subgraph/{node_id}", params={"depth": depth}, timeout=10)
    return r.json()

if __name__ == '__main__':
    import sys
    cmd = sys.argv[1]
    if cmd == 'stats':
        print(json.dumps(get_stats(), ensure_ascii=False, indent=2))
    elif cmd == 'nodes':
        search = sys.argv[2] if len(sys.argv) > 2 else None
        print(json.dumps(list_nodes(search), ensure_ascii=False, indent=2))
    elif cmd == 'companies':
        search = sys.argv[2] if len(sys.argv) > 2 else None
        print(json.dumps(list_companies(search), ensure_ascii=False, indent=2))
    elif cmd == 'company':
        print(json.dumps(get_company(sys.argv[2]), ensure_ascii=False, indent=2))
    elif cmd == 'node':
        print(json.dumps(get_node(sys.argv[2]), ensure_ascii=False, indent=2))
