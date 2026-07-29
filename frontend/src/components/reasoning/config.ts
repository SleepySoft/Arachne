import type { OutputType } from "@/types";

export const OUTPUT_OPTIONS: { value: OutputType; label: string }[] = [
  { value: "subgraph", label: "子图" },
  { value: "temporary_graph", label: "临时推理图" },
  { value: "paths", label: "路径" },
  { value: "node_scores", label: "节点得分" },
  { value: "edge_scores", label: "边得分" },
  { value: "evidence_chains", label: "证据链" },
  { value: "feature_tables", label: "特征表" },
];

/** arachne_flow 引擎的关联任务实际会产出的输出类型。 */
export const FLOW_OUTPUTS: OutputType[] = ["temporary_graph", "paths", "node_scores"];

export const DEFAULT_OUTPUTS: OutputType[] = [
  "subgraph",
  "paths",
  "evidence_chains",
  "feature_tables",
];

export type ResultTab = OutputType | "overview" | "visual" | "company_exposures" | "story";
