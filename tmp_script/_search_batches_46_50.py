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
    "黄酒", "客车", "漆包线", "光学", "船舶", "午餐肉", "聚氯乙烯", "木结构",
    "磷化工", "麻醉", "葡萄酒", "安宫牛黄", "变压器", "远洋捕捞", "光缆",
    "造纸", "乘用车", "稀土", "铜箔", "特钢", "小卫星"
]
for kw in keywords:
    items = search_nodes(kw)
    print(f"=== {kw} ===")
    for it in items[:6]:
        print(f"  {it['node_id']}: {it['canonical_name_zh']} ({it['entity_type']})")
    if not items:
        print("  (none)")
