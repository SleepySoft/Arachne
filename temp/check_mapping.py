import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as c:
        r = await c.get('http://localhost:16060/api/v1/industries/test_ind_up_a754ba/mappings?page=1&page_size=100')
        data = r.json()
        print('total', data['total'])
        for m in data['items']:
            print(m)

asyncio.run(main())
