# Batch 051 Construction Log

**Date:** 2026-05-25
**Companies:** 600125.SH – 600135.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+8)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `rail_logistics` | 铁路物流 | service |
| 2 | `rice` | 大米 | material |
| 3 | `flour` | 面粉 | material |
| 4 | `edible_oil` | 食用油 | material |
| 5 | `trade_agent` | 贸易代理 | service |
| 6 | `mobile_phone` | 移动电话 | device |
| 7 | `beer` | 啤酒 | material |
| 8 | `tech_park` | 科技园区 | infrastructure |
| 9 | `environmental_service` | 环保服务 | service |
| 10 | `photographic_film` | 感光胶片 | material |
| 11 | `solar_pv_material` | 光伏材料 | material |

## 2. New Industrial Edges (+2)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `rice_to_flour` | rice → flour | material_flow |
| 2 | `solar_pv_material_to_photovoltaic_cell` | solar_pv_material → photovoltaic_cell | composition |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `tielong_logistics` | 中铁铁龙集装箱物流股份有限公司 | 600125.SH | 辽宁 | 大连 |
| 2 | `hangzhou_steel` | 杭州钢铁股份有限公司 | 600126.SH | 浙江 | 杭州 |
| 3 | `jinjian_rice` | 金健米业股份有限公司 | 600127.SH | 湖南 | 常德 |
| 4 | `suhao_hongye` | 苏豪弘业股份有限公司 | 600128.SH | 江苏 | 南京 |
| 5 | `taiji_group` | 重庆太极实业(集团)股份有限公司 | 600129.SH | 重庆 | 重庆 |
| 6 | `bird_mobile` | 宁波波导股份有限公司 | 600130.SH | 浙江 | 宁波 |
| 7 | `sgcc_ict` | 国网信息通信股份有限公司 | 600131.SH | 四川 | 阿坝 |
| 8 | `chongqing_beer` | 重庆啤酒股份有限公司 | 600132.SH | 重庆 | 重庆 |
| 9 | `donghu_hitech` | 武汉东湖高新集团股份有限公司 | 600133.SH | 湖北 | 武汉 |
| 10 | `lucky_film` | 乐凯胶片股份有限公司 | 600135.SH | 河北 | 保定 |

## 4. Company Node Exposures (+18)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 铁龙物流 | rail_logistics | operate | 铁路物流运营商 | 0.9 |
| 铁龙物流 | logistics_service | provide_service | 综合物流服务商 | 0.8 |
| 杭钢股份 | steel_plate | produce | 钢铁板材生产商 | 0.95 |
| 金健米业 | rice | produce | 大米生产商 | 0.9 |
| 金健米业 | flour | produce | 面粉生产商 | 0.85 |
| 金健米业 | edible_oil | produce | 食用油生产商 | 0.85 |
| 苏豪弘业 | trade_agent | provide_service | 进出口贸易代理商 | 0.9 |
| 苏豪弘业 | textile_product | procure | 纺织品贸易商 | 0.8 |
| 太极集团 | chinese_patent_medicine | produce | 中成药生产商 | 0.95 |
| 波导股份 | mobile_phone | manufacture | 移动电话制造商 | 0.9 |
| 国网信通 | power_supply | provide_service | 电力供应及通信服务商 | 0.9 |
| 国网信通 | communication_equipment | manufacture | 通信设备制造商 | 0.8 |
| 重庆啤酒 | beer | produce | 啤酒生产商 | 0.95 |
| 东湖高新 | tech_park | operate | 科技园区运营商 | 0.85 |
| 东湖高新 | environmental_service | provide_service | 环保服务提供商 | 0.8 |
| 东湖高新 | power_generation | operate | 火力发电运营商 | 0.75 |
| 乐凯胶片 | photographic_film | produce | 感光胶片生产商 | 0.85 |
| 乐凯胶片 | solar_pv_material | produce | 光伏材料生产商 | 0.8 |

---

**Graph increment:** Nodes +8, Edges +2
