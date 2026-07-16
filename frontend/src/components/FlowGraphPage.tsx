import { useMemo, useRef, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { GitBranch, Layers } from "lucide-react";

import { GraphCanvas, GraphCanvasRef } from "@/components/GraphCanvas";
import { getFlowSubgraph, listFlows } from "@/services/api";
import {
  ArachneFlowEdge,
  Confidence,
  EntityType,
  FlowSummary,
  GraphEdge,
  GraphNode,
  IndustrialNode,
  NodeStatus,
} from "@/types";

function adaptFlowNode(node: GraphNode): IndustrialNode {
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
    canonical_name_en: node.canonical_name_en ?? (props.canonical_name_en as string | undefined) ?? undefined,
    aliases,
    definition: node.definition ?? (props.definition as string | undefined) ?? "",
    entity_type: node.entity_type as EntityType,
    evidence: [],
    confidence: (node.confidence ?? (props.confidence as string | undefined) ?? "LOW") as Confidence,
    status: (node.status ?? (props.status as string | undefined) ?? "PENDING") as NodeStatus,
    notes: node.notes ?? (props.notes as string | undefined) ?? undefined,
    created_at: node.created_at ?? undefined,
    updated_at: node.updated_at ?? undefined,
  };
}

function adaptFlowEdge(edge: GraphEdge): GraphEdge {
  const e = edge as ArachneFlowEdge;
  return {
    edge_uuid: e.edge_uuid ?? "",
    edge_id: e.edge_id,
    from_node: e.from_node,
    to_node: e.to_node,
    description: e.description ?? "",
    evidence: [],
    confidence: (e.confidence ?? "LOW") as Confidence,
    notes: e.notes ?? undefined,
    created_at: e.created_at ?? undefined,
    updated_at: e.updated_at ?? undefined,
    edge_namespace: "arachne_flow",
    edge_type: e.edge_type,
  } as GraphEdge;
}

export function FlowGraphPage() {
  const canvasRef = useRef<GraphCanvasRef>(null);
  const [selectedFlowId, setSelectedFlowId] = useState<string | null>(null);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

  const { data: flows = [] } = useQuery({
    queryKey: ["flows"],
    queryFn: listFlows,
  });

  const { data: subgraph, isLoading } = useQuery({
    queryKey: ["flow-subgraph", selectedFlowId],
    queryFn: () => getFlowSubgraph(selectedFlowId!, 3),
    enabled: !!selectedFlowId,
  });

  const selectedNode = useMemo(() => {
    if (!subgraph || !selectedNodeId) return null;
    return subgraph.nodes.find((n) => n.node_id === selectedNodeId) || null;
  }, [subgraph, selectedNodeId]);

  const adaptedData = useMemo(() => {
    if (!subgraph) return undefined;
    return {
      nodes: subgraph.nodes.map(adaptFlowNode),
      edges: subgraph.edges.map(adaptFlowEdge),
    };
  }, [subgraph]);

  const filters = {
    edgeNamespaces: ["arachne_flow"],
    edgeTypes: ["feedstock", "tool", "component", "subject", "primary_result", "intermediate", "ref", "next"],
    entityTypes: ["arachne_flow:resource", "arachne_flow:action", "arachne_flow:method"],
    status: ["ACTIVE", "PENDING", "REJECTED"],
    confidence: ["HIGH", "MEDIUM", "LOW"],
    showIsA: false,
    showPartOf: false,
    showWeakOntology: false,
    showDerivedFrom: false,
  };

  return (
    <div className="flex h-full w-full overflow-hidden">
      {/* Sidebar */}
      <div className="w-64 flex-shrink-0 border-r border-slate-700 bg-slate-900/95 flex flex-col">
        <div className="p-3 border-b border-slate-700 flex items-center gap-2 text-slate-100 font-medium">
          <Layers className="h-4 w-4 text-emerald-400" />
          <span>Arachne Flow</span>
        </div>
        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {flows.map((flow) => (
            <FlowListItem
              key={flow.flow_id}
              flow={flow}
              active={flow.flow_id === selectedFlowId}
              onClick={() => {
                setSelectedFlowId(flow.flow_id);
                setSelectedNodeId(null);
              }}
            />
          ))}
        </div>
        <div className="p-3 border-t border-slate-700 text-xs text-slate-400">
          共 {flows.length} 个流程文件
        </div>
      </div>

      {/* Canvas */}
      <div className="flex-1 relative bg-slate-950">
        {!selectedFlowId && <EmptyState />}
        {selectedFlowId && isLoading && <LoadingState />}
        {adaptedData && (
          <GraphCanvas
            ref={canvasRef}
            sourceData={adaptedData}
            filters={filters}
            onNodeClick={(node) => setSelectedNodeId(node.node_id)}
            onEdgeClick={() => {}}
            onClearSelection={() => setSelectedNodeId(null)}
            onBeforeDragStart={() => {}}
            onBeforeManualLayout={() => {}}
            onBeforeCameraChange={() => {}}
          />
        )}

        {/* Detail panel */}
        {selectedNode && (
          <div className="absolute right-4 top-4 w-72 rounded-lg border border-slate-700 bg-slate-900/95 p-4 shadow-lg">
            <h3 className="text-sm font-semibold text-slate-100 mb-2">节点详情</h3>
            <FlowNodeDetail node={selectedNode} />
          </div>
        )}
      </div>
    </div>
  );
}

function FlowListItem({
  flow,
  active,
  onClick,
}: {
  flow: FlowSummary;
  active: boolean;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className={`w-full text-left px-3 py-2 rounded-md text-sm transition-colors ${
        active
          ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
          : "text-slate-300 hover:bg-slate-800"
      }`}
    >
      <div className="font-medium truncate">{flow.root_product}</div>
      <div className="text-xs text-slate-500 mt-0.5 flex items-center gap-2">
        <GitBranch className="h-3 w-3" />
        {flow.triples} triples
      </div>
    </button>
  );
}

function EmptyState() {
  return (
    <div className="absolute inset-0 flex items-center justify-center text-slate-500">
      <div className="text-center">
        <Layers className="h-10 w-10 mx-auto mb-3 opacity-50" />
        <p>在左侧选择一个流程文件以加载</p>
      </div>
    </div>
  );
}

function LoadingState() {
  return (
    <div className="absolute inset-0 flex items-center justify-center text-slate-400">
      <div className="animate-pulse">加载流程子图...</div>
    </div>
  );
}

function FlowNodeDetail({ node }: { node: GraphNode }) {
  const kind = node.entity_type.replace("arachne_flow:", "");
  const props = (node.properties || {}) as Record<string, any>;
  return (
    <div className="space-y-2 text-sm">
      <div className="flex items-center gap-2">
        <span className="text-xs px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 uppercase">{kind}</span>
      </div>
      <div>
        <span className="text-slate-500">ID:</span>
        <span className="ml-2 text-slate-200 break-all">{node.node_id}</span>
      </div>
      <div>
        <span className="text-slate-500">名称:</span>
        <span className="ml-2 text-slate-200">{node.label}</span>
      </div>
      {props.method_ref && (
        <div>
          <span className="text-slate-500">引用方法:</span>
          <span className="ml-2 text-slate-200">{String(props.method_ref)}</span>
        </div>
      )}
      {props.resource_type && (
        <div>
          <span className="text-slate-500">资源类型:</span>
          <span className="ml-2 text-slate-200">{String(props.resource_type)}</span>
        </div>
      )}
    </div>
  );
}
