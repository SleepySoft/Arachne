import json
import httpx

BASE_URL = "http://localhost:8005/api/v1"

for n in range(100, 106):
    with open(f'data/stock_batches/batch_{n}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    exists_count = 0
    not_found = []
    for c in data:
        cid = f"sh_{c['symbol']}"
        r = httpx.get(f"{BASE_URL}/companies/{cid}", timeout=10)
        if r.status_code == 200:
            exists_count += 1
        else:
            not_found.append((cid, c['name']))
    
    print(f"Batch {n}: {exists_count}/{len(data)} exist. Missing: {[n for _, n in not_found]}")
