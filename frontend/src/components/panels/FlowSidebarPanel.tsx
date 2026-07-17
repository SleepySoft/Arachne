import { useQuery } from "@tanstack/react-query";
import { GitBranch, RotateCcw } from "lucide-react";
import { CollapsibleSection } from "@/components/CollapsibleSection";
import { FilterPanel } from "@/components/FilterPanel";
import { listFlows } from "@/services/api";
import { FlowSummary } from "@/types";
import { IndustrialFiltersState } from "@/types/view";

interface FlowSidebarPanelProps {
  selectedFlowIds: string[];
  onToggleFlow: (flowId: string) => void;
  onRecompile: () => void;
  recompiling: boolean;
  activeFilters: IndustrialFiltersState;
  onChangeFilters: (filters: IndustrialFiltersState) => void;
  engine?: string;
}

/**
 * arachne_flow 引擎的左侧栏：流程文件多选 + 重新编译 + 过滤器。
 * 与 legacy 侧栏共用同一外层布局（选择 chips + 折叠区块 + 过滤）。
 */
export function FlowSidebarPanel({
  selectedFlowIds,
  onToggleFlow,
  onRecompile,
  recompiling,
  activeFilters,
  onChangeFilters,
  engine = "arachne_flow",
}: FlowSidebarPanelProps) {
  const { data: flows = [], isLoading } = useQuery({
    queryKey: ["flows"],
    queryFn: listFlows,
  });

  const selectedFlows = flows.filter((f) => selectedFlowIds.includes(f.flow_id));

  return (
    <div className="flex h-full flex-col overflow-hidden">
      {/* Active selection chips */}
      {selectedFlows.length > 0 && (
        <div className="border-b border-slate-800 p-2">
          <div className="mb-1.5 text-[10px] font-semibold uppercase tracking-wider text-slate-500">
            当前选择
          </div>
          <div className="flex flex-wrap gap-1">
            {selectedFlows.map((flow) => (
              <span
                key={flow.flow_id}
                className="flex items-center gap-1 rounded bg-emerald-900/30 px-1.5 py-0.5 text-[10px] text-emerald-300"
              >
                {flow.root_product}
                <button
                  onClick={() => onToggleFlow(flow.flow_id)}
                  className="text-emerald-500 hover:text-emerald-200"
                  title="移除"
                >
                  ×
                </button>
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="flex-1 overflow-y-auto">
        <CollapsibleSection title="流程文件" badge={selectedFlowIds.length}>
          <div className="space-y-1 p-2">
            {isLoading && <div className="px-2 py-1 text-xs text-slate-500">加载中...</div>}
            {!isLoading && flows.length === 0 && (
              <div className="px-2 py-1 text-xs text-slate-500">未找到流程文件</div>
            )}
            {flows.map((flow) => (
              <FlowListItem
                key={flow.flow_id}
                flow={flow}
                checked={selectedFlowIds.includes(flow.flow_id)}
                onToggle={() => onToggleFlow(flow.flow_id)}
              />
            ))}
          </div>
        </CollapsibleSection>

        <CollapsibleSection title="过滤">
          <FilterPanel filters={activeFilters} onChange={onChangeFilters} engine={engine} />
        </CollapsibleSection>
      </div>

      {/* Recompile action */}
      <div className="border-t border-slate-800 p-3 space-y-2">
        <button
          onClick={onRecompile}
          disabled={selectedFlowIds.length === 0 || recompiling}
          className="flex w-full items-center justify-center gap-1.5 rounded-md bg-slate-700 px-3 py-2 text-sm text-slate-100 transition-colors hover:bg-slate-600 disabled:bg-slate-800 disabled:text-slate-500"
        >
          <RotateCcw className={`h-3.5 w-3.5 ${recompiling ? "animate-spin" : ""}`} />
          {recompiling ? "编译中..." : `重新编译${selectedFlowIds.length > 0 ? ` (${selectedFlowIds.length})` : ""}`}
        </button>
        <div className="text-[10px] text-slate-600">
          共 {flows.length} 个流程文件；勾选后自动加载合并子图
        </div>
      </div>
    </div>
  );
}

function FlowListItem({
  flow,
  checked,
  onToggle,
}: {
  flow: FlowSummary;
  checked: boolean;
  onToggle: () => void;
}) {
  return (
    <label
      className={`flex cursor-pointer items-start gap-2 rounded-md px-3 py-2 text-sm transition-colors ${
        checked
          ? "border border-emerald-500/30 bg-emerald-500/15 text-emerald-300"
          : "text-slate-300 hover:bg-slate-800"
      }`}
    >
      <input
        type="checkbox"
        className="mt-0.5 accent-emerald-500"
        checked={checked}
        onChange={onToggle}
      />
      <div className="min-w-0 flex-1">
        <div className="truncate font-medium">{flow.root_product}</div>
        <div className="mt-0.5 flex items-center gap-2 text-xs text-slate-500">
          <GitBranch className="h-3 w-3" />
          {flow.triples} triples
          {flow.status && (
            <span
              className={`rounded px-1 ${
                flow.status === "COMPILED"
                  ? "bg-emerald-500/20 text-emerald-400"
                  : "bg-slate-700 text-slate-400"
              }`}
            >
              {flow.status}
            </span>
          )}
        </div>
      </div>
    </label>
  );
}
