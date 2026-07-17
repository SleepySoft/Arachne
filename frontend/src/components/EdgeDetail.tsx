import { useMutation, useQuery } from "@tanstack/react-query";
import { ArrowRight, Edit2, Trash2, X } from "lucide-react";
import { GraphEdge, IndustrialNode } from "@/types";
import { deleteEdge, getNode } from "@/services/api";

const FIELD_LABELS: Record<string, string> = {
  edge_id: "关系ID (edge_id)",
  namespace: "命名空间 (edge_namespace)",
  type: "类型 (edge_type)",
  from_node: "起点 (from_node)",
  to_node: "终点 (to_node)",
  confidence: "置信度 (confidence)",
  description: "描述 (description)",
  evidence: "证据 (evidence)",
  notes: "备注 (notes)",
};

const NAMESPACE_LABELS: Record<string, string> = {
  industrial_flow: "产业流",
  ontology: "本体",
  arachne_flow: "流程",
};

const CONFIDENCE_LABELS: Record<string, string> = {
  HIGH: "高",
  MEDIUM: "中",
  LOW: "低",
};

interface EdgeDetailProps {
  edge: GraphEdge;
  onEdit: () => void;
  onClose: () => void;
  onEdgeDeleted?: (edgeId: string) => void;
  onSelectNode?: (node: IndustrialNode) => void;
  /** 只读模式：隐藏编辑/删除按钮，用于只读引擎（如 arachne_flow）。 */
  readOnly?: boolean;
  /** 引擎名称；非 legacy 时通过 ?engine= 获取端点节点。 */
  engine?: string;
}

export function EdgeDetail({
  edge,
  onEdit,
  onClose,
  onEdgeDeleted,
  onSelectNode,
  readOnly = false,
  engine,
}: EdgeDetailProps) {
  const { data: fromNodeRaw } = useQuery({
    queryKey: ["node", engine ?? "legacy", edge.from_node],
    queryFn: () => getNode(edge.from_node, engine),
    enabled: !!edge.from_node,
  });
  const { data: toNodeRaw } = useQuery({
    queryKey: ["node", engine ?? "legacy", edge.to_node],
    queryFn: () => getNode(edge.to_node, engine),
    enabled: !!edge.to_node,
  });
  const fromNode = toEndpointNode(fromNodeRaw);
  const toNode = toEndpointNode(toNodeRaw);

  const deleteMutation = useMutation({
    mutationFn: () => deleteEdge(edge.edge_id),
    onSuccess: () => {
      onEdgeDeleted?.(edge.edge_id);
      onClose();
    },
  });

  return (
    <div className="space-y-4 p-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-slate-200">关系详情</h3>
        <div className="flex items-center gap-1">
          {!readOnly && (
            <>
              <button
                onClick={onEdit}
                className="rounded p-1 text-slate-400 hover:bg-slate-800 hover:text-cyan-400"
              >
                <Edit2 className="h-3.5 w-3.5" />
              </button>
              <button
                onClick={() => {
                  if (confirm("确定删除此关系？")) {
                    deleteMutation.mutate();
                  }
                }}
                className="rounded p-1 text-slate-400 hover:bg-slate-800 hover:text-red-400"
              >
                <Trash2 className="h-3.5 w-3.5" />
              </button>
            </>
          )}
          <button
            onClick={onClose}
            className="rounded p-1 text-slate-400 hover:bg-slate-800 hover:text-slate-200"
          >
            <X className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>

      <div className="space-y-3">
        <Field label={FIELD_LABELS.edge_id} value={edge.edge_id} mono />
        <Field
          label={FIELD_LABELS.namespace}
          value={`${NAMESPACE_LABELS[edge.edge_namespace] || edge.edge_namespace} (${edge.edge_namespace})`}
          badge
        />
        <Field label={FIELD_LABELS.type} value={`${edge.edge_type_label || edge.edge_type} (${edge.edge_type})`} badge />

        <div>
          <div className="text-[10px] font-semibold uppercase text-slate-500">{FIELD_LABELS.from_node}</div>
          <NodeEndpointCard node={fromNode} nodeId={edge.from_node} onClick={onSelectNode} />
        </div>

        <div className="flex items-center justify-center">
          <ArrowRight className="h-5 w-5 text-cyan-500" />
        </div>

        <div>
          <div className="text-[10px] font-semibold uppercase text-slate-500">{FIELD_LABELS.to_node}</div>
          <NodeEndpointCard node={toNode} nodeId={edge.to_node} onClick={onSelectNode} />
        </div>

        <Field
          label={FIELD_LABELS.confidence}
          value={`${CONFIDENCE_LABELS[edge.confidence] || edge.confidence} (${edge.confidence})`}
          badge
        />

        <div>
          <div className="text-[10px] font-semibold uppercase text-slate-500">{FIELD_LABELS.description}</div>
          <div className="mt-1 text-sm leading-relaxed text-slate-300">{edge.description || "—"}</div>
        </div>

        {edge.evidence.length > 0 && (
          <div>
            <div className="text-[10px] font-semibold uppercase text-slate-500">
              {FIELD_LABELS.evidence} ({edge.evidence.length})
            </div>
            <div className="mt-1 space-y-2">
              {edge.evidence.map((ev, i) => (
                <div key={i} className="rounded border border-slate-800 bg-slate-850 p-2">
                  <div className="text-xs font-medium text-slate-300">{ev.source_title}</div>
                  <div className="mt-1 text-xs italic text-slate-500">&ldquo;{ev.quote}&rdquo;</div>
                  {ev.source_url && (
                    <a
                      href={ev.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="mt-1 block truncate text-xs text-cyan-400 hover:underline"
                    >
                      {ev.source_url}
                    </a>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {edge.notes && (
          <div>
            <div className="text-[10px] font-semibold uppercase text-slate-500">{FIELD_LABELS.notes}</div>
            <div className="mt-1 text-xs text-slate-400">{edge.notes}</div>
          </div>
        )}
      </div>
    </div>
  );
}

/** 将任意引擎返回的节点统一成端点卡片所需的形状（补全 canonical_name_zh）。 */
function toEndpointNode(node: any): IndustrialNode | undefined {
  if (!node) return undefined;
  return {
    ...node,
    canonical_name_zh: node.canonical_name_zh ?? node.label ?? node.node_id,
    aliases: node.aliases ?? [],
    evidence: node.evidence ?? [],
  };
}

function NodeEndpointCard({
  node,
  nodeId,
  onClick,
}: {
  node?: IndustrialNode;
  nodeId: string;
  onClick?: (node: IndustrialNode) => void;
}) {
  return (
    <button
      type="button"
      onClick={() => node && onClick?.(node)}
      disabled={!node || !onClick}
      className="mt-1 flex w-full items-center justify-between rounded border border-cyan-900/40 bg-cyan-950/20 px-3 py-2 text-left transition-colors hover:border-cyan-700/60 hover:bg-cyan-900/20 disabled:cursor-default disabled:opacity-60"
    >
      <div className="min-w-0">
        <div className="truncate text-sm font-medium text-cyan-100">
          {node ? node.canonical_name_zh : nodeId}
        </div>
        <div className="mt-0.5 truncate text-xs font-mono text-cyan-400/80">{nodeId}</div>
      </div>
      {node && (
        <span className="ml-2 shrink-0 rounded bg-slate-800 px-1.5 py-0.5 text-[10px] text-slate-300">
          {node.entity_type}
        </span>
      )}
    </button>
  );
}

function Field({
  label,
  value,
  mono,
  badge,
}: {
  label: string;
  value: string;
  mono?: boolean;
  badge?: boolean;
}) {
  return (
    <div>
      <div className="text-[10px] font-semibold uppercase text-slate-500">{label}</div>
      {badge ? (
        <span className="mt-1 inline-block rounded bg-slate-800 px-2 py-0.5 text-xs text-slate-300">
          {value}
        </span>
      ) : (
        <div className={`mt-0.5 text-sm text-slate-300 ${mono ? "font-mono" : ""}`}>{value}</div>
      )}
    </div>
  );
}
