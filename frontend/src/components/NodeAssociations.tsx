import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ChevronDown, ChevronRight, Loader2, Building2, Factory, X } from "lucide-react";
import { IndustrialNode, Company, Industry } from "@/types";
import { deleteIndustryMapping, getCompaniesByNode, getIndustriesByNode } from "@/services/api";
import { NodeEdgeList } from "./NodeEdgeList";

interface NodeAssociationsProps {
  node: IndustrialNode;
  onRefreshGraph: () => void;
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
  onRefreshGraph,
  onSelectNode,
  onSelectCompany,
  onSelectIndustry,
}: NodeAssociationsProps) {
  const queryClient = useQueryClient();
  const [relsOpen, setRelsOpen] = useState(true);
  const [companiesOpen, setCompaniesOpen] = useState(false);
  const [industriesOpen, setIndustriesOpen] = useState(false);

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
    enabled: companiesOpen,
    staleTime: 60_000,
  });

  const {
    data: industriesData,
    isLoading: industriesLoading,
    error: industriesError,
  } = useQuery({
    queryKey: ["industries-by-node", node.node_id],
    queryFn: () => getIndustriesByNode(node.node_id),
    enabled: industriesOpen,
    staleTime: 60_000,
  });

  const companies = companiesData?.companies || [];
  const exposures = companiesData?.exposures || [];
  const industries = industriesData?.industries || [];
  const mappings = industriesData?.mappings || [];

  return (
    <div className="space-y-2">
      <CollapsibleSection
        title="关联关系"
        open={relsOpen}
        onToggle={() => setRelsOpen((v) => !v)}
      >
        <NodeEdgeList
          nodeId={node.node_id}
          onRefreshGraph={onRefreshGraph}
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
      </CollapsibleSection>
    </div>
  );
}
