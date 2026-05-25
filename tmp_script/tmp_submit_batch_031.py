#!/usr/bin/env python3
"""Batch 031 Submission Script (000820-000831)"""
import requests
BASE_URL = "http://localhost:8000/api/v1"
submit_graph = lambda b: requests.post(f"{BASE_URL}/batches", json=b)
submit_business = lambda b: requests.post(f"{BASE_URL}/business-batches", json=b)

nodes = [
    {"node_id":"energy_efficiency_engineering","canonical_name_zh":"节能环保工程","canonical_name_en":"Energy Efficiency Engineering","aliases":["节能工程","环保工程"],"definition":"围绕钢铁、有色等高耗能行业开展的节能减排技术改造、余热余压利用、环保设施建设和工程总承包服务，涵盖工程设计、设备供货、EPC总承包等全链条业务。","entity_type":"service","evidence":[{"source_title":"*ST节能 主营业务","quote":"主要业务:钢铁,有色行业节能环保工程咨询,设计,设备供货和EPC总承包业务"}],"confidence":"HIGH","status":"ACTIVE"},
    {"node_id":"packaging_machinery","canonical_name_zh":"包装机械","canonical_name_en":"Packaging Machinery","aliases":["包装设备","印刷包装机械"],"definition":"用于完成产品包装过程的机械设备，包括填充、灌装、封口、裹包、贴标、捆扎、集装等工序的专用设备，广泛应用于食品、饮料、医药、日化等行业。","entity_type":"device","evidence":[{"source_title":"ST京机 主营业务","quote":"主要产品:包装机械,汽车零部件制造"}],"confidence":"HIGH","status":"ACTIVE"},
    {"node_id":"soda_ash","canonical_name_zh":"纯碱","canonical_name_en":"Soda Ash","aliases":["碳酸钠","苏打"],"definition":"化学名碳酸钠（Na₂CO₃），是重要的基础化工原料，广泛用于玻璃制造、洗涤剂生产、造纸、印染、食品加工和冶金等行业，主要通过氨碱法或联碱法生产。","entity_type":"material","evidence":[{"source_title":"山东海化 主营业务","quote":"主要产品为纯碱,烧碱等产品的生产和销售"}],"confidence":"HIGH","status":"ACTIVE"},
    {"node_id":"cold_rolled_silicon_steel","canonical_name_zh":"冷轧硅钢","canonical_name_en":"Cold Rolled Silicon Steel","aliases":["电工钢","硅钢片"],"definition":"含硅量0.5%~4.5%的低碳电工钢薄板，具有优异的磁导率和低铁损特性，是制造变压器、电机、发电机等电力设备铁芯的关键软磁材料。","entity_type":"material","evidence":[{"source_title":"太钢不锈 主营业务","quote":"主要产品:不锈钢,冷轧硅钢,碳钢热轧卷板...等"}],"confidence":"HIGH","status":"ACTIVE"},
    {"node_id":"rare_earth_oxide","canonical_name_zh":"稀土氧化物","canonical_name_en":"Rare Earth Oxide","aliases":["稀土精矿"],"definition":"稀土元素与氧结合形成的化合物，是稀土冶炼分离的主要产品形式，包括氧化镧、氧化铈、氧化钕等，是制备稀土金属、稀土永磁材料、稀土发光材料等下游产品的基础原料。","entity_type":"material","evidence":[{"source_title":"中国稀土 主营业务","quote":"主要业务:稀土氧化物,稀土金属,稀土深加工产品经营及贸易"}],"confidence":"HIGH","status":"ACTIVE"},
    {"node_id":"rare_earth_metal","canonical_name_zh":"稀土金属","canonical_name_en":"Rare Earth Metal","aliases":["稀土合金"],"definition":"通过电解还原或金属热还原工艺从稀土氧化物中提炼得到的金属单质或合金，包括镧、铈、钕、镝等，是制造稀土永磁材料、储氢合金、催化材料等功能材料的关键原料。","entity_type":"material","evidence":[{"source_title":"中国稀土 经营范围","quote":"主营:稀土氧化物,稀土金属,稀土深加工产品经营及贸易"}],"confidence":"HIGH","status":"ACTIVE"}
]

edges = [
    {"edge_id":"flow_soda_ash_to_glass","from_node":"soda_ash","to_node":"flat_glass","description":"纯碱作为助熔剂用于平板玻璃制造。","edge_namespace":"industrial_flow","edge_type":"material_flow","evidence":[{"source_title":"山东海化 产业链","quote":"纯碱→玻璃"}],"confidence":"HIGH"},
    {"edge_id":"flow_rare_earth_oxide_to_metal","from_node":"rare_earth_oxide","to_node":"rare_earth_metal","description":"稀土氧化物经电解还原制成稀土金属。","edge_namespace":"industrial_flow","edge_type":"material_flow","evidence":[{"source_title":"中国稀土 产业链","quote":"稀土氧化物→稀土金属"}],"confidence":"HIGH"},
    {"edge_id":"flow_rare_earth_metal_to_magnet","from_node":"rare_earth_metal","to_node":"ndfeb_magnet","description":"稀土金属（钕、镝等）用于制造钕铁硼永磁材料。","edge_namespace":"industrial_flow","edge_type":"material_flow","evidence":[{"source_title":"中国稀土 产业链","quote":"稀土金属→永磁材料"}],"confidence":"HIGH"}
]

companies = [
    {"company_id":"shenwu_energy_saving","name_zh":"神雾节能股份有限公司","aliases":["*ST节能"],"stock_codes":["000820.SZ"],"description":"主要业务为钢铁、有色行业节能环保工程咨询、设计、设备供货和EPC总承包业务。","country":"CN","province":"江西","city":"南昌市","founded_year":1993,"employee_count":175,"company_type":"public","status":"ACTIVE"},
    {"company_id":"jingshan_light_machinery","name_zh":"湖北京山轻工机械股份有限公司","aliases":["ST京机"],"stock_codes":["000821.SZ"],"description":"主要产品包括包装机械、汽车零部件制造、人工智能和工业自动化等多项业务。","country":"CN","province":"湖北","city":"荆门市","founded_year":1993,"employee_count":5166,"company_type":"public","status":"ACTIVE"},
    {"company_id":"shandong_haihua","name_zh":"山东海化股份有限公司","aliases":["山东海化"],"stock_codes":["000822.SZ"],"description":"主要产品为纯碱、烧碱等产品的生产和销售，是山东省重要的盐化工企业。","country":"CN","province":"山东","city":"潍坊市","founded_year":1998,"employee_count":4451,"company_type":"public","status":"ACTIVE"},
    {"company_id":"chaoshen_electronics","name_zh":"广东汕头超声电子股份有限公司","aliases":["超声电子"],"stock_codes":["000823.SZ"],"description":"主要业务为印制线路板、液晶显示器、超声电子仪器、超薄及特种覆铜板的研制、生产和销售。","country":"CN","province":"广东","city":"汕头市","founded_year":1997,"employee_count":7531,"company_type":"public","status":"ACTIVE"},
    {"company_id":"taigang_stainless","name_zh":"山西太钢不锈钢股份有限公司","aliases":["太钢不锈"],"stock_codes":["000825.SZ"],"description":"主要产品包括不锈钢、冷轧硅钢、碳钢热轧卷板、火车轮轴钢、合金模具钢、军工钢等，是中国最大的不锈钢生产企业。","country":"CN","province":"山西","city":"太原市","founded_year":1998,"employee_count":13080,"company_type":"public","status":"ACTIVE"},
    {"company_id":"tus_environment","name_zh":"启迪环境科技发展股份有限公司","aliases":["*ST启环"],"stock_codes":["000826.SZ"],"description":"主营业务为固体废弃物处置系统工程设计、承建及固体废弃物处置设备系统集成业务。","country":"CN","province":"湖北","city":"宜昌市","founded_year":1993,"employee_count":42617,"company_type":"public","status":"ACTIVE"},
    {"company_id":"dongguan_holdings","name_zh":"东莞发展控股股份有限公司","aliases":["东莞控股"],"stock_codes":["000828.SZ"],"description":"主要业务为高速公路运营管理、融资租赁及商业保理业务。","country":"CN","province":"广东","city":"东莞市","founded_year":1997,"employee_count":864,"company_type":"public","status":"ACTIVE"},
    {"company_id":"tianyin_holdings","name_zh":"天音通信控股股份有限公司","aliases":["天音控股"],"stock_codes":["000829.SZ"],"description":"主要产品包括移动通讯产品销售、酒类产品销售，是国内重要的手机分销渠道商。","country":"CN","province":"江西","city":"赣州市","founded_year":1997,"employee_count":3558,"company_type":"public","status":"ACTIVE"},
    {"company_id":"luxi_chemical","name_zh":"鲁西化工集团股份有限公司","aliases":["鲁西化工"],"stock_codes":["000830.SZ"],"description":"主要业务为化肥的生产与销售，主要产品包括尿素、复合肥等，同时涉及化工新材料领域。","country":"CN","province":"山东","city":"聊城市","founded_year":1998,"employee_count":12124,"company_type":"public","status":"ACTIVE"},
    {"company_id":"china_rare_earth","name_zh":"中国稀土集团资源科技股份有限公司","aliases":["中国稀土"],"stock_codes":["000831.SZ"],"description":"主要业务为稀土氧化物、稀土金属、稀土深加工产品的经营及贸易，是中国稀土行业的重要企业。","country":"CN","province":"江西","city":"赣州市","founded_year":1998,"employee_count":528,"company_type":"public","status":"ACTIVE"}
]

exposures = [
    {"exposure_id":"exp_sws_energy_eff","company_id":"shenwu_energy_saving","node_id":"energy_efficiency_engineering","activity_type":"operate","role":"节能环保工程承包商","weight":0.9,"confidence":"HIGH","evidence":[{"source_title":"*ST节能 主营业务","quote":"主要业务:钢铁,有色行业节能环保工程咨询,设计,设备供货和EPC总承包业务"}],"status":"ACTIVE"},
    {"exposure_id":"exp_jlm_packaging","company_id":"jingshan_light_machinery","node_id":"packaging_machinery","activity_type":"manufacture","role":"包装机械制造商","weight":0.9,"confidence":"HIGH","evidence":[{"source_title":"ST京机 主营业务","quote":"主要产品:包装机械,汽车零部件制造"}],"status":"ACTIVE"},
    {"exposure_id":"exp_jlm_auto_part","company_id":"jingshan_light_machinery","node_id":"automotive_part","activity_type":"manufacture","role":"汽车零部件制造商","weight":0.7,"confidence":"HIGH","evidence":[{"source_title":"ST京机 主营业务","quote":"主要产品:...汽车零部件制造"}],"status":"ACTIVE"},
    {"exposure_id":"exp_shh_soda_ash","company_id":"shandong_haihua","node_id":"soda_ash","activity_type":"produce","role":"纯碱生产商","weight":0.9,"confidence":"HIGH","evidence":[{"source_title":"山东海化 主营业务","quote":"主要产品为纯碱,烧碱等产品的生产和销售"}],"status":"ACTIVE"},
    {"exposure_id":"exp_shh_caustic","company_id":"shandong_haihua","node_id":"caustic_soda","activity_type":"produce","role":"烧碱生产商","weight":0.8,"confidence":"HIGH","evidence":[{"source_title":"山东海化 主营业务","quote":"主要产品为纯碱,烧碱等产品的生产和销售"}],"status":"ACTIVE"},
    {"exposure_id":"exp_cse_pcb","company_id":"chaoshen_electronics","node_id":"pcb","activity_type":"manufacture","role":"印制线路板制造商","weight":0.9,"confidence":"HIGH","evidence":[{"source_title":"超声电子 主营业务","quote":"主要业务:印制线路板...的研制,生产和销售"}],"status":"ACTIVE"},
    {"exposure_id":"exp_cse_lcd","company_id":"chaoshen_electronics","node_id":"lcd_panel","activity_type":"manufacture","role":"液晶显示器制造商","weight":0.8,"confidence":"HIGH","evidence":[{"source_title":"超声电子 主营业务","quote":"主要业务:...液晶显示器...的研制,生产和销售"}],"status":"ACTIVE"},
    {"exposure_id":"exp_tg_stainless","company_id":"taigang_stainless","node_id":"stainless_steel","activity_type":"produce","role":"不锈钢生产商","weight":0.9,"confidence":"HIGH","evidence":[{"source_title":"太钢不锈 主营业务","quote":"主要产品:不锈钢...等"}],"status":"ACTIVE"},
    {"exposure_id":"exp_tg_silicon_steel","company_id":"taigang_stainless","node_id":"cold_rolled_silicon_steel","activity_type":"produce","role":"冷轧硅钢生产商","weight":0.8,"confidence":"HIGH","evidence":[{"source_title":"太钢不锈 主营业务","quote":"主要产品:不锈钢,冷轧硅钢...等"}],"status":"ACTIVE"},
    {"exposure_id":"exp_tg_steel_plate","company_id":"taigang_stainless","node_id":"steel_plate","activity_type":"produce","role":"碳钢板材生产商","weight":0.7,"confidence":"HIGH","evidence":[{"source_title":"太钢不锈 主营业务","quote":"主要产品:...碳钢热轧卷板...等"}],"status":"ACTIVE"},
    {"exposure_id":"exp_te_solid_waste","company_id":"tus_environment","node_id":"solid_waste_treatment","activity_type":"operate","role":"固废处置运营商","weight":0.9,"confidence":"HIGH","evidence":[{"source_title":"*ST启环 主营业务","quote":"主营业务为固体废弃物处置系统工程设计,承建及固体废弃物处置设备系统集成业务"}],"status":"ACTIVE"},
    {"exposure_id":"exp_te_waste_treatment","company_id":"tus_environment","node_id":"municipal_waste_treatment","activity_type":"operate","role":"城市废弃物处理运营商","weight":0.7,"confidence":"HIGH","evidence":[{"source_title":"*ST启环 经营范围","quote":"城市垃圾及工业固体废弃物处置"}],"status":"ACTIVE"},
    {"exposure_id":"exp_dg_highway","company_id":"dongguan_holdings","node_id":"highway_operation_service","activity_type":"operate","role":"高速公路运营商","weight":0.9,"confidence":"HIGH","evidence":[{"source_title":"东莞控股 主营业务","quote":"主要业务:高速公路运营管理"}],"status":"ACTIVE"},
    {"exposure_id":"exp_ty_mobile","company_id":"tianyin_holdings","node_id":"mobile_terminal","activity_type":"operate","role":"手机分销商","weight":0.9,"confidence":"HIGH","evidence":[{"source_title":"天音控股 主营业务","quote":"主要产品:移动通讯产品销售"}],"status":"ACTIVE"},
    {"exposure_id":"exp_ty_liquor","company_id":"tianyin_holdings","node_id":"liquor","activity_type":"operate","role":"酒类产品经销商","weight":0.6,"confidence":"HIGH","evidence":[{"source_title":"天音控股 主营业务","quote":"主要产品:...酒类产品销售"}],"status":"ACTIVE"},
    {"exposure_id":"exp_lx_urea","company_id":"luxi_chemical","node_id":"urea","activity_type":"produce","role":"尿素生产商","weight":0.9,"confidence":"HIGH","evidence":[{"source_title":"鲁西化工 主营业务","quote":"主要业务:化肥的生产与销售,主要产品:尿素,复合肥"}],"status":"ACTIVE"},
    {"exposure_id":"exp_lx_compound_fert","company_id":"luxi_chemical","node_id":"compound_fertilizer","activity_type":"produce","role":"复合肥生产商","weight":0.8,"confidence":"HIGH","evidence":[{"source_title":"鲁西化工 主营业务","quote":"主要产品:尿素,复合肥"}],"status":"ACTIVE"},
    {"exposure_id":"exp_cre_oxide","company_id":"china_rare_earth","node_id":"rare_earth_oxide","activity_type":"produce","role":"稀土氧化物生产商","weight":0.9,"confidence":"HIGH","evidence":[{"source_title":"中国稀土 主营业务","quote":"主要业务:稀土氧化物,稀土金属,稀土深加工产品经营及贸易"}],"status":"ACTIVE"},
    {"exposure_id":"exp_cre_metal","company_id":"china_rare_earth","node_id":"rare_earth_metal","activity_type":"produce","role":"稀土金属生产商","weight":0.8,"confidence":"HIGH","evidence":[{"source_title":"中国稀土 经营范围","quote":"主营:稀土氧化物,稀土金属..."}],"status":"ACTIVE"}
]

if __name__ == "__main__":
    gb = {"batch_id":"batch_031_graph","task_description":"Batch 031: Industrial nodes and edges for 10 companies (000820-000831). Focus on energy efficiency engineering, packaging machinery, soda ash, PCB/LCD, stainless steel/silicon steel, solid waste, highway, mobile/liquor distribution, fertilizer, rare earth.","nodes_to_upsert":nodes,"edges_to_upsert":edges,"rejected_or_pending":[]}
    bb = {"batch_id":"batch_031_business","task_description":"Batch 031: Company registrations and exposures for 10 companies (000820-000831).","industries_to_upsert":[],"industry_node_mappings_to_upsert":[],"companies_to_upsert":companies,"company_node_exposures_to_upsert":exposures}
    r1 = submit_graph(gb); print(f"Graph: {r1.status_code}", r1.json())
    r2 = submit_business(bb); print(f"Business: {r2.status_code}", r2.json())
