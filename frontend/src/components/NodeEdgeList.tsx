import { useMemo, useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Edit2, Trash2, Plus, ArrowUp, ArrowDown } from "lucide-react";
import { GraphEdge, IndustrialNode } from "@/types";
import { listEdges, deleteEdge, listNodes, getNode } from "@/services/api";
import { EdgeForm } from "./EdgeForm";
import { QuickEdgeForm } from "./QuickEdgeForm";

interface NodeEdgeListProps {
  nodeId: string;
  onEdgeCreated?: (edge: GraphEdge) => void;
  onEdgeUpdated?: (edge: GraphEdge) => void;
  onEdgeDeleted?: (edgeId: string) => void;
  onSelectNode?: (node: IndustrialNode) => void;
}

export function NodeEdgeList({
  nodeId,
  onEdgeCreated,
  onEdgeUpdated,
  onEdgeDeleted,
  onSelectNode,
}: NodeEdgeListProps) {
  const queryClient = useQueryClient();
  const [editingEdge, setEditingEdge] = useState<GraphEdge | null>(null);
  const [creatingDirection, setCreatingDirection] = useState<"outgoing" | "incoming" | null>(null);
  const [quickDraft, setQuickDraft] = useState<{
      from_node: string;
      to_node: string;
      edge_type: string;
      description?: string;
      notes?: string;
    } | null>(null);

    const { data: outgoingData } = useQuery({
      queryKey: ["edges-outgoing", nodeId],
      queryFn: () => listEdges(1, 100, undefined, undefined, nodeId, undefined),
    });

    const { data: incomingData } = useQuery({
      queryKey: ["edges-incoming", nodeId],
      queryFn: () => listEdges(1, 100, undefined, undefined, undefined, nodeId),
    });

    const { data: nodesData } = useQuery({
      queryKey: ["all-nodes-for-edge-list"],
      queryFn: () => listNodes(1, 1000),
      staleTime: 60_000,
    });

    const nodeMap = useMemo(() => {
      const map: Record<string, IndustrialNode> = {};
      nodesData?.items.forEach((n) => {
        map[n.node_id] = n;
      });
      return map;
    }, [nodesData]);

    const deleteMutation = useMutation({
      mutationFn: deleteEdge,
      onSuccess: (_, edgeId) => {
        queryClient.invalidateQueries({ queryKey: ["edges-outgoing", nodeId] });
        queryClient.invalidateQueries({ queryKey: ["edges-incoming", nodeId] });
        queryClient.invalidateQueries({ queryKey: ["stats"] });
        onEdgeDeleted?.(edgeId);
      },
    });

    const outgoingEdges = outgoingData?.items || [];
    const incomingEdges = incomingData?.items || [];

    const handleSuccess = (edge: GraphEdge, mode: "create" | "update") => {
      queryClient.invalidateQueries({ queryKey: ["edges-outgoing", nodeId] });
      queryClient.invalidateQueries({ queryKey: ["edges-incoming", nodeId] });
      queryClient.invalidateQueries({ queryKey: ["stats"] });
      setEditingEdge(null);
      setCreatingDirection(null);
      setQuickDraft(null);
      if (mode === "create") {
        onEdgeCreated?.(edge);
      } else {
        onEdgeUpdated?.(edge);
      }
    };

    const handleNodeClick = async (otherNodeId: string) => {
      if (!onSelectNode) return;
      const cached = nodeMap[otherNodeId];
      if (cached) {
        onSelectNode(cached);
        return;
      }
      try {
        const fetched = await getNode(otherNodeId);
        onSelectNode(fetched);
      } catch {
        // ignore fetch errors
      }
    };

    const renderEdgeItem = (edge: GraphEdge, direction: "outgoing" | "incoming") => {
      const otherNodeId = direction === "outgoing" ? edge.to_node : edge.from_node;
      const otherNode = nodeMap[otherNodeId];
      const displayName = otherNode?.canonical_name_zh || otherNodeId;
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
                  <span className="text-slate-400">→</span>{" "}
                  <button
                    onClick={() => handleNodeClick(otherNodeId)}
                    className="text-cyan-400 hover:underline"
                    title={otherNodeId}
                  >
                    {displayName}
                  </button>
                </>
              ) : (
                <>
                  <button
                    onClick={() => handleNodeClick(otherNodeId)}
                    className="text-cyan-400 hover:underline"
                    title={otherNodeId}
                  >
                    {displayName}
                  </button>{" "}
                  <span className="text-slate-400">→</span>
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

    const isAdding = creatingDirection !== null;

    return (
      <div className="space-y-3">
        {/* Header */}
        <div className="flex items-center justify-between">
          <h4 className="text-xs font-semibold text-slate-300">关联关系</h4>
          <div className="flex items-center gap-1">
            {!isAdding && (
              <>
                <button
                  onClick={() => setCreatingDirection("incoming")}
                  className="flex items-center gap-1 rounded bg-slate-800 px-1.5 py-0.5 text-[10px] text-slate-400 hover:bg-slate-700 hover:text-cyan-400"
                  title="添加上游关系"
                >
                  <Plus className="h-3 w-3" />
                  上游
                </button>
                <button
                  onClick={() => setCreatingDirection("outgoing")}
                  className="flex items-center gap-1 rounded bg-slate-800 px-1.5 py-0.5 text-[10px] text-slate-400 hover:bg-slate-700 hover:text-cyan-400"
                  title="添加下游关系"
                >
                  <Plus className="h-3 w-3" />
                  下游
                </button>
              </>
            )}
          </div>
        </div>

        {/* Quick add form */}
        {creatingDirection && (
          <QuickEdgeForm
            anchorNodeId={nodeId}
            direction={creatingDirection === "outgoing" ? "downstream" : "upstream"}
            onSuccess={(edge) => handleSuccess(edge, "create")}
            onCancel={() => {
              setCreatingDirection(null);
              setQuickDraft(null);
            }}
            onExpand={(draft) => {
              setQuickDraft(draft);
            }}
          />
        )}

        {/* Incoming — 上游放上面 */}
        {incomingEdges.length > 0 && (
          <div className="space-y-1">
            <div className="text-[10px] font-medium uppercase tracking-wider text-slate-500">
              上游 ({incomingEdges.length})
            </div>
            {incomingEdges.map((e) => renderEdgeItem(e, "incoming"))}
          </div>
        )}

        {/* Outgoing — 下游放下边 */}
        {outgoingEdges.length > 0 && (
          <div className="space-y-1">
            <div className="text-[10px] font-medium uppercase tracking-wider text-slate-500">
              下游 ({outgoingEdges.length})
            </div>
            {outgoingEdges.map((e) => renderEdgeItem(e, "outgoing"))}
          </div>
        )}

        {outgoingEdges.length === 0 && incomingEdges.length === 0 && !isAdding && (
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
                onSuccess={(edge) => handleSuccess(edge, "update")}
              />
            </div>
          </div>
        )}

        {/* Full create modal (expanded from quick draft) */}
        {creatingDirection && quickDraft && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm">
            <div className="w-full max-w-md rounded-lg border border-slate-700 bg-slate-900 shadow-2xl">
              <EdgeForm
                mode="create"
                defaultFromNode={quickDraft.from_node}
                defaultToNode={quickDraft.to_node}
                prefillData={quickDraft}
                onClose={() => setQuickDraft(null)}
                onSuccess={(edge) => handleSuccess(edge, "create")}
              />
            </div>
          </div>
        )}
      </div>
    );
}
