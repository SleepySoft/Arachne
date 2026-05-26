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

keywords = [
    "钾", "肥", "肉", "猪", "电", "钢", "铁", "路", "桥", "柴油",
    "摩托", "水泥", "糖", "啤酒", "港", "物流", "药", "家电", "电机"
]

all_nodes = []
for kw in keywords:
    items = search_nodes(kw)
    for it in items:
        nid = it["node_id"]
        if nid not in [n["node_id"] for n in all_nodes]:
            all_nodes.append(it)

print(f"Found {len(all_nodes)} unique nodes matching keywords")
for n in all_nodes:
    print(f"  {n['node_id']}: {n['canonical_name_zh']} ({n['entity_type']})")
