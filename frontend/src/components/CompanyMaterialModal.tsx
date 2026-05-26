import { useState, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { X, Users, ArrowUp, ArrowDown, Link2, Check } from "lucide-react";
import { getMaterialConnections } from "@/services/api";

interface CNode {
  company_id: string;
  name_zh: string;
  company_type: string;
  status: string;
}

interface CEdge {
  from_company_id: string;
  to_company_id: string;
  path_count: number;
  strength: number;
  confidence: string;
  relation_type?: string;
  relation_subtype?: string;
}

interface SelectedCompany {
  company_id: string;
  name_zh: string;
  via_node_id: string;
  via_node_name: string;
  direction: "peer" | "upstream" | "downstream";
  activity_type: string;
}

interface CompanyMaterialModalProps {
  companyId: string;
  companyName: string;
  isOpen: boolean;
  onClose: () => void;
  onAddToView: (nodes: CNode[], edges: CEdge[]) => void;
}

export function CompanyMaterialModal({
  companyId,
  companyName,
  isOpen,
  onClose,
  onAddToView,
}: CompanyMaterialModalProps) {
  const { data, isLoading } = useQuery({
    queryKey: ["material-connections", companyId],
    queryFn: () => getMaterialConnections(companyId),
    enabled: isOpen,
  });

  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [selected, setSelected] = useState<Map<string, SelectedCompany>>(new Map());

  const exposures = data?.exposures ?? [];

  const activeExposure = useMemo(
    () => exposures.find((e) => e.node_id === selectedNodeId),
    [exposures, selectedNodeId]
  );

  if (!isOpen) return null;

  const toggleCompany = (
    company_id: string,
    name_zh: string,
    via_node_id: string,
    via_node_name: string,
    direction: "peer" | "upstream" | "downstream",
    activity_type: string
  ) => {
    setSelected((prev) => {
      const next = new Map(prev);
      const key = `${company_id}:${via_node_id}:${direction}`;
      if (next.has(key)) {
        next.delete(key);
      } else {
        next.set(key, { company_id, name_zh, via_node_id, via_node_name, direction, activity_type });
      }
      return next;
    });
  };

  const handleAddToView = () => {
    const nodes: CNode[] = [];
    const nodeIds = new Set<string>();
    const edges: CEdge[] = [];

    selected.forEach((item) => {
      if (!nodeIds.has(item.company_id)) {
        nodes.push({
          company_id: item.company_id,
          name_zh: item.name_zh,
          company_type: "unknown",
          status: "ACTIVE",
        });
        nodeIds.add(item.company_id);
      }

      // Create edge from anchor to selected company
      // direction determines the edge direction
      const edge: CEdge =
        item.direction === "upstream"
          ? {
              from_company_id: item.company_id,
              to_company_id: companyId,
              path_count: 1,
              strength: 0.5,
              confidence: "MEDIUM",
              relation_type: "inferred_industrial",
              relation_subtype: `via_${item.via_node_id}`,
            }
          : item.direction === "downstream"
            ? {
                from_company_id: companyId,
                to_company_id: item.company_id,
                path_count: 1,
                strength: 0.5,
                confidence: "MEDIUM",
                relation_type: "inferred_industrial",
                relation_subtype: `via_${item.via_node_id}`,
              }
            : {
                // peer: bidirectional or undirectional, use a weak edge both ways
                from_company_id: companyId,
                to_company_id: item.company_id,
                path_count: 1,
                strength: 0.3,
                confidence: "MEDIUM",
                relation_type: "similarity_or_peer",
                relation_subtype: `peer_via_${item.via_node_id}`,
              };
      edges.push(edge);
    });

    onAddToView(nodes, edges);
    onClose();
  };

  const renderCompanyList = (
    items: { company_id: string; name_zh: string; activity_type: string; weight: number; node_id?: string; node_name?: string }[],
    direction: "peer" | "upstream" | "downstream"
  ) => {
    if (items.length === 0) {
      return <div className="py-4 text-center text-xs text-slate-500">暂无数据</div>;
    }
    return (
      <div className="space-y-1">
        {items.map((item) => {
          const via_node_id = item.node_id ?? activeExposure?.node_id ?? "";
          const via_node_name = item.node_name ?? activeExposure?.node_name ?? "";
          const key = `${item.company_id}:${via_node_id}:${direction}`;
          const isChecked = selected.has(key);
          return (
            <label
              key={key}
              className={`flex cursor-pointer items-center gap-2 rounded px-2 py-1.5 transition-colors ${isChecked ? "bg-cyan-900/20" : "hover:bg-slate-800"}`}
            >
              <input
                type="checkbox"
                checked={isChecked}
                onChange={() =>
                  toggleCompany(
                    item.company_id,
                    item.name_zh,
                    via_node_id,
                    via_node_name,
                    direction,
                    item.activity_type
                  )
                }
                className="h-3.5 w-3.5 rounded border-slate-600 bg-slate-800 text-cyan-500 focus:ring-cyan-500"
              />
              <span className="flex-1 text-xs text-slate-200">{item.name_zh}</span>
              <span className="text-[10px] text-slate-500">{item.activity_type}</span>
              {item.weight !== undefined && (
                <span className="text-[10px] text-slate-600">{(item.weight * 100).toFixed(0)}%</span>
              )}
            </label>
          );
        })}
      </div>
    );
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm">
      <div className="flex h-[85vh] w-[90vw] max-w-5xl flex-col overflow-hidden rounded-lg border border-slate-700 bg-slate-900 shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-700 px-5 py-3">
          <div className="flex items-center gap-2">
            <Link2 className="h-4 w-4 text-cyan-400" />
            <h2 className="text-sm font-semibold text-slate-100">
              物料关联探索：<span className="text-cyan-400">{companyName}</span>
            </h2>
          </div>
          <button
            onClick={onClose}
            className="flex h-7 w-7 items-center justify-center rounded text-slate-400 hover:bg-slate-800 hover:text-slate-200"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        {/* Body */}
        <div className="flex flex-1 overflow-hidden">
          {/* Left: Material List */}
          <div className="w-64 border-r border-slate-700 bg-slate-900/50">
            <div className="px-3 py-2 text-[10px] font-medium uppercase tracking-wider text-slate-500">
              暴露物料 ({exposures.length})
            </div>
            {isLoading ? (
              <div className="px-3 py-4 text-xs text-slate-500">加载中...</div>
            ) : exposures.length === 0 ? (
              <div className="px-3 py-4 text-xs text-slate-500">该公司暂无产业暴露</div>
            ) : (
              <div className="space-y-0.5 px-2">
                {exposures.map((exp) => {
                  const isActive = selectedNodeId === exp.node_id;
                  const hasPeers = exp.peers.length;
                  const hasUp = exp.upstream.length;
                  const hasDown = exp.downstream.length;
                  const total = hasPeers + hasUp + hasDown;
                  return (
                    <button
                      key={exp.node_id}
                      onClick={() => {
                        setSelectedNodeId(exp.node_id);
                      }}
                      className={`w-full rounded px-2.5 py-2 text-left transition-colors ${
                        isActive ? "bg-slate-800" : "hover:bg-slate-800/50"
                      }`}
                    >
                      <div className="text-xs font-medium text-slate-200">{exp.node_name}</div>
                      <div className="mt-0.5 flex items-center gap-2 text-[10px] text-slate-500">
                        <span>{exp.activity_type}</span>
                        {total > 0 && <span className="text-cyan-500">{total} 关联</span>}
                      </div>
                    </button>
                  );
                })}
              </div>
            )}
          </div>

          {/* Right: Connection Details */}
          <div className="flex-1 overflow-y-auto bg-slate-950/30">
            {!activeExposure ? (
              <div className="flex h-full items-center justify-center text-xs text-slate-500">
                左侧选择一个物料查看关联公司
              </div>
            ) : (
              <div className="space-y-4 p-4">
                {/* Peers */}
                <div className="rounded border border-slate-800">
                  <div className="flex items-center gap-1.5 border-b border-slate-800 bg-slate-800/30 px-3 py-2">
                    <Users className="h-3.5 w-3.5 text-purple-400" />
                    <span className="text-xs font-medium text-slate-200">同行公司</span>
                    <span className="ml-auto text-[10px] text-slate-500">{activeExposure.peers.length}</span>
                  </div>
                  <div className="p-2">
                    {renderCompanyList(activeExposure.peers, "peer")}
                  </div>
                </div>

                {/* Upstream */}
                <div className="rounded border border-slate-800">
                  <div className="flex items-center gap-1.5 border-b border-slate-800 bg-slate-800/30 px-3 py-2">
                    <ArrowUp className="h-3.5 w-3.5 text-amber-400" />
                    <span className="text-xs font-medium text-slate-200">上游供应商</span>
                    <span className="ml-auto text-[10px] text-slate-500">{activeExposure.upstream.length}</span>
                  </div>
                  <div className="p-2">
                    {renderCompanyList(activeExposure.upstream, "upstream")}
                  </div>
                </div>

                {/* Downstream */}
                <div className="rounded border border-slate-800">
                  <div className="flex items-center gap-1.5 border-b border-slate-800 bg-slate-800/30 px-3 py-2">
                    <ArrowDown className="h-3.5 w-3.5 text-emerald-400" />
                    <span className="text-xs font-medium text-slate-200">下游客户</span>
                    <span className="ml-auto text-[10px] text-slate-500">{activeExposure.downstream.length}</span>
                  </div>
                  <div className="p-2">
                    {renderCompanyList(activeExposure.downstream, "downstream")}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between border-t border-slate-700 px-5 py-3">
          <div className="text-xs text-slate-400">
            已选择 <span className="font-medium text-cyan-400">{selected.size}</span> 家公司
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setSelected(new Map())}
              className="rounded px-3 py-1.5 text-xs text-slate-400 hover:bg-slate-800 hover:text-slate-200"
            >
              清空
            </button>
            <button
              onClick={handleAddToView}
              disabled={selected.size === 0}
              className="flex items-center gap-1 rounded bg-cyan-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-cyan-500 disabled:cursor-not-allowed disabled:opacity-40"
            >
              <Check className="h-3 w-3" />
              添加到视图
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
