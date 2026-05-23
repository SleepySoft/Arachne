import { useEffect, useState } from "react";
import { Building2, Loader2, X } from "lucide-react";
import { Company, CompanyNodeExposure } from "@/types";
import { getCompaniesByNode } from "@/services/api";

interface NodeCompaniesPanelProps {
  nodeId: string;
  nodeName: string;
  onClose: () => void;
  onSelectCompany: (company: Company) => void;
}

export function NodeCompaniesPanel({
  nodeId,
  nodeName,
  onClose,
  onSelectCompany,
}: NodeCompaniesPanelProps) {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [exposures, setExposures] = useState<CompanyNodeExposure[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      try {
        setLoading(true);
        setError(null);
        const data = await getCompaniesByNode(nodeId);
        if (!cancelled) {
          setCompanies(data.companies);
          setExposures(data.exposures);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "加载失败");
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    load();
    return () => {
      cancelled = true;
    };
  }, [nodeId]);

  const exposureMap = new Map<string, CompanyNodeExposure[]>();
  exposures.forEach((e) => {
    const list = exposureMap.get(e.company_id) || [];
    list.push(e);
    exposureMap.set(e.company_id, list);
  });

  return (
    <div className="flex h-full flex-col bg-slate-900">
      <div className="flex items-center justify-between border-b border-slate-700 px-4 py-3">
        <div className="min-w-0">
          <h3 className="text-sm font-semibold text-slate-200">关联公司</h3>
          <p className="mt-0.5 truncate text-xs text-slate-400">{nodeName}</p>
        </div>
        <button
          onClick={onClose}
          className="rounded p-1 text-slate-400 hover:bg-slate-800 hover:text-slate-200"
        >
          <X size={16} />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-3">
        {loading && (
          <div className="flex items-center justify-center py-8">
            <Loader2 size={18} className="animate-spin text-slate-500" />
            <span className="ml-2 text-xs text-slate-400">加载中...</span>
          </div>
        )}
        {error && (
          <div className="rounded bg-red-900/20 p-3 text-xs text-red-400">
            {error}
          </div>
        )}
        {!loading && !error && companies.length === 0 && (
          <div className="py-8 text-center text-xs text-slate-500">
            暂无关联公司
          </div>
        )}
        {!loading &&
          companies.map((company) => {
            const exps = exposureMap.get(company.company_id) || [];
            return (
              <button
                key={company.company_id}
                onClick={() => onSelectCompany(company)}
                className="mb-2 flex w-full items-start gap-2 rounded border border-slate-700 bg-slate-800/50 p-2 text-left hover:border-slate-600 hover:bg-slate-800"
              >
                <Building2 size={14} className="mt-0.5 shrink-0 text-cyan-400" />
                <div className="min-w-0">
                  <div className="truncate text-xs font-medium text-slate-200">
                    {company.name_zh}
                  </div>
                  <div className="mt-1 flex flex-wrap gap-1">
                    {exps.map((e, i) => (
                      <span
                        key={i}
                        className="inline-block rounded bg-slate-700 px-1.5 py-0.5 text-[10px] text-slate-300"
                      >
                        {e.activity_type}
                        {e.weight !== 1.0 && ` · ${e.weight}`}
                      </span>
                    ))}
                  </div>
                </div>
              </button>
            );
          })}
      </div>
    </div>
  );
}
