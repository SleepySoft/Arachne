export type QueryScope =
  | "industrial_node"
  | "industrial_edge"
  | "factual_node"
  | "factual_edge"
  | "company"
  | "industry"
  | "claim";

export type SearchMode = "exact" | "alias" | "normalized" | "keyword" | "prefix";

export type ObjectKind = "node" | "edge" | "claim" | "metadata";

export type GraphType = "industrial" | "factual" | "concept";

export type MatchType =
  | "exact"
  | "alias"
  | "normalized"
  | "keyword"
  | "prefix"
  | "metadata";

export type TaskType =
  | "association"
  | "impact_propagation"
  | "bottleneck_detection"
  | "substitution_search"
  | "candidate_discovery"
  | "cross_graph_context";

export type TraversalDirection = "forward" | "backward" | "both";

export type OutputType =
  | "temporary_graph"
  | "subgraph"
  | "paths"
  | "evidence_chains"
  | "node_scores"
  | "edge_scores"
  | "candidate_nodes"
  | "candidate_edges"
  | "feature_tables"
  | "adjacency_matrix";

export type ResultStatus = "success" | "partial" | "failed" | "no_result";

export interface ObjectQueryRequest {
  query_id: string;
  query_text: string;
  query_scope: QueryScope;
  search_mode?: SearchMode;
  filters?: Record<string, unknown>;
  limit?: number;
  include_evidence?: boolean;
  include_metadata?: boolean;
}

export interface ObjectCandidate {
  object_id: string;
  object_kind: ObjectKind;
  graph?: GraphType;
  canonical_name?: string;
  aliases: string[];
  entity_type?: string;
  edge_type?: string;
  status?: string;
  confidence?: string;
  match_type: MatchType;
  match_score?: number;
  evidence_refs: string[];
  metadata: Record<string, unknown>;
}

export interface ObjectQueryResult {
  query_id: string;
  status: ResultStatus;
  candidates: ObjectCandidate[];
  diagnostics: Record<string, unknown>;
}

export interface ReasoningConstraints {
  max_depth?: number;
  max_paths?: number;
  max_nodes?: number;
  max_edges?: number;
  allowed_graphs?: GraphType[];
  allowed_node_types?: string[];
  allowed_edge_namespaces?: string[];
  allowed_edge_types?: string[];
  min_node_confidence?: string;
  min_edge_confidence?: string;
  include_pending_nodes?: boolean;
  include_low_confidence_edges?: boolean;
  traversal_direction?: TraversalDirection;
  stop_node_types?: string[];
  allow_cross_graph_metadata_links?: boolean;
  require_evidence?: boolean;
}

export interface ReasoningTask {
  task_id: string;
  task_type: TaskType;
  source_nodes?: string[];
  source_edges?: string[];
  source_claims?: string[];
  source_metadata?: string[];
  parameters?: Record<string, unknown>;
  constraints: ReasoningConstraints;
  requested_outputs: OutputType[];
  context?: Record<string, unknown>;
}

export interface ReasoningDiagnostics {
  truncated?: boolean;
  truncation_reason?: string | null;
  warnings: string[];
  rule_violations?: Record<string, unknown>[];
  missing_evidence_count?: number;
  low_confidence_node_count?: number;
  low_confidence_edge_count?: number;
  pending_node_count?: number;
  dangling_reference_count?: number;
  graph_boundary_crossed?: boolean;
  metadata_links_used?: number;
  execution_time_ms?: number;
}

export interface ReasoningResultEnvelope {
  reasoning_id: string;
  task_id: string;
  task_type: string;
  status: ResultStatus;
  generated_at: string;
  input_fingerprint: string;
  graph_snapshot_ids: string[];
  output_types: string[];
  result_payload: Record<string, unknown>;
  diagnostics: ReasoningDiagnostics;
}

export interface ReasoningSubgraphNode {
  node_uuid?: string;
  node_id: string;
  canonical_name_zh?: string;
  canonical_name_en?: string;
  entity_type?: string;
  confidence?: string;
  status?: string;
  aliases?: string[];
  definition?: string;
  [key: string]: unknown;
}

export interface ReasoningSubgraphEdge {
  edge_uuid?: string;
  edge_id: string;
  from_node: string;
  to_node: string;
  edge_namespace?: string;
  edge_type?: string;
  description?: string;
  confidence?: string;
  [key: string]: unknown;
}

export interface ReasoningSubgraph {
  nodes: ReasoningSubgraphNode[];
  edges: ReasoningSubgraphEdge[];
}

export interface ReasoningPath {
  path_id: string;
  start_node_id: string;
  end_node_id: string;
  node_sequence: string[];
  edge_sequence: string[];
  graph_sequence: string[];
  path_length: number;
  path_score: number;
  score_components?: Record<string, unknown>;
}

export interface PathOutput {
  paths: ReasoningPath[];
  total_paths_found: number;
  returned_paths: number;
  truncated: boolean;
  truncation_reason?: string | null;
}

export interface NodeScore {
  node_id: string;
  graph: string;
  score: number;
  rank: number;
  score_type: string;
  score_components: Record<string, unknown>;
  source_paths?: string[];
  evidence_chain_ids?: string[];
  flags?: string[];
}

export interface EdgeScore {
  edge_id: string;
  graph: string;
  score: number;
  rank: number;
  score_type: string;
  score_components: Record<string, unknown>;
}

export interface EvidenceRef {
  evidence_id: string;
  source_system: string;
  source_title: string;
  source_url?: string;
  quote: string;
  collected_at?: string;
  reliability?: string;
}

export interface EvidenceChain {
  evidence_chain_id: string;
  supports: "node" | "edge" | "path" | "candidate_node" | "candidate_edge" | "score";
  target_id: string;
  evidence_items: EvidenceRef[];
  completeness: "complete" | "partial" | "missing";
}

export interface FeatureTable {
  table_id: string;
  entity_level: "node" | "edge" | "path" | "candidate";
  columns: string[];
  rows: Record<string, unknown>[];
}

export interface TempGraphNode {
  temp_node_id: string;
  origin_graph: string;
  origin_node_id: string;
  node_type: string;
  label: string;
  properties: Record<string, unknown>;
  score?: number;
  score_components?: Record<string, unknown>;
  evidence_refs?: string[];
}

export interface TempGraphEdge {
  temp_edge_id: string;
  origin_graph: string;
  origin_edge_id: string;
  from_temp_node_id: string;
  to_temp_node_id: string;
  edge_namespace: string;
  edge_type: string;
  properties: Record<string, unknown>;
  weight?: number;
}

export interface TemporaryReasoningGraph {
  temp_graph_id: string;
  reasoning_id: string;
  graph_scope: string;
  source_graphs: string[];
  nodes: TempGraphNode[];
  edges: TempGraphEdge[];
  created_at: string;
}
