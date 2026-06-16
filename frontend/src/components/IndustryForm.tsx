import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { X } from "lucide-react";
import { Industry, IndustryType } from "@/types";
import { createIndustry, updateIndustry } from "@/services/api";

interface IndustryFormProps {
  mode: "create" | "edit";
  industry?: Industry;
  onClose: () => void;
  onSuccess: (industry: Industry) => void;
}

export function IndustryForm({ mode, industry, onClose, onSuccess }: IndustryFormProps) {
  const queryClient = useQueryClient();
  const [form, setForm] = useState({
    industry_id: industry?.industry_id ?? "",
    name_zh: industry?.name_zh ?? "",
    name_en: industry?.name_en ?? "",
    aliases: industry?.aliases?.join(", ") ?? "",
    industry_type: (industry?.industry_type ?? "curated_view") as IndustryType,
    description: industry?.description ?? "",
    status: (industry?.status ?? "ACTIVE") as Industry["status"],
    notes: industry?.notes ?? "",
  });
  const [error, setError] = useState<string | null>(null);

  const mutation = useMutation({
    mutationFn: async () => {
      if (mode === "create") {
        return createIndustry({
          ...form,
          aliases: form.aliases
            .split(",")
            .map((s) => s.trim())
            .filter(Boolean),
        });
      } else {
        if (!industry) throw new Error("No industry to update");
        return updateIndustry(industry.industry_id, {
          name_zh: form.name_zh,
          name_en: form.name_en,
          aliases: form.aliases
            .split(",")
            .map((s) => s.trim())
            .filter(Boolean),
          industry_type: form.industry_type,
          description: form.description,
          status: form.status,
          notes: form.notes,
        });
      }
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["industries"] });
      onSuccess(data);
    },
    onError: (err: Error) => setError(err.message),
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    mutation.mutate();
  };

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b border-slate-800 px-4 py-3">
        <h3 className="text-sm font-semibold text-slate-100">
          {mode === "create" ? "创建行业" : "编辑行业"}
        </h3>
        <button onClick={onClose} className="flex h-7 w-7 items-center justify-center rounded text-slate-400 hover:bg-slate-800 hover:text-slate-200">
          <X className="h-3.5 w-3.5" />
        </button>
      </div>

      <form onSubmit={handleSubmit} className="flex-1 space-y-3 overflow-y-auto p-4">
        {error && <div className="rounded bg-red-900/30 px-2.5 py-1.5 text-xs text-red-300">{error}</div>}

        <FormField label="行业 ID">
          <input
            value={form.industry_id}
            onChange={(e) => setForm((f) => ({ ...f, industry_id: e.target.value }))}
            disabled={mode === "edit"}
            placeholder="例如 intelligent_driving"
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none disabled:opacity-50"
          />
        </FormField>

        <FormField label="中文名称 *">
          <input
            value={form.name_zh}
            onChange={(e) => setForm((f) => ({ ...f, name_zh: e.target.value }))}
            required
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
          />
        </FormField>

        <FormField label="英文名称">
          <input
            value={form.name_en}
            onChange={(e) => setForm((f) => ({ ...f, name_en: e.target.value }))}
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
          />
        </FormField>

        <FormField label="别名（逗号分隔）">
          <input
            value={form.aliases}
            onChange={(e) => setForm((f) => ({ ...f, aliases: e.target.value }))}
            placeholder="例如 智能制造, 先进制造"
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
          />
        </FormField>

        <FormField label="类型">
          <select
            value={form.industry_type}
            onChange={(e) => setForm((f) => ({ ...f, industry_type: e.target.value as IndustryType }))}
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
          >
            <option value="curated_view">产业链视图</option>
            <option value="formal_industry">正式行业</option>
            <option value="theme_view">市场主题</option>
          </select>
        </FormField>

        <FormField label="状态">
          <select
            value={form.status}
            onChange={(e) => setForm((f) => ({ ...f, status: e.target.value as Industry["status"] }))}
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
          >
            <option value="ACTIVE">启用</option>
            <option value="PENDING">待审</option>
            <option value="REJECTED">拒绝</option>
            <option value="ARCHIVED">归档</option>
          </select>
        </FormField>

        <FormField label="描述">
          <textarea
            value={form.description}
            onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
            rows={3}
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
          />
        </FormField>

        <FormField label="备注">
          <textarea
            value={form.notes}
            onChange={(e) => setForm((f) => ({ ...f, notes: e.target.value }))}
            rows={2}
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
          />
        </FormField>

        <button
          type="submit"
          disabled={mutation.isPending}
          className="mt-2 w-full rounded bg-cyan-600 py-2 text-xs font-medium text-white hover:bg-cyan-500 disabled:opacity-50"
        >
          {mutation.isPending ? "保存中..." : mode === "create" ? "创建" : "保存"}
        </button>
      </form>
    </div>
  );
}

function FormField({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="space-y-1">
      <label className="text-[10px] font-medium uppercase tracking-wider text-slate-500">{label}</label>
      {children}
    </div>
  );
}
