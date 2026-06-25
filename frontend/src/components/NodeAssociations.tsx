import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ChevronDown, ChevronRight, Loader2, Building2, Factory, X, Plus, Search } from "lucide-react";
import { IndustrialNode, Company, Industry, GraphEdge, CompanyActivityType } from "@/types";
import {
  createCompanyExposure,
  createIndustryMapping,
  deleteIndustryMapping,
  getCompaniesByNode,
  getIndustriesByNode,
  listCompanies,
  listIndustries,
} from "@/services/api";
import { NodeEdgeList } from "./NodeEdgeList";

interface NodeAssociationsProps {
  node: IndustrialNode;
  onEdgeCreated?: (edge: GraphEdge) => void;
  onEdgeUpdated?: (edge: GraphEdge) => void;
  onEdgeDeleted?: (edgeId: string) => void;
  onSelectNode?: (node: IndustrialNode) => void;
  onSelectCompany?: (company: Company) => void;
  onSelectIndustry?: (industry: Industry) => void;
}

function CollapsibleSection({
  title,
  count,
  open,
  onToggle,
  children,
}: {
  title: string;
  count?: number;
  open: boolean;
  onToggle: () => void;
  children: React.ReactNode;
}) {
  return (
    <div className="rounded border border-slate-800 bg-slate-900/40">
      <button
        onClick={onToggle}
        className="flex w-full items-center justify-between px-3 py-2 text-left hover:bg-slate-800/50"
      >
        <span className="flex items-center gap-2 text-xs font-semibold text-slate-300">
          {title}
          {count !== undefined && (
            <span className="rounded bg-slate-800 px-1.5 py-0.5 text-[10px] text-slate-500">
              {count}
            </span>
          )}
        </span>
        {open ? (
          <ChevronDown className="h-3.5 w-3.5 text-slate-500" />
        ) : (
          <ChevronRight className="h-3.5 w-3.5 text-slate-500" />
        )}
      </button>
      {open && <div className="border-t border-slate-800 px-3 py-2">{children}</div>}
    </div>
  );
}

export function NodeAssociations({
  node,
  onEdgeCreated,
  onEdgeUpdated,
  onEdgeDeleted,
  onSelectNode,
  onSelectCompany,
  onSelectIndustry,
}: NodeAssociationsProps) {
  const queryClient = useQueryClient();
  const [relsOpen, setRelsOpen] = useState(true);
  const [companiesOpen, setCompaniesOpen] = useState(false);
  const [industriesOpen, setIndustriesOpen] = useState(false);

  // Quick-add industry mapping state
  const [showAddIndustry, setShowAddIndustry] = useState(false);
  const [industryQuery, setIndustryQuery] = useState("");
  const [selectedIndustry, setSelectedIndustry] = useState<Industry | null>(null);
  const [industryMappingId, setIndustryMappingId] = useState("");
  const [industryRole, setIndustryRole] = useState("");

  // Quick-add company exposure state
  const [showAddCompany, setShowAddCompany] = useState(false);
  const [companyQuery, setCompanyQuery] = useState("");
  const [selectedCompany, setSelectedCompany] = useState<Company | null>(null);
  const [exposureId, setExposureId] = useState("");
  const [activityType, setActivityType] = useState<CompanyActivityType>("manufacture");
  const [companyRole, setCompanyRole] = useState("");

  const removeMappingMutation = useMutation({
    mutationFn: ({ industryId, mappingId }: { industryId: string; mappingId: string }) =>
      deleteIndustryMapping(industryId, mappingId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["industries-by-node", node.node_id] });
    },
  });

  const {
    data: companiesData,
    isLoading: companiesLoading,
    error: companiesError,
  } = useQuery({
    queryKey: ["companies-by-node", node.node_id],
    queryFn: () => getCompaniesByNode(node.node_id),
    staleTime: 60_000,
  });

  const {
    data: industriesData,
    isLoading: industriesLoading,
    error: industriesError,
  } = useQuery({
    queryKey: ["industries-by-node", node.node_id],
    queryFn: () => getIndustriesByNode(node.node_id),
    staleTime: 60_000,
  });

  const companies = companiesData?.companies || [];
  const exposures = companiesData?.exposures || [];
  const industries = industriesData?.industries || [];
  const mappings = industriesData?.mappings || [];

  const { data: industrySearchData } = useQuery({
    queryKey: ["industries", 1, 10, undefined, undefined, industryQuery],
    queryFn: () => listIndustries(1, 10, undefined, undefined, industryQuery),
    enabled: industryQuery.length >= 1 && showAddIndustry,
  });

  const { data: companySearchData } = useQuery({
    queryKey: ["companies", 1, 10, undefined, undefined, undefined, companyQuery],
    queryFn: () => listCompanies(1, 10, undefined, undefined, undefined, companyQuery),
    enabled: companyQuery.length >= 1 && showAddCompany,
  });

  const createIndustryMappingMutation = useMutation({
    mutationFn: async () => {
      if (!selectedIndustry) throw new Error("请选择行业");
      if (!industryMappingId) throw new Error("请填写映射 ID");
      return createIndustryMapping(selectedIndustry.industry_id, {
        mapping_id: industryMappingId,
        industry_id: selectedIndustry.industry_id,
        node_id: node.node_id,
        role: industryRole || undefined,
        weight: 1.0,
        confidence: "MEDIUM",
        evidence: [],
        status: "ACTIVE",
      });
    },
    onSuccess: () => {
      setShowAddIndustry(false);
      setSelectedIndustry(null);
      setIndustryQuery("");
      setIndustryMappingId("");
      setIndustryRole("");
      queryClient.invalidateQueries({ queryKey: ["industries-by-node", node.node_id] });
    },
  });

  const createCompanyExposureMutation = useMutation({
    mutationFn: async () => {
      if (!selectedCompany) throw new Error("请选择公司");
      if (!exposureId) throw new Error("请填写暴露 ID");
      return createCompanyExposure(selectedCompany.company_id, {
        exposure_id: exposureId,
        company_id: selectedCompany.company_id,
        node_id: node.node_id,
        activity_type: activityType,
        role: companyRole || undefined,
        weight: 1.0,
        confidence: "MEDIUM",
        evidence: [],
        status: "ACTIVE",
      });
    },
    onSuccess: () => {
      setShowAddCompany(false);
      setSelectedCompany(null);
      setCompanyQuery("");
      setExposureId("");
      setCompanyRole("");
      queryClient.invalidateQueries({ queryKey: ["companies-by-node", node.node_id] });
    },
  });

  const handleSelectIndustry = (industry: Industry) => {
    setSelectedIndustry(industry);
    setIndustryMappingId(`${industry.industry_id}_contains_${node.node_id}`);
    setIndustryQuery("");
  };

  const handleSelectCompany = (company: Company) => {
    setSelectedCompany(company);
    setExposureId(`${company.company_id}_exposes_${node.node_id}`);
    setCompanyQuery("");
  };

  return (
    <div className="space-y-2">
      <CollapsibleSection
        title="关联关系"
        open={relsOpen}
        onToggle={() => setRelsOpen((v) => !v)}
      >
        <NodeEdgeList
          nodeId={node.node_id}
          onEdgeCreated={onEdgeCreated}
          onEdgeUpdated={onEdgeUpdated}
          onEdgeDeleted={onEdgeDeleted}
          onSelectNode={onSelectNode}
        />
      </CollapsibleSection>

      <CollapsibleSection
        title="关联公司"
        count={companies.length}
        open={companiesOpen}
        onToggle={() => setCompaniesOpen((v) => !v)}
      >
        {companiesLoading ? (
          <div className="flex items-center justify-center gap-2 py-4 text-xs text-slate-500">
            <Loader2 className="h-3.5 w-3.5 animate-spin" />
            加载关联公司...
          </div>
        ) : companiesError ? (
          <div className="py-2 text-xs text-red-400">加载失败</div>
        ) : companies.length === 0 ? (
          <div className="py-2 text-center text-[10px] text-slate-600">暂无关联公司</div>
        ) : (
          <div className="space-y-1.5">
            {companies.map((c) => {
              const exp = exposures.find((e) => e.company_id === c.company_id);
              return (
                <div
                  key={c.company_id}
                  className="flex items-start gap-2 rounded bg-slate-800/30 px-2 py-1.5"
                >
                  <Building2 className="mt-0.5 h-3 w-3 shrink-0 text-slate-500" />
                  <div className="min-w-0 flex-1">
                    {onSelectCompany ? (
                      <button
                        onClick={() => onSelectCompany(c)}
                        className="truncate text-xs text-cyan-400 hover:underline"
                        title={c.name_zh}
                      >
                        {c.name_zh}
                      </button>
                    ) : (
                      <div className="truncate text-xs text-slate-200" title={c.name_zh}>
                        {c.name_zh}
                      </div>
                    )}
                    <div className="mt-0.5 flex flex-wrap items-center gap-1.5 text-[10px] text-slate-500">
                      <span>{c.country}</span>
                      {exp && (
                        <>
                          <span>·</span>
                          <span>{exp.activity_type}</span>
                          {exp.role && <span>({exp.role})</span>}
                        </>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
        {!companiesLoading && !showAddCompany && (
          <button
            onClick={() => setShowAddCompany(true)}
            className="mt-2 flex w-full items-center justify-center gap-1 rounded border border-dashed border-slate-700 py-2 text-xs text-cyan-400 hover:border-cyan-600 hover:bg-cyan-900/10"
          >
            <Plus className="h-3.5 w-3.5" />
            关联到公司
          </button>
        )}
        {showAddCompany && (
          <form
            onSubmit={(e) => {
              e.preventDefault();
              createCompanyExposureMutation.mutate();
            }}
            className="mt-3 space-y-3 rounded border border-slate-700 bg-slate-800/30 p-3"
          >
            <div className="flex items-center justify-between">
              <h4 className="text-xs font-medium text-cyan-400">关联到公司</h4>
              <button
                type="button"
                onClick={() => {
                  setShowAddCompany(false);
                  setSelectedCompany(null);
                  setCompanyQuery("");
                  setExposureId("");
                  setCompanyRole("");
                  createCompanyExposureMutation.reset();
                }}
                className="rounded p-1 text-slate-500 hover:bg-slate-700"
              >
                <X className="h-3 w-3" />
              </button>
            </div>

            {createCompanyExposureMutation.error && (
              <div className="rounded bg-red-900/30 px-2 py-1.5 text-[11px] text-red-300">
                {createCompanyExposureMutation.error.message}
              </div>
            )}

            <div className="space-y-1">
              <label className="text-[10px] font-medium uppercase tracking-wider text-slate-500">
                选择公司
              </label>
              <div className="relative">
                <Search className="absolute left-2 top-1/2 h-3 w-3 -translate-y-1/2 text-slate-500" />
                <input
                  type="text"
                  value={selectedCompany ? selectedCompany.name_zh : companyQuery}
                  onChange={(e) => {
                    setCompanyQuery(e.target.value);
                    if (selectedCompany) setSelectedCompany(null);
                  }}
                  placeholder="搜索公司..."
                  className="w-full rounded border border-slate-700 bg-slate-800 py-1.5 pl-6 pr-2 text-xs text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
                />
                {companySearchData && companyQuery && !selectedCompany && (
                  <div className="absolute z-10 mt-1 max-h-32 w-full overflow-auto rounded border border-slate-700 bg-slate-800 shadow-lg">
                    {companySearchData.items.length === 0 ? (
                      <div className="px-2 py-1.5 text-xs text-slate-500">无结果</div>
                    ) : (
                      companySearchData.items.map((c) => (
                        <button
                          key={c.company_id}
                          type="button"
                          onClick={() => handleSelectCompany(c)}
                          className="flex w-full items-center gap-2 px-2 py-1.5 text-left text-xs hover:bg-slate-700"
                        >
                          <span className="font-medium text-slate-200">{c.name_zh}</span>
                          <span className="text-[10px] text-slate-500">{c.company_id}</span>
                        </button>
                      ))
                    )}
                  </div>
                )}
              </div>
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-medium uppercase tracking-wider text-slate-500">
                暴露 ID *
              </label>
              <input
                type="text"
                value={exposureId}
                onChange={(e) => setExposureId(e.target.value)}
                placeholder="例如 company_exposes_node"
                pattern="^[a-z][a-z0-9_]*$"
                minLength={3}
                maxLength={64}
                required
                className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
              />
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-medium uppercase tracking-wider text-slate-500">
                活动类型
              </label>
              <select
                value={activityType}
                onChange={(e) => setActivityType(e.target.value as CompanyActivityType)}
                className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
              >
                <option value="rnd">研发 (rnd)</option>
                <option value="design">设计 (design)</option>
                <option value="manufacture">制造 (manufacture)</option>
                <option value="produce">生产 (produce)</option>
                <option value="supply">供应 (supply)</option>
                <option value="distribute">分销 (distribute)</option>
                <option value="consume">消费 (consume)</option>
                <option value="service">服务 (service)</option>
                <option value="unknown">未知 (unknown)</option>
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-medium uppercase tracking-wider text-slate-500">
                角色
              </label>
              <input
                type="text"
                value={companyRole}
                onChange={(e) => setCompanyRole(e.target.value)}
                placeholder="例如 主要供应商"
                className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
              />
            </div>

            <div className="flex gap-2">
              <button
                type="submit"
                disabled={createCompanyExposureMutation.isPending}
                className="flex-1 rounded bg-cyan-600 py-1.5 text-xs font-medium text-white hover:bg-cyan-500 disabled:opacity-50"
              >
                {createCompanyExposureMutation.isPending ? "保存中..." : "关联"}
              </button>
              <button
                type="button"
                onClick={() => {
                  setShowAddCompany(false);
                  setSelectedCompany(null);
                  setCompanyQuery("");
                  setExposureId("");
                  setCompanyRole("");
                  createCompanyExposureMutation.reset();
                }}
                className="rounded border border-slate-700 bg-slate-800 px-3 py-1.5 text-xs text-slate-300 hover:bg-slate-700"
              >
                取消
              </button>
            </div>
          </form>
        )}
      </CollapsibleSection>

      <CollapsibleSection
        title="关联行业"
        count={industries.length}
        open={industriesOpen}
        onToggle={() => setIndustriesOpen((v) => !v)}
      >
        {industriesLoading ? (
          <div className="flex items-center justify-center gap-2 py-4 text-xs text-slate-500">
            <Loader2 className="h-3.5 w-3.5 animate-spin" />
            加载关联行业...
          </div>
        ) : industriesError ? (
          <div className="py-2 text-xs text-red-400">加载失败</div>
        ) : industries.length === 0 ? (
          <div className="py-2 text-center text-[10px] text-slate-600">暂无关联行业</div>
        ) : (
          <div className="space-y-1.5">
            {industries.map((ind) => (
              <div
                key={ind.industry_id}
                className="flex items-start gap-2 rounded bg-slate-800/30 px-2 py-1.5"
              >
                <Factory className="mt-0.5 h-3 w-3 shrink-0 text-slate-500" />
                <div className="min-w-0 flex-1">
                  {onSelectIndustry ? (
                    <button
                      onClick={() => onSelectIndustry(ind)}
                      className="truncate text-xs text-cyan-400 hover:underline"
                      title={ind.name_zh}
                    >
                      {ind.name_zh}
                    </button>
                  ) : (
                    <div className="truncate text-xs text-slate-200" title={ind.name_zh}>
                      {ind.name_zh}
                    </div>
                  )}
                  <div className="mt-0.5 text-[10px] text-slate-500">
                    {ind.industry_type} · {ind.status}
                  </div>
                </div>
                {mappings
                  .filter((m) => m.industry_id === ind.industry_id)
                  .map((m) => (
                    <button
                      key={m.mapping_id}
                      title="移除该行业映射"
                      disabled={removeMappingMutation.isPending}
                      onClick={(e) => {
                        e.stopPropagation();
                        if (confirm(`确定移除行业映射 ${m.mapping_id} 吗？`)) {
                          removeMappingMutation.mutate({ industryId: ind.industry_id, mappingId: m.mapping_id });
                        }
                      }}
                      className="ml-1 shrink-0 rounded p-1 text-slate-500 hover:bg-red-900/20 hover:text-red-400 disabled:opacity-50"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  ))}
              </div>
            ))}
          </div>
        )}
        {!industriesLoading && !showAddIndustry && (
          <button
            onClick={() => setShowAddIndustry(true)}
            className="mt-2 flex w-full items-center justify-center gap-1 rounded border border-dashed border-slate-700 py-2 text-xs text-cyan-400 hover:border-cyan-600 hover:bg-cyan-900/10"
          >
            <Plus className="h-3.5 w-3.5" />
            关联到新行业
          </button>
        )}
        {showAddIndustry && (
          <form
            onSubmit={(e) => {
              e.preventDefault();
              createIndustryMappingMutation.mutate();
            }}
            className="mt-3 space-y-3 rounded border border-slate-700 bg-slate-800/30 p-3"
          >
            <div className="flex items-center justify-between">
              <h4 className="text-xs font-medium text-cyan-400">关联到新行业</h4>
              <button
                type="button"
                onClick={() => {
                  setShowAddIndustry(false);
                  setSelectedIndustry(null);
                  setIndustryQuery("");
                  setIndustryMappingId("");
                  setIndustryRole("");
                  createIndustryMappingMutation.reset();
                }}
                className="rounded p-1 text-slate-500 hover:bg-slate-700"
              >
                <X className="h-3 w-3" />
              </button>
            </div>

            {createIndustryMappingMutation.error && (
              <div className="rounded bg-red-900/30 px-2 py-1.5 text-[11px] text-red-300">
                {createIndustryMappingMutation.error.message}
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
                value={industryMappingId}
                onChange={(e) => setIndustryMappingId(e.target.value)}
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
                value={industryRole}
                onChange={(e) => setIndustryRole(e.target.value)}
                placeholder="例如 核心产品、上游部件"
                className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
              />
            </div>

            <div className="flex gap-2">
              <button
                type="submit"
                disabled={createIndustryMappingMutation.isPending}
                className="flex-1 rounded bg-cyan-600 py-1.5 text-xs font-medium text-white hover:bg-cyan-500 disabled:opacity-50"
              >
                {createIndustryMappingMutation.isPending ? "保存中..." : "关联"}
              </button>
              <button
                type="button"
                onClick={() => {
                  setShowAddIndustry(false);
                  setSelectedIndustry(null);
                  setIndustryQuery("");
                  setIndustryMappingId("");
                  setIndustryRole("");
                  createIndustryMappingMutation.reset();
                }}
                className="rounded border border-slate-700 bg-slate-800 px-3 py-1.5 text-xs text-slate-300 hover:bg-slate-700"
              >
                取消
              </button>
            </div>
          </form>
        )}
      </CollapsibleSection>
    </div>
  );
}
