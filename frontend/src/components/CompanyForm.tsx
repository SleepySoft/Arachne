import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { X } from "lucide-react";
import { Company, CompanyType } from "@/types";
import { createCompany, updateCompany } from "@/services/api";

interface CompanyFormProps {
  mode: "create" | "edit";
  company?: Company;
  onClose: () => void;
  onSuccess: (company: Company) => void;
}

export function CompanyForm({ mode, company, onClose, onSuccess }: CompanyFormProps) {
  const queryClient = useQueryClient();
  const [form, setForm] = useState({
    company_id: company?.company_id ?? "",
    name_zh: company?.name_zh ?? "",
    name_en: company?.name_en ?? "",
    stock_codes: company?.stock_codes.join(", ") ?? "",
    description: company?.description ?? "",
    country: company?.country ?? "CN",
    province: company?.province ?? "",
    city: company?.city ?? "",
    founded_year: company?.founded_year?.toString() ?? "",
    employee_count: company?.employee_count?.toString() ?? "",
    revenue_cny: company?.revenue_cny?.toString() ?? "",
    market_cap_cny: company?.market_cap_cny?.toString() ?? "",
    net_profit_cny: company?.net_profit_cny?.toString() ?? "",
    company_type: (company?.company_type ?? "unknown") as CompanyType,
    status: (company?.status ?? "ACTIVE") as Company["status"],
    notes: company?.notes ?? "",
  });
  const [error, setError] = useState<string | null>(null);

  const mutation = useMutation({
    mutationFn: async () => {
      const payload = {
        name_zh: form.name_zh,
        name_en: form.name_en || undefined,
        stock_codes: form.stock_codes.split(",").map((s) => s.trim()).filter(Boolean),
        description: form.description || undefined,
        country: form.country,
        province: form.province || undefined,
        city: form.city || undefined,
        founded_year: form.founded_year ? parseInt(form.founded_year) : undefined,
        employee_count: form.employee_count ? parseInt(form.employee_count) : undefined,
        revenue_cny: form.revenue_cny ? parseFloat(form.revenue_cny) : undefined,
        market_cap_cny: form.market_cap_cny ? parseFloat(form.market_cap_cny) : undefined,
        net_profit_cny: form.net_profit_cny ? parseFloat(form.net_profit_cny) : undefined,
        company_type: form.company_type,
        status: form.status,
        notes: form.notes || undefined,
      };
      if (mode === "create") {
        return createCompany({ company_id: form.company_id, ...payload });
      } else {
        if (!company) throw new Error("No company to update");
        return updateCompany(company.company_id, payload);
      }
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["companies"] });
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
          {mode === "create" ? "创建公司" : "编辑公司"}
        </h3>
        <button onClick={onClose} className="flex h-7 w-7 items-center justify-center rounded text-slate-400 hover:bg-slate-800 hover:text-slate-200">
          <X className="h-3.5 w-3.5" />
        </button>
      </div>

      <form onSubmit={handleSubmit} className="flex-1 space-y-3 overflow-y-auto p-4">
        {error && <div className="rounded bg-red-900/30 px-2.5 py-1.5 text-xs text-red-300">{error}</div>}

        <FormField label="公司 ID">
          <input
            value={form.company_id}
            onChange={(e) => setForm((f) => ({ ...f, company_id: e.target.value }))}
            disabled={mode === "edit"}
            placeholder="例如 hesai_technology"
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

        <FormField label="股票代码">
          <input
            value={form.stock_codes}
            onChange={(e) => setForm((f) => ({ ...f, stock_codes: e.target.value }))}
            placeholder="多个用逗号分隔"
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
          />
        </FormField>

        <div className="grid grid-cols-2 gap-2">
          <FormField label="类型">
            <select
              value={form.company_type}
              onChange={(e) => setForm((f) => ({ ...f, company_type: e.target.value as CompanyType }))}
              className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
            >
              <option value="public">上市公司</option>
              <option value="private">民营</option>
              <option value="state_owned">国企</option>
              <option value="startup">初创</option>
              <option value="unknown">未知</option>
            </select>
          </FormField>
          <FormField label="状态">
            <select
              value={form.status}
              onChange={(e) => setForm((f) => ({ ...f, status: e.target.value as Company["status"] }))}
              className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
            >
              <option value="ACTIVE">启用</option>
              <option value="PENDING">待审</option>
              <option value="REJECTED">拒绝</option>
              <option value="ARCHIVED">归档</option>
            </select>
          </FormField>
        </div>

        <div className="grid grid-cols-3 gap-2">
          <FormField label="国家">
            <input
              value={form.country}
              onChange={(e) => setForm((f) => ({ ...f, country: e.target.value }))}
              className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
            />
          </FormField>
          <FormField label="省份">
            <input
              value={form.province}
              onChange={(e) => setForm((f) => ({ ...f, province: e.target.value }))}
              className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
            />
          </FormField>
          <FormField label="城市">
            <input
              value={form.city}
              onChange={(e) => setForm((f) => ({ ...f, city: e.target.value }))}
              className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
            />
          </FormField>
        </div>

        <div className="grid grid-cols-2 gap-2">
          <FormField label="成立年份">
            <input
              type="number"
              value={form.founded_year}
              onChange={(e) => setForm((f) => ({ ...f, founded_year: e.target.value }))}
              className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
            />
          </FormField>
          <FormField label="员工数">
            <input
              type="number"
              value={form.employee_count}
              onChange={(e) => setForm((f) => ({ ...f, employee_count: e.target.value }))}
              className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
            />
          </FormField>
        </div>

        <div className="grid grid-cols-3 gap-2">
          <FormField label="营收 (CNY)">
            <input
              type="number"
              value={form.revenue_cny}
              onChange={(e) => setForm((f) => ({ ...f, revenue_cny: e.target.value }))}
              className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
            />
          </FormField>
          <FormField label="市值 (CNY)">
            <input
              type="number"
              value={form.market_cap_cny}
              onChange={(e) => setForm((f) => ({ ...f, market_cap_cny: e.target.value }))}
              className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
            />
          </FormField>
          <FormField label="净利润 (CNY)">
            <input
              type="number"
              value={form.net_profit_cny}
              onChange={(e) => setForm((f) => ({ ...f, net_profit_cny: e.target.value }))}
              className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
            />
          </FormField>
        </div>

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
