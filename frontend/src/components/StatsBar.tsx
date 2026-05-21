import { useQuery } from "@tanstack/react-query";
import { Activity, GitBranch, Layers } from "lucide-react";
import { getStats } from "@/services/api";

export function StatsBar() {
  const { data } = useQuery({
    queryKey: ["stats"],
    queryFn: getStats,
    refetchInterval: 30000,
  });

  return (
    <div className="flex h-full items-center justify-between px-4">
      <div className="flex items-center gap-2">
        <Layers className="h-5 w-5 text-cyan-400" />
        <span className="text-lg font-bold tracking-tight text-slate-100">
          Arachne
        </span>
        <span className="text-xs text-slate-500 font-medium ml-1">
          统一产业本体图
        </span>
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
