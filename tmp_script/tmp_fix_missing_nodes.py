#!/usr/bin/env python3
"""Fix missing nodes and re-submit failed edges from batches 028-030."""
import requests
BASE_URL = "http://localhost:8000/api/v1"

# 1. Create missing nodes
nodes = [
    {"node_id":"gypsum","canonical_name_zh":"建筑石膏","canonical_name_en":"Building Gypsum","aliases":["石膏","生石膏"],"definition":"以天然石膏或工业副产石膏（如脱硫石膏、磷石膏）为原料，经破碎、煅烧、粉磨等工艺制成的气硬性胶凝材料，主要成分为半水硫酸钙，是生产石膏板、石膏砌块、抹灰石膏等建材的核心原料。","entity_type":"material","evidence":[{"source_title":"北新建材 生产原料","quote":"石膏板以建筑石膏为主要原料"}],"confidence":"HIGH","status":"ACTIVE"},
    {"node_id":"lithium_ion_battery","canonical_name_zh":"锂离子电池","canonical_name_en":"Lithium-ion Battery","aliases":["锂电池","锂电芯"],"definition":"以锂的化合物为正极材料、石墨等碳材料为负极材料，通过锂离子在正负极之间嵌入和脱嵌实现充放电的二次电池，具有能量密度高、自放电率低、无记忆效应等优点，广泛应用于电动汽车、储能系统、消费电子等领域。","entity_type":"device","evidence":[{"source_title":"盐湖股份 新能源布局","quote":"碳酸锂用于生产锂离子电池"}],"confidence":"HIGH","status":"ACTIVE"},
    {"node_id":"ndfeb_magnet","canonical_name_zh":"钕铁硼永磁体","canonical_name_en":"NdFeB Permanent Magnet","aliases":["钕铁硼磁材","稀土永磁"],"definition":"以钕（Nd）、铁（Fe）、硼（B）为主要成分的稀土永磁材料，是目前磁能积最高的永磁材料，具有优异的磁性能和机械性能，广泛用于新能源汽车驱动电机、风力发电机、节能家电、智能制造等领域。","entity_type":"material","evidence":[{"source_title":"英洛华 主营业务","quote":"主要业务:钕铁硼磁性材料...的研发,生产和销售"}],"confidence":"HIGH","status":"ACTIVE"},
    {"node_id":"cigarette","canonical_name_zh":"卷烟","canonical_name_en":"Cigarette","aliases":["香烟","纸烟"],"definition":"将烟叶切成烟丝，用纸卷制成圆筒形条状制品，经过烘焙、加香、滤嘴接装等工艺加工而成的烟草消费品，是烟草工业的主要终端产品形态。","entity_type":"material","evidence":[{"source_title":"陕西金叶 产业链","quote":"烟标包装用于卷烟产品"}],"confidence":"HIGH","status":"ACTIVE"},
    {"node_id":"refined_oil","canonical_name_zh":"成品油","canonical_name_en":"Refined Oil Product","aliases":["石油制品","精炼油品"],"definition":"原油经过炼厂蒸馏、催化裂化、加氢精制等工艺加工后得到的各类石油产品，包括汽油、柴油、煤油、润滑油、石脑油、燃料油等，是交通运输、工业生产和社会生活的主要能源和原料。","entity_type":"material","evidence":[{"source_title":"岳阳兴长 主营业务","quote":"主要业务:石油化工产品的生产,销售"}],"confidence":"HIGH","status":"ACTIVE"}
]

edges = [
    {"edge_id":"flow_gypsum_to_board","from_node":"gypsum","to_node":"gypsum_board","description":"石膏经加工制成石膏板。","edge_namespace":"industrial_flow","edge_type":"material_flow","evidence":[{"source_title":"北新建材 生产流程","quote":"石膏板以建筑石膏为主要原料"}],"confidence":"HIGH"},
    {"edge_id":"flow_lithium_carbonate_to_battery","from_node":"lithium_carbonate","to_node":"lithium_ion_battery","description":"碳酸锂用于生产锂离子电池正极材料和电解液。","edge_namespace":"industrial_flow","edge_type":"material_flow","evidence":[{"source_title":"盐湖股份 新能源布局","quote":"碳酸锂生产"}],"confidence":"HIGH"},
    {"edge_id":"flow_ndfeb_to_micro_motor","from_node":"ndfeb_magnet","to_node":"micro_motor","description":"钕铁硼永磁材料用于制造微电机的永磁转子。","edge_namespace":"industrial_flow","edge_type":"composition","evidence":[{"source_title":"英洛华 产品关联","quote":"钕铁硼+电机"}],"confidence":"HIGH"},
    {"edge_id":"flow_cigarette_packaging_to_tobacco","from_node":"cigarette_packaging","to_node":"cigarette","description":"烟标包装作为卷烟产品的外包装材料。","edge_namespace":"industrial_flow","edge_type":"composition","evidence":[{"source_title":"陕西金叶 产业链","quote":"烟标印刷→烟草包装"}],"confidence":"HIGH"},
    {"edge_id":"flow_methanol_to_fuel","from_node":"methanol","to_node":"refined_oil","description":"甲醇作为化工原料用于油品添加剂和清洁燃料生产。","edge_namespace":"industrial_flow","edge_type":"material_flow","evidence":[{"source_title":"岳阳兴长 产品关联","quote":"石油化工产品"}],"confidence":"HIGH"}
]

if __name__ == "__main__":
    gb = {"batch_id":"batch_fix_missing_nodes_graph","task_description":"Fix: Create missing nodes (gypsum, lithium_ion_battery, ndfeb_magnet, cigarette, refined_oil) and re-submit failed edges from batches 028-030.","nodes_to_upsert":nodes,"edges_to_upsert":edges,"rejected_or_pending":[]}
    r = requests.post(f"{BASE_URL}/batches", json=gb)
    print(f"Graph fix: {r.status_code}", r.json())
