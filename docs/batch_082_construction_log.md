# Batch 082 Construction Log

**Date:** 2026-05-25
**Companies:** 600550.SH – 600562.SH (10 companies)
**Status:** ✅ Submitted successfully

---

## 1. New Industrial Nodes (+8)

| # | Node ID | Name (ZH) | Entity Type |
|---|---------|-----------|-------------|
| 1 | `transformer` | 变压器 | device |
| 2 | `tft_lcd_module` | TFT液晶显示模组 | component |
| 3 | `touch_screen_module` | 触摸屏模组 | component |
| 4 | `smart_city` | 智慧城市 | service |
| 5 | `welding_electrode` | 焊条 | material |
| 6 | `electric_drive` | 电气传动装置 | system |
| 7 | `power_semiconductor_component` | 电力半导体元器件 | component |
| 8 | `microwave_product` | 微波产品 | component |

## 2. New Industrial Edges (+3)

| # | Edge ID | From Node → To Node | Type |
|---|---------|---------------------|------|
| 1 | `transformer_to_power_grid` | transformer → power_grid | composition |
| 2 | `tft_lcd_module_to_display_panel` | tft_lcd_module → display_panel | composition |
| 3 | `welding_electrode_to_steel_structure` | welding_electrode → steel_structure | material_flow |

## 3. Companies Registered (+10)

| # | Company ID | Name | Stock Code | Province | City |
|---|-----------|------|-----------|----------|------|
| 1 | `baobian_elec` | 保定天威保变电气股份有限公司 | 600550.SH | 河北 | 保定市 |
| 2 | `times_publishing` | 时代出版传媒股份有限公司 | 600551.SH | 安徽 | 合肥市 |
| 3 | `kaisheng_tech` | 凯盛科技股份有限公司 | 600552.SH | 安徽 | 蚌埠市 |
| 4 | `tianxiaxiu` | 天下秀数字科技(集团)股份有限公司 | 600556.SH | 广西 | 北海市 |
| 5 | `kangyuan` | 江苏康缘药业股份有限公司 | 600557.SH | 江苏 | 连云港市 |
| 6 | `atlantic` | 四川大西洋焊接材料股份有限公司 | 600558.SH | 四川 | 自贡市 |
| 7 | `laobaigan` | 河北衡水老白干酒业股份有限公司 | 600559.SH | 河北 | 衡水市 |
| 8 | `aritime` | 北京金自天正智能控制股份有限公司 | 600560.SH | 北京 | 北京市 |
| 9 | `jiangxi_changyun` | 江西长运股份有限公司 | 600561.SH | 江西 | 南昌市 |
| 10 | `guorui` | 国睿科技股份有限公司 | 600562.SH | 江苏 | 南京市 |

## 4. Company Node Exposures (+27)

| Company | Node | Activity Type | Role | Weight |
|---------|------|--------------|------|--------|
| 保变电气 | transformer | manufacture | 变压器制造商 | 0.95 |
| 保变电气 | current_transformer | manufacture | 互感器制造商 | 0.9 |
| 保变电气 | solar_cell | produce | 太阳能电池组件生产商 | 0.85 |
| 时代出版 | book_publishing | operate | 图书出版运营商 | 0.95 |
| 时代出版 | journal_publishing | operate | 期刊出版运营商 | 0.9 |
| 时代出版 | printing_service | provide_service | 印刷复制服务商 | 0.85 |
| 凯盛科技 | tft_lcd_module | manufacture | TFT液晶显示模组制造商 | 0.95 |
| 凯盛科技 | touch_screen_module | manufacture | 触摸屏模组制造商 | 0.95 |
| 凯盛科技 | ito_conductive_glass | manufacture | ITO导电膜玻璃制造商 | 0.9 |
| 天下秀 | smart_city | provide_service | 智慧城市服务商 | 0.95 |
| 天下秀 | software | provide_service | 软件服务商 | 0.85 |
| 康缘药业 | chinese_patent_medicine | produce | 中成药生产商 | 0.95 |
| 康缘药业 | pharmaceutical | produce | 药品生产商 | 0.9 |
| 大西洋 | welding_electrode | produce | 焊条生产商 | 0.95 |
| 大西洋 | welding_wire | produce | 焊丝生产商 | 0.95 |
| 大西洋 | welding_material | produce | 焊接材料生产商 | 0.9 |
| 老白干酒 | liquor | produce | 白酒生产商 | 0.95 |
| 老白干酒 | pig | produce | 商品猪生产商 | 0.85 |
| 老白干酒 | feed | produce | 饲料生产商 | 0.8 |
| 金自天正 | electric_drive | manufacture | 电气传动装置制造商 | 0.95 |
| 金自天正 | industrial_control_system | manufacture | 工业计算机控制系统制造商 | 0.9 |
| 金自天正 | power_semiconductor_component | manufacture | 电力半导体元器件制造商 | 0.9 |
| 江西长运 | passenger_transport | operate | 公路旅客运输运营商 | 0.95 |
| 江西长运 | tourism_service | provide_service | 旅游服务商 | 0.85 |
| 江西长运 | vehicle_rental | operate | 车辆租赁运营商 | 0.8 |
| 国睿科技 | microwave_product | manufacture | 微波产品制造商 | 0.95 |
| 国睿科技 | communication_equipment | manufacture | 通信设备制造商 | 0.9 |

---

**Graph increment:** Nodes +8, Edges +3
