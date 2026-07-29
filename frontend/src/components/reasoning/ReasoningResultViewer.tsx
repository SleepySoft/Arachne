import { useEffect, useMemo, useRef, useState, type ReactNode } from "react";
import { AlertTriangle, ChevronRight, Database, GitBranch, Layers, Table2 } from "lucide-react";
import {
  CompanyExposuresOutput,
  EdgeScore,
  EvidenceChain,
  FeatureTable,
  NodeScore,
  ReasoningPath,
  ReasoningResultEnvelope,
  ReasoningSubgraph,
  TaskType,
  TemporaryReasoningGraph,
  EDGE_TYPE_LABELS,
} from "@/types";
import { OUTPUT_OPTIONS, type ResultTab } from "./config";
import { cn, Badge } from "./ui";
import cytoscape from "cytoscape";
import cytoscapeDagre from "cytoscape-dagre";

cytoscape.use(cytoscapeDagre);

interface ReasoningResultViewerProps {
  result: ReasoningResultEnvelope;
  isFlowEngine: boolean;
  seedLabels: string[];
  onDeepDive: (nodeId: string, label: string) => void;
  onRunWithEngine: (engine: string) => void;
}

export function ReasoningResultViewer({
  result,
  isFlowEngine,
  seedLabels,
  onDeepDive,
  onRunWithEngine,
}: ReasoningResultViewerProps) {
  const [activeTab, setActiveTab] = useState<ResultTab>("overview");
  const taskType = (result.task_type as TaskType) || "association";

  useEffect(() => {
    const payload = result.result_payload;
    const hasStory =
      ((payload.paths as unknown[] | undefined)?.length ?? 0) > 0 ||
      ((payload.node_scores as unknown[] | undefined)?.length ?? 0) > 0;
    const hasGraph = !!payload.subgraph || !!payload.temporary_graph;
    setActiveTab(hasStory ? "story" : hasGraph ? "visual" : "overview");
  }, [result]);

  const resultGraph: ReasoningSubgraph | TemporaryReasoningGraph | null = useMemo(() => {
    if (!result) return null;
    const payload = result.result_payload;
    if (activeTab === "subgraph" && payload.subgraph) {
      return payload.subgraph as ReasoningSubgraph;
    }
    if (activeTab === "temporary_graph" && payload.temporary_graph) {
      return payload.temporary_graph as TemporaryReasoningGraph;
    }
    // If current tab is overview but graph outputs exist, prefer the first available graph
    if (payload.subgraph) return payload.subgraph as ReasoningSubgraph;
    if (payload.temporary_graph) return payload.temporary_graph as TemporaryReasoningGraph;
    return null;
  }, [result, activeTab]);

  const resultPaths = useMemo<ReasoningPath[]>(() => {
    if (!result?.result_payload.paths) return [];
    return (result.result_payload.paths as { paths: ReasoningPath[] }).paths || [];
  }, [result]);

  const resultNodeScores = useMemo<NodeScore[]>(() => {
    return (result?.result_payload.node_scores as NodeScore[]) || [];
  }, [result]);

  const resultEdgeScores = useMemo<EdgeScore[]>(() => {
    return (result?.result_payload.edge_scores as EdgeScore[]) || [];
  }, [result]);

  const resultEvidenceChains = useMemo<EvidenceChain[]>(() => {
    return (result?.result_payload.evidence_chains as EvidenceChain[]) || [];
  }, [result]);

  const resultFeatureTables = useMemo<FeatureTable[]>(() => {
    return (result?.result_payload.feature_tables as FeatureTable[]) || [];
  }, [result]);

  const resultCompanyExposures = useMemo<CompanyExposuresOutput | null>(() => {
    return (result?.result_payload.company_exposures as CompanyExposuresOutput) || null;
  }, [result]);

  const resultNodeCounts = useMemo<Record<string, number> | null>(() => {
    return (result?.result_payload.node_counts as Record<string, number>) || null;
  }, [result]);

  const availableTabs = useMemo(() => {
    const set = new Set<ResultTab>(["overview"]);
    if (!result) return set;
    const payload = result.result_payload;
    if (
      ((payload.paths as unknown[] | undefined)?.length ?? 0) > 0 ||
      ((payload.node_scores as unknown[] | undefined)?.length ?? 0) > 0
    )
      set.add("story");
    if (payload.subgraph || payload.temporary_graph) set.add("visual");
    if (payload.subgraph) set.add("subgraph");
    if (payload.temporary_graph) set.add("temporary_graph");
    if (payload.paths) set.add("paths");
    if (payload.node_scores) set.add("node_scores");
    if (payload.edge_scores) set.add("edge_scores");
    if (payload.evidence_chains) set.add("evidence_chains");
    if (payload.feature_tables) set.add("feature_tables");
    if (payload.company_exposures) set.add("company_exposures");
    return set;
  }, [result]);

  const tabLabel = (t: ResultTab) => {
    if (t === "story") return "解读";
    if (t === "overview") return "概览";
    if (t === "visual") return "可视化图";
    if (t === "company_exposures") return "公司暴露";
    return OUTPUT_OPTIONS.find((o) => o.value === t)?.label || t;
  };

  return (
            <>
              {/* Tabs */}
              <div className="flex items-center gap-1 border-b border-slate-800 bg-slate-900/50 px-4 py-2">
                {(["story", "overview", ...Array.from(availableTabs).filter((t) => t !== "overview" && t !== "story")] as ResultTab[])
                  .filter((t) => availableTabs.has(t))
                  .map((t) => (
                  <button
                    key={t}
                    onClick={() => setActiveTab(t)}
                    className={cn(
                      "rounded px-3 py-1.5 text-xs font-medium transition-colors",
                      activeTab === t
                        ? "bg-cyan-600 text-white"
                        : "text-slate-400 hover:bg-slate-800 hover:text-slate-200"
                    )}
                  >
                    {tabLabel(t)}
                  </button>
                ))}
              </div>

              {/* Tab content */}
              <div className="flex-1 overflow-auto p-6">
                {result.status !== "success" && (
                  <NoResultView
                    result={result}
                    isFlowEngine={isFlowEngine}
                    onDeepDive={onDeepDive}
                    onRunWithEngine={onRunWithEngine}
                  />
                )}
                {result.status === "success" && activeTab === "story" && (
                  <StoryView
                    result={result}
                    onDeepDive={onDeepDive}
                    onShowCompanies={() => setActiveTab("company_exposures")}
                    onShowGraph={() => setActiveTab("visual")}
                  />
                )}
                {result.status === "success" && activeTab === "overview" && (
                  <div className="space-y-4">
                    <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
                      <h4 className="mb-1 text-sm font-medium text-slate-200">结果说明</h4>
                      <p className="text-xs leading-5 text-slate-400">
                        从起点{" "}
                        <span className="font-medium text-cyan-300">
                          {seedLabels.join("、")}
                        </span>{" "}
                        执行{" "}
                        <span className="font-medium text-cyan-300">
                          {taskType === "association" ? "关联扩展" : "影响传播"}
                        </span>
                        ，共发现{" "}
                        <span className="font-medium text-slate-200">
                          {resultGraph
                            ? `${
                                "nodes" in resultGraph
                                  ? resultGraph.nodes.length
                                  : (resultGraph as TemporaryReasoningGraph).nodes.length
                              } 个节点、${
                                "edges" in resultGraph
                                  ? resultGraph.edges.length
                                  : (resultGraph as TemporaryReasoningGraph).edges.length
                              } 条边`
                            : "—"}
                        </span>
                        ，找到 {resultPaths.length} 条路径。
                        {taskType === "association" && "关联扩展用于发现与起点相关的上下游节点和关系。"}
                        {taskType === "impact_propagation" && "影响传播用于量化上游扰动沿供应链向下传递的强度。"}
                        {taskType === "bottleneck_detection" && "瓶颈检测用于找出被多条路径共享、替代来源少的关键节点。"}
                        {taskType === "substitution_search" && "替代搜索用于基于物料谱系和结构相似性寻找可替代节点。"}
                        {taskType === "candidate_discovery" && "候选发现用于识别图中可能缺失的工艺节点或关系。"}
                        {taskType === "cross_graph_context" && "跨图上下文用于把产业节点关联到公司、行业和关键人员。"}
                      </p>
                    </div>

                    <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
                      <SummaryCard
                      icon={<Layers className="h-4 w-4 text-cyan-400" />}
                      label="图结构"
                      value={
                        result.result_payload.subgraph || result.result_payload.temporary_graph
                          ? "有"
                          : "无"
                      }
                    />
                    <SummaryCard
                      icon={<GitBranch className="h-4 w-4 text-amber-400" />}
                      label="路径数"
                      value={String(resultPaths.length)}
                    />
                    <SummaryCard
                      icon={<Database className="h-4 w-4 text-emerald-400" />}
                      label="证据链"
                      value={String(resultEvidenceChains.length)}
                    />
                    <SummaryCard
                      icon={<Table2 className="h-4 w-4 text-purple-400" />}
                      label="特征表"
                      value={String(resultFeatureTables.length)}
                    />
                    {result.diagnostics.warnings.length > 0 && (
                      <div className="col-span-2 lg:col-span-4 rounded border border-amber-900/30 bg-amber-950/20 p-3 text-xs text-amber-300">
                        <div className="mb-1 font-medium">诊断警告</div>
                        <ul className="list-inside list-disc space-y-0.5">
                          {result.diagnostics.warnings.map((w, i) => (
                            <li key={i}>{w}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
                )}

                {activeTab === "visual" && resultGraph && (
                  <div className="flex h-[calc(100%-1rem)] flex-col gap-2">
                    {"temp_graph_id" in resultGraph && resultNodeCounts && (
                      <div className="flex flex-wrap items-center gap-x-3 gap-y-1 rounded-lg border border-slate-800 bg-slate-900/60 px-3 py-2 text-[10px] text-slate-400">
                        <span>
                          主线 <b className="text-slate-200">{resultNodeCounts.main ?? 0}</b>
                        </span>
                        <span>
                          工艺 <b className="text-violet-300">{resultNodeCounts.method ?? 0}</b>
                        </span>
                        <span>
                          协同投入 <b className="text-slate-200">{resultNodeCounts.support ?? 0}</b>
                        </span>
                        <span>
                          支线关联 <b className="text-sky-300">{resultNodeCounts.branch ?? 0}</b>
                        </span>
                        {resultCompanyExposures && (
                          <span>
                            关联公司 <b className="text-amber-300">{resultCompanyExposures.total_companies}</b>
                          </span>
                        )}
                        <span className="text-slate-600">
                          黄框为起点；沿主线从左到右阅读，支线/协同为辅助信息
                        </span>
                      </div>
                    )}
                    <div className="min-h-0 flex-1 rounded-lg border border-slate-800 bg-slate-900/60 p-2">
                      <ResultGraph graph={resultGraph} isTemp={"temp_graph_id" in resultGraph} />
                    </div>
                  </div>
                )}

                {(activeTab === "subgraph" || activeTab === "temporary_graph") && resultGraph && (
                  <GraphView data={resultGraph} isTemp={activeTab === "temporary_graph"} />
                )}

                {activeTab === "paths" && <PathsView paths={resultPaths} />}
                {activeTab === "node_scores" && <NodeScoresView scores={resultNodeScores} />}
                {activeTab === "edge_scores" && <EdgeScoresView scores={resultEdgeScores} />}
                {activeTab === "evidence_chains" && <EvidenceChainsView chains={resultEvidenceChains} />}
                {activeTab === "feature_tables" && <FeatureTablesView tables={resultFeatureTables} />}
                {activeTab === "company_exposures" && resultCompanyExposures && (
                  <CompanyExposuresView data={resultCompanyExposures} />
                )}
              </div>
            </>
  );
}

function SummaryCard({
  icon,
  label,
  value,
}: {
  icon: ReactNode;
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
      <div className="mb-2 flex items-center gap-2 text-[10px] font-medium uppercase tracking-wider text-slate-500">
        {icon}
        {label}
      </div>
      <div className="text-xl font-semibold text-slate-200">{value}</div>
    </div>
  );
}

function GraphView({
  data,
  isTemp,
}: {
  data: ReasoningSubgraph | TemporaryReasoningGraph;
  isTemp: boolean;
}) {
  const nodes = isTemp
    ? (data as TemporaryReasoningGraph).nodes.map((n) => ({
        id: n.temp_node_id,
        label: n.label,
        type: n.node_type,
        score: n.score,
      }))
    : (data as ReasoningSubgraph).nodes.map((n) => ({
        id: n.node_id,
        label: n.canonical_name_zh || n.node_id,
        type: n.entity_type,
        score: undefined,
      }));

  const edges = isTemp
    ? (data as TemporaryReasoningGraph).edges.map((e) => ({
        id: e.temp_edge_id,
        from: e.from_temp_node_id,
        to: e.to_temp_node_id,
        type: e.edge_type,
        weight: e.weight,
      }))
    : (data as ReasoningSubgraph).edges.map((e) => ({
        id: e.edge_id,
        from: e.from_node,
        to: e.to_node,
        type: e.edge_type,
        weight: undefined,
      }));

  return (
    <div className="space-y-4">
      <div className="text-xs text-slate-500">
        共 {nodes.length} 个节点，{edges.length} 条边
        {isTemp && "（临时推理图，含得分/权重）"}
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div className="rounded-lg border border-slate-800 bg-slate-900/60">
          <div className="border-b border-slate-800 px-4 py-2 text-xs font-medium text-slate-300">节点</div>
          <div className="max-h-96 overflow-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-900 text-slate-500">
                <tr>
                  <th className="px-3 py-2">ID</th>
                  <th className="px-3 py-2">名称</th>
                  <th className="px-3 py-2">类型</th>
                  {isTemp && <th className="px-3 py-2">得分</th>}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {nodes.map((n) => (
                  <tr key={n.id} className="hover:bg-slate-800/40">
                    <td className="px-3 py-2 font-mono text-slate-400">{n.id}</td>
                    <td className="px-3 py-2 text-slate-200">{n.label}</td>
                    <td className="px-3 py-2">
                      <Badge color="cyan">{n.type}</Badge>
                    </td>
                    {isTemp && <td className="px-3 py-2">{formatScore(n.score)}</td>}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="rounded-lg border border-slate-800 bg-slate-900/60">
          <div className="border-b border-slate-800 px-4 py-2 text-xs font-medium text-slate-300">边</div>
          <div className="max-h-96 overflow-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-900 text-slate-500">
                <tr>
                  <th className="px-3 py-2">ID</th>
                  <th className="px-3 py-2">起点</th>
                  <th className="px-3 py-2">终点</th>
                  <th className="px-3 py-2">类型</th>
                  {isTemp && <th className="px-3 py-2">权重</th>}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {edges.map((e) => (
                  <tr key={e.id} className="hover:bg-slate-800/40">
                    <td className="px-3 py-2 font-mono text-slate-400">{e.id}</td>
                    <td className="px-3 py-2 text-slate-300">{e.from}</td>
                    <td className="px-3 py-2 text-slate-300">{e.to}</td>
                    <td className="px-3 py-2">
                      <Badge color="amber">{e.type}</Badge>
                    </td>
                    {isTemp && <td className="px-3 py-2">{formatScore(e.weight)}</td>}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

function ResultGraph({
  graph,
  isTemp,
}: {
  graph: ReasoningSubgraph | TemporaryReasoningGraph;
  isTemp: boolean;
}) {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<cytoscape.Core | null>(null);

  const nodeColor = (type?: string) => {
    const map: Record<string, string> = {
      material: "#f59e0b",
      part: "#38bdf8",
      device: "#a78bfa",
      equipment: "#34d399",
      system: "#f472b6",
      software: "#818cf8",
      infrastructure: "#94a3b8",
      process: "#fb923c",
      service: "#2dd4bf",
      technology_capability: "#c084fc",
      platform: "#60a5fa",
      standard: "#a3e635",
      data_asset: "#fbbf24",
      unknown: "#64748b",
    };
    return map[type || "unknown"] || "#64748b";
  };

  const elements = useMemo(() => {
    const nodes = isTemp
      ? (graph as TemporaryReasoningGraph).nodes.map((n) => ({
          data: {
            id: n.temp_node_id,
            label: n.label,
            type: n.node_type,
            score: n.score,
            line: n.properties?.line as string | undefined,
          },
        }))
      : (graph as ReasoningSubgraph).nodes.map((n) => ({
          data: {
            id: n.node_id,
            label: n.canonical_name_zh || n.node_id,
            type: n.entity_type,
          },
        }));
    const edges = isTemp
      ? (graph as TemporaryReasoningGraph).edges.map((e) => ({
          data: {
            id: e.temp_edge_id,
            source: e.from_temp_node_id,
            target: e.to_temp_node_id,
            type: EDGE_TYPE_LABELS[e.edge_type] ?? e.edge_type,
            weight: e.weight,
            line: e.properties?.line as string | undefined,
          },
        }))
      : (graph as ReasoningSubgraph).edges.map((e) => ({
          data: {
            id: e.edge_id,
            source: e.from_node,
            target: e.to_node,
            type: EDGE_TYPE_LABELS[e.edge_type ?? ""] ?? e.edge_type,
          },
        }));
    return [...nodes, ...edges];
  }, [graph, isTemp]);

  useEffect(() => {
    if (!containerRef.current) return;

    const cy = cytoscape({
      container: containerRef.current,
      elements,
      style: [
        {
          selector: "node",
          style: {
            label: "data(label)",
            "background-color": "data(color)",
            color: "#e2e8f0",
            "font-size": "10px",
            "text-valign": "bottom",
            "text-halign": "center",
            "text-margin-y": "4px",
            "text-background-color": "#0f172a",
            "text-background-opacity": 0.8,
            "text-background-padding": "2px 4px",
            "text-background-shape": "roundrectangle",
            width: 24,
            height: 24,
            "border-width": 2,
            "border-color": "#1e293b",
          } as unknown as cytoscape.Css.Node,
        },
        {
          selector: "edge",
          style: {
            width: 2,
            "line-color": "#475569",
            "target-arrow-color": "#475569",
            "target-arrow-shape": "triangle",
            "arrow-scale": 0.8,
            "curve-style": "bezier",
            label: "data(type)",
            "font-size": "8px",
            color: "#94a3b8",
            "text-background-color": "#0f172a",
            "text-background-opacity": 0.8,
            "text-background-padding": "1px 3px",
            "text-background-shape": "roundrectangle",
          } as unknown as cytoscape.Css.Edge,
        },
        // ---- 主线/支线视觉编码（仅 flow 临时图带 line 属性）----
        {
          selector: 'edge[line = "branch"]',
          style: {
            label: "",
            "line-style": "dashed",
            "line-color": "#38bdf8",
            "target-arrow-color": "#38bdf8",
            opacity: 0.65,
            width: 1,
          } as unknown as cytoscape.Css.Edge,
        },
        {
          selector: 'edge[line = "support"]',
          style: {
            label: "",
            "line-color": "#475569",
            "target-arrow-color": "#475569",
            opacity: 0.5,
            width: 1,
          } as unknown as cytoscape.Css.Edge,
        },
        {
          selector: 'edge[line = "method"]',
          style: {
            "line-style": "dashed",
            "line-color": "#a78bfa",
            "target-arrow-color": "#a78bfa",
            width: 1,
          } as unknown as cytoscape.Css.Edge,
        },
        {
          // 起点：空心圆圈（透明填充 + 粗边框 + 加大），在密集图里一眼可辨
          selector: 'node[line = "seed"]',
          style: {
            "background-fill": "hollow",
            "border-color": "#facc15",
            "border-width": 5,
            width: 36,
            height: 36,
          } as unknown as cytoscape.Css.Node,
        },
        {
          selector: 'node[line = "support"]',
          style: {
            width: 16,
            height: 16,
            opacity: 0.75,
            "font-size": "8px",
          } as unknown as cytoscape.Css.Node,
        },
        {
          selector: 'node[line = "branch"]',
          style: {
            width: 18,
            height: 18,
            "border-color": "#38bdf8",
            "font-size": "9px",
          } as unknown as cytoscape.Css.Node,
        },
        {
          selector: 'node[line = "method"]',
          style: {
            shape: "hexagon",
          } as unknown as cytoscape.Css.Node,
        },
      ],
      minZoom: 0.1,
      maxZoom: 3,
      wheelSensitivity: 1.0,
    });

    // Set node colors after init so we can use our helper
    cy.nodes().forEach((n) => {
      n.data("color", nodeColor(n.data("type")));
    });

    // Explicitly run the layout; the `layout` init option does not always execute.
    const layout = cy.layout({
      name: "dagre",
      rankDir: "LR",
      padding: 20,
      animate: false,
      fit: false,
    } as cytoscape.LayoutOptions);
    layout.on("layoutstop", () => {
      cy.fit(undefined, 24);
    });
    layout.run();

    cyRef.current = cy;

    return () => {
      cy.destroy();
      cyRef.current = null;
    };
  }, [elements]);

  return (
    <div className="relative h-full w-full">
      <div ref={containerRef} className="h-full w-full" />
      {isTemp && (
        <div className="pointer-events-none absolute left-2 top-2 space-y-1 rounded bg-slate-950/80 px-2 py-1.5 text-[10px] text-slate-400">
          <div className="flex items-center gap-1.5">
            <span className="inline-block h-0.5 w-4 rounded" style={{ backgroundColor: "#64748b" }} />
            主线（物料转化链，1 阶段 = 资源→动作→资源）
          </div>
          <div className="flex items-center gap-1.5">
            <span
              className="inline-block h-0 w-4 border-t border-dashed"
              style={{ borderColor: "#a78bfa" }}
            />
            工艺引用（动作 → 方法）
          </div>
          <div className="flex items-center gap-1.5">
            <span className="inline-block h-0.5 w-4 rounded" style={{ backgroundColor: "#475569" }} />
            协同投入（该阶段还需要的物料/设备）
          </div>
          <div className="flex items-center gap-1.5">
            <span
              className="inline-block h-0 w-4 border-t border-dashed"
              style={{ borderColor: "#38bdf8" }}
            />
            支线（同工艺的其他流程及其物料）
          </div>
          <div className="flex items-center gap-1.5">
            <span
              className="inline-block h-2.5 w-2.5 rounded-full border-2"
              style={{ borderColor: "#facc15" }}
            />
            起点（空心圆圈）
          </div>
        </div>
      )}
    </div>
  );
}

function PathsView({ paths }: { paths: ReasoningPath[] }) {
  if (paths.length === 0) return <Empty message="无路径" />;
  return (
    <div className="space-y-3">
      {paths.map((p) => (
        <div key={p.path_id} className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
          <div className="mb-2 flex items-center justify-between">
            <span className="font-mono text-[10px] text-slate-500">{p.path_id}</span>
            <Badge color="emerald">score {formatScore(p.path_score)}</Badge>
          </div>
          <div className="flex flex-wrap items-center gap-1 text-xs">
            {p.node_sequence.map((nid, idx) => {
              const name =
                p.node_name_map?.[nid]?.canonical_name_zh ||
                p.node_name_map?.[nid]?.canonical_name_en ||
                nid;
              return (
                <span key={idx} className="flex items-center gap-1">
                  <span className="rounded bg-slate-800 px-2 py-1 text-slate-200" title={nid}>
                    {name}
                  </span>
                  {idx < p.node_sequence.length - 1 && (
                    <ChevronRight className="h-3 w-3 text-slate-600" />
                  )}
                </span>
              );
            })}
          </div>
          <div className="mt-2 text-[10px] text-slate-500">
            长度 {p.path_length} · 边 {p.edge_sequence.join(", ")}
          </div>
        </div>
      ))}
    </div>
  );
}

function NodeScoresView({ scores }: { scores: NodeScore[] }) {
  if (scores.length === 0) return <Empty message="无节点得分" />;
  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900/60">
      <table className="w-full text-left text-xs">
        <thead className="bg-slate-900 text-slate-500">
          <tr>
            <th className="px-3 py-2">排名</th>
            <th className="px-3 py-2">节点</th>
            <th className="px-3 py-2">名称</th>
            <th className="px-3 py-2">类型</th>
            <th className="px-3 py-2">得分</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800">
          {scores.map((s) => (
            <tr key={s.node_id} className="hover:bg-slate-800/40">
              <td className="px-3 py-2">{s.rank}</td>
              <td className="px-3 py-2 font-mono text-slate-300">{s.node_id}</td>
              <td className="px-3 py-2 text-slate-200">
                {s.canonical_name_zh || s.canonical_name_en || "—"}
              </td>
              <td className="px-3 py-2">
                <Badge color="cyan">{s.entity_type}</Badge>
              </td>
              <td className="px-3 py-2 font-semibold text-cyan-300">{formatScore(s.score)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function EdgeScoresView({ scores }: { scores: EdgeScore[] }) {
  if (scores.length === 0) return <Empty message="无边得分" />;
  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900/60">
      <table className="w-full text-left text-xs">
        <thead className="bg-slate-900 text-slate-500">
          <tr>
            <th className="px-3 py-2">排名</th>
            <th className="px-3 py-2">边</th>
            <th className="px-3 py-2">起点</th>
            <th className="px-3 py-2">终点</th>
            <th className="px-3 py-2">类型</th>
            <th className="px-3 py-2">得分</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800">
          {scores.map((s) => (
            <tr key={s.edge_id} className="hover:bg-slate-800/40">
              <td className="px-3 py-2">{s.rank}</td>
              <td className="px-3 py-2 font-mono text-slate-300">{s.edge_id}</td>
              <td className="px-3 py-2 text-slate-200">
                {s.from_node_name_zh || s.from_node_name_en || s.from_node || "—"}
              </td>
              <td className="px-3 py-2 text-slate-200">
                {s.to_node_name_zh || s.to_node_name_en || s.to_node || "—"}
              </td>
              <td className="px-3 py-2">
                <Badge color="amber">{s.edge_type}</Badge>
              </td>
              <td className="px-3 py-2 font-semibold text-cyan-300">{formatScore(s.score)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function EvidenceChainsView({ chains }: { chains: EvidenceChain[] }) {
  if (chains.length === 0) return <Empty message="无证据链" />;
  return (
    <div className="space-y-3">
      {chains.map((c) => (
        <div key={c.evidence_chain_id} className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
          <div className="mb-2 flex items-center justify-between">
            <span className="font-mono text-[10px] text-slate-500">{c.evidence_chain_id}</span>
            <div className="flex gap-2">
              <Badge color="cyan">{c.supports}</Badge>
              <Badge color={c.completeness === "complete" ? "emerald" : "amber"}>
                {c.completeness}
              </Badge>
            </div>
          </div>
          <div className="mb-2 text-xs text-slate-300">目标：{c.target_id}</div>
          <div className="space-y-2">
            {c.evidence_items.map((item, idx) => (
              <div key={idx} className="rounded border border-slate-800 bg-slate-900 p-2 text-xs">
                <div className="font-medium text-slate-200">{item.source_title}</div>
                {item.quote && <div className="mt-1 text-slate-400">{item.quote}</div>}
                {item.source_url && (
                  <a
                    href={item.source_url}
                    target="_blank"
                    rel="noreferrer"
                    className="mt-1 block truncate text-[10px] text-cyan-400 hover:underline"
                  >
                    {item.source_url}
                  </a>
                )}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

function FeatureTablesView({ tables }: { tables: FeatureTable[] }) {
  if (tables.length === 0) return <Empty message="无特征表" />;
  return (
    <div className="space-y-6">
      {tables.map((t) => (
        <div key={t.table_id} className="rounded-lg border border-slate-800 bg-slate-900/60">
          <div className="border-b border-slate-800 px-4 py-2 text-xs font-medium text-slate-300">
            {t.table_id} <Badge color="slate">{t.entity_level}</Badge>{" "}
            <span className="text-slate-500">{t.rows.length} 行</span>
          </div>
          <div className="overflow-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-900 text-slate-500">
                <tr>
                  {t.columns.slice(0, 12).map((col) => (
                    <th key={String(col)} className="whitespace-nowrap px-3 py-2">
                      {String(col)}
                    </th>
                  ))}
                  {t.columns.length > 12 && (
                    <th className="px-3 py-2">+{t.columns.length - 12} 列</th>
                  )}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {t.rows.slice(0, 20).map((row, idx) => (
                  <tr key={idx} className="hover:bg-slate-800/40">
                    {t.columns.slice(0, 12).map((col) => (
                      <td key={String(col)} className="whitespace-nowrap px-3 py-2 text-slate-300">
                        {formatCell(row[col])}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
            {t.rows.length > 20 && (
              <div className="px-3 py-2 text-[10px] text-slate-500">还有 {t.rows.length - 20} 行未显示</div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

function CompanyExposuresView({ data }: { data: CompanyExposuresOutput }) {
  if (data.companies.length === 0) return <Empty message="无公司暴露" />;
  return (
    <div className="space-y-4">
      <div className="text-xs text-slate-500">
        共 {data.total_companies} 家公司、{data.total_exposures} 条暴露记录
      </div>
      {data.companies.map((c) => (
        <div key={c.company_id} className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
          <div className="mb-2 flex items-center justify-between">
            <div>
              <div className="text-sm font-medium text-slate-200">
                {c.name_zh || c.name_en || c.company_id}
              </div>
              <div className="text-[10px] text-slate-500">{c.company_id}</div>
            </div>
            <div className="flex gap-2">
              {c.stock_codes?.map((code) => (
                <Badge key={code} color="slate">
                  {code}
                </Badge>
              ))}
              {c.company_type && <Badge color="cyan">{c.company_type}</Badge>}
            </div>
          </div>
          <div className="flex flex-wrap gap-2">
            {c.exposed_nodes.map((n) => (
              <div
                key={n.node_id}
                className="rounded border border-slate-800 bg-slate-900 px-2 py-1 text-xs"
                title={n.node_id}
              >
                <span className="text-slate-200">
                  {n.canonical_name_zh || n.canonical_name_en || n.node_id}
                </span>
                {n.activity_type && (
                  <span className="ml-1 text-[10px] text-slate-500">({n.activity_type})</span>
                )}
                {n.weight !== undefined && (
                  <span className="ml-1 text-[10px] text-cyan-400">w{n.weight}</span>
                )}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

function formatCell(value: unknown): string {
  if (value === null || value === undefined) return "—";
  if (typeof value === "boolean") return value ? "true" : "false";
  if (typeof value === "object") return JSON.stringify(value).slice(0, 80);
  return String(value).slice(0, 80);
}

function formatScore(value: number | null | undefined, digits = 3): string {
  if (value === null || value === undefined || Number.isNaN(value)) return "—";
  return value.toFixed(digits);
}

function Empty({ message }: { message: string }) {
  return (
    <div className="flex flex-1 items-center justify-center text-sm text-slate-500">{message}</div>
  );
}

// ============================================================
// StoryView：把推理结果转译成可读的“故事”
// ============================================================

interface StoryFinding {
  nodeId: string;
  name: string;
  text: string;
  color: "cyan" | "amber" | "emerald";
}

function StoryView({
  result,
  onDeepDive,
  onShowCompanies,
  onShowGraph,
}: {
  result: ReasoningResultEnvelope;
  onDeepDive: (nodeId: string, label: string) => void;
  onShowCompanies: () => void;
  onShowGraph: () => void;
}) {
  const payload = result.result_payload;
  const paths = (payload.paths as ReasoningPath[] | undefined) ?? [];
  const scores = (payload.node_scores as NodeScore[] | undefined) ?? [];
  const counts = (payload.node_counts as Record<string, number> | undefined) ?? null;
  const companies =
    (payload.company_exposures as CompanyExposuresOutput | undefined) ?? null;
  const tempGraph = (payload.temporary_graph as TemporaryReasoningGraph | undefined) ?? null;

  // 名称解析：路径 name_map + 得分 + 临时图 label
  const nameOf = (() => {
    const map = new Map<string, string>();
    paths.forEach((p) => {
      Object.entries(p.node_name_map || {}).forEach(([nid, info]) => {
        const nm = info?.canonical_name_zh || info?.canonical_name_en;
        if (nm && !map.has(nid)) map.set(nid, nm);
      });
    });
    scores.forEach((s) => {
      const nm = s.canonical_name_zh || s.canonical_name_en;
      if (nm && !map.has(s.node_id)) map.set(s.node_id, nm);
    });
    tempGraph?.nodes.forEach((n) => {
      if (n.label && !map.has(n.temp_node_id)) map.set(n.temp_node_id, n.label);
    });
    return (nid: string) => map.get(nid) || nid.split(":").pop() || nid;
  })();

  const seedIds = (payload.seed_nodes as string[] | undefined) ?? [];
  const seedNames = seedIds.map(nameOf).join("、");

  // 主线链：最长的 3 条路径，按终点去重
  const mainChains = [...paths]
    .sort((a, b) => b.node_sequence.length - a.node_sequence.length)
    .filter((p, i, arr) => arr.findIndex((q) => q.end_node_id === p.end_node_id) === i)
    .slice(0, 3);

  // 关键发现
  const findings: StoryFinding[] = [];
  const hubResources = scores.filter(
    (s) =>
      (s.score_components?.line === "main" || s.score_components?.line === "seed") &&
      ((s.score_components?.main_actions as number | undefined) ?? 0) >= 2
  );
  hubResources.slice(0, 3).forEach((s) => {
    findings.push({
      nodeId: s.node_id,
      name: nameOf(s.node_id),
      text: `连接 ${s.score_components?.main_actions} 个主线环节，是多条产品链的交汇点。它的供应波动会沿多条链传导。`,
      color: "cyan",
    });
  });
  const sharedMethods = scores.filter(
    (s) =>
      s.score_components?.line === "method" &&
      ((s.score_components?.branch_links as number | undefined) ?? 0) >= 1
  );
  sharedMethods.slice(0, 2).forEach((s) => {
    findings.push({
      nodeId: s.node_id,
      name: nameOf(s.node_id),
      text: `共享工艺：被 ${s.score_components?.branch_links} 个流程使用。同一工艺横向迁移可能带来新的应用市场。`,
      color: "amber",
    });
  });
  const branchMaterials = scores.filter((s) => s.score_components?.line === "branch");
  if (branchMaterials.length > 0) {
    findings.push({
      nodeId: branchMaterials[0].node_id,
      name: nameOf(branchMaterials[0].node_id),
      text: `支线共发现 ${branchMaterials.length} 种关联物料（来自同工艺的其他流程），可作为替代与协同线索。`,
      color: "emerald",
    });
  }

  const topCompanies = [...(companies?.companies ?? [])]
    .sort((a, b) => (b.exposed_nodes?.length ?? 0) - (a.exposed_nodes?.length ?? 0))
    .slice(0, 5);

  // 公司产业上下文（cross_graph_context 任务）
  interface CtxCompany {
    company_id: string;
    name_zh?: string | null;
    stock_codes?: string[];
    nodes: { node_id: string; label: string; activity_type?: string | null }[];
  }
  const companyCtx = payload.company_context as
    | {
        seed_companies: ({
          position: { node_id: string; label: string; activity_type?: string | null }[];
          in_flow_node_count: number;
          exposed_node_count: number;
        } & CtxCompany)[];
        peers: CtxCompany[];
        related_companies?: CtxCompany[];
        upstream_companies: CtxCompany[];
        downstream_companies: CtxCompany[];
      }
    | undefined;

  const companySection = (title: string, items: CtxCompany[] | undefined, color: string) =>
    items && items.length > 0 ? (
      <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
        <h4 className="mb-2 text-sm font-medium text-slate-200">
          {title} <span className="text-slate-500">（{items.length}）</span>
        </h4>
        <div className="flex flex-wrap gap-2 text-xs">
          {items.slice(0, 12).map((c) => (
            <button
              key={c.company_id}
              onClick={() => onDeepDive(c.company_id, c.name_zh || c.company_id)}
              className={`rounded px-2 py-1 ${color} hover:brightness-125`}
              title={c.nodes.map((n) => n.label).join("、")}
            >
              {c.name_zh || c.company_id}
              <span className="ml-1 opacity-70">
                · {c.nodes.slice(0, 2).map((n) => n.label).join("、")}
                {c.nodes.length > 2 ? ` +${c.nodes.length - 2}` : ""}
              </span>
            </button>
          ))}
        </div>
        <p className="mt-2 text-[10px] text-slate-600">
          公司名后为其暴露的环节；同一家公司可能因多环节布局同时出现在多个分类中（纵向一体化）。
        </p>
      </div>
    ) : null;

  return (
    <div className="max-w-3xl space-y-4">
      {/* 一句话概览 */}
      <div className="rounded-lg border border-cyan-900/40 bg-cyan-950/20 p-4">
        <p className="text-sm leading-6 text-slate-200">
          以 <span className="font-semibold text-cyan-300">「{seedNames}」</span> 为起点
          {counts ? (
            <>
              ，主线覆盖 <b>{counts.main ?? 0}</b> 个环节、<b>{counts.method ?? 0}</b> 种工艺，
              另有 <b>{counts.support ?? 0}</b> 项协同投入和 <b>{counts.branch ?? 0}</b> 项支线关联物料
            </>
          ) : (
            <>，共发现 {paths.length} 条关联路径</>
          )}
          {companies && (
            <>
              ，涉足这些环节的公司共 <b>{companies.total_companies}</b> 家
            </>
          )}
          。
        </p>
      </div>

      {/* 公司产业位置（公司上下文任务） */}
      {companyCtx?.seed_companies?.map((sc) => (
        <div key={sc.company_id} className="rounded-lg border border-amber-900/40 bg-amber-950/20 p-4">
          <h4 className="mb-2 text-sm font-medium text-amber-300">
            {sc.name_zh || sc.company_id} 的产业位置
            <span className="ml-2 text-[10px] font-normal text-slate-500">
              暴露 {sc.exposed_node_count} 个节点，其中 {sc.in_flow_node_count} 个在流程图中
            </span>
          </h4>
          <div className="flex flex-wrap gap-2 text-xs">
            {sc.position.map((p) => (
              <button
                key={p.node_id}
                onClick={() => onDeepDive(p.node_id, p.label)}
                className="rounded bg-slate-800 px-2 py-1 text-slate-200 hover:bg-slate-700"
                title={p.node_id}
              >
                {p.label}
                {p.activity_type && (
                  <span className="ml-1 text-amber-500/80">{String(p.activity_type)}</span>
                )}
              </button>
            ))}
          </div>
        </div>
      ))}

      {companySection("同业公司（同环节同活动）", companyCtx?.peers, "bg-cyan-900/30 text-cyan-300")}
      {companySection("上游公司", companyCtx?.upstream_companies, "bg-emerald-900/30 text-emerald-300")}
      {companySection("下游公司", companyCtx?.downstream_companies, "bg-sky-900/30 text-sky-300")}
      {companySection("相关公司（同工艺/支线配套）", companyCtx?.related_companies, "bg-violet-900/30 text-violet-300")}

      {/* 主线故事 */}
      {mainChains.length > 0 && (
        <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
          <h4 className="mb-2 text-sm font-medium text-slate-200">主线讲了什么</h4>
          <div className="space-y-2">
            {mainChains.map((p) => (
              <div key={p.path_id} className="flex flex-wrap items-center gap-1 text-xs">
                <Badge color="slate">{Math.max(1, Math.floor((p.node_sequence.length - 1) / 2))} 阶段</Badge>
                {p.node_sequence.map((nid, idx) => (
                  <span key={idx} className="flex items-center gap-1">
                    <span
                      className={cn(
                        "rounded px-1.5 py-0.5",
                        idx % 2 === 1
                          ? "bg-orange-900/30 text-orange-300"
                          : "bg-slate-800 text-slate-200"
                      )}
                      title={nid}
                    >
                      {nameOf(nid)}
                    </span>
                    {idx < p.node_sequence.length - 1 && (
                      <ChevronRight className="h-3 w-3 text-slate-600" />
                    )}
                  </span>
                ))}
              </div>
            ))}
          </div>
          <p className="mt-2 text-[10px] text-slate-500">
            橙色为工艺动作，其余为物料/产品；完整路径见「路径」标签页。
          </p>
        </div>
      )}

      {/* 关键发现 */}
      {findings.length > 0 && (
        <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
          <h4 className="mb-2 text-sm font-medium text-slate-200">关键发现</h4>
          <div className="space-y-2">
            {findings.map((f, i) => (
              <div key={i} className="flex items-start justify-between gap-3 text-xs leading-5">
                <p className="text-slate-300">
                  <Badge color={f.color}>{f.name}</Badge>{" "}
                  <span className="text-slate-400">{f.text}</span>
                </p>
                <button
                  onClick={() => onDeepDive(f.nodeId, f.name)}
                  className="shrink-0 rounded bg-slate-800 px-2 py-1 text-[10px] text-cyan-300 hover:bg-slate-700"
                >
                  以此为起点深入
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 产业玩家 */}
      {topCompanies.length > 0 && (
        <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
          <h4 className="mb-2 text-sm font-medium text-slate-200">产业玩家</h4>
          <div className="flex flex-wrap items-center gap-2 text-xs">
            {topCompanies.map((c) => (
              <span key={c.company_id} className="rounded bg-amber-900/20 px-2 py-1 text-amber-300">
                {c.name_zh || c.company_id}
                <span className="ml-1 text-amber-500/70">×{c.exposed_nodes?.length ?? 0}</span>
              </span>
            ))}
            <button
              onClick={onShowCompanies}
              className="rounded bg-slate-800 px-2 py-1 text-[10px] text-slate-300 hover:bg-slate-700"
            >
              查看全部 {companies?.total_companies} 家 →
            </button>
          </div>
        </div>
      )}

      {/* 怎么用 */}
      <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
        <h4 className="mb-2 text-sm font-medium text-slate-200">接下来怎么用</h4>
        <ul className="list-inside list-disc space-y-1 text-xs leading-5 text-slate-400">
          <li>
            点{" "}
            <button onClick={onShowGraph} className="text-cyan-400 hover:underline">
              「可视化图」
            </button>{" "}
            沿主线从左到右阅读：实线是物料转化链，紫色六边形是工艺，灰点是协同投入，蓝虚线是支线。
          </li>
          <li>对某个发现感兴趣？点「以此为起点深入」，会以它为新种子重新推理，看到它的专属故事。</li>
          <li>想看上游供应就切「遍历方向 = backward」，看下游应用就切 forward；调「最大深度」控制故事长度。</li>
          <li>「节点得分」标签页按关联强度排序，得分越高越是枢纽（瓶颈/替代分析优先看它们）。</li>
        </ul>
      </div>
    </div>
  );
}

// ============================================================
// NoResultView：NO_RESULT / FAILED 的明确说明与可操作建议
// ============================================================

interface FlowSuggestion {
  node_id: string;
  label: string;
  score?: number;
}

function NoResultView({
  result,
  isFlowEngine,
  onDeepDive,
  onRunWithEngine,
}: {
  result: ReasoningResultEnvelope;
  isFlowEngine: boolean;
  onDeepDive: (nodeId: string, label: string) => void;
  onRunWithEngine: (engine: string) => void;
}) {
  const warnings = result.diagnostics?.warnings ?? [];
  const suggestions =
    (result.result_payload?.missing_flow_suggestions as FlowSuggestion[] | undefined) ?? [];

  return (
    <div className="max-w-2xl space-y-4">
      <div className="rounded-lg border border-amber-900/40 bg-amber-950/20 p-4">
        <h4 className="mb-1 flex items-center gap-2 text-sm font-medium text-amber-300">
          <AlertTriangle className="h-4 w-4" />
          {result.status === "no_result" ? "没有找到关联结果" : "推理执行失败"}
        </h4>
        {warnings.length > 0 ? (
          <ul className="list-inside list-disc space-y-1 text-xs leading-5 text-slate-400">
            {warnings.map((w, i) => (
              <li key={i}>{w}</li>
            ))}
          </ul>
        ) : (
          <p className="text-xs text-slate-400">起点在当前图中没有任何可遍历的关联。</p>
        )}
      </div>

      {suggestions.length > 0 && (
        <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
          <h4 className="mb-2 text-sm font-medium text-slate-200">
            流程图内存在的相似起点，点击直接推理
          </h4>
          <div className="flex flex-wrap gap-2">
            {suggestions.map((s) => (
              <button
                key={s.node_id}
                onClick={() => onDeepDive(s.node_id, s.label)}
                className="rounded bg-cyan-900/30 px-2 py-1 text-xs text-cyan-300 hover:bg-cyan-900/50"
                title={s.node_id}
              >
                {s.label}
              </button>
            ))}
          </div>
        </div>
      )}

      {isFlowEngine && (
        <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4 text-xs leading-5 text-slate-400">
          <p>
            流程图（arachne-flow）引擎只覆盖已编译流程文件（data/flows/）中的资源与工艺，
            产业图谱中的很多节点（如行业角色、商业模式类节点）不在其中。
          </p>
          <p className="mt-1">
            想对该起点做全产业图推理？
            <button
              onClick={() => onRunWithEngine("legacy")}
              className="ml-1 rounded bg-slate-800 px-2 py-0.5 text-cyan-300 hover:bg-slate-700"
            >
              切换到产业图（legacy）重跑
            </button>
          </p>
        </div>
      )}
    </div>
  );
}
