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

keywords = ["煤", "磷", "钾盐", "房地产", "住宅", "商品房", "车联网", "物联网", "航天", "卫星"]
for kw in keywords:
    items = search_nodes(kw)
    print(f"=== {kw} ===")
    for it in items[:10]:
        print(f"  {it['node_id']}: {it['canonical_name_zh']} ({it['entity_type']})")
    if len(items) > 10:
        print(f"  ... and {len(items)-10} more")
    if not items:
        print("  (none)")
