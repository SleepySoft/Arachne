import { useMutation } from "@tanstack/react-query";
import { Edit2, Trash2, X } from "lucide-react";
import { IndustrialNode } from "@/types";
import { deleteNode } from "@/services/api";
import { NodeEdgeList } from "./NodeEdgeList";

interface NodeDetailProps {
  node: IndustrialNode;
  onEdit: () => void;
  onClose: () => void;
  onRefresh: () => void;
  onSelectNode?: (node: IndustrialNode) => void;
}

export function NodeDetail({ node, onEdit, onClose, onRefresh, onSelectNode }: NodeDetailProps) {
  const deleteMutation = useMutation({
    mutationFn: deleteNode,
    onSuccess: () => {
      onRefresh();
      onClose();
    },
  });

  return (
    <div className="space-y-4 p-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-slate-200">节点详情</h3>
        <div className="flex items-center gap-1">
          <button
            onClick={onEdit}
            className="rounded p-1 text-slate-400 hover:bg-slate-800 hover:text-cyan-400"
          >
            <Edit2 className="h-3.5 w-3.5" />
          </button>
          <button
            onClick={() => {
              if (confirm("确定删除此节点？关联的关系也会被删除。")) {
                deleteMutation.mutate(node.node_id);
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

      {isDraftNode(node) && (
        <div className="rounded border border-amber-700/50 bg-amber-900/20 px-3 py-2">
          <div className="text-xs font-medium text-amber-400">⚠️ 草稿节点 / 待完善</div>
          <div className="mt-0.5 text-[10px] text-amber-300/80">
            该节点由快速添加创建，ID、定义、类型或证据可能不完整，后续需要人工或 AI 补全。
          </div>
        </div>
      )}

      <div className="space-y-3">
        <Field label="node_id" value={node.node_id} mono />
        <Field label="中文名" value={node.canonical_name_zh} />
        <Field label="英文名" value={node.canonical_name_en || "—"} />
        <Field label="类型" value={node.entity_type} badge />
        <Field label="状态" value={node.status} badge />
        <Field label="置信度" value={node.confidence} badge />

        <div>
          <div className="text-[10px] font-semibold uppercase text-slate-500">定义</div>
          <div className="mt-1 text-sm leading-relaxed text-slate-300">{node.definition}</div>
        </div>

        {node.aliases.length > 0 && (
          <div>
            <div className="text-[10px] font-semibold uppercase text-slate-500">别名</div>
            <div className="mt-1 flex flex-wrap gap-1">
              {node.aliases.map((a) => (
                <span key={a} className="rounded bg-slate-800 px-2 py-0.5 text-xs text-slate-400">
                  {a}
                </span>
              ))}
            </div>
          </div>
        )}

        {node.evidence.length > 0 && (
          <div>
            <div className="text-[10px] font-semibold uppercase text-slate-500">
              证据 ({node.evidence.length})
            </div>
            <div className="mt-1 space-y-2">
              {node.evidence.map((ev, i) => (
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

        {node.notes && (
          <div>
            <div className="text-[10px] font-semibold uppercase text-slate-500">备注</div>
            <div className="mt-1 text-xs text-slate-400">{node.notes}</div>
          </div>
        )}

        {/* Relationship section: single entry point */}
        <div className="border-t border-slate-800 pt-3">
          <NodeEdgeList
            nodeId={node.node_id}
            onRefreshGraph={onRefresh}
            onSelectNode={onSelectNode}
          />
        </div>
      </div>
    </div>
  );
}

function isDraftNode(node: IndustrialNode): boolean {
  return (
    node.status === "PENDING" ||
    node.entity_type === "unknown" ||
    !node.definition ||
    node.definition.trim() === "" ||
    node.node_id.startsWith("draft_")
  );
}

function Field({
  label,
  value,
  mono,
  badge,
}: {
  label: string;
  value?: string | null;
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
