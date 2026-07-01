import { useEffect, useRef, useState } from "react";
import {
  Building2,
  CheckSquare,
  ChevronDown,
  ChevronUp,
  GripVertical,
  Info,
  Loader2,
  Square,
  X,
} from "lucide-react";
import { Company, CompanyNodeExposure, IndustrialNode } from "@/types";
import { getCompaniesByNodes } from "@/services/api";

interface CompanyFilterPanelProps {
  nodes: IndustrialNode[];
  visible: boolean;
  onClose: () => void;
  onHighlightNodes: (nodeIds: string[]) => void;
  onViewCompanyDetail?: (company: Company) => void;
}

export function CompanyFilterPanel({
  nodes,
  visible,
  onClose,
  onHighlightNodes,
  onViewCompanyDetail,
}: CompanyFilterPanelProps) {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [exposures, setExposures] = useState<CompanyNodeExposure[]>([]);
  const [checkedCompanyIds, setCheckedCompanyIds] = useState<Set<string>>(
    new Set()
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [collapsed, setCollapsed] = useState(false);
  const [position, setPosition] = useState<{ x: number; y: number }>(() => {
    const width = 288; // w-72
    const margin = 16;
    const x =
      typeof window !== "undefined"
        ? Math.max(margin, window.innerWidth - width - margin)
        : margin;
    return { x, y: 80 };
  });
  const draggingRef = useRef(false);
  const dragOffsetRef = useRef<{ x: number; y: number }>({ x: 0, y: 0 });
  const panelRef = useRef<HTMLDivElement>(null);

  const nodeIds = nodes.map((n) => n.node_id);

  // Load companies whenever the filtered node set changes.
  useEffect(() => {
    let cancelled = false;
    async function load() {
      if (nodeIds.length === 0) {
        setCompanies([]);
        setExposures([]);
        setCheckedCompanyIds(new Set());
        onHighlightNodes([]);
        return;
      }
      try {
        setLoading(true);
        setError(null);
        const data = await getCompaniesByNodes(nodeIds);
        if (!cancelled) {
          setCompanies(data.companies);
          setExposures(data.exposures);
          // Default: no companies selected; user checks to highlight nodes.
          setCheckedCompanyIds(new Set());
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
  }, [nodeIds.join(","), onHighlightNodes]);

  // Recompute highlight whenever checked companies or exposures change.
  useEffect(() => {
    const nodeIdsToHighlight = new Set<string>();
    exposures.forEach((e) => {
      if (checkedCompanyIds.has(e.company_id)) {
        nodeIdsToHighlight.add(e.node_id);
      }
    });
    onHighlightNodes(Array.from(nodeIdsToHighlight));
  }, [checkedCompanyIds, exposures, onHighlightNodes]);

  const handleMouseDown = (e: React.MouseEvent) => {
    if (!panelRef.current) return;
    draggingRef.current = true;
    const rect = panelRef.current.getBoundingClientRect();
    dragOffsetRef.current = {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    };

    const handleMouseMove = (ev: MouseEvent) => {
      if (!draggingRef.current) return;
      setPosition({
        x: ev.clientX - dragOffsetRef.current.x,
        y: ev.clientY - dragOffsetRef.current.y,
      });
    };

    const handleMouseUp = () => {
      draggingRef.current = false;
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };

    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);
  };

  const toggleCompany = (companyId: string) => {
    setCheckedCompanyIds((prev) => {
      const next = new Set(prev);
      if (next.has(companyId)) {
        next.delete(companyId);
      } else {
        next.add(companyId);
      }
      return next;
    });
  };

  const checkAll = () => {
    setCheckedCompanyIds(new Set(companies.map((c) => c.company_id)));
  };

  const uncheckAll = () => {
    setCheckedCompanyIds(new Set());
  };

  const nodeNameMap = new Map<string, string>();
  nodes.forEach((n) => nodeNameMap.set(n.node_id, n.canonical_name_zh));

  if (!visible) return null;

  const dragHandle = (
    <div
      className="flex cursor-move items-center gap-2"
      onMouseDown={handleMouseDown}
    >
      <GripVertical size={14} className="text-slate-500" />
      <Building2 size={14} className="text-cyan-400" />
      <div>
        <div className="flex items-center gap-1.5">
          <h3 className="text-sm font-semibold text-slate-200">关联公司</h3>
          <span className="text-xs text-slate-500">({companies.length})</span>
        </div>
        <p className="text-[10px] leading-none text-slate-500">
          {nodes.length} 个选中节点
        </p>
      </div>
    </div>
  );

  if (collapsed) {
    return (
      <div
        ref={panelRef}
        className="fixed z-30 flex items-center justify-between gap-3 rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 shadow-xl"
        style={{ left: position.x, top: position.y }}
      >
        {dragHandle}
        <div className="flex items-center gap-1">
          <button
            onClick={() => setCollapsed(false)}
            className="rounded p-1 text-slate-400 hover:bg-slate-800 hover:text-slate-200"
            title="展开"
          >
            <ChevronUp size={14} />
          </button>
          <button
            onClick={onClose}
            className="rounded p-1 text-slate-400 hover:bg-slate-800 hover:text-slate-200"
            title="关闭"
          >
            <X size={14} />
          </button>
        </div>
      </div>
    );
  }

  const exposureMap = new Map<string, CompanyNodeExposure[]>();
  exposures.forEach((e) => {
    const list = exposureMap.get(e.company_id) || [];
    list.push(e);
    exposureMap.set(e.company_id, list);
  });

  return (
    <div
      ref={panelRef}
      className="fixed z-30 flex w-72 flex-col rounded-lg border border-slate-700 bg-slate-900 shadow-xl"
      style={{ left: position.x, top: position.y, maxHeight: "calc(100vh - 120px)" }}
    >
      <div className="flex items-center justify-between border-b border-slate-700 px-3 py-2">
        {dragHandle}
        <div className="flex items-center gap-1">
          <button
            onClick={() => setCollapsed(true)}
            className="rounded p-1 text-slate-400 hover:bg-slate-800 hover:text-slate-200"
            title="折叠"
          >
            <ChevronDown size={14} />
          </button>
          <button
            onClick={onClose}
            className="rounded p-1 text-slate-400 hover:bg-slate-800 hover:text-slate-200"
            title="关闭"
          >
            <X size={14} />
          </button>
        </div>
      </div>

      <div className="flex items-center justify-between border-b border-slate-800 px-3 py-1.5">
        <span className="text-[10px] text-slate-500">
          已选 {checkedCompanyIds.size}/{companies.length} 家公司
        </span>
        <div className="flex items-center gap-2">
          <button
            onClick={checkAll}
            className="text-[10px] text-cyan-400 hover:text-cyan-300"
          >
            全选
          </button>
          <button
            onClick={uncheckAll}
            className="text-[10px] text-slate-400 hover:text-slate-300"
          >
            取消
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-3">
        {nodes.length === 0 && (
          <div className="py-4 text-center text-xs text-slate-500">
            右键节点 → 查看关联公司 以加载
          </div>
        )}

        {loading && (
          <div className="flex items-center justify-center py-6">
            <Loader2 size={16} className="animate-spin text-slate-500" />
            <span className="ml-2 text-xs text-slate-400">加载中...</span>
          </div>
        )}
        {error && (
          <div className="rounded bg-red-900/20 p-2 text-xs text-red-400">
            {error}
          </div>
        )}
        {!loading && !error && companies.length === 0 && nodes.length > 0 && (
          <div className="py-6 text-center text-xs text-slate-500">
            暂无关联公司
          </div>
        )}
        {!loading &&
          !error &&
          companies.map((company) => {
            const exps = exposureMap.get(company.company_id) || [];
            const checked = checkedCompanyIds.has(company.company_id);
            return (
              <div
                key={company.company_id}
                onClick={() => toggleCompany(company.company_id)}
                className={`mb-2 flex w-full cursor-pointer items-start gap-2 rounded border p-2 text-left ${
                  checked
                    ? "border-slate-600 bg-slate-800"
                    : "border-slate-700 bg-slate-800/50 opacity-70"
                }`}
              >
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    toggleCompany(company.company_id);
                  }}
                  className="mt-0.5 shrink-0 text-slate-300 hover:text-slate-100"
                >
                  {checked ? (
                    <CheckSquare size={14} className="text-cyan-400" />
                  ) : (
                    <Square size={14} />
                  )}
                </button>
                <div className="min-w-0 flex-1">
                  <div className="truncate text-xs font-medium text-slate-200">
                    {company.name_zh}
                  </div>
                  <div className="mt-1 flex flex-wrap gap-1">
                    {exps.map((e, i) => (
                      <span
                        key={i}
                        className="inline-block rounded bg-slate-700 px-1.5 py-0.5 text-[10px] text-slate-300"
                      >
                        {nodeNameMap.get(e.node_id) || e.node_id}
                        {e.activity_type && ` · ${e.activity_type}`}
                        {e.weight !== 1.0 && ` · ${e.weight}`}
                      </span>
                    ))}
                  </div>
                </div>
                {onViewCompanyDetail && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onViewCompanyDetail(company);
                    }}
                    title="查看公司详情"
                    className="shrink-0 rounded p-1 text-slate-400 hover:bg-slate-700 hover:text-slate-200"
                  >
                    <Info size={14} />
                  </button>
                )}
              </div>
            );
          })}
      </div>
    </div>
  );
}
