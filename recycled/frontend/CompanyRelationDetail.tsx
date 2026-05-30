import { useEffect, useState } from "react";
import { X, ArrowRight, GitBranch } from "lucide-react";
import { getCompanyRelationPaths } from "@/services/api";
import type { CompanyRelationPath } from "@/services/api";

interface CompanyRelationDetailProps {
  fromCompanyId: string;
  toCompanyId: string;
  relationType?: string;
  relationSubtype?: string;
  pathCount?: number;
  onClose: () => void;
}

const RELATION_TYPE_LABELS: Record<string, string> = {
  inferred_industrial: "产业推断",
  evidenced_business: "业务关系",
  person_relation: "人事关联",
};

const SUBTYPE_LABELS: Record<string, string> = {
  upstream_of: "上游",
  downstream_of: "下游",
  supplier: "供应商",
  customer: "客户",
  partner: "合作伙伴",
  shareholder: "股东",
  executive: "高管",
};

export function CompanyRelationDetail({
  fromCompanyId,
  toCompanyId,
  relationType,
  relationSubtype,
  pathCount,
  onClose,
}: CompanyRelationDetailProps) {
  const [paths, setPaths] = useState<CompanyRelationPath[]>([]);
  const [fromName, setFromName] = useState(fromCompanyId);
  const [toName, setToName] = useState(toCompanyId);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    getCompanyRelationPaths(fromCompanyId, toCompanyId)
      .then((data) => {
        if (cancelled) return;
        setPaths(data.paths);
        setFromName(data.from_company_name);
        setToName(data.to_company_name);
      })
      .catch(() => {
        if (cancelled) return;
        setPaths([]);
      })
      .finally(() => {
        if (cancelled) return;
        setLoading(false);
      });
    return () => { cancelled = true; };
  }, [fromCompanyId, toCompanyId]);

  const typeLabel = RELATION_TYPE_LABELS[relationType || ""] || relationType || "关系";
  const subtypeLabel = SUBTYPE_LABELS[relationSubtype || ""] || relationSubtype || "";

  return (
    <div className="flex h-full flex-col bg-slate-900 text-slate-200">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-700 px-4 py-3">
        <div className="flex items-center gap-2">
          <GitBranch className="h-4 w-4 text-cyan-400" />
          <h3 className="text-sm font-semibold">关系依据</h3>
        </div>
        <button
          onClick={onClose}
          className="rounded p-1 text-slate-500 hover:bg-slate-800 hover:text-slate-300"
        >
          <X className="h-4 w-4" />
        </button>
      </div>

      {/* Relation summary */}
      <div className="border-b border-slate-700 px-4 py-3">
        <div className="mb-1 text-xs text-slate-500">关系类型</div>
        <div className="flex items-center gap-2">
          <span className="rounded bg-cyan-900/40 px-2 py-0.5 text-xs font-medium text-cyan-400">
            {typeLabel}
          </span>
          {subtypeLabel && (
            <span className="rounded bg-slate-800 px-2 py-0.5 text-xs text-slate-400">
              {subtypeLabel}
            </span>
          )}
          {typeof pathCount === "number" && (
            <span className="text-xs text-slate-500">({pathCount} 条路径)</span>
          )}
        </div>
        <div className="mt-2 flex items-center gap-2 text-sm">
          <span className="font-medium text-slate-300">{fromName}</span>
          <ArrowRight className="h-3 w-3 text-slate-500" />
          <span className="font-medium text-slate-300">{toName}</span>
        </div>
      </div>

      {/* Paths */}
      <div className="flex-1 overflow-auto px-4 py-3">
        {loading ? (
          <div className="text-xs text-slate-500">加载中...</div>
        ) : paths.length === 0 ? (
          <div className="text-xs text-slate-500">暂无路径数据</div>
        ) : (
          <div className="space-y-3">
            <div className="text-xs text-slate-500">
              以下产业流支撑了这条推断：
            </div>
            {paths.map((p, idx) => (
              <div
                key={idx}
                className="rounded border border-slate-700 bg-slate-800/50 p-3"
              >
                <div className="flex items-center gap-2 text-sm">
                  <span className="text-slate-300">{p.from_node.canonical_name_zh}</span>
                  <ArrowRight className="h-3 w-3 text-cyan-500" />
                  <span className="text-slate-300">{p.to_node.canonical_name_zh}</span>
                </div>
                <div className="mt-1 text-xs text-slate-500">
                  边类型: {p.edge_type}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
