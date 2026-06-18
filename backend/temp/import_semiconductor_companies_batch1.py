import asyncio
import httpx
from datetime import date

BATCH = {
    "batch_id": "semiconductor_companies_batch_001",
    "task_description": "录入半导体产业链核心公司及其产业节点暴露关系（第一批：制造/设备/材料/设计/封测龙头）",
    "industries_to_upsert": [],
    "industry_node_mappings_to_upsert": [],
    "companies_to_upsert": [
        # 晶圆代工 / IDM
        {"company_id": "smic", "name_zh": "中芯国际", "name_en": "Semiconductor Manufacturing International Corporation", "stock_codes": ["688981.SH", "00981.HK"], "country": "CN", "company_type": "public", "description": "中国大陆最大晶圆代工厂，覆盖先进及成熟制程"},
        {"company_id": "hualihong", "name_zh": "华虹半导体", "name_en": "Hua Hong Semiconductor", "stock_codes": ["688347.SH", "01347.HK"], "country": "CN", "company_type": "public", "description": "特色工艺晶圆代工龙头"},
        {"company_id": "jcet", "name_zh": "长电科技", "name_en": "JCET", "stock_codes": ["600584.SH"], "country": "CN", "company_type": "public", "description": "全球前三 OSAT，先进封装龙头"},
        {"company_id": "tongfu_microelectronics", "name_zh": "通富微电", "name_en": "Tongfu Microelectronics", "stock_codes": ["002156.SZ"], "country": "CN", "company_type": "public", "description": "国内第二大封测厂，AMD 深度合作"},
        {"company_id": "huatian_technology", "name_zh": "华天科技", "name_en": "Huatian Technology", "stock_codes": ["002185.SZ"], "country": "CN", "company_type": "public", "description": "国内第三大封测厂"},
        {"company_id": "silan_micro", "name_zh": "士兰微", "name_en": "Silan Microelectronics", "stock_codes": ["600460.SH"], "country": "CN", "company_type": "public", "description": "IDM 模式，功率半导体与 MCU"},
        {"company_id": "cr_micro", "name_zh": "华润微", "name_en": "China Resources Microelectronics", "stock_codes": ["688396.SH"], "country": "CN", "company_type": "state_owned", "description": "IDM 模式，功率半导体与传感器"},

        # 设备
        {"company_id": "naura_technology", "name_zh": "北方华创", "name_en": "NAURA Technology", "stock_codes": ["002371.SZ"], "country": "CN", "company_type": "public", "description": "国内半导体设备平台龙头，覆盖刻蚀、沉积、清洗、热处理"},
        {"company_id": "amec", "name_zh": "中微公司", "name_en": "Advanced Micro-Fabrication Equipment", "stock_codes": ["688012.SH"], "country": "CN", "company_type": "public", "description": "刻蚀设备及 MOCVD 龙头"},
        {"company_id": "piotech", "name_zh": "拓荆科技", "name_en": "Piotech", "stock_codes": ["688072.SH"], "country": "CN", "company_type": "public", "description": "薄膜沉积设备（PECVD/ALD/SACVD）"},
        {"company_id": "hwatsing", "name_zh": "华海清科", "name_en": "Hwatsing Technology", "stock_codes": ["688120.SH"], "country": "CN", "company_type": "public", "description": "CMP 设备龙头"},
        {"company_id": "acmr", "name_zh": "盛美上海", "name_en": "ACM Research Shanghai", "stock_codes": ["688082.SH"], "country": "CN", "company_type": "public", "description": "清洗、电镀、炉管设备"},
        {"company_id": "kingsemi", "name_zh": "芯源微", "name_en": "Kingsemi", "stock_codes": ["688037.SH"], "country": "CN", "company_type": "public", "description": "涂胶显影及清洗设备"},
        {"company_id": "jingce_electronic", "name_zh": "精测电子", "name_en": "Jingce Electronic", "stock_codes": ["300567.SZ"], "country": "CN", "company_type": "public", "description": "半导体量测/检测设备"},
        {"company_id": "skyverse", "name_zh": "中科飞测", "name_en": "Skyverse", "stock_codes": ["688361.SH"], "country": "CN", "company_type": "public", "description": "量测/检测设备"},
        {"company_id": "changsheng_technology", "name_zh": "长川科技", "name_en": "Changsheng Technology", "stock_codes": ["300604.SZ"], "country": "CN", "company_type": "public", "description": "测试机、分选机"},
        {"company_id": "accotest", "name_zh": "华峰测控", "name_en": "AccoTest", "stock_codes": ["688200.SH"], "country": "CN", "company_type": "public", "description": "模拟及混合信号测试机"},

        # 材料
        {"company_id": "nsig", "name_zh": "沪硅产业", "name_en": "National Silicon Industry", "stock_codes": ["688126.SH"], "country": "CN", "company_type": "public", "description": "12/8/6 英寸硅片"},
        {"company_id": "anji_microelectronics", "name_zh": "安集科技", "name_en": "Anji Microelectronics", "stock_codes": ["688019.SH"], "country": "CN", "company_type": "public", "description": "CMP 抛光液"},
        {"company_id": "jiangfeng_electronic", "name_zh": "江丰电子", "name_en": "Konfoong Materials International", "stock_codes": ["300666.SZ"], "country": "CN", "company_type": "public", "description": "高纯溅射靶材"},
        {"company_id": "nanda_photoelectric", "name_zh": "南大光电", "name_en": "Nanda Photoelectric", "stock_codes": ["300346.SZ"], "country": "CN", "company_type": "public", "description": "ArF 光刻胶、电子特气"},
        {"company_id": "jianghua_micro", "name_zh": "江化微", "name_en": "Jianghua Microelectronics", "stock_codes": ["603078.SH"], "country": "CN", "company_type": "public", "description": "湿化学品"},
        {"company_id": "huat_gas", "name_zh": "华特气体", "name_en": "Huat Gas", "stock_codes": ["688268.SH"], "country": "CN", "company_type": "public", "description": "电子特种气体"},
        {"company_id": "jacques_technology", "name_zh": "雅克科技", "name_en": "Jacques Technology", "stock_codes": ["002409.SZ"], "country": "CN", "company_type": "public", "description": "电子特气、前驱体"},

        # EDA / IP
        {"company_id": "empyrean", "name_zh": "华大九天", "name_en": "Empyrean Technology", "stock_codes": ["301269.SZ"], "country": "CN", "company_type": "public", "description": "全流程 EDA 工具"},
        {"company_id": "primarius", "name_zh": "概伦电子", "name_en": "Primarius Technologies", "stock_codes": ["688206.SH"], "country": "CN", "company_type": "public", "description": "器件建模及电路仿真 EDA"},
        {"company_id": "verisilicon", "name_zh": "芯原股份", "name_en": "VeriSilicon", "stock_codes": ["688521.SH"], "country": "CN", "company_type": "public", "description": "半导体 IP 及 Chiplet 设计服务"},

        # 设计 - CPU/GPU/AI/FPGA
        {"company_id": "hygon", "name_zh": "海光信息", "name_en": "Hygon Information Technology", "stock_codes": ["688041.SH"], "country": "CN", "company_type": "public", "description": "x86 CPU、DCU/AI 加速器"},
        {"company_id": "loongson", "name_zh": "龙芯中科", "name_en": "Loongson Technology", "stock_codes": ["688047.SH"], "country": "CN", "company_type": "public", "description": "自主指令集 CPU"},
        {"company_id": "cambricon", "name_zh": "寒武纪", "name_en": "Cambricon", "stock_codes": ["688256.SH"], "country": "CN", "company_type": "public", "description": "AI 芯片"},
        {"company_id": "jingjia_micro", "name_zh": "景嘉微", "name_en": "Jingjia Microelectronics", "stock_codes": ["300474.SZ"], "country": "CN", "company_type": "public", "description": "GPU/图形芯片"},
        {"company_id": "anlogic", "name_zh": "安路科技", "name_en": "Anlogic", "stock_codes": ["688107.SH"], "country": "CN", "company_type": "public", "description": "FPGA"},
        {"company_id": "gigadevice", "name_zh": "兆易创新", "name_en": "GigaDevice", "stock_codes": ["603986.SH"], "country": "CN", "company_type": "public", "description": "MCU、NOR Flash"},

        # 设计 - CIS / 模拟 / PMIC / 射频
        {"company_id": "will_semiconductor", "name_zh": "韦尔股份", "name_en": "Will Semiconductor", "stock_codes": ["603501.SH"], "country": "CN", "company_type": "public", "description": "CIS 图像传感器龙头"},
        {"company_id": "galaxycore", "name_zh": "格科微", "name_en": "GalaxyCore", "stock_codes": ["688728.SH"], "country": "CN", "company_type": "public", "description": "CIS"},
        {"company_id": "sgmicro", "name_zh": "圣邦股份", "name_en": "SG Micro", "stock_codes": ["300661.SZ"], "country": "CN", "company_type": "public", "description": "模拟芯片、PMIC"},
        {"company_id": "maxscend", "name_zh": "卓胜微", "name_en": "Maxscend Microelectronics", "stock_codes": ["300782.SZ"], "country": "CN", "company_type": "public", "description": "射频前端"},
        {"company_id": "southchip", "name_zh": "南芯科技", "name_en": "Southchip", "stock_codes": ["688484.SH"], "country": "CN", "company_type": "public", "description": "电源管理、充电芯片"},
        {"company_id": "novosense", "name_zh": "纳芯微", "name_en": "Novosense", "stock_codes": ["688052.SH"], "country": "CN", "company_type": "public", "description": "模拟/隔离芯片"},

        # 功率半导体
        {"company_id": "star_power", "name_zh": "斯达半导", "name_en": "StarPower Semiconductor", "stock_codes": ["603290.SH"], "country": "CN", "company_type": "public", "description": "IGBT 模块"},
        {"company_id": "yangjie_technology", "name_zh": "扬杰科技", "name_en": "Yangjie Technology", "stock_codes": ["300373.SZ"], "country": "CN", "company_type": "public", "description": "分立器件、功率半导体"},
        {"company_id": "tianshan_advanced", "name_zh": "天岳先进", "name_en": "SICC", "stock_codes": ["688234.SH"], "country": "CN", "company_type": "public", "description": "SiC 衬底"},
    ],
    "company_node_exposures_to_upsert": [
        # 代工 / IDM
        {"exposure_id": "smic_founds_advanced", "company_id": "smic", "node_id": "foundry", "activity_type": "manufacture", "role": "晶圆代工龙头，覆盖先进及成熟制程", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "中芯国际是中国大陆最大晶圆代工厂，覆盖先进及成熟制程"}]},
        {"exposure_id": "smic_mature_node", "company_id": "smic", "node_id": "mature_process_node", "activity_type": "manufacture", "role": "成熟制程代工", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "中芯国际覆盖先进及成熟制程"}]},
        {"exposure_id": "smic_advanced_node", "company_id": "smic", "node_id": "advanced_process_node", "activity_type": "manufacture", "role": "先进制程代工", "weight": 0.8, "confidence": "MEDIUM", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "中芯国际覆盖先进及成熟制程"}]},
        {"exposure_id": "hualihong_founds", "company_id": "hualihong", "node_id": "foundry", "activity_type": "manufacture", "role": "特色工艺晶圆代工龙头", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "华虹半导体是特色工艺晶圆代工龙头"}]},
        {"exposure_id": "hualihong_mature", "company_id": "hualihong", "node_id": "mature_process_node", "activity_type": "manufacture", "role": "成熟制程特色工艺代工", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "华虹半导体特色工艺代工"}]},
        {"exposure_id": "jcet_osat", "company_id": "jcet", "node_id": "osat", "activity_type": "manufacture", "role": "全球前三 OSAT，先进封装龙头", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "长电科技是全球前三 OSAT"}]},
        {"exposure_id": "tongfu_osat", "company_id": "tongfu_microelectronics", "node_id": "osat", "activity_type": "manufacture", "role": "国内第二大封测厂", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "通富微电是国内第二大封测厂"}]},
        {"exposure_id": "huatian_osat", "company_id": "huatian_technology", "node_id": "osat", "activity_type": "manufacture", "role": "国内第三大封测厂", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "华天科技是国内第三大封测厂"}]},
        {"exposure_id": "silan_idm", "company_id": "silan_micro", "node_id": "idm", "activity_type": "manufacture", "role": "IDM 模式，功率半导体与 MCU", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "士兰微为 IDM 模式"}]},
        {"exposure_id": "silan_power", "company_id": "silan_micro", "node_id": "power_semiconductor", "activity_type": "produce", "role": "功率半导体", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "士兰微功率半导体与 MCU"}]},
        {"exposure_id": "silan_mcu", "company_id": "silan_micro", "node_id": "mcu", "activity_type": "produce", "role": "MCU", "weight": 0.8, "confidence": "MEDIUM", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "士兰微功率半导体与 MCU"}]},
        {"exposure_id": "crmicro_idm", "company_id": "cr_micro", "node_id": "idm", "activity_type": "manufacture", "role": "IDM 模式", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "华润微为 IDM 模式"}]},
        {"exposure_id": "crmicro_power", "company_id": "cr_micro", "node_id": "power_semiconductor", "activity_type": "produce", "role": "功率半导体", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "华润微功率半导体与传感器"}]},

        # 设备
        {"exposure_id": "naura_etching", "company_id": "naura_technology", "node_id": "etching_machine", "activity_type": "produce", "role": "刻蚀设备", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "北方华创覆盖刻蚀、沉积、清洗、热处理"}]},
        {"exposure_id": "naura_cvd", "company_id": "naura_technology", "node_id": "cvd_equipment", "activity_type": "produce", "role": "CVD/PVD 薄膜沉积设备", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "北方华创覆盖刻蚀、沉积、清洗、热处理"}]},
        {"exposure_id": "naura_pvd", "company_id": "naura_technology", "node_id": "pvd_equipment", "activity_type": "produce", "role": "PVD 设备", "weight": 0.8, "confidence": "MEDIUM", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "北方华创覆盖刻蚀、沉积、清洗、热处理"}]},
        {"exposure_id": "naura_cleaning", "company_id": "naura_technology", "node_id": "cleaning_equipment", "activity_type": "produce", "role": "清洗设备", "weight": 0.8, "confidence": "MEDIUM", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "北方华创覆盖刻蚀、沉积、清洗、热处理"}]},
        {"exposure_id": "amec_etching", "company_id": "amec", "node_id": "etching_machine", "activity_type": "produce", "role": "刻蚀设备及 MOCVD 龙头", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "中微公司为刻蚀设备及 MOCVD 龙头"}]},
        {"exposure_id": "piotech_cvd", "company_id": "piotech", "node_id": "cvd_equipment", "activity_type": "produce", "role": "PECVD/SACVD 薄膜沉积", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "拓荆科技薄膜沉积设备"}]},
        {"exposure_id": "piotech_ald", "company_id": "piotech", "node_id": "ald_equipment", "activity_type": "produce", "role": "ALD 原子层沉积", "weight": 0.9, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "拓荆科技 ALD 设备"}]},
        {"exposure_id": "hwatsing_cmp", "company_id": "hwatsing", "node_id": "cmp_equipment", "activity_type": "produce", "role": "CMP 设备龙头", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "华海清科 CMP 设备龙头"}]},
        {"exposure_id": "acmr_cleaning", "company_id": "acmr", "node_id": "cleaning_equipment", "activity_type": "produce", "role": "清洗、电镀、炉管设备", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "盛美上海清洗、电镀、炉管设备"}]},
        {"exposure_id": "kingsemi_track", "company_id": "kingsemi", "node_id": "track_coater_developer", "activity_type": "produce", "role": "涂胶显影设备", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "芯源微涂胶显影及清洗设备"}]},
        {"exposure_id": "jingce_metrology", "company_id": "jingce_electronic", "node_id": "metrology_equipment", "activity_type": "produce", "role": "量测/检测设备", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "精测电子半导体量测/检测设备"}]},
        {"exposure_id": "skyverse_metrology", "company_id": "skyverse", "node_id": "metrology_equipment", "activity_type": "produce", "role": "量测/检测设备", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "中科飞测量测/检测设备"}]},
        {"exposure_id": "changsheng_test", "company_id": "changsheng_technology", "node_id": "metrology_equipment", "activity_type": "produce", "role": "测试机、分选机", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "长川科技测试机、分选机"}]},
        {"exposure_id": "accotest_test", "company_id": "accotest", "node_id": "metrology_equipment", "activity_type": "produce", "role": "模拟及混合信号测试机", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "华峰测控模拟及混合信号测试机"}]},

        # 材料
        {"exposure_id": "nsig_wafer", "company_id": "nsig", "node_id": "silicon_wafer", "activity_type": "produce", "role": "12/8/6 英寸硅片", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "沪硅产业 12/8/6 英寸硅片"}]},
        {"exposure_id": "nsig_silicon", "company_id": "nsig", "node_id": "silicon", "activity_type": "produce", "role": "硅材料", "weight": 0.8, "confidence": "MEDIUM", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "沪硅产业硅片材料"}]},
        {"exposure_id": "anji_slurry", "company_id": "anji_microelectronics", "node_id": "cmp_slurry", "activity_type": "produce", "role": "CMP 抛光液", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "安集科技 CMP 抛光液"}]},
        {"exposure_id": "jiangfeng_target", "company_id": "jiangfeng_electronic", "node_id": "sputtering_target", "activity_type": "produce", "role": "高纯溅射靶材", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "江丰电子高纯溅射靶材"}]},
        {"exposure_id": "nanda_photoresist", "company_id": "nanda_photoelectric", "node_id": "euv_photoresist", "activity_type": "produce", "role": "ArF 光刻胶", "weight": 0.8, "confidence": "MEDIUM", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "南大光电 ArF 光刻胶、电子特气"}]},
        {"exposure_id": "nanda_gas", "company_id": "nanda_photoelectric", "node_id": "electronic_special_gases", "activity_type": "produce", "role": "电子特气", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "南大光电 ArF 光刻胶、电子特气"}]},
        {"exposure_id": "jianghua_wet", "company_id": "jianghua_micro", "node_id": "wet_chemicals", "activity_type": "produce", "role": "湿化学品", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "江化微湿化学品"}]},
        {"exposure_id": "huat_gas", "company_id": "huat_gas", "node_id": "electronic_special_gases", "activity_type": "produce", "role": "电子特种气体", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "华特气体电子特种气体"}]},
        {"exposure_id": "jacques_gas", "company_id": "jacques_technology", "node_id": "electronic_special_gases", "activity_type": "produce", "role": "电子特气、前驱体", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "雅克科技电子特气、前驱体"}]},

        # EDA / IP
        {"exposure_id": "empyrean_eda", "company_id": "empyrean", "node_id": "eda_software", "activity_type": "provide_service", "role": "全流程 EDA 工具", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "华大九天全流程 EDA 工具"}]},
        {"exposure_id": "primarius_eda", "company_id": "primarius", "node_id": "eda_software", "activity_type": "provide_service", "role": "器件建模及电路仿真 EDA", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "概伦电子器件建模 EDA、电路仿真"}]},
        {"exposure_id": "verisilicon_ip", "company_id": "verisilicon", "node_id": "ip_core", "activity_type": "provide_service", "role": "半导体 IP 及 Chiplet 设计服务", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "芯原股份半导体 IP 及 Chiplet 设计服务"}]},

        # 设计 - CPU/GPU/AI/FPGA
        {"exposure_id": "hygon_cpu", "company_id": "hygon", "node_id": "cpu", "activity_type": "produce", "role": "x86 CPU", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "海光信息 x86 CPU"}]},
        {"exposure_id": "hygon_ai", "company_id": "hygon", "node_id": "ai_accelerator", "activity_type": "produce", "role": "DCU/AI 加速器", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "海光信息 DCU/AI 加速器"}]},
        {"exposure_id": "loongson_cpu", "company_id": "loongson", "node_id": "cpu", "activity_type": "produce", "role": "自主指令集 CPU", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "龙芯中科自主指令集 CPU"}]},
        {"exposure_id": "cambricon_ai", "company_id": "cambricon", "node_id": "ai_accelerator", "activity_type": "produce", "role": "AI 芯片", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "寒武纪 AI 芯片"}]},
        {"exposure_id": "jingjia_gpu", "company_id": "jingjia_micro", "node_id": "gpu", "activity_type": "produce", "role": "GPU/图形芯片", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "景嘉微 GPU/图形芯片"}]},
        {"exposure_id": "anlogic_fpga", "company_id": "anlogic", "node_id": "fpga", "activity_type": "produce", "role": "FPGA", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "安路科技 FPGA"}]},
        {"exposure_id": "gigadevice_mcu", "company_id": "gigadevice", "node_id": "mcu", "activity_type": "produce", "role": "MCU", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "兆易创新 MCU"}]},
        {"exposure_id": "gigadevice_flash", "company_id": "gigadevice", "node_id": "memory_chip", "activity_type": "produce", "role": "NOR Flash", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "兆易创新 NOR Flash"}]},

        # 设计 - CIS / 模拟 / PMIC / 射频
        {"exposure_id": "will_cis", "company_id": "will_semiconductor", "node_id": "cis", "activity_type": "produce", "role": "CIS 图像传感器龙头", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "韦尔股份 CIS 图像传感器龙头"}]},
        {"exposure_id": "galaxycore_cis", "company_id": "galaxycore", "node_id": "cis", "activity_type": "produce", "role": "CIS", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "格科微 CIS"}]},
        {"exposure_id": "sgmicro_analog", "company_id": "sgmicro", "node_id": "analog_chip", "activity_type": "produce", "role": "模拟芯片", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "圣邦股份模拟芯片、PMIC"}]},
        {"exposure_id": "sgmicro_pmic", "company_id": "sgmicro", "node_id": "pmic", "activity_type": "produce", "role": "PMIC", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "圣邦股份模拟芯片、PMIC"}]},
        {"exposure_id": "maxscend_rf", "company_id": "maxscend", "node_id": "rf_chip", "activity_type": "produce", "role": "射频前端", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "卓胜微射频前端"}]},
        {"exposure_id": "southchip_pmic", "company_id": "southchip", "node_id": "pmic", "activity_type": "produce", "role": "电源管理、充电芯片", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "南芯科技电源管理、充电芯片"}]},
        {"exposure_id": "novosense_analog", "company_id": "novosense", "node_id": "analog_chip", "activity_type": "produce", "role": "模拟/隔离芯片", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "纳芯微模拟/隔离芯片"}]},

        # 功率半导体
        {"exposure_id": "star_power_igbt", "company_id": "star_power", "node_id": "power_semiconductor", "activity_type": "produce", "role": "IGBT 模块", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "斯达半导 IGBT 模块"}]},
        {"exposure_id": "yangjie_power", "company_id": "yangjie_technology", "node_id": "power_semiconductor", "activity_type": "produce", "role": "分立器件、功率半导体", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "扬杰科技分立器件、功率半导体"}]},
        {"exposure_id": "tianshan_sic", "company_id": "tianshan_advanced", "node_id": "power_semiconductor", "activity_type": "produce", "role": "SiC 衬底及器件", "weight": 1.0, "confidence": "HIGH", "status": "ACTIVE", "evidence": [{"source_title": "半导体产业链公司研报", "quote": "天岳先进 SiC 衬底"}]},
    ],
}


async def main():
    async with httpx.AsyncClient() as client:
        r = await client.post("http://localhost:16060/api/v1/business-batches", json=BATCH)
        print(r.status_code)
        print(r.json())


asyncio.run(main())
