import asyncio
import httpx

BASE_URL = "http://localhost:8005/api/v1"

batches = {
    "Batch 111": [
        "piston", "wheel_hub", "automotive_air_conditioner", "shock_absorber",
        "coated_paper", "white_cardboard", "writing_paper", "offset_paper",
        "tank (military vehicle)", "railway_vehicle", "special_purpose_vehicle",
        "metallurgical_machinery", "water_supply", "industrial_gas",
        "waste_heat_power_generation", "live_pig", "breeding_pig", "pork_product",
        "ferrite", "magnetic_device"
    ],
    "Batch 112": [
        "digital_marketing", "gold", "silver", "bismuth", "palladium", "rhodium",
        "radar", "rf_component", "communication_engineering", "steel_wire_rope",
        "steel_wire", "hemorrhoid_medicine", "energy_storage", "chip_card",
        "smart_card", "button", "zipper", "garment_accessory", "polymer_material"
    ],
    "Batch 113": [
        "kitchen_appliance", "led_lighting", "building_material_machinery",
        "textile_machinery", "carbon_fiber_equipment", "human_serum_albumin",
        "intravenous_immunoglobulin", "blood_product", "laser_marking_machine",
        "laser_welding_machine", "cnc_machine", "automated_conveying_system",
        "warehousing_system", "intelligent_logistics", "central_air_conditioner",
        "heat_exchanger", "electrolytic_capacitor_paper", "filter_paper",
        "color_printing_packaging", "aluminized_packaging", "plastic_film",
        "clean_energy", "integrated_energy_service"
    ],
    "Batch 114": [
        "polymer_material", "anti_infective_drug", "cardiovascular_drug",
        "embroidery_machine", "in_vitro_diagnostic_reagent", "medical_instrument",
        "aircraft_maintenance", "aviation_testing", "home_appliance_retail",
        "electronics_retail", "connector", "mobile_phone_battery", "drill_chuck",
        "power_tool_switch", "powder_metallurgy_part", "intelligent_manufacturing",
        "advertising_media", "building_media"
    ],
    "Batch 115": [
        "power_automation_protection", "high_voltage_switch", "mutual_inductor",
        "power_capacitor", "reactor", "jacket", "t_shirt", "cotton_padded_garment",
        "sweater", "genetic_testing_service", "tire_mold", "cookware",
        "passenger_cableway", "performance", "waste_incineration_power_generation",
        "waste_treatment", "gas_stove", "water_heater", "range_hood",
        "disinfection_cabinet", "optical_lens", "camera_module", "touch_display_module",
        "detonator", "explosive", "industrial_explosive"
    ]
}

async def check_term(client: httpx.AsyncClient, term: str):
    node_id = term.strip()
    try:
        resp = await client.get(f"{BASE_URL}/nodes/{node_id}", timeout=10.0)
        if resp.status_code == 200:
            data = resp.json()
            return {
                "term": term,
                "exists": "YES",
                "exact_node_id": data.get("id") or data.get("node_id") or node_id,
                "similar_nodes": []
            }
    except Exception as e:
        return {"term": term, "exists": "ERROR", "exact_node_id": None, "similar_nodes": [], "error": str(e)}

    # 404 or not found, try search
    try:
        resp = await client.get(f"{BASE_URL}/nodes", params={"search": node_id}, timeout=10.0)
        similar = []
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list):
                similar = data
            elif isinstance(data, dict):
                similar = data.get("items", data.get("results", data.get("data", [])))
        return {
            "term": term,
            "exists": "NO",
            "exact_node_id": None,
            "similar_nodes": similar
        }
    except Exception as e:
        return {"term": term, "exists": "ERROR", "exact_node_id": None, "similar_nodes": [], "error": str(e)}

async def main():
    results = {}
    async with httpx.AsyncClient() as client:
        for batch_name, terms in batches.items():
            print(f"\n=== {batch_name} ===")
            batch_results = []
            for term in terms:
                result = await check_term(client, term)
                batch_results.append(result)
                status = result["exists"]
                node_id = result.get("exact_node_id") or "N/A"
                sim_count = len(result.get("similar_nodes", []))
                print(f"  [{status}] {term} -> exact={node_id}, similar={sim_count}")
            results[batch_name] = batch_results

    # Print structured report
    print("\n\n" + "="*80)
    print("STRUCTURED REPORT")
    print("="*80)
    for batch_name, batch_results in results.items():
        print(f"\n{batch_name}")
        print("-" * 60)
        for r in batch_results:
            term = r["term"]
            exists = r["exists"]
            exact = r.get("exact_node_id") or "N/A"
            similar = r.get("similar_nodes", [])
            print(f"term: {term}")
            print(f"  exists: {exists}")
            print(f"  exact_node_id: {exact}")
            if similar:
                sim_strs = []
                for s in similar[:5]:
                    if isinstance(s, dict):
                        sid = s.get("id") or s.get("node_id") or str(s)
                        sname = s.get("name") or s.get("label") or ""
                        sim_strs.append(f"{sid}" + (f" ({sname})" if sname else ""))
                    else:
                        sim_strs.append(str(s))
                print(f"  similar_nodes: {', '.join(sim_strs)}")
            else:
                print(f"  similar_nodes: None")
            print()

if __name__ == "__main__":
    asyncio.run(main())
