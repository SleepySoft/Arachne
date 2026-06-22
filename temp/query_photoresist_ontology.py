# -*- coding: utf-8 -*-
import asyncio
import httpx

BASE = "http://localhost:16060/api/v1"

async def main():
    async with httpx.AsyncClient() as c:
        for child, parent in [
            ("duv_photoresist", "photoresist"),
            ("euv_photoresist", "photoresist"),
            ("tungsten_hexafluoride", "electronic_special_gases"),
        ]:
            r = await c.get(f"{BASE}/edges?from_node={child}&to_node={parent}&page=1&page_size=10")
            data = r.json()
            print(f"{child} -> {parent}: {data['total']}")
            for e in data['items']:
                print(f"  {e['edge_id']} {e['edge_type']}")

asyncio.run(main())
