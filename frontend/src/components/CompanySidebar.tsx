import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Building, Landmark, Search, Store, TrendingUp } from "lucide-react";
import { Company, CompanyType } from "@/types";
import { listCompanies } from "@/services/api";

interface CompanySidebarProps {
  selectedId?: string;
  onSelect: (company: Company) => void;
  onCreate: () => void;
}

const TYPE_ICONS: Record<CompanyType, typeof Building> = {
  public: TrendingUp,
  private: Store,
  state_owned: Landmark,
  startup: Building,
  unknown: Building,
};

const TYPE_LABELS: Record<CompanyType, string> = {
  public: "上市公司",
  private: "民营",
  state_owned: "国企",
  startup: "初创",
  unknown: "未知",
};

export function CompanySidebar({ selectedId, onSelect, onCreate }: CompanySidebarProps) {
  const [search, setSearch] = useState("");
  const [companyType, setCompanyType] = useState<CompanyType | "">("");
  const [status, setStatus] = useState("");

  const { data, isLoading } = useQuery({
    queryKey: ["companies", 1, 50, undefined, companyType || undefined, status || undefined, search || undefined],
    queryFn: () => listCompanies(1, 50, undefined, companyType || undefined, status || undefined, search || undefined),
  });

  return (
    <div className="flex h-full flex-col">
      <div className="border-b border-slate-800 px-3 py-2">
        <h2 className="text-xs font-semibold uppercase tracking-wider text-slate-400">公司视图</h2>
      </div>

      <div className="px-3 py-2">
        <div className="relative">
          <Search className="absolute left-2 top-1/2 h-3 w-3 -translate-y-1/2 text-slate-500" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="搜索公司..."
            className="w-full rounded border border-slate-700 bg-slate-800 py-1 pl-6 pr-2 text-xs text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
          />
        </div>
      </div>

      <div className="flex gap-1 px-3 pb-2">
        <select
          value={companyType}
          onChange={(e) => setCompanyType(e.target.value as CompanyType | "")}
          className="flex-1 rounded border border-slate-700 bg-slate-800 py-1 px-1.5 text-[10px] text-slate-300 focus:border-cyan-500 focus:outline-none"
        >
          <option value="">全部类型</option>
          <option value="public">上市</option>
          <option value="private">民营</option>
          <option value="state_owned">国企</option>
          <option value="startup">初创</option>
        </select>
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          className="flex-1 rounded border border-slate-700 bg-slate-800 py-1 px-1.5 text-[10px] text-slate-300 focus:border-cyan-500 focus:outline-none"
        >
          <option value="">全部状态</option>
          <option value="ACTIVE">启用</option>
          <option value="PENDING">待审</option>
          <option value="ARCHIVED">归档</option>
        </select>
      </div>

      <div className="flex-1 overflow-y-auto px-2 pb-2">
        {isLoading ? (
          <div className="py-4 text-center text-xs text-slate-500">加载中...</div>
        ) : data?.items.length === 0 ? (
          <div className="py-4 text-center text-xs text-slate-500">无结果</div>
        ) : (
          <div className="space-y-1">
            {data?.items.map((co) => {
              const Icon = TYPE_ICONS[co.company_type];
              const isActive = co.company_id === selectedId;
              return (
                <button
                  key={co.company_id}
                  onClick={() => onSelect(co)}
                  className={`flex w-full items-start gap-2 rounded px-2 py-1.5 text-left transition-colors ${
                    isActive
                      ? "bg-cyan-900/30 border border-cyan-700/50"
                      : "hover:bg-slate-800 border border-transparent"
                  }`}
                >
                  <Icon className={`mt-0.5 h-3.5 w-3.5 shrink-0 ${isActive ? "text-cyan-400" : "text-slate-500"}`} />
                  <div className="min-w-0 flex-1">
                    <div className={`truncate text-xs font-medium ${isActive ? "text-cyan-300" : "text-slate-200"}`}>
                      {co.name_zh}
                    </div>
                    <div className="mt-0.5 flex items-center gap-1.5">
                      <span className="text-[10px] text-slate-500">{TYPE_LABELS[co.company_type]}</span>
                      {co.stock_codes && co.stock_codes.length > 0 && (
                        <span className="text-[10px] text-slate-600">{co.stock_codes[0]}</span>
                      )}
                      <span
                        className={`rounded px-1 py-0 text-[9px] ${
                          co.status === "ACTIVE"
                            ? "bg-emerald-900/40 text-emerald-400"
                            : co.status === "PENDING"
                            ? "bg-amber-900/40 text-amber-400"
                            : "bg-slate-700 text-slate-400"
                        }`}
                      >
                        {co.status}
                      </span>
                    </div>
                  </div>
                </button>
              );
            })}
          </div>
        )}
      </div>

      <div className="border-t border-slate-800 p-2">
        <button
          onClick={onCreate}
          className="flex w-full items-center justify-center gap-1 rounded border border-slate-700 bg-slate-800 py-1.5 text-xs text-slate-300 hover:border-cyan-600 hover:text-cyan-400"
        >
          <Building className="h-3 w-3" />
          创建公司
        </button>
      </div>
    </div>
  );
}
