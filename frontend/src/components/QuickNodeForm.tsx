import { useEffect, useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Plus, X, Sparkles } from "lucide-react";
import { IndustrialNode, IndustrialNodeQuickCreate } from "@/types";
import { fuzzySearchNodes, quickCreateNode } from "@/services/api";
import { SimilarNodesPanel } from "./SimilarNodesPanel";

interface QuickNodeFormProps {
  onSuccess?: (node: IndustrialNode) => void;
  onCancel?: () => void;
  initialName?: string;
}

export function QuickNodeForm({ onSuccess, onCancel, initialName = "" }: QuickNodeFormProps) {
  const queryClient = useQueryClient();
  const [form, setForm] = useState<IndustrialNodeQuickCreate>({
    canonical_name_zh: initialName,
    canonical_name_en: "",
    entity_type: "unknown",
    notes: "",
  });
  const [similar, setSimilar] = useState<{ score: number; node: IndustrialNode }[]>([]);
  const [searching, setSearching] = useState(false);
  const [dismissed, setDismissed] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const nameQuery = [form.canonical_name_zh, form.canonical_name_en]
    .map((s) => s?.trim())
    .filter(Boolean)[0];

  useEffect(() => {
    if (!nameQuery || nameQuery.length < 2) {
      setSimilar([]);
      setDismissed(false);
      return;
    }
    const timer = setTimeout(async () => {
      setSearching(true);
      try {
        const res = await fuzzySearchNodes(nameQuery, 5, 0.35);
        setSimilar(res.items);
      } catch {
        setSimilar([]);
      } finally {
        setSearching(false);
      }
    }, 400);
    return () => clearTimeout(timer);
  }, [nameQuery]);

  const mutation = useMutation({
    mutationFn: quickCreateNode,
    onSuccess: (node) => {
      queryClient.invalidateQueries({ queryKey: ["nodes"] });
      queryClient.invalidateQueries({ queryKey: ["stats"] });
      setForm({ canonical_name_zh: "", canonical_name_en: "", entity_type: "unknown", notes: "" });
      setError(null);
      onSuccess?.(node);
    },
    onError: (err: Error) => setError(err.message),
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!form.canonical_name_zh?.trim() && !form.canonical_name_en?.trim()) {
      setError("请填写中文名或英文名至少一项");
      return;
    }
    const payload: IndustrialNodeQuickCreate = {
      ...form,
      canonical_name_zh: form.canonical_name_zh?.trim() || undefined,
      canonical_name_en: form.canonical_name_en?.trim() || undefined,
      notes: form.notes?.trim() || undefined,
    };
    mutation.mutate(payload);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-2 rounded border border-dashed border-cyan-700/50 bg-cyan-900/10 p-2.5">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-1 text-[11px] font-medium text-cyan-400">
          <Sparkles className="h-3 w-3" />
          快速添加草稿节点
        </div>
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="rounded p-0.5 text-slate-500 hover:bg-slate-800 hover:text-slate-300"
          >
            <X className="h-3 w-3" />
          </button>
        )}
      </div>

      {error && (
        <div className="rounded bg-red-900/30 px-2 py-1 text-[10px] text-red-300">{error}</div>
      )}

      {!dismissed && (
        <SimilarNodesPanel
          query={nameQuery || ""}
          items={similar}
          onSelect={(node) => {
            setError(null);
            onSuccess?.(node);
          }}
          onDismiss={() => setDismissed(true)}
        />
      )}

      {searching && similar.length === 0 && (
        <div className="text-[10px] text-slate-500">正在检查相似节点...</div>
      )}

      <div className="flex gap-2">
        <input
          type="text"
          value={form.canonical_name_zh || ""}
          onChange={(e) => setForm((f) => ({ ...f, canonical_name_zh: e.target.value }))}
          placeholder="中文名 *"
          className="flex-1 rounded border border-slate-700 bg-slate-800 px-2 py-1 text-xs text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
        />
        <input
          type="text"
          value={form.canonical_name_en || ""}
          onChange={(e) => setForm((f) => ({ ...f, canonical_name_en: e.target.value }))}
          placeholder="English name *"
          className="flex-1 rounded border border-slate-700 bg-slate-800 px-2 py-1 text-xs text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
        />
      </div>

      <div className="flex gap-2">
        <select
          value={form.entity_type}
          onChange={(e) => setForm((f) => ({ ...f, entity_type: e.target.value as IndustrialNode["entity_type"] }))}
          className="rounded border border-slate-700 bg-slate-800 px-2 py-1 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
        >
          <option value="unknown">未知类型</option>
          <option value="material">材料</option>
          <option value="component">部件</option>
          <option value="device">器件</option>
          <option value="module">模块</option>
          <option value="subsystem">子系统</option>
          <option value="system">系统</option>
          <option value="platform">平台</option>
          <option value="infrastructure">基础设施</option>
          <option value="application_system">应用系统</option>
          <option value="service">服务</option>
          <option value="technology_capability">技术能力</option>
        </select>
        <input
          type="text"
          value={form.notes || ""}
          onChange={(e) => setForm((f) => ({ ...f, notes: e.target.value }))}
          placeholder="备注（可选）"
          className="flex-1 rounded border border-slate-700 bg-slate-800 px-2 py-1 text-xs text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
        />
      </div>

      <button
        type="submit"
        disabled={mutation.isPending}
        className="flex w-full items-center justify-center gap-1 rounded bg-cyan-600/80 py-1 text-xs font-medium text-white hover:bg-cyan-500 disabled:opacity-50"
      >
        <Plus className="h-3 w-3" />
        {mutation.isPending ? "添加中..." : similar.length > 0 && !dismissed ? "仍要添加为新节点" : "添加为草稿节点（PENDING）"}
      </button>

      <p className="text-[9px] text-slate-500">
        只需名称即可创建。系统会自动生成占位 ID 并设为待完善状态，后续可由 AI 或管理员补全定义、证据和规范 ID。
      </p>
    </form>
  );
}
