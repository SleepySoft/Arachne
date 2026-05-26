import urllib.request, json, urllib.parse

def api_get(path):
    req = urllib.request.Request(f'http://localhost:8005{path}')
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": e.code, "msg": e.read().decode()[:200]}
    except Exception as e:
        return {"error": str(e)}

# Check if companies from batch 034/035 exist
codes = [
    "000893", "000895", "001896", "000897", "000898",
    "000899", "000900", "000901", "000902", "000903"
]

for code in codes:
    # Search company by stock code in name
    q = urllib.parse.quote(code)
    result = api_get(f"/api/v1/companies?page=1&page_size=20&search={q}")
    items = result.get("items", [])
    if items:
        print(f"{code}: FOUND {len(items)} companies")
        for c in items:
            print(f"  - {c['company_id']}: {c['name_zh']} ({c.get('stock_code','')})")
    else:
        print(f"{code}: NOT FOUND")
