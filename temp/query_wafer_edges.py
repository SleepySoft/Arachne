# -*- coding: utf-8 -*-
import asyncio
import httpx

BASE = "http://localhost:16060/api/v1"

async def main():
    async with httpx.AsyncClient() as c:
        # edges from/to wafer
        for direction in ["from_node", "to_node"]:
            r = await c.get(f"{BASE}/edges?page=1&page_size=100&{direction}=wafer")
            data = r.json()
            print(f"\n{direction}=wafer total={data['total']}")
            for e in data['items']:
                print(f"  {e['edge_id']}: {e['from_node']} -> {e['to_node']} [{e['edge_namespace']}/{e['edge_type']}]")

        # existing relevant nodes
        relevant_prefixes = [
            "lithography", "etching", "cleaning", "ion_implanter", "cmp", "metrology",
            "photoresist", "electronic_special_gases", "wet_chemicals", "sputtering_target",
            "cmp_slurry", "cmp_pad", "eda", "ip_core", "foundry", "idm", "chip_design",
            "wafer_manufacturing", "wafer", "silicon_wafer", "chip"
        ]
        r = await c.get(f"{BASE}/nodes?page=1&page_size=1000")
        nodes = r.json()['items']
        print("\nrelevant nodes:")
        for n in nodes:
            if any(p in n['node_id'] for p in relevant_prefixes):
                print(f"  {n['node_id']}: {n.get('canonical_name_zh')} ({n.get('entity_type')})")

asyncio.run(main())
