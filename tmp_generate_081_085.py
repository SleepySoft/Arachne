#!/usr/bin/env python3
"""Generate tmp_submit_batch_081.py through tmp_submit_batch_085.py."""
import json, os

TEMPLATE = '''#!/usr/bin/env python3
"""Submit batch %%NNN%% to Arachne API."""
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

NEW_NODES = %%NEW_NODES%%

NEW_EDGES = %%NEW_EDGES%%

COMPANIES = %%COMPANIES%%

EXPOSURES = %%EXPOSURES%%

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
            "evidence": make_evidence(f"tushare batch %%NNN%%: " + n["canonical_name_zh"]),
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
            "evidence": make_evidence(f"tushare batch %%NNN%%: " + e["description"]),
        })
    return {
        "batch_id": "batch_%%NNN%%",
        "task_description": "Batch %%NNN%%: industrial nodes and edges",
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
            "evidence": make_evidence(f"tushare batch %%NNN%%: " + exp["company_id"] + " -> " + exp["node_id"]),
        })
    return {
        "batch_id": "batch_%%NNN%%",
        "task_description": "Batch %%NNN%%: companies and exposures",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": companies_to_upsert,
        "company_node_exposures_to_upsert": exposures_to_upsert,
    }

if __name__ == "__main__":
    print("=" * 60)
    print("Batch %%NNN%% Submission")
    print("=" * 60)
    graph_batch = build_graph_batch()
    print(f"\\nGraph batch: {len(graph_batch['nodes_to_upsert'])} nodes, {len(graph_batch['edges_to_upsert'])} edges")
    if graph_batch["nodes_to_upsert"] or graph_batch["edges_to_upsert"]:
        status, resp = api_post("batches", graph_batch)
        print(f"Graph batch response: {status}")
        if status not in (200, 201):
            print(f"  ERROR: {resp}")
    else:
        print("Graph batch: nothing to submit")
    biz_batch = build_business_batch()
    print(f"\\nBusiness batch: {len(biz_batch['companies_to_upsert'])} companies, {len(biz_batch['company_node_exposures_to_upsert'])} exposures")
    status, resp = api_post("business-batches", biz_batch)
    print(f"Business batch response: {status}")
    if status not in (200, 201):
        print(f"  ERROR: {resp}")
    print("\\nDone.")
'''

BATCH_081 = {
    "new_nodes": [
        {"node_id": "silicon_ingot", "canonical_name_zh": "硅棒", "definition": "通过提拉法或浇铸法生长的圆柱形高纯度硅晶体，是制造太阳能电池和半导体芯片的基础材料", "entity_type": "material"},
        {"node_id": "water_purifier_faucet", "canonical_name_zh": "净水龙头", "definition": "集成了过滤净化功能的龙头设备，用于家庭或商业场所的饮用水净化", "entity_type": "device"},
        {"node_id": "cotton_seed", "canonical_name_zh": "棉种", "definition": "用于棉花种植的优良种子，是棉花农业生产的基础投入品", "entity_type": "material"},
        {"node_id": "malt", "canonical_name_zh": "大麦芽", "definition": "大麦经浸麦、发芽、烘干等工序制成的产品，主要用于啤酒酿造和食品工业", "entity_type": "material"},
        {"node_id": "intelligent_textile_equipment", "canonical_name_zh": "智能化纺织成套设备", "definition": "采用自动化和智能化技术实现纺纱、织造、染整等工序的成套纺织机械设备", "entity_type": "system"},
        {"node_id": "tungsten_concentrate", "canonical_name_zh": "钨精矿", "definition": "钨矿石经选矿富集后得到的高品位钨矿物产品，是钨冶炼的初始原料", "entity_type": "material"},
        {"node_id": "cemented_carbide", "canonical_name_zh": "硬质合金", "definition": "以碳化钨为硬质相、钴为粘结相烧结制成的高硬度耐磨材料，用于切削工具和耐磨零件", "entity_type": "material"},
        {"node_id": "gold_jewelry", "canonical_name_zh": "黄金珠宝饰品", "definition": "以黄金为主要材质制作的珠宝首饰和装饰品", "entity_type": "material"},
    ],
    "new_edges": [
        {"edge_id": "silicon_ingot_to_solar_cell", "from_node": "silicon_ingot", "to_node": "solar_cell", "edge_type": "material_flow", "description": "硅棒是制造晶体硅太阳能电池的核心原材料"},
        {"edge_id": "tungsten_concentrate_to_cemented_carbide", "from_node": "tungsten_concentrate", "to_node": "cemented_carbide", "edge_type": "material_flow", "description": "钨精矿经冶炼加工后制成硬质合金产品"},
        {"edge_id": "cemented_carbide_to_cutting_tool", "from_node": "cemented_carbide", "to_node": "cutting_tool", "edge_type": "material_flow", "description": "硬质合金是制造切削刀具的主要材料"},
    ],
    "companies": [
        {"company_id": "st_yijing", "name_zh": "亿晶光电科技股份有限公司", "stock_code": "600537.SH", "province": "江苏", "city": "常州市", "industry": "电气设备", "main_business": "晶体硅太阳能电池片和电池组件的生产和销售以及光伏发电业务"},
        {"company_id": "guofa", "name_zh": "北海国发川山生物股份有限公司", "stock_code": "600538.SH", "province": "广西", "city": "北海市", "industry": "医药商业", "main_business": "医药制造及医药流通产业,农药产业,酒店和环保"},
        {"company_id": "shitou", "name_zh": "太原狮头水泥股份有限公司", "stock_code": "600539.SH", "province": "山西", "city": "太原市", "industry": "互联网", "main_business": "净水龙头及配件的生产与销售,污水处理项目工程,河道治理等水技术,环保技术"},
        {"company_id": "xinsai", "name_zh": "新疆赛里木现代农业股份有限公司", "stock_code": "600540.SH", "province": "新疆", "city": "博尔塔拉", "industry": "种植业", "main_business": "棉花,棉种"},
        {"company_id": "st_mogao", "name_zh": "甘肃莫高实业发展股份有限公司", "stock_code": "600543.SH", "province": "甘肃", "city": "兰州市", "industry": "红黄酒", "main_business": "大麦芽,葡萄及葡萄酒,甘草系列产品"},
        {"company_id": "saurer", "name_zh": "卓郎智能技术股份有限公司", "stock_code": "600545.SH", "province": "新疆", "city": "乌鲁木齐市", "industry": "纺织机械", "main_business": "智能化纺织成套设备及核心零部件的研发,生产和销售"},
        {"company_id": "shanmei_intl", "name_zh": "山煤国际能源集团股份有限公司", "stock_code": "600546.SH", "province": "山西", "city": "太原市", "industry": "煤炭开采", "main_business": "煤炭开采与煤炭贸易业务"},
        {"company_id": "shandong_gold", "name_zh": "山东黄金矿业股份有限公司", "stock_code": "600547.SH", "province": "山东", "city": "济南市", "industry": "黄金", "main_business": "黄金开采,黄金珠宝饰品"},
        {"company_id": "shenzhen_expressway", "name_zh": "深圳高速公路集团股份有限公司", "stock_code": "600548.SH", "province": "广东", "city": "深圳市", "industry": "路桥", "main_business": "经营梅观高速,机荷高速,盐坝高速,水官高速以及长沙环路和湖北隔蒲潭大桥"},
        {"company_id": "xiamen_tungsten", "name_zh": "厦门钨业股份有限公司", "stock_code": "600549.SH", "province": "福建", "city": "厦门市", "industry": "小金属", "main_business": "钨精矿,钨钼中间制品,粉末产品,丝材板材,硬质合金,切削刀具,各种稀土氧化物,稀土金属,稀土发光材料,磁性材料,贮氢合金粉,锂电池"},
    ],
    "exposures": [
        {"exposure_id": "st_yijing_produce_silicon_ingot", "company_id": "st_yijing", "node_id": "silicon_ingot", "activity_type": "produce", "role": "硅棒生产商", "weight": 0.95},
        {"exposure_id": "st_yijing_produce_solar_cell", "company_id": "st_yijing", "node_id": "solar_cell", "activity_type": "produce", "role": "太阳能电池片生产商", "weight": 0.95},
        {"exposure_id": "st_yijing_produce_photovoltaic", "company_id": "st_yijing", "node_id": "photovoltaic", "activity_type": "produce", "role": "光伏组件生产商", "weight": 0.9},
        {"exposure_id": "guofa_produce_pesticide", "company_id": "guofa", "node_id": "pesticide", "activity_type": "produce", "role": "农药生产商", "weight": 0.95},
        {"exposure_id": "guofa_produce_pharmaceutical", "company_id": "guofa", "node_id": "pharmaceutical", "activity_type": "produce", "role": "药品生产商", "weight": 0.9},
        {"exposure_id": "guofa_operate_hotel_service", "company_id": "guofa", "node_id": "hotel_service", "activity_type": "operate", "role": "酒店服务商", "weight": 0.8},
        {"exposure_id": "shitou_manufacture_water_purifier_faucet", "company_id": "shitou", "node_id": "water_purifier_faucet", "activity_type": "manufacture", "role": "净水龙头制造商", "weight": 0.95},
        {"exposure_id": "shitou_operate_water_treatment", "company_id": "shitou", "node_id": "water_treatment", "activity_type": "operate", "role": "污水处理运营商", "weight": 0.9},
        {"exposure_id": "xinsai_produce_cotton", "company_id": "xinsai", "node_id": "cotton", "activity_type": "produce", "role": "棉花生产商", "weight": 0.95},
        {"exposure_id": "xinsai_produce_cotton_seed", "company_id": "xinsai", "node_id": "cotton_seed", "activity_type": "produce", "role": "棉种生产商", "weight": 0.9},
        {"exposure_id": "st_mogao_produce_malt", "company_id": "st_mogao", "node_id": "malt", "activity_type": "produce", "role": "大麦芽生产商", "weight": 0.95},
        {"exposure_id": "st_mogao_produce_wine", "company_id": "st_mogao", "node_id": "wine", "activity_type": "produce", "role": "葡萄酒生产商", "weight": 0.9},
        {"exposure_id": "st_mogao_produce_licorice", "company_id": "st_mogao", "node_id": "licorice", "activity_type": "produce", "role": "甘草系列产品生产商", "weight": 0.85},
        {"exposure_id": "saurer_manufacture_intelligent_textile_equipment", "company_id": "saurer", "node_id": "intelligent_textile_equipment", "activity_type": "manufacture", "role": "智能化纺织成套设备制造商", "weight": 0.95},
        {"exposure_id": "saurer_manufacture_textile_machinery", "company_id": "saurer", "node_id": "textile_machinery", "activity_type": "manufacture", "role": "纺织机械制造商", "weight": 0.9},
        {"exposure_id": "shanmei_intl_operate_coal", "company_id": "shanmei_intl", "node_id": "coal", "activity_type": "operate", "role": "煤炭经营商", "weight": 0.95},
        {"exposure_id": "shanmei_intl_operate_coal_mining", "company_id": "shanmei_intl", "node_id": "coal_mining", "activity_type": "operate", "role": "煤炭开采运营商", "weight": 0.9},
        {"exposure_id": "shandong_gold_produce_gold", "company_id": "shandong_gold", "node_id": "gold", "activity_type": "produce", "role": "黄金生产商", "weight": 0.95},
        {"exposure_id": "shandong_gold_produce_gold_jewelry", "company_id": "shandong_gold", "node_id": "gold_jewelry", "activity_type": "produce", "role": "黄金珠宝饰品生产商", "weight": 0.9},
        {"exposure_id": "shenzhen_expressway_operate_expressway", "company_id": "shenzhen_expressway", "node_id": "expressway", "activity_type": "operate", "role": "高速公路运营商", "weight": 0.95},
        {"exposure_id": "shenzhen_expressway_operate_toll_road", "company_id": "shenzhen_expressway", "node_id": "toll_road", "activity_type": "operate", "role": "路桥收费运营商", "weight": 0.9},
        {"exposure_id": "xiamen_tungsten_produce_tungsten_concentrate", "company_id": "xiamen_tungsten", "node_id": "tungsten_concentrate", "activity_type": "produce", "role": "钨精矿生产商", "weight": 0.95},
        {"exposure_id": "xiamen_tungsten_produce_cemented_carbide", "company_id": "xiamen_tungsten", "node_id": "cemented_carbide", "activity_type": "produce", "role": "硬质合金生产商", "weight": 0.95},
        {"exposure_id": "xiamen_tungsten_produce_cutting_tool", "company_id": "xiamen_tungsten", "node_id": "cutting_tool", "activity_type": "produce", "role": "切削刀具生产商", "weight": 0.9},
        {"exposure_id": "xiamen_tungsten_produce_rare_earth_metal", "company_id": "xiamen_tungsten", "node_id": "rare_earth_metal", "activity_type": "produce", "role": "稀土金属生产商", "weight": 0.85},
        {"exposure_id": "xiamen_tungsten_produce_lithium_battery", "company_id": "xiamen_tungsten", "node_id": "lithium_battery", "activity_type": "produce", "role": "锂电池生产商", "weight": 0.85},
    ],
}

BATCH_082 = {
    "new_nodes": [
        {"node_id": "transformer", "canonical_name_zh": "变压器", "definition": "利用电磁感应原理改变交流电压的静止电气设备，是输配电系统的核心装备", "entity_type": "device"},
        {"node_id": "tft_lcd_module", "canonical_name_zh": "TFT液晶显示模组", "definition": "采用薄膜晶体管技术驱动的液晶显示面板模组，用于各类电子设备的图像显示", "entity_type": "component"},
        {"node_id": "touch_screen_module", "canonical_name_zh": "触摸屏模组", "definition": "集成了触控感应和显示功能的模组，可实现人机交互操作", "entity_type": "component"},
        {"node_id": "smart_city", "canonical_name_zh": "智慧城市", "definition": "利用物联网、云计算和大数据技术实现城市管理和服务的智能化系统", "entity_type": "service"},
        {"node_id": "welding_electrode", "canonical_name_zh": "焊条", "definition": "涂有药皮的熔化电极，用于手工电弧焊的焊接材料", "entity_type": "material"},
        {"node_id": "electric_drive", "canonical_name_zh": "电气传动装置", "definition": "将电能转换为机械能驱动负载运行的电气控制系统，包括变频器、电机等", "entity_type": "system"},
        {"node_id": "power_semiconductor_component", "canonical_name_zh": "电力半导体元器件", "definition": "用于电力电子变换和控制的大功率半导体器件，如晶闸管、IGBT等", "entity_type": "component"},
        {"node_id": "microwave_product", "canonical_name_zh": "微波产品", "definition": "利用微波频段电磁波进行信号传输和处理的产品，用于通信、雷达等领域", "entity_type": "component"},
    ],
    "new_edges": [
        {"edge_id": "transformer_to_power_grid", "from_node": "transformer", "to_node": "power_grid", "edge_type": "composition", "description": "变压器是电力输配电系统中实现电压变换的核心设备"},
        {"edge_id": "tft_lcd_module_to_display_panel", "from_node": "tft_lcd_module", "to_node": "display_panel", "edge_type": "composition", "description": "TFT液晶显示模组是各类显示终端设备的核心显示部件"},
        {"edge_id": "welding_electrode_to_steel_structure", "from_node": "welding_electrode", "to_node": "steel_structure", "edge_type": "material_flow", "description": "焊条是钢结构建筑和制造中连接钢材的消耗材料"},
    ],
    "companies": [
        {"company_id": "baobian_elec", "name_zh": "保定天威保变电气股份有限公司", "stock_code": "600550.SH", "province": "河北", "city": "保定市", "industry": "电气设备", "main_business": "变压器,互感器,太阳能电池组件,吊装带"},
        {"company_id": "times_publishing", "name_zh": "时代出版传媒股份有限公司", "stock_code": "600551.SH", "province": "安徽", "city": "合肥市", "industry": "出版业", "main_business": "图书,期刊,全媒体出版策划经营及印刷复制,传媒科技研发,股权投资"},
        {"company_id": "kaisheng_tech", "name_zh": "凯盛科技股份有限公司", "stock_code": "600552.SH", "province": "安徽", "city": "蚌埠市", "industry": "元器件", "main_business": "TFT液晶显示模组,触摸屏模组,TFT玻璃减薄,ITO导电膜玻璃,柔性ITO导电膜"},
        {"company_id": "tianxiaxiu", "name_zh": "天下秀数字科技(集团)股份有限公司", "stock_code": "600556.SH", "province": "广西", "city": "北海市", "industry": "互联网", "main_business": "智慧城市相关业务"},
        {"company_id": "kangyuan", "name_zh": "江苏康缘药业股份有限公司", "stock_code": "600557.SH", "province": "江苏", "city": "连云港市", "industry": "中成药", "main_business": "胶囊,口服液,冲剂片,丸剂"},
        {"company_id": "atlantic", "name_zh": "四川大西洋焊接材料股份有限公司", "stock_code": "600558.SH", "province": "四川", "city": "自贡市", "industry": "钢加工", "main_business": "焊条,焊丝"},
        {"company_id": "laobaigan", "name_zh": "河北衡水老白干酒业股份有限公司", "stock_code": "600559.SH", "province": "河北", "city": "衡水市", "industry": "白酒", "main_business": "白酒,商品猪,种猪,饲料"},
        {"company_id": "aritime", "name_zh": "北京金自天正智能控制股份有限公司", "stock_code": "600560.SH", "province": "北京", "city": "北京市", "industry": "电气设备", "main_business": "电气传动装置,工业计算机控制系统,工业专用检测及控制仪表,电力半导体元器件"},
        {"company_id": "jiangxi_changyun", "name_zh": "江西长运股份有限公司", "stock_code": "600561.SH", "province": "江西", "city": "南昌市", "industry": "公共交通", "main_business": "公路旅客运输,旅游服务,车辆租赁"},
        {"company_id": "guorui", "name_zh": "国睿科技股份有限公司", "stock_code": "600562.SH", "province": "江苏", "city": "南京市", "industry": "通信设备", "main_business": "微波与信息技术相关产品的生产和销售"},
    ],
    "exposures": [
        {"exposure_id": "baobian_elec_manufacture_transformer", "company_id": "baobian_elec", "node_id": "transformer", "activity_type": "manufacture", "role": "变压器制造商", "weight": 0.95},
        {"exposure_id": "baobian_elec_manufacture_current_transformer", "company_id": "baobian_elec", "node_id": "current_transformer", "activity_type": "manufacture", "role": "互感器制造商", "weight": 0.9},
        {"exposure_id": "baobian_elec_produce_solar_cell", "company_id": "baobian_elec", "node_id": "solar_cell", "activity_type": "produce", "role": "太阳能电池组件生产商", "weight": 0.85},
        {"exposure_id": "times_publishing_operate_book_publishing", "company_id": "times_publishing", "node_id": "book_publishing", "activity_type": "operate", "role": "图书出版运营商", "weight": 0.95},
        {"exposure_id": "times_publishing_operate_journal_publishing", "company_id": "times_publishing", "node_id": "journal_publishing", "activity_type": "operate", "role": "期刊出版运营商", "weight": 0.9},
        {"exposure_id": "times_publishing_provide_service_printing_service", "company_id": "times_publishing", "node_id": "printing_service", "activity_type": "provide_service", "role": "印刷复制服务商", "weight": 0.85},
        {"exposure_id": "kaisheng_tech_manufacture_tft_lcd_module", "company_id": "kaisheng_tech", "node_id": "tft_lcd_module", "activity_type": "manufacture", "role": "TFT液晶显示模组制造商", "weight": 0.95},
        {"exposure_id": "kaisheng_tech_manufacture_touch_screen_module", "company_id": "kaisheng_tech", "node_id": "touch_screen_module", "activity_type": "manufacture", "role": "触摸屏模组制造商", "weight": 0.95},
        {"exposure_id": "kaisheng_tech_manufacture_ito_conductive_glass", "company_id": "kaisheng_tech", "node_id": "ito_conductive_glass", "activity_type": "manufacture", "role": "ITO导电膜玻璃制造商", "weight": 0.9},
        {"exposure_id": "tianxiaxiu_provide_service_smart_city", "company_id": "tianxiaxiu", "node_id": "smart_city", "activity_type": "provide_service", "role": "智慧城市服务商", "weight": 0.95},
        {"exposure_id": "tianxiaxiu_provide_service_software", "company_id": "tianxiaxiu", "node_id": "software", "activity_type": "provide_service", "role": "软件服务商", "weight": 0.85},
        {"exposure_id": "kangyuan_produce_chinese_patent_medicine", "company_id": "kangyuan", "node_id": "chinese_patent_medicine", "activity_type": "produce", "role": "中成药生产商", "weight": 0.95},
        {"exposure_id": "kangyuan_produce_pharmaceutical", "company_id": "kangyuan", "node_id": "pharmaceutical", "activity_type": "produce", "role": "药品生产商", "weight": 0.9},
        {"exposure_id": "atlantic_produce_welding_electrode", "company_id": "atlantic", "node_id": "welding_electrode", "activity_type": "produce", "role": "焊条生产商", "weight": 0.95},
        {"exposure_id": "atlantic_produce_welding_wire", "company_id": "atlantic", "node_id": "welding_wire", "activity_type": "produce", "role": "焊丝生产商", "weight": 0.95},
        {"exposure_id": "atlantic_produce_welding_material", "company_id": "atlantic", "node_id": "welding_material", "activity_type": "produce", "role": "焊接材料生产商", "weight": 0.9},
        {"exposure_id": "laobaigan_produce_liquor", "company_id": "laobaigan", "node_id": "liquor", "activity_type": "produce", "role": "白酒生产商", "weight": 0.95},
        {"exposure_id": "laobaigan_produce_pig", "company_id": "laobaigan", "node_id": "pig", "activity_type": "produce", "role": "商品猪生产商", "weight": 0.85},
        {"exposure_id": "laobaigan_produce_feed", "company_id": "laobaigan", "node_id": "feed", "activity_type": "produce", "role": "饲料生产商", "weight": 0.8},
        {"exposure_id": "aritime_manufacture_electric_drive", "company_id": "aritime", "node_id": "electric_drive", "activity_type": "manufacture", "role": "电气传动装置制造商", "weight": 0.95},
        {"exposure_id": "aritime_manufacture_industrial_control_system", "company_id": "aritime", "node_id": "industrial_control_system", "activity_type": "manufacture", "role": "工业计算机控制系统制造商", "weight": 0.9},
        {"exposure_id": "aritime_manufacture_power_semiconductor_component", "company_id": "aritime", "node_id": "power_semiconductor_component", "activity_type": "manufacture", "role": "电力半导体元器件制造商", "weight": 0.9},
        {"exposure_id": "jiangxi_changyun_operate_passenger_transport", "company_id": "jiangxi_changyun", "node_id": "passenger_transport", "activity_type": "operate", "role": "公路旅客运输运营商", "weight": 0.95},
        {"exposure_id": "jiangxi_changyun_provide_service_tourism_service", "company_id": "jiangxi_changyun", "node_id": "tourism_service", "activity_type": "provide_service", "role": "旅游服务商", "weight": 0.85},
        {"exposure_id": "jiangxi_changyun_operate_vehicle_rental", "company_id": "jiangxi_changyun", "node_id": "vehicle_rental", "activity_type": "operate", "role": "车辆租赁运营商", "weight": 0.8},
        {"exposure_id": "guorui_manufacture_microwave_product", "company_id": "guorui", "node_id": "microwave_product", "activity_type": "manufacture", "role": "微波产品制造商", "weight": 0.95},
        {"exposure_id": "guorui_manufacture_communication_equipment", "company_id": "guorui", "node_id": "communication_equipment", "activity_type": "manufacture", "role": "通信设备制造商", "weight": 0.9},
    ],
}

BATCH_083 = {
    "new_nodes": [
        {"node_id": "film_capacitor", "canonical_name_zh": "薄膜电容器", "definition": "以金属化薄膜为电介质的电容器，具有自愈性好、可靠性高的特点，广泛用于电子电力领域", "entity_type": "component"},
        {"node_id": "corrugated_paperboard", "canonical_name_zh": "箱纸板", "definition": "用于制造瓦楞纸箱的纸板材料，由面纸和瓦楞芯纸复合而成", "entity_type": "material"},
        {"node_id": "carton", "canonical_name_zh": "纸箱", "definition": "由瓦楞纸板制成的包装容器，广泛用于商品运输和储存包装", "entity_type": "material"},
        {"node_id": "medium_thick_plate", "canonical_name_zh": "中厚板", "definition": "厚度在4.5-60mm之间的钢板，用于造船、桥梁、压力容器等重型结构", "entity_type": "material"},
        {"node_id": "hot_rolled_coil", "canonical_name_zh": "热轧卷板", "definition": "经热轧工艺生产的卷状钢板，是冷轧板、镀锌板等产品的原料", "entity_type": "material"},
        {"node_id": "financial_software", "canonical_name_zh": "金融软件", "definition": "用于银行、证券、保险等金融机构业务处理和管理的信息系统软件", "entity_type": "service"},
        {"node_id": "beer", "canonical_name_zh": "啤酒", "definition": "以大麦芽、啤酒花为主要原料经发酵酿制而成的低酒精度饮料", "entity_type": "material"},
        {"node_id": "coal_railway_transport", "canonical_name_zh": "煤炭铁路运输", "definition": "通过铁路专用线或公共铁路网络进行煤炭长距离运输的物流服务", "entity_type": "service"},
    ],
    "new_edges": [
        {"edge_id": "film_capacitor_to_electronic_device", "from_node": "film_capacitor", "to_node": "electronic_device", "edge_type": "composition", "description": "薄膜电容器是电子电力设备中储存和调节电能的核心元件"},
        {"edge_id": "corrugated_paperboard_to_carton", "from_node": "corrugated_paperboard", "to_node": "carton", "edge_type": "material_flow", "description": "箱纸板经裁切折叠后制成纸箱包装容器"},
        {"edge_id": "hot_rolled_coil_to_automobile", "from_node": "hot_rolled_coil", "to_node": "automobile", "edge_type": "material_flow", "description": "热轧卷板经冷轧等深加工后用于制造汽车车身和零部件"},
    ],
    "companies": [
        {"company_id": "faratronic", "name_zh": "厦门法拉电子股份有限公司", "stock_code": "600563.SH", "province": "福建", "city": "厦门市", "industry": "元器件", "main_business": "薄膜电容器,变压器及金属化膜等"},
        {"company_id": "jichuan", "name_zh": "湖北济川药业股份有限公司", "stock_code": "600566.SH", "province": "湖北", "city": "黄冈市", "industry": "中成药", "main_business": "药品的研发,生产和销售"},
        {"company_id": "shan_ying", "name_zh": "山鹰国际控股股份公司", "stock_code": "600567.SH", "province": "上海", "city": "上海市", "industry": "造纸", "main_business": "箱纸板,纸箱"},
        {"company_id": "st_zhongzhu", "name_zh": "中珠医疗控股股份有限公司", "stock_code": "600568.SH", "province": "湖北", "city": "潜江市", "industry": "医疗保健", "main_business": "医疗,医药和房地产"},
        {"company_id": "anyang_steel", "name_zh": "安阳钢铁股份有限公司", "stock_code": "600569.SH", "province": "河南", "city": "安阳市", "industry": "普钢", "main_business": "中厚板,热轧卷板,高速线材,建材,型材等"},
        {"company_id": "hundsun", "name_zh": "恒生电子股份有限公司", "stock_code": "600570.SH", "province": "浙江", "city": "杭州市", "industry": "软件服务", "main_business": "软件及服务,系统集成,硬件销售"},
        {"company_id": "sunyar", "name_zh": "信雅达科技股份有限公司", "stock_code": "600571.SH", "province": "浙江", "city": "杭州市", "industry": "软件服务", "main_business": "电子影像处理系统,客户服务中心系统,计算机主机通讯安全系统"},
        {"company_id": "conba", "name_zh": "浙江康恩贝制药股份有限公司", "stock_code": "600572.SH", "province": "浙江", "city": "杭州市", "industry": "中成药", "main_business": "以现代植物药为核心,特色化学药为重要支持的产品结构"},
        {"company_id": "huiquan", "name_zh": "福建省燕京惠泉啤酒股份有限公司", "stock_code": "600573.SH", "province": "福建", "city": "泉州市", "industry": "啤酒", "main_business": "啤酒的生产与销售"},
        {"company_id": "huaihe_energy", "name_zh": "淮河能源(集团)股份有限公司", "stock_code": "600575.SH", "province": "安徽", "city": "淮南市", "industry": "火力发电", "main_business": "煤炭,集装箱,外贸大宗散货,件杂货等货种的装卸中转以及配煤业务,煤炭铁路运输服务"},
    ],
    "exposures": [
        {"exposure_id": "faratronic_manufacture_film_capacitor", "company_id": "faratronic", "node_id": "film_capacitor", "activity_type": "manufacture", "role": "薄膜电容器制造商", "weight": 0.95},
        {"exposure_id": "faratronic_produce_metallized_film", "company_id": "faratronic", "node_id": "metallized_film", "activity_type": "produce", "role": "金属化膜生产商", "weight": 0.9},
        {"exposure_id": "jichuan_produce_pharmaceutical", "company_id": "jichuan", "node_id": "pharmaceutical", "activity_type": "produce", "role": "药品生产商", "weight": 0.95},
        {"exposure_id": "jichuan_produce_chinese_patent_medicine", "company_id": "jichuan", "node_id": "chinese_patent_medicine", "activity_type": "produce", "role": "中成药生产商", "weight": 0.9},
        {"exposure_id": "shan_ying_produce_corrugated_paperboard", "company_id": "shan_ying", "node_id": "corrugated_paperboard", "activity_type": "produce", "role": "箱纸板生产商", "weight": 0.95},
        {"exposure_id": "shan_ying_produce_carton", "company_id": "shan_ying", "node_id": "carton", "activity_type": "produce", "role": "纸箱生产商", "weight": 0.95},
        {"exposure_id": "shan_ying_produce_paper", "company_id": "shan_ying", "node_id": "paper", "activity_type": "produce", "role": "造纸商", "weight": 0.9},
        {"exposure_id": "st_zhongzhu_provide_service_medical_service", "company_id": "st_zhongzhu", "node_id": "medical_service", "activity_type": "provide_service", "role": "医疗服务商", "weight": 0.95},
        {"exposure_id": "st_zhongzhu_produce_pharmaceutical", "company_id": "st_zhongzhu", "node_id": "pharmaceutical", "activity_type": "produce", "role": "药品生产商", "weight": 0.9},
        {"exposure_id": "st_zhongzhu_operate_real_estate_development", "company_id": "st_zhongzhu", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发运营商", "weight": 0.85},
        {"exposure_id": "anyang_steel_produce_medium_thick_plate", "company_id": "anyang_steel", "node_id": "medium_thick_plate", "activity_type": "produce", "role": "中厚板生产商", "weight": 0.95},
        {"exposure_id": "anyang_steel_produce_hot_rolled_coil", "company_id": "anyang_steel", "node_id": "hot_rolled_coil", "activity_type": "produce", "role": "热轧卷板生产商", "weight": 0.95},
        {"exposure_id": "anyang_steel_produce_high_speed_wire_rod", "company_id": "anyang_steel", "node_id": "high_speed_wire_rod", "activity_type": "produce", "role": "高速线材生产商", "weight": 0.9},
        {"exposure_id": "anyang_steel_produce_steel", "company_id": "anyang_steel", "node_id": "steel", "activity_type": "produce", "role": "钢材生产商", "weight": 0.95},
        {"exposure_id": "hundsun_provide_service_financial_software", "company_id": "hundsun", "node_id": "financial_software", "activity_type": "provide_service", "role": "金融软件服务商", "weight": 0.95},
        {"exposure_id": "hundsun_provide_service_system_integration", "company_id": "hundsun", "node_id": "system_integration", "activity_type": "provide_service", "role": "系统集成服务商", "weight": 0.9},
        {"exposure_id": "hundsun_provide_service_software", "company_id": "hundsun", "node_id": "software", "activity_type": "provide_service", "role": "软件服务商", "weight": 0.9},
        {"exposure_id": "sunyar_provide_service_electronic_image_processing", "company_id": "sunyar", "node_id": "electronic_image_processing", "activity_type": "provide_service", "role": "电子影像处理系统服务商", "weight": 0.95},
        {"exposure_id": "sunyar_provide_service_customer_service_system", "company_id": "sunyar", "node_id": "customer_service_system", "activity_type": "provide_service", "role": "客户服务中心系统服务商", "weight": 0.9},
        {"exposure_id": "sunyar_provide_service_software", "company_id": "sunyar", "node_id": "software", "activity_type": "provide_service", "role": "软件服务商", "weight": 0.85},
        {"exposure_id": "conba_produce_modern_botanical_medicine", "company_id": "conba", "node_id": "modern_botanical_medicine", "activity_type": "produce", "role": "现代植物药生产商", "weight": 0.95},
        {"exposure_id": "conba_produce_chemical_drug", "company_id": "conba", "node_id": "chemical_drug", "activity_type": "produce", "role": "化学药生产商", "weight": 0.9},
        {"exposure_id": "conba_produce_chinese_patent_medicine", "company_id": "conba", "node_id": "chinese_patent_medicine", "activity_type": "produce", "role": "中成药生产商", "weight": 0.9},
        {"exposure_id": "huiquan_produce_beer", "company_id": "huiquan", "node_id": "beer", "activity_type": "produce", "role": "啤酒生产商", "weight": 0.95},
        {"exposure_id": "huiquan_produce_beverage", "company_id": "huiquan", "node_id": "beverage", "activity_type": "produce", "role": "饮料生产商", "weight": 0.85},
        {"exposure_id": "huaihe_energy_operate_coal", "company_id": "huaihe_energy", "node_id": "coal", "activity_type": "operate", "role": "煤炭经营商", "weight": 0.95},
        {"exposure_id": "huaihe_energy_operate_coal_railway_transport", "company_id": "huaihe_energy", "node_id": "coal_railway_transport", "activity_type": "operate", "role": "煤炭铁路运输运营商", "weight": 0.9},
        {"exposure_id": "huaihe_energy_operate_bulk_cargo_handling", "company_id": "huaihe_energy", "node_id": "bulk_cargo_handling", "activity_type": "operate", "role": "大宗散货装卸运营商", "weight": 0.85},
    ],
}

BATCH_084 = {
    "new_nodes": [
        {"node_id": "enameled_wire", "canonical_name_zh": "漆包电磁线", "definition": "表面涂覆绝缘漆的铜或铝导线，用于电机、变压器等电气设备的绕组", "entity_type": "material"},
        {"node_id": "power_cable", "canonical_name_zh": "电线电缆", "definition": "用于传输和分配电能的导线及其绝缘护套的组合产品", "entity_type": "component"},
        {"node_id": "desulfurization_byproduct", "canonical_name_zh": "脱硫副产品", "definition": "燃煤电厂烟气脱硫过程中产生的副产物，如石膏等", "entity_type": "material"},
        {"node_id": "chemical_equipment", "canonical_name_zh": "化工装备", "definition": "用于化工生产过程的专用机械设备，包括反应釜、换热器、塔器等", "entity_type": "device"},
        {"node_id": "industrial_motor", "canonical_name_zh": "工业驱动及控制电机", "definition": "用于驱动工业生产机械设备的电动机及其控制系统", "entity_type": "component"},
        {"node_id": "electric_bicycle", "canonical_name_zh": "电动自行车", "definition": "以蓄电池为辅助能源，在普通自行车基础上安装电机和控制系统的两轮交通工具", "entity_type": "system"},
        {"node_id": "mining_automation", "canonical_name_zh": "矿山自动化", "definition": "利用自动化技术实现矿山采掘、运输、通风等过程的无人化或少人化运行", "entity_type": "service"},
        {"node_id": "ocean_engineering", "canonical_name_zh": "海洋工程", "definition": "在海洋环境中进行的油气开发、海上风电等工程建设和运维服务", "entity_type": "service"},
    ],
    "new_edges": [
        {"edge_id": "enameled_wire_to_motor", "from_node": "enameled_wire", "to_node": "motor", "edge_type": "composition", "description": "漆包电磁线是电机和变压器绕组的核心导电材料"},
        {"edge_id": "industrial_motor_to_industrial_equipment", "from_node": "industrial_motor", "to_node": "industrial_equipment", "edge_type": "composition", "description": "工业电机是驱动各类工业机械设备的核心动力部件"},
        {"edge_id": "ocean_engineering_to_offshore_oil", "from_node": "ocean_engineering", "to_node": "offshore_oil", "edge_type": "capability_supply", "description": "海洋工程为海上油气开发提供平台建设和运维服务能力"},
    ],
    "companies": [
        {"company_id": "xiangyuan", "name_zh": "浙江祥源文旅股份有限公司", "stock_code": "600576.SH", "province": "浙江", "city": "杭州市", "industry": "旅游景点", "main_business": "房地产开发,连锁酒店经营投资"},
        {"company_id": "jinda", "name_zh": "铜陵精达特种电磁线股份有限公司", "stock_code": "600577.SH", "province": "安徽", "city": "铜陵市", "industry": "电气设备", "main_business": "漆包电磁线,裸铜线和电线电缆的制造和销售"},
        {"company_id": "jingneng_power", "name_zh": "北京京能电力股份有限公司", "stock_code": "600578.SH", "province": "北京", "city": "北京市", "industry": "火力发电", "main_business": "发电量,供热量,脱硫副产品"},
        {"company_id": "sinochem_equip", "name_zh": "中化装备科技(青岛)股份有限公司", "stock_code": "600579.SH", "province": "山东", "city": "青岛市", "industry": "化工机械", "main_business": "化工装备的研发,生产和销售"},
        {"company_id": "wolong", "name_zh": "卧龙电气驱动集团股份有限公司", "stock_code": "600580.SH", "province": "浙江", "city": "绍兴市", "industry": "电气设备", "main_business": "工业驱动及控制电机,中高压电机,家用电器电机,微电机,电动自行车,蓄电池"},
        {"company_id": "st_bayi", "name_zh": "新疆八一钢铁股份有限公司", "stock_code": "600581.SH", "province": "新疆", "city": "乌鲁木齐市", "industry": "普钢", "main_business": "高速线材,螺纹钢,热轧板卷,冷轧薄板,中厚板等建筑及工业用钢"},
        {"company_id": "tiandi", "name_zh": "天地科技股份有限公司", "stock_code": "600582.SH", "province": "北京", "city": "北京市", "industry": "专用机械", "main_business": "矿山自动化,机械化设备,煤炭洗选装备,矿井生产技术服务与经营,地下特殊工程施工"},
        {"company_id": "cooec", "name_zh": "海洋石油工程股份有限公司", "stock_code": "600583.SH", "province": "天津", "city": "天津市", "industry": "石油开采", "main_business": "海洋工程"},
        {"company_id": "jcet", "name_zh": "江苏长电科技股份有限公司", "stock_code": "600584.SH", "province": "江苏", "city": "无锡市", "industry": "半导体", "main_business": "集成电路封装测试,分立器件制造销售"},
        {"company_id": "conch", "name_zh": "安徽海螺水泥股份有限公司", "stock_code": "600585.SH", "province": "安徽", "city": "芜湖市", "industry": "水泥", "main_business": "水泥的生产与销售"},
    ],
    "exposures": [
        {"exposure_id": "xiangyuan_operate_real_estate_development", "company_id": "xiangyuan", "node_id": "real_estate_development", "activity_type": "operate", "role": "房地产开发运营商", "weight": 0.95},
        {"exposure_id": "xiangyuan_operate_hotel_service", "company_id": "xiangyuan", "node_id": "hotel_service", "activity_type": "operate", "role": "连锁酒店运营商", "weight": 0.9},
        {"exposure_id": "xiangyuan_operate_tourism_investment", "company_id": "xiangyuan", "node_id": "tourism_investment", "activity_type": "operate", "role": "文旅投资运营商", "weight": 0.85},
        {"exposure_id": "jinda_produce_enameled_wire", "company_id": "jinda", "node_id": "enameled_wire", "activity_type": "produce", "role": "漆包电磁线生产商", "weight": 0.95},
        {"exposure_id": "jinda_produce_bare_copper_wire", "company_id": "jinda", "node_id": "bare_copper_wire", "activity_type": "produce", "role": "裸铜线生产商", "weight": 0.9},
        {"exposure_id": "jinda_produce_power_cable", "company_id": "jinda", "node_id": "power_cable", "activity_type": "produce", "role": "电线电缆生产商", "weight": 0.9},
        {"exposure_id": "jingneng_power_operate_power_generation", "company_id": "jingneng_power", "node_id": "power_generation", "activity_type": "operate", "role": "发电运营商", "weight": 0.95},
        {"exposure_id": "jingneng_power_provide_service_heating_supply", "company_id": "jingneng_power", "node_id": "heating_supply", "activity_type": "provide_service", "role": "热力供应商", "weight": 0.9},
        {"exposure_id": "jingneng_power_produce_desulfurization_byproduct", "company_id": "jingneng_power", "node_id": "desulfurization_byproduct", "activity_type": "produce", "role": "脱硫副产品生产商", "weight": 0.8},
        {"exposure_id": "sinochem_equip_manufacture_chemical_equipment", "company_id": "sinochem_equip", "node_id": "chemical_equipment", "activity_type": "manufacture", "role": "化工装备制造商", "weight": 0.95},
        {"exposure_id": "sinochem_equip_operate_chemical_industry", "company_id": "sinochem_equip", "node_id": "chemical_industry", "activity_type": "operate", "role": "化工行业服务商", "weight": 0.85},
        {"exposure_id": "wolong_manufacture_industrial_motor", "company_id": "wolong", "node_id": "industrial_motor", "activity_type": "manufacture", "role": "工业电机制造商", "weight": 0.95},
        {"exposure_id": "wolong_manufacture_medium_high_voltage_motor", "company_id": "wolong", "node_id": "medium_high_voltage_motor", "activity_type": "manufacture", "role": "中高压电机制造商", "weight": 0.9},
        {"exposure_id": "wolong_manufacture_household_appliance_motor", "company_id": "wolong", "node_id": "household_appliance_motor", "activity_type": "manufacture", "role": "家用电器电机制造商", "weight": 0.9},
        {"exposure_id": "wolong_manufacture_electric_bicycle", "company_id": "wolong", "node_id": "electric_bicycle", "activity_type": "manufacture", "role": "电动自行车制造商", "weight": 0.85},
        {"exposure_id": "st_bayi_produce_high_speed_wire_rod", "company_id": "st_bayi", "node_id": "high_speed_wire_rod", "activity_type": "produce", "role": "高速线材生产商", "weight": 0.95},
        {"exposure_id": "st_bayi_produce_rebar", "company_id": "st_bayi", "node_id": "rebar", "activity_type": "produce", "role": "螺纹钢生产商", "weight": 0.95},
        {"exposure_id": "st_bayi_produce_hot_rolled_coil", "company_id": "st_bayi", "node_id": "hot_rolled_coil", "activity_type": "produce", "role": "热轧卷板生产商", "weight": 0.9},
        {"exposure_id": "st_bayi_produce_steel", "company_id": "st_bayi", "node_id": "steel", "activity_type": "produce", "role": "钢铁生产商", "weight": 0.95},
        {"exposure_id": "tiandi_provide_service_mining_automation", "company_id": "tiandi", "node_id": "mining_automation", "activity_type": "provide_service", "role": "矿山自动化服务商", "weight": 0.95},
        {"exposure_id": "tiandi_manufacture_coal_washing_equipment", "company_id": "tiandi", "node_id": "coal_washing_equipment", "activity_type": "manufacture", "role": "煤炭洗选装备制造商", "weight": 0.9},
        {"exposure_id": "tiandi_operate_coal_mining", "company_id": "tiandi", "node_id": "coal_mining", "activity_type": "operate", "role": "煤炭开采运营商", "weight": 0.85},
        {"exposure_id": "cooec_operate_ocean_engineering", "company_id": "cooec", "node_id": "ocean_engineering", "activity_type": "operate", "role": "海洋工程运营商", "weight": 0.95},
        {"exposure_id": "cooec_provide_service_offshore_oil", "company_id": "cooec", "node_id": "offshore_oil", "activity_type": "provide_service", "role": "海上油气工程服务商", "weight": 0.9},
        {"exposure_id": "jcet_provide_service_integrated_circuit_packaging", "company_id": "jcet", "node_id": "integrated_circuit_packaging", "activity_type": "provide_service", "role": "集成电路封装测试服务商", "weight": 0.95},
        {"exposure_id": "jcet_manufacture_semiconductor_device", "company_id": "jcet", "node_id": "semiconductor_device", "activity_type": "manufacture", "role": "半导体分立器件制造商", "weight": 0.9},
        {"exposure_id": "conch_produce_cement", "company_id": "conch", "node_id": "cement", "activity_type": "produce", "role": "水泥生产商", "weight": 0.95},
        {"exposure_id": "conch_produce_building_material", "company_id": "conch", "node_id": "building_material", "activity_type": "produce", "role": "建材生产商", "weight": 0.9},
    ],
}

BATCH_085 = {
    "new_nodes": [
        {"node_id": "flat_glass", "canonical_name_zh": "平板玻璃", "definition": "通过浮法等工艺生产的平整透明玻璃板材，广泛用于建筑门窗、幕墙、汽车等领域", "entity_type": "material"},
        {"node_id": "sterilization_equipment", "canonical_name_zh": "消毒灭菌设备", "definition": "用于医疗器械、药品等消毒灭菌处理的专用设备，包括高温高压灭菌器、环氧乙烷灭菌器等", "entity_type": "device"},
        {"node_id": "pharmaceutical_equipment", "canonical_name_zh": "制药设备", "definition": "用于药品生产过程中的专用机械设备，包括制粒机、压片机、灌装机等", "entity_type": "device"},
        {"node_id": "amino_composite_material", "canonical_name_zh": "氨基复合材料", "definition": "以氨基树脂为基体的复合材料，具有硬度高、耐磨性好的特点，用于制造餐具和装饰材料", "entity_type": "material"},
        {"node_id": "idc", "canonical_name_zh": "互联网数据中心", "definition": "提供服务器托管、租用及互联网接入等服务的专业化数据中心设施", "entity_type": "service"},
        {"node_id": "bearing", "canonical_name_zh": "轴承", "definition": "支承机械旋转体并降低其运动过程中摩擦系数的精密机械零部件", "entity_type": "component"},
        {"node_id": "high_performance_aluminum_sheet", "canonical_name_zh": "高性能铝合金板材", "definition": "通过合金化及热处理获得高强度、耐腐蚀等优异性能的铝板带材产品", "entity_type": "material"},
        {"node_id": "glyphosate", "canonical_name_zh": "草甘膦", "definition": "一种广谱灭生性除草剂的主要有效成分，通过抑制植物芳香族氨基酸合成途径起作用", "entity_type": "material"},
    ],
    "new_edges": [
        {"edge_id": "flat_glass_to_construction", "from_node": "flat_glass", "to_node": "construction", "edge_type": "material_flow", "description": "平板玻璃是建筑门窗幕墙和室内装修的主要材料"},
        {"edge_id": "bearing_to_automobile", "from_node": "bearing", "to_node": "automobile", "edge_type": "composition", "description": "轴承是汽车发动机、变速箱和车轮等关键部位的精密支撑部件"},
        {"edge_id": "glyphosate_to_pesticide", "from_node": "glyphosate", "to_node": "pesticide", "edge_type": "material_flow", "description": "草甘膦是生产广谱除草剂农药的主要有效成分"},
    ],
    "companies": [
        {"company_id": "jinjing", "name_zh": "山东金晶科技股份有限公司", "stock_code": "600586.SH", "province": "山东", "city": "淄博市", "industry": "玻璃", "main_business": "玻璃和纯碱的生产与销售"},
        {"company_id": "shinva", "name_zh": "山东新华医疗器械股份有限公司", "stock_code": "600587.SH", "province": "山东", "city": "淄博市", "industry": "医疗保健", "main_business": "消毒灭菌设备,放射诊断及治疗设备,制药设备,环保设备"},
        {"company_id": "yonyou", "name_zh": "用友网络科技股份有限公司", "stock_code": "600588.SH", "province": "北京", "city": "北京市", "industry": "软件服务", "main_business": "软件销售,技术服务及培训,软件配套用品销售"},
        {"company_id": "dawei", "name_zh": "大位数据科技(广东)集团股份有限公司", "stock_code": "600589.SH", "province": "广东", "city": "揭阳市", "industry": "软件服务", "main_business": "氨基复合材料,苯酐及增塑剂等化工材料;互联网数据中心(IDC),云计算,CDN"},
        {"company_id": "tellhow", "name_zh": "泰豪科技股份有限公司", "stock_code": "600590.SH", "province": "江西", "city": "南昌市", "industry": "通信设备", "main_business": "智能电力,装备信息,智能节能,电机产业"},
        {"company_id": "longxi", "name_zh": "福建龙溪轴承(集团)股份有限公司", "stock_code": "600592.SH", "province": "福建", "city": "漳州市", "industry": "机械基件", "main_business": "轴承,汽车配件"},
        {"company_id": "dalian_shengya", "name_zh": "大连圣亚旅游控股股份有限公司", "stock_code": "600593.SH", "province": "辽宁", "city": "大连市", "industry": "旅游景点", "main_business": "景观,餐饮,景点场地出租"},
        {"company_id": "yibai", "name_zh": "贵州益佰制药股份有限公司", "stock_code": "600594.SH", "province": "贵州", "city": "贵阳市", "industry": "中成药", "main_business": "OTC药,处方药"},
        {"company_id": "zhongfu", "name_zh": "河南中孚实业股份有限公司", "stock_code": "600595.SH", "province": "河南", "city": "郑州市", "industry": "铝", "main_business": "高性能铝合金板材,易拉罐罐体,罐盖,拉环料,高档双零铝箔毛料,印刷版基"},
        {"company_id": "xinan", "name_zh": "浙江新安化工集团股份有限公司", "stock_code": "600596.SH", "province": "浙江", "city": "杭州市", "industry": "化工原料", "main_business": "以草甘膦为主的农药产品和有机硅新材料产品"},
    ],
    "exposures": [
        {"exposure_id": "jinjing_produce_flat_glass", "company_id": "jinjing", "node_id": "flat_glass", "activity_type": "produce", "role": "平板玻璃生产商", "weight": 0.95},
        {"exposure_id": "jinjing_produce_soda_ash", "company_id": "jinjing", "node_id": "soda_ash", "activity_type": "produce", "role": "纯碱生产商", "weight": 0.9},
        {"exposure_id": "shinva_manufacture_sterilization_equipment", "company_id": "shinva", "node_id": "sterilization_equipment", "activity_type": "manufacture", "role": "消毒灭菌设备制造商", "weight": 0.95},
        {"exposure_id": "shinva_manufacture_radiotherapy_equipment", "company_id": "shinva", "node_id": "radiotherapy_equipment", "activity_type": "manufacture", "role": "放射诊断及治疗设备制造商", "weight": 0.9},
        {"exposure_id": "shinva_manufacture_pharmaceutical_equipment", "company_id": "shinva", "node_id": "pharmaceutical_equipment", "activity_type": "manufacture", "role": "制药设备制造商", "weight": 0.9},
        {"exposure_id": "yonyou_provide_service_application_software", "company_id": "yonyou", "node_id": "application_software", "activity_type": "provide_service", "role": "应用软件服务商", "weight": 0.95},
        {"exposure_id": "yonyou_provide_service_software", "company_id": "yonyou", "node_id": "software", "activity_type": "provide_service", "role": "软件服务商", "weight": 0.95},
        {"exposure_id": "yonyou_provide_service_it_service", "company_id": "yonyou", "node_id": "it_service", "activity_type": "provide_service", "role": "IT服务商", "weight": 0.9},
        {"exposure_id": "dawei_produce_amino_composite_material", "company_id": "dawei", "node_id": "amino_composite_material", "activity_type": "produce", "role": "氨基复合材料生产商", "weight": 0.95},
        {"exposure_id": "dawei_produce_phthalic_anhydride", "company_id": "dawei", "node_id": "phthalic_anhydride", "activity_type": "produce", "role": "苯酐生产商", "weight": 0.9},
        {"exposure_id": "dawei_produce_plasticizer", "company_id": "dawei", "node_id": "plasticizer", "activity_type": "produce", "role": "增塑剂生产商", "weight": 0.9},
        {"exposure_id": "dawei_operate_idc", "company_id": "dawei", "node_id": "idc", "activity_type": "operate", "role": "互联网数据中心运营商", "weight": 0.85},
        {"exposure_id": "dawei_provide_service_cloud_computing", "company_id": "dawei", "node_id": "cloud_computing", "activity_type": "provide_service", "role": "云计算服务商", "weight": 0.85},
        {"exposure_id": "tellhow_manufacture_smart_grid_device", "company_id": "tellhow", "node_id": "smart_grid_device", "activity_type": "manufacture", "role": "智能电力设备制造商", "weight": 0.95},
        {"exposure_id": "tellhow_manufacture_electric_motor", "company_id": "tellhow", "node_id": "electric_motor", "activity_type": "manufacture", "role": "电机制造商", "weight": 0.9},
        {"exposure_id": "tellhow_provide_service_energy_saving", "company_id": "tellhow", "node_id": "energy_saving", "activity_type": "provide_service", "role": "节能服务商", "weight": 0.85},
        {"exposure_id": "longxi_manufacture_bearing", "company_id": "longxi", "node_id": "bearing", "activity_type": "manufacture", "role": "轴承制造商", "weight": 0.95},
        {"exposure_id": "longxi_manufacture_automobile_part", "company_id": "longxi", "node_id": "automobile_part", "activity_type": "manufacture", "role": "汽车配件制造商", "weight": 0.9},
        {"exposure_id": "dalian_shengya_operate_scenic_spot", "company_id": "dalian_shengya", "node_id": "scenic_spot", "activity_type": "operate", "role": "景点运营商", "weight": 0.95},
        {"exposure_id": "dalian_shengya_operate_catering_service", "company_id": "dalian_shengya", "node_id": "catering_service", "activity_type": "operate", "role": "餐饮服务商", "weight": 0.85},
        {"exposure_id": "dalian_shengya_provide_service_tourism_service", "company_id": "dalian_shengya", "node_id": "tourism_service", "activity_type": "provide_service", "role": "旅游服务商", "weight": 0.85},
        {"exposure_id": "yibai_produce_otc_drug", "company_id": "yibai", "node_id": "otc_drug", "activity_type": "produce", "role": "OTC药品生产商", "weight": 0.95},
        {"exposure_id": "yibai_produce_prescription_drug", "company_id": "yibai", "node_id": "prescription_drug", "activity_type": "produce", "role": "处方药生产商", "weight": 0.95},
        {"exposure_id": "yibai_produce_pharmaceutical", "company_id": "yibai", "node_id": "pharmaceutical", "activity_type": "produce", "role": "药品生产商", "weight": 0.9},
        {"exposure_id": "zhongfu_produce_high_performance_aluminum_sheet", "company_id": "zhongfu", "node_id": "high_performance_aluminum_sheet", "activity_type": "produce", "role": "高性能铝合金板材生产商", "weight": 0.95},
        {"exposure_id": "zhongfu_produce_can_body_stock", "company_id": "zhongfu", "node_id": "can_body_stock", "activity_type": "produce", "role": "易拉罐料生产商", "weight": 0.9},
        {"exposure_id": "zhongfu_produce_aluminum_foil", "company_id": "zhongfu", "node_id": "aluminum_foil", "activity_type": "produce", "role": "铝箔生产商", "weight": 0.9},
        {"exposure_id": "xinan_produce_glyphosate", "company_id": "xinan", "node_id": "glyphosate", "activity_type": "produce", "role": "草甘膦生产商", "weight": 0.95},
        {"exposure_id": "xinan_produce_organosilicon", "company_id": "xinan", "node_id": "organosilicon", "activity_type": "produce", "role": "有机硅生产商", "weight": 0.95},
        {"exposure_id": "xinan_produce_pesticide", "company_id": "xinan", "node_id": "pesticide", "activity_type": "produce", "role": "农药生产商", "weight": 0.9},
    ],
}

ALL_BATCHES = {
    81: BATCH_081,
    82: BATCH_082,
    83: BATCH_083,
    84: BATCH_084,
    85: BATCH_085,
}

os.makedirs("tmp_script", exist_ok=True)

for nnn, data in ALL_BATCHES.items():
    content = TEMPLATE
    content = content.replace("%%NNN%%", f"{nnn:03d}")
    content = content.replace("%%NEW_NODES%%", json.dumps(data["new_nodes"], ensure_ascii=False, indent=4))
    content = content.replace("%%NEW_EDGES%%", json.dumps(data["new_edges"], ensure_ascii=False, indent=4))
    content = content.replace("%%COMPANIES%%", json.dumps(data["companies"], ensure_ascii=False, indent=4))
    content = content.replace("%%EXPOSURES%%", json.dumps(data["exposures"], ensure_ascii=False, indent=4))
    path = f"tmp_script/tmp_submit_batch_{nnn:03d}.py"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {path}")

print("\nAll 5 scripts generated.")
