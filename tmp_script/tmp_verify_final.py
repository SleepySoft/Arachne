import asyncio, httpx

API_BASE = "http://localhost:8000/api/v1"

async def check():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_BASE}/companies?limit=20")
        data = resp.json()
        print(f"Companies total: {data['total']}")
        for c in data["items"]:
            print(f"  {c['company_id']}: {c['name_zh']}")
        
        for c in data["items"]:
            resp2 = await client.get(f"{API_BASE}/companies/{c['company_id']}/exposures")
            exp_data = resp2.json()
            print(f"{c['company_id']} exposures: {len(exp_data)}")

asyncio.run(check())
