import httpx

BASE_URL = "http://localhost:8005/api/v1"

searches = [
    "纺织", "市场租赁", "房地产", "焦炭", "煤气", "蒸汽", "造纸", "新闻纸", "包装纸",
    "仓储", "化工", "电力", "农药", "杀虫剂", "软件", "网络设备", "海运", "船舶运输",
    "包装印刷", "证券印刷"
]

with open('tmp_script/_batch102_nodes.txt', 'w', encoding='utf-8') as f:
    for kw in searches:
        r = httpx.get(f"{BASE_URL}/nodes", params={"search": kw, "page": 1, "page_size": 20}, timeout=10)
        data = r.json()
        items = data.get("items", [])
        f.write(f"\n=== '{kw}' ({len(items)} results) ===\n")
        for item in items[:10]:
            f.write(f"  {item['node_id']} | {item['canonical_name_zh']} | {item['entity_type']}\n")

print("Done")
