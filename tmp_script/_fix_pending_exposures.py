"""
One-time fix: activate all PENDING company exposures and recompute company view.
"""
import requests

BASE = "http://localhost:8000/api/v1"

# Step 1: Check how many PENDING exposures exist
r = requests.get(f"{BASE}/companies?page=1&page_size=1000", timeout=60)
companies = r.json()["items"]
print(f"Total companies: {len(companies)}")

pending_count = 0
for c in companies:
    cid = c["company_id"]
    ex = requests.get(f"{BASE}/companies/{cid}/exposures?page=1&page_size=1000", timeout=60)
    data = ex.json()
    for e in data.get("items", []):
        if e.get("status") == "PENDING":
            pending_count += 1

print(f"PENDING exposures found: {pending_count}")

# Step 2: Activate all PENDING exposures via direct DB update
# We'll use the backend's internal logic by calling update on each exposure
for c in companies:
    cid = c["company_id"]
    ex = requests.get(f"{BASE}/companies/{cid}/exposures?page=1&page_size=1000", timeout=60)
    data = ex.json()
    for e in data.get("items", []):
        if e.get("status") == "PENDING":
            eid = e["exposure_id"]
            upd = requests.put(
                f"{BASE}/companies/{cid}/exposures/{eid}",
                json={"status": "ACTIVE"},
                timeout=30,
            )
            if upd.status_code not in (200, 204):
                print(f"  Failed to activate {eid}: {upd.status_code}")

print("Activation done.")

# Step 3: Trigger company view recomputation
r = requests.post(f"{BASE}/company-view/compute", timeout=30)
print(f"Compute triggered: {r.status_code}")
print(r.json())
