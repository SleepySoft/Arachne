import asyncio
import httpx

BATCH = {
    "batch_id": "semiconductor_companies_batch_002",
    "task_description": "录入全球主要半导体公司及其产业节点暴露关系（第二批：海外龙头）",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": [
        # 代工 / IDM
        {"company_id": "tsmc", "name_zh": "台积电", "name_en": "Taiwan Semiconductor Manufacturing Company", "stock_codes": ["2330.TW", "TSM"], "country": "TW", "company_type": "public", "description": "全球最大晶圆代工厂"},
        {"company_id": "samsung_electronics", "name_zh": "三星电子", "name_en": "Samsung Electronics", "stock_codes": ["005930.KS"], "country": "KR", "company_type": "public", "description": "存储、代工、CIS 等综合半导体巨头"},
        {"company_id": "intel", "name_zh": "英特尔", "name_en": "Intel Corporation", "stock_codes": ["INTC"], "country": "US", "company_type": "public", "description": "CPU 龙头，IDM/代工"},
        {"company_id": "globalfoundries", "name_zh": "格芯", "name_en": "GlobalFoundries", "stock_codes": ["GFS"], "country": "US", "company_type": "public", "description": "晶圆代工"},
        {"company_id": "umc", "name_zh": "联电", "name_en": "United Microelectronics Corporation", "stock_codes": ["2303.TW"], "country": "TW", "company_type": "public", "description": "晶圆代工"},
        {"company_id": "tower_semiconductor", "name_zh": "高塔半导体", "name_en": "Tower Semiconductor", "stock_codes": ["TSEM"], "country": "IL", "company_type": "public", "description": "特色工艺代工"},

        # 设备
        {"company_id": "asml", "name_zh": "阿斯麦", "name_en": "ASML Holding", "stock_codes": ["ASML"], "country": "NL", "company_type": "public", "description": "EUV/DUV 光刻机龙头"},
        {"company_id": "applied_materials", "name_zh": "应用材料", "name_en": "Applied Materials", "stock_codes": ["AMAT"], "country": "US", "company_type": "public", "description": "半导体设备平台龙头"},
        {"company_id": "lam_research", "name_zh": "泛林半导体", "name_en": "Lam Research", "stock_codes": ["LRCX"], "country": "US", "company_type": "public", "description": "刻蚀、沉积、清洗设备"},
        {"company_id": "kla", "name_zh": "科磊", "name_en": "KLA Corporation", "stock_codes": ["KLAC"], "country": "US", "company_type": "public", "description": "量测/检测设备"},
        {"company_id": "tel", "name_zh": "东京电子", "name_en": "Tokyo Electron", "stock_codes": ["8035.T"], "country": "JP", "company_type": "public", "description": "涂胶显影、沉积、清洗设备"},
        {"company_id": "screen", "name_zh": "迪恩士", "name_en": "SCREEN Holdings", "stock_codes": ["7735.T"], "country": "JP", "company_type": "public", "description": "清洗设备"},
        {"company_id": "advantest", "name_zh": "爱德万", "name_en": "Advantest", "stock_codes": ["6857.T"], "country": "JP", "company_type": "public", "description": "半导体测试设备"},
        {"company_id": "teradyne", "name_zh": "泰瑞达", "name_en": "Teradyne", "stock_codes": ["TER"], "country": "US", "company_type": "public", "description": "半导体测试设备"},
        {"company_id": "nikon", "name_zh": "尼康", "name_en": "Nikon", "stock_codes": ["7731.T"], "country": "JP", "company_type": "public", "description": "DUV 光刻机"},
        {"company_id": "canon", "name_zh": "佳能", "name_en": "Canon", "stock_codes": ["7751.T"], "country": "JP", "company_type": "public", "description": "DUV/封装光刻机、CIS"},

        # 材料
        {"company_id": "shin_etsu", "name_zh": "信越化学", "name_en": "Shin-Etsu Chemical", "stock_codes": ["4063.T"], "country": "JP", "company_type": "public", "description": "全球第一大硅片、光刻胶"},
        {"company_id": "sumco", "name_zh": "胜高", "name_en": "SUMCO", "stock_codes": ["3436.T"], "country": "JP", "company_type": "public", "description": "12 英寸硅片"},
        {"company_id": "jsr", "name_zh": "JSR", "name_en": "JSR Corporation", "stock_codes": ["4185.T"], "country": "JP", "company_type": "public", "description": "光刻胶龙头"},
        {"company_id": "tok", "name_zh": "东京应化", "name_en": "Tokyo Ohka Kogyo", "stock_codes": ["4186.T"], "country": "JP", "company_type": "public", "description": "光刻胶"},
        {"company_id": "entegris", "name_zh": "英特格", "name_en": "Entegris", "stock_codes": ["ENTG"], "country": "US", "company_type": "public", "description": "特种材料、化学品、气体输送"},
        {"company_id": "linde", "name_zh": "林德", "name_en": "Linde plc", "stock_codes": ["LIN"], "country": "IE", "company_type": "public", "description": "电子特气"},
        {"company_id": "air_liquide", "name_zh": "液化空气", "name_en": "Air Liquide", "stock_codes": ["AI.PA"], "country": "FR", "company_type": "public", "description": "电子大宗/特种气体"},

        # 设计 - CPU/GPU/AI/FPGA
        {"company_id": "nvidia", "name_zh": "英伟达", "name_en": "NVIDIA Corporation", "stock_codes": ["NVDA"], "country": "US", "company_type": "public", "description": "GPU / AI 加速器龙头"},
        {"company_id": "amd", "name_zh": "超威半导体", "name_en": "Advanced Micro Devices", "stock_codes": ["AMD"], "country": "US", "company_type": "public", "description": "CPU / GPU / FPGA"},
        {"company_id": "qualcomm", "name_zh": "高通", "name_en": "Qualcomm", "stock_codes": ["QCOM"], "country": "US", "company_type": "public", "description": "移动 SoC / 射频"},
        {"company_id": "broadcom", "name_zh": "博通", "name_en": "Broadcom", "stock_codes": ["AVGO"], "country": "US", "company_type": "public", "description": "网络/存储/射频芯片"},
        {"company_id": "marvell", "name_zh": "美满电子", "name_en": "Marvell Technology", "stock_codes": ["MRVL"], "country": "US", "company_type": "public", "description": "网络/存储/定制芯片"},
        {"company_id": "mediatek", "name_zh": "联发科", "name_en": "MediaTek", "stock_codes": ["2454.TW"], "country": "TW", "company_type": "public", "description": "移动 SoC"},
        {"company_id": "lattice", "name_zh": "莱迪思", "name_en": "Lattice Semiconductor", "stock_codes": ["LSCC"], "country": "US", "company_type": "public", "description": "FPGA"},
        {"company_id": "hisilicon", "name_zh": "海思半导体", "name_en": "HiSilicon", "stock_codes": [], "country": "CN", "company_type": "private", "description": "华为子公司，手机 SoC / AI / 基站 / 服务器芯片"},

        # 存储
        {"company_id": "sk_hynix", "name_zh": "SK 海力士", "name_en": "SK Hynix", "stock_codes": ["000660.KS"], "country": "KR", "company_type": "public", "description": "DRAM / NAND / HBM"},
        {"company_id": "micron", "name_zh": "美光科技", "name_en": "Micron Technology", "stock_codes": ["MU"], "country": "US", "company_type": "public", "description": "DRAM / NAND"},
        {"company_id": "kioxia", "name_zh": "铠侠", "name_en": "Kioxia", "stock_codes": [], "country": "JP", "company_type": "private", "description": "NAND Flash"},

        # CIS / 传感器
        {"company_id": "sony", "name_zh": "索尼", "name_en": "Sony Group", "stock_codes": ["6758.T"], "country": "JP", "company_type": "public", "description": "CIS 龙头"},
        {"company_id": "on_semi", "name_zh": "安森美", "name_en": "ON Semiconductor", "stock_codes": ["ON"], "country": "US", "company_type": "public", "description": "CIS / 功率 / 传感器"},

        # 模拟 / PMIC / 射频
        {"company_id": "texas_instruments", "name_zh": "德州仪器", "name_en": "Texas Instruments", "stock_codes": ["TXN"], "country": "US", "company_type": "public", "description": "模拟 / PMIC"},
        {"company_id": "adi", "name_zh": "亚德诺", "name_en": "Analog Devices", "stock_codes": ["ADI"], "country": "US", "company_type": "public", "description": "模拟 / 信号链"},
        {"company_id": "infineon", "name_zh": "英飞凌", "name_en": "Infineon Technologies", "stock_codes": ["IFNNY"], "country": "DE", "company_type": "public", "description": "汽车/工业 MCU / 功率 / PMIC"},
        {"company_id": "stmicroelectronics", "name_zh": "意法半导体", "name_en": "STMicroelectronics", "stock_codes": ["STM"], "country": "CH", "company_type": "public", "description": "MCU / 功率 / 模拟 / 传感器"},
        {"company_id": "nxp", "name_zh": "恩智浦", "name_en": "NXP Semiconductors", "stock_codes": ["NXPI"], "country": "NL", "company_type": "public", "description": "汽车/工业 MCU / 模拟 / PMIC"},
        {"company_id": "renesas", "name_zh": "瑞萨电子", "name_en": "Renesas Electronics", "stock_codes": ["6723.T"], "country": "JP", "company_type": "public", "description": "汽车 MCU / SoC / 功率"},
        {"company_id": "skyworks", "name_zh": "思佳讯", "name_en": "Skyworks Solutions", "stock_codes": ["SWKS"], "country": "US", "company_type": "public", "description": "射频前端"},
        {"company_id": "qorvo", "name_zh": "威讯", "name_en": "Qorvo", "stock_codes": ["QRVO"], "country": "US", "company_type": "public", "description": "射频前端"},

        # 功率半导体
        {"company_id": "wolfspeed", "name_zh": "狼速", "name_en": "Wolfspeed", "stock_codes": ["WOLF"], "country": "US", "company_type": "public", "description": "SiC 衬底/器件"},
        {"company_id": "rohm", "name_zh": "罗姆", "name_en": "Rohm", "stock_codes": ["6963.T"], "country": "JP", "company_type": "public", "description": "SiC / IGBT"},

        # EDA / IP
        {"company_id": "synopsys", "name_zh": "新思科技", "name_en": "Synopsys", "stock_codes": ["SNPS"], "country": "US", "company_type": "public", "description": "数字/模拟/验证 EDA 全流程"},
        {"company_id": "cadence", "name_zh": "楷登电子", "name_en": "Cadence Design Systems", "stock_codes": ["CDNS"], "country": "US", "company_type": "public", "description": "数字/模拟/验证 EDA"},
        {"company_id": "arm", "name_zh": "安谋控股", "name_en": "Arm Holdings", "stock_codes": ["ARM"], "country": "GB", "company_type": "public", "description": "CPU IP 架构授权"},

        # 封测
        {"company_id": "ase", "name_zh": "日月光", "name_en": "ASE Technology Holding", "stock_codes": ["3711.TW"], "country": "TW", "company_type": "public", "description": "全球最大 OSAT"},
        {"company_id": "amkor", "name_zh": "安靠科技", "name_en": "Amkor Technology", "stock_codes": ["AMKR"], "country": "US", "company_type": "public", "description": "全球第二大 OSAT"},
    ],
    "company_node_exposures_to_upsert": [
        # 代工 / IDM
        {"exposure_id": "tsmc_founds", "company_id": "tsmc", "node_id": "foundry", "activity_type": "manufacture", "role": "全球最大晶圆代工厂", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "台积电是全球最大晶圆代工"}]},
        {"exposure_id": "tsmc_advanced", "company_id": "tsmc", "node_id": "advanced_process_node", "activity_type": "manufacture", "role": "先进制程代工", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "台积电先进制程代工"}]},
        {"exposure_id": "samsung_founds", "company_id": "samsung_electronics", "node_id": "foundry", "activity_type": "manufacture", "role": "存储、代工、CIS 综合巨头", "weight": 0.8, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "三星电子存储、代工、CIS"}]},
        {"exposure_id": "samsung_memory", "company_id": "samsung_electronics", "node_id": "memory_chip", "activity_type": "produce", "role": "DRAM / NAND 龙头", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "三星电子存储龙头"}]},
        {"exposure_id": "samsung_cis", "company_id": "samsung_electronics", "node_id": "cis", "activity_type": "produce", "role": "CIS", "weight": 0.8, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "三星电子 CIS"}]},
        {"exposure_id": "intel_cpu", "company_id": "intel", "node_id": "cpu", "activity_type": "produce", "role": "CPU 龙头", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "英特尔 CPU 龙头"}]},
        {"exposure_id": "intel_gpu", "company_id": "intel", "node_id": "gpu", "activity_type": "produce", "role": "GPU", "weight": 0.7, "confidence": "MEDIUM", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "英特尔 GPU"}]},
        {"exposure_id": "intel_idm", "company_id": "intel", "node_id": "idm", "activity_type": "manufacture", "role": "IDM/代工", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "英特尔 IDM/代工"}]},
        {"exposure_id": "globalfoundries_founds", "company_id": "globalfoundries", "node_id": "foundry", "activity_type": "manufacture", "role": "晶圆代工", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "格芯晶圆代工"}]},
        {"exposure_id": "umc_founds", "company_id": "umc", "node_id": "foundry", "activity_type": "manufacture", "role": "晶圆代工", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "联电晶圆代工"}]},
        {"exposure_id": "tower_founds", "company_id": "tower_semiconductor", "node_id": "foundry", "activity_type": "manufacture", "role": "特色工艺代工", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "高塔半导体特色工艺代工"}]},

        # 设备
        {"exposure_id": "asml_lithography", "company_id": "asml", "node_id": "lithography_machine", "activity_type": "produce", "role": "EUV/DUV 光刻机垄断", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "ASML EUV/DUV 光刻机垄断"}]},
        {"exposure_id": "amat_equipment", "company_id": "applied_materials", "node_id": "cvd_equipment", "activity_type": "produce", "role": "CVD/PVD/刻蚀/CMP/离子注入/量测综合平台", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "应用材料刻蚀、沉积、CMP、离子注入、量测"}]},
        {"exposure_id": "amat_pvd", "company_id": "applied_materials", "node_id": "pvd_equipment", "activity_type": "produce", "role": "PVD 设备", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "应用材料 PVD 设备"}]},
        {"exposure_id": "amat_etching", "company_id": "applied_materials", "node_id": "etching_machine", "activity_type": "produce", "role": "刻蚀设备", "weight": 0.8, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "应用材料刻蚀设备"}]},
        {"exposure_id": "lam_etching", "company_id": "lam_research", "node_id": "etching_machine", "activity_type": "produce", "role": "刻蚀设备龙头", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "泛林半导体刻蚀、沉积、清洗"}]},
        {"exposure_id": "lam_cvd", "company_id": "lam_research", "node_id": "cvd_equipment", "activity_type": "produce", "role": "CVD 设备", "weight": 0.9, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "泛林半导体 CVD 设备"}]},
        {"exposure_id": "kla_metrology", "company_id": "kla", "node_id": "metrology_equipment", "activity_type": "produce", "role": "量测/检测设备龙头", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "科磊量测/检测设备"}]},
        {"exposure_id": "tel_track", "company_id": "tel", "node_id": "track_coater_developer", "activity_type": "produce", "role": "涂胶显影设备", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "东京电子涂胶显影、沉积、清洗设备"}]},
        {"exposure_id": "tel_cvd", "company_id": "tel", "node_id": "cvd_equipment", "activity_type": "produce", "role": "CVD 设备", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "东京电子沉积设备"}]},
        {"exposure_id": "tel_ald", "company_id": "tel", "node_id": "ald_equipment", "activity_type": "produce", "role": "ALD 设备", "weight": 0.9, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "东京电子 ALD 设备"}]},
        {"exposure_id": "screen_cleaning", "company_id": "screen", "node_id": "cleaning_equipment", "activity_type": "produce", "role": "清洗设备", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "迪恩士清洗设备"}]},
        {"exposure_id": "advantest_test", "company_id": "advantest", "node_id": "metrology_equipment", "activity_type": "produce", "role": "半导体测试设备", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "爱德万半导体测试设备"}]},
        {"exposure_id": "teradyne_test", "company_id": "teradyne", "node_id": "metrology_equipment", "activity_type": "produce", "role": "半导体测试设备", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "泰瑞达半导体测试设备"}]},
        {"exposure_id": "nikon_lithography", "company_id": "nikon", "node_id": "lithography_machine", "activity_type": "produce", "role": "DUV 光刻机", "weight": 0.8, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "尼康 DUV 光刻机"}]},
        {"exposure_id": "canon_lithography", "company_id": "canon", "node_id": "lithography_machine", "activity_type": "produce", "role": "DUV/封装光刻机", "weight": 0.7, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "佳能 DUV/封装光刻机"}]},

        # 材料
        {"exposure_id": "shinetsu_wafer", "company_id": "shin_etsu", "node_id": "silicon_wafer", "activity_type": "produce", "role": "全球第一大硅片", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "信越化学全球第一大硅片"}]},
        {"exposure_id": "shinetsu_photoresist", "company_id": "shin_etsu", "node_id": "photoresist", "activity_type": "produce", "role": "光刻胶", "weight": 0.8, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "信越化学光刻胶"}]},
        {"exposure_id": "sumco_wafer", "company_id": "sumco", "node_id": "silicon_wafer", "activity_type": "produce", "role": "12 英寸硅片", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "胜高 12 英寸硅片"}]},
        {"exposure_id": "jsr_photoresist", "company_id": "jsr", "node_id": "euv_photoresist", "activity_type": "produce", "role": "EUV 光刻胶龙头", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "JSR 光刻胶龙头"}]},
        {"exposure_id": "jsr_duv", "company_id": "jsr", "node_id": "duv_photoresist", "activity_type": "produce", "role": "DUV 光刻胶", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "JSR DUV 光刻胶"}]},
        {"exposure_id": "tok_photoresist", "company_id": "tok", "node_id": "photoresist", "activity_type": "produce", "role": "光刻胶", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "东京应化光刻胶"}]},
        {"exposure_id": "entegris_materials", "company_id": "entegris", "node_id": "wet_chemicals", "activity_type": "produce", "role": "特种化学品、材料", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "英特格特种材料、化学品"}]},
        {"exposure_id": "linde_gas", "company_id": "linde", "node_id": "electronic_special_gases", "activity_type": "produce", "role": "电子特气", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "林德电子特气"}]},
        {"exposure_id": "airliquide_gas", "company_id": "air_liquide", "node_id": "electronic_special_gases", "activity_type": "produce", "role": "电子大宗/特种气体", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "液化空气电子大宗/特种气体"}]},

        # 设计 - CPU/GPU/AI/FPGA
        {"exposure_id": "nvidia_gpu", "company_id": "nvidia", "node_id": "gpu", "activity_type": "produce", "role": "GPU / AI 加速器龙头", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "英伟达 GPU / AI 加速器"}]},
        {"exposure_id": "nvidia_ai", "company_id": "nvidia", "node_id": "ai_accelerator", "activity_type": "produce", "role": "AI 加速器", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "英伟达 AI 加速器"}]},
        {"exposure_id": "amd_cpu", "company_id": "amd", "node_id": "cpu", "activity_type": "produce", "role": "CPU", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "AMD CPU"}]},
        {"exposure_id": "amd_gpu", "company_id": "amd", "node_id": "gpu", "activity_type": "produce", "role": "GPU", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "AMD GPU"}]},
        {"exposure_id": "amd_fpga", "company_id": "amd", "node_id": "fpga", "activity_type": "produce", "role": "FPGA（原 Xilinx）", "weight": 0.9, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "AMD FPGA"}]},
        {"exposure_id": "qualcomm_soc", "company_id": "qualcomm", "node_id": "soc", "activity_type": "produce", "role": "移动 SoC", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "高通移动 SoC"}]},
        {"exposure_id": "qualcomm_rf", "company_id": "qualcomm", "node_id": "rf_chip", "activity_type": "produce", "role": "射频前端", "weight": 0.8, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "高通射频"}]},
        {"exposure_id": "broadcom_soc", "company_id": "broadcom", "node_id": "soc", "activity_type": "produce", "role": "网络/存储/射频芯片", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "博通网络/存储/射频芯片"}]},
        {"exposure_id": "marvell_soc", "company_id": "marvell", "node_id": "soc", "activity_type": "produce", "role": "网络/存储/定制芯片", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "美满电子网络/存储/定制芯片"}]},
        {"exposure_id": "mediatek_soc", "company_id": "mediatek", "node_id": "soc", "activity_type": "produce", "role": "移动 SoC", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "联发科移动 SoC"}]},
        {"exposure_id": "lattice_fpga", "company_id": "lattice", "node_id": "fpga", "activity_type": "produce", "role": "FPGA", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "莱迪思 FPGA"}]},
        {"exposure_id": "hisilicon_soc", "company_id": "hisilicon", "node_id": "soc", "activity_type": "produce", "role": "手机 SoC / AI / 基站 / 服务器芯片", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "海思半导体手机 SoC / AI / 基站 / 服务器芯片"}]},
        {"exposure_id": "hisilicon_ai", "company_id": "hisilicon", "node_id": "ai_accelerator", "activity_type": "produce", "role": "AI 芯片", "weight": 0.9, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "海思 AI 芯片"}]},

        # 存储
        {"exposure_id": "skhynix_memory", "company_id": "sk_hynix", "node_id": "memory_chip", "activity_type": "produce", "role": "DRAM / NAND / HBM", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "SK 海力士 DRAM / NAND / HBM"}]},
        {"exposure_id": "micron_memory", "company_id": "micron", "node_id": "memory_chip", "activity_type": "produce", "role": "DRAM / NAND", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "美光科技 DRAM / NAND"}]},
        {"exposure_id": "kioxia_nand", "company_id": "kioxia", "node_id": "nand_flash_chip", "activity_type": "produce", "role": "NAND Flash", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "铠侠 NAND Flash"}]},

        # CIS
        {"exposure_id": "sony_cis", "company_id": "sony", "node_id": "cis", "activity_type": "produce", "role": "CIS 龙头", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "索尼 CIS 龙头"}]},
        {"exposure_id": "onsemi_cis", "company_id": "on_semi", "node_id": "cis", "activity_type": "produce", "role": "CIS / 功率 / 传感器", "weight": 0.8, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "安森美 CIS"}]},
        {"exposure_id": "onsemi_power", "company_id": "on_semi", "node_id": "power_semiconductor", "activity_type": "produce", "role": "功率半导体", "weight": 0.9, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "安森美功率半导体"}]},

        # 模拟 / PMIC / 射频
        {"exposure_id": "ti_analog", "company_id": "texas_instruments", "node_id": "analog_chip", "activity_type": "produce", "role": "模拟芯片龙头", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "德州仪器模拟芯片"}]},
        {"exposure_id": "ti_pmic", "company_id": "texas_instruments", "node_id": "pmic", "activity_type": "produce", "role": "PMIC", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "德州仪器 PMIC"}]},
        {"exposure_id": "adi_analog", "company_id": "adi", "node_id": "analog_chip", "activity_type": "produce", "role": "模拟 / 信号链", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "亚德诺模拟 / 信号链"}]},
        {"exposure_id": "infineon_power", "company_id": "infineon", "node_id": "power_semiconductor", "activity_type": "produce", "role": "IGBT / SiC / PMIC", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "英飞凌功率半导体"}]},
        {"exposure_id": "infineon_pmic", "company_id": "infineon", "node_id": "pmic", "activity_type": "produce", "role": "PMIC", "weight": 0.8, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "英飞凌 PMIC"}]},
        {"exposure_id": "st_power", "company_id": "stmicroelectronics", "node_id": "power_semiconductor", "activity_type": "produce", "role": "SiC / IGBT / MCU", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "意法半导体功率半导体"}]},
        {"exposure_id": "st_mcu", "company_id": "stmicroelectronics", "node_id": "mcu", "activity_type": "produce", "role": "MCU", "weight": 0.9, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "意法半导体 MCU"}]},
        {"exposure_id": "nxp_mcu", "company_id": "nxp", "node_id": "mcu", "activity_type": "produce", "role": "汽车/工业 MCU", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "恩智浦 MCU"}]},
        {"exposure_id": "nxp_pmic", "company_id": "nxp", "node_id": "pmic", "activity_type": "produce", "role": "PMIC", "weight": 0.8, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "恩智浦 PMIC"}]},
        {"exposure_id": "renesas_mcu", "company_id": "renesas", "node_id": "mcu", "activity_type": "produce", "role": "汽车 MCU", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "瑞萨电子汽车 MCU"}]},
        {"exposure_id": "renesas_power", "company_id": "renesas", "node_id": "power_semiconductor", "activity_type": "produce", "role": "功率半导体", "weight": 0.8, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "瑞萨电子功率半导体"}]},
        {"exposure_id": "skyworks_rf", "company_id": "skyworks", "node_id": "rf_chip", "activity_type": "produce", "role": "射频前端", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "思佳讯射频前端"}]},
        {"exposure_id": "qorvo_rf", "company_id": "qorvo", "node_id": "rf_chip", "activity_type": "produce", "role": "射频前端", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "威讯射频前端"}]},

        # 功率半导体
        {"exposure_id": "wolfspeed_sic", "company_id": "wolfspeed", "node_id": "power_semiconductor", "activity_type": "produce", "role": "SiC 衬底/器件", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "狼速 SiC 衬底/器件"}]},
        {"exposure_id": "rohm_power", "company_id": "rohm", "node_id": "power_semiconductor", "activity_type": "produce", "role": "SiC / IGBT", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "罗姆 SiC / IGBT"}]},

        # EDA / IP
        {"exposure_id": "synopsys_eda", "company_id": "synopsys", "node_id": "eda_software", "activity_type": "provide_service", "role": "数字/模拟/验证 EDA 全流程", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "新思科技 EDA 全流程"}]},
        {"exposure_id": "cadence_eda", "company_id": "cadence", "node_id": "eda_software", "activity_type": "provide_service", "role": "数字/模拟/验证 EDA", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "楷登电子 EDA"}]},
        {"exposure_id": "arm_ip", "company_id": "arm", "node_id": "ip_core", "activity_type": "provide_service", "role": "CPU IP 架构授权", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "安谋控股 CPU IP"}]},

        # 封测
        {"exposure_id": "ase_osat", "company_id": "ase", "node_id": "osat", "activity_type": "manufacture", "role": "全球最大 OSAT", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "日月光全球最大 OSAT"}]},
        {"exposure_id": "amkor_osat", "company_id": "amkor", "node_id": "osat", "activity_type": "manufacture", "role": "全球第二大 OSAT", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "安靠科技全球第二大 OSAT"}]},
    ],
}


async def main():
    async with httpx.AsyncClient() as client:
        r = await client.post("http://localhost:16060/api/v1/business-batches", json=BATCH)
        print(r.status_code)
        print(r.json())


asyncio.run(main())
