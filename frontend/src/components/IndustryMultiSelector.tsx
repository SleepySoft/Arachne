import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Building2, Factory, RefreshCw, Search, Tags } from "lucide-react";
import { Industry, IndustryType } from "@/types";
import { listIndustries } from "@/services/api";

interface IndustryMultiSelectorProps {
  selectedIds: string[];
  onToggle: (industry: Industry) => void;
  onSelect: (industry: Industry) => void;
  onCreate: () => void;
}

const TYPE_ICONS: Record<IndustryType, typeof Building2> = {
  formal_industry: Factory,
  curated_view: Building2,
  theme_view: Tags,
};

const TYPE_LABELS: Record<IndustryType, string> = {
  formal_industry: "正式行业",
  curated_view: "产业链视图",
  theme_view: "市场主题",
};

export function IndustryMultiSelector({
  selectedIds,
  onToggle,
  onSelect,
  onCreate,
}: IndustryMultiSelectorProps) {
  const [search, setSearch] = useState("");
  const [industryType, setIndustryType] = useState<IndustryType | "">("");
  const [status, setStatus] = useState("");

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["industries", 1, 50, industryType || null, status || null, search || null],
    queryFn: () => listIndustries(1, 50, industryType || undefined, status || undefined, search || undefined),
    refetchOnMount: "always",
  });

  return (
    <div className="flex h-full flex-col">
      <div className="px-3 py-2">
        <div className="relative">
          <Search className="absolute left-2 top-1/2 h-3 w-3 -translate-y-1/2 text-slate-500" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="搜索行业..."
            className="w-full rounded border border-slate-700 bg-slate-800 py-1 pl-6 pr-2 text-xs text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
          />
        </div>
      </div>

      <div className="flex gap-1 px-3 pb-2">
        <select
          value={industryType}
          onChange={(e) => setIndustryType(e.target.value as IndustryType | "")}
          className="flex-1 rounded border border-slate-700 bg-slate-800 py-1 px-1.5 text-[10px] text-slate-300 focus:border-cyan-500 focus:outline-none"
        >
          <option value="">全部类型</option>
          <option value="formal_industry">正式行业</option>
          <option value="curated_view">产业链</option>
          <option value="theme_view">主题</option>
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
        ) : error ? (
          <div className="py-4 text-center">
            <div className="text-xs text-red-400 mb-2">加载失败</div>
            <button
              onClick={() => refetch()}
              className="flex items-center gap-1 mx-auto rounded bg-slate-800 px-2 py-1 text-xs text-slate-300 hover:bg-slate-700"
            >
              <RefreshCw className="h-3 w-3" />
              重试
            </button>
          </div>
        ) : !data || data.items.length === 0 ? (
          <div className="py-4 text-center text-xs text-slate-500">无结果</div>
        ) : (
          <div className="space-y-1">
            {data.items.map((ind) => {
              const Icon = TYPE_ICONS[ind.industry_type];
              const isSelected = selectedIds.includes(ind.industry_id);
              return (
                <div
                  key={ind.industry_id}
                  className={`flex items-start gap-1.5 rounded px-1.5 py-1.5 text-left transition-colors ${
                    isSelected
                      ? "bg-cyan-900/20 border border-cyan-700/30"
                      : "hover:bg-slate-800 border border-transparent"
                  }`}
                >
                  <input
                    type="checkbox"
                    checked={isSelected}
                    onChange={() => onToggle(ind)}
                    className="mt-0.5 h-3 w-3 shrink-0 rounded border-slate-600 bg-slate-800 text-cyan-500"
                  />
                  <button
                    onClick={() => onSelect(ind)}
                    className="flex min-w-0 flex-1 items-start gap-1.5 text-left"
                  >
                    <Icon className={`mt-0.5 h-3.5 w-3.5 shrink-0 ${isSelected ? "text-cyan-400" : "text-slate-500"}`} />
                    <div className="min-w-0 flex-1">
                      <div className={`truncate text-xs font-medium ${isSelected ? "text-cyan-300" : "text-slate-200"}`}>
                        {ind.name_zh}
                      </div>
                      <div className="mt-0.5 flex items-center gap-1.5">
                        <span className="text-[10px] text-slate-500">{TYPE_LABELS[ind.industry_type]}</span>
                        <span
                          className={`rounded px-1 py-0 text-[9px] ${
                            ind.status === "ACTIVE"
                              ? "bg-emerald-900/40 text-emerald-400"
                              : ind.status === "PENDING"
                              ? "bg-amber-900/40 text-amber-400"
                              : "bg-slate-700 text-slate-400"
                          }`}
                        >
                          {ind.status}
                        </span>
                      </div>
                    </div>
                  </button>
                </div>
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
          <Building2 className="h-3 w-3" />
          创建行业
        </button>
      </div>
    </div>
  );
}
