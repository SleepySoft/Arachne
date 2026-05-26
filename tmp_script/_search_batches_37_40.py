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
    "电机", "继电器", "推土机", "铁路车辆", "反渗透膜", "轮胎钢丝", "钢帘线",
    "啤酒", "麦芽", "淀粉", "燃料乙醇", "味精", "柠檬酸", "氧化铝", "铝产品",
    "粘胶", "化纤", "无纺布", "核黄素", "客车", "载重汽车", "锡", "钽",
    "煤层气", "磁材", "番茄制品", "风机", "非晶"
]
for kw in keywords:
    items = search_nodes(kw)
    print(f"=== {kw} ===")
    for it in items[:5]:
        print(f"  {it['node_id']}: {it['canonical_name_zh']} ({it['entity_type']})")
    if not items:
        print("  (none)")
