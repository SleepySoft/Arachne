# Batch 006 产业图与公司视图构建日志

**构建时间**: 2026-05-23
**数据来源**: `data/stock_batches/batch_006.json`
**涉及公司**: 10家中国公司

---

## 一、准备与查询

### 已有实体查询
构建前系统中已有201个产业节点、50家公司。batch_006重点复用了：
- `container_handling_service` / `logistics_service` — 盐田港
- `residential_property` / `commercial_property` / `construction_service` — 天健集团
- `petrochemical_product` / `electricity_power` — 广聚能源
- `lcd_panel` / `display_module` / `photovoltaic_module` / `silicon_material` — TCL科技
- `municipal_waste_treatment` — 中成股份
- `traditional_chinese_medicine` / `biological_drug` — 丰原药业（batch_005新建）
- `wind_power_generation` / `solar_power_generation` — 川能动力
- `cable_tv_equipment` / `network_equipment` — 华数传媒

### 关键网络核查
- **TCL科技（000100.SZ）**: 经网络核查，TCL科技已于2019年剥离消费电子和家电业务，当前核心主业为**半导体显示（TCL华星，2024年营收1,043亿元）**和**新能源光伏及硅材料（TCL中环）**。原始json数据中的main_business信息已过时，本次构建基于2024年年报最新业务披露。TCL科技的暴露节点聚焦于`lcd_panel`、`oled_panel`、`display_module`、`photovoltaic_module`、`silicon_material`，而非传统家电终端。

---

## 二、产业图构建

### 新建产业节点（11个）

| 类别 | node_id | 中文名 | entity_type | 对应公司 |
|---|---|---|---|---|
| **建材** | ready_mixed_concrete | 商品混凝土 | material | 盐田港 |
| **航空** | airport_operation_service | 机场运营服务 | service | 深圳机场 |
| **能源** | lpg | 液化石油气 | material | 广聚能源 |
| **航空** | general_aviation_service | 通用航空服务 | service | 中信海直 |
| **显示** | oled_panel | OLED面板 | component | TCL科技 |
| **环保** | hazardous_waste_treatment_service | 危险废物处理服务 | service | 中成股份 |
| **环保** | recycling_service | 再生资源回收服务 | service | 中成股份 |
| **医药** | chemical_drug | 化学药 | material | 丰原药业 |
| **广电** | cable_tv_network_service | 有线电视网络服务 | service | 华数传媒 |
| **通信** | broadband_network_service | 宽带网络服务 | service | 华数传媒 |
| **传媒** | new_media_service | 新媒体服务 | service | 华数传媒 |

### 新建产业流边（4条）

1. **能源**: refining_service → lpg（炼油服务产出液化石油气）
2. **医药**: pharmaceutical_raw_material → chemical_drug（原料药→化学药）
3. **广电**: cable_tv_equipment → cable_tv_network_service（设备支撑网络服务）
4. **通信**: network_equipment → broadband_network_service（网络设备支撑宽带服务）

---

## 三、公司视图构建

### 10家公司全部创建成功

| 股票代码 | 公司名 | 公司ID | 核心产业 |
|---|---|---|---|
| 000088.SZ | 盐田港 | yantian_port | 港口物流、商品混凝土 |
| 000089.SZ | 深圳机场 | shenzhen_airport | 机场运营 |
| 000090.SZ | 天健集团 | tianjian_group | 房地产开发、市政工程 |
| 000096.SZ | 广聚能源 | guangju_energy | 石油制品、LPG、电力投资 |
| 000099.SZ | 中信海直 | citic_offshore_helicopter | 通用航空 |
| 000100.SZ | TCL科技 | tcl_technology | 半导体显示、新能源光伏 |
| 000151.SZ | 中成股份 | zhongcheng | 固废治理、危废处理、再生资源 |
| 000153.SZ | 丰原药业 | fengyuan_pharmaceutical | 中成药、化学药、生物药 |
| 000155.SZ | 川能动力 | chuanneng_power | 风力发电、光伏发电 |
| 000156.SZ | 华数传媒 | huashu_media | 有线电视、宽带网络、新媒体 |

### 公司节点暴露（27条）

| 公司 | 暴露节点数 | 关键暴露 |
|---|---|---|
| 盐田港 | 3 | container_handling_service, logistics_service, ready_mixed_concrete |
| 深圳机场 | 1 | airport_operation_service |
| 天健集团 | 3 | residential_property, construction_service, commercial_property |
| 广聚能源 | 3 | petrochemical_product, lpg, electricity_power |
| 中信海直 | 1 | general_aviation_service |
| TCL科技 | 5 | lcd_panel, oled_panel, display_module, photovoltaic_module, silicon_material |
| 中成股份 | 3 | municipal_waste_treatment, hazardous_waste_treatment_service, recycling_service |
| 丰原药业 | 3 | traditional_chinese_medicine, chemical_drug, biological_drug |
| 川能动力 | 2 | wind_power_generation, solar_power_generation |
| 华数传媒 | 3 | cable_tv_network_service, broadband_network_service, new_media_service |

---

## 四、系统状态更新

```
Total nodes: 212 (+11)
Total edges: 177 (+4)
Total companies: 60 (+10)
Total exposures: 162 (+27)
```

---

## 五、关键发现与启发

### 1. 过期业务信息的修正
- TCL科技是本次构建最重要的发现：原始json中的main_business数据严重滞后（描述的是2019年前的家电业务），而实际主业已转变为半导体显示和新能源光伏。
- **启发**: 后续批次中，对于业务转型剧烈的公司（尤其是科技公司），必须通过网络核查确认最新业务结构，不能仅依赖json中的静态数据。

### 2. 服务型企业的暴露策略
- 盐田港（港口）、深圳机场（机场）、中信海直（通航）、华数传媒（网络）均为基础设施/平台运营商，其暴露节点均为**service**类型。
- 广聚能源作为能源贸易商，对`petrochemical_product`和`lpg`的activity_type使用了`provide_service`而非`manufacture`，准确反映了其贸易属性而非生产属性。

### 3. 医药三大分类的补齐
- batch_005建立了`traditional_chinese_medicine`和`biological_drug`，batch_006通过丰原药业补齐了`chemical_drug`，形成了中药-化学药-生物药的完整医药分类体系。
- 三者共同的上游均为`pharmaceutical_raw_material`，体现了医药产业的共性。

### 4. 环保产业的服务化趋势
- 中成股份代表了环保产业从"设备制造"向"服务运营"的转型。其暴露节点均为服务类（municipal_waste_treatment, hazardous_waste_treatment_service, recycling_service），而非设备节点。
- 这与batch_005中华控赛格的`environmental_protection_equipment`形成互补，覆盖了环保产业的"设备+服务"双维度。

### 5. 显示产业的节点细化
- TCL科技的加入使显示产业从`lcd_panel`扩展到`oled_panel`，反映了显示技术从LCD向OLED演进的技术路线。
- 同时TCL中环的硅材料和光伏业务暴露了`photovoltaic_module`和`silicon_material`，显示了一家企业的跨领域布局。

---

## 六、后续批次建议

1. **工程机械**: batch_007中的中联重科（000157）和徐工机械（000425，batch_009）均为工程机械龙头，可能需要新建`construction_machinery`等节点。
2. **水泥建材**: batch_007中的金隅冀东（000401）主营水泥，可复用已有`cement`节点。
3. **血液制品**: batch_007中的派林生物（000403）主营血液制品，医药细分领域需要新建`blood_product`节点。
4. **压缩机**: batch_007中的长虹华意（000404）主营冰箱压缩机，需要新建`refrigeration_compressor`节点。
