# Arachne Node Existence Report — Batches 106-110

**API Base:** `http://localhost:8005/api/v1`  
**Total Nodes in Graph:** 1,107 | **Total Edges:** 534

---

## Summary by Batch

| Batch | Checked | Exists | Missing |
|-------|---------|--------|---------|
| 106 | 13 | 3 | 10 |
| 107 | 7 | 1 | 6 |
| 108 | 15 | 3 | 12 |
| 109 | 10 | 2 | 8 |
| 110 | 17 | 2 | 15 |
| **Total** | **62** | **11** | **51** |

---

## Batch 106

| # | Term / Node ID | Exists? | Notes / Similar Nodes |
|---|----------------|---------|----------------------|
| 1 | `diesel_engine` | **YES** | — |
| 2 | `compressor` | NO | `refrigeration_compressor`, `air_conditioner_compressor` exist |
| 3 | `mobile_phone` | **YES** | — |
| 4 | `industrial_sewing_machine` | **YES** | — |
| 5 | `sewing_machine` | NO | `industrial_sewing_machine` exists (more specific variant) |
| 6 | `coal_chemical_product` | NO | Generic "product" matches; no direct coal-chemical node |
| 7 | `software_development` | NO | `software_development_service` exists |
| 8 | `service_outsourcing` | NO | No close match |
| 9 | `system_integration` | NO | `information_system_integration` exists |
| 10 | `intelligent_transportation` | NO | `intelligent_transport_system` exists (very close synonym) |
| 11 | `lead_acid_battery` | NO | `energy_storage_battery`, `lithium_ion_battery` exist |
| 12 | `technology_park_development` / `park_operation` / `technology_park` | NO | `industrial_park_operation`, `tech_park_operation_service` exist |
| 13 | `intelligent_building` | NO | `office_building`, `building_material` exist |

**Suggested new node IDs for Batch 106:** `compressor`, `sewing_machine`, `coal_chemical_product`, `software_development`, `service_outsourcing`, `system_integration`, `intelligent_transportation`, `lead_acid_battery`, `technology_park_development`, `intelligent_building`

---

## Batch 107

| # | Term / Node ID | Exists? | Notes / Similar Nodes |
|---|----------------|---------|----------------------|
| 1 | `plush_textile` | NO | `flax_textile`, `wool_textile`, `textile_product`, `textile_machinery` exist |
| 2 | `highway_bridge_construction` | NO | `bridge_construction`, `highway`, `civil_construction` exist |
| 3 | `security_service` | NO | `emergency_security_service`, `mobile_app_security_service` exist |
| 4 | `medical_device` | **YES** | — |
| 5 | `gas_storage_equipment` | NO | `cold_storage_equipment`, `refrigeration_equipment` exist |
| 6 | `human_resource_service` | NO | No close match |
| 7 | `aviation_new_material` | NO | `catalytic_material`, `semiconductor_material` exist (generic) |

**Suggested new node IDs for Batch 107:** `plush_textile`, `highway_bridge_construction`, `security_service`, `gas_storage_equipment`, `human_resource_service`, `aviation_new_material`

---

## Batch 108

| # | Term / Node ID | Exists? | Notes / Similar Nodes |
|---|----------------|---------|----------------------|
| 1 | `heat_supply` | **YES** | — |
| 2 | `securities_brokerage` | **YES** | — |
| 3 | `nucleotide` | NO | No close match |
| 4 | `msg` / `monosodium_glutamate` / `flavor_enhancer` | NO | **`monosodium_glutamate` exists!** — use `monosodium_glutamate` instead of `msg` |
| 5 | `soy_sauce` | **YES** | — |
| 6 | `recombinant_human_insulin` | NO | No close match |
| 7 | `infusion_solution` | NO | `cloud_solution` only (unrelated) |
| 8 | `power_cable` | **YES** | — |
| 9 | `electrical_wire` / `wire_cable` | NO | **`wire_cable` exists!** — use `wire_cable` instead |
| 10 | `carbon_fiber_composite_conductor` | NO | `low_carbon_energy_saving`, semiconductor-related nodes exist (unrelated) |
| 11 | `oil_gas_exploration` | NO | `petroleum_exploration` exists (close synonym) |
| 12 | `petroleum_engineering_service` | NO | `oilfield_service` exists |
| 13 | `condiment` | NO | **`food_condiment` exists!** — use `food_condiment` instead |
| 14 | `amino_acid` | NO | `sulfuric_acid`, `citric_acid`, `amino_composite_material` exist |
| 15 | `organic_fertilizer` | NO | `chemical_fertilizer`, `compound_fertilizer`, `phosphate_fertilizer` exist |

**Key aliases found in Batch 108:**
- Use `monosodium_glutamate` (not `msg`)
- Use `wire_cable` (not `electrical_wire`)
- Use `food_condiment` (not `condiment`)

**Suggested new node IDs for Batch 108:** `nucleotide`, `recombinant_human_insulin`, `infusion_solution`, `carbon_fiber_composite_conductor`, `oil_gas_exploration`, `petroleum_engineering_service`, `amino_acid`, `organic_fertilizer`

---

## Batch 109

| # | Term / Node ID | Exists? | Notes / Similar Nodes |
|---|----------------|---------|----------------------|
| 1 | `sewage_treatment` | NO | `city_sewage_treatment`, `sewage_treatment_service` exist |
| 2 | `toll_road` | NO | `road_engineering`, `road_bridge` exist |
| 3 | `power_generation_equipment` | **YES** | — |
| 4 | `solar_glass` / `photovoltaic_glass` | NO | **`pv_glass` exists!** — use `pv_glass` instead |
| 5 | `semiconductor_chip` / `integrated_circuit` | NO | **`integrated_circuit` exists!** — use `integrated_circuit` instead |
| 6 | `aerospace_electronic_equipment` | NO | Many generic "equipment" nodes; no exact match |
| 7 | `printing_service` | **YES** | — |
| 8 | `cheese` | NO | No close match |
| 9 | `liquid_milk` | NO | `soy_milk_powder` exists (different product) |
| 10 | `lithium_ion_battery_material` / `battery_material` | NO | `battery_cathode_material` exists (specific component) |

**Key aliases found in Batch 109:**
- Use `pv_glass` (not `solar_glass`)
- Use `integrated_circuit` (not `semiconductor_chip`)

**Suggested new node IDs for Batch 109:** `sewage_treatment`, `toll_road`, `aerospace_electronic_equipment`, `cheese`, `liquid_milk`, `lithium_ion_battery_material`

---

## Batch 110

| # | Term / Node ID | Exists? | Notes / Similar Nodes |
|---|----------------|---------|----------------------|
| 1 | `relay` | NO | No close match |
| 2 | `low_voltage_electrical` / `low_voltage_electrical_apparatus` | NO | `rail_transit_electrical`, `low_carbon_energy_saving` exist |
| 3 | `contactor` | NO | No close match |
| 4 | `automation_equipment` | NO | Many generic "equipment" nodes; no exact match |
| 5 | `electricity_power_generation` | NO | `solar_power_generation`, `thermal_power_generation`, `hydro_power_generation`, `power_generation_equipment` exist |
| 6 | `ice_cream` | NO | No close match |
| 7 | `milk_powder` | NO | `soy_milk_powder`, `bleaching_powder` exist |
| 8 | `electronic_aluminum_foil` | NO | `hydrophilic_aluminum_foil`, `copper_foil` exist |
| 9 | `high_purity_aluminum` | NO | `automotive_aluminum`, `aluminum_alloy`, `aluminum_profile` exist |
| 10 | `aluminum_rod` | NO | `steel_wire_rod` exists (different material) |
| 11 | `formed_foil` | NO | `hydrophilic_aluminum_foil`, `copper_foil` exist |
| 12 | `etched_foil` | NO | `hydrophilic_aluminum_foil`, `copper_foil` exist |
| 13 | `viscose_fiber` | **YES** | — |
| 14 | `aero_engine` / `aircraft_engine` / `aviation_engine` | NO | `aero_engine_part` exists (component only) |
| 15 | `elevator_parts` | **YES** | — |
| 16 | `airport_operation` / `airport_service` | NO | `airport_operation_service` exists (very close) |
| 17 | `air_ground_service` | NO | No close match |

**Suggested new node IDs for Batch 110:** `relay`, `low_voltage_electrical`, `contactor`, `automation_equipment`, `electricity_power_generation`, `ice_cream`, `milk_powder`, `electronic_aluminum_foil`, `high_purity_aluminum`, `aluminum_rod`, `formed_foil`, `etched_foil`, `aero_engine`, `airport_operation`, `air_ground_service`

---

## Critical Findings — Existing Aliases (Do NOT create new nodes)

| Your Term | Existing Node ID in Graph | Action |
|-----------|---------------------------|--------|
| `msg` / `flavor_enhancer` | `monosodium_glutamate` | Use existing |
| `electrical_wire` / `wire_cable` | `wire_cable` | Use existing |
| `condiment` | `food_condiment` | Use existing |
| `solar_glass` / `photovoltaic_glass` | `pv_glass` | Use existing |
| `semiconductor_chip` / `integrated_circuit` | `integrated_circuit` | Use existing |

## Close Synonyms Already in Graph

| Your Term | Very Similar Existing Node |
|-----------|---------------------------|
| `software_development` | `software_development_service` |
| `system_integration` | `information_system_integration` |
| `intelligent_transportation` | `intelligent_transport_system` |
| `technology_park_development` | `industrial_park_operation`, `tech_park_operation_service` |
| `sewing_machine` | `industrial_sewing_machine` |
| `sewage_treatment` | `city_sewage_treatment`, `sewage_treatment_service` |
| `oil_gas_exploration` | `petroleum_exploration` |
| `airport_operation` | `airport_operation_service` |

---

## Recommended New Nodes to Create (51 total)

**Batch 106 (10):** `compressor`, `sewing_machine`, `coal_chemical_product`, `software_development`, `service_outsourcing`, `system_integration`, `intelligent_transportation`, `lead_acid_battery`, `technology_park_development`, `intelligent_building`

**Batch 107 (6):** `plush_textile`, `highway_bridge_construction`, `security_service`, `gas_storage_equipment`, `human_resource_service`, `aviation_new_material`

**Batch 108 (8):** `nucleotide`, `recombinant_human_insulin`, `infusion_solution`, `carbon_fiber_composite_conductor`, `oil_gas_exploration`, `petroleum_engineering_service`, `amino_acid`, `organic_fertilizer`

**Batch 109 (6):** `sewage_treatment`, `toll_road`, `aerospace_electronic_equipment`, `cheese`, `liquid_milk`, `lithium_ion_battery_material`

**Batch 110 (15):** `relay`, `low_voltage_electrical`, `contactor`, `automation_equipment`, `electricity_power_generation`, `ice_cream`, `milk_powder`, `electronic_aluminum_foil`, `high_purity_aluminum`, `aluminum_rod`, `formed_foil`, `etched_foil`, `aero_engine`, `airport_operation`, `air_ground_service`
