import asyncio, httpx

async def main():
    async with httpx.AsyncClient() as c:
        r = await c.get('http://localhost:16060/api/v1/industries/semiconductor_industry/subgraph')
        d = r.json()
        nodes = {n['node_id']: n for n in d['nodes']}
        edges = d['edges']
        print('=== NODES ===')
        for nid in sorted(nodes):
            n = nodes[nid]
            print(f"{nid}: {n.get('canonical_name_zh','')} | {n.get('node_type','')} | {n.get('definition','')[:60]}")
        print('\n=== EDGES ===')
        for e in sorted(edges, key=lambda x: (x['from_node'], x['to_node'])):
            print(f"{e['from_node']} --[{e['edge_namespace']}/{e['edge_type']}]--> {e['to_node']}")

asyncio.run(main())
