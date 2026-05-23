import { useEffect, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Loader2,
  Trash2,
  ChevronDown,
  ChevronRight,
  Sparkles,
  Network,
} from "lucide-react";
import {
  computeCompanySubgraph,
  deleteCompanySubgraph,
  getCompanySubgraphDetail,
  getComputationJob,
  listCompanySubgraphs,
} from "@/services/api";
import { CompanySubgraph } from "@/types";

interface CompanySubgraphPanelProps {
  companyId: string;
  onLoadSubgraph: (nodes: unknown[], edges: unknown[]) => void;
}

export function CompanySubgraphPanel({
  companyId,
  onLoadSubgraph,
}: CompanySubgraphPanelProps) {
  const queryClient = useQueryClient();
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [computingJobId, setComputingJobId] = useState<string | null>(null);
  const [computeProgress, setComputeProgress] = useState(0);
  const [showForm, setShowForm] = useState(false);
  const [versionName, setVersionName] = useState("");

  const { data: listData, isLoading: listLoading } = useQuery({
    queryKey: ["company-subgraphs", companyId],
    queryFn: () => listCompanySubgraphs(companyId),
  });

  const { data: detailData } = useQuery({
    queryKey: ["company-subgraph-detail", companyId, selectedId],
    queryFn: () =>
      selectedId ? getCompanySubgraphDetail(companyId, selectedId) : null,
    enabled: !!selectedId,
  });

  const computeMutation = useMutation({
    mutationFn: (name?: string) => computeCompanySubgraph(companyId, { version_name: name }),
    onSuccess: (data) => {
      setComputingJobId(data.job_id);
      setComputeProgress(0);
      setShowForm(false);
      setVersionName("");
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (subgraphId: string) => deleteCompanySubgraph(companyId, subgraphId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["company-subgraphs", companyId] });
      setSelectedId(null);
    },
  });

  // Poll job status
  useEffect(() => {
    if (!computingJobId) return;
    const interval = setInterval(async () => {
      try {
        const job = await getComputationJob(computingJobId);
        if (job.status === "completed") {
          setComputingJobId(null);
          setComputeProgress(100);
          queryClient.invalidateQueries({ queryKey: ["company-subgraphs", companyId] });
          clearInterval(interval);
        } else if (job.status === "failed") {
          setComputingJobId(null);
          alert("计算失败: " + (job.error_message || "未知错误"));
          clearInterval(interval);
        } else if (job.status === "running" && job.total_items && job.total_items > 0) {
          setComputeProgress(
            Math.min(100, Math.round((job.processed_items / job.total_items) * 100))
          );
        }
      } catch {
        // ignore poll errors
      }
    }, 1000);
    return () => clearInterval(interval);
  }, [computingJobId, companyId, queryClient]);

  const subgraphs = listData?.items ?? [];

  return (
    <div className="border-t border-slate-800 pt-3">
      <div className="mb-2 flex items-center justify-between">
        <h4 className="text-xs font-semibold text-slate-300">
          子图版本 ({listData?.total ?? 0})
        </h4>
        <button
          onClick={() => setShowForm((s) => !s)}
          disabled={!!computingJobId}
          className="flex items-center gap-1 rounded px-1.5 py-0.5 text-[10px] text-cyan-400 hover:bg-cyan-900/20 disabled:opacity-50"
        >
          {computingJobId ? (
            <Loader2 className="h-3 w-3 animate-spin" />
          ) : (
            <Sparkles className="h-3 w-3" />
          )}
          {computingJobId ? "计算中..." : "计算新版本"}
        </button>
      </div>

      {computingJobId && (
        <div className="mb-2">
          <div className="h-1.5 w-full overflow-hidden rounded-full bg-slate-800">
            <div
              className="h-full rounded-full bg-cyan-500 transition-all"
              style={{ width: `${computeProgress}%` }}
            />
          </div>
          <div className="mt-0.5 text-[10px] text-slate-500">{computeProgress}%</div>
        </div>
      )}

      {showForm && (
        <div className="mb-2 flex items-center gap-1">
          <input
            value={versionName}
            onChange={(e) => setVersionName(e.target.value)}
            placeholder="版本名称（可选）"
            className="flex-1 rounded border border-slate-700 bg-slate-800 px-2 py-1 text-[10px] text-slate-200 outline-none placeholder:text-slate-600"
          />
          <button
            onClick={() => computeMutation.mutate(versionName || undefined)}
            className="rounded bg-cyan-900/30 px-2 py-1 text-[10px] text-cyan-400 hover:bg-cyan-900/50"
          >
            确认
          </button>
        </div>
      )}

      {listLoading && (
        <div className="py-2 text-center text-xs text-slate-500">加载中...</div>
      )}

      <div className="space-y-1">
        {subgraphs.map((sg) => (
          <SubgraphVersionItem
            key={sg.subgraph_id}
            subgraph={sg}
            isSelected={selectedId === sg.subgraph_id}
            detail={detailData && selectedId === sg.subgraph_id ? detailData : null}
            onSelect={() => setSelectedId(sg.subgraph_id)}
            onLoad={() => {
              if (detailData && selectedId === sg.subgraph_id) {
                onLoadSubgraph(detailData.nodes, detailData.edges);
              }
            }}
            onDelete={() => {
              if (confirm("确定删除这个子图版本？")) {
                deleteMutation.mutate(sg.subgraph_id);
              }
            }}
          />
        ))}
        {subgraphs.length === 0 && !listLoading && (
          <div className="py-2 text-center text-xs text-slate-500">暂无子图版本</div>
        )}
      </div>
    </div>
  );
}

function SubgraphVersionItem({
  subgraph,
  isSelected,
  detail,
  onSelect,
  onLoad,
  onDelete,
}: {
  subgraph: CompanySubgraph;
  isSelected: boolean;
  detail: CompanySubgraph | null;
  onSelect: () => void;
  onLoad: () => void;
  onDelete: () => void;
}) {
  const ns = subgraph.nodes_summary;
  const es = subgraph.edges_summary;
  const rs = subgraph.relations_summary;

  return (
    <div className="rounded border border-slate-800 bg-slate-800/30">
      <button
        onClick={onSelect}
        className="flex w-full items-center gap-1.5 px-2 py-1.5 text-left"
      >
        {isSelected ? (
          <ChevronDown className="h-3 w-3 shrink-0 text-slate-500" />
        ) : (
          <ChevronRight className="h-3 w-3 shrink-0 text-slate-500" />
        )}
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-1.5">
            <span className="truncate text-xs font-medium text-slate-200">
              {subgraph.version_name || subgraph.subgraph_id}
            </span>
            <span className="shrink-0 rounded bg-slate-700 px-1 py-0 text-[9px] text-slate-400">
              {ns?.total ?? 0}节点 {es?.total ?? 0}边 {rs?.total ?? 0}关系
            </span>
          </div>
          <div className="text-[10px] text-slate-500">
            {subgraph.created_at
              ? new Date(subgraph.created_at).toLocaleString("zh-CN")
              : ""}
          </div>
        </div>
      </button>

      {isSelected && detail && (
        <div className="border-t border-slate-800 px-2 pb-2 pt-1.5">
          <div className="mb-2 flex items-center gap-1">
            <button
              onClick={onLoad}
              className="flex items-center gap-1 rounded bg-slate-700/50 px-1.5 py-0.5 text-[10px] text-cyan-400 hover:bg-slate-700"
            >
              <Network className="h-3 w-3" />
              加载到画布
            </button>
            <button
              onClick={onDelete}
              className="flex items-center gap-1 rounded bg-slate-700/50 px-1.5 py-0.5 text-[10px] text-red-400 hover:bg-slate-700"
            >
              <Trash2 className="h-3 w-3" />
              删除
            </button>
          </div>

          {detail.nodes.length > 0 && (
            <div className="mb-1.5">
              <div className="text-[10px] font-medium text-slate-400">节点</div>
              <div className="mt-0.5 flex flex-wrap gap-1">
                {detail.nodes.map((n) => (
                  <span
                    key={n.node_id}
                    className="inline-block rounded bg-slate-700/50 px-1.5 py-0.5 text-[10px] text-slate-300"
                  >
                    {n.canonical_name_zh || n.node_id}
                    <span className="ml-1 text-slate-500">({n.activity_type})</span>
                  </span>
                ))}
              </div>
            </div>
          )}

          {detail.edges.length > 0 && (
            <div className="mb-1.5">
              <div className="text-[10px] font-medium text-slate-400">边</div>
              <div className="mt-0.5 space-y-0.5">
                {detail.edges.map((e) => (
                  <div key={e.edge_id} className="text-[10px] text-slate-400">
                    {e.from_node} → {e.to_node}{" "}
                    <span className="text-slate-500">({e.edge_type_label || e.edge_type})</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {detail.relations.length > 0 && (
            <div>
              <div className="text-[10px] font-medium text-slate-400">关系</div>
              <div className="mt-0.5 space-y-0.5">
                {detail.relations.map((rel) => (
                  <div key={`${rel.from_company_id}-${rel.to_company_id}-${rel.relation_type}`} className="text-[10px] text-slate-400">
                    {rel.from_company_id} → {rel.to_company_id}{" "}
                    <span className="text-slate-500">({rel.relation_subtype || rel.relation_type})</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
