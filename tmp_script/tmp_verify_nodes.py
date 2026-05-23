import asyncio, sys, json
sys.path.insert(0, 'backend')
from app.database import get_async_driver

# 55 new nodes from batch_002
new_node_ids = [
    "steel_rebar", "architectural_design_service", "color_tv", "refrigerator", "washing_machine",
    "mobile_phone", "pcb_board", "pcb_substrate", "semiconductor_device", "display_module",
    "steel_sheet", "precious_metal", "gold_jewelry", "bicycle", "electric_bicycle",
    "watch", "watch_movement", "watch_component", "stainless_steel", "agricultural_product",
    "grain_oil", "tea", "food_condiment", "food_ingredient", "grain_storage_service",
    "grain_processing", "dram_chip", "nand_flash_chip", "memory_dimm", "usb_flash_drive",
    "packaging_substrate", "hard_disk_drive", "container", "bulk_cargo", "port_operation_service",
    "container_handling_service", "bonded_warehousing_service", "shipping_service", "automotive_sales_service",
    "automotive_maintenance_service", "automotive_inspection_service", "jewelry_retail_service",
    "coal", "electricity_power", "coal_power_generation", "gas_power_generation",
    "wind_power_generation", "solar_power_generation", "hydro_power_generation", "waste_to_energy",
    "sludge_treatment", "waste_water_treatment", "city_gas_supply", "electricity_transmission",
    "electricity_distribution"
]

async def check():
    driver = get_async_driver()
    async with driver.session() as session:
        for nid in new_node_ids:
            result = await session.run("MATCH (n:IndustrialNode {node_id: $id}) RETURN n.node_id AS id", id=nid)
            rec = await result.single()
            status = "EXISTS" if rec else "MISSING"
            print(f"{nid}: {status}")

asyncio.run(check())
