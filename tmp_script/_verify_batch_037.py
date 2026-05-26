import urllib.request, json

def api_get(path):
    url = f"http://localhost:8005{path}"
    try:
        resp = urllib.request.urlopen(url, timeout=10)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": e.code}

company_ids = ["jinling_pharm", "wodun_tech", "hisense_appliance", "jiadian_motor", "hegang_resources",
               "zhonghe_tech", "fuxing_share", "china_railway_materials", "sinosteel_intl", "st_lanhuang"]

for cid in company_ids:
    c = api_get(f"/api/v1/companies/{cid}")
    if "error" in c:
        print(f"{cid}: MISSING")
    else:
        exps = api_get(f"/api/v1/companies/{cid}/exposures")
        print(f"{cid}: OK, exposures={exps.get('total',0)}")
