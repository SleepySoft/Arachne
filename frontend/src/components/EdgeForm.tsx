import { useMutation, useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { X } from "lucide-react";
import {
  Confidence,
  EdgeNamespace,
  EDGE_TYPE_LABELS,
  GraphEdge,
  IndustrialFlowEdgeCreate,
  OntologyEdgeCreate,
} from "@/types";
import { createEdge, listNodes, updateEdge } from "@/services/api";

interface EdgeFormProps {
  mode: "create" | "edit";
  edge?: GraphEdge;
  defaultFromNode?: string;
  defaultToNode?: string;
  prefillData?: {
    from_node?: string;
    to_node?: string;
    edge_type?: string;
    description?: string;
    notes?: string;
  };
  onClose: () => void;
  onSuccess: (edge: GraphEdge) => void;
}

const EDGE_NAMESPACES = ["industrial_flow", "ontology"] as const;

const INDUSTRIAL_FLOW_TYPES = [
  "material_flow",
  "composition",
  "energy_flow",
  "information_flow",
  "capability_supply",
  "service_flow",
  "produces",
];

const ONTOLOGY_TYPES = ["alias_of", "is_a", "variant_of", "related_term"];
const CONFIDENCES = ["HIGH", "MEDIUM", "LOW"];

export function EdgeForm({ mode, edge, defaultFromNode, defaultToNode, prefillData, onClose, onSuccess }: EdgeFormProps) {
  const [namespace, setNamespace] = useState<EdgeNamespace>(edge?.edge_namespace || "industrial_flow");
  const [form, setForm] = useState({
    edge_id: edge?.edge_id || "",
    from_node: edge?.from_node || defaultFromNode || prefillData?.from_node || "",
    to_node: edge?.to_node || defaultToNode || prefillData?.to_node || "",
    edge_type: edge?.edge_type || prefillData?.edge_type || "material_flow",
    description: edge?.description || prefillData?.description || "",
    confidence: edge?.confidence || "LOW",
    notes: edge?.notes || prefillData?.notes || "",
  });
  const [error, setError] = useState("");

  const { data: nodesData } = useQuery({
    queryKey: ["nodes", 1, 1000],
    queryFn: () => listNodes(1, 1000),
  });

  const nodeOptions = nodesData?.items || [];

  const mutation = useMutation({
    mutationFn: async () => {
      if (namespace === "industrial_flow") {
        const payload: IndustrialFlowEdgeCreate = {
          edge_namespace: "industrial_flow",
          edge_id: form.edge_id,
          from_node: form.from_node,
          to_node: form.to_node,
          edge_type: form.edge_type as IndustrialFlowEdgeCreate["edge_type"],
          description: form.description,
          evidence: [],
          confidence: form.confidence as Confidence,
          notes: form.notes || undefined,
        };
        if (mode === "create") return createEdge(payload);
        return updateEdge(edge!.edge_id, payload);
      } else {
        const payload: OntologyEdgeCreate = {
          edge_namespace: "ontology",
          edge_id: form.edge_id,
          from_node: form.from_node,
          to_node: form.to_node,
          edge_type: form.edge_type as OntologyEdgeCreate["edge_type"],
          description: form.description,
          evidence: [],
          confidence: form.confidence as Confidence,
          notes: form.notes || undefined,
        };
        if (mode === "create") return createEdge(payload);
        return updateEdge(edge!.edge_id, payload);
      }
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

  const typeOptions = namespace === "industrial_flow" ? INDUSTRIAL_FLOW_TYPES : ONTOLOGY_TYPES;

  return (
    <div className="space-y-4 p-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-slate-200">
          {mode === "create" ? "创建关系" : "编辑关系"}
        </h3>
        <button onClick={onClose} className="rounded p-1 text-slate-400 hover:bg-slate-800">
          <X className="h-3.5 w-3.5" />
        </button>
      </div>

      {error && (
        <div className="rounded bg-red-900/20 p-2 text-xs text-red-400">{error}</div>
      )}

      <form onSubmit={handleSubmit} className="space-y-3">
        <FormField label="命名空间 *">
          <select
            value={namespace}
            disabled={mode === "edit"}
            onChange={(e) => {
              const ns = e.target.value as EdgeNamespace;
              setNamespace(ns);
              setForm({
                ...form,
                edge_type: ns === "industrial_flow" ? "material_flow" : "alias_of",
              });
            }}
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-sm text-slate-200 focus:border-cyan-500 focus:outline-none disabled:opacity-50"
          >
            {EDGE_NAMESPACES.map((ns) => (
              <option key={ns} value={ns}>
                {ns}
              </option>
            ))}
          </select>
        </FormField>

        <FormField label="edge_id *">
          <input
            required
            pattern="^[a-z][a-z0-9_]*$"
            disabled={mode === "edit"}
            value={form.edge_id}
            onChange={(e) => setForm({ ...form, edge_id: e.target.value })}
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-sm text-slate-200 focus:border-cyan-500 focus:outline-none disabled:opacity-50"
          />
        </FormField>

        <FormField label="起点节点 *">
          <select
            required
            disabled={mode === "edit"}
            value={form.from_node}
            onChange={(e) => setForm({ ...form, from_node: e.target.value })}
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-sm text-slate-200 focus:border-cyan-500 focus:outline-none disabled:opacity-50"
          >
            <option value="">选择节点</option>
            {nodeOptions.map((n) => (
              <option key={n.node_id} value={n.node_id}>
                {n.canonical_name_zh} ({n.node_id})
              </option>
            ))}
          </select>
        </FormField>

        <FormField label="终点节点 *">
          <select
            required
            disabled={mode === "edit"}
            value={form.to_node}
            onChange={(e) => setForm({ ...form, to_node: e.target.value })}
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-sm text-slate-200 focus:border-cyan-500 focus:outline-none disabled:opacity-50"
          >
            <option value="">选择节点</option>
            {nodeOptions.map((n) => (
              <option key={n.node_id} value={n.node_id}>
                {n.canonical_name_zh} ({n.node_id})
              </option>
            ))}
          </select>
        </FormField>

        <FormField label="关系类型 *">
          <select
            value={form.edge_type}
            onChange={(e) => setForm({ ...form, edge_type: e.target.value as IndustrialFlowEdgeCreate["edge_type"] | OntologyEdgeCreate["edge_type"] })}
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-sm text-slate-200 focus:border-cyan-500 focus:outline-none"
          >
            {typeOptions.map((t) => (
              <option key={t} value={t}>
                {EDGE_TYPE_LABELS[t] || t}
              </option>
            ))}
          </select>
        </FormField>

        <FormField label="描述 *">
          <textarea
            required
            rows={3}
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-sm text-slate-200 focus:border-cyan-500 focus:outline-none"
          />
        </FormField>

        <FormField label="置信度">
          <select
            value={form.confidence}
            onChange={(e) => setForm({ ...form, confidence: e.target.value as Confidence })}
            className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-sm text-slate-200 focus:border-cyan-500 focus:outline-none"
          >
            {CONFIDENCES.map((c) => (
              <option key={c} value={c}>
                {c}
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
            {mutation.isPending ? "保存中..." : "保存"}
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
