import httpx

BASE_URL = "http://localhost:8005/api/v1"

searches = [
    "装载机", "挖掘机", "工程机械", "信托", "自行车", "康体设备", "浮法玻璃",
    "玻璃加工", "隧道", "市政工程", "汽车贸易", "有色金属", "出版", "图书",
    "电梯", "自动扶梯", "地铁", "公共交通", "有线电视", "广电网络",
    "医药批发", "医药零售", "典当", "保险", "超市", "外贸", "机电产品"
]

with open('tmp_script/_batch104_nodes.txt', 'w', encoding='utf-8') as f:
    for kw in searches:
        r = httpx.get(f"{BASE_URL}/nodes", params={"search": kw, "page": 1, "page_size": 20}, timeout=10)
        data = r.json()
        items = data.get("items", [])
        f.write(f"\n=== '{kw}' ({len(items)} results) ===\n")
        for item in items[:10]:
            f.write(f"  {item['node_id']} | {item['canonical_name_zh']} | {item['entity_type']}\n")

print("Done")
