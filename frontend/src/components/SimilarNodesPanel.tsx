import { AlertTriangle, ArrowRight } from "lucide-react";
import { IndustrialNode } from "@/types";

interface SimilarNodesPanelProps {
  query: string;
  items: { score: number; node: IndustrialNode }[];
  onSelect: (node: IndustrialNode) => void;
  onDismiss?: () => void;
}

export function SimilarNodesPanel({ query, items, onSelect, onDismiss }: SimilarNodesPanelProps) {
  if (!query.trim() || items.length === 0) return null;

  const highScore = items[0]?.score >= 0.85;

  return (
    <div className="rounded border border-amber-700/50 bg-amber-900/20 p-2.5">
      <div className="mb-2 flex items-start gap-2">
        <AlertTriangle className="mt-0.5 h-3.5 w-3.5 shrink-0 text-amber-400" />
        <div className="flex-1">
          <div className="text-xs font-medium text-amber-400">
            发现 {items.length} 个可能相似的节点
          </div>
          <div className="text-[10px] text-amber-300/80">
            {highScore
              ? "相似度很高，建议先检查是否已有相同节点，避免重复添加。"
              : "如果以下节点与你的意图一致，建议直接选用而非新建。"}
          </div>
        </div>
        {onDismiss && (
          <button
            onClick={onDismiss}
            className="text-[10px] text-amber-400/70 hover:text-amber-400"
          >
            忽略
          </button>
        )}
      </div>

      <div className="space-y-1">
        {items.map(({ score, node }) => (
          <button
            key={node.node_id}
            type="button"
            onClick={() => onSelect(node)}
            className="flex w-full items-center gap-2 rounded border border-slate-800 bg-slate-800/50 px-2 py-1.5 text-left hover:border-cyan-600 hover:bg-slate-800"
          >
            <div className="min-w-0 flex-1">
              <div className="flex items-center gap-1.5">
                <span className="truncate text-xs text-slate-200">
                  {node.canonical_name_zh || node.canonical_name_en || node.node_id}
                </span>
                <span className="shrink-0 text-[10px] text-slate-500">{node.node_id}</span>
              </div>
              {node.definition && (
                <div className="truncate text-[10px] text-slate-500">{node.definition}</div>
              )}
            </div>
            <div className="flex items-center gap-1.5">
              <span
                className={`shrink-0 rounded px-1 py-0 text-[9px] ${
                  score >= 0.85
                    ? "bg-red-900/40 text-red-300"
                    : score >= 0.6
                    ? "bg-amber-900/40 text-amber-300"
                    : "bg-slate-700 text-slate-400"
                }`}
              >
                {(score * 100).toFixed(0)}%
              </span>
              <ArrowRight className="h-3 w-3 shrink-0 text-cyan-500" />
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
