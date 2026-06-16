import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Search, X, Plus, Trash2 } from "lucide-react";
import { Confidence, Evidence, IndustryNodeMapping, RecordStatus } from "@/types";
import { createIndustryMapping, listNodes, updateIndustryMapping } from "@/services/api";

interface IndustryMappingFormProps {
  industryId: string;
  mapping?: IndustryNodeMapping;
  onClose: () => void;
  onSuccess: () => void;
}

const CONFIDENCES: Confidence[] = ["HIGH", "MEDIUM", "LOW"];
const STATUSES: RecordStatus[] = ["ACTIVE", "PENDING", "REJECTED", "ARCHIVED"];

export function IndustryMappingForm({
  industryId,
  mapping,
  onClose,
  onSuccess,
}: IndustryMappingFormProps) {
  const queryClient = useQueryClient();
  const isEdit = Boolean(mapping);

  const [nodeQuery, setNodeQuery] = useState("");
  const [selectedNodeId, setSelectedNodeId] = useState(mapping?.node_id || "");
  const [selectedNodeName, setSelectedNodeName] = useState(mapping?.node_id || "");
  const [mappingId, setMappingId] = useState(mapping?.mapping_id || "");
  const [role, setRole] = useState(mapping?.role || "");
  const [weight, setWeight] = useState<number>(mapping?.weight ?? 1.0);
  const [confidence, setConfidence] = useState<Confidence>(mapping?.confidence || "MEDIUM");
  const [status, setStatus] = useState<RecordStatus>(mapping?.status || "ACTIVE");
  const [notes, setNotes] = useState(mapping?.notes || "");
  const [evidence, setEvidence] = useState<Evidence[]>(
    mapping?.evidence?.length ? mapping.evidence : [{ source_title: "", quote: "" }]
  );
  const [error, setError] = useState<string | null>(null);

  const { data: nodeSearchData } = useQuery({
    queryKey: ["nodes", 1, 10, undefined, undefined, nodeQuery],
    queryFn: () => listNodes(1, 10, undefined, undefined, nodeQuery),
    enabled: nodeQuery.length >= 1 && !isEdit,
  });

  const mutation = useMutation({
    mutationFn: async () => {
      const payload: Partial<IndustryNodeMapping> = {
        mapping_id: mappingId,
        industry_id: industryId,
        node_id: selectedNodeId,
        role: role || undefined,
        weight,
        confidence,
        evidence: evidence.filter((e) => e.source_title.trim() || e.quote.trim()),
        status,
        notes: notes || undefined,
      };
      if (isEdit && mapping) {
        return updateIndustryMapping(industryId, mapping.mapping_id, payload);
      }
      return createIndustryMapping(industryId, payload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["industry-mappings", industryId] });
      queryClient.invalidateQueries({ queryKey: ["industry-subgraph", industryId] });
      queryClient.invalidateQueries({ queryKey: ["industries-by-node"] });
      onSuccess();
    },
    onError: (err: Error) => setError(err.message),
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!selectedNodeId) {
      setError("请选择一个节点");
      return;
    }
    if (!mappingId) {
      setError("请填写映射 ID");
      return;
    }
    if (confidence === "HIGH" && !evidence.some((e) => e.source_title.trim() && e.quote.trim())) {
      setError("高置信度映射必须提供至少一条完整证据（来源标题和引用）");
      return;
    }
    mutation.mutate();
  };

  const addEvidence = () => {
    setEvidence([...evidence, { source_title: "", quote: "" }]);
  };

  const removeEvidence = (idx: number) => {
    setEvidence(evidence.filter((_, i) => i !== idx));
  };

  const updateEvidence = (idx: number, field: keyof Evidence, value: string) => {
    setEvidence(evidence.map((e, i) => (i === idx ? { ...e, [field]: value } : e)));
  };

  const handleSelectNode = (nodeId: string, nodeName: string) => {
    setSelectedNodeId(nodeId);
    setSelectedNodeName(nodeName);
    if (!mappingId) {
      setMappingId(`${industryId}_contains_${nodeId}`);
    }
    setNodeQuery("");
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-3 border-t border-slate-800 pt-3">
      <div className="flex items-center justify-between">
        <h5 className="text-xs font-medium text-cyan-400">
          {isEdit ? "编辑映射" : "添加节点映射"}
        </h5>
        <button
          type="button"
          onClick={onClose}
          className="rounded p-1 text-slate-500 hover:bg-slate-800 hover:text-slate-300"
        >
          <X className="h-3 w-3" />
        </button>
      </div>

      {error && <div className="rounded bg-red-900/30 px-2 py-1.5 text-[11px] text-red-300">{error}</div>}

      {/* Node selector */}
      <div className="space-y-1">
        <label className="text-[10px] font-medium uppercase tracking-wider text-slate-500">
          节点 {isEdit && "（不可更改）"}
        </label>
        {isEdit ? (
          <div className="rounded border border-slate-700 bg-slate-800/50 px-2 py-1.5 text-xs text-slate-300">
            {selectedNodeName}
          </div>
        ) : (
          <div className="relative">
            <Search className="absolute left-2 top-1/2 h-3 w-3 -translate-y-1/2 text-slate-500" />
            <input
              type="text"
              value={selectedNodeId ? selectedNodeName : nodeQuery}
              onChange={(e) => {
                setNodeQuery(e.target.value);
                if (selectedNodeId) {
                  setSelectedNodeId("");
                  setSelectedNodeName("");
                }
              }}
              placeholder="搜索并选择节点..."
              className="w-full rounded border border-slate-700 bg-slate-800 py-1.5 pl-6 pr-2 text-xs text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
            />
            {nodeSearchData && nodeQuery && !selectedNodeId && (
              <div className="absolute z-10 mt-1 max-h-40 w-full overflow-auto rounded border border-slate-700 bg-slate-800 shadow-lg">
                {nodeSearchData.items.length === 0 ? (
                  <div className="px-2 py-1.5 text-xs text-slate-500">无结果</div>
                ) : (
                  nodeSearchData.items.map((node) => (
                    <button
                      key={node.node_id}
                      type="button"
                      onClick={() => handleSelectNode(node.node_id, `${node.canonical_name_zh} (${node.node_id})`)}
                      className="flex w-full items-center gap-2 px-2 py-1.5 text-left text-xs hover:bg-slate-700"
                    >
                      <span className="font-medium text-slate-200">{node.canonical_name_zh}</span>
                      <span className="text-[10px] text-slate-500">{node.node_id}</span>
                      <span className="ml-auto rounded bg-slate-700 px-1.5 py-0 text-[9px] text-slate-400">
                        {node.entity_type}
                      </span>
                    </button>
                  ))
                )}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Mapping ID */}
      <div className="space-y-1">
        <label className="text-[10px] font-medium uppercase tracking-wider text-slate-500">
          映射 ID *
        </label>
        <input
          type="text"
          value={mappingId}
          onChange={(e) => setMappingId(e.target.value)}
          disabled={isEdit}
          placeholder="例如 robotics_contains_motor"
          pattern="^[a-z][a-z0-9_]*$"
          minLength={3}
          maxLength={64}
          required
          className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none disabled:opacity-50"
        />
      </div>

      {/* Role */}
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

      {/* Weight */}
      <div className="space-y-1">
        <label className="text-[10px] font-medium uppercase tracking-wider text-slate-500">
          权重 (0-1)
        </label>
        <input
          type="number"
          min={0}
          max={1}
          step={0.05}
          value={weight}
          onChange={(e) => setWeight(Number(e.target.value))}
          className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
        />
      </div>

      {/* Confidence */}
      <div className="space-y-1">
        <label className="text-[10px] font-medium uppercase tracking-wider text-slate-500">
          置信度
        </label>
        <select
          value={confidence}
          onChange={(e) => setConfidence(e.target.value as Confidence)}
          className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
        >
          {CONFIDENCES.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </div>

      {/* Status */}
      <div className="space-y-1">
        <label className="text-[10px] font-medium uppercase tracking-wider text-slate-500">
          状态
        </label>
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value as RecordStatus)}
          className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
        >
          {STATUSES.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
      </div>

      {/* Evidence */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <label className="text-[10px] font-medium uppercase tracking-wider text-slate-500">
            证据
          </label>
          <button
            type="button"
            onClick={addEvidence}
            className="flex items-center gap-0.5 text-[10px] text-cyan-400 hover:text-cyan-300"
          >
            <Plus className="h-3 w-3" />
            添加
          </button>
        </div>
        {evidence.map((ev, idx) => (
          <div key={idx} className="space-y-1.5 rounded border border-slate-800 bg-slate-800/30 p-2">
            <div className="flex items-center gap-1">
              <input
                type="text"
                value={ev.source_title}
                onChange={(e) => updateEvidence(idx, "source_title", e.target.value)}
                placeholder="来源标题"
                className="flex-1 rounded border border-slate-700 bg-slate-800 px-2 py-1 text-[11px] text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
              />
              <button
                type="button"
                onClick={() => removeEvidence(idx)}
                className="rounded p-1 text-slate-500 hover:bg-slate-800 hover:text-red-400"
              >
                <Trash2 className="h-3 w-3" />
              </button>
            </div>
            <input
              type="text"
              value={ev.source_url || ""}
              onChange={(e) => updateEvidence(idx, "source_url", e.target.value)}
              placeholder="来源 URL（可选）"
              className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1 text-[11px] text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
            />
            <textarea
              value={ev.quote}
              onChange={(e) => updateEvidence(idx, "quote", e.target.value)}
              placeholder="引用内容"
              rows={2}
              className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1 text-[11px] text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
            />
          </div>
        ))}
      </div>

      {/* Notes */}
      <div className="space-y-1">
        <label className="text-[10px] font-medium uppercase tracking-wider text-slate-500">
          备注
        </label>
        <textarea
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          rows={2}
          className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
        />
      </div>

      <div className="flex gap-2 pt-1">
        <button
          type="submit"
          disabled={mutation.isPending}
          className="flex-1 rounded bg-cyan-600 py-1.5 text-xs font-medium text-white hover:bg-cyan-500 disabled:opacity-50"
        >
          {mutation.isPending ? "保存中..." : isEdit ? "保存" : "添加"}
        </button>
        <button
          type="button"
          onClick={onClose}
          className="rounded border border-slate-700 bg-slate-800 px-3 py-1.5 text-xs text-slate-300 hover:bg-slate-700"
        >
          取消
        </button>
      </div>
    </form>
  );
}
