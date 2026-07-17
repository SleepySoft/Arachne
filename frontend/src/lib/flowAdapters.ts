import {
  ArachneFlowEdge,
  Confidence,
  EDGE_TYPE_LABELS,
  EntityType,
  GraphEdge,
  GraphNode,
  IndustrialNode,
  NodeStatus,
} from "@/types";

/**
 * 将 arachne_flow 引擎返回的 GraphNode 适配为画布/面板使用的 IndustrialNode 形状。
 * 引擎未记录的字段使用展示默认值（编译产物视为 ACTIVE，置信度 MEDIUM）。
 */
export function adaptFlowNode(node: GraphNode): IndustrialNode {
  const props = (node.properties || {}) as Record<string, any>;
  const aliases = Array.isArray(props.aliases)
    ? (props.aliases as string[])
    : props.aliases
    ? [String(props.aliases)]
    : [];
  return {
    node_uuid: node.node_uuid ?? "",
    node_id: node.node_id,
    canonical_name_zh: node.label || String(props.canonical_name_zh || node.node_id),
    canonical_name_en:
      node.canonical_name_en ?? (props.canonical_name_en as string | undefined) ?? undefined,
    aliases,
    definition: node.definition ?? (props.definition as string | undefined) ?? "",
    entity_type: node.entity_type as EntityType,
    evidence: [],
    confidence: (node.confidence ??
      (props.confidence as string | undefined) ??
      "MEDIUM") as Confidence,
    status: (node.status ?? (props.status as string | undefined) ?? "ACTIVE") as NodeStatus,
    notes: node.notes ?? (props.notes as string | undefined) ?? undefined,
    created_at: node.created_at ?? undefined,
    updated_at: node.updated_at ?? undefined,
    properties: props,
  };
}

/** 将 arachne_flow 引擎返回的 GraphEdge 适配为画布/面板使用的 GraphEdge 形状。 */
export function adaptFlowEdge(edge: GraphEdge): GraphEdge {
  const e = edge as ArachneFlowEdge;
  const props = (e as unknown as { properties?: Record<string, any> }).properties ?? {};
  const baseLabel = EDGE_TYPE_LABELS[e.edge_type] ?? e.edge_type;
  // 合并视图中聚合边（count>1）在标签上体现数量
  const count = typeof props.count === "number" ? props.count : 0;
  const label = count > 1 ? `${baseLabel} ×${count}` : baseLabel;
  return {
    edge_uuid: e.edge_uuid ?? "",
    edge_id: e.edge_id,
    from_node: e.from_node,
    to_node: e.to_node,
    description: e.description ?? "",
    evidence: [],
    confidence: (e.confidence ?? "MEDIUM") as Confidence,
    notes: e.notes ?? undefined,
    created_at: e.created_at ?? undefined,
    updated_at: e.updated_at ?? undefined,
    edge_namespace: "arachne_flow",
    edge_type: e.edge_type,
    edge_type_label: label,
    properties: props,
  } as GraphEdge;
}
