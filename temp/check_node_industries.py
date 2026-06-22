import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as c:
        # List all industries
        r = await c.get('http://localhost:16060/api/v1/industries?page=1&page_size=200')
        industries = r.json()['items']
        # Find industry whose name contains 原始名称
        target = None
        for ind in industries:
            name = ind.get('name_zh') or ''
            if '原始名称' in name:
                target = ind
                print('found industry:', ind)
                break
        if not target:
            print('no industry named 原始名称')
        # Get industries by node for silicon and silicon_material
        for nid in ['silicon', 'silicon_material']:
            r2 = await c.get(f'http://localhost:16060/api/v1/industries/by-node/{nid}')
            data = r2.json()
            print(f'\nnode {nid}:')
            for ind in data['industries']:
                print('  ', ind['industry_id'], ind['name_zh'])
            for m in data['mappings']:
                print('  mapping:', m['mapping_id'], m['industry_id'])

asyncio.run(main())
