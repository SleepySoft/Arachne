import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as c:
        r = await c.get('http://localhost:16060/api/v1/industries?page=1&page_size=200')
        industries = r.json()['items']
        test_inds = [ind for ind in industries if ind['industry_id'].startswith('test_')]
        print('test industries count:', len(test_inds))
        for ind in test_inds:
            print(ind['industry_id'], ind['name_zh'], ind['status'])
            r2 = await c.get(f"http://localhost:16060/api/v1/industries/{ind['industry_id']}/mappings?page=1&page_size=100")
            mappings = r2.json()['items']
            for m in mappings:
                print('  mapping:', m['mapping_id'], m['node_id'])

asyncio.run(main())
