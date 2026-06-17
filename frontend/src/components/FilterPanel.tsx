import { Filter } from "lucide-react";
import {
  CONFIDENCE_OPACITY,
  EdgeNamespace,
  ENTITY_TYPE_COLORS,
  EntityType,
} from "@/types";

interface FilterState {
  edgeNamespaces: string[];
  edgeTypes: string[];
  entityTypes: string[];
  status: string[];
  confidence: string[];
  showWeakOntology: boolean;
}

type ArrayFilterKey = "edgeNamespaces" | "edgeTypes" | "entityTypes" | "status" | "confidence";

interface FilterPanelProps {
  filters: FilterState;
  onChange: (filters: FilterState) => void;
}

const STATUSES = ["ACTIVE", "PENDING", "REJECTED"];
const CONFIDENCES = ["HIGH", "MEDIUM", "LOW"];

export function FilterPanel({ filters, onChange }: FilterPanelProps) {
  const toggle = (key: ArrayFilterKey, value: string) => {
    const arr = filters[key];
    const next = arr.includes(value)
      ? arr.filter((v) => v !== value)
      : [...arr, value];
    onChange({ ...filters, [key]: next });
  };

  return (
    <div className="space-y-4 p-3">
      <div className="flex items-center gap-2 text-sm font-semibold text-slate-300">
        <Filter className="h-4 w-4" />
        过滤
      </div>

      {/* Edge Namespace */}
      <FilterGroup title="关系命名空间">
        {(["industrial_flow", "ontology"] as EdgeNamespace[]).map((ns) => (
          <label key={ns} className="flex items-center gap-2 text-xs text-slate-400">
            <input
              type="checkbox"
              checked={filters.edgeNamespaces.includes(ns)}
              onChange={() => toggle("edgeNamespaces", ns)}
              className="h-3 w-3 rounded border-slate-600 bg-slate-800 text-cyan-500"
            />
            <span>{ns === "industrial_flow" ? "产业流" : "本体"}</span>
          </label>
        ))}
      </FilterGroup>

      {/* Entity Type */}
      <FilterGroup title="实体类型">
        {(Object.keys(ENTITY_TYPE_COLORS) as EntityType[]).map((t) => (
          <label key={t} className="flex items-center gap-2 text-xs text-slate-400">
            <input
              type="checkbox"
              checked={filters.entityTypes.includes(t)}
              onChange={() => toggle("entityTypes", t)}
              className="h-3 w-3 rounded border-slate-600 bg-slate-800 text-cyan-500"
            />
            <span
              className="inline-block h-2 w-2 rounded-full"
              style={{ backgroundColor: ENTITY_TYPE_COLORS[t] }}
            />
            <span>{t}</span>
          </label>
        ))}
      </FilterGroup>

      {/* Status */}
      <FilterGroup title="节点状态">
        {STATUSES.map((s) => (
          <label key={s} className="flex items-center gap-2 text-xs text-slate-400">
            <input
              type="checkbox"
              checked={filters.status.includes(s)}
              onChange={() => toggle("status", s)}
              className="h-3 w-3 rounded border-slate-600 bg-slate-800 text-cyan-500"
            />
            <span>{s}</span>
          </label>
        ))}
      </FilterGroup>

      {/* Confidence */}
      <FilterGroup title="置信度">
        {CONFIDENCES.map((c) => (
          <label key={c} className="flex items-center gap-2 text-xs text-slate-400">
            <input
              type="checkbox"
              checked={filters.confidence.includes(c)}
              onChange={() => toggle("confidence", c)}
              className="h-3 w-3 rounded border-slate-600 bg-slate-800 text-cyan-500"
            />
            <span
              className="inline-block h-2 w-2 rounded-full bg-slate-400"
              style={{ opacity: CONFIDENCE_OPACITY[c as keyof typeof CONFIDENCE_OPACITY] }}
            />
            <span>{c}</span>
          </label>
        ))}
      </FilterGroup>
    </div>
  );
}

function FilterGroup({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="space-y-1.5">
      <div className="text-[10px] font-semibold uppercase tracking-wider text-slate-500">
        {title}
      </div>
      <div className="space-y-1">{children}</div>
    </div>
  );
}
