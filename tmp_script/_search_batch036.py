import urllib.request, json, urllib.parse

def search_nodes(keyword):
    q = urllib.parse.quote(keyword)
    req = urllib.request.Request(f'http://localhost:8005/api/v1/nodes?page=1&page_size=50&search={q}')
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode())
        return data.get("items", [])
    except Exception as e:
        return []

for kw in ["木地板", "地板", "人造板", "摩托车", "摩托", "广告", "注射剂", "蔗渣", "纸浆", "尿素"]:
    items = search_nodes(kw)
    print(f"=== {kw} ===")
    for it in items[:8]:
        print(f"  {it['node_id']}: {it['canonical_name_zh']} ({it['entity_type']})")
    if not items:
        print("  (none)")
