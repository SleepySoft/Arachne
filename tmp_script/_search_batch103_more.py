import httpx

BASE_URL = "http://localhost:8005/api/v1"

searches = [
    "能源技术", "能源工程", "生物农药", "兽药原料", "农业机械"
]

with open('tmp_script/_batch103_more.txt', 'w', encoding='utf-8') as f:
    for kw in searches:
        r = httpx.get(f"{BASE_URL}/nodes", params={"search": kw, "page": 1, "page_size": 20}, timeout=10)
        data = r.json()
        items = data.get("items", [])
        f.write(f"\n=== '{kw}' ({len(items)} results) ===\n")
        for item in items[:10]:
            f.write(f"  {item['node_id']} | {item['canonical_name_zh']} | {item['entity_type']}\n")

print("Done")
