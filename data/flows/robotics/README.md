# Robotics arachne-flow files

机器人产业流程图：零部件（shared）→ 本体（各形态）→ 集成与服务。

## 结构

**共享零部件链（被各本体流程 include）**
- `joint_module_manufacturing.yaml` — 减速器/无框电机/丝杠/编码器/驱动器 → 关节执行器
- `dexterous_hand_manufacturing.yaml` — 空心杯电机/丝杠/触觉传感 → 灵巧手
- `servo_system_manufacturing.yaml` — 电机/驱动器/编码器 → 伺服系统
- `robot_control_system.yaml` — 主控计算平台/控制器/控制软件 → 控制系统
- `perception_suite.yaml` — 视觉/力觉/触觉/IMU/激光雷达 → 感知套件

**本体流程（一个文件 = 一种形态）**
- `industrial_robot_manufacturing.yaml` — 工业机器人 + 协作机器人（basis 衍生）
- `humanoid_robot_manufacturing.yaml` — 人形机器人 + 双足/轮足/轮臂三个形态变体（basis 衍生）
- `quadruped_robot_manufacturing.yaml` — 四足机器人（机器狗）
- `mobile_robot_manufacturing.yaml` — 移动机器人（AGV/AMR）
- `service_robot_manufacturing.yaml` — 服务机器人

**集成与服务**
- `robot_system_integration_service.yaml` — 本体 → 系统集成 → 自动化产线
- `warehouse_automation.yaml` — 移动机器人 → 自动化仓储
- `robot_services.yaml` — 机器人租赁（RaaS）与运维服务

## 建模说明

- 形态变体用 `basis` 角色（以通用平台衍生），不用 component——与 semiconductor/ssd.yaml 的变体惯例一致。
- 服务类流程：RaaS 用 `basis`（以机器人本体为资产基础），运维用 `subject`（以本体为作用对象）。
- RESOURCE/METHOD 均为全局节点（对应 PG industrial_nodes），ACTION 按文件名命名空间化。
