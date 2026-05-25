import asyncio
import asyncpg

async def main():
    try:
        conn = await asyncpg.connect("postgresql://postgres:postgres@localhost:5433/arachne")
        
        # Check company_view_versions
        rows = await conn.fetch("SELECT version_id, job_id, status, created_at FROM company_view_versions ORDER BY version_id")
        print(f"company_view_versions: {len(rows)} rows")
        for r in rows:
            print(f"  version_id={r['version_id']} status={r['status']} created_at={r['created_at']}")
        
        # Check companies count
        c = await conn.fetchval("SELECT COUNT(*) FROM companies")
        print(f"\ncompanies: {c} rows")
        
        await conn.close()
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(main())
