import { useMutation, useQuery } from "@tanstack/react-query";
import { Edit2, Trash2, X } from "lucide-react";
import { GraphEdge } from "@/types";
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
  onRefresh: () => void;
}

export function EdgeDetail({ edge, onEdit, onClose, onRefresh }: EdgeDetailProps) {
  const { data: fromNode } = useQuery({
    queryKey: ["node", edge.from_node],
    queryFn: () => getNode(edge.from_node),
    enabled: !!edge.from_node,
  });
  const { data: toNode } = useQuery({
    queryKey: ["node", edge.to_node],
    queryFn: () => getNode(edge.to_node),
    enabled: !!edge.to_node,
  });

  const fromLabel = fromNode
    ? `${fromNode.canonical_name_zh} (${edge.from_node})`
    : edge.from_node;
  const toLabel = toNode
    ? `${toNode.canonical_name_zh} (${edge.to_node})`
    : edge.to_node;

  const deleteMutation = useMutation({
    mutationFn: () => deleteEdge(edge.edge_id),
    onSuccess: () => {
      onRefresh();
      onClose();
    },
  });

  return (
    <div className="space-y-4 p-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-slate-200">关系详情</h3>
        <div className="flex items-center gap-1">
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
        <Field label={FIELD_LABELS.from_node} value={fromLabel} />
        <Field label={FIELD_LABELS.to_node} value={toLabel} />
        <Field
          label={FIELD_LABELS.confidence}
          value={`${CONFIDENCE_LABELS[edge.confidence] || edge.confidence} (${edge.confidence})`}
          badge
        />

        <div>
          <div className="text-[10px] font-semibold uppercase text-slate-500">{FIELD_LABELS.description}</div>
          <div className="mt-1 text-sm leading-relaxed text-slate-300">{edge.description}</div>
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
