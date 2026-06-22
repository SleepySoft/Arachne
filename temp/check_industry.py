import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as c:
        r = await c.get('http://localhost:16060/api/v1/industries?search=%E5%8E%9F%E5%A7%8B%E5%90%8D%E7%A7%B0&page=1&page_size=10')
        print(r.json())
        # also list all industries
        r2 = await c.get('http://localhost:16060/api/v1/industries?page=1&page_size=100')
        for ind in r2.json()['items']:
            print(ind['industry_id'], ind['name_zh'])

asyncio.run(main())
