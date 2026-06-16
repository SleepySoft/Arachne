import { useEffect, useState } from "react";
import { Factory, Loader2, Plus, Search, X } from "lucide-react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Industry, IndustryNodeMapping } from "@/types";
import { createIndustryMapping, getIndustriesByNode, listIndustries } from "@/services/api";

interface NodeIndustriesPanelProps {
  nodeId: string;
  nodeName: string;
  onClose: () => void;
  onSelectIndustry: (industry: Industry) => void;
}

export function NodeIndustriesPanel({
  nodeId,
  nodeName,
  onClose,
  onSelectIndustry,
}: NodeIndustriesPanelProps) {
  const queryClient = useQueryClient();
  const [industries, setIndustries] = useState<Industry[]>([]);
  const [mappings, setMappings] = useState<IndustryNodeMapping[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [industryQuery, setIndustryQuery] = useState("");
  const [selectedIndustry, setSelectedIndustry] = useState<Industry | null>(null);
  const [mappingId, setMappingId] = useState("");
  const [role, setRole] = useState("");
  const [formError, setFormError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      try {
        setLoading(true);
        setError(null);
        const data = await getIndustriesByNode(nodeId);
        if (!cancelled) {
          setIndustries(data.industries);
          setMappings(data.mappings);
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

  const { data: industrySearchData } = useQuery({
    queryKey: ["industries", 1, 10, undefined, undefined, industryQuery],
    queryFn: () => listIndustries(1, 10, undefined, undefined, industryQuery),
    enabled: industryQuery.length >= 1 && showAddForm,
  });

  const createMappingMutation = useMutation({
    mutationFn: async () => {
      if (!selectedIndustry) throw new Error("请选择行业");
      if (!mappingId) throw new Error("请填写映射 ID");
      return createIndustryMapping(selectedIndustry.industry_id, {
        mapping_id: mappingId,
        industry_id: selectedIndustry.industry_id,
        node_id: nodeId,
        role: role || undefined,
        weight: 1.0,
        confidence: "MEDIUM",
        evidence: [],
        status: "ACTIVE",
      });
    },
    onSuccess: async () => {
      setShowAddForm(false);
      setSelectedIndustry(null);
      setIndustryQuery("");
      setMappingId("");
      setRole("");
      setFormError(null);
      queryClient.invalidateQueries({ queryKey: ["industries-by-node"] });
      try {
        const data = await getIndustriesByNode(nodeId);
        setIndustries(data.industries);
        setMappings(data.mappings);
      } catch (err) {
        setError(err instanceof Error ? err.message : "刷新失败");
      }
    },
    onError: (err: Error) => setFormError(err.message),
  });

  const mappingMap = new Map<string, IndustryNodeMapping[]>();
  mappings.forEach((m) => {
    const list = mappingMap.get(m.industry_id) || [];
    list.push(m);
    mappingMap.set(m.industry_id, list);
  });

  const handleSelectIndustry = (industry: Industry) => {
    setSelectedIndustry(industry);
    setMappingId(`${industry.industry_id}_contains_${nodeId}`);
    setIndustryQuery("");
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);
    createMappingMutation.mutate();
  };

  return (
    <div className="flex h-full flex-col bg-slate-900">
      <div className="flex items-center justify-between border-b border-slate-700 px-4 py-3">
        <div className="min-w-0">
          <h3 className="text-sm font-semibold text-slate-200">关联行业</h3>
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
        {!loading && !error && industries.length === 0 && (
          <div className="py-8 text-center text-xs text-slate-500">
            暂无关联行业
          </div>
        )}
        {!loading &&
          !error &&
          industries.map((industry) => {
            const maps = mappingMap.get(industry.industry_id) || [];
            return (
              <button
                key={industry.industry_id}
                onClick={() => onSelectIndustry(industry)}
                className="mb-2 flex w-full items-start gap-2 rounded border border-slate-700 bg-slate-800/50 p-2 text-left hover:border-slate-600 hover:bg-slate-800"
              >
                <Factory size={14} className="mt-0.5 shrink-0 text-amber-400" />
                <div className="min-w-0">
                  <div className="truncate text-xs font-medium text-slate-200">
                    {industry.name_zh}
                  </div>
                  <div className="mt-1 flex flex-wrap gap-1">
                    {maps.map((m, i) => (
                      <span
                        key={i}
                        className="inline-block rounded bg-slate-700 px-1.5 py-0.5 text-[10px] text-slate-300"
                      >
                        {m.role || "关联"}
                        {m.weight !== 1.0 && ` · ${m.weight}`}
                      </span>
                    ))}
                  </div>
                </div>
              </button>
            );
          })}

        {!showAddForm && (
          <button
            onClick={() => setShowAddForm(true)}
            className="mt-2 flex w-full items-center justify-center gap-1 rounded border border-dashed border-slate-700 py-2 text-xs text-cyan-400 hover:border-cyan-600 hover:bg-cyan-900/10"
          >
            <Plus size={14} />
            关联到新行业
          </button>
        )}

        {showAddForm && (
          <form onSubmit={handleSubmit} className="mt-3 space-y-3 rounded border border-slate-700 bg-slate-800/30 p-3">
            <div className="flex items-center justify-between">
              <h4 className="text-xs font-medium text-cyan-400">关联到新行业</h4>
              <button
                type="button"
                onClick={() => {
                  setShowAddForm(false);
                  setSelectedIndustry(null);
                  setIndustryQuery("");
                  setFormError(null);
                }}
                className="rounded p-1 text-slate-500 hover:bg-slate-700"
              >
                <X size={14} />
              </button>
            </div>

            {formError && (
              <div className="rounded bg-red-900/30 px-2 py-1.5 text-[11px] text-red-300">
                {formError}
              </div>
            )}

            <div className="space-y-1">
              <label className="text-[10px] font-medium uppercase tracking-wider text-slate-500">
                选择行业
              </label>
              <div className="relative">
                <Search className="absolute left-2 top-1/2 h-3 w-3 -translate-y-1/2 text-slate-500" />
                <input
                  type="text"
                  value={selectedIndustry ? selectedIndustry.name_zh : industryQuery}
                  onChange={(e) => {
                    setIndustryQuery(e.target.value);
                    if (selectedIndustry) setSelectedIndustry(null);
                  }}
                  placeholder="搜索行业..."
                  className="w-full rounded border border-slate-700 bg-slate-800 py-1.5 pl-6 pr-2 text-xs text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
                />
                {industrySearchData && industryQuery && !selectedIndustry && (
                  <div className="absolute z-10 mt-1 max-h-32 w-full overflow-auto rounded border border-slate-700 bg-slate-800 shadow-lg">
                    {industrySearchData.items.length === 0 ? (
                      <div className="px-2 py-1.5 text-xs text-slate-500">无结果</div>
                    ) : (
                      industrySearchData.items.map((ind) => (
                        <button
                          key={ind.industry_id}
                          type="button"
                          onClick={() => handleSelectIndustry(ind)}
                          className="flex w-full items-center gap-2 px-2 py-1.5 text-left text-xs hover:bg-slate-700"
                        >
                          <span className="font-medium text-slate-200">{ind.name_zh}</span>
                          <span className="text-[10px] text-slate-500">{ind.industry_id}</span>
                        </button>
                      ))
                    )}
                  </div>
                )}
              </div>
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-medium uppercase tracking-wider text-slate-500">
                映射 ID *
              </label>
              <input
                type="text"
                value={mappingId}
                onChange={(e) => setMappingId(e.target.value)}
                placeholder="例如 industry_contains_node"
                pattern="^[a-z][a-z0-9_]*$"
                minLength={3}
                maxLength={64}
                required
                className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
              />
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-medium uppercase tracking-wider text-slate-500">
                角色
              </label>
              <input
                type="text"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                placeholder="例如 核心产品、上游部件"
                className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
              />
            </div>

            <div className="flex gap-2">
              <button
                type="submit"
                disabled={createMappingMutation.isPending}
                className="flex-1 rounded bg-cyan-600 py-1.5 text-xs font-medium text-white hover:bg-cyan-500 disabled:opacity-50"
              >
                {createMappingMutation.isPending ? "保存中..." : "关联"}
              </button>
              <button
                type="button"
                onClick={() => {
                  setShowAddForm(false);
                  setSelectedIndustry(null);
                  setIndustryQuery("");
                  setFormError(null);
                }}
                className="rounded border border-slate-700 bg-slate-800 px-3 py-1.5 text-xs text-slate-300 hover:bg-slate-700"
              >
                取消
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
