import httpx

BASE_URL = "http://localhost:8005/api/v1"

searches = [
    "原油", "天然气", "石油", "零售", "百货", "酒店", "供暖", "旅游", "白酒", "酒",
    "电力", "火力发电", "煤炭", "钢板", "中厚板", "热轧", "冷轧", "线棒材", "钢绞线",
    "创业投资", "磨料", "磨具", "钢材", "医药", "纺织", "羊绒", "盐", "仓储", "物流",
    "供应链", "化学原料药", "抗生素", "兽药", "乳制品"
]

with open('tmp_script/_batch101_nodes.txt', 'w', encoding='utf-8') as f:
    for kw in searches:
        r = httpx.get(f"{BASE_URL}/nodes", params={"search": kw, "page": 1, "page_size": 20}, timeout=10)
        data = r.json()
        items = data.get("items", [])
        f.write(f"\n=== '{kw}' ({len(items)} results) ===\n")
        for item in items[:10]:
            f.write(f"  {item['node_id']} | {item['canonical_name_zh']} | {item['entity_type']}\n")

print("Done")
