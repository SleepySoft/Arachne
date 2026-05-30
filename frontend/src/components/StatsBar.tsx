import { useQuery } from "@tanstack/react-query";
import { Activity, Building2, GitBranch, Layers, Network } from "lucide-react";
import { getStats } from "@/services/api";
export type MainView = "industrial_graph";

interface StatsBarProps {
  mainView: MainView;
  onChangeMainView: (view: MainView) => void;
}

export function StatsBar({ mainView, onChangeMainView }: StatsBarProps) {
  const { data: graphStats } = useQuery({
    queryKey: ["stats"],
    queryFn: getStats,
    refetchInterval: 30000,
  });

  return (
    <div className="flex h-full items-center justify-between px-4">
      <div className="flex items-center gap-3">
        {/* Logo */}
        <div className="flex items-center gap-2">
          <Layers className="h-5 w-5 text-cyan-400" />
          <span className="text-lg font-bold tracking-tight text-slate-100">Arachne</span>
          <span className="ml-1 text-xs font-medium text-slate-500">产业本体图</span>
        </div>

        {/* Main View Switcher — 公司视图已移除，保留单视图 */}
        <div className="ml-4 flex items-center rounded-lg border border-slate-700 bg-slate-800 p-0.5">
          <ViewTab
            active={mainView === "industrial_graph"}
            onClick={() => onChangeMainView("industrial_graph")}
            icon={<GitBranch className="h-3 w-3" />}
            label="产业图"
          />
        </div>
      </div>

      {/* Stats — contextual by view */}
      <div className="flex items-center gap-6">
        {mainView === "industrial_graph" ? (
          <>
            <StatItem
              icon={<Activity className="h-4 w-4 text-emerald-400" />}
              label="节点"
              value={graphStats?.total_nodes ?? "—"}
            />
            <StatItem
              icon={<GitBranch className="h-4 w-4 text-amber-400" />}
              label="关系"
              value={graphStats?.total_edges ?? "—"}
            />
          </>
        ) : (
          <>
            <StatItem
              icon={<Building2 className="h-4 w-4 text-cyan-400" />}
              label="公司"
              value={companyNetworkStats?.nodes ?? "—"}
            />
            <StatItem
              icon={<Network className="h-4 w-4 text-amber-400" />}
              label="推断关系"
              value={companyNetworkStats?.edges ?? "—"}
            />
          </>
        )}
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
      className={`flex items-center gap-1 rounded-md px-3 py-1.5 text-xs font-medium transition-colors ${
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
