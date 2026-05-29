#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix missing infrastructure nodes for batches 121-125."""
import json, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ev(source_title, quote="产业通用分类"):
    return [{"source_title": source_title, "source_url": None, "quote": quote}]

nodes = [
    {"node_id": "pharmaceutical", "canonical_name_zh": "药品", "canonical_name_en": "pharmaceutical", "entity_type": "material", "aliases": ["药物"], "definition": "用于预防、治疗、诊断疾病的化学或生物制品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "electronic_component", "canonical_name_zh": "电子元器件", "canonical_name_en": "electronic component", "entity_type": "component", "aliases": [], "definition": "电子电路中的基本组成单元，包括电阻、电容、二极管、集成电路等", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "cng_equipment", "canonical_name_zh": "压缩天然气设备", "canonical_name_en": "CNG equipment", "entity_type": "device", "aliases": [], "definition": "用于压缩天然气储存和加注的专用设备", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "filtration_equipment", "canonical_name_zh": "过滤设备", "canonical_name_en": "filtration equipment", "entity_type": "device", "aliases": [], "definition": "用于分离固体和液体或气体的机械设备", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "aluminum", "canonical_name_zh": "铝", "canonical_name_en": "aluminum", "entity_type": "material", "aliases": ["铝材"], "definition": "银白色轻金属，地壳中含量最丰富的金属元素，广泛用于工业制造", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "power_generation", "canonical_name_zh": "发电", "canonical_name_en": "power generation", "entity_type": "service", "aliases": [], "definition": "将各类能源转化为电能的生产活动", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "home_textile", "canonical_name_zh": "家用纺织品", "canonical_name_en": "home textile", "entity_type": "material", "aliases": [], "definition": "用于家庭装饰和日常使用的纺织产品，包括毛巾、窗帘、床上用品等", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "shipping", "canonical_name_zh": "航运", "canonical_name_en": "shipping", "entity_type": "service", "aliases": ["海运"], "definition": "利用船舶进行货物和旅客运输的服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "import_export", "canonical_name_zh": "进出口贸易", "canonical_name_en": "import export", "entity_type": "service", "aliases": [], "definition": "货物和服务的跨国进出口贸易活动", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "human_resource", "canonical_name_zh": "人力资源", "canonical_name_en": "human resource", "entity_type": "service", "aliases": [], "definition": "与劳动力招聘、培训、管理相关的服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "chemical_product", "canonical_name_zh": "化工产品", "canonical_name_en": "chemical product", "entity_type": "material", "aliases": [], "definition": "通过化学工艺生产的基础化学品和精细化工产品", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "chemical_process", "canonical_name_zh": "化工工艺", "canonical_name_en": "chemical process", "entity_type": "service", "aliases": [], "definition": "将原料通过化学反应转化为产品的工业生产过程", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "e_commerce", "canonical_name_zh": "电子商务", "canonical_name_en": "e-commerce", "entity_type": "service", "aliases": [], "definition": "通过电子网络进行的商品和服务交易活动", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "epoxy_resin", "canonical_name_zh": "环氧树脂", "canonical_name_en": "epoxy resin", "entity_type": "material", "aliases": [], "definition": "含有环氧基团的高分子聚合物，广泛用作涂料、胶粘剂和复合材料基体", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "telecommunication", "canonical_name_zh": "电信", "canonical_name_en": "telecommunication", "entity_type": "service", "aliases": [], "definition": "利用有线、无线、光纤等通信技术进行信息传输的服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "pharmaceutical_api", "canonical_name_zh": "原料药", "canonical_name_en": "active pharmaceutical ingredient", "entity_type": "material", "aliases": ["API"], "definition": "用于药品制造的活性化学成分", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "mining", "canonical_name_zh": "采矿", "canonical_name_en": "mining", "entity_type": "service", "aliases": [], "definition": "从地壳中开采矿产资源的工业活动", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "real_estate", "canonical_name_zh": "房地产", "canonical_name_en": "real estate", "entity_type": "service", "aliases": [], "definition": "土地、建筑物及附属设施的开发、经营和管理活动", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "automotive", "canonical_name_zh": "汽车", "canonical_name_en": "automotive", "entity_type": "system", "aliases": [], "definition": "以动力驱动的道路车辆及其零部件的制造和销售产业", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "mining_equipment", "canonical_name_zh": "矿山机械", "canonical_name_en": "mining equipment", "entity_type": "device", "aliases": [], "definition": "用于矿山开采、选矿和运输的机械设备", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "aerospace", "canonical_name_zh": "航空航天", "canonical_name_en": "aerospace", "entity_type": "service", "aliases": [], "definition": "航空器和航天器的研发、制造和运营活动", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "metal_fabrication", "canonical_name_zh": "金属加工", "canonical_name_en": "metal fabrication", "entity_type": "service", "aliases": [], "definition": "对金属材料进行切割、成型、焊接和组装的加工活动", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "sports_equipment", "canonical_name_zh": "体育器材", "canonical_name_en": "sports equipment", "entity_type": "device", "aliases": [], "definition": "用于体育运动和健身活动的各类器材和装备", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "railway", "canonical_name_zh": "铁路", "canonical_name_en": "railway", "entity_type": "service", "aliases": [], "definition": "以轨道为基础的交通运输系统", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "logistics", "canonical_name_zh": "物流", "canonical_name_en": "logistics", "entity_type": "service", "aliases": [], "definition": "物品从供应地向接收地的实体流动过程及相关服务", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
    {"node_id": "steel", "canonical_name_zh": "钢铁", "canonical_name_en": "steel", "entity_type": "material", "aliases": [], "definition": "以铁为主要成分，含碳量一般在0.02%至2.11%之间的合金材料", "status": "ACTIVE", "confidence": "HIGH", "evidence": ev("产业分类")},
]

graph = {
    "batch_id": "fix_missing_nodes_121_125",
    "task_description": "Fix missing infrastructure nodes for batches 121-125",
    "nodes_to_upsert": nodes,
    "edges_to_upsert": []
}

path = os.path.join(BASE_DIR, "tmp_script", "fix_missing_nodes_121_125.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(graph, f, ensure_ascii=False, indent=2)

print(f"Fix batch: {len(nodes)} nodes written")
