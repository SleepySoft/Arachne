import requests, json
r = requests.get('http://localhost:8000/api/v1/companies?page=1&page_size=2', timeout=30)
companies = r.json()['items']
for c in companies:
    cid = c['company_id']
    ex = requests.get(f'http://localhost:8000/api/v1/companies/{cid}/exposures', timeout=30)
    data = ex.json()
    print(f"{cid}: type={type(data).__name__}")
    if isinstance(data, list):
        print(f"  count={len(data)}")
        for e in data:
            print(f"    {e.get('node_id')} -> {e.get('status')}")
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2)[:500])
