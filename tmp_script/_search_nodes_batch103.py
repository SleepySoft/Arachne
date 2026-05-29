import httpx

BASE_URL = "http://localhost:8005/api/v1"

searches = [
    "水泥", "熟料", "液化天然气", "LNG", "甲醇", "煤炭", "公路", "拖拉机", "生物制药",
    "钢铁", "板材", "长材", "轮轴", "白酒", "帘子布", "工业丝", "尼龙", "维生素",
    "青霉素", "头孢", "百货", "广告"
]

with open('tmp_script/_batch103_nodes.txt', 'w', encoding='utf-8') as f:
    for kw in searches:
        r = httpx.get(f"{BASE_URL}/nodes", params={"search": kw, "page": 1, "page_size": 20}, timeout=10)
        data = r.json()
        items = data.get("items", [])
        f.write(f"\n=== '{kw}' ({len(items)} results) ===\n")
        for item in items[:10]:
            f.write(f"  {item['node_id']} | {item['canonical_name_zh']} | {item['entity_type']}\n")

print("Done")
