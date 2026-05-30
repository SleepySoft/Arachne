import asyncio, httpx

async def test():
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://localhost:8000/api/v1/industries?limit=10")
        data = resp.json()
        if data["items"]:
            ind = data["items"][0]
            print(f"Testing industry: {ind['industry_id']}")
            resp2 = await client.get(f"http://localhost:8000/api/v1/industries/{ind['industry_id']}/subgraph")
            sub = resp2.json()
            print(f"Nodes: {len(sub['nodes'])}, Edges: {len(sub['edges'])}")
            if sub["edges"]:
                e = sub["edges"][0]
                print(f"First edge keys: {list(e.keys())}")
                print(f"Has edge_namespace: {'edge_namespace' in e}")

asyncio.run(test())
