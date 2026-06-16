import { useMutation } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { X } from "lucide-react";
import { IndustrialNode, IndustrialNodeCreate } from "@/types";
import { createNode, fuzzySearchNodes, updateNode } from "@/services/api";
import { SimilarNodesPanel } from "./SimilarNodesPanel";

interface NodeFormProps {
  mode: "create" | "edit";
  node?: IndustrialNode;
  onClose: () => void;
  onSuccess: (node: IndustrialNode) => void;
}

const ENTITY_TYPES = [
  "material",
  "component",
  "device",
  "module",
  "subsystem",
  "system",
  "platform",
  "infrastructure",
  "application_system",
  "service",
  "technology_capability",
  "unknown",
];

const CONFIDENCES = ["HIGH", "MEDIUM", "LOW"];
const STATUSES = ["ACTIVE", "PENDING", "REJECTED"];

export function NodeForm({ mode, node, onClose, onSuccess }: NodeFormProps) {
  const [form, setForm] = useState<{
    node_id: string;
    canonical_name_zh: string;
    canonical_name_en: string;
    aliases: string;
    definition: string;
    entity_type: string;
    confidence: string;
    status: string;
    notes: string;
  }>({
    node_id: node?.node_id || "",
    canonical_name_zh: node?.canonical_name_zh || "",
    canonical_name_en: node?.canonical_name_en || "",
    aliases: node?.aliases?.join(", ") || "",
    definition: node?.definition || "",
    entity_type: node?.entity_type || "unknown",
    confidence: node?.confidence || "LOW",
    status: node?.status || "PENDING",
    notes: node?.notes || "",
  });
  const [similar, setSimilar] = useState<{ score: number; node: IndustrialNode }[]>([]);
  const [dismissed, setDismissed] = useState(false);
  const [error, setError] = useState("");

  const nameQuery = [form.canonical_name_zh, form.canonical_name_en]
    .map((s) => s?.trim())
    .filter(Boolean)[0];

  useEffect(() => {
    if (mode === "edit" || !nameQuery || nameQuery.length < 2) {
      setSimilar([]);
      setDismissed(false);
      return;
    }
    const timer = setTimeout(async () => {
      try {
        const res = await fuzzySearchNodes(nameQuery, 5, 0.35);
        setSimilar(res.items);
      } catch {
        setSimilar([]);
      }
    }, 400);
    return () => clearTimeout(timer);
  }, [nameQuery, mode]);

  const mutation = useMutation({
    mutationFn: async () => {
      const payload: IndustrialNodeCreate = {
        node_id: form.node_id!,
        canonical_name_zh: form.canonical_name_zh!,
        canonical_name_en: form.canonical_name_en || undefined,
        aliases: form.aliases
          ? String(form.aliases)
              .split(",")
              .map((s) => s.trim())
              .filter(Boolean)
          : [],
        definition: form.definition!,
        entity_type: form.entity_type as IndustrialNode["entity_type"],
        confidence: form.confidence as IndustrialNode["confidence"],
        status: form.status as IndustrialNode["status"],
        evidence: [],
        notes: form.notes || undefined,
      };
      if (mode === "create") {
        return createNode(payload);
      }
      return updateNode(node!.node_id, payload);
    },
    onSuccess: (data) => {
      onSuccess(data);
    },
    onError: (err: Error) => {
      setError(err.message);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    mutation.mutate();
  };

  return (
    <div className="space-y-4 p-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-slate-200">
          {mode === "create" ? "创建节点" : "编辑节点"}
        </h3>
        <button onClick={onClose} className="rounded p-1 text-slate-400 hover:bg-slate-800">
          <X className="h-3.5 w-3.5" />
        </button>
      </div>

      {error && (
        <div className="rounded bg-red-900/20 p-2 text-xs text-red-400">{error}</div>
      )}

      {mode === "create" && !dismissed && (
        <SimilarNodesPanel
          query={nameQuery || ""}
          items={similar}
          onSelect={(node) => {
            setError("");
            onSuccess(node);
          }}
          onDismiss={() => setDismissed(true)}
        />
      )}

      <form onSubmit={handleSubmit} className="space-y-3">
        <FormField label="node_id *">
          <input
            required
            pattern="^[a-z][a-z0-9_]*$"
            minLength={3}
            maxLength={64}
            disabled={mode === "edit"}
            value={form.node_id}
            onChange={(e) => setForm({ ...form, node_id: e.target.value })}
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-sm text-slate-200 focus:border-cyan-500 focus:outline-none disabled:opacity-50"
          />
        </FormField>

        <FormField label="中文名 *">
          <input
            required
            value={form.canonical_name_zh}
            onChange={(e) => setForm({ ...form, canonical_name_zh: e.target.value })}
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-sm text-slate-200 focus:border-cyan-500 focus:outline-none"
          />
        </FormField>

        <FormField label="英文名">
          <input
            value={form.canonical_name_en || ""}
            onChange={(e) => setForm({ ...form, canonical_name_en: e.target.value })}
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-sm text-slate-200 focus:border-cyan-500 focus:outline-none"
          />
        </FormField>

        <FormField label="别名（逗号分隔）">
          <input
            value={form.aliases}
            onChange={(e) => setForm({ ...form, aliases: e.target.value })}
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-sm text-slate-200 focus:border-cyan-500 focus:outline-none"
          />
        </FormField>

        <FormField label="定义 *">
          <textarea
            required
            rows={3}
            value={form.definition}
            onChange={(e) => setForm({ ...form, definition: e.target.value })}
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-sm text-slate-200 focus:border-cyan-500 focus:outline-none"
          />
        </FormField>

        <FormField label="实体类型 *">
          <select
            value={form.entity_type}
            onChange={(e) => setForm({ ...form, entity_type: e.target.value })}
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-sm text-slate-200 focus:border-cyan-500 focus:outline-none"
          >
            {ENTITY_TYPES.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </FormField>

        <FormField label="置信度">
          <select
            value={form.confidence}
            onChange={(e) => setForm({ ...form, confidence: e.target.value })}
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-sm text-slate-200 focus:border-cyan-500 focus:outline-none"
          >
            {CONFIDENCES.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </FormField>

        <FormField label="状态">
          <select
            value={form.status}
            onChange={(e) => setForm({ ...form, status: e.target.value })}
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-sm text-slate-200 focus:border-cyan-500 focus:outline-none"
          >
            {STATUSES.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
        </FormField>

        <FormField label="备注">
          <textarea
            rows={2}
            value={form.notes || ""}
            onChange={(e) => setForm({ ...form, notes: e.target.value })}
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-sm text-slate-200 focus:border-cyan-500 focus:outline-none"
          />
        </FormField>

        <div className="pt-2">
          <button
            type="submit"
            disabled={mutation.isPending}
            className="w-full rounded bg-cyan-600 py-2 text-sm font-medium text-white hover:bg-cyan-500 disabled:opacity-50"
          >
            {mutation.isPending ? "保存中..." : similar.length > 0 && !dismissed ? "仍要保存为新节点" : "保存"}
          </button>
        </div>
      </form>
    </div>
  );
}

function FormField({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <label className="block text-xs font-medium text-slate-400">{label}</label>
      <div className="mt-1">{children}</div>
    </div>
  );
}
