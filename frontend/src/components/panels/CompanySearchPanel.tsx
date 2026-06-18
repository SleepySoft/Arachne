import { CompanyNetworkEdge, CompanyNetworkNode } from "@/types";
import { ExplorationEdge as EEdge } from "@/components/ExplorationCanvas";

interface CompanySearchPanelProps {
  companyExploreMode: "bulk" | "manual";
  setCompanyExploreMode: (mode: "bulk" | "manual") => void;
  companyDisplayMode: "empty" | "global" | "local";
  orderedChain: string[];
  fixedIds: Set<string>;
  nodeStore: Map<string, CompanyNetworkNode>;
  currentFocusId: string | null;
  previewData: { centerId: string; nodes: CompanyNetworkNode[]; edges: CompanyNetworkEdge[] } | null;
  selectedExplorationEdge: EEdge | null;
  onClear: () => void;
}

export function CompanySearchPanel({
  companyExploreMode,
  setCompanyExploreMode,
  companyDisplayMode,
  orderedChain,
  fixedIds,
  nodeStore,
  currentFocusId,
  previewData,
  selectedExplorationEdge,
  onClear,
}: CompanySearchPanelProps) {
  return (
    <div className="flex items-center gap-2">
      <div className="flex items-center rounded border border-slate-700 bg-slate-800/50 overflow-hidden">
        <button
          onClick={() => setCompanyExploreMode("bulk")}
          className={`px-2 py-1 text-[10px] font-medium transition-colors ${
            companyExploreMode === "bulk"
              ? "bg-cyan-600/20 text-cyan-400"
              : "text-slate-500 hover:text-slate-300"
          }`}
          title="自动加载全部上下游关联"
        >
          全量
        </button>
        <button
          onClick={() => setCompanyExploreMode("manual")}
          className={`px-2 py-1 text-[10px] font-medium transition-colors ${
            companyExploreMode === "manual"
              ? "bg-cyan-600/20 text-cyan-400"
              : "text-slate-500 hover:text-slate-300"
          }`}
          title="只显示通过物料关联面板选择的公司"
        >
          探索
        </button>
      </div>
      {companyDisplayMode === "empty" && (
        <span className="text-xs text-slate-500">选择一个公司开始浏览，或绘制全局图</span>
      )}
      {companyDisplayMode === "local" && (
        <div className="flex items-center gap-1 overflow-hidden">
          {companyExploreMode === "manual" ? (
            selectedExplorationEdge ? (
              <span className="text-xs text-slate-300">
                {selectedExplorationEdge.type === "exposure"
                  ? `${selectedExplorationEdge.source} → ${selectedExplorationEdge.target}${selectedExplorationEdge.label ? " (" + selectedExplorationEdge.label + ")" : ""}`
                  : `${selectedExplorationEdge.source} → ${selectedExplorationEdge.target} (${selectedExplorationEdge.edge_type || "industrial_flow"})`}
              </span>
            ) : (
              <span className="text-xs text-slate-500">点击物料节点探索关联公司，点击边查看连接详情</span>
            )
          ) : (
            <>
              {orderedChain.map((id, idx) => (
                <span key={id} className="flex items-center gap-1">
                  {idx > 0 && <span className="text-slate-600">→</span>}
                  <span className={`text-xs ${id === currentFocusId ? "text-cyan-400 font-medium" : "text-slate-400"}`}>
                    {nodeStore.get(id)?.name_zh || id}
                  </span>
                </span>
              ))}
              {fixedIds.size > 0 && (
                <span className="text-xs text-amber-500 ml-1">
                  (+{fixedIds.size} 固定)
                </span>
              )}
              {previewData && (
                <span className="text-xs text-slate-500 ml-1">— 关联节点临时显示</span>
              )}
            </>
          )}
        </div>
      )}
      {companyDisplayMode === "global" && (
        <span className="text-xs text-slate-500">全局网络视图 — 点击节点高亮，双击开始考察</span>
      )}
      {companyDisplayMode !== "empty" && (
        <button
          onClick={onClear}
          className="ml-auto flex items-center gap-1 rounded-md bg-amber-600/20 px-2.5 py-1 text-xs font-medium text-amber-400 hover:bg-amber-600/30 transition-colors"
        >
          清空视图
        </button>
      )}
    </div>
  );
}
