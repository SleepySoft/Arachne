#!/usr/bin/env python3
"""Submit batch 082 to Arachne API."""
import json, requests
from datetime import datetime

BASE = "http://localhost:8005/api/v1"

def api_post(path, payload):
    r = requests.post(f"{BASE}/{path}", json=payload, timeout=30)
    return r.status_code, r.text if r.status_code not in (200, 201) else r.json()

def make_evidence(quote, source_title="Tushare数据"):
    return [{
        "source_title": source_title,
        "quote": quote,
        "source_reference": "tushare",
        "confidence": "HIGH",
        "recorded_at": datetime.now().isoformat()
    }]

NEW_NODES = [
    {
        "node_id": "transformer",
        "canonical_name_zh": "变压器",
        "definition": "利用电磁感应原理改变交流电压的静止电气设备，是输配电系统的核心装备",
        "entity_type": "device"
    },
    {
        "node_id": "tft_lcd_module",
        "canonical_name_zh": "TFT液晶显示模组",
        "definition": "采用薄膜晶体管技术驱动的液晶显示面板模组，用于各类电子设备的图像显示",
        "entity_type": "component"
    },
    {
        "node_id": "touch_screen_module",
        "canonical_name_zh": "触摸屏模组",
        "definition": "集成了触控感应和显示功能的模组，可实现人机交互操作",
        "entity_type": "component"
    },
    {
        "node_id": "smart_city",
        "canonical_name_zh": "智慧城市",
        "definition": "利用物联网、云计算和大数据技术实现城市管理和服务的智能化系统",
        "entity_type": "service"
    },
    {
        "node_id": "welding_electrode",
        "canonical_name_zh": "焊条",
        "definition": "涂有药皮的熔化电极，用于手工电弧焊的焊接材料",
        "entity_type": "material"
    },
    {
        "node_id": "electric_drive",
        "canonical_name_zh": "电气传动装置",
        "definition": "将电能转换为机械能驱动负载运行的电气控制系统，包括变频器、电机等",
        "entity_type": "system"
    },
    {
        "node_id": "power_semiconductor_component",
        "canonical_name_zh": "电力半导体元器件",
        "definition": "用于电力电子变换和控制的大功率半导体器件，如晶闸管、IGBT等",
        "entity_type": "component"
    },
    {
        "node_id": "microwave_product",
        "canonical_name_zh": "微波产品",
        "definition": "利用微波频段电磁波进行信号传输和处理的产品，用于通信、雷达等领域",
        "entity_type": "component"
    }
]

NEW_EDGES = [
    {
        "edge_id": "transformer_to_power_grid",
        "from_node": "transformer",
        "to_node": "power_grid",
        "edge_type": "composition",
        "description": "变压器是电力输配电系统中实现电压变换的核心设备"
    },
    {
        "edge_id": "tft_lcd_module_to_display_panel",
        "from_node": "tft_lcd_module",
        "to_node": "display_panel",
        "edge_type": "composition",
        "description": "TFT液晶显示模组是各类显示终端设备的核心显示部件"
    },
    {
        "edge_id": "welding_electrode_to_steel_structure",
        "from_node": "welding_electrode",
        "to_node": "steel_structure",
        "edge_type": "material_flow",
        "description": "焊条是钢结构建筑和制造中连接钢材的消耗材料"
    }
]

COMPANIES = [
    {
        "company_id": "baobian_elec",
        "name_zh": "保定天威保变电气股份有限公司",
        "stock_code": "600550.SH",
        "province": "河北",
        "city": "保定市",
        "industry": "电气设备",
        "main_business": "变压器,互感器,太阳能电池组件,吊装带"
    },
    {
        "company_id": "times_publishing",
        "name_zh": "时代出版传媒股份有限公司",
        "stock_code": "600551.SH",
        "province": "安徽",
        "city": "合肥市",
        "industry": "出版业",
        "main_business": "图书,期刊,全媒体出版策划经营及印刷复制,传媒科技研发,股权投资"
    },
    {
        "company_id": "kaisheng_tech",
        "name_zh": "凯盛科技股份有限公司",
        "stock_code": "600552.SH",
        "province": "安徽",
        "city": "蚌埠市",
        "industry": "元器件",
        "main_business": "TFT液晶显示模组,触摸屏模组,TFT玻璃减薄,ITO导电膜玻璃,柔性ITO导电膜"
    },
    {
        "company_id": "tianxiaxiu",
        "name_zh": "天下秀数字科技(集团)股份有限公司",
        "stock_code": "600556.SH",
        "province": "广西",
        "city": "北海市",
        "industry": "互联网",
        "main_business": "智慧城市相关业务"
    },
    {
        "company_id": "kangyuan",
        "name_zh": "江苏康缘药业股份有限公司",
        "stock_code": "600557.SH",
        "province": "江苏",
        "city": "连云港市",
        "industry": "中成药",
        "main_business": "胶囊,口服液,冲剂片,丸剂"
    },
    {
        "company_id": "atlantic",
        "name_zh": "四川大西洋焊接材料股份有限公司",
        "stock_code": "600558.SH",
        "province": "四川",
        "city": "自贡市",
        "industry": "钢加工",
        "main_business": "焊条,焊丝"
    },
    {
        "company_id": "laobaigan",
        "name_zh": "河北衡水老白干酒业股份有限公司",
        "stock_code": "600559.SH",
        "province": "河北",
        "city": "衡水市",
        "industry": "白酒",
        "main_business": "白酒,商品猪,种猪,饲料"
    },
    {
        "company_id": "aritime",
        "name_zh": "北京金自天正智能控制股份有限公司",
        "stock_code": "600560.SH",
        "province": "北京",
        "city": "北京市",
        "industry": "电气设备",
        "main_business": "电气传动装置,工业计算机控制系统,工业专用检测及控制仪表,电力半导体元器件"
    },
    {
        "company_id": "jiangxi_changyun",
        "name_zh": "江西长运股份有限公司",
        "stock_code": "600561.SH",
        "province": "江西",
        "city": "南昌市",
        "industry": "公共交通",
        "main_business": "公路旅客运输,旅游服务,车辆租赁"
    },
    {
        "company_id": "guorui",
        "name_zh": "国睿科技股份有限公司",
        "stock_code": "600562.SH",
        "province": "江苏",
        "city": "南京市",
        "industry": "通信设备",
        "main_business": "微波与信息技术相关产品的生产和销售"
    }
]

EXPOSURES = [
    {
        "exposure_id": "baobian_elec_manufacture_transformer",
        "company_id": "baobian_elec",
        "node_id": "transformer",
        "activity_type": "manufacture",
        "role": "变压器制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "baobian_elec_manufacture_current_transformer",
        "company_id": "baobian_elec",
        "node_id": "current_transformer",
        "activity_type": "manufacture",
        "role": "互感器制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "baobian_elec_produce_solar_cell",
        "company_id": "baobian_elec",
        "node_id": "solar_cell",
        "activity_type": "produce",
        "role": "太阳能电池组件生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "times_publishing_operate_book_publishing",
        "company_id": "times_publishing",
        "node_id": "book_publishing",
        "activity_type": "operate",
        "role": "图书出版运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "times_publishing_operate_journal_publishing",
        "company_id": "times_publishing",
        "node_id": "journal_publishing",
        "activity_type": "operate",
        "role": "期刊出版运营商",
        "weight": 0.9
    },
    {
        "exposure_id": "times_publishing_provide_service_printing_service",
        "company_id": "times_publishing",
        "node_id": "printing_service",
        "activity_type": "provide_service",
        "role": "印刷复制服务商",
        "weight": 0.85
    },
    {
        "exposure_id": "kaisheng_tech_manufacture_tft_lcd_module",
        "company_id": "kaisheng_tech",
        "node_id": "tft_lcd_module",
        "activity_type": "manufacture",
        "role": "TFT液晶显示模组制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "kaisheng_tech_manufacture_touch_screen_module",
        "company_id": "kaisheng_tech",
        "node_id": "touch_screen_module",
        "activity_type": "manufacture",
        "role": "触摸屏模组制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "kaisheng_tech_manufacture_ito_conductive_glass",
        "company_id": "kaisheng_tech",
        "node_id": "ito_conductive_glass",
        "activity_type": "manufacture",
        "role": "ITO导电膜玻璃制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "tianxiaxiu_provide_service_smart_city",
        "company_id": "tianxiaxiu",
        "node_id": "smart_city",
        "activity_type": "provide_service",
        "role": "智慧城市服务商",
        "weight": 0.95
    },
    {
        "exposure_id": "tianxiaxiu_provide_service_software",
        "company_id": "tianxiaxiu",
        "node_id": "software",
        "activity_type": "provide_service",
        "role": "软件服务商",
        "weight": 0.85
    },
    {
        "exposure_id": "kangyuan_produce_chinese_patent_medicine",
        "company_id": "kangyuan",
        "node_id": "chinese_patent_medicine",
        "activity_type": "produce",
        "role": "中成药生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "kangyuan_produce_pharmaceutical",
        "company_id": "kangyuan",
        "node_id": "pharmaceutical",
        "activity_type": "produce",
        "role": "药品生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "atlantic_produce_welding_electrode",
        "company_id": "atlantic",
        "node_id": "welding_electrode",
        "activity_type": "produce",
        "role": "焊条生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "atlantic_produce_welding_wire",
        "company_id": "atlantic",
        "node_id": "welding_wire",
        "activity_type": "produce",
        "role": "焊丝生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "atlantic_produce_welding_material",
        "company_id": "atlantic",
        "node_id": "welding_material",
        "activity_type": "produce",
        "role": "焊接材料生产商",
        "weight": 0.9
    },
    {
        "exposure_id": "laobaigan_produce_liquor",
        "company_id": "laobaigan",
        "node_id": "liquor",
        "activity_type": "produce",
        "role": "白酒生产商",
        "weight": 0.95
    },
    {
        "exposure_id": "laobaigan_produce_pig",
        "company_id": "laobaigan",
        "node_id": "pig",
        "activity_type": "produce",
        "role": "商品猪生产商",
        "weight": 0.85
    },
    {
        "exposure_id": "laobaigan_produce_feed",
        "company_id": "laobaigan",
        "node_id": "feed",
        "activity_type": "produce",
        "role": "饲料生产商",
        "weight": 0.8
    },
    {
        "exposure_id": "aritime_manufacture_electric_drive",
        "company_id": "aritime",
        "node_id": "electric_drive",
        "activity_type": "manufacture",
        "role": "电气传动装置制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "aritime_manufacture_industrial_control_system",
        "company_id": "aritime",
        "node_id": "industrial_control_system",
        "activity_type": "manufacture",
        "role": "工业计算机控制系统制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "aritime_manufacture_power_semiconductor_component",
        "company_id": "aritime",
        "node_id": "power_semiconductor_component",
        "activity_type": "manufacture",
        "role": "电力半导体元器件制造商",
        "weight": 0.9
    },
    {
        "exposure_id": "jiangxi_changyun_operate_passenger_transport",
        "company_id": "jiangxi_changyun",
        "node_id": "passenger_transport",
        "activity_type": "operate",
        "role": "公路旅客运输运营商",
        "weight": 0.95
    },
    {
        "exposure_id": "jiangxi_changyun_provide_service_tourism_service",
        "company_id": "jiangxi_changyun",
        "node_id": "tourism_service",
        "activity_type": "provide_service",
        "role": "旅游服务商",
        "weight": 0.85
    },
    {
        "exposure_id": "jiangxi_changyun_operate_vehicle_rental",
        "company_id": "jiangxi_changyun",
        "node_id": "vehicle_rental",
        "activity_type": "operate",
        "role": "车辆租赁运营商",
        "weight": 0.8
    },
    {
        "exposure_id": "guorui_manufacture_microwave_product",
        "company_id": "guorui",
        "node_id": "microwave_product",
        "activity_type": "manufacture",
        "role": "微波产品制造商",
        "weight": 0.95
    },
    {
        "exposure_id": "guorui_manufacture_communication_equipment",
        "company_id": "guorui",
        "node_id": "communication_equipment",
        "activity_type": "manufacture",
        "role": "通信设备制造商",
        "weight": 0.9
    }
]

def build_graph_batch():
    nodes_to_upsert = []
    for n in NEW_NODES:
        nodes_to_upsert.append({
            "node_id": n["node_id"],
            "canonical_name_zh": n["canonical_name_zh"],
            "canonical_name_en": n.get("canonical_name_en"),
            "definition": n["definition"],
            "entity_type": n["entity_type"],
            "confidence": "HIGH",
            "status": "ACTIVE",
            "evidence": make_evidence(f"tushare batch 082: " + n["canonical_name_zh"]),
        })
    edges_to_upsert = []
    for e in NEW_EDGES:
        edges_to_upsert.append({
            "edge_id": e["edge_id"],
            "from_node": e["from_node"],
            "to_node": e["to_node"],
            "edge_namespace": "industrial_flow",
            "edge_type": e["edge_type"],
            "description": e["description"],
            "confidence": "HIGH",
            "evidence": make_evidence(f"tushare batch 082: " + e["description"]),
        })
    return {
        "batch_id": "batch_082",
        "task_description": "Batch 082: industrial nodes and edges",
        "nodes_to_upsert": nodes_to_upsert,
        "edges_to_upsert": edges_to_upsert,
    }

def build_business_batch():
    companies_to_upsert = []
    for c in COMPANIES:
        companies_to_upsert.append({
            "company_id": c["company_id"],
            "name_zh": c["name_zh"],
            "name_en": c.get("name_en"),
            "stock_codes": [c["stock_code"]],
            "country": "CN",
            "province": c["province"],
            "city": c["city"],
            "industry": c["industry"],
            "main_business": c["main_business"],
            "company_type": "public",
            "status": "ACTIVE",
            "evidence": make_evidence("tushare: " + c["main_business"]),
        })
    exposures_to_upsert = []
    for exp in EXPOSURES:
        exposures_to_upsert.append({
            "exposure_id": exp["exposure_id"],
            "company_id": exp["company_id"],
            "node_id": exp["node_id"],
            "activity_type": exp["activity_type"],
            "role": exp["role"],
            "weight": exp["weight"],
            "confidence": "HIGH",
            "status": "ACTIVE",
            "evidence": make_evidence(f"tushare batch 082: " + exp["company_id"] + " -> " + exp["node_id"]),
        })
    return {
        "batch_id": "batch_082",
        "task_description": "Batch 082: companies and exposures",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch 082 Submission")
    print("=" * 60)
    graph_batch = build_graph_batch()
    print(f"\nGraph batch: {len(graph_batch['nodes_to_upsert'])} nodes, {len(graph_batch['edges_to_upsert'])} edges")
    if graph_batch["nodes_to_upsert"] or graph_batch["edges_to_upsert"]:
        status, resp = api_post("batches", graph_batch)
        print(f"Graph batch response: {status}")
        if status not in (200, 201):
            print(f"  ERROR: {resp}")
    else:
        print("Graph batch: nothing to submit")
    biz_batch = build_business_batch()
    print(f"\nBusiness batch: {len(biz_batch['companies_to_upsert'])} companies, {len(biz_batch['company_node_exposures_to_upsert'])} exposures")
    status, resp = api_post("business-batches", biz_batch)
    print(f"Business batch response: {status}")
    if status not in (200, 201):
        print(f"  ERROR: {resp}")
    print("\nDone.")
