import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as c:
        r = await c.get('http://localhost:16060/api/v1/industries/test_ind_up_a754ba')
        d = r.json()
        print(repr(d['name_zh']))

asyncio.run(main())
