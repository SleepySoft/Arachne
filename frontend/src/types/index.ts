export type Confidence = "HIGH" | "MEDIUM" | "LOW";
export type NodeStatus = "ACTIVE" | "PENDING" | "REJECTED";
export type EntityType =
  | "material"
  | "component"
  | "device"
  | "module"
  | "subsystem"
  | "system"
  | "platform"
  | "infrastructure"
  | "application_system"
  | "service"
  | "technology_capability"
  | "unknown";

export type IndustrialFlowType =
  | "material_flow"
  | "composition"
  | "energy_flow"
  | "information_flow"
  | "capability_supply"
  | "service_flow";

export type OntologyType =
  | "alias_of"
  | "is_a"
  | "variant_of"
  | "related_term";

export type EdgeNamespace = "industrial_flow" | "ontology";

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
}

export interface IndustrialFlowEdge extends BaseEdge {
  edge_namespace: "industrial_flow";
  edge_type: IndustrialFlowType;
}

export interface OntologyEdge extends BaseEdge {
  edge_namespace: "ontology";
  edge_type: OntologyType;
}

export type GraphEdge = IndustrialFlowEdge | OntologyEdge;

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

export const ENTITY_TYPE_COLORS: Record<EntityType, string> = {
  material: "#f87171",
  component: "#fb923c",
  device: "#fbbf24",
  module: "#a3e635",
  subsystem: "#34d399",
  system: "#22d3ee",
  platform: "#60a5fa",
  infrastructure: "#818cf8",
  application_system: "#c084fc",
  service: "#f472b6",
  technology_capability: "#94a3b8",
  unknown: "#64748b",
};

export const EDGE_NAMESPACE_STYLES: Record<
  EdgeNamespace,
  { color: string; lineStyle: string }
> = {
  industrial_flow: { color: "#22d3ee", lineStyle: "solid" },
  ontology: { color: "#fbbf24", lineStyle: "dashed" },
};

export const CONFIDENCE_OPACITY: Record<Confidence, number> = {
  HIGH: 1.0,
  MEDIUM: 0.75,
  LOW: 0.5,
};
