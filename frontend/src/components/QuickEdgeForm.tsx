import { useEffect, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ArrowRight, Maximize2, Plus, Search, X } from "lucide-react";
import { GraphEdge, IndustrialFlowEdgeQuickCreate, IndustrialFlowType, IndustrialNode } from "@/types";
import { getNode, listNodes, quickCreateEdge } from "@/services/api";

interface QuickEdgeFormProps {
  anchorNodeId: string;
  direction: "upstream" | "downstream";
  initialTargetNodeId?: string;
  initialTargetNode?: IndustrialNode;
  onSuccess?: (edge: GraphEdge) => void;
  onCancel?: () => void;
  onExpand?: (draft: {
    from_node: string;
    to_node: string;
    edge_type: string;
    description?: string;
    notes?: string;
  }) => void;
}

const EDGE_TYPES: { value: IndustrialFlowType; label: string }[] = [
  { value: "material_input", label: "物料输入" },
  { value: "energy_input", label: "能量输入" },
  { value: "information_input", label: "信息输入" },
  { value: "equipment_enablement", label: "设备使能" },
  { value: "process_output", label: "工艺产出" },
  { value: "service_provision", label: "服务提供" },
  { value: "capability_enablement", label: "能力使能" },
  { value: "structural_composition", label: "结构组成" },
  { value: "supply_relation", label: "供应关系" },
  { value: "derived_from", label: "派生自" },
  { value: "unknown", label: "未知关系" },
];

export function QuickEdgeForm({
  anchorNodeId,
  direction,
  initialTargetNodeId,
  initialTargetNode,
  onSuccess,
  onCancel,
  onExpand,
}: QuickEdgeFormProps) {
  const queryClient = useQueryClient();
  const [query, setQuery] = useState("");
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(
    initialTargetNodeId || null
  );
  const [selectedNodeOverride, setSelectedNodeOverride] = useState<IndustrialNode | null>(
    initialTargetNode || null
  );
  const [edgeType, setEdgeType] = useState<IndustrialFlowType>("material_input");
  const [description, setDescription] = useState("");
  const [notes, setNotes] = useState("");
  const [error, setError] = useState<string | null>(null);

  const { data: anchorNode } = useQuery({
    queryKey: ["node", anchorNodeId],
    queryFn: () => getNode(anchorNodeId),
  });

  const { data: searchData } = useQuery({
    queryKey: ["nodes", 1, 10, undefined, undefined, query],
    queryFn: () => listNodes(1, 10, undefined, undefined, query),
    enabled: query.length >= 1,
  });

  const selectedNode =
    selectedNodeOverride ||
    searchData?.items.find((n) => n.node_id === selectedNodeId) ||
    null;

  useEffect(() => {
    if (initialTargetNodeId) setSelectedNodeId(initialTargetNodeId);
    if (initialTargetNode) setSelectedNodeOverride(initialTargetNode);
  }, [initialTargetNodeId, initialTargetNode]);

  const isUpstream = direction === "upstream";
  const fromNodeId = isUpstream ? selectedNodeId : anchorNodeId;
  const toNodeId = isUpstream ? anchorNodeId : selectedNodeId;
  const fromNodeName = isUpstream
    ? selectedNode?.canonical_name_zh
    : anchorNode?.canonical_name_zh;
  const toNodeName = isUpstream
    ? anchorNode?.canonical_name_zh
    : selectedNode?.canonical_name_zh;

  const mutation = useMutation({
    mutationFn: async () => {
      if (!fromNodeId || !toNodeId) throw new Error("请选择另一个节点");
      const payload: IndustrialFlowEdgeQuickCreate = {
        from_node: fromNodeId,
        to_node: toNodeId,
        edge_type: edgeType,
        description: description.trim() || undefined,
        notes: notes.trim() || undefined,
      };
      return quickCreateEdge(payload);
    },
    onSuccess: (edge) => {
      queryClient.invalidateQueries({ queryKey: ["edges-outgoing", anchorNodeId] });
      queryClient.invalidateQueries({ queryKey: ["edges-incoming", anchorNodeId] });
      queryClient.invalidateQueries({ queryKey: ["stats"] });
      setSelectedNodeId(null);
      setQuery("");
      setDescription("");
      setNotes("");
      setError(null);
      onSuccess?.(edge);
    },
    onError: (err: Error) => setError(err.message),
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!selectedNodeId) {
      setError("请选择另一个节点");
      return;
    }
    mutation.mutate();
  };

  const handleExpand = () => {
    if (!fromNodeId || !toNodeId) {
      setError("请选择另一个节点后再展开完整表单");
      return;
    }
    onExpand?.({
      from_node: fromNodeId,
      to_node: toNodeId,
      edge_type: edgeType,
      description: description.trim() || undefined,
      notes: notes.trim() || undefined,
    });
  };

  if (!anchorNode) {
    return (
      <div className="rounded border border-dashed border-cyan-700/50 bg-cyan-900/10 p-2.5 text-xs text-cyan-400">
        加载中...
      </div>
    );
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-2 rounded border border-dashed border-cyan-700/50 bg-cyan-900/10 p-2.5"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-1 text-[11px] font-medium text-cyan-400">
          <Plus className="h-3 w-3" />
          快速添加{isUpstream ? "上游" : "下游"}关系
        </div>
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="rounded p-0.5 text-slate-500 hover:bg-slate-800 hover:text-slate-300"
          >
            <X className="h-3 w-3" />
          </button>
        )}
      </div>

      {error && (
        <div className="rounded bg-red-900/30 px-2 py-1 text-[10px] text-red-300">{error}</div>
      )}

      {/* Direction visualization */}
      <div className="flex items-center gap-1 text-[10px] text-slate-400">
        <span className="truncate rounded bg-slate-800 px-1.5 py-0.5">
          {fromNodeName || (isUpstream ? "上游节点" : anchorNode.canonical_name_zh)}
        </span>
        <ArrowRight className="h-3 w-3 shrink-0 text-cyan-500" />
        <span className="truncate rounded bg-slate-800 px-1.5 py-0.5">
          {toNodeName || (isUpstream ? anchorNode.canonical_name_zh : "下游节点")}
        </span>
      </div>

      {/* Node search */}
      <div className="relative">
        <Search className="absolute left-2 top-1/2 h-3 w-3 -translate-y-1/2 text-slate-500" />
        <input
          type="text"
          value={selectedNode ? selectedNode.canonical_name_zh : query}
          onChange={(e) => {
            setQuery(e.target.value);
            if (selectedNodeId) setSelectedNodeId(null);
            if (selectedNodeOverride) setSelectedNodeOverride(null);
          }}
          placeholder={isUpstream ? "搜索上游节点（供应商）..." : "搜索下游节点（客户/应用）..."}
          className="w-full rounded border border-slate-700 bg-slate-800 py-1.5 pl-6 pr-2 text-xs text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
        />
        {searchData && query && !selectedNode && (
          <div className="absolute z-10 mt-1 max-h-32 w-full min-w-[240px] overflow-auto rounded border border-slate-700 bg-slate-800 shadow-lg">
            {searchData.items.length === 0 ? (
              <div className="px-2 py-1.5 text-xs text-slate-500">无结果</div>
            ) : (
              searchData.items
                .filter((n) => n.node_id !== anchorNodeId)
                .map((node) => (
                  <button
                    key={node.node_id}
                    type="button"
                    onClick={() => {
                      setSelectedNodeId(node.node_id);
                      setQuery("");
                    }}
                    className="flex w-full min-w-0 items-center gap-2 whitespace-nowrap px-2 py-1.5 text-left text-xs hover:bg-slate-700"
                  >
                    <span className="min-w-0 flex-1 truncate font-medium text-slate-200">
                      {node.canonical_name_zh || node.canonical_name_en}
                    </span>
                    <span className="shrink-0 text-[10px] text-slate-500">{node.node_id}</span>
                    <span className="shrink-0 rounded bg-slate-700 px-1 py-0 text-[9px] text-slate-400">
                      {node.entity_type}
                    </span>
                  </button>
                ))
            )}
          </div>
        )}
      </div>

      {/* Edge type */}
      <select
        value={edgeType}
        onChange={(e) => setEdgeType(e.target.value as IndustrialFlowType)}
        className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
      >
        {EDGE_TYPES.map((t) => (
          <option key={t.value} value={t.value}>
            {t.label}
          </option>
        ))}
      </select>

      {/* Description */}
      <input
        type="text"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder={isUpstream ? "描述上游如何为当前节点提供输入（可选）" : "描述当前节点如何为下游提供输入（可选）"}
        className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1 text-xs text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
      />

      {/* Notes */}
      <input
        type="text"
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
        placeholder="备注（可选）"
        className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1 text-xs text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
      />

      <div className="flex gap-2">
        <button
          type="submit"
          disabled={mutation.isPending || !selectedNodeId}
          className="flex flex-1 items-center justify-center gap-1 rounded bg-cyan-600/80 py-1 text-xs font-medium text-white hover:bg-cyan-500 disabled:opacity-50"
        >
          <Plus className="h-3 w-3" />
          {mutation.isPending ? "创建中..." : `创建${isUpstream ? "上游" : "下游"}关系`}
        </button>
        <button
          type="button"
          onClick={handleExpand}
          disabled={!selectedNodeId}
          title="展开完整表单（可填写 edge_id、证据等）"
          className="flex items-center justify-center gap-1 rounded border border-slate-600 bg-slate-800 px-2 py-1 text-xs text-slate-300 hover:border-cyan-600 hover:text-cyan-400 disabled:opacity-50"
        >
          <Maximize2 className="h-3 w-3" />
          完整
        </button>
      </div>
    </form>
  );
}
