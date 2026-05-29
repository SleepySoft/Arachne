import httpx
import json

BASE_URL = "http://localhost:8005/api/v1"

companies = [
    "sh_600764", "sh_600765", "sh_600768", "sh_600769", "sh_600770",
    "sh_600771", "sh_600773", "sh_600774", "sh_600775", "sh_600776"
]

with open('tmp_script/_exposures_check.txt', 'w', encoding='utf-8') as f:
    for cid in companies:
        r = httpx.get(f"{BASE_URL}/companies/{cid}/exposures", params={"page": 1, "page_size": 100}, timeout=10)
        data = r.json()
        items = data.get("items", [])
        f.write(f"\n=== {cid}: {len(items)} exposures ===\n")
        for item in items:
            f.write(f"  {item['exposure_id']} -> {item['node_id']} ({item['activity_type']})\n")

print("Done")
