import { useMutation } from "@tanstack/react-query";
import { Edit2, Trash2, X } from "lucide-react";
import { GraphEdge } from "@/types";
import { deleteEdge } from "@/services/api";

interface EdgeDetailProps {
  edge: GraphEdge;
  onEdit: () => void;
  onClose: () => void;
  onRefresh: () => void;
}

export function EdgeDetail({ edge, onEdit, onClose, onRefresh }: EdgeDetailProps) {
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
        <Field label="edge_id" value={edge.edge_id} mono />
        <Field label="命名空间" value={edge.edge_namespace} badge />
        <Field label="类型" value={edge.edge_type} badge />
        <Field label="起点" value={edge.from_node} mono />
        <Field label="终点" value={edge.to_node} mono />
        <Field label="置信度" value={edge.confidence} badge />

        <div>
          <div className="text-[10px] font-semibold uppercase text-slate-500">描述</div>
          <div className="mt-1 text-sm leading-relaxed text-slate-300">{edge.description}</div>
        </div>

        {edge.evidence.length > 0 && (
          <div>
            <div className="text-[10px] font-semibold uppercase text-slate-500">
              证据 ({edge.evidence.length})
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
            <div className="text-[10px] font-semibold uppercase text-slate-500">备注</div>
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
