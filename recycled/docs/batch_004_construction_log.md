# Batch 004 产业图构建日志

## 任务概述

为 `data/stock_batches/batch_004.json` 中的 **10家上市公司** 构建产业实体图和公司视图。

## 涉及公司

| 股票代码 | 公司简称 | 公司ID | 核心业务 |
|---|---|---|---|
| 000042.SZ | 中洲控股 | zhongzhou_holding | 房地产开发 |
| 001914.SZ | 招商积余 | cms_jiyu | 地产开发、物业管理 |
| 000045.SZ | 深纺织A | shenzhen_textile | 偏光片等光学膜 |
| 000048.SZ | 京基智农 | jingji_smartfarm | 生猪养殖、饲料、种鸡肉鸡、房地产 |
| 000049.SZ | 德赛电池 | desay_battery | 电源管理系统、各类锂电池 |
| 000050.SZ | 深天马A | tianma_micro | 液晶显示面板、显示模组 |
| 000055.SZ | 方大集团 | fangda_group | 节能幕墙、轨道交通屏蔽门、LED显示、光伏 |
| 000056.SZ | *ST皇庭 | huangting_international | 连锁商业、房地产开发、物业管理 |
| 000058.SZ | 深赛格 | seg_electronics | 电子专业市场、物业租赁、IT零售、光伏 |
| 000059.SZ | 华锦股份 | huajin_chemical | 石油化工产品、化学肥料 |

## 数据来源

- **Tushare**: 获取了各公司的财务指标（2025年报营收、净利润）和市值数据。
- **网络搜索**: 核查了方大集团幕墙/屏蔽门业务细节、京基智农养殖产业链、深纺织A偏光片业务转型、华锦股份石化业务构成。
- **年报/公开资料**: 所有节点和边的证据均引用自公司2024/2025年年报或行业常识。

## 产业图构建成果

### 新建产业节点

本次共新建 **13个产业节点**。

| 类别 | node_id | 中文名 | entity_type | 对应公司 |
|---|---|---|---|---|
| **农业** | animal_feed | 饲料 | material | 京基智农 |
| **农业** | live_pig | 生猪 | material | 京基智农 |
| **农业** | poultry | 家禽 | material | 京基智农 |
| **建材** | building_curtain_wall | 建筑幕墙 | component | 方大集团 |
| **建材** | platform_screen_door | 站台屏蔽门 | subsystem | 方大集团 |
| **显示** | led_display_screen | LED显示屏 | device | 方大集团 |
| **材料** | aluminum_panel | 铝板 | material | 方大集团 |
| **商业** | chain_retail_service | 连锁零售服务 | service | *ST皇庭 |
| **电子市场** | electronics_market_service | 电子专业市场服务 | service | 深赛格 |
| **石化** | crude_oil | 原油 | material | 华锦股份 |
| **石化** | petrochemical_product | 石油化工产品 | material | 华锦股份 |
| **石化** | chemical_fertilizer | 化学肥料 | material | 华锦股份 |
| **石化** | refining_service | 石油炼化服务 | service | 华锦股份 |

### 已有节点复用

复用了现有图谱中的大量节点：
- **房地产链**: land, construction_service, residential_property, commercial_property, property_management_service, housing_rental_service（中洲控股、招商积余、*ST皇庭、深赛格、京基智农、方大集团）
- **显示面板链**: lcd_panel, lcd_monitor, display_module, lcd_polarizer, oled_polarizer（深天马A、深纺织A）
- **锂电池链**: bms_component, consumer_battery_pack, energy_storage_battery（德赛电池）
- **光伏链**: photovoltaic_module（方大集团、深赛格）
- **玻璃链**: float_glass（方大集团幕墙用玻璃）

### 新建产业流边

本次共新建 **15条产业流边**：

1. **农业链**: agricultural_product → animal_feed → live_pig / poultry
2. **显示链**: lcd_panel → display_module（深天马A核心产业链）
3. **建材链**: aluminum_panel / float_glass → building_curtain_wall; steel_sheet → platform_screen_door; semiconductor_device → led_display_screen
4. **商业链**: commercial_property → chain_retail_service
5. **电子市场链**: it_hardware → electronics_market_service
6. **石化链**: crude_oil → refining_service → petrochemical_product; natural_gas → petrochemical_product; petrochemical_product → plastic_resin / chemical_fertilizer

### 公司视图构建成果

**10家公司** 全部创建成功，共建立 **31条 CompanyNodeExposure**。

| 公司 | 暴露节点数 | 核心暴露 |
|---|---|---|
| 中洲控股 | 2 | residential_property, commercial_property (produce) |
| 招商积余 | 3 | residential_property (produce), property_management_service, housing_rental_service (provide_service) |
| 深纺织A | 2 | lcd_polarizer, oled_polarizer (manufacture) |
| 京基智农 | 4 | animal_feed (manufacture), live_pig, poultry, residential_property (produce) |
| 德赛电池 | 3 | bms_component, consumer_battery_pack, energy_storage_battery (manufacture) |
| 深天马A | 3 | lcd_panel, display_module, lcd_monitor (manufacture) |
| 方大集团 | 5 | building_curtain_wall, platform_screen_door, led_display_screen, photovoltaic_module (manufacture), residential_property (produce) |
| *ST皇庭 | 3 | residential_property (produce), property_management_service, chain_retail_service (provide_service) |
| 深赛格 | 4 | electronics_market_service, property_management_service, housing_rental_service (provide_service), photovoltaic_module (manufacture) |
| 华锦股份 | 2 | petrochemical_product, chemical_fertilizer (manufacture) |

## 系统最终状态

```
Total nodes: 171 (新增13)
Total edges: 156 (新增15)
Total companies: 40 (新增10)
Total exposures: 105 (新增31)
```

## 发现与启发

### 1. 产业链覆盖多样性
- **华锦股份** 引入了石化产业链（原油 → 炼化 → 石化产品 → 塑料/化肥），填补了图谱在重化工领域的空白，与已有的 plastic_resin 节点形成上下游衔接。
- **京基智农** 引入了农业产业链（农产品 → 饲料 → 生猪/家禽），是图谱首次纳入农业养殖领域，拓展了产业图的覆盖广度。

### 2. 已有节点的大量复用
- 本次10家公司中有 **6家涉及房地产业务**（中洲控股、招商积余、京基智农、方大集团、*ST皇庭、深赛格），全部复用了已有的房地产链节点（land, construction_service, residential_property 等），无需新建任何地产节点。
- **深天马A** 和 **深纺织A** 均位于显示面板产业链，深天马A暴露到 lcd_panel/display_module/lcd_monitor，深纺织A暴露到 lcd_polarizer/oled_polarizer，两者形成面板 → 偏光片的上下游关系（已有产业链）。
- **德赛电池** 复用了已有的 bms_component 和 consumer_battery_pack 节点，与 batch_003 的电池产业链形成衔接。

### 3. 多元化公司的聚焦策略
- **方大集团** 业务非常多元（幕墙、屏蔽门、LED、光伏、房地产），但聚焦了 4 个制造业节点 + 1 个地产节点，避免了过度拆分。其中幕墙和屏蔽门是核心业务，LED和光伏是衍生业务。
- **深赛格** 的核心是"电子专业市场运营"（华强北模式），而非IT硬件制造。光伏（碲化镉薄膜电池）是次要业务，暴露权重设为 0.4。

### 4. 亏损公司的处理
- 本次有 **4家公司净利润为负**（中洲控股、方大集团、*ST皇庭、华锦股份），但产业关系不受财务亏损影响，所有公司均正常创建并建立暴露关系。
- *ST皇庭虽然被标记为ST（退市风险警示），但其连锁商业和物业管理的产业关系仍然有效。

### 5. 显示面板产业链的完整性
- 深天马A（面板制造）→ 深纺织A（偏光片制造）的产业链关系通过已有节点自然形成：
  - 深天马A 制造 lcd_panel / display_module
  - 深纺织A 制造 lcd_polarizer（面板的上游材料）
  - 已有边：pva_film → lcd_polarizer, tac_film → lcd_polarizer
  - 新增边：lcd_panel → display_module
- 这为后续推断两家公司之间的 inferred_industrial_relation 奠定了基础。

## 待后续完善

1. **行业过滤器配置**: 可为 batch_004 配置行业视图（如"农业养殖"、"显示面板"、"石化化工"、"建材幕墙"等）。
2. **公司关系推断**: 深天马A 与 深纺织A 在显示面板产业链上形成上下游关系；方大集团 与 中集集团 在物流/运输装备领域可能有交集。
3. **前端验证**: 可在前端查看各公司的临时子图，验证暴露关系的正确性。
