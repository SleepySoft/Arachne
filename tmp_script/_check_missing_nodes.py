import requests
BASE = 'http://localhost:8000/api/v1'

candidates = [
    'flat_glass', 'sugar_cane', 'oilfield_service', 'public_transportation', 'ship',
    'kitchen_appliance', 'passenger_car', 'stainless_steel', 'tap_water_supply',
    'natural_gas', 'gasoline', 'diesel'
]

missing = []
for n in candidates:
    r = requests.get(f'{BASE}/nodes/{n}')
    if r.status_code != 200:
        missing.append(n)
        print(f"MISSING: {n}")
    else:
        data = r.json()
        print(f"EXISTS: {n} | {data.get('canonical_name_zh', 'N/A')}")

print(f"\nTotal missing: {len(missing)}")
