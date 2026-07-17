import { useQuery } from "@tanstack/react-query";
import { Activity, Brain, Database, GitBranch, Layers, Network } from "lucide-react";
import { getHealth, getStats, listEngines } from "@/services/api";
export type MainView = "industrial_graph" | "company_graph" | "flow_graph" | "db_checks" | "reasoning";
export type GraphEngine = string;

interface StatsBarProps {
  mainView: MainView;
  onChangeMainView: (view: MainView) => void;
  graphEngine?: GraphEngine;
  onChangeGraphEngine?: (engine: GraphEngine) => void;
}

export function StatsBar({
  mainView,
  onChangeMainView,
  graphEngine = "legacy",
  onChangeGraphEngine,
}: StatsBarProps) {
  const { data: graphStats } = useQuery({
    queryKey: ["stats"],
    queryFn: getStats,
    refetchInterval: 30000,
  });

  const { data: health } = useQuery({
    queryKey: ["health"],
    queryFn: getHealth,
    refetchInterval: 10000,
    retry: false,
  });

  const { data: enginesData } = useQuery({
    queryKey: ["engines"],
    queryFn: listEngines,
    staleTime: 60000,
  });

  const engineOptions = enginesData?.engines ?? [
    { name: "legacy", label: "legacy 引擎" },
    { name: "arachne_flow", label: "arachne_flow 引擎" },
  ];

  const companyNetworkStats = { nodes: 0, edges: 0 };

  return (
    <div className="flex h-full items-center justify-between px-4">
      <div className="flex items-center gap-3">
        {/* Logo */}
        <div className="flex items-center gap-2">
          <Layers className="h-5 w-5 text-cyan-400" />
          <span className="text-lg font-bold tracking-tight text-slate-100">Arachne</span>
          <span className="ml-1 text-xs font-medium text-slate-500">产业本体图</span>
        </div>

        {/* Engine selector */}
        <div className="ml-4 flex items-center">
          <select
            value={graphEngine}
            title={engineOptions.find((e) => e.name === graphEngine)?.description}
            onChange={(e) => onChangeGraphEngine?.(e.target.value)}
            className="h-8 rounded-md border border-slate-700 bg-slate-900 px-2 text-sm text-slate-200 outline-none focus:border-cyan-500 disabled:opacity-50"
            disabled={!enginesData}
          >
            {engineOptions.map((engine) => (
              <option key={engine.name} value={engine.name}>
                {engine.label}
              </option>
            ))}
          </select>
        </div>

        {/* Main View Switcher */}
        <div className="ml-3 flex items-center rounded-lg border border-slate-700 bg-slate-800 p-0.5">
          <ViewTab
            active={mainView === "industrial_graph"}
            onClick={() => onChangeMainView("industrial_graph")}
            icon={<GitBranch className="h-3 w-3" />}
            label="产业图"
          />
          <ViewTab
            active={mainView === "db_checks"}
            onClick={() => onChangeMainView("db_checks")}
            icon={<Database className="h-3 w-3" />}
            label="数据检查"
          />
          <ViewTab
            active={mainView === "flow_graph"}
            onClick={() => onChangeMainView("flow_graph")}
            icon={<Layers className="h-3 w-3" />}
            label="流程图"
          />
          <ViewTab
            active={mainView === "reasoning"}
            onClick={() => onChangeMainView("reasoning")}
            icon={<Brain className="h-3 w-3" />}
            label="推理"
          />
        </div>
      </div>

      {/* DB health indicators */}
      <div className="flex items-center gap-3">
        <StatusDot label="Neo4j" status={health?.neo4j === "ok" ? "ok" : "error"} />
        <StatusDot label="PostgreSQL" status={health?.postgres === "ok" ? "ok" : health?.postgres === "not_configured" ? "warning" : "error"} />
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
        ) : mainView === "company_graph" ? (
          <>
            <StatItem
              icon={<Network className="h-4 w-4 text-cyan-400" />}
              label="公司"
              value={companyNetworkStats?.nodes ?? "—"}
            />
            <StatItem
              icon={<Network className="h-4 w-4 text-amber-400" />}
              label="推断关系"
              value={companyNetworkStats?.edges ?? "—"}
            />
          </>
        ) : null}
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

function StatusDot({ label, status }: { label: string; status: "ok" | "warning" | "error" }) {
  const color =
    status === "ok" ? "bg-emerald-500" : status === "warning" ? "bg-amber-500" : "bg-red-500";
  const text = status === "ok" ? "text-emerald-400" : status === "warning" ? "text-amber-400" : "text-red-400";
  return (
    <div className="flex items-center gap-1.5 text-xs" title={`${label}: ${status}`}>
      <span className={`h-2 w-2 rounded-full ${color}`} />
      <span className={`font-medium ${text}`}>{label}</span>
    </div>
  );
}
