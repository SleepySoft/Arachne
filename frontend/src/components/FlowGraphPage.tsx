import { useMemo, useRef, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { GitBranch, Layers, RotateCcw, Eye } from "lucide-react";

import { GraphCanvas, GraphCanvasRef } from "@/components/GraphCanvas";
import { Layout } from "@/components/Layout";
import {
  compileFlows,
  getFlowsSubgraph,
  listFlows,
} from "@/services/api";
import {
  ARACHNE_FLOW_ACTION_TYPE_LABELS,
  ARACHNE_FLOW_NODE_TYPE_LABELS,
  ARACHNE_FLOW_PREDICATES,
  ARACHNE_FLOW_RESOURCE_TYPE_LABELS,
  ArachneFlowEdge,
  Confidence,
  EDGE_TYPE_LABELS,
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
    edge_type_label: EDGE_TYPE_LABELS[e.edge_type] ?? e.edge_type,
  } as GraphEdge;
}

export function FlowGraphPage() {
  const canvasRef = useRef<GraphCanvasRef>(null);
  const queryClient = useQueryClient();
  const [selectedFlowIds, setSelectedFlowIds] = useState<string[]>([]);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [subgraphQueryKey, setSubgraphQueryKey] = useState<string>("");
  const [canvasVersion, setCanvasVersion] = useState(0);

  const { data: flows = [] } = useQuery({
    queryKey: ["flows"],
    queryFn: listFlows,
  });

  const { data: subgraph, isLoading } = useQuery({
    queryKey: ["flows-subgraph", subgraphQueryKey],
    queryFn: () => getFlowsSubgraph(selectedFlowIds, 3),
    enabled: selectedFlowIds.length > 0 && subgraphQueryKey !== "",
  });

  const compileMutation = useMutation({
    mutationFn: compileFlows,
    onSuccess: () => {
      // Refresh flow compile status, force the current subgraph to refetch,
      // and bump the canvas key so it re-renders even if the selection key is unchanged.
      queryClient.invalidateQueries({ queryKey: ["flows"] });
      queryClient.invalidateQueries({ queryKey: ["flows-subgraph"] });
      setCanvasVersion((v) => v + 1);
    },
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

  const toggleFlow = (flowId: string) => {
    setSelectedFlowIds((prev) =>
      prev.includes(flowId) ? prev.filter((id) => id !== flowId) : [...prev, flowId]
    );
  };

  const viewSelected = () => {
    if (selectedFlowIds.length === 0) return;
    setSelectedNodeId(null);
    setSubgraphQueryKey(selectedFlowIds.join(","));
    // Force GraphCanvas remount so a new selection always reloads the canvas.
    setCanvasVersion((v) => v + 1);
  };

  const recompileSelected = () => {
    if (selectedFlowIds.length === 0) return;
    compileMutation.mutate(selectedFlowIds);
  };

  const filters = {
    edgeNamespaces: ["arachne_flow"],
    edgeTypes: ARACHNE_FLOW_PREDICATES,
    entityTypes: ["arachne_flow:resource", "arachne_flow:action", "arachne_flow:method"],
    status: ["ACTIVE", "PENDING", "REJECTED"],
    confidence: ["HIGH", "MEDIUM", "LOW"],
    showIsA: false,
    showPartOf: false,
    showWeakOntology: false,
    showDerivedFrom: false,
  };

  const leftSidebar = (
    <div className="flex flex-col h-full">
      <div className="p-3 border-b border-slate-800 flex items-center gap-2 text-slate-100 font-medium">
        <Layers className="h-4 w-4 text-emerald-400" />
        <span>Arachne Flow</span>
      </div>
      <div className="flex-1 overflow-y-auto p-2 space-y-1">
        {flows.map((flow) => (
          <FlowListItem
            key={flow.flow_id}
            flow={flow}
            checked={selectedFlowIds.includes(flow.flow_id)}
            onToggle={() => toggleFlow(flow.flow_id)}
          />
        ))}
      </div>
      <div className="p-3 border-t border-slate-800 space-y-2">
        <button
          onClick={viewSelected}
          disabled={selectedFlowIds.length === 0 || isLoading}
          className="w-full flex items-center justify-center gap-1.5 px-3 py-2 rounded-md bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-700 disabled:text-slate-400 text-white text-sm transition-colors"
        >
          <Eye className="h-3.5 w-3.5" />
          查看子图 {selectedFlowIds.length > 0 && `(${selectedFlowIds.length})`}
        </button>
        <button
          onClick={recompileSelected}
          disabled={selectedFlowIds.length === 0 || compileMutation.isPending}
          className="w-full flex items-center justify-center gap-1.5 px-3 py-2 rounded-md bg-slate-700 hover:bg-slate-600 disabled:bg-slate-800 disabled:text-slate-500 text-slate-100 text-sm transition-colors"
        >
          <RotateCcw className="h-3.5 w-3.5" />
          重新编译 {selectedFlowIds.length > 0 && `(${selectedFlowIds.length})`}
        </button>
        {compileMutation.isPending && (
          <div className="text-xs text-slate-400">编译中...</div>
        )}
        {compileMutation.isSuccess && (
          <div className="text-xs text-emerald-400">编译完成，已刷新</div>
        )}
        {compileMutation.error && (
          <div className="text-xs text-red-400">编译失败</div>
        )}
      </div>
      <div className="p-3 border-t border-slate-800 text-xs text-slate-500">
        共 {flows.length} 个流程文件
      </div>
    </div>
  );

  const searchPanel = (
    <div className="flex items-center justify-between text-sm text-slate-300">
      <span>
        引擎: <span className="text-emerald-400 font-medium">arachne_flow</span>
      </span>
      <span className="text-slate-500">
        {subgraph ? `${subgraph.nodes.length} 节点 / ${subgraph.edges.length} 边` : "未加载"}
      </span>
    </div>
  );

  const centerCanvas = (
    <>
      {selectedFlowIds.length === 0 && <EmptyState />}
      {selectedFlowIds.length > 0 && isLoading && <LoadingState />}
      {adaptedData && (
        <GraphCanvas
          key={`${subgraphQueryKey}-${canvasVersion}`}
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
    </>
  );

  const rightPanel = selectedNode ? (
    <div className="p-4">
      <h3 className="text-sm font-semibold text-slate-100 mb-3">节点详情</h3>
      <FlowNodeDetail node={selectedNode} />
    </div>
  ) : (
    <div className="p-4 text-sm text-slate-500">
      <p>点击画布上的节点查看详情。</p>
      <p className="mt-2">左侧可多选流程文件，然后“查看子图”合并渲染；修改 YAML 后可用“重新编译”。</p>
    </div>
  );

  return (
    <Layout
      leftSidebar={leftSidebar}
      searchPanel={searchPanel}
      centerCanvas={centerCanvas}
      rightPanel={rightPanel}
    />
  );
}

function FlowListItem({
  flow,
  checked,
  onToggle,
}: {
  flow: FlowSummary;
  checked: boolean;
  onToggle: () => void;
}) {
  return (
    <label
      className={`flex items-start gap-2 px-3 py-2 rounded-md text-sm cursor-pointer transition-colors ${
        checked
          ? "bg-emerald-500/15 text-emerald-300 border border-emerald-500/30"
          : "text-slate-300 hover:bg-slate-800"
      }`}
    >
      <input
        type="checkbox"
        className="mt-0.5 accent-emerald-500"
        checked={checked}
        onChange={onToggle}
      />
      <div className="flex-1 min-w-0">
        <div className="font-medium truncate">{flow.root_product}</div>
        <div className="text-xs text-slate-500 mt-0.5 flex items-center gap-2">
          <GitBranch className="h-3 w-3" />
          {flow.triples} triples
          {flow.status && (
            <span
              className={`px-1 rounded ${
                flow.status === "COMPILED" ? "bg-emerald-500/20 text-emerald-400" : "bg-slate-700 text-slate-400"
              }`}
            >
              {flow.status}
            </span>
          )}
        </div>
      </div>
    </label>
  );
}

function EmptyState() {
  return (
    <div className="absolute inset-0 flex items-center justify-center text-slate-500">
      <div className="text-center">
        <Layers className="h-10 w-10 mx-auto mb-3 opacity-50" />
        <p>在左侧选择一个或多个流程文件以加载子图</p>
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
  const kindLabel = ARACHNE_FLOW_NODE_TYPE_LABELS[kind] ?? kind;
  const props = (node.properties || {}) as Record<string, any>;
  const resourceType = props.resource_type ? String(props.resource_type) : undefined;
  const actionType = props.action_type ? String(props.action_type) : undefined;
  return (
    <div className="space-y-2 text-sm">
      <div className="flex items-center gap-2">
        <span className="text-xs px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">{kindLabel}</span>
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
      {resourceType && (
        <div>
          <span className="text-slate-500">资源类型:</span>
          <span className="ml-2 text-slate-200">
            {ARACHNE_FLOW_RESOURCE_TYPE_LABELS[resourceType] ?? resourceType}
          </span>
        </div>
      )}
      {actionType && (
        <div>
          <span className="text-slate-500">动作类型:</span>
          <span className="ml-2 text-slate-200">
            {ARACHNE_FLOW_ACTION_TYPE_LABELS[actionType] ?? actionType}
          </span>
        </div>
      )}
      <div>
        <span className="text-slate-500">类型标识:</span>
        <span className="ml-2 text-slate-400 break-all">{node.entity_type}</span>
      </div>
    </div>
  );
}
