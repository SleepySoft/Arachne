# Arachne Graph Reasoning Kernel 设计文档 V0.2

## 1. 定位

Arachne 是结构化图推理内核。

职责范围：

1. 管理稳定图谱。
2. 根据确定对象 ID 执行图查询与推理。
3. 生成临时推理图、路径、证据链、分数、特征表。
4. 为上游 AI、IIS、量化程序提供机器可读输出。
5. 生成候选节点、候选关系，供后续审核沉淀。

边界约束：

1. 不接入大模型。
2. 不处理自然语言输入。
3. 不执行语义消歧。
4. 不输出定性判断。
5. 不预测未来。
6. 不将推理结果直接写入正式图。
7. 不在正式图之间建立跨图边。

***

## 2. 图谱结构

Arachne 当前包含三类正式图。

```text
1. Industrial Graph
   产业图。描述稳定产业实体、产业流、本体关系。

2. Relationship Graph
   关系图。描述企业、组织、人之间的事实关系。

3. Concept Graph
   概念图。描述经验、因果、机制、规则、抽象概念。
```

正式图之间无直接边。

跨图关联依赖 PostgreSQL metadata。

推理阶段可生成跨图临时图。

临时图可缓存、审计、过期、导出。

临时图不得直接转写为正式图。

***

## 3. 外部系统分工

### 3.1 IIS

IIS 负责：

```text
- 情报采集
- 原文解析
- 信息抽取
- claim 生成
- 实体候选生成
- 关系候选生成
- 来源与 quote 维护
```

Arachne 接收 IIS 的结构化结果。

### 3.2 上游 AI / 应用层

上游 AI 或应用层负责：

```text
- 用户意图理解
- 查询词规范化
- 候选对象选择
- 推理任务构造
- Arachne 输出解释
- 定性分析
- 报告生成
```

### 3.3 Arachne

Arachne 负责：

```text
- 对象查询
- 对象 ID 返回
- 图遍历
- 路径搜索
- 临时图构建
- 证据链聚合
- 分数计算
- 特征表输出
- 候选入图对象生成
- 规则校验
```

***

## 4. 调用流程

推理调用分两阶段。

```text
Stage 1: Object Resolution
查询接口返回确切对象 ID。

Stage 2: Reasoning Execution
推理接口接收对象 ID，执行确定性推理任务。
```

完整流程：

```text
IIS / 上游 AI
   ↓
ObjectQueryRequest
   ↓
Arachne Query API
   ↓
ObjectQueryResult
   ↓
上游选择 node_id / edge_id / claim_id
   ↓
ReasoningTask
   ↓
Arachne Reasoning API
   ↓
ReasoningResultEnvelope
```

***

## 5. 对象查询接口

### 5.1 设计原则

查询接口用于获取确切对象 ID。

接口不执行 LLM 语义匹配。

接口不执行主观消歧。

接口可以使用确定性检索能力：

```text
- exact match
- alias match
- normalized name match
- prefix match
- keyword match
- metadata filter
- graph filter
- entity_type filter
- confidence/status filter
```

查询结果返回候选对象列表。

候选选择由上游完成。

### 5.2 ObjectQueryRequest

```python
class ObjectQueryRequest(BaseModel):
    query_id: str

    query_text: str

    query_scope: Literal[
        "industrial_node",
        "industrial_edge",
        "relationship_node",
        "relationship_edge",
        "concept_node",
        "concept_edge",
        "metadata",
        "claim"
    ]

    search_mode: Literal[
        "exact",
        "alias",
        "normalized",
        "keyword",
        "prefix"
    ] = "normalized"

    filters: dict = {}

    limit: int = 20

    include_evidence: bool = False
    include_metadata: bool = True
```

### 5.3 ObjectQueryResult

```python
class ObjectQueryResult(BaseModel):
    query_id: str

    status: Literal[
        "success",
        "no_result",
        "partial",
        "failed"
    ]

    candidates: List["ObjectCandidate"]

    diagnostics: dict = {}
```

```python
class ObjectCandidate(BaseModel):
    object_id: str

    object_kind: Literal[
        "node",
        "edge",
        "claim",
        "metadata"
    ]

    graph: Optional[Literal[
        "industrial",
        "relationship",
        "concept"
    ]] = None

    canonical_name: Optional[str] = None
    aliases: List[str] = []

    entity_type: Optional[str] = None
    edge_type: Optional[str] = None

    status: Optional[str] = None
    confidence: Optional[str] = None

    match_type: Literal[
        "exact",
        "alias",
        "normalized",
        "keyword",
        "prefix",
        "metadata"
    ]

    match_score: Optional[float] = None

    evidence_refs: List[str] = []
    metadata: dict = {}
```

### 5.4 查询输出约束

查询接口只返回候选对象。

查询接口不返回推理路径。

查询接口不返回影响判断。

查询接口不选择唯一对象。

当返回多个候选时，上游必须显式选择对象 ID。

***

## 6. 推理输入接口

### 6.1 ReasoningTask

所有推理任务使用统一输入外壳。

```python
class ReasoningTask(BaseModel):
    task_id: str

    task_type: Literal[
        "association",
        "impact_propagation",
        "bottleneck_detection",
        "substitution_search",
        "candidate_discovery",
        "cross_graph_context"
    ]

    source_nodes: List[str] = []
    source_edges: List[str] = []
    source_claims: List[str] = []
    source_metadata: List[str] = []

    parameters: dict = {}

    constraints: "ReasoningConstraints"

    requested_outputs: List[Literal[
        "temporary_graph",
        "subgraph",
        "paths",
        "evidence_chains",
        "node_scores",
        "edge_scores",
        "candidate_nodes",
        "candidate_edges",
        "feature_tables",
        "adjacency_matrix"
    ]]

    context: Optional["TaskContext"] = None
```

### 6.2 输入约束

`source_nodes`、`source_edges`、`source_claims` 必须使用确切 ID。

Arachne 不接受以下输入作为推理起点：

```text
- 自然语言问题
- 未解析实体名
- 未确认候选词
- 模糊产业概念
- 无 graph scope 的对象
```

非法示例：

```json
{
  "task_type": "impact_propagation",
  "source_nodes": ["镓"]
}
```

合法示例：

```json
{
  "task_type": "impact_propagation",
  "source_nodes": ["gallium"]
}
```

***

## 7. ReasoningConstraints

```python
class ReasoningConstraints(BaseModel):
    max_depth: int = 3
    max_paths: int = 100
    max_nodes: int = 500
    max_edges: int = 1000

    allowed_graphs: List[Literal[
        "industrial",
        "relationship",
        "concept"
    ]] = ["industrial"]

    allowed_node_types: Optional[List[str]] = None
    allowed_edge_namespaces: Optional[List[str]] = None
    allowed_edge_types: Optional[List[str]] = None

    min_node_confidence: Confidence = Confidence.LOW
    min_edge_confidence: Confidence = Confidence.LOW

    include_pending_nodes: bool = False
    include_low_confidence_edges: bool = True

    traversal_direction: Literal[
        "forward",
        "backward",
        "both"
    ] = "forward"

    stop_node_types: Optional[List[str]] = None

    allow_cross_graph_metadata_links: bool = False

    require_evidence: bool = False
```

***

## 8. TaskContext

```python
class TaskContext(BaseModel):
    region_ids: List[str] = []

    time_window_start: Optional[datetime] = None
    time_window_end: Optional[datetime] = None

    metadata_filters: dict = {}

    upstream_system: Optional[str] = None
    upstream_trace_id: Optional[str] = None

    notes: Optional[str] = None
```

地域、时间、行业标签、来源范围优先作为 metadata filter 使用。

地域暂不进入 V0.2 正式图类型。

***

## 9. 推理任务类型

### 9.1 Association

输入：

```text
- source_nodes
- max_depth
- traversal_direction
- allowed_edge_types
```

输出：

```text
- subgraph
- paths
- evidence_chains
- feature_tables
```

用途：

```text
- 上下游展开
- 邻域结构获取
- 产业链局部结构导出
```

***

### 9.2 Impact Propagation

输入：

```text
- source_nodes
- event_type
- propagation_profile
- decay policy
- allowed_edge_types
```

输出：

```text
- temporary_graph
- paths
- node_scores
- edge_scores
- evidence_chains
- feature_tables
```

`event_type` 由上游提供。

Arachne 根据 `propagation_profile` 使用确定性传播规则。

示例：

```json
{
  "event_type": "supply_shock",
  "propagation_profile": "supply_forward"
}
```

***

### 9.3 Bottleneck Detection

输入：

```text
- source_nodes
- analysis_scope
- metrics
```

输出：

```text
- subgraph
- node_scores
- paths
- feature_tables
```

可计算指标：

```text
- in_degree
- out_degree
- path_frequency
- betweenness
- downstream_dependency_count
- evidence_coverage
```

***

### 9.4 Substitution Search

输入：

```text
- source_nodes
- substitution_modes
- allowed_edge_types
```

输出：

```text
- temporary_graph
- candidate_nodes
- paths
- node_scores
- evidence_chains
- feature_tables
```

替代候选仅表示结构候选。

可行性评估由上游完成。

***

### 9.5 Candidate Discovery

输入：

```text
- IIS candidate_entities
- IIS candidate_relations
- source_claims
```

输出：

```text
- candidate_nodes
- candidate_edges
- nearest_existing_objects
- conflict_report
- evidence_chains
- diagnostics
```

用途：

```text
- 新物料发现
- 新工艺发现
- 新产业关系发现
- 入图候选生成
```

***

### 9.6 Cross Graph Context

输入：

```text
- source_nodes
- metadata linkage constraints
- allowed_graphs
```

输出：

```text
- temporary_graph
- metadata_links
- paths
- feature_tables
```

用途：

```text
- 产业节点关联公司暴露
- 公司节点关联产业能力
- 概念机制关联产业路径
```

跨图连接只出现在临时图。

***

## 10. 统一输出外壳

### 10.1 ReasoningResultEnvelope

```python
class ReasoningResultEnvelope(BaseModel):
    reasoning_id: str
    task_id: str
    task_type: str

    status: Literal[
        "success",
        "partial",
        "failed",
        "no_result"
    ]

    generated_at: datetime

    input_fingerprint: str
    graph_snapshot_ids: List[str]

    output_types: List[str]

    result_payload: dict

    diagnostics: "ReasoningDiagnostics"
```

输出统一使用 envelope。

`result_payload` 按 `task_type` 差异化。

***

## 11. 统一输出组件

### 11.1 TemporaryReasoningGraph

```python
class TemporaryReasoningGraph(BaseModel):
    temp_graph_id: str
    reasoning_id: str

    graph_scope: Literal[
        "single_graph",
        "cross_graph"
    ]

    source_graphs: List[Literal[
        "industrial",
        "relationship",
        "concept"
    ]]

    nodes: List["TempGraphNode"]
    edges: List["TempGraphEdge"]

    metadata_links: List["MetadataLink"] = []

    created_at: datetime
    expires_at: Optional[datetime] = None
```

```python
class TempGraphNode(BaseModel):
    temp_node_id: str

    origin_graph: Optional[Literal[
        "industrial",
        "relationship",
        "concept",
        "iis",
        "reasoning",
        "metadata"
    ]]

    origin_node_id: Optional[str] = None

    node_type: str
    label: str

    properties: dict = {}

    score: Optional[float] = None
    score_components: dict = {}

    evidence_refs: List[str] = []
```

```python
class TempGraphEdge(BaseModel):
    temp_edge_id: str

    origin_graph: Optional[Literal[
        "industrial",
        "relationship",
        "concept",
        "metadata",
        "reasoning"
    ]]

    origin_edge_id: Optional[str] = None

    from_temp_node_id: str
    to_temp_node_id: str

    edge_namespace: str
    edge_type: str

    properties: dict = {}

    weight: Optional[float] = None
    score_components: dict = {}

    evidence_refs: List[str] = []
```

***

### 11.2 SubgraphOutput

```python
class SubgraphOutput(BaseModel):
    center_nodes: List[str]
    depth: int

    nodes: List[dict]
    edges: List[dict]

    truncated: bool
    truncation_reason: Optional[str] = None
```

`SubgraphOutput` 只包含正式图中的原始节点与边。

***

### 11.3 PathOutput

```python
class PathOutput(BaseModel):
    paths: List["ReasoningPath"]

    total_paths_found: int
    returned_paths: int

    truncated: bool
    truncation_reason: Optional[str] = None
```

```python
class ReasoningPath(BaseModel):
    path_id: str

    start_node_id: str
    end_node_id: str

    node_sequence: List[str]
    edge_sequence: List[str]

    graph_sequence: List[str]

    path_length: int

    path_score: Optional[float] = None
    score_components: dict = {}

    evidence_chain_id: Optional[str] = None

    flags: List[str] = []
```

***

### 11.4 EvidenceChain

```python
class EvidenceChain(BaseModel):
    evidence_chain_id: str

    supports: Literal[
        "node",
        "edge",
        "path",
        "candidate_node",
        "candidate_edge",
        "score"
    ]

    target_id: str

    evidence_items: List["EvidenceRef"]

    completeness: Literal[
        "complete",
        "partial",
        "missing"
    ]
```

```python
class EvidenceRef(BaseModel):
    evidence_id: str

    source_system: Literal[
        "industrial_graph",
        "relationship_graph",
        "concept_graph",
        "iis",
        "manual"
    ]

    source_title: str
    source_url: Optional[str] = None
    quote: str

    collected_at: Optional[datetime] = None

    reliability: Confidence
```

***

### 11.5 NodeScore

```python
class NodeScore(BaseModel):
    node_id: str
    graph: str

    score: float
    rank: int

    score_type: str

    score_components: dict

    source_paths: List[str] = []
    evidence_chain_ids: List[str] = []

    flags: List[str] = []
```

***

### 11.6 EdgeScore

```python
class EdgeScore(BaseModel):
    edge_id: str
    graph: str

    score: float
    rank: int

    score_type: str

    score_components: dict

    source_paths: List[str] = []
    evidence_chain_ids: List[str] = []

    flags: List[str] = []
```

***

### 11.7 FeatureTable

```python
class FeatureTable(BaseModel):
    table_id: str

    entity_level: Literal[
        "node",
        "edge",
        "path",
        "candidate"
    ]

    columns: List[str]
    rows: List[dict]
```

FeatureTable 面向量化程序、Notebook、BI、上游 AI。

***

## 12. Diagnostics

```python
class ReasoningDiagnostics(BaseModel):
    truncated: bool = False
    truncation_reason: Optional[str] = None

    warnings: List[str] = []

    rule_violations: List[dict] = []

    missing_evidence_count: int = 0
    low_confidence_node_count: int = 0
    low_confidence_edge_count: int = 0
    pending_node_count: int = 0

    dangling_reference_count: int = 0

    graph_boundary_crossed: bool = False
    metadata_links_used: int = 0

    execution_time_ms: int
```

Diagnostics 供上游控制解释强度、过滤结果、降低权重、触发复核。

***

## 13. 产业图边的推理增强字段

建议为 `IndustrialFlowEdge` 增加可选推理字段。

```python
class IndustrialFlowReasoningAttributes(BaseModel):
    role_of_from_node: Optional[str] = None

    dependency_strength: Optional[Literal[
        "critical",
        "important",
        "optional",
        "unknown"
    ]] = "unknown"

    substitutability: Optional[Literal[
        "low",
        "medium",
        "high",
        "unknown"
    ]] = "unknown"

    cost_sensitivity: Optional[Literal[
        "low",
        "medium",
        "high",
        "unknown"
    ]] = "unknown"

    supply_risk_sensitivity: Optional[Literal[
        "low",
        "medium",
        "high",
        "unknown"
    ]] = "unknown"

    reasoning_weight: Optional[float] = None
```

用途：

```text
- 影响传播权重计算
- 瓶颈识别
- 替代搜索
- 路径排序
- 量化特征生成
```

***

## 14. Candidate Discovery 输出

### 14.1 CandidateNode

```python
class CandidateNodeOutput(BaseModel):
    candidate_id: str

    proposed_graph: Literal[
        "industrial",
        "relationship",
        "concept"
    ]

    proposed_node_id: Optional[str] = None

    canonical_name: str
    aliases: List[str] = []

    proposed_entity_type: Optional[str] = None

    source_claims: List[str] = []

    nearest_existing_objects: List[str] = []

    evidence_chain_ids: List[str] = []

    validation_status: Literal[
        "valid",
        "warning",
        "invalid",
        "needs_review"
    ]

    rule_violations: List[dict] = []

    flags: List[str] = []
```

### 14.2 CandidateEdge

```python
class CandidateEdgeOutput(BaseModel):
    candidate_id: str

    proposed_graph: Literal[
        "industrial",
        "relationship",
        "concept"
    ]

    from_object_id: Optional[str] = None
    to_object_id: Optional[str] = None

    from_text: Optional[str] = None
    to_text: Optional[str] = None

    proposed_edge_namespace: Optional[str] = None
    proposed_edge_type: Optional[str] = None

    source_claims: List[str] = []

    evidence_chain_ids: List[str] = []

    validation_status: Literal[
        "valid",
        "warning",
        "invalid",
        "needs_review"
    ]

    rule_violations: List[dict] = []

    flags: List[str] = []
```

Candidate 输出进入审核流程。

审核通过后才允许写入正式图。

***

## 15. 输出组合规范

### 15.1 Association

默认输出：

```text
- subgraph
- paths
- evidence_chains
- feature_tables
```

可选输出：

```text
- node_scores
- temporary_graph
```

### 15.2 Impact Propagation

默认输出：

```text
- temporary_graph
- paths
- node_scores
- edge_scores
- evidence_chains
- feature_tables
```

### 15.3 Bottleneck Detection

默认输出：

```text
- subgraph
- node_scores
- paths
- feature_tables
```

可选输出：

```text
- evidence_chains
- temporary_graph
```

### 15.4 Substitution Search

默认输出：

```text
- temporary_graph
- candidate_nodes
- paths
- node_scores
- evidence_chains
- feature_tables
```

### 15.5 Candidate Discovery

默认输出：

```text
- candidate_nodes
- candidate_edges
- nearest_existing_objects
- evidence_chains
- diagnostics
```

### 15.6 Cross Graph Context

默认输出：

```text
- temporary_graph
- metadata_links
- paths
- feature_tables
- diagnostics
```

***

## 16. 示例调用

### 16.1 查询对象 ID

```json
{
  "query_id": "qry_001",
  "query_text": "镓",
  "query_scope": "industrial_node",
  "search_mode": "normalized",
  "filters": {
    "entity_type": ["material"],
    "status": ["ACTIVE", "PENDING"]
  },
  "limit": 10,
  "include_evidence": true,
  "include_metadata": true
}
```

返回：

```json
{
  "query_id": "qry_001",
  "status": "success",
  "candidates": [
    {
      "object_id": "gallium",
      "object_kind": "node",
      "graph": "industrial",
      "canonical_name": "镓",
      "aliases": ["Ga"],
      "entity_type": "material",
      "status": "ACTIVE",
      "confidence": "HIGH",
      "match_type": "exact",
      "match_score": 1.0,
      "evidence_refs": ["ev_gallium_001"],
      "metadata": {}
    }
  ],
  "diagnostics": {}
}
```

### 16.2 发起影响传播

```json
{
  "task_id": "task_impact_gallium_001",
  "task_type": "impact_propagation",
  "source_nodes": ["gallium"],
  "source_claims": ["iis_claim_20260702_001"],
  "parameters": {
    "event_type": "supply_shock",
    "propagation_profile": "supply_forward",
    "edge_weight_policy": "default_industrial_flow_v1",
    "decay": {
      "method": "depth_decay",
      "factor": 0.75
    }
  },
  "constraints": {
    "max_depth": 4,
    "max_paths": 100,
    "allowed_graphs": ["industrial"],
    "allowed_edge_types": [
      "material_input",
      "process_output",
      "structural_composition",
      "supply_relation"
    ],
    "traversal_direction": "forward",
    "include_pending_nodes": false,
    "include_low_confidence_edges": true,
    "allow_cross_graph_metadata_links": false,
    "require_evidence": false
  },
  "requested_outputs": [
    "temporary_graph",
    "paths",
    "node_scores",
    "evidence_chains",
    "feature_tables"
  ]
}
```

***

## 17. 主图沉淀规则

以下对象可进入候选沉淀流程：

```text
- 新稳定产业实体
- 新稳定产业关系
- 新概念规则
- 新关系图事实
```

以下对象仅保留为情报、临时图、推理输出或上游分析材料：

```text
- 短期价格变化
- 公司扩产事件
- 政策扰动
- 新闻事件
- 机构观点
- 市场预测
- 推理路径
- 影响分数
- 机会或风险假设
```

正式入图流程：

```text
Candidate
   ↓
Schema Validation
   ↓
Rule Check
   ↓
Duplicate / Conflict Check
   ↓
Evidence Check
   ↓
Human Review
   ↓
Formal Graph Upsert
```

***

## 18. V0.2 硬约束

```text
1. 推理前必须先解析对象 ID。
2. 推理接口只接受确切 ID。
3. 查询接口只返回候选对象。
4. 查询接口不执行语义消歧。
5. 上游负责候选选择。
6. Arachne 不接入大模型。
7. Arachne 不输出自然语言结论。
8. Arachne 输出结构化原始推理材料。
9. 三类正式图之间无正式边。
10. 跨图推理依赖 metadata 与临时图。
11. 临时图不得直接写入正式图。
12. 推理结果不得直接写入正式图。
13. 候选节点和候选边必须经过审核沉淀。
14. 所有输出必须携带 diagnostics。
15. 涉及证据的输出必须返回 evidence_refs 或 evidence_chains。
```

***

## 19. V0.2 核心定义

Arachne 的工程定义：

```text
Arachne 接收确切对象 ID 和结构化推理任务，
在正式图与 metadata 之上执行确定性图推理，
输出临时图、子图、路径、证据链、分数与特征表，
供上游 AI、IIS、量化程序和人工研究流程继续处理。
```

V0.2 的最小实现对象：

```text
1. ObjectQueryRequest
2. ObjectQueryResult
3. ReasoningTask
4. ReasoningConstraints
5. ReasoningResultEnvelope
6. TemporaryReasoningGraph
7. ReasoningPath
8. EvidenceChain
9. NodeScore / EdgeScore
10. FeatureTable
11. ReasoningDiagnostics
```

优先实现顺序：

```text
1. Object Query API
2. Association
3. Impact Propagation
4. EvidenceChain
5. FeatureTable
6. Candidate Discovery
7. Bottleneck Detection
8. Substitution Search
9. Cross Graph Context
