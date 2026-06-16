import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ArrowRight, Plus, Search, X } from "lucide-react";
import { GraphEdge, IndustrialFlowEdgeQuickCreate, IndustrialFlowType, IndustrialNode } from "@/types";
import { listNodes, quickCreateEdge } from "@/services/api";

interface QuickEdgeFormProps {
  anchorNode: IndustrialNode;
  direction: "upstream" | "downstream";
  onSuccess?: (edge: GraphEdge) => void;
  onCancel?: () => void;
}

const EDGE_TYPES: { value: IndustrialFlowType; label: string }[] = [
  { value: "material_flow", label: "物料流" },
  { value: "composition", label: "组成/构成" },
  { value: "energy_flow", label: "能量流" },
  { value: "information_flow", label: "信息流" },
  { value: "capability_supply", label: "能力供给" },
  { value: "service_flow", label: "服务流" },
];

export function QuickEdgeForm({
  anchorNode,
  direction,
  onSuccess,
  onCancel,
}: QuickEdgeFormProps) {
  const queryClient = useQueryClient();
  const [query, setQuery] = useState("");
  const [selectedNode, setSelectedNode] = useState<IndustrialNode | null>(null);
  const [edgeType, setEdgeType] = useState<IndustrialFlowType>("material_flow");
  const [description, setDescription] = useState("");
  const [notes, setNotes] = useState("");
  const [error, setError] = useState<string | null>(null);

  const isUpstream = direction === "upstream";
  const fromNode = isUpstream ? selectedNode : anchorNode;
  const toNode = isUpstream ? anchorNode : selectedNode;

  const { data: searchData } = useQuery({
    queryKey: ["nodes", 1, 10, undefined, undefined, query],
    queryFn: () => listNodes(1, 10, undefined, undefined, query),
    enabled: query.length >= 1,
  });

  const mutation = useMutation({
    mutationFn: async () => {
      if (!selectedNode) throw new Error("请选择另一个节点");
      const payload: IndustrialFlowEdgeQuickCreate = {
        from_node: fromNode!.node_id,
        to_node: toNode!.node_id,
        edge_type: edgeType,
        description: description.trim() || undefined,
        notes: notes.trim() || undefined,
      };
      return quickCreateEdge(payload);
    },
    onSuccess: (edge) => {
      queryClient.invalidateQueries({ queryKey: ["edges-outgoing", anchorNode.node_id] });
      queryClient.invalidateQueries({ queryKey: ["edges-incoming", anchorNode.node_id] });
      queryClient.invalidateQueries({ queryKey: ["stats"] });
      setSelectedNode(null);
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
    if (!selectedNode) {
      setError("请选择另一个节点");
      return;
    }
    mutation.mutate();
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-2 rounded border border-dashed border-cyan-700/50 bg-cyan-900/10 p-2.5">
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
          {isUpstream ? (selectedNode?.canonical_name_zh || "上游节点") : anchorNode.canonical_name_zh}
        </span>
        <ArrowRight className="h-3 w-3 shrink-0 text-cyan-500" />
        <span className="truncate rounded bg-slate-800 px-1.5 py-0.5">
          {isUpstream ? anchorNode.canonical_name_zh : (selectedNode?.canonical_name_zh || "下游节点")}
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
            if (selectedNode) setSelectedNode(null);
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
                .filter((n) => n.node_id !== anchorNode.node_id)
                .map((node) => (
                  <button
                    key={node.node_id}
                    type="button"
                    onClick={() => {
                      setSelectedNode(node);
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
      <div className="flex gap-2">
        <select
          value={edgeType}
          onChange={(e) => setEdgeType(e.target.value as IndustrialFlowType)}
          className="flex-1 rounded border border-slate-700 bg-slate-800 px-2 py-1 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
        >
          {EDGE_TYPES.map((t) => (
            <option key={t.value} value={t.value}>
              {t.label}
            </option>
          ))}
        </select>
      </div>

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

      <button
        type="submit"
        disabled={mutation.isPending || !selectedNode}
        className="flex w-full items-center justify-center gap-1 rounded bg-cyan-600/80 py-1 text-xs font-medium text-white hover:bg-cyan-500 disabled:opacity-50"
      >
        <Plus className="h-3 w-3" />
        {mutation.isPending ? "创建中..." : `创建${isUpstream ? "上游" : "下游"}关系`}
      </button>

      <p className="text-[9px] text-slate-500">
        关系方向：{isUpstream ? "上游节点 → 当前节点" : "当前节点 → 下游节点"}。系统会自动生成 edge_id 和默认描述，后续可补全证据与精修描述。
      </p>
    </form>
  );
}
