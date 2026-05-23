import asyncio, httpx

API_BASE = "http://localhost:8000/api/v1"

async def check():
    async with httpx.AsyncClient() as client:
        # Get all exposures for Shenzhen Energy with high limit
        resp = await client.get(f"{API_BASE}/companies/shenzhen_energy/exposures?limit=100")
        data = resp.json()
        print(f"shenzhen_energy total exposures: {data['total']}")
        for e in data["items"]:
            print(f"  {e['exposure_id']}: {e['node_id']} ({e['activity_type']})")
        
        # Also check Konka
        resp2 = await client.get(f"{API_BASE}/companies/konka_group/exposures?limit=100")
        data2 = resp2.json()
        print(f"konka_group total exposures: {data2['total']}")
        for e in data2["items"]:
            print(f"  {e['exposure_id']}: {e['node_id']} ({e['activity_type']})")

asyncio.run(check())
