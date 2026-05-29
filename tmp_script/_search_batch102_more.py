import httpx

BASE_URL = "http://localhost:8005/api/v1"

searches = [
    "商业地产", "市场", "租赁", "焦炉煤气", "煤气", "文化纸", "包装纸", "食品包装",
    "航运", "沿海运输", "智能卡", "卡类", "证券印刷", "防伪印刷", "印刷"
]

with open('tmp_script/_batch102_more.txt', 'w', encoding='utf-8') as f:
    for kw in searches:
        r = httpx.get(f"{BASE_URL}/nodes", params={"search": kw, "page": 1, "page_size": 20}, timeout=10)
        data = r.json()
        items = data.get("items", [])
        f.write(f"\n=== '{kw}' ({len(items)} results) ===\n")
        for item in items[:10]:
            f.write(f"  {item['node_id']} | {item['canonical_name_zh']} | {item['entity_type']}\n")

print("Done")
