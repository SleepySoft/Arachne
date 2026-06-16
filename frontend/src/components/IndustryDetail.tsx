import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Edit2, Trash2, X, Link2, Plus, Crosshair } from "lucide-react";
import { Industry, IndustryNodeMapping } from "@/types";
import {
  deleteIndustry,
  deleteIndustryMapping,
  getIndustrySubgraph,
  listIndustryMappings,
} from "@/services/api";
import { IndustryMappingForm } from "./IndustryMappingForm";

interface IndustryDetailProps {
  industry: Industry;
  onEdit: () => void;
  onClose: () => void;
  onRefresh: () => void;
  onLoadSubgraph: (nodes: unknown[], edges: unknown[]) => void;
  onHighlightNodes: (nodeIds: string[]) => void;
}

function Field({ label, value, badge }: { label: string; value?: string | number | null; badge?: boolean }) {
  if (value === undefined || value === null || value === "") return null;
  return (
    <div className="flex flex-col gap-0.5">
      <span className="text-[10px] font-medium uppercase tracking-wider text-slate-500">{label}</span>
      {badge ? (
        <span className="w-fit rounded bg-slate-800 px-1.5 py-0.5 text-xs text-slate-300">{value}</span>
      ) : (
        <span className="text-xs text-slate-200">{value}</span>
      )}
    </div>
  );
}

export function IndustryDetail({
  industry,
  onEdit,
  onClose,
  onRefresh,
  onLoadSubgraph,
  onHighlightNodes,
}: IndustryDetailProps) {
  const queryClient = useQueryClient();
  const [showMappingForm, setShowMappingForm] = useState(false);
  const [editingMapping, setEditingMapping] = useState<IndustryNodeMapping | null>(null);

  const { data: subgraph } = useQuery({
    queryKey: ["industry-subgraph", industry.industry_id],
    queryFn: () => getIndustrySubgraph(industry.industry_id),
  });

  const { data: mappingsData } = useQuery({
    queryKey: ["industry-mappings", industry.industry_id, 1, 50],
    queryFn: () => listIndustryMappings(industry.industry_id, 1, 50),
  });

  const deleteMutation = useMutation({
    mutationFn: deleteIndustry,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["industries"] });
      onRefresh();
      onClose();
    },
  });

  const deleteMappingMutation = useMutation({
    mutationFn: (mappingId: string) => deleteIndustryMapping(industry.industry_id, mappingId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["industry-mappings", industry.industry_id] });
      queryClient.invalidateQueries({ queryKey: ["industry-subgraph", industry.industry_id] });
      queryClient.invalidateQueries({ queryKey: ["industries-by-node"] });
    },
  });

  const handleAddSuccess = () => {
    setShowMappingForm(false);
    setEditingMapping(null);
  };

  const handleEdit = (mapping: IndustryNodeMapping) => {
    setEditingMapping(mapping);
    setShowMappingForm(false);
  };

  return (
    <div className="flex h-full flex-col">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 px-4 py-3">
        <h3 className="truncate pr-2 text-sm font-semibold text-slate-100">{industry.name_zh}</h3>
        <div className="flex items-center gap-1">
          <button
            onClick={() => {
              if (subgraph) onLoadSubgraph(subgraph.nodes, subgraph.edges);
            }}
            title="加载子图"
            className="flex h-7 w-7 items-center justify-center rounded text-slate-400 hover:bg-slate-800 hover:text-cyan-400"
          >
            <Link2 className="h-3.5 w-3.5" />
          </button>
          <button
            onClick={() => {
              const nodeIds = mappingsData?.items.map((m) => m.node_id) ?? [];
              if (nodeIds.length > 0) onHighlightNodes(nodeIds);
            }}
            title="在图中高亮"
            className="flex h-7 w-7 items-center justify-center rounded text-slate-400 hover:bg-slate-800 hover:text-yellow-400"
          >
            <Crosshair className="h-3.5 w-3.5" />
          </button>
          <button
            onClick={onEdit}
            title="编辑"
            className="flex h-7 w-7 items-center justify-center rounded text-slate-400 hover:bg-slate-800 hover:text-cyan-400"
          >
            <Edit2 className="h-3.5 w-3.5" />
          </button>
          <button
            onClick={() => {
              if (confirm("确定删除这个行业？")) deleteMutation.mutate(industry.industry_id);
            }}
            title="删除"
            className="flex h-7 w-7 items-center justify-center rounded text-slate-400 hover:bg-slate-800 hover:text-red-400"
          >
            <Trash2 className="h-3.5 w-3.5" />
          </button>
          <button
            onClick={onClose}
            title="关闭"
            className="flex h-7 w-7 items-center justify-center rounded text-slate-400 hover:bg-slate-800 hover:text-slate-200"
          >
            <X className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 space-y-4 overflow-y-auto p-4">
        <div className="space-y-2">
          <Field label="ID" value={industry.industry_id} badge />
          <Field label="英文名" value={industry.name_en} />
          <Field label="类型" value={industry.industry_type} badge />
          <Field label="状态" value={industry.status} badge />
          {industry.aliases.length > 0 && (
            <Field label="别名" value={industry.aliases.join("、")} />
          )}
          <Field label="描述" value={industry.description} />
          {industry.notes && <Field label="备注" value={industry.notes} />}
        </div>

        {/* Mappings */}
        <div className="border-t border-slate-800 pt-3">
          <div className="mb-2 flex items-center justify-between">
            <h4 className="text-xs font-semibold text-slate-300">
              映射节点 ({mappingsData?.total ?? 0})
            </h4>
            <button
              onClick={() => {
                setEditingMapping(null);
                setShowMappingForm(true);
              }}
              className="flex items-center gap-1 rounded px-1.5 py-0.5 text-[10px] text-cyan-400 hover:bg-cyan-900/20"
            >
              <Plus className="h-3 w-3" />
              添加
            </button>
          </div>
          <div className="space-y-1.5">
            {mappingsData?.items.map((m) => (
              <div
                key={m.mapping_id}
                className="rounded border border-slate-800 bg-slate-800/50 px-2.5 py-1.5"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-medium text-slate-200">{m.node_id}</span>
                  <div className="flex items-center gap-1">
                    <span className="text-[10px] text-slate-500">{m.weight.toFixed(2)}</span>
                    <button
                      onClick={() => handleEdit(m)}
                      title="编辑映射"
                      className="rounded p-0.5 text-slate-500 hover:bg-slate-700 hover:text-cyan-400"
                    >
                      <Edit2 className="h-3 w-3" />
                    </button>
                    <button
                      onClick={() => {
                        if (confirm(`确定删除映射 ${m.mapping_id}？`)) {
                          deleteMappingMutation.mutate(m.mapping_id);
                        }
                      }}
                      title="删除映射"
                      className="rounded p-0.5 text-slate-500 hover:bg-slate-700 hover:text-red-400"
                    >
                      <Trash2 className="h-3 w-3" />
                    </button>
                  </div>
                </div>
                {m.role && <span className="text-[10px] text-slate-400">{m.role}</span>}
              </div>
            ))}
            {(mappingsData?.items.length ?? 0) === 0 && (
              <div className="py-2 text-center text-xs text-slate-500">暂无映射节点</div>
            )}
          </div>

          {showMappingForm && !editingMapping && (
            <IndustryMappingForm
              industryId={industry.industry_id}
              onClose={() => setShowMappingForm(false)}
              onSuccess={handleAddSuccess}
            />
          )}

          {editingMapping && (
            <IndustryMappingForm
              industryId={industry.industry_id}
              mapping={editingMapping}
              onClose={() => setEditingMapping(null)}
              onSuccess={handleAddSuccess}
            />
          )}
        </div>
      </div>
    </div>
  );
}
