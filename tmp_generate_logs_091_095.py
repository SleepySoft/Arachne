#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate construction logs for batches 091-095."""

import os

BATCHES = {
    91: {
        "nodes_created": 13,
        "edges_created": 3,
        "companies": 10,
        "exposures": 26,
        "new_nodes": [
            ("tech_park_operation_service", "科技产业园区运营服务", "service"),
            ("automotive_glass", "汽车玻璃", "component"),
            ("taxi_operation_service", "出租汽车运营服务", "service"),
            ("chinese_medicine_preparation", "中药制剂", "material"),
            ("chemical_drug_preparation", "化学药品制剂", "material"),
            ("health_food", "保健食品", "material"),
            ("sapphire_crystal_material", "蓝宝石晶体材料", "material"),
            ("single_crystal_furnace", "单晶炉", "device"),
            ("sapphire_product", "蓝宝石制品", "component"),
            ("semiconductor_backend_service", "半导体后工序服务", "service"),
            ("telecom_cable", "通信电缆", "component"),
            ("printing_material", "印刷材料", "material"),
            ("financial_equipment", "金融设备", "device"),
        ],
        "new_edges": [
            ("float_glass", "automotive_glass", "material_flow", "浮法玻璃经深加工制成汽车玻璃"),
            ("sapphire_crystal_material", "sapphire_product", "material_flow", "蓝宝石晶体材料经加工制成蓝宝石制品"),
            ("single_crystal_furnace", "sapphire_crystal_material", "capability_supply", "单晶炉提供晶体生长能力，产出蓝宝石晶体材料"),
        ],
        "companies_list": [
            ("sh_600658", "电子城", "园区开发"),
            ("sh_600660", "福耀玻璃", "汽车配件"),
            ("sh_600661", "昂立教育", "文教休闲"),
            ("sh_600662", "外服控股", "文教休闲"),
            ("sh_600663", "陆家嘴", "园区开发"),
            ("sh_600664", "哈药股份", "化学制药"),
            ("sh_600665", "天地源", "全国地产"),
            ("sh_600666", "奥瑞德", "元器件"),
            ("sh_600667", "太极实业", "半导体"),
            ("sh_600668", "尖峰集团", "水泥"),
        ],
    },
    92: {
        "nodes_created": 13,
        "edges_created": 1,
        "companies": 10,
        "exposures": 26,
        "new_nodes": [
            ("ophthalmic_eye_drop", "眼科用滴眼液", "material"),
            ("chinese_patent_medicine_liquid", "中成药液体制剂", "material"),
            ("hydrophilic_aluminum_foil", "亲水铝箔", "material"),
            ("tungsten_material", "钨材料", "material"),
            ("ferromanganese", "锰铁合金", "material"),
            ("ferrochrome", "铬铁合金", "material"),
            ("smart_property_management", "智能化物业管理服务", "service"),
            ("commercial_housing_rental", "商品房租赁服务", "service"),
            ("water_tourism_service", "水上旅游服务", "service"),
            ("bicycle_part", "自行车零部件", "component"),
            ("gas_appliance", "燃气具", "component"),
            ("domestic_trade_service", "国内贸易服务", "service"),
            ("foreign_trade_service", "外贸进出口服务", "service"),
        ],
        "new_edges": [
            ("cement", "ready_mixed_concrete", "material_flow", "水泥是生产混凝土的主要原料"),
        ],
        "companies_list": [
            ("sh_600671", "天目药业", "中成药"),
            ("sh_600673", "东阳光", "综合类"),
            ("sh_600674", "川投能源", "水力发电"),
            ("sh_600675", "中华企业", "区域地产"),
            ("sh_600676", "交运股份", "汽车配件"),
            ("sh_600678", "ST金顶", "水泥"),
            ("sh_600679", "上海凤凰", "文教休闲"),
            ("sh_600681", "百川能源", "供气供热"),
            ("sh_600682", "南京新百", "生物制药"),
            ("sh_600683", "京投发展", "区域地产"),
        ],
    },
    93: {
        "nodes_created": 18,
        "edges_created": 0,
        "companies": 10,
        "exposures": 41,
        "new_nodes": [
            ("special_vessel", "特种船舶", "system"),
            ("frp_product", "玻璃钢制品", "component"),
            ("marine_furniture", "船舶家具", "component"),
            ("synthetic_fiber", "合成纤维", "material"),
            ("petroleum_product", "石油产品", "material"),
            ("wool_textile", "毛纺织品", "material"),
            ("ammonium_bicarbonate", "碳酸氢铵", "material"),
            ("ammonium_chloride", "氯化铵", "material"),
            ("dimethyl_ether", "二甲醚", "material"),
            ("melamine", "三聚氰胺", "material"),
            ("sodium_nitrate", "硝酸钠", "material"),
            ("sodium_nitrite", "亚硝酸钠", "material"),
            ("m_phenylenediamine", "间苯二胺", "material"),
            ("n_butylaldehyde", "正丁醛", "material"),
            ("isobutylaldehyde", "异丁醛", "material"),
            ("octanol", "辛醇", "material"),
            ("cyclohexanone", "环己酮", "material"),
            ("inland_river_ferry", "内河客滚运输服务", "service"),
            ("coastal_chemical_transport", "沿海化工品运输服务", "service"),
        ],
        "new_edges": [],
        "companies_list": [
            ("sh_600684", "珠江股份", "区域地产"),
            ("sh_600685", "中船防务", "船舶"),
            ("sh_600686", "金龙汽车", "汽车整车"),
            ("sh_600688", "上海石化", "石油加工"),
            ("sh_600689", "上海三毛", "综合类"),
            ("sh_600690", "海尔智家", "家用电器"),
            ("sh_600691", "潞化科技", "农药化肥"),
            ("sh_600692", "亚通股份", "区域地产"),
            ("sh_600693", "东百集团", "百货"),
            ("sh_600694", "大商股份", "百货"),
        ],
    },
    94: {
        "nodes_created": 10,
        "edges_created": 0,
        "companies": 10,
        "exposures": 22,
        "new_nodes": [
            ("turbocharger", "涡轮增压器", "component"),
            ("engine_valve", "发动机进排气门", "component"),
            ("engine_cooling_fan", "发动机冷却风扇", "component"),
            ("led_epitaxial_wafer", "LED外延片", "material"),
            ("led_chip", "LED芯片", "component"),
            ("scenic_area_operation_service", "景区运营管理服务", "service"),
            ("travel_agency_service", "旅行社服务", "service"),
            ("performance_service", "演出演艺服务", "service"),
            ("cultural_tourism_product", "文化旅游商品", "material"),
            ("lcd_substrate_glass", "液晶基板玻璃", "material"),
        ],
        "new_edges": [],
        "companies_list": [
            ("sh_600696", "*ST岩石", "白酒"),
            ("sh_600697", "欧亚集团", "百货"),
            ("sh_600698", "湖南天雁", "汽车配件"),
            ("sh_600699", "均胜电子", "汽车配件"),
            ("sh_600702", "舍得酒业", "白酒"),
            ("sh_600703", "三安光电", "半导体"),
            ("sh_600704", "物产中大", "仓储物流"),
            ("sh_600706", "曲江文旅", "旅游景点"),
            ("sh_600707", "彩虹股份", "元器件"),
            ("sh_600708", "光明地产", "全国地产"),
        ],
    },
    95: {
        "nodes_created": 10,
        "edges_created": 1,
        "companies": 10,
        "exposures": 25,
        "new_nodes": [
            ("diesel_generator_set", "柴油发电机组", "system"),
            ("outdoor_power_equipment", "户外动力设备", "system"),
            ("pv_product", "光伏产品", "material"),
            ("nonferrous_mining_service", "有色金属采选服务", "service"),
            ("metal_financial_service", "金属金融服务", "service"),
            ("pharmaceutical_manufacturing", "医药制造服务", "service"),
            ("strontium_compound", "锶化合物", "material"),
            ("automotive_body_part", "汽车车身零部件", "component"),
            ("digital_medical_system", "数字医疗系统", "system"),
            ("heat_supply", "热力供应服务", "service"),
            ("container_transport_service", "集装箱运输服务", "service"),
        ],
        "new_edges": [
            ("diesel_generator_set", "ship", "composition", "柴油发电机组可作为船舶辅助发电设备"),
        ],
        "companies_list": [
            ("sh_600710", "苏美达", "商贸代理"),
            ("sh_600711", "盛屯矿业", "小金属"),
            ("sh_600712", "南宁百货", "百货"),
            ("sh_600713", "南京医药", "医药商业"),
            ("sh_600714", "金瑞矿业", "化工原料"),
            ("sh_600715", "文投控股", "影视音像"),
            ("sh_600716", "凤凰股份", "区域地产"),
            ("sh_600717", "天津港", "港口"),
            ("sh_600718", "东软集团", "软件服务"),
            ("sh_600719", "大连热电", "供气供热"),
        ],
    },
}

LOG_TEMPLATE = """# Batch {batch_num:03d} Construction Log

## Overview

- **Batch Number**: {batch_num:03d}
- **Companies**: 10
- **New Industrial Nodes**: {nodes_created}
- **New Industrial Edges**: {edges_created}
- **New Company-Node Exposures**: {exposures}
- **Submission Time**: 2026-05-25

## Graph Changes

### New Nodes ({nodes_created})

| node_id | canonical_name_zh | entity_type |
|---|---|---|
{nodes_table}

### New Edges ({edges_created})

| source | target | edge_type | description |
|---|---|---|---|
{edges_table}

## Companies Submitted

| company_id | name_zh | industry |
|---|---|---|
{companies_table}

## Notes

- All nodes and edges validated against schema constraints.
- Evidence attached to each node/edge from company business descriptions.
- Company IDs use `sh_` prefix with numeric stock code (schema-compliant snake_case).
- Exposures map companies to industrial nodes with activity type and weight.
"""


def generate_log(batch_num, data):
    nodes_table = "\n".join(
        f"| {nid} | {name} | {etype} |"
        for nid, name, etype in data["new_nodes"]
    )
    if data["new_edges"]:
        edges_table = "\n".join(
            f"| {src} | {tgt} | {etype} | {desc} |"
            for src, tgt, etype, desc in data["new_edges"]
        )
    else:
        edges_table = "| — | — | — | No new edges in this batch |"
    companies_table = "\n".join(
        f"| {cid} | {name} | {ind} |"
        for cid, name, ind in data["companies_list"]
    )

    content = LOG_TEMPLATE.format(
        batch_num=batch_num,
        nodes_created=data["nodes_created"],
        edges_created=data["edges_created"],
        exposures=data["exposures"],
        nodes_table=nodes_table,
        edges_table=edges_table,
        companies_table=companies_table,
    )
    path = f"docs/batch_{batch_num:03d}_construction_log.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {path}")


def main():
    for batch_num in range(91, 96):
        generate_log(batch_num, BATCHES[batch_num])
    print("All 5 construction logs generated.")


if __name__ == "__main__":
    main()
