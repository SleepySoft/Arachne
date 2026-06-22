import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as c:
        r = await c.get('http://localhost:16060/api/v1/companies?page=1&page_size=200')
        companies = r.json()['items']
        test_co = [co for co in companies if co['company_id'].startswith('test_')]
        print('test companies count:', len(test_co))
        for co in test_co[:20]:
            print(co['company_id'], co['name_zh'])

asyncio.run(main())
