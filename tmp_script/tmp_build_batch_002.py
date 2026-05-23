"""
Batch 002 产业图与公司视图构建脚本 - Part 3
公司和暴露关系定义 + 提交逻辑
"""

import os
import sys
sys.path.insert(0, 'backend')

import json
import asyncio
import httpx
from datetime import datetime, date

API_BASE = "http://localhost:8000/api/v1"

# ============================================================
# 公司定义（Company）
# ============================================================

COMPANIES = []

COMPANIES.append({
    "company_id": "shahe_property",
    "name_zh": "沙河实业股份有限公司",
    "name_en": "Shahe Industrial Co., Ltd.",
    "aliases": ["沙河股份"],
    "stock_codes": ["000014.SZ"],
    "description": "深圳本地房地产开发企业，主要从事房地产开发经营、物业租赁和物业管理业务。",
    "country": "CN",
    "province": "广东",
    "city": "深圳",
    "founded_year": 1987,
    "employee_count": 73,
    "company_type": "public",
    "status": "ACTIVE",
    "notes": "batch_002 录入"
})

COMPANIES.append({
    "company_id": "konka_group",
    "name_zh": "康佳集团股份有限公司",
    "name_en": "Konka Group Co., Ltd.",
    "aliases": ["*ST康佳A", "康佳"],
    "stock_codes": ["000016.SZ"],
    "description": "中国老牌家电企业，主要从事彩电、白电、半导体及PCB业务的研发、生产和销售。",
    "country": "CN",
    "province": "广东",
    "city": "深圳",
    "founded_year": 1980,
    "employee_count": 13358,
    "company_type": "public",
    "status": "ACTIVE",
    "notes": "batch_002 录入；2024年亏损35.35亿元"
})

COMPANIES.append({
    "company_id": "shenzhonghua_a",
    "name_zh": "深圳中华自行车(集团)股份有限公司",
    "name_en": "Shenzhen China Bicycle (Group) Co., Ltd.",
    "aliases": ["深中华A"],
    "stock_codes": ["000017.SZ"],
    "description": "业务涵盖珠宝黄金、自行车及新能源锂电池材料的生产和销售。",
    "country": "CN",
    "province": "广东",
    "city": "深圳",
    "founded_year": 1984,
    "employee_count": 81,
    "company_type": "public",
    "status": "ACTIVE",
    "notes": "batch_002 录入"
})

COMPANIES.append({
    "company_id": "shenliang_holdings",
    "name_zh": "深圳市深粮控股股份有限公司",
    "name_en": "Shenzhen Shenliang Holdings Co., Ltd.",
    "aliases": ["深粮控股"],
    "stock_codes": ["000019.SZ"],
    "description": "深圳市属国有大型粮食企业，主营粮油贸易、仓储、加工及茶与食品原料业务。",
    "country": "CN",
    "province": "广东",
    "city": "深圳",
    "founded_year": 1981,
    "employee_count": 1162,
    "company_type": "state_owned",
    "status": "ACTIVE",
    "notes": "batch_002 录入"
})

COMPANIES.append({
    "company_id": "shenhuafa_a",
    "name_zh": "深圳中恒华发股份有限公司",
    "name_en": "Shenzhen Zhongheng Huafa Co., Ltd.",
    "aliases": ["深华发A"],
    "stock_codes": ["000020.SZ"],
    "description": "主要从事液晶显示器、注塑件、电路板等电子产品的生产，以及物业租赁业务。",
    "country": "CN",
    "province": "广东",
    "city": "深圳",
    "founded_year": 1981,
    "employee_count": 490,
    "company_type": "public",
    "status": "ACTIVE",
    "notes": "batch_002 录入"
})

COMPANIES.append({
    "company_id": "shenzhen_kaifa",
    "name_zh": "深圳长城开发科技股份有限公司",
    "name_en": "Shenzhen Kaifa Technology Co., Ltd.",
    "aliases": ["深科技"],
    "stock_codes": ["000021.SZ"],
    "description": "全球领先的电子制造服务企业，核心业务为存储半导体封测、高端制造和计量智能终端。",
    "country": "CN",
    "province": "广东",
    "city": "深圳",
    "founded_year": 1985,
    "employee_count": 20330,
    "company_type": "state_owned",
    "status": "ACTIVE",
    "notes": "batch_002 录入；长鑫存储核心封测厂商"
})

COMPANIES.append({
    "company_id": "cms_port",
    "name_zh": "招商局港口集团股份有限公司",
    "name_en": "China Merchants Port Group Co., Ltd.",
    "aliases": ["招商港口"],
    "stock_codes": ["001872.SZ"],
    "description": "中国领先的港口投资、开发和运营商，主要从事集装箱和散杂货的港口装卸、仓储及运输服务。",
    "country": "CN",
    "province": "广东",
    "city": "深圳",
    "founded_year": 1990,
    "employee_count": 15013,
    "company_type": "state_owned",
    "status": "ACTIVE",
    "notes": "batch_002 录入"
})

COMPANIES.append({
    "company_id": "teli_a",
    "name_zh": "深圳市特力(集团)股份有限公司",
    "name_en": "Shenzhen Teli (Group) Co., Ltd.",
    "aliases": ["特力A"],
    "stock_codes": ["000025.SZ"],
    "description": "业务涵盖珠宝首饰商业运营、汽车销售及维修保养、物业租赁等综合服务。",
    "country": "CN",
    "province": "广东",
    "city": "深圳",
    "founded_year": 1986,
    "employee_count": 160,
    "company_type": "public",
    "status": "ACTIVE",
    "notes": "batch_002 录入"
})

COMPANIES.append({
    "company_id": "fiyta",
    "name_zh": "飞亚达精密科技股份有限公司",
    "name_en": "Fiyta Precision Technology Co., Ltd.",
    "aliases": ["飞亚达"],
    "stock_codes": ["000026.SZ"],
    "description": "中国钟表行业龙头企业，主要从事手表及零配件的设计开发、制造、销售和维修，以及世界名表商业连锁销售。",
    "country": "CN",
    "province": "广东",
    "city": "深圳",
    "founded_year": 1990,
    "employee_count": 3156,
    "company_type": "public",
    "status": "ACTIVE",
    "notes": "batch_002 录入；航空工业集团旗下"
})

COMPANIES.append({
    "company_id": "shenzhen_energy",
    "name_zh": "深圳能源集团股份有限公司",
    "name_en": "Shenzhen Energy Group Co., Ltd.",
    "aliases": ["深圳能源"],
    "stock_codes": ["000027.SZ"],
    "description": "深圳市属大型综合能源集团，业务涵盖煤电、气电、风电、光伏、水电、垃圾焚烧发电及城市燃气供应。",
    "country": "CN",
    "province": "广东",
    "city": "深圳",
    "founded_year": 1993,
    "employee_count": 12527,
    "company_type": "state_owned",
    "status": "ACTIVE",
    "notes": "batch_002 录入；清洁能源装机占比超75%"
})

# ============================================================
# 公司-产业节点暴露关系（CompanyNodeExposure）
# ============================================================

EXPOSURES = []

# ---- 沙河股份 ----
EXPOSURES.append({"exposure_id": "shahe_property_produce_residential_property", "company_id": "shahe_property", "node_id": "residential_property", "activity_type": "produce", "role": "商品住宅开发商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "沙河股份2024年年报", "quote": "在合法取得土地使用权范围内从事房地产开发经营业务"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "shahe_property_produce_commercial_property", "company_id": "shahe_property", "node_id": "commercial_property", "activity_type": "produce", "role": "商业地产开发商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "沙河股份2024年年报", "quote": "从事房地产开发经营业务；国内商业,物资供销业"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "shahe_property_operate_property_mgmt", "company_id": "shahe_property", "node_id": "property_management_service", "activity_type": "operate", "role": "物业管理服务商", "weight": 0.5, "confidence": "HIGH", "evidence": [{"source_title": "沙河股份2024年年报", "quote": "物业管理"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "shahe_property_provide_service_housing_rental", "company_id": "shahe_property", "node_id": "housing_rental_service", "activity_type": "provide_service", "role": "住房租赁运营商", "weight": 0.4, "confidence": "HIGH", "evidence": [{"source_title": "沙河股份2024年年报", "quote": "物业租赁业"}], "status": "ACTIVE"})

# ---- 康佳 ----
EXPOSURES.append({"exposure_id": "konka_produce_color_tv", "company_id": "konka_group", "node_id": "color_tv", "activity_type": "produce", "role": "彩色电视机制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "康佳2024年年报", "quote": "主要产品包括彩色电视机"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "konka_produce_refrigerator", "company_id": "konka_group", "node_id": "refrigerator", "activity_type": "produce", "role": "冰箱制造商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "康佳2024年年报", "quote": "生产经营冰箱"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "konka_produce_washing_machine", "company_id": "konka_group", "node_id": "washing_machine", "activity_type": "produce", "role": "洗衣机制造商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "康佳2024年年报", "quote": "生产经营洗衣机"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "konka_produce_pcb", "company_id": "konka_group", "node_id": "pcb_board", "activity_type": "produce", "role": "PCB制造商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "康佳2024年年报", "quote": "半导体PCB业务"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "konka_produce_semiconductor", "company_id": "konka_group", "node_id": "semiconductor_device", "activity_type": "produce", "role": "半导体器件生产商", "weight": 0.5, "confidence": "HIGH", "evidence": [{"source_title": "康佳2024年年报", "quote": "半导体业务"}], "status": "ACTIVE"})

# ---- 深中华A ----
EXPOSURES.append({"exposure_id": "shenzhonghua_produce_gold_jewelry", "company_id": "shenzhonghua_a", "node_id": "gold_jewelry", "activity_type": "produce", "role": "黄金珠宝制造商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "深中华A2024年年报", "quote": "主要业务为珠宝黄金业务"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "shenzhonghua_produce_bicycle", "company_id": "shenzhonghua_a", "node_id": "bicycle", "activity_type": "produce", "role": "自行车制造商", "weight": 0.3, "confidence": "HIGH", "evidence": [{"source_title": "深中华A2024年年报", "quote": "自行车及新能锂电池材料业务"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "shenzhonghua_produce_electric_bicycle", "company_id": "shenzhonghua_a", "node_id": "electric_bicycle", "activity_type": "produce", "role": "电动自行车制造商", "weight": 0.4, "confidence": "HIGH", "evidence": [{"source_title": "深中华A2024年年报", "quote": "研发生产电动自行车、电动摩托车"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "shenzhonghua_produce_lithium_anode", "company_id": "shenzhonghua_a", "node_id": "lithium_battery_anode", "activity_type": "produce", "role": "锂电池负极材料生产商", "weight": 0.3, "confidence": "HIGH", "evidence": [{"source_title": "深中华A2024年年报", "quote": "新能锂电池材料业务"}], "status": "ACTIVE"})

# ---- 深粮控股 ----
EXPOSURES.append({"exposure_id": "shenliang_operate_grain_storage", "company_id": "shenliang_holdings", "node_id": "grain_storage_service", "activity_type": "operate", "role": "粮食仓储运营商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "深粮控股2024年年报", "quote": "粮油储备；仓储服务；粮食流通服务"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "shenliang_operate_grain_processing", "company_id": "shenliang_holdings", "node_id": "grain_processing", "activity_type": "operate", "role": "粮食加工商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "深粮控股2024年年报", "quote": "粮油及制品经营及加工"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "shenliang_produce_grain_oil", "company_id": "shenliang_holdings", "node_id": "grain_oil", "activity_type": "produce", "role": "粮油产品供应商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "深粮控股2024年年报", "quote": "粮油贸易、粮油加工等粮油流通及粮油储备服务业务"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "shenliang_produce_tea", "company_id": "shenliang_holdings", "node_id": "tea", "activity_type": "produce", "role": "茶叶生产商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "深粮控股2024年年报", "quote": "生产茶叶、茶制品、茶及天然植物提取物"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "shenliang_produce_food_ingredient", "company_id": "shenliang_holdings", "node_id": "food_ingredient", "activity_type": "produce", "role": "食品原料及配料生产商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "深粮控股2024年年报", "quote": "食品原料(配料)生产、研发和销售业务"}], "status": "ACTIVE"})

# ---- 深华发A ----
EXPOSURES.append({"exposure_id": "shenhuafa_produce_lcd_monitor", "company_id": "shenhuafa_a", "node_id": "lcd_monitor", "activity_type": "produce", "role": "液晶显示器制造商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "深华发A2024年年报", "quote": "生产经营液晶显示器"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "shenhuafa_produce_injection_molding", "company_id": "shenhuafa_a", "node_id": "injection_molding_part", "activity_type": "produce", "role": "注塑件制造商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "深华发A2024年年报", "quote": "注塑件"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "shenhuafa_produce_pcb", "company_id": "shenhuafa_a", "node_id": "pcb_board", "activity_type": "produce", "role": "电路板制造商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "深华发A2024年年报", "quote": "生产经营印刷线路板"}], "status": "ACTIVE"})

# ---- 深科技 ----
EXPOSURES.append({"exposure_id": "shenzhen_kaifa_produce_dram", "company_id": "shenzhen_kaifa", "node_id": "dram_chip", "activity_type": "produce", "role": "DRAM芯片封测商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "深科技2024年年报", "quote": "产品包括DRAM、NAND Flash以及嵌入式存储芯片"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "shenzhen_kaifa_produce_nand", "company_id": "shenzhen_kaifa", "node_id": "nand_flash_chip", "activity_type": "produce", "role": "NAND Flash芯片封测商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "深科技2024年年报", "quote": "产品包括NAND Flash"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "shenzhen_kaifa_produce_hard_disk_platter", "company_id": "shenzhen_kaifa", "node_id": "hard_disk_platter", "activity_type": "produce", "role": "硬盘盘片制造商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "深科技2024年年报", "quote": "盘基片业务"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "shenzhen_kaifa_produce_magnetic_head", "company_id": "shenzhen_kaifa", "node_id": "magnetic_head", "activity_type": "produce", "role": "硬盘磁头制造商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "深科技2024年年报", "quote": "硬盘磁头业务"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "shenzhen_kaifa_produce_smart_meter", "company_id": "shenzhen_kaifa", "node_id": "smart_meter", "activity_type": "produce", "role": "智能电表制造商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "深科技2024年年报", "quote": "计量智能终端；智能电表等"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "shenzhen_kaifa_produce_memory_dimm", "company_id": "shenzhen_kaifa", "node_id": "memory_dimm", "activity_type": "produce", "role": "存储模组制造商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "深科技历史业务", "quote": "中国知名的半导体存储模组制造企业"}], "status": "ACTIVE"})

# ---- 招商港口 ----
EXPOSURES.append({"exposure_id": "cms_port_operate_port", "company_id": "cms_port", "node_id": "port_operation_service", "activity_type": "operate", "role": "港口码头运营商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "招商港口2024年年报", "quote": "港口码头建设、管理和经营"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "cms_port_provide_container_handling", "company_id": "cms_port", "node_id": "container_handling_service", "activity_type": "provide_service", "role": "集装箱装卸服务商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "招商港口2024年年报", "quote": "主要从事集装箱的港口装卸"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "cms_port_provide_bonded", "company_id": "cms_port", "node_id": "bonded_warehousing_service", "activity_type": "provide_service", "role": "保税仓储服务商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "招商港口2024年年报", "quote": "进出口各类货物保税仓储业务"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "cms_port_provide_shipping", "company_id": "cms_port", "node_id": "shipping_service", "activity_type": "provide_service", "role": "航运及运输服务商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "招商港口2024年年报", "quote": "国际、国内货物的装卸、中转、仓储、运输"}], "status": "ACTIVE"})

# ---- 特力A ----
EXPOSURES.append({"exposure_id": "teli_provide_jewelry_retail", "company_id": "teli_a", "node_id": "jewelry_retail_service", "activity_type": "provide_service", "role": "珠宝零售运营商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "特力A2024年年报", "quote": "销售珠宝首饰及其原料、半成品；商业服务"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "teli_provide_automotive_sales", "company_id": "teli_a", "node_id": "automotive_sales_service", "activity_type": "provide_service", "role": "汽车销售服务商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "特力A2024年年报", "quote": "主营业务：汽车销售"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "teli_provide_automotive_maintenance", "company_id": "teli_a", "node_id": "automotive_maintenance_service", "activity_type": "provide_service", "role": "汽车维修保养服务商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "特力A2024年年报", "quote": "汽车检测维修及配件销售"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "teli_provide_automotive_inspection", "company_id": "teli_a", "node_id": "automotive_inspection_service", "activity_type": "provide_service", "role": "汽车检测服务商", "weight": 0.6, "confidence": "HIGH", "evidence": [{"source_title": "特力A2024年年报", "quote": "汽车检测维修"}], "status": "ACTIVE"})

# ---- 飞亚达 ----
EXPOSURES.append({"exposure_id": "fiyta_produce_watch", "company_id": "fiyta", "node_id": "watch", "activity_type": "produce", "role": "手表制造商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "飞亚达2024年年报", "quote": "钟表及其零配件的设计开发、制造、销售和维修"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "fiyta_produce_watch_movement", "company_id": "fiyta", "node_id": "watch_movement", "activity_type": "produce", "role": "自主机芯制造商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "飞亚达2024年年报", "quote": "手表自主机心"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "fiyta_produce_watch_component", "company_id": "fiyta", "node_id": "watch_component", "activity_type": "produce", "role": "钟表零部件制造商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "飞亚达2024年年报", "quote": "关键零部件研制"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "fiyta_provide_watch_retail", "company_id": "fiyta", "node_id": "watch_retail_service", "activity_type": "provide_service", "role": "世界名表连锁零售商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "飞亚达2024年年报", "quote": "世界名表的商业连锁销售"}], "status": "ACTIVE"})

# ---- 深圳能源 ----
EXPOSURES.append({"exposure_id": "shenzhen_energy_operate_coal_power", "company_id": "shenzhen_energy", "node_id": "coal_power_generation", "activity_type": "operate", "role": "燃煤发电运营商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "深圳能源2024年年报", "quote": "电力-煤电；燃煤热电"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "shenzhen_energy_operate_gas_power", "company_id": "shenzhen_energy", "node_id": "gas_power_generation", "activity_type": "operate", "role": "燃气发电运营商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "深圳能源2024年年报", "quote": "电力-气电"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "shenzhen_energy_operate_wind_power", "company_id": "shenzhen_energy", "node_id": "wind_power_generation", "activity_type": "operate", "role": "风力发电运营商", "weight": 0.8, "confidence": "HIGH", "evidence": [{"source_title": "深圳能源2024年年报", "quote": "电力-风电"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "shenzhen_energy_operate_solar_power", "company_id": "shenzhen_energy", "node_id": "solar_power_generation", "activity_type": "operate", "role": "光伏发电运营商", "weight": 0.75, "confidence": "HIGH", "evidence": [{"source_title": "深圳能源2024年年报", "quote": "电力-光伏"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "shenzhen_energy_operate_hydro_power", "company_id": "shenzhen_energy", "node_id": "hydro_power_generation", "activity_type": "operate", "role": "水力发电运营商", "weight": 0.7, "confidence": "HIGH", "evidence": [{"source_title": "深圳能源2024年年报", "quote": "电力-水电"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "shenzhen_energy_operate_waste_to_energy", "company_id": "shenzhen_energy", "node_id": "waste_to_energy", "activity_type": "operate", "role": "垃圾焚烧发电运营商", "weight": 0.85, "confidence": "HIGH", "evidence": [{"source_title": "深圳能源2024年年报", "quote": "固废处理；垃圾焚烧发电"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "shenzhen_energy_operate_city_gas", "company_id": "shenzhen_energy", "node_id": "city_gas_supply", "activity_type": "operate", "role": "城市燃气供应商", "weight": 0.9, "confidence": "HIGH", "evidence": [{"source_title": "深圳能源2024年年报", "quote": "城市燃气供应"}], "status": "ACTIVE"})
EXPOSURES.append({"exposure_id": "shenzhen_energy_produce_electricity", "company_id": "shenzhen_energy", "node_id": "electricity_power", "activity_type": "produce", "role": "电力生产商", "weight": 0.95, "confidence": "HIGH", "evidence": [{"source_title": "深圳能源2024年年报", "quote": "主要业务是各种常规能源和新能源的开发、生产、购销"}], "status": "ACTIVE"})

print(f"Companies: {len(COMPANIES)}")
print(f"Exposures: {len(EXPOSURES)}")
