import httpx, json

BASE = 'http://localhost:8005/api/v1'

# Stats
r = httpx.get(f'{BASE}/query/stats', timeout=30)
stats = r.json()
print('=== Graph Stats ===')
print(json.dumps(stats, ensure_ascii=False, indent=2))

# Company count
r = httpx.get(f'{BASE}/companies?page=1&page_size=1', timeout=30)
companies = r.json()
total_companies = companies.get('total', '?')
print(f'\n=== Total Companies: {total_companies} ===')

# Exposure count
r = httpx.get(f'{BASE}/companies?page=1&page_size=100', timeout=30)
all_companies = r.json().get('items', [])
total_exposures = 0
for c in all_companies:
    cid = c['company_id']
    rr = httpx.get(f'{BASE}/companies/{cid}/exposures', timeout=30)
    exps = rr.json()
    total_exposures += len(exps)
print(f'=== Total Exposures: {total_exposures} ===')
