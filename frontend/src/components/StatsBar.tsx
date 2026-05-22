import { useQuery } from "@tanstack/react-query";
import { Activity, Building2, Factory, GitBranch, Layers } from "lucide-react";
import { getStats } from "@/services/api";

export type ViewMode = "graph" | "industries" | "companies";

interface StatsBarProps {
  viewMode: ViewMode;
  onChangeView: (mode: ViewMode) => void;
}

export function StatsBar({ viewMode, onChangeView }: StatsBarProps) {
  const { data } = useQuery({
    queryKey: ["stats"],
    queryFn: getStats,
    refetchInterval: 30000,
  });

  return (
    <div className="flex h-full items-center justify-between px-4">
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2">
          <Layers className="h-5 w-5 text-cyan-400" />
          <span className="text-lg font-bold tracking-tight text-slate-100">Arachne</span>
          <span className="ml-1 text-xs font-medium text-slate-500">统一产业本体图</span>
        </div>

        {/* View Switcher */}
        <div className="ml-4 flex items-center rounded-lg border border-slate-700 bg-slate-800 p-0.5">
          <ViewTab
            active={viewMode === "graph"}
            onClick={() => onChangeView("graph")}
            icon={<GitBranch className="h-3 w-3" />}
            label="产业图"
          />
          <ViewTab
            active={viewMode === "industries"}
            onClick={() => onChangeView("industries")}
            icon={<Factory className="h-3 w-3" />}
            label="行业"
          />
          <ViewTab
            active={viewMode === "companies"}
            onClick={() => onChangeView("companies")}
            icon={<Building2 className="h-3 w-3" />}
            label="公司"
          />
        </div>
      </div>

      <div className="flex items-center gap-6">
        <StatItem
          icon={<Activity className="h-4 w-4 text-emerald-400" />}
          label="节点"
          value={data?.total_nodes ?? "—"}
        />
        <StatItem
          icon={<GitBranch className="h-4 w-4 text-amber-400" />}
          label="关系"
          value={data?.total_edges ?? "—"}
        />
      </div>
    </div>
  );
}

function ViewTab({
  active,
  onClick,
  icon,
  label,
}: {
  active: boolean;
  onClick: () => void;
  icon: React.ReactNode;
  label: string;
}) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center gap-1 rounded-md px-2.5 py-1 text-xs font-medium transition-colors ${
        active
          ? "bg-cyan-600 text-white"
          : "text-slate-400 hover:bg-slate-700 hover:text-slate-200"
      }`}
    >
      {icon}
      {label}
    </button>
  );
}

function StatItem({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: number | string;
}) {
  return (
    <div className="flex items-center gap-2 text-sm">
      {icon}
      <span className="text-slate-400">{label}</span>
      <span className="font-mono font-semibold text-slate-200">{value}</span>
    </div>
  );
}
