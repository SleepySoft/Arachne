# -*- coding: utf-8 -*-
import asyncio
import httpx

EXPOSURES = [
    {
        "company_id": "huat_gas",
        "node_id": "tungsten_hexafluoride",
        "activity_type": "provide_service",
        "role": "根据客户需求供应纯化六氟化钨产品（无合成产能）",
        "weight": 0.4,
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [{
            "source_title": "华特气体投资者互动回复（同花顺/证券时报）",
            "source_url": "https://finance.ifeng.com/c/8tu9Jpd9Z0G",
            "quote": "截至目前，公司并无六氟化钨合成产能，仅根据部分客户要求供应纯化六氟化钨产品，业务占比较小。"
        }],
    },
    {
        "company_id": "air_liquide",
        "node_id": "tungsten_hexafluoride",
        "activity_type": "produce",
        "role": "全球电子级六氟化钨主要供应商之一，约占 24% 供应能力",
        "weight": 0.8,
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [{
            "source_title": "Global Electronic Special Tungsten Hexafluoride (WF6) Market Size, Industry Share & Forecast 2026-2034",
            "source_url": "https://www.verifiedmarketreports.com/product/electronic-grade-tungsten-hexafluoride-wf6-market/",
            "quote": "Air Liquide: Approximately 24% of the Electronic Special Tungsten Hexafluoride (WF6) Market supply capacity is associated with Air Liquide due to its strong semiconductor gas purification infrastructure and advanced electronic materials portfolio."
        }],
    },
    {
        "company_id": "linde",
        "node_id": "tungsten_hexafluoride",
        "activity_type": "produce",
        "role": "全球电子级六氟化钨主要供应商之一，约占 21% 供应能力",
        "weight": 0.8,
        "confidence": "MEDIUM",
        "status": "ACTIVE",
        "evidence": [{
            "source_title": "Global Electronic Special Tungsten Hexafluoride (WF6) Market Size, Industry Share & Forecast 2026-2034",
            "source_url": "https://www.verifiedmarketreports.com/product/electronic-grade-tungsten-hexafluoride-wf6-market/",
            "quote": "Linde: Linde contributes nearly 21% of global semiconductor-grade WF6 supply operations, supported by extensive specialty gas distribution networks and advanced purification systems."
        }],
    },
]


async def main():
    async with httpx.AsyncClient(timeout=60.0) as client:
        for exp in EXPOSURES:
            exp_id = f"{exp['company_id']}_{exp['node_id']}"
            payload = {**exp, "exposure_id": exp_id}
            r = await client.post(
                f"http://localhost:16060/api/v1/companies/{exp['company_id']}/exposures",
                json=payload,
            )
            print(exp["company_id"], r.status_code, r.json() if r.status_code >= 400 else "ok")


asyncio.run(main())
