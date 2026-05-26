import urllib.request, json, urllib.parse

def list_edges(from_node=None, to_node=None):
    params = []
    if from_node:
        params.append(f"from_node={from_node}")
    if to_node:
        params.append(f"to_node={to_node}")
    q = "&".join(params)
    url = f'http://localhost:8005/api/v1/edges?page=1&page_size=50'
    if q:
        url += "&" + q
    try:
        resp = urllib.request.urlopen(url, timeout=10)
        data = json.loads(resp.read().decode())
        return data.get("items", [])
    except Exception as e:
        return []

# Check some likely existing edges
pairs = [
    ("iron_ore", "steel_plate"),
    ("live_pig", "meat_product"),
    ("coal", "coal_power_generation"),
    ("potassium_chloride", "chemical_fertilizer"),
    ("compound_fertilizer", "chemical_fertilizer"),
]

for f, t in pairs:
    items = list_edges(from_node=f, to_node=t)
    print(f"{f} -> {t}: {len(items)} edges")
    for e in items:
        print(f"  {e['edge_id']} ({e['edge_type']})")
