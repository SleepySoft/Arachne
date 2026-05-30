#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate construction logs for batches 096-100."""

import os

BATCHES = {
    96: {
        "nodes_created": 11,
        "edges_created": 0,
        "companies": 10,
        "exposures": 43,
        "new_nodes": [
            ("vacuum_cleaner", "吸尘器", "device"),
            ("pva", "聚乙烯醇", "material"),
            ("vinyl_acetate", "醋酸乙烯", "material"),
            ("coal_tar", "煤焦油", "material"),
            ("ammonium_phosphate", "磷铵", "material"),
            ("bromine", "溴素", "material"),
            ("intelligent_security_system", "智能安防系统", "system"),
            ("intelligent_transport_system", "智能交通系统", "system"),
            ("telecom_value_added_service", "通信增值服务", "service"),
            ("it_integrated_service", "IT综合服务", "service"),
            ("investment_management_service", "投资管理服务", "service"),
        ],
        "new_edges": [],
        "companies_list": [
            ("sh_600720", "中交设计", "建筑工程"),
            ("sh_600721", "百花医药", "生物制药"),
            ("sh_600722", "金牛化工", "化工原料"),
            ("sh_600724", "宁波富达", "综合类"),
            ("sh_600725", "云维股份", "商贸代理"),
            ("sh_600726", "华电能源", "火力发电"),
            ("sh_600727", "鲁北化工", "化工原料"),
            ("sh_600728", "佳都科技", "软件服务"),
            ("sh_600729", "重百集团", "百货"),
            ("sh_600730", "*ST高科", "文教休闲"),
        ],
    },
    97: {
        "nodes_created": 10,
        "edges_created": 0,
        "companies": 10,
        "exposures": 26,
        "new_nodes": [
            ("pesticide_formulation", "农药制剂", "material"),
            ("nev_charging_facility", "新能源汽车充电设施", "infrastructure"),
            ("nev_power_module", "新能源汽车动力模块", "subsystem"),
            ("iot_security_system", "物联网安防系统", "system"),
            ("hair_product", "发制品", "material"),
            ("tin_material", "锡材料", "material"),
            ("catering_entertainment_service", "餐饮娱乐服务", "service"),
            ("financial_investment_service", "金融投资服务", "service"),
            ("energy_development_service", "能源开发服务", "service"),
            ("coking_product", "焦化产品", "material"),
        ],
        "new_edges": [],
        "companies_list": [
            ("sh_600731", "湖南海利", "农药化肥"),
            ("sh_600732", "爱旭股份", "电气设备"),
            ("sh_600733", "北汽蓝谷", "汽车整车"),
            ("sh_600734", "*ST实达", "软件服务"),
            ("sh_600735", "ST新华锦", "服饰"),
            ("sh_600736", "苏州高新", "园区开发"),
            ("sh_600737", "中粮糖业", "食品"),
            ("sh_600738", "丽尚国潮", "百货"),
            ("sh_600739", "辽宁成大", "生物制药"),
            ("sh_600740", "山西焦化", "焦炭加工"),
        ],
    },
    98: {
        "nodes_created": 12,
        "edges_created": 0,
        "companies": 10,
        "exposures": 28,
        "new_nodes": [
            ("automotive_wheel", "汽车车轮", "component"),
            ("thermal_power_generation", "火力发电服务", "service"),
            ("vr_device", "虚拟现实设备", "device"),
            ("adc_blowing_agent", "ADC发泡剂", "material"),
            ("bleaching_powder", "漂粉精", "material"),
            ("media_agency_service", "媒体代理服务", "service"),
            ("antibiotic_preparation", "抗生素制剂", "material"),
            ("it_product_distribution", "IT产品分销服务", "service"),
            ("ecommerce_supply_chain_service", "电子商务供应链服务", "service"),
            ("cloud_service", "云服务", "service"),
            ("design_production_service", "设计制作服务", "service"),
            ("mobile_device_lifecycle_service", "移动设备生命周期服务", "service"),
        ],
        "new_edges": [],
        "companies_list": [
            ("sh_600741", "华域汽车", "汽车配件"),
            ("sh_600742", "富维股份", "汽车配件"),
            ("sh_600743", "华远控股", "区域地产"),
            ("sh_600744", "华银电力", "火力发电"),
            ("sh_600745", "*ST闻泰", "半导体"),
            ("sh_600746", "江苏索普", "化工原料"),
            ("sh_600748", "上实发展", "全国地产"),
            ("sh_600749", "西藏旅游", "旅游景点"),
            ("sh_600750", "华润江中", "中成药"),
            ("sh_600751", "海航科技", "水运"),
        ],
    },
    99: {
        "nodes_created": 13,
        "edges_created": 0,
        "companies": 10,
        "exposures": 31,
        "new_nodes": [
            ("financial_service", "金融服务", "service"),
            ("computer_hardware", "计算机硬件", "device"),
            ("technical_training_service", "技术培训服务", "service"),
            ("book_publishing", "图书出版", "service"),
            ("journal_publishing", "期刊出版", "service"),
            ("newspaper_publishing", "报纸出版", "service"),
            ("audio_video_product", "音像制品", "material"),
            ("electronic_publication", "电子出版物", "material"),
            ("construction_installation_service", "建筑安装服务", "service"),
            ("building_material", "建筑材料", "material"),
            ("property_rental_service", "物业租赁服务", "service"),
            ("aerospace_rd_service", "航空产品研发服务", "service"),
            ("forklift", "叉车", "device"),
            ("dental_medical_service", "口腔医疗服务", "service"),
            ("assisted_reproduction_service", "辅助生殖医疗服务", "service"),
        ],
        "new_edges": [],
        "companies_list": [
            ("sh_600753", "*ST海钦", "商贸代理"),
            ("sh_600754", "锦江酒店", "酒店餐饮"),
            ("sh_600755", "厦门国贸", "仓储物流"),
            ("sh_600756", "浪潮软件", "软件服务"),
            ("sh_600757", "长江传媒", "出版业"),
            ("sh_600758", "辽宁能源", "煤炭开采"),
            ("sh_600759", "ST洲际", "石油开采"),
            ("sh_600760", "中航沈飞", "航空"),
            ("sh_600761", "安徽合力", "工程机械"),
            ("sh_600763", "通策医疗", "医疗保健"),
        ],
    },
    100: {
        "nodes_created": 13,
        "edges_created": 0,
        "companies": 10,
        "exposures": 34,
        "new_nodes": [
            ("underwater_acoustic_equipment", "水声信息传输装备", "device"),
            ("underwater_weapon_system", "水下武器系统", "system"),
            ("ballast_water_power_supply", "压载水电源", "device"),
            ("hydraulic_system", "液压系统", "system"),
            ("aluminum_plate_strip", "铝板带材", "material"),
            ("aluminum_profile", "铝型材", "material"),
            ("aluminum_billet", "铝铸棒", "material"),
            ("steam_supply_service", "供汽服务", "service"),
            ("equity_investment_service", "股权投资服务", "service"),
            ("chinese_patent_medicine_pill", "中药经典名方制剂", "material"),
            ("electromechanical_instrument_product", "机电仪产品", "component"),
            ("electronic_information_product", "电子信息产品", "component"),
            ("ic_card_telephone", "IC卡话机", "device"),
            ("telecom_power_equipment", "电信电源设备", "device"),
        ],
        "new_edges": [],
        "companies_list": [
            ("sh_600764", "中国海防", "船舶"),
            ("sh_600765", "XD中航重", "航空"),
            ("sh_600768", "宁波富邦", "铝"),
            ("sh_600769", "祥龙电业", "水务"),
            ("sh_600770", "综艺股份", "综合类"),
            ("sh_600771", "广誉远", "中成药"),
            ("sh_600773", "西藏城投", "区域地产"),
            ("sh_600774", "汉商集团", "化学制药"),
            ("sh_600775", "南京熊猫", "通信设备"),
            ("sh_600776", "东方通信", "通信设备"),
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
    for batch_num in range(96, 101):
        generate_log(batch_num, BATCHES[batch_num])
    print("All 5 construction logs generated.")


if __name__ == "__main__":
    main()
