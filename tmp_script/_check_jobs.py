import asyncio, sys
sys.path.insert(0, 'backend')
from app.database_postgres import get_postgres_pool

async def main():
    pool = await get_postgres_pool()
    if pool is None:
        print('PostgreSQL not available')
        return
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT job_id, job_type, status, error_message FROM computation_jobs WHERE error_message IS NOT NULL ORDER BY created_at DESC LIMIT 10"
        )
        for r in rows:
            print(f"Job {r['job_id']}: type={r['job_type']}, status={r['status']}, error={r['error_message']}")
        if not rows:
            print('No failed jobs found')
    await pool.close()

asyncio.run(main())
