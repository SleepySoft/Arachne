import sys, os
os.chdir('C:/D/code/Arachne')
sys.path.insert(0, 'backend')
import asyncio
from app.database_postgres import get_postgres_pool

async def main():
    pool = await get_postgres_pool()
    if not pool:
        print('PostgreSQL not available')
        return
    async with pool.acquire() as conn:
        rows = await conn.fetch('SELECT company_id, name_zh FROM companies ORDER BY company_id')
        print(f'Total companies: {len(rows)}')
        for r in rows:
            print(f"{r['company_id']} | {r['name_zh']}")
    await pool.close()

asyncio.run(main())
