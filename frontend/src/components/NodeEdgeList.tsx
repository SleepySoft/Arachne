import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Edit2, Trash2, Plus, ArrowUp, ArrowDown } from "lucide-react";
import { GraphEdge } from "@/types";
import { listEdges, deleteEdge } from "@/services/api";
import { EdgeForm } from "./EdgeForm";

interface NodeEdgeListProps {
  nodeId: string;
  onRefreshGraph: () => void;
}

export function NodeEdgeList({ nodeId, onRefreshGraph }: NodeEdgeListProps) {
  const queryClient = useQueryClient();
  const [editingEdge, setEditingEdge] = useState<GraphEdge | null>(null);
  const [creatingEdge, setCreatingEdge] = useState<"outgoing" | "incoming" | null>(null);

  const { data: outgoingData } = useQuery({
    queryKey: ["edges-outgoing", nodeId],
    queryFn: () => listEdges(1, 100, undefined, undefined, nodeId, undefined),
  });

  const { data: incomingData } = useQuery({
    queryKey: ["edges-incoming", nodeId],
    queryFn: () => listEdges(1, 100, undefined, undefined, undefined, nodeId),
  });

  const deleteMutation = useMutation({
    mutationFn: deleteEdge,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["edges-outgoing", nodeId] });
      queryClient.invalidateQueries({ queryKey: ["edges-incoming", nodeId] });
      onRefreshGraph();
    },
  });

  const outgoingEdges = outgoingData?.items || [];
  const incomingEdges = incomingData?.items || [];

  const renderEdgeItem = (edge: GraphEdge, direction: "outgoing" | "incoming") => {
    const otherNode = direction === "outgoing" ? edge.to_node : edge.from_node;
    const isIndustrial = edge.edge_namespace === "industrial_flow";
    return (
      <div
        key={edge.edge_id}
        className="flex items-center gap-2 rounded border border-slate-800 bg-slate-800/30 px-2 py-1.5"
      >
        {direction === "outgoing" ? (
          <ArrowDown className="h-3 w-3 shrink-0 text-emerald-400" />
        ) : (
          <ArrowUp className="h-3 w-3 shrink-0 text-amber-400" />
        )}
        <div className="min-w-0 flex-1">
          <div className="truncate text-xs text-slate-200">
            {direction === "outgoing" ? (
              <>
                <span className="text-slate-400">→</span> {otherNode}
              </>
            ) : (
              <>
                {otherNode} <span className="text-slate-400">→</span>
              </>
            )}
          </div>
          <div className="flex items-center gap-1.5">
            <span className="text-[10px] text-slate-500">
              {edge.edge_type_label || edge.edge_type}
            </span>
            {isIndustrial && (
              <span className="text-[10px] text-slate-600">{edge.confidence}</span>
            )}
          </div>
        </div>
        <div className="flex items-center gap-0.5">
          <button
            onClick={() => setEditingEdge(edge)}
            className="flex h-6 w-6 items-center justify-center rounded text-slate-500 hover:bg-slate-700 hover:text-cyan-400"
            title="编辑"
          >
            <Edit2 className="h-3 w-3" />
          </button>
          <button
            onClick={() => {
              if (confirm(`确定删除关系 ${edge.edge_id}？`)) deleteMutation.mutate(edge.edge_id);
            }}
            className="flex h-6 w-6 items-center justify-center rounded text-slate-500 hover:bg-slate-700 hover:text-red-400"
            title="删除"
          >
            <Trash2 className="h-3 w-3" />
          </button>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-3">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h4 className="text-xs font-semibold text-slate-300">关联关系</h4>
        <div className="flex items-center gap-1">
          <button
            onClick={() => setCreatingEdge("outgoing")}
            className="flex items-center gap-1 rounded bg-slate-800 px-1.5 py-0.5 text-[10px] text-slate-400 hover:bg-slate-700 hover:text-cyan-400"
            title="添加下游关系"
          >
            <Plus className="h-3 w-3" />
            下游
          </button>
          <button
            onClick={() => setCreatingEdge("incoming")}
            className="flex items-center gap-1 rounded bg-slate-800 px-1.5 py-0.5 text-[10px] text-slate-400 hover:bg-slate-700 hover:text-cyan-400"
            title="添加上游关系"
          >
            <Plus className="h-3 w-3" />
            上游
          </button>
        </div>
      </div>

      {/* Outgoing */}
      {outgoingEdges.length > 0 && (
        <div className="space-y-1">
          <div className="text-[10px] font-medium uppercase tracking-wider text-slate-500">
            下游 ({outgoingEdges.length})
          </div>
          {outgoingEdges.map((e) => renderEdgeItem(e, "outgoing"))}
        </div>
      )}

      {/* Incoming */}
      {incomingEdges.length > 0 && (
        <div className="space-y-1">
          <div className="text-[10px] font-medium uppercase tracking-wider text-slate-500">
            上游 ({incomingEdges.length})
          </div>
          {incomingEdges.map((e) => renderEdgeItem(e, "incoming"))}
        </div>
      )}

      {outgoingEdges.length === 0 && incomingEdges.length === 0 && (
        <div className="py-2 text-center text-[10px] text-slate-600">暂无关系</div>
      )}

      {/* Edit Modal */}
      {editingEdge && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm">
          <div className="w-full max-w-md rounded-lg border border-slate-700 bg-slate-900 shadow-2xl">
            <EdgeForm
              mode="edit"
              edge={editingEdge}
              onClose={() => setEditingEdge(null)}
              onSuccess={() => {
                setEditingEdge(null);
                queryClient.invalidateQueries({ queryKey: ["edges-outgoing", nodeId] });
                queryClient.invalidateQueries({ queryKey: ["edges-incoming", nodeId] });
                onRefreshGraph();
              }}
            />
          </div>
        </div>
      )}

      {/* Create Modal */}
      {creatingEdge && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm">
          <div className="w-full max-w-md rounded-lg border border-slate-700 bg-slate-900 shadow-2xl">
            <EdgeForm
              mode="create"
              defaultFromNode={creatingEdge === "outgoing" ? nodeId : undefined}
              defaultToNode={creatingEdge === "incoming" ? nodeId : undefined}
              onClose={() => setCreatingEdge(null)}
              onSuccess={() => {
                setCreatingEdge(null);
                queryClient.invalidateQueries({ queryKey: ["edges-outgoing", nodeId] });
                queryClient.invalidateQueries({ queryKey: ["edges-incoming", nodeId] });
                onRefreshGraph();
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}
