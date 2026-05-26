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

for kw in ["钾盐", "钾盐矿", "磷矿石", "磷矿", "航天应用", "车联网", "商业地产"]:
    items = search_nodes(kw)
    print(f"=== {kw} ===")
    for it in items[:5]:
        print(f"  {it['node_id']}: {it['canonical_name_zh']} ({it['entity_type']})")
    if not items:
        print("  (none)")
