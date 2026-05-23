import requests

BASE = "http://localhost:8000/api/v1"

print("=== Industry Subgraphs ===")
for ind_id in ['banking', 'real_estate', 'landscaping']:
    r = requests.get(f"{BASE}/industries/{ind_id}/subgraph")
    if r.status_code == 200:
        data = r.json()
        print(f"{ind_id}: nodes={len(data['nodes'])} edges={len(data['edges'])}")
    else:
        print(f"{ind_id}: ERROR {r.status_code}")

print("\n=== Company Subgraphs ===")
for cid in ['pingan_bank', 'vanke', 'csgholding']:
    r = requests.get(f"{BASE}/companies/{cid}/subgraph")
    if r.status_code == 200:
        data = r.json()
        print(f"{cid}: nodes={len(data['nodes'])} edges={len(data['edges'])}")
    else:
        print(f"{cid}: ERROR {r.status_code}")

print("\n=== Reverse Lookup ===")
r = requests.get(f"{BASE}/companies/by-node/loan_service")
if r.status_code == 200:
    data = r.json()
    print(f"Companies by loan_service: {len(data['items'])}")
    for c in data['items'][:3]:
        print(f"  {c['company_id']}")
else:
    print(f"Reverse lookup ERROR {r.status_code}")

print("\n=== All Companies List ===")
r = requests.get(f"{BASE}/companies")
if r.status_code == 200:
    data = r.json()
    print(f"Total companies: {data['total']}")
    for c in data['items']:
        print(f"  {c['company_id']} | {c['name_zh']}")
