import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Edit2, Trash2, X, Link2, Plus, Crosshair } from "lucide-react";
import { Company } from "@/types";
import { deleteCompany, getCompanySubgraph, listCompanyExposures } from "@/services/api";

interface CompanyDetailProps {
  company: Company;
  onEdit: () => void;
  onClose: () => void;
  onRefresh: () => void;
  onLoadSubgraph: (nodes: unknown[], edges: unknown[]) => void;
  onHighlightNodes: (nodeIds: string[]) => void;
  onAddExposure: () => void;
}

function Field({ label, value, badge }: { label: string; value?: string | number | null; badge?: boolean }) {
  if (value === undefined || value === null || value === "") return null;
  return (
    <div className="flex flex-col gap-0.5">
      <span className="text-[10px] font-medium uppercase tracking-wider text-slate-500">{label}</span>
      {badge ? (
        <span className="w-fit rounded bg-slate-800 px-1.5 py-0.5 text-xs text-slate-300">{value}</span>
      ) : (
        <span className="text-xs text-slate-200">{value}</span>
      )}
    </div>
  );
}

function formatCurrency(value?: number): string | undefined {
  if (value === undefined || value === null) return undefined;
  if (value >= 100000000) return `${(value / 100000000).toFixed(2)} 亿`;
  if (value >= 10000) return `${(value / 10000).toFixed(2)} 万`;
  return value.toString();
}

export function CompanyDetail({
  company,
  onEdit,
  onClose,
  onRefresh,
  onLoadSubgraph,
  onHighlightNodes,
  onAddExposure,
}: CompanyDetailProps) {
  const queryClient = useQueryClient();

  const { data: tempSubgraph } = useQuery({
    queryKey: ["company-temp-subgraph", company.company_id],
    queryFn: () => getCompanySubgraph(company.company_id),
  });

  const { data: exposuresData } = useQuery({
    queryKey: ["company-exposures", company.company_id, 1, 50],
    queryFn: () => listCompanyExposures(company.company_id, 1, 50),
  });

  const deleteMutation = useMutation({
    mutationFn: deleteCompany,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["companies"] });
      onRefresh();
      onClose();
    },
  });

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b border-slate-800 px-4 py-3">
        <h3 className="truncate pr-2 text-sm font-semibold text-slate-100">{company.name_zh}</h3>
        <div className="flex items-center gap-1">
          <button
            onClick={() => {
              if (tempSubgraph) onLoadSubgraph(tempSubgraph.nodes, tempSubgraph.edges);
            }}
            title="加载临时子图"
            className="flex h-7 w-7 items-center justify-center rounded text-slate-400 hover:bg-slate-800 hover:text-cyan-400"
          >
            <Link2 className="h-3.5 w-3.5" />
          </button>
          <button
            onClick={() => {
              const nodeIds = exposuresData?.items.map((e) => e.node_id) ?? [];
              if (nodeIds.length > 0) onHighlightNodes(nodeIds);
            }}
            title="在图中高亮"
            className="flex h-7 w-7 items-center justify-center rounded text-slate-400 hover:bg-slate-800 hover:text-yellow-400"
          >
            <Crosshair className="h-3.5 w-3.5" />
          </button>
          <button
            onClick={onEdit}
            title="编辑"
            className="flex h-7 w-7 items-center justify-center rounded text-slate-400 hover:bg-slate-800 hover:text-cyan-400"
          >
            <Edit2 className="h-3.5 w-3.5" />
          </button>
          <button
            onClick={() => {
              if (confirm("确定删除这个公司？")) deleteMutation.mutate(company.company_id);
            }}
            title="删除"
            className="flex h-7 w-7 items-center justify-center rounded text-slate-400 hover:bg-slate-800 hover:text-red-400"
          >
            <Trash2 className="h-3.5 w-3.5" />
          </button>
          <button
            onClick={onClose}
            title="关闭"
            className="flex h-7 w-7 items-center justify-center rounded text-slate-400 hover:bg-slate-800 hover:text-slate-200"
          >
            <X className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>

      <div className="flex-1 space-y-4 overflow-y-auto p-4">
        <div className="space-y-2">
          <Field label="ID" value={company.company_id} badge />
          <Field label="英文名" value={company.name_en} />
          {company.stock_codes && company.stock_codes.length > 0 && (
            <Field label="股票代码" value={company.stock_codes.join(" / ")} badge />
          )}
          <Field label="类型" value={company.company_type} badge />
          <Field label="国家" value={company.country} badge />
          <Field label="地区" value={company.province ? `${company.province}${company.city ? ` · ${company.city}` : ""}` : undefined} />
          <Field label="成立年份" value={company.founded_year} />
          <Field label="员工数" value={company.employee_count ? `${company.employee_count.toLocaleString()} 人` : undefined} />
          <Field label="营收" value={formatCurrency(company.revenue_cny)} />
          <Field label="市值" value={formatCurrency(company.market_cap_cny)} />
          <Field label="净利润" value={formatCurrency(company.net_profit_cny)} />
          <Field label="状态" value={company.status} badge />
          {company.aliases && company.aliases.length > 0 && <Field label="别名" value={company.aliases.join("、")} />}
          <Field label="描述" value={company.description} />
          {company.notes && <Field label="备注" value={company.notes} />}
        </div>

        <div className="border-t border-slate-800 pt-3">
          <div className="mb-2 flex items-center justify-between">
            <h4 className="text-xs font-semibold text-slate-300">
              产业暴露 ({exposuresData?.total ?? 0})
            </h4>
            <button
              onClick={onAddExposure}
              className="flex items-center gap-1 rounded px-1.5 py-0.5 text-[10px] text-cyan-400 hover:bg-cyan-900/20"
            >
              <Plus className="h-3 w-3" />
              添加
            </button>
          </div>
          <div className="space-y-1.5">
            {exposuresData?.items.map((exp) => (
              <div
                key={exp.exposure_id}
                className="rounded border border-slate-800 bg-slate-800/50 px-2.5 py-1.5"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-medium text-slate-200">{exp.node_id}</span>
                  <span className="text-[10px] text-slate-500">{exp.weight.toFixed(2)}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-[10px] text-slate-400">{exp.activity_type}</span>
                  {exp.role && <span className="text-[10px] text-slate-500">{exp.role}</span>}
                </div>
              </div>
            ))}
            {(exposuresData?.items.length ?? 0) === 0 && (
              <div className="text-center text-xs text-slate-500 py-2">暂无产业暴露</div>
            )}
          </div>
        </div>


      </div>
    </div>
  );
}
