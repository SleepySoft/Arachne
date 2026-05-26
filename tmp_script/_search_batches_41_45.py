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
    "服务器", "变速器", "混合动力", "电驱动", "焦煤", "石油树脂", "聚丙烯",
    "中成药", "白酒", "杂交水稻", "维生素", "稀土钢", "污水处理", "油轮",
    "汽油", "润滑油", "合成树脂", "挖掘机", "混凝土", "直升机", "X射线", "磁共振"
]
for kw in keywords:
    items = search_nodes(kw)
    print(f"=== {kw} ===")
    for it in items[:6]:
        print(f"  {it['node_id']}: {it['canonical_name_zh']} ({it['entity_type']})")
    if not items:
        print("  (none)")
