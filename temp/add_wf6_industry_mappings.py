# -*- coding: utf-8 -*-
import asyncio
import httpx

INDUSTRY_ID = "semiconductor_industry"
NODE_IDS = [
    "tungsten_hexafluoride",
    "tungsten_pentachloride",
    "tungsten_hexachloride",
    "tungsten_hexacarbonyl",
    "molybdenum_precursor",
    "tungsten_film",
    "molybdenum_film",
]


async def main():
    async with httpx.AsyncClient(timeout=60.0) as client:
        for node_id in NODE_IDS:
            mapping_id = f"{INDUSTRY_ID}_contains_{node_id}"
            payload = {
                "mapping_id": mapping_id,
                "industry_id": INDUSTRY_ID,
                "node_id": node_id,
                "role": "semiconductor metallization key material",
                "weight": 0.9,
                "confidence": "MEDIUM",
                "status": "PENDING",
            }
            r = await client.post(
                f"http://localhost:16060/api/v1/industries/{INDUSTRY_ID}/mappings",
                json=payload,
            )
            print(node_id, r.status_code, r.json() if r.status_code >= 400 else "ok")


asyncio.run(main())
