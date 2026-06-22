import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as c:
        for from_node, to_node in [
            ('silicon','semiconductor'),
            ('silicon','silicon_wafer'),
            ('silicon_wafer','wafer'),
            ('semiconductor_device','chip'),
            ('chip','semiconductor_device'),
            ('integrated_circuit','semiconductor_device'),
        ]:
            r = await c.get(f'http://localhost:16060/api/v1/edges?from_node={from_node}&to_node={to_node}&page=1&page_size=20')
            data = r.json()
            print(from_node, '->', to_node, 'count', data['total'])
            for e in data['items']:
                print('  ', e['edge_id'], e['edge_namespace'], e['edge_type'], e.get('description'))

asyncio.run(main())
