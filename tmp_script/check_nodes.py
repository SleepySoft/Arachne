import asyncio
import httpx

BASE = "http://localhost:8005/api/v1"

batches = {
    "Batch 106": [
        ("diesel_engine",),
        ("compressor",),
        ("mobile_phone",),
        ("industrial_sewing_machine",),
        ("sewing_machine",),
        ("coal_chemical_product",),
        ("software_development",),
        ("service_outsourcing",),
        ("system_integration",),
        ("intelligent_transportation",),
        ("lead_acid_battery",),
        ("technology_park_development", "park_operation", "technology_park"),
        ("intelligent_building",),
    ],
    "Batch 107": [
        ("plush_textile",),
        ("highway_bridge_construction",),
        ("security_service",),
        ("medical_device",),
        ("gas_storage_equipment",),
        ("human_resource_service",),
        ("aviation_new_material",),
    ],
    "Batch 108": [
        ("heat_supply",),
        ("securities_brokerage",),
        ("nucleotide",),
        ("msg", "monosodium_glutamate", "flavor_enhancer"),
        ("soy_sauce",),
        ("recombinant_human_insulin",),
        ("infusion_solution",),
        ("power_cable",),
        ("electrical_wire", "wire_cable"),
        ("carbon_fiber_composite_conductor",),
        ("oil_gas_exploration",),
        ("petroleum_engineering_service",),
        ("condiment",),
        ("amino_acid",),
        ("organic_fertilizer",),
    ],
    "Batch 109": [
        ("sewage_treatment",),
        ("toll_road",),
        ("power_generation_equipment",),
        ("solar_glass", "photovoltaic_glass"),
        ("semiconductor_chip", "integrated_circuit"),
        ("aerospace_electronic_equipment",),
        ("printing_service",),
        ("cheese",),
        ("liquid_milk",),
        ("lithium_ion_battery_material", "battery_material"),
    ],
    "Batch 110": [
        ("relay",),
        ("low_voltage_electrical", "low_voltage_electrical_apparatus"),
        ("contactor",),
        ("automation_equipment",),
        ("electricity_power_generation",),
        ("ice_cream",),
        ("milk_powder",),
        ("electronic_aluminum_foil",),
        ("high_purity_aluminum",),
        ("aluminum_rod",),
        ("formed_foil",),
        ("etched_foil",),
        ("viscose_fiber",),
        ("aero_engine", "aircraft_engine", "aviation_engine"),
        ("elevator_parts",),
        ("airport_operation", "airport_service"),
        ("air_ground_service",),
    ],
}

async def check_node(client: httpx.AsyncClient, node_id: str):
    r = await client.get(f"{BASE}/nodes/{node_id}")
    return r.status_code == 200

async def search_nodes(client: httpx.AsyncClient, term: str):
    r = await client.get(f"{BASE}/nodes", params={"search": term, "page_size": 20})
    if r.status_code != 200:
        return []
    data = r.json()
    # The API returns a dict with items
    if isinstance(data, dict):
        return data.get("items", data.get("data", []))
    if isinstance(data, list):
        return data
    return []

async def process():
    async with httpx.AsyncClient(timeout=30) as client:
        for batch_name, items in batches.items():
            print(f"\n{'='*60}")
            print(f"  {batch_name}")
            print(f"{'='*60}")
            for terms in items:
                primary = terms[0]
                alts = terms[1:]

                exists = await check_node(client, primary)
                status = "EXISTS" if exists else "NOT FOUND"
                print(f"\n  {primary}  ->  {status}")

                similar = []
                search_terms = list(terms) if not exists else []
                # Also search for fragments of the primary id as fallback
                if not exists:
                    # Add some heuristic search terms
                    fragments = [t for t in terms]
                    # if primary has underscores, also try the last word
                    if "_" in primary:
                        fragments.append(primary.split("_")[-1])
                    # and the first word
                    if "_" in primary:
                        fragments.append(primary.split("_")[0])
                    search_terms = list(dict.fromkeys(fragments))  # dedup, preserve order

                for st in search_terms:
                    results = await search_nodes(client, st)
                    for node in results:
                        nid = node.get("node_id") or node.get("id")
                        name = node.get("name", "")
                        ntype = node.get("node_type", "")
                        if nid and nid != primary:
                            similar.append((nid, name, ntype))
                        elif nid == primary and not exists:
                            # API returned it in search but direct GET failed?
                            pass

                # dedup similar by node_id
                seen = set()
                uniq_similar = []
                for nid, name, ntype in similar:
                    if nid and nid not in seen:
                        seen.add(nid)
                        uniq_similar.append((nid, name, ntype))

                if uniq_similar:
                    print(f"    Similar nodes found:")
                    for nid, name, ntype in uniq_similar[:8]:
                        print(f"      - {nid}  (name='{name}', type={ntype})")
                    if len(uniq_similar) > 8:
                        print(f"      ... and {len(uniq_similar)-8} more")
                else:
                    if not exists:
                        print(f"    No similar nodes found.")

                if not exists:
                    suggested = primary
                    print(f"    Suggested node_id: {suggested}")

if __name__ == "__main__":
    asyncio.run(process())
