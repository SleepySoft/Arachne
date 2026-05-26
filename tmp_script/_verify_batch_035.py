import urllib.request, json, urllib.parse

def api_get(path):
    url = f"http://localhost:8005{path}"
    try:
        resp = urllib.request.urlopen(url, timeout=10)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": e.code}
    except Exception as e:
        return {"error": str(e)}

company_ids = [
    "asia_potash", "shuanghui_dev", "yuneng_holdings", "tianjin_jinbin",
    "angang_steel", "ganeng_power", "modern_investment", "aerospace_tech",
    "xinyangfeng", "st_yundong"
]

for cid in company_ids:
    c = api_get(f"/api/v1/companies/{cid}")
    if "error" in c:
        print(f"{cid}: MISSING (error {c['error']})")
    else:
        print(f"{cid}: OK - {c['name_zh']}")
        # check exposures
        exps = api_get(f"/api/v1/companies/{cid}/exposures")
        items = exps.get("items", [])
        print(f"  exposures: {len(items)}")
        for e in items:
            print(f"    - {e['node_id']} ({e['activity_type']}, w={e['weight']})")
