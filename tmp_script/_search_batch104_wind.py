import httpx

BASE_URL = "http://localhost:8005/api/v1"

searches = ["风电", "风力发电", "风能", "电梯", "扶梯", "环卫", "矿用装备"]

with open('tmp_script/_batch104_wind.txt', 'w', encoding='utf-8') as f:
    for kw in searches:
        r = httpx.get(f"{BASE_URL}/nodes", params={"search": kw, "page": 1, "page_size": 20}, timeout=10)
        data = r.json()
        items = data.get("items", [])
        f.write(f"\n=== '{kw}' ({len(items)} results) ===\n")
        for item in items[:10]:
            f.write(f"  {item['node_id']} | {item['canonical_name_zh']} | {item['entity_type']}\n")

print("Done")
