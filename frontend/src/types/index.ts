export type Confidence = "HIGH" | "MEDIUM" | "LOW";
export type NodeStatus = "ACTIVE" | "PENDING" | "REJECTED";
export type EntityType =
  | "material"
  | "part"
  | "device"
  | "equipment"
  | "system"
  | "software"
  | "infrastructure"
  | "process"
  | "service"
  | "technology_capability"
  | "platform"
  | "standard"
  | "data_asset"
  | "arachne_flow:resource"
  | "arachne_flow:action"
  | "arachne_flow:method"
  | "unknown";

export type IndustrialFlowType =
  | "material_input"
  | "energy_input"
  | "information_input"
  | "equipment_enablement"
  | "process_output"
  | "service_provision"
  | "capability_enablement"
  | "structural_composition"
  | "supply_relation"
  | "derived_from"
  | "unknown";

export type OntologyType =
  | "alias_of"
  | "is_a"
  | "part_of"
  | "variant_of"
  /** @deprecated `related_term` is deprecated; keep for backward compatibility only. */
  | "related_term";

export type EdgeNamespace = "industrial_flow" | "ontology" | "arachne_flow";

export type ProvRole = "entity" | "activity" | "agent";

export type ProvRelation =
  | "used"
  | "wasGeneratedBy"
  | "wasDerivedFrom"
  | "wasAttributedTo"
  | "wasAssociatedWith"
  | "actedOnBehalfOf";

export interface ProvStatement {
  statement_uuid: string;
  statement_id: string;
  node_id: string;
  node_role: ProvRole;
  prov_relation: ProvRelation;
  target_node_id: string;
  target_role: ProvRole;
  is_inferred: boolean;
  evidence: Evidence[];
  confidence: Confidence;
  status: NodeStatus;
  notes?: string;
  created_at?: string;
  updated_at?: string;
}

export interface PaginatedProvStatements {
  total: number;
  page: number;
  page_size: number;
  items: ProvStatement[];
}

export interface Evidence {
  source_title: string;
  source_url?: string;
  quote: string;
}

export interface IndustrialNode {
  node_uuid: string;
  node_id: string;
  canonical_name_zh: string;
  canonical_name_en?: string;
  aliases: string[];
  definition: string;
  entity_type: EntityType;
  evidence: Evidence[];
  confidence: Confidence;
  status: NodeStatus;
  notes?: string;
  created_at?: string;
  updated_at?: string;
}

export interface IndustryNodeAssociation {
  industry_id: string;
  role?: string;
  weight?: number;
  confidence?: Confidence;
  status?: NodeStatus;
  notes?: string;
}

export interface IndustrialNodeCreate {
  node_id: string;
  canonical_name_zh: string;
  canonical_name_en?: string;
  aliases: string[];
  definition: string;
  entity_type: EntityType;
  evidence: Evidence[];
  confidence: Confidence;
  status: NodeStatus;
  notes?: string;
  industry_ids?: IndustryNodeAssociation[];
}

export interface IndustrialNodeUpdate {
  canonical_name_zh?: string;
  canonical_name_en?: string;
  aliases?: string[];
  definition?: string;
  entity_type?: EntityType;
  evidence?: Evidence[];
  confidence?: Confidence;
  status?: NodeStatus;
  notes?: string;
}

export interface IndustrialNodeQuickCreate {
  node_id?: string;
  canonical_name_zh?: string;
  canonical_name_en?: string;
  aliases?: string[];
  definition?: string;
  entity_type?: EntityType;
  evidence?: Evidence[];
  confidence?: Confidence;
  status?: NodeStatus;
  notes?: string;
  industry_ids?: IndustryNodeAssociation[];
}

export interface BaseEdge {
  edge_uuid: string;
  edge_id: string;
  from_node: string;
  to_node: string;
  description: string;
  evidence: Evidence[];
  confidence: Confidence;
  notes?: string;
  created_at?: string;
  updated_at?: string;
  edge_type_label?: string;
}

export interface IndustrialFlowEdge extends BaseEdge {
  edge_namespace: "industrial_flow";
  edge_type: IndustrialFlowType;
}

export interface OntologyEdge extends BaseEdge {
  edge_namespace: "ontology";
  edge_type: OntologyType;
}

export interface ArachneFlowEdge extends BaseEdge {
  edge_namespace: "arachne_flow";
  edge_type: string;
}

export type GraphEdge = IndustrialFlowEdge | OntologyEdge | ArachneFlowEdge;

export interface GraphNode {
  node_id: string;
  label: string;
  entity_type: EntityType;
  node_uuid?: string;
  canonical_name_zh?: string;
  canonical_name_en?: string;
  aliases?: string[];
  definition?: string;
  evidence?: Evidence[];
  confidence?: string;
  status?: string;
  notes?: string;
  is_test?: boolean;
  created_at?: string;
  updated_at?: string;
  properties?: Record<string, unknown>;
}

export interface IndustrialFlowEdgeCreate {
  edge_namespace: "industrial_flow";
  edge_id: string;
  from_node: string;
  to_node: string;
  edge_type: IndustrialFlowType;
  description: string;
  evidence: Evidence[];
  confidence: Confidence;
  notes?: string;
}

export interface IndustrialFlowEdgeQuickCreate {
  edge_id?: string;
  from_node: string;
  to_node: string;
  edge_type?: IndustrialFlowType;
  description?: string;
  evidence?: Evidence[];
  confidence?: Confidence;
  notes?: string;
}

export interface OntologyEdgeCreate {
  edge_namespace: "ontology";
  edge_id: string;
  from_node: string;
  to_node: string;
  edge_type: OntologyType;
  description: string;
  evidence: Evidence[];
  confidence: Confidence;
  notes?: string;
}

export type GraphEdgeCreate = IndustrialFlowEdgeCreate | OntologyEdgeCreate;

export interface RejectedOrPendingItem {
  term: string;
  reason: string;
  suggested_action: string;
  evidence: Evidence[];
  notes?: string;
}

export interface GraphRegistrationBatch {
  batch_id: string;
  task_description: string;
  nodes_to_upsert: IndustrialNode[];
  edges_to_upsert: GraphEdge[];
  rejected_or_pending: RejectedOrPendingItem[];
}

export interface PaginatedNodes {
  total: number;
  page: number;
  page_size: number;
  items: IndustrialNode[];
}

export interface PaginatedEdges {
  total: number;
  page: number;
  page_size: number;
  items: GraphEdge[];
}

export interface GraphStats {
  total_nodes: number;
  total_edges: number;
  node_type_distribution: Record<string, number>;
  edge_namespace_distribution: Record<string, number>;
  edge_type_distribution: Record<string, number>;
  status_distribution: Record<string, number>;
  confidence_distribution: Record<string, number>;
}

export interface SubgraphResult {
  center_node_id: string;
  depth: number;
  nodes: IndustrialNode[];
  edges: GraphEdge[];
}

// ============================================================
// Industry Types
// ============================================================

export type IndustryType = "formal_industry" | "curated_view" | "theme_view";

export type RecordStatus = "ACTIVE" | "PENDING" | "REJECTED" | "ARCHIVED";

export interface Industry {
  industry_uuid: string;
  industry_id: string;
  name_zh: string;
  name_en?: string;
  aliases: string[];
  industry_type: IndustryType;
  description?: string;
  status: RecordStatus;
  notes?: string;
  created_at?: string;
  updated_at?: string;
}

export interface IndustryNodeMapping {
  mapping_uuid: string;
  mapping_id: string;
  industry_id: string;
  node_id: string;
  role?: string;
  weight: number;
  confidence: Confidence;
  evidence: Evidence[];
  status: RecordStatus;
  notes?: string;
  created_at?: string;
  updated_at?: string;
}

export interface PaginatedIndustries {
  total: number;
  page: number;
  page_size: number;
  items: Industry[];
}

export interface PaginatedMappings {
  total: number;
  page: number;
  page_size: number;
  items: IndustryNodeMapping[];
}

// ============================================================
// Company Types
// ============================================================

export type CompanyType = "public" | "private" | "state_owned" | "startup" | "unknown";

export type CompanyActivityType =
  | "rnd"
  | "design"
  | "manufacture"
  | "produce"
  | "integrate"
  | "operate"
  | "provide_service"
  | "procure"
  | "use"
  | "unknown";

export interface Company {
  company_uuid: string;
  company_id: string;
  name_zh: string;
  name_en?: string;
  aliases: string[];
  stock_codes: string[];
  description?: string;
  country: string;
  province?: string;
  city?: string;
  founded_year?: number;
  employee_count?: number;
  revenue_cny?: number;
  market_cap_cny?: number;
  net_profit_cny?: number;
  company_type: CompanyType;
  status: RecordStatus;
  notes?: string;
  created_at?: string;
  updated_at?: string;
}

export interface CompanyNodeExposure {
  exposure_uuid: string;
  exposure_id: string;
  company_id: string;
  node_id: string;
  activity_type: CompanyActivityType;
  role?: string;
  weight: number;
  confidence: Confidence;
  evidence: Evidence[];
  status: RecordStatus;
  as_of_date?: string;
  notes?: string;
  created_at?: string;
  updated_at?: string;
}

export interface PaginatedCompanies {
  total: number;
  page: number;
  page_size: number;
  items: Company[];
}

export interface PaginatedExposures {
  total: number;
  page: number;
  page_size: number;
  items: CompanyNodeExposure[];
}

// ============================================================
// Company Subgraph Types (公司子图域)
// ============================================================

export type SubgraphRelationType =
  | "inferred_industrial"
  | "evidenced_business"
  | "person_relation";

export type SubgraphRelationSubtype =
  | "upstream_of"
  | "downstream_of"
  | "supplier"
  | "customer"
  | "partner"
  | "shareholder"
  | "executive";

export interface CompanySubgraphNode {
  node_id: string;
  canonical_name_zh: string;
  entity_type: string;
  activity_type: string;
  weight: number;
  role?: string;
  exposure_confidence?: string;
}

export interface CompanySubgraphEdge {
  edge_id: string;
  from_node: string;
  to_node: string;
  edge_namespace: string;
  edge_type: string;
  edge_type_label?: string;
  description?: string;
  confidence?: string;
}

export interface CompanySubgraphRelation {
  relation_id?: number;
  from_company_id: string;
  to_company_id: string;
  relation_type: SubgraphRelationType;
  relation_subtype?: SubgraphRelationSubtype;
  strength: number;
  confidence: Confidence;
  evidence: Evidence[];
  notes?: string;
}

export interface CompanySubgraph {
  subgraph_uuid: string;
  subgraph_id: string;
  company_id: string;
  version_name?: string;
  description?: string;
  status: RecordStatus;
  nodes_summary?: { total: number; by_entity_type: Record<string, number> };
  edges_summary?: { total: number; by_edge_namespace: Record<string, number> };
  relations_summary?: { total: number; by_relation_type: Record<string, number> };
  created_at?: string;
  updated_at?: string;
  nodes: CompanySubgraphNode[];
  edges: CompanySubgraphEdge[];
  relations: CompanySubgraphRelation[];
}

export interface PaginatedCompanySubgraphs {
  total: number;
  page: number;
  page_size: number;
  items: CompanySubgraph[];
}

export interface ComputationJob {
  job_id: string;
  job_type: string;
  target_id?: string;
  status: string;
  total_items?: number;
  processed_items: number;
  result_summary?: Record<string, unknown>;
  error_message?: string;
  created_at?: string;
  started_at?: string;
  completed_at?: string;
}

export const ENTITY_TYPE_COLORS: Record<EntityType, string> = {
  material: "#f87171",
  part: "#fb923c",
  device: "#fbbf24",
  equipment: "#f59e0b",
  system: "#22d3ee",
  software: "#c084fc",
  infrastructure: "#818cf8",
  process: "#f97316",
  service: "#f472b6",
  technology_capability: "#94a3b8",
  platform: "#60a5fa",
  standard: "#a78bfa",
  data_asset: "#2dd4bf",
  "arachne_flow:resource": "#34d399",
  "arachne_flow:action": "#fbbf24",
  "arachne_flow:method": "#a78bfa",
  unknown: "#64748b",
};

export const EDGE_NAMESPACE_STYLES: Record<
  EdgeNamespace,
  { color: string; lineStyle: string }
> = {
  industrial_flow: { color: "#22d3ee", lineStyle: "solid" },
  ontology: { color: "#fbbf24", lineStyle: "dashed" },
  arachne_flow: { color: "#34d399", lineStyle: "solid" },
};

export const CONFIDENCE_OPACITY: Record<Confidence, number> = {
  HIGH: 1.0,
  MEDIUM: 0.75,
  LOW: 0.5,
};

export const EDGE_TYPE_LABELS: Record<string, string> = {
  // IndustrialFlowType
  material_input: "物料输入",
  energy_input: "能量输入",
  information_input: "信息输入",
  equipment_enablement: "设备使能",
  process_output: "工艺产出",
  service_provision: "服务提供",
  capability_enablement: "能力使能",
  structural_composition: "结构组成",
  supply_relation: "供应关系",
  derived_from: "派生自",
  unknown: "未知关系",
  // OntologyType
  alias_of: "别名/同义",
  is_a: "是一种",
  part_of: "组成部分",
  variant_of: "变体",
  // Deprecated ontology type — kept for backward compatibility with existing edges.
  related_term: "相关术语（已废弃）",
};


// Database check types
export type CheckSeverity = "ERROR" | "WARNING" | "INFO";

export interface DbCheckIssue {
  issue_id: string;
  check_id: string;
  severity: CheckSeverity;
  title: string;
  summary: string;
  details: Record<string, unknown>;
  affected_ids: string[];
  fixable: boolean;
}

export interface DbCheckResult {
  check_id: string;
  name: string;
  description: string;
  severity: CheckSeverity;
  fixable: boolean;
  issues: DbCheckIssue[];
  issue_count: number;
}

export interface DbCheckMeta {
  check_id: string;
  name: string;
  description: string;
  severity: CheckSeverity;
  fixable: boolean;
}

export interface DbFixResult {
  check_id: string;
  fixed_count: number;
  skipped_count: number;
  messages: string[];
}

// ============================================================
// UI / Shared Types
// ============================================================

export type PanelType =
  | "none"
  | "node-detail"
  | "edge-detail"
  | "node-create"
  | "node-edit"
  | "edge-create"
  | "edge-edit"
  | "batch-upload"
  | "industry-detail"
  | "industry-create"
  | "industry-edit"
  | "company-detail"
  | "company-create"
  | "company-edit"
  | "node-companies"
  | "multi-node-companies"
  | "node-industries"
  | "node-prov"
  | "company-relation-detail";

export interface FlowSummary {
  flow_id: string;
  title: string;
  root_product: string;
  file: string;
  triples: number;
  status?: string;
  md5?: string;
  compiled_at?: string;
}

export interface FlowCompileResult {
  flow_id: string;
  resources: number;
  actions: number;
  methods: number;
  edges: number;
  dual: number;
}

export interface EngineInfo {
  name: string;
  label: string;
  description?: string;
  is_read_only?: boolean;
  supports_flows?: boolean;
  default_view?: string;
}

// Company network node type used for canvas
export interface CompanyNetworkNode {
  company_id: string;
  name_zh: string;
  company_type: string;
  status: string;
}

export interface CompanyNetworkEdge {
  from_company_id: string;
  to_company_id: string;
  path_count: number;
  strength: number;
  confidence: string;
  relation_type?: string;
  relation_subtype?: string;
}

// Backward-compatible aliases
export type CNode = CompanyNetworkNode;
export type CEdge = CompanyNetworkEdge;

// Reasoning kernel types
export * from "./reasoning";
