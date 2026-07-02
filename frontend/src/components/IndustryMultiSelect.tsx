import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Search, X } from "lucide-react";
import { Industry, IndustryNodeAssociation } from "@/types";
import { listIndustries } from "@/services/api";

interface IndustryMultiSelectProps {
  selected: IndustryNodeAssociation[];
  onChange: (selected: IndustryNodeAssociation[]) => void;
  placeholder?: string;
}

export function IndustryMultiSelect({
  selected,
  onChange,
  placeholder = "搜索并添加行业...",
}: IndustryMultiSelectProps) {
  const [query, setQuery] = useState("");

  const { data } = useQuery({
    queryKey: ["industries", 1, 10, undefined, undefined, query],
    queryFn: () => listIndustries(1, 10, undefined, undefined, query),
    enabled: query.length >= 1,
  });

  const addIndustry = (industry: Industry) => {
    if (selected.some((s) => s.industry_id === industry.industry_id)) return;
    onChange([
      ...selected,
      {
        industry_id: industry.industry_id,
        weight: 1.0,
        confidence: "MEDIUM",
        status: "ACTIVE",
      },
    ]);
    setQuery("");
  };

  const removeIndustry = (industryId: string) => {
    onChange(selected.filter((s) => s.industry_id !== industryId));
  };

  return (
    <div className="space-y-1.5">
      <label className="block text-[10px] font-medium text-slate-400">
        所属行业（可选）
      </label>

      <div className="relative">
        <Search className="absolute left-2 top-1/2 h-3 w-3 -translate-y-1/2 text-slate-500" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={placeholder}
          className="w-full rounded border border-slate-700 bg-slate-800 py-1 pl-5 pr-2 text-xs text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
        />
        {data && query && (
          <div className="absolute z-10 mt-1 max-h-32 w-full overflow-auto rounded border border-slate-700 bg-slate-800 shadow-lg">
            {data.items.length === 0 ? (
              <div className="px-2 py-1 text-xs text-slate-500">无结果</div>
            ) : (
              data.items.map((ind) => (
                <button
                  key={ind.industry_id}
                  type="button"
                  onClick={() => addIndustry(ind)}
                  className="flex w-full items-center gap-2 px-2 py-1 text-left text-xs hover:bg-slate-700"
                >
                  <span className="truncate font-medium text-slate-200">
                    {ind.name_zh}
                  </span>
                  <span className="shrink-0 text-[10px] text-slate-500">
                    {ind.industry_id}
                  </span>
                </button>
              ))
            )}
          </div>
        )}
      </div>

      {selected.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {selected.map((s) => (
            <span
              key={s.industry_id}
              className="inline-flex max-w-full items-center gap-1 rounded bg-cyan-900/30 px-1.5 py-0.5 text-[10px] text-cyan-300"
            >
              <span className="truncate">{s.industry_id}</span>
              <button
                type="button"
                onClick={() => removeIndustry(s.industry_id)}
                className="shrink-0 text-cyan-500 hover:text-cyan-200"
              >
                <X className="h-3 w-3" />
              </button>
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
