import { useEffect, useMemo, useRef, useState } from "react";
import { useMutation } from "@tanstack/react-query";
import {
  AlertTriangle,
  Brain,
  Check,
  ChevronRight,
  Database,
  GitBranch,
  Layers,
  Loader2,
  Play,
  Plus,
  Search,
  Table2,
  X,
} from "lucide-react";
import {
  ObjectCandidate,
  ObjectQueryRequest,
  OutputType,
  ReasoningResultEnvelope,
  ReasoningTask,
  ReasoningSubgraph,
  ReasoningPath,
  NodeScore,
  EdgeScore,
  EvidenceChain,
  FeatureTable,
  TemporaryReasoningGraph,
  QueryScope,
  TaskType,
  TraversalDirection,
} from "@/types";
import { queryReasoningObjects, executeReasoning } from "@/services/api";
import cytoscape from "cytoscape";
import cytoscapeDagre from "cytoscape-dagre";

cytoscape.use(cytoscapeDagre);

const SCOPE_OPTIONS: { value: QueryScope; label: string }[] = [
  { value: "industrial_node", label: "产业节点" },
  { value: "industrial_edge", label: "产业关系" },
  { value: "factual_node", label: "事实节点" },
  { value: "factual_edge", label: "事实关系" },
  { value: "company", label: "公司" },
  { value: "industry", label: "行业" },
  { value: "claim", label: "断言" },
];

const TASK_OPTIONS: { value: TaskType; label: string }[] = [
  { value: "association", label: "关联扩展" },
  { value: "impact_propagation", label: "影响传播" },
];

const OUTPUT_OPTIONS: { value: OutputType; label: string }[] = [
  { value: "subgraph", label: "子图" },
  { value: "temporary_graph", label: "临时推理图" },
  { value: "paths", label: "路径" },
  { value: "node_scores", label: "节点得分" },
  { value: "edge_scores", label: "边得分" },
  { value: "evidence_chains", label: "证据链" },
  { value: "feature_tables", label: "特征表" },
];

const DEFAULT_OUTPUTS: OutputType[] = [
  "subgraph",
  "paths",
  "evidence_chains",
  "feature_tables",
];

function cn(...classes: (string | false | undefined)[]) {
  return classes.filter(Boolean).join(" ");
}

function FormField({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="space-y-1">
      <label className="text-[10px] font-medium uppercase tracking-wider text-slate-500">{label}</label>
      {children}
    </div>
  );
}

function Card({
  title,
  icon,
  children,
  className,
}: {
  title?: string;
  icon?: React.ReactNode;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("rounded-lg border border-slate-800 bg-slate-900/60", className)}>
      {title && (
        <div className="flex items-center gap-2 border-b border-slate-800 px-4 py-3">
          {icon && <span className="text-slate-400">{icon}</span>}
          <h3 className="text-sm font-medium text-slate-200">{title}</h3>
        </div>
      )}
      <div className="p-4">{children}</div>
    </div>
  );
}

function Badge({
  children,
  color = "slate",
}: {
  children: React.ReactNode;
  color?: "slate" | "cyan" | "amber" | "emerald" | "red";
}) {
  const map = {
    slate: "bg-slate-800 text-slate-300",
    cyan: "bg-cyan-900/40 text-cyan-300",
    amber: "bg-amber-900/40 text-amber-300",
    emerald: "bg-emerald-900/40 text-emerald-300",
    red: "bg-red-900/40 text-red-300",
  };
  return (
    <span className={cn("rounded px-1.5 py-0.5 text-[10px] font-medium", map[color])}>
      {children}
    </span>
  );
}

function formatError(err: unknown, context: string): string {
  let message = context;
  if (err && typeof err === "object" && "response" in err) {
    const axiosErr = err as { response?: { status?: number; statusText?: string; data?: unknown } };
    message += `：${axiosErr.response?.status ?? ""} ${axiosErr.response?.statusText ?? ""}`;
    if (axiosErr.response?.data && typeof axiosErr.response.data === "object") {
      const data = axiosErr.response.data as { detail?: string; message?: string };
      if (data.detail || data.message) message += `（${data.detail || data.message}）`;
    }
  } else if (err instanceof Error) {
    message += `：${err.message}`;
  }
  return message;
}

export function ReasoningPage() {
  // ----- Object query state -----
  const [queryText, setQueryText] = useState("");
  const [queryScope, setQueryScope] = useState<QueryScope>("industrial_node");
  const [candidates, setCandidates] = useState<ObjectCandidate[]>([]);
  const [queryError, setQueryError] = useState<string | null>(null);

  const queryMutation = useMutation({
    mutationFn: (payload: ObjectQueryRequest) => queryReasoningObjects(payload),
    onSuccess: (data) => {
      setQueryError(null);
      setCandidates(data.candidates);
    },
    onError: (err) => setQueryError(formatError(err, "对象查询失败")),
  });

  const handleQuery = () => {
    if (!queryText.trim()) return;
    setQueryError(null);
    queryMutation.mutate({
      query_id: `rq_${Date.now()}`,
      query_text: queryText.trim(),
      query_scope: queryScope,
      limit: 20,
    });
  };

  // ----- Selected sources -----
  const [sources, setSources] = useState<{ object_id: string; label: string }[]>([]);

  const addSource = (c: ObjectCandidate) => {
    const label = c.canonical_name || c.object_id;
    setSources((prev) => {
      if (prev.some((s) => s.object_id === c.object_id)) return prev;
      return [...prev, { object_id: c.object_id, label }];
    });
  };

  const removeSource = (id: string) => {
    setSources((prev) => prev.filter((s) => s.object_id !== id));
  };

  // ----- Task configuration -----
  const [taskType, setTaskType] = useState<TaskType>("association");
  const [maxDepth, setMaxDepth] = useState(2);
  const [maxPaths, setMaxPaths] = useState(50);
  const [maxNodes, setMaxNodes] = useState(200);
  const [traversalDirection, setTraversalDirection] = useState<TraversalDirection>("forward");
  const [propagationProfile, setPropagationProfile] = useState("supply_forward");
  const [outputs, setOutputs] = useState<OutputType[]>(DEFAULT_OUTPUTS);

  useEffect(() => {
    // Suggest sensible defaults per task type
    if (taskType === "association") {
      setOutputs(["subgraph", "paths", "evidence_chains", "feature_tables"]);
    } else if (taskType === "impact_propagation") {
      setOutputs([
        "temporary_graph",
        "paths",
        "node_scores",
        "edge_scores",
        "evidence_chains",
        "feature_tables",
      ]);
    }
  }, [taskType]);

  const toggleOutput = (o: OutputType) => {
    setOutputs((prev) => (prev.includes(o) ? prev.filter((x) => x !== o) : [...prev, o]));
  };

  // ----- Execution -----
  const [result, setResult] = useState<ReasoningResultEnvelope | null>(null);
  const [executeError, setExecuteError] = useState<string | null>(null);
type ResultTab = OutputType | "overview" | "visual";

  const [activeTab, setActiveTab] = useState<ResultTab>("overview");

  const executeMutation = useMutation({
    mutationFn: (payload: ReasoningTask) => executeReasoning(payload),
    onSuccess: (data, variables) => {
      setExecuteError(null);
      setResult(data);
      const hasGraph =
        variables.requested_outputs.includes("subgraph") ||
        variables.requested_outputs.includes("temporary_graph");
      setActiveTab(hasGraph ? "visual" : "overview");
    },
    onError: (err) => setExecuteError(formatError(err, "推理执行失败")),
  });

  const [runningExample, setRunningExample] = useState(false);

  const runExample = async () => {
    try {
      setRunningExample(true);
      setExecuteError(null);
      setQueryText("芯片");
      setQueryScope("industrial_node");
      setTaskType("association");
      setOutputs(["subgraph", "paths", "evidence_chains", "feature_tables"]);

      const queryRes = await queryReasoningObjects({
        query_id: "example",
        query_text: "芯片",
        query_scope: "industrial_node",
        limit: 5,
      });
      const chip = queryRes.candidates.find((c) => c.object_id === "chip") || queryRes.candidates[0];
      if (!chip) {
        setExecuteError("示例查询未返回芯片节点");
        return;
      }
      setSources([{ object_id: chip.object_id, label: chip.canonical_name || chip.object_id }]);

      const payload: ReasoningTask = {
        task_id: "example_run",
        task_type: "association",
        source_nodes: [chip.object_id],
        parameters: {},
        constraints: {
          max_depth: 2,
          max_paths: 50,
          max_nodes: 200,
          traversal_direction: "forward",
        },
        requested_outputs: ["subgraph", "paths", "evidence_chains", "feature_tables"],
      };
      const res = await executeReasoning(payload);
      setResult(res);
      setActiveTab("visual");
    } catch (err) {
      setExecuteError(formatError(err, "运行示例失败"));
    } finally {
      setRunningExample(false);
    }
  };

  const handleRun = () => {
    if (sources.length === 0) {
      setExecuteError("请至少选择一个起点对象");
      return;
    }
    if (outputs.length === 0) {
      setExecuteError("请至少选择一项输出");
      return;
    }
    setExecuteError(null);

    const parameters: Record<string, unknown> = {};
    if (taskType === "impact_propagation") {
      parameters.propagation_profile = propagationProfile;
    }

    const payload: ReasoningTask = {
      task_id: `rt_${Date.now()}`,
      task_type: taskType,
      source_nodes: sources.map((s) => s.object_id),
      parameters,
      constraints: {
        max_depth: maxDepth,
        max_paths: maxPaths,
        max_nodes: maxNodes,
        traversal_direction: traversalDirection,
      },
      requested_outputs: outputs,
    };

    executeMutation.mutate(payload);
  };

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

  const availableTabs = useMemo(() => {
    const set = new Set<ResultTab>(["overview"]);
    if (!result) return set;
    const payload = result.result_payload;
    if (payload.subgraph || payload.temporary_graph) set.add("visual");
    if (payload.subgraph) set.add("subgraph");
    if (payload.temporary_graph) set.add("temporary_graph");
    if (payload.paths) set.add("paths");
    if (payload.node_scores) set.add("node_scores");
    if (payload.edge_scores) set.add("edge_scores");
    if (payload.evidence_chains) set.add("evidence_chains");
    if (payload.feature_tables) set.add("feature_tables");
    return set;
  }, [result]);

  const tabLabel = (t: ResultTab) => {
    if (t === "overview") return "概览";
    if (t === "visual") return "可视化图";
    return OUTPUT_OPTIONS.find((o) => o.value === t)?.label || t;
  };

  return (
    <div className="flex h-full flex-col overflow-hidden bg-slate-950 text-slate-200">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 bg-slate-900 px-6 py-4">
        <div className="flex items-center gap-3">
          <Brain className="h-5 w-5 text-cyan-400" />
          <div>
            <h1 className="text-lg font-semibold text-slate-100">图推理引擎</h1>
            <p className="text-xs text-slate-500">输入一个产业节点，自动发现它的上下游、影响范围与证据链</p>
          </div>
        </div>
        <button
          onClick={runExample}
          disabled={runningExample}
          className="flex items-center gap-2 rounded bg-cyan-600/20 px-3 py-1.5 text-xs font-medium text-cyan-400 hover:bg-cyan-600/30 disabled:opacity-50"
        >
          {runningExample ? <Loader2 className="h-3 w-3 animate-spin" /> : <Play className="h-3 w-3" />}
          运行示例：芯片
        </button>
        {result && (
          <div className="flex items-center gap-3 text-xs">
            <Badge color={result.status === "success" ? "emerald" : "amber"}>{result.status}</Badge>
            <span className="text-slate-500">reasoning_id:</span>
            <span className="font-mono text-slate-300">{result.reasoning_id}</span>
            <span className="text-slate-500">
              {result.diagnostics.execution_time_ms ?? "—"} ms
            </span>
          </div>
        )}
      </div>

      {/* Main workspace */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left: input */}
        <div className="flex w-[420px] shrink-0 flex-col gap-4 overflow-y-auto border-r border-slate-800 bg-slate-950 p-4">
          {/* Query */}
          <Card title="1. 搜索对象" icon={<Search className="h-4 w-4" />}>
            <div className="space-y-3">
              <p className="text-xs text-slate-500">
                输入名称或别名搜索节点/公司/行业，点击“添加”将其加入推理起点。
              </p>
              <FormField label="查询范围">
                <select
                  value={queryScope}
                  onChange={(e) => setQueryScope(e.target.value as QueryScope)}
                  className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
                >
                  {SCOPE_OPTIONS.map((s) => (
                    <option key={s.value} value={s.value}>
                      {s.label}
                    </option>
                  ))}
                </select>
              </FormField>
              <FormField label="查询文本">
                <div className="flex gap-2">
                  <input
                    value={queryText}
                    onChange={(e) => setQueryText(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleQuery()}
                    placeholder="输入名称/别名/ID 片段，如：芯片"
                    className="flex-1 rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 placeholder:text-slate-600 focus:border-cyan-500 focus:outline-none"
                  />
                  <button
                    onClick={handleQuery}
                    disabled={queryMutation.isPending || !queryText.trim()}
                    className="flex items-center gap-1 rounded bg-cyan-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-cyan-500 disabled:opacity-50"
                  >
                    {queryMutation.isPending ? <Loader2 className="h-3 w-3 animate-spin" /> : <Search className="h-3 w-3" />}
                    查询
                  </button>
                </div>
              </FormField>

              {queryError && (
                <div className="flex items-center gap-2 rounded bg-red-950/30 px-2 py-1.5 text-xs text-red-400">
                  <AlertTriangle className="h-3 w-3" />
                  {queryError}
                </div>
              )}

              <div className="flex items-center justify-between">
                <span className="text-[10px] text-slate-600">没有头绪？</span>
                <button
                  onClick={() => {
                    setQueryText("芯片");
                    setQueryScope("industrial_node");
                  }}
                  className="text-[10px] text-cyan-400 hover:text-cyan-300"
                >
                  填入示例：芯片
                </button>
              </div>

              {candidates.length > 0 && (
                <div className="max-h-56 overflow-y-auto rounded border border-slate-800">
                  {candidates.map((c) => (
                    <div
                      key={c.object_id}
                      className="flex items-center gap-2 border-b border-slate-800 px-2 py-2 last:border-0 hover:bg-slate-800/60"
                    >
                      <div className="min-w-0 flex-1">
                        <div className="flex items-center gap-2">
                          <span className="truncate text-xs font-medium text-slate-200">
                            {c.canonical_name || c.object_id}
                          </span>
                          <Badge color="slate">{c.object_kind}</Badge>
                          {c.entity_type && <Badge color="cyan">{c.entity_type}</Badge>}
                          {c.match_score !== undefined && (
                            <Badge color={c.match_score >= 0.85 ? "emerald" : "amber"}>
                              {(c.match_score * 100).toFixed(0)}%
                            </Badge>
                          )}
                        </div>
                        <div className="truncate text-[10px] text-slate-500">{c.object_id}</div>
                      </div>
                      <button
                        onClick={() => addSource(c)}
                        disabled={sources.some((s) => s.object_id === c.object_id)}
                        className="flex shrink-0 items-center gap-1 rounded bg-slate-800 px-2 py-1 text-[10px] text-slate-300 hover:bg-slate-700 disabled:opacity-40"
                      >
                        {sources.some((s) => s.object_id === c.object_id) ? (
                          <Check className="h-3 w-3" />
                        ) : (
                          <Plus className="h-3 w-3" />
                        )}
                        添加
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </Card>

          {/* Selected sources */}
          <Card title="2. 已选起点" icon={<Layers className="h-4 w-4" />}>
            {sources.length === 0 ? (
              <div className="text-xs text-slate-500">推理需要至少一个起点。请先在上方搜索并添加。</div>
            ) : (
              <div className="flex flex-wrap gap-2">
                {sources.map((s) => (
                  <div
                    key={s.object_id}
                    className="flex items-center gap-1 rounded bg-cyan-900/30 px-2 py-1 text-xs text-cyan-200"
                  >
                    <span className="max-w-[180px] truncate">{s.label}</span>
                    <span className="text-[10px] text-cyan-400/70">{s.object_id}</span>
                    <button
                      onClick={() => removeSource(s.object_id)}
                      className="ml-1 rounded p-0.5 hover:bg-cyan-800/50"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </Card>

          {/* Task config */}
          <Card title="3. 配置推理任务" icon={<Brain className="h-4 w-4" />}>
            <div className="space-y-3">
              <p className="text-xs text-slate-500">
                选择任务类型、遍历约束和希望返回的输出内容，然后运行推理。
              </p>
              <FormField label="任务类型">
                <select
                  value={taskType}
                  onChange={(e) => setTaskType(e.target.value as TaskType)}
                  className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
                >
                  {TASK_OPTIONS.map((t) => (
                    <option key={t.value} value={t.value}>
                      {t.label}
                    </option>
                  ))}
                </select>
              </FormField>

              {taskType === "impact_propagation" && (
                <FormField label="传播策略">
                  <select
                    value={propagationProfile}
                    onChange={(e) => setPropagationProfile(e.target.value)}
                    className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
                  >
                    <option value="supply_forward"> supply_forward（供应前向）</option>
                    <option value="supply_backward">supply_backward（供应后向）</option>
                    <option value="demand_forward">demand_forward（需求前向）</option>
                    <option value="technology_diffusion">technology_diffusion（技术扩散）</option>
                  </select>
                </FormField>
              )}

              <div className="grid grid-cols-2 gap-3">
                <FormField label="最大深度">
                  <input
                    type="number"
                    min={1}
                    max={10}
                    value={maxDepth}
                    onChange={(e) => setMaxDepth(parseInt(e.target.value, 10) || 1)}
                    className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
                  />
                </FormField>
                <FormField label="最大路径数">
                  <input
                    type="number"
                    min={1}
                    value={maxPaths}
                    onChange={(e) => setMaxPaths(parseInt(e.target.value, 10) || 1)}
                    className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
                  />
                </FormField>
                <FormField label="最大节点数">
                  <input
                    type="number"
                    min={1}
                    value={maxNodes}
                    onChange={(e) => setMaxNodes(parseInt(e.target.value, 10) || 1)}
                    className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
                  />
                </FormField>
                <FormField label="遍历方向">
                  <select
                    value={traversalDirection}
                    onChange={(e) => setTraversalDirection(e.target.value as TraversalDirection)}
                    className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
                  >
                    <option value="forward">forward（下游）</option>
                    <option value="backward">backward（上游）</option>
                    <option value="both">both（双向）</option>
                  </select>
                </FormField>
              </div>

              <FormField label="输出内容">
                <div className="grid grid-cols-2 gap-2">
                  {OUTPUT_OPTIONS.map((o) => (
                    <label
                      key={o.value}
                      className={cn(
                        "flex cursor-pointer items-center gap-2 rounded border px-2 py-1.5 text-xs transition-colors",
                        outputs.includes(o.value)
                          ? "border-cyan-700/50 bg-cyan-900/20 text-cyan-200"
                          : "border-slate-800 bg-slate-900 text-slate-400 hover:bg-slate-800"
                      )}
                    >
                      <input
                        type="checkbox"
                        checked={outputs.includes(o.value)}
                        onChange={() => toggleOutput(o.value)}
                        className="h-3 w-3 rounded border-slate-600 bg-slate-800 text-cyan-500 focus:ring-0"
                      />
                      {o.label}
                    </label>
                  ))}
                </div>
              </FormField>

              {executeError && (
                <div className="flex items-center gap-2 rounded bg-red-950/30 px-2 py-1.5 text-xs text-red-400">
                  <AlertTriangle className="h-3 w-3" />
                  {executeError}
                </div>
              )}

              <button
                onClick={handleRun}
                disabled={executeMutation.isPending || sources.length === 0}
                className="flex w-full items-center justify-center gap-2 rounded bg-cyan-600 py-2 text-xs font-medium text-white hover:bg-cyan-500 disabled:opacity-50"
              >
                {executeMutation.isPending ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Play className="h-4 w-4" />
                )}
                运行推理（{sources.length} 个起点）
              </button>
            </div>
          </Card>
        </div>

        {/* Right: results */}
        <div className="flex flex-1 flex-col overflow-hidden bg-slate-950">
          {!result && !executeMutation.isPending && (
            <div className="flex flex-1 flex-col items-center justify-center gap-4 text-slate-500">
              <Brain className="h-12 w-12 opacity-20" />
              <div className="max-w-md space-y-2 text-center text-sm">
                <p>使用流程：</p>
                <ol className="list-inside list-decimal space-y-1 text-xs text-slate-400">
                  <li>在左侧搜索节点/公司/行业</li>
                  <li>点击“添加”将其设为推理起点</li>
                  <li>选择任务类型（关联扩展 / 影响传播）和输出内容</li>
                  <li>点击“运行推理”，在右侧查看结果</li>
                </ol>
              </div>
            </div>
          )}

          {executeMutation.isPending && (
            <div className="flex flex-1 flex-col items-center justify-center gap-3 text-slate-400">
              <Loader2 className="h-8 w-8 animate-spin" />
              <p className="text-sm">推理运行中...</p>
            </div>
          )}

          {result && (
            <>
              {/* Tabs */}
              <div className="flex items-center gap-1 border-b border-slate-800 bg-slate-900/50 px-4 py-2">
                {(["overview", ...Array.from(availableTabs).filter((t) => t !== "overview")] as ResultTab[]).map((t) => (
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
                {activeTab === "overview" && (
                  <div className="space-y-4">
                    <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
                      <h4 className="mb-1 text-sm font-medium text-slate-200">结果说明</h4>
                      <p className="text-xs leading-5 text-slate-400">
                        从起点{" "}
                        <span className="font-medium text-cyan-300">
                          {sources.map((s) => s.label).join("、")}
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
                  <div className="h-[calc(100%-1rem)] rounded-lg border border-slate-800 bg-slate-900/60 p-2">
                    <ResultGraph graph={resultGraph} isTemp={"temp_graph_id" in resultGraph} />
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
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

function SummaryCard({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
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
            type: e.edge_type,
            weight: e.weight,
          },
        }))
      : (graph as ReasoningSubgraph).edges.map((e) => ({
          data: {
            id: e.edge_id,
            source: e.from_node,
            target: e.to_node,
            type: e.edge_type,
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
      ],
      layout: { name: "dagre", rankDir: "TB", padding: 20 } as cytoscape.LayoutOptions,
      minZoom: 0.1,
      maxZoom: 3,
      wheelSensitivity: 0.2,
    });

    // Set node colors after init so we can use our helper
    cy.nodes().forEach((n) => {
      n.data("color", nodeColor(n.data("type")));
    });

    cy.fit(undefined, 24);
    cyRef.current = cy;

    return () => {
      cy.destroy();
      cyRef.current = null;
    };
  }, [elements]);

  return <div ref={containerRef} className="h-full w-full" />;
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
            {p.node_sequence.map((nid, idx) => (
              <span key={idx} className="flex items-center gap-1">
                <span className="rounded bg-slate-800 px-2 py-1 text-slate-200">{nid}</span>
                {idx < p.node_sequence.length - 1 && (
                  <ChevronRight className="h-3 w-3 text-slate-600" />
                )}
              </span>
            ))}
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
            <th className="px-3 py-2">得分</th>
            <th className="px-3 py-2">类型</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800">
          {scores.map((s) => (
            <tr key={s.node_id} className="hover:bg-slate-800/40">
              <td className="px-3 py-2">{s.rank}</td>
              <td className="px-3 py-2 font-mono text-slate-300">{s.node_id}</td>
              <td className="px-3 py-2 font-semibold text-cyan-300">{formatScore(s.score)}</td>
              <td className="px-3 py-2 text-slate-400">{s.score_type}</td>
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
            <th className="px-3 py-2">得分</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800">
          {scores.map((s) => (
            <tr key={s.edge_id} className="hover:bg-slate-800/40">
              <td className="px-3 py-2">{s.rank}</td>
              <td className="px-3 py-2 font-mono text-slate-300">{s.edge_id}</td>
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
