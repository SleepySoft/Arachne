import httpx
import json

BASE_URL = "http://localhost:8005/api/v1"

# Batch 100 companies to check
companies = [
    ("sh_600764", "中国海防"),
    ("sh_600765", "XD中航重机"),
    ("sh_600768", "宁波富邦"),
    ("sh_600769", "祥龙电业"),
    ("sh_600770", "综艺股份"),
    ("sh_600771", "广誉远"),
    ("sh_600773", "西藏城投"),
    ("sh_600774", "汉商集团"),
    ("sh_600775", "南京熊猫"),
    ("sh_600776", "东方通信"),
]

# Key nodes to search for
node_keywords = [
    "水声", "声纳", "液压", "锻件", "铸件", "换热器", "铝板", "铝型材", "发电", "供电", "供热", "供水", "污水",
    "太阳能", "电池", "集成电路", "软件", "中药", "中成药", "房地产开发", "零售", "百货", "会展",
    "移动通信", "卫星通信", "通信设备", "传输设备", "IC卡"
]

with open('tmp_script/_check_existing_result.txt', 'w', encoding='utf-8') as f:
    f.write("=== Checking Existing Companies ===\n")
    for cid, name in companies:
        r = httpx.get(f"{BASE_URL}/companies/{cid}", timeout=10)
        if r.status_code == 200:
            f.write(f"EXISTS: {cid} ({name})\n")
        else:
            f.write(f"NOT FOUND: {cid} ({name})\n")
    
    f.write("\n=== Checking Existing Nodes ===\n")
    for kw in node_keywords:
        r = httpx.get(f"{BASE_URL}/nodes", params={"search": kw, "page": 1, "page_size": 20}, timeout=10)
        data = r.json()
        items = data.get("items", [])
        f.write(f"\nSearch '{kw}': {len(items)} results\n")
        for item in items[:5]:
            f.write(f"  {item['node_id']} | {item['canonical_name_zh']} | {item['entity_type']}\n")

print("Results written to tmp_script/_check_existing_result.txt")
