#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check node existence for batches 116-120 candidates."""

import json
import urllib.request
import urllib.parse

BASE_URL = "http://localhost:8005/api/v1"

# All candidate node IDs for batches 116-120
CANDIDATES = [
    # Batch 116
    "gene_engineering_drug", "biochemical_drug", "chemical_drug", "freeze_dried_powder_injection",
    "antitumor_drug", "recombinant_protein", "interleukin", "growth_factor",
    "api", "salmon_calcitonin", "thymopentin", "somatostatin", "ganciclovir",
    "oxaliplatin", "temozolomide", "heparin_sodium",
    "section_steel", "steel_bar", "rebar", "hot_rolled_coil", "cold_rolled_sheet",
    "heavy_plate", "steel_rolling", "coking", "iron_ore", "coke",
    "modified_plastic", "engineering_plastic", "synthetic_resin", "synthetic_fiber",
    "glass_fiber_reinforced_plastic", "bio_based_material", "rubber_product", "sponge_product",
    "recycled_resource", "plastic_product",
    "lead_acid_battery", "gas_turbine_power", "steam_turbine_power", "diesel_engine_power",
    "marine_engine", "marine_equipment", "ship_support_equipment", "battery",
    "lead", "zinc", "lead_zinc_alloy", "non_ferrous_metal_smelting", "industrial_sulfuric_acid",
    "sulfur_dioxide", "energy_storage_battery", "used_power_battery_recycling",
    "concentrated_apple_juice", "concentrated_fruit_vegetable_juice",
    "livestock_poultry_breeding", "slaughtering_processing", "meat_product",
    "quick_frozen_food", "dairy_product", "catering_service", "organic_fertilizer",
    "coal_mining", "coal_washing", "coal_and_products",
    "wire_cable", "cable_accessory", "superconducting_system", "optical_fiber",
    "optical_cable", "marine_engineering_equipment", "offshore_wind_power_equipment",
    "communication_equipment", "navigation_instrument",
    "hydropower", "electric_power_supply", "natural_gas_supply", "tap_water_supply",
    # Batch 117
    "textile", "textile_garment", "textile_raw_material", "electronic_equipment",
    "steam", "heat_supply", "thermal_power",
    "washing_machine", "refrigerator", "microwave_oven", "bidet", "air_purifier",
    "kitchen_appliance",
    "asphalt_concrete_pavers", "stabilized_soil_mixer", "construction_machinery",
    "hoisting_machinery", "mining_machinery",
    "textile_printing_dyeing", "dye", "woven_fabric", "gold_jewelry",
    "thermal_power_generation", "electric_power",
    "hydropower_station", "port", "crude_oil", "refined_oil_product", "liquid_chemical",
    "cement_production_line", "cement_equipment", "concrete_product", "engineering_contracting",
    "corn_seed", "vegetable_seed", "flower", "crop_seed",
    # Batch 118
    "cotton_yarn", "blended_yarn", "cotton_grey_cloth", "blended_grey_cloth",
    "decorative_veneer", "plywood", "wooden_floor", "furniture", "wood_processing",
    "health_examination", "health_management", "medical_service",
    "audio_system", "loudspeaker_unit", "electronic_connector", "electronic_component",
    "bearing", "spindle", "non_metallic_mineral_product", "non_ferrous_metal_alloy",
    "analytical_instrument", "photovoltaic_equipment",
    "building_decoration", "intelligent_building_system", "fire_protection_engineering",
    "curtain_wall", "smart_city",
    "automotive_interior_exterior_trim", "automotive_body_metal_part", "automotive_lightweight_material",
    "automotive_part",
    "integrated_circuit", "smart_chip", "special_integrated_circuit", "memory_chip",
    "globe_valve", "electronic_expansion_valve", "solenoid_valve", "refrigeration_air_conditioning_equipment",
    "pump", "motor", "fan",
    "railway_video_monitoring", "railway_disaster_prevention_system", "railway_communication_system",
    "railway_operation_maintenance_service",
    # Batch 119
    "international_engineering_contracting", "complete_equipment_export", "overseas_project",
    "digital_tv_receiver", "set_top_box", "led_display",
    "salt", "industrial_salt", "daily_chemical_salt", "mirabilite", "natural_gas",
    "wind_power", "solar_power_generation",
    "coal", "coal_and_product",
    "commercial_bank", "investment_bank", "insurance", "financial_bond", "foreign_exchange",
    "fine_chemical", "petrochemical_product", "printing_ink", "coating", "dye_product",
    "daily_chemical_product",
    "automotive_connector", "wire_harness", "flexible_printed_circuit", "led",
    "crystalline_silicon_solar_cell", "permanent_magnet_ferrite", "soft_magnet_ferrite",
    "magnetic_material", "solar_pv_equipment",
    "real_estate_development", "property_management", "house_leasing",
    "manganese_tetroxide", "steel_wire", "permanent_magnet_device", "rare_earth_functional_material",
    "electronic_special_material", "graphite_carbon_product", "graphene",
    # Batch 120
    "electromagnetic_flowmeter", "pressure_transmitter", "automation_instrument",
    "electronic_special_material", "new_membrane_material",
    "scenic_spot", "tourism_service", "wedding_service", "convention_exhibition",
    "railway_transport", "coal_transportation",
    "water_conservancy_project", "municipal_engineering", "road_engineering",
    "electromechanical_installation", "wind_power_generation", "solar_power",
    "urban_rail_transit", "harbor_waterway_engineering", "airport_engineering",
    "dangerous_chemical",
    "foundation_engineering", "steel_structure_engineering", "bridge_engineering",
    "real_estate",
    "power_industry_software", "financial_management_software",
    "spandex", "synthetic_fiber_product",
    "industry_application_software", "system_integration", "artificial_intelligence",
    "refractory_material", "fused_cast_zirconia_corundum", "fused_cast_alumina",
    "inorganic_non_metallic_material",
]

def check_node(node_id):
    url = f"{BASE_URL}/nodes/{node_id}"
    try:
        req = urllib.request.Request(url, method="GET")
        req.add_header("Accept", "application/json")
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode())
                return "EXISTS", data.get("name", "")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "MISSING", ""
        return f"ERROR_{e.code}", ""
    except Exception as e:
        return f"ERR", str(e)
    return "UNKNOWN", ""

def search_nodes(term):
    url = f"{BASE_URL}/nodes?search={urllib.parse.quote(term)}&limit=20"
    try:
        req = urllib.request.Request(url, method="GET")
        req.add_header("Accept", "application/json")
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            items = data.get("items", [])
            return [(i.get("node_id"), i.get("name")) for i in items]
    except Exception:
        return []

if __name__ == "__main__":
    print("=== Node Existence Check for Batches 116-120 ===\n")
    exists = []
    missing = []
    errors = []

    for cid in CANDIDATES:
        status, name = check_node(cid)
        if status == "EXISTS":
            exists.append((cid, name))
        elif status == "MISSING":
            missing.append(cid)
        else:
            errors.append((cid, status))

    print(f"--- EXISTS ({len(exists)}) ---")
    for cid, name in exists:
        print(f"  {cid} -> {name}")

    print(f"\n--- MISSING ({len(missing)}) ---")
    for cid in missing:
        print(f"  {cid}")

    if errors:
        print(f"\n--- ERRORS ({len(errors)}) ---")
        for cid, status in errors:
            print(f"  {cid} -> {status}")

    # Also do a few fuzzy searches for ambiguous terms
    print("\n=== Fuzzy Searches ===")
    fuzzy_terms = ["steel", "battery", "solar", "software", "textile", "construction", "coal", "railway"]
    for term in fuzzy_terms:
        results = search_nodes(term)
        print(f"\n  search '{term}':")
        for nid, nname in results[:5]:
            print(f"    {nid} = {nname}")
