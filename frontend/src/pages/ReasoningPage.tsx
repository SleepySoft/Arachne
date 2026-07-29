import { useEffect, useState } from "react";
import { useMutation } from "@tanstack/react-query";
import {
  AlertTriangle,
  Brain,
  Check,
  Layers,
  Loader2,
  Play,
  Plus,
  Search,
  X,
} from "lucide-react";
import {
  ObjectCandidate,
  ObjectQueryRequest,
  OutputType,
  ReasoningResultEnvelope,
  ReasoningTask,
  QueryScope,
  TaskType,
  TraversalDirection,
} from "@/types";
import { queryReasoningObjects, executeReasoning } from "@/services/api";
import { OUTPUT_OPTIONS, FLOW_OUTPUTS, DEFAULT_OUTPUTS } from "@/components/reasoning/config";
import { cn, FormField, Card, Badge } from "@/components/reasoning/ui";
import { ReasoningResultViewer } from "@/components/reasoning/ReasoningResultViewer";

// 起点范围由任务决定（见 seedSpec），不再需要手工选择范围；scopeHint 仍用于输入框占位/示例。

function scopeHint(scope: QueryScope): {
  label: string;
  placeholder: string;
  example: string;
} {
  switch (scope) {
    case "industrial_node":
      return {
        label: "节点名称",
        placeholder: "输入节点名称/别名/ID 片段，如：芯片",
        example: "芯片",
      };
    case "factual_node":
      return {
        label: "事实节点",
        placeholder: "输入人员姓名或公司名/股票代码，如：张三、比亚迪",
        example: "张三 / 比亚迪",
      };
    case "company":
      return {
        label: "公司名称",
        placeholder: "输入公司名/别名/股票代码，如：比亚迪",
        example: "比亚迪",
      };
    case "industry":
      return {
        label: "行业名称",
        placeholder: "输入行业名/别名，如：半导体",
        example: "半导体",
      };
    default:
      return {
        label: "查询文本",
        placeholder: "输入名称/别名/ID 片段",
        example: "芯片",
      };
  }
}

const TASK_OPTIONS: { value: TaskType; label: string }[] = [
  { value: "association", label: "关联扩展" },
  { value: "impact_propagation", label: "影响传播" },
  { value: "bottleneck_detection", label: "瓶颈检测" },
  { value: "substitution_search", label: "替代搜索" },
  { value: "candidate_discovery", label: "候选发现" },
  { value: "cross_graph_context", label: "跨图上下文" },
];

const ENGINE_OPTIONS: { value: string; label: string }[] = [
  { value: "arachne_flow", label: "流程图（arachne-flow）" },
  { value: "legacy", label: "产业图（legacy）" },
];

/** arachne_flow 引擎支持的任务类型。 */
const FLOW_TASK_OPTIONS: { value: TaskType; label: string }[] = [
  { value: "association", label: "关联扩展" },
  { value: "cross_graph_context", label: "公司产业上下文" },
];

/** 各任务的一句话说明（选择任务时展示，让用户知道该输什么、能得到什么）。 */
const TASK_DESC: Record<string, string> = {
  association: "从产业节点出发，沿物料转化链展开上下游，适合回答“它从哪来、到哪去”。",
  impact_propagation: "量化上游扰动（断供/涨价）沿供应链向下游传递的强度。",
  bottleneck_detection: "找出被多条路径共享、替代来源少的关键节点（卡脖子环节）。",
  substitution_search: "基于物料谱系与结构相似性，为节点寻找可替代对象。",
  candidate_discovery: "识别图中可能缺失的工艺节点或关系。",
  cross_graph_context: "把产业节点关联到公司、行业和关键人员。",
};

const FLOW_TASK_DESC: Record<string, string> = {
  association:
    "从产业节点出发：展开主线（物料转化链）与支线（同工艺关联），讲述产品的制造故事。起点：产业节点。",
  cross_graph_context:
    "从公司出发：解析公司暴露的产业节点，展开它在产业链中的位置，并找出同业、上游、下游与相关公司。起点：公司。",
};

/** 任务 -> 起点类型。页面为任务优先设计：先选任务，起点搜索范围随之固定。 */
function seedSpec(taskType: TaskType, isFlowEngine: boolean): {
  label: string;
  scope: QueryScope;
  factualType: "" | "person" | "company";
} {
  if (isFlowEngine && taskType === "cross_graph_context") {
    return { label: "公司（事实节点）", scope: "factual_node", factualType: "company" };
  }
  return { label: "产业节点", scope: "industrial_node", factualType: "" };
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
  const [factualNodeType, setFactualNodeType] = useState<"" | "person" | "company">("");
  const [candidates, setCandidates] = useState<ObjectCandidate[]>([]);
  const [suggestions, setSuggestions] = useState<ObjectCandidate[]>([]);
  const [queryError, setQueryError] = useState<string | null>(null);

  const queryMutation = useMutation({
    mutationFn: (payload: ObjectQueryRequest) => queryReasoningObjects(payload),
    onSuccess: (data) => {
      setQueryError(null);
      setCandidates(data.candidates);
      setSuggestions(data.suggestions ?? []);
    },
    onError: (err) => setQueryError(formatError(err, "对象查询失败")),
  });

  const handleQuery = () => {
    if (!queryText.trim()) return;
    setQueryError(null);
    const filters: Record<string, unknown> = {};
    if (queryScope === "factual_node" && factualNodeType) {
      filters.object_type = factualNodeType;
    }
    queryMutation.mutate({
      query_id: `rq_${Date.now()}`,
      query_text: queryText.trim(),
      query_scope: queryScope,
      filters,
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
  const [engine, setEngine] = useState<string>("arachne_flow");
  const isFlowEngine = engine === "arachne_flow";
  const [taskType, setTaskType] = useState<TaskType>("association");
  const [maxDepth, setMaxDepth] = useState(2);
  const [maxPaths, setMaxPaths] = useState(50);
  const [maxNodes, setMaxNodes] = useState(200);
  const [traversalDirection, setTraversalDirection] = useState<TraversalDirection>("forward");
  const [propagationProfile, setPropagationProfile] = useState("supply_forward");
  const [includeCompanyExposures, setIncludeCompanyExposures] = useState(false);
  const [maxCompanyExposures, setMaxCompanyExposures] = useState(20);
  const [expandOntology, setExpandOntology] = useState(false);
  const [outputs, setOutputs] = useState<OutputType[]>(DEFAULT_OUTPUTS);

  useEffect(() => {
    // arachne_flow 引擎仅支持部分任务类型，切换引擎时回落到受支持的任务
    if (isFlowEngine && !FLOW_TASK_OPTIONS.some((t) => t.value === taskType)) {
      setTaskType("association");
    }
  }, [isFlowEngine, taskType]);

  useEffect(() => {
    // flow 引擎有独立的广度收敛（单资源 ACTION 上限），节点预算可以给得更紧
    setMaxNodes(isFlowEngine ? 120 : 200);
  }, [isFlowEngine]);

  useEffect(() => {
    // 任务决定起点类型：选公司产业上下文则搜索公司，其余搜索产业节点
    const spec = seedSpec(taskType, isFlowEngine);
    setQueryScope(spec.scope);
    setFactualNodeType(spec.factualType);
  }, [taskType, isFlowEngine]);

  useEffect(() => {
    // Suggest sensible defaults per task type
    if (taskType === "association") {
      setOutputs(
        isFlowEngine
          ? [...FLOW_OUTPUTS]
          : ["subgraph", "paths", "evidence_chains", "feature_tables"]
      );
    } else if (taskType === "impact_propagation") {
      setOutputs([
        "temporary_graph",
        "paths",
        "node_scores",
        "edge_scores",
        "evidence_chains",
        "feature_tables",
      ]);
    } else if (taskType === "bottleneck_detection") {
      setOutputs(["temporary_graph", "node_scores", "candidate_nodes", "paths"]);
    } else if (taskType === "substitution_search") {
      setOutputs(["candidate_nodes", "temporary_graph", "paths"]);
    } else if (taskType === "candidate_discovery") {
      setOutputs(["candidate_nodes", "candidate_edges", "feature_tables"]);
    } else if (taskType === "cross_graph_context") {
      setOutputs(["temporary_graph", "paths"]);
    }
  }, [taskType, isFlowEngine]);

  const toggleOutput = (o: OutputType) => {
    setOutputs((prev) => (prev.includes(o) ? prev.filter((x) => x !== o) : [...prev, o]));
  };

  // ----- Execution -----
  const [result, setResult] = useState<ReasoningResultEnvelope | null>(null);
  const [executeError, setExecuteError] = useState<string | null>(null);

  const executeMutation = useMutation({
    mutationFn: (payload: ReasoningTask) => executeReasoning(payload),
    onSuccess: (data) => {
      setExecuteError(null);
      setResult(data);
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

      const exampleOutputs: OutputType[] = isFlowEngine
        ? ["temporary_graph", "paths"]
        : ["subgraph", "paths", "evidence_chains", "feature_tables"];
      setOutputs(exampleOutputs);
      const payload: ReasoningTask = {
        task_id: "example_run",
        task_type: "association",
        source_nodes: [chip.object_id],
        parameters: {
          include_company_exposures: includeCompanyExposures,
          max_company_exposures: maxCompanyExposures,
        },
        constraints: {
          max_depth: 2,
          max_paths: 50,
          max_nodes: 200,
          traversal_direction: "forward",
        },
        requested_outputs: exampleOutputs,
        engine,
      };
      const res = await executeReasoning(payload);
      setResult(res);
    } catch (err) {
      setExecuteError(formatError(err, "运行示例失败"));
    } finally {
      setRunningExample(false);
    }
  };

  const buildPayload = (sourceIds: string[]): ReasoningTask => {
    const parameters: Record<string, unknown> = {};
    if (taskType === "impact_propagation") {
      parameters.propagation_profile = propagationProfile;
    }

    if (includeCompanyExposures) {
      parameters.include_company_exposures = true;
      parameters.max_company_exposures = maxCompanyExposures;
    }
    if (expandOntology) {
      parameters.expand_ontology = true;
    }

    return {
      task_id: `rt_${Date.now()}`,
      task_type: taskType,
      source_nodes: sourceIds,
      parameters,
      constraints: {
        max_depth: maxDepth,
        max_paths: maxPaths,
        max_nodes: maxNodes,
        traversal_direction: traversalDirection,
      },
      requested_outputs: outputs,
      engine,
    };
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
    executeMutation.mutate(buildPayload(sources.map((s) => s.object_id)));
  };

  /** 以某个结果节点为新起点直接深入推理（“讲故事”的下一步操作）。 */
  const deepDive = (nodeId: string, label: string) => {
    setSources([{ object_id: nodeId, label }]);
    setQueryText(label);
    setExecuteError(null);
    executeMutation.mutate(buildPayload([nodeId]));
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
          {/* Step 1: 选择任务（任务优先：先定任务，起点类型随之确定） */}
          <Card title="1. 选择任务" icon={<Brain className="h-4 w-4" />}>
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <FormField label="推理引擎">
                  <select
                    value={engine}
                    onChange={(e) => setEngine(e.target.value)}
                    className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
                  >
                    {ENGINE_OPTIONS.map((opt) => (
                      <option key={opt.value} value={opt.value}>
                        {opt.label}
                      </option>
                    ))}
                  </select>
                </FormField>
                <FormField label="任务类型">
                  <select
                    value={taskType}
                    onChange={(e) => setTaskType(e.target.value as TaskType)}
                    className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
                  >
                    {(isFlowEngine ? FLOW_TASK_OPTIONS : TASK_OPTIONS).map((t) => (
                      <option key={t.value} value={t.value}>
                        {t.label}
                      </option>
                    ))}
                  </select>
                </FormField>
              </div>
              <p className="rounded bg-slate-900 px-2 py-1.5 text-xs leading-5 text-slate-400">
                {(isFlowEngine ? FLOW_TASK_DESC : TASK_DESC)[taskType] ?? ""}
              </p>
            </div>
          </Card>

          {/* Step 2: 添加起点 */}
          <Card title="2. 添加起点" icon={<Search className="h-4 w-4" />}>
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-xs">
                <span className="text-slate-500">起点类型</span>
                <Badge color="cyan">{seedSpec(taskType, isFlowEngine).label}</Badge>
              </div>
              <FormField label={scopeHint(queryScope).label}>
                <div className="flex gap-2">
                  <input
                    value={queryText}
                    onChange={(e) => setQueryText(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleQuery()}
                    placeholder={scopeHint(queryScope).placeholder}
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
                    setQueryText(scopeHint(queryScope).example);
                  }}
                  className="text-[10px] text-cyan-400 hover:text-cyan-300"
                >
                  填入示例：{scopeHint(queryScope).example}
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

              {candidates.length === 0 && suggestions.length === 0 && !queryMutation.isPending && (
                <p className="text-[10px] text-slate-600">
                  输入名称并查询后，此处会列出匹配与相似的节点。
                </p>
              )}

              {suggestions.length > 0 && (
                <div>
                  <div className="mb-1 text-[10px] font-semibold uppercase tracking-wider text-slate-500">
                    相似建议（可添加为起点）
                  </div>
                  <div className="max-h-56 overflow-y-auto rounded border border-slate-800/60">
                    {suggestions.map((c) => (
                      <div
                        key={c.object_id}
                        className="flex items-center gap-2 border-b border-slate-800/60 px-2 py-1.5 last:border-0 hover:bg-slate-800/40"
                      >
                        <div className="min-w-0 flex-1">
                          <div className="flex items-center gap-2">
                            <span className="truncate text-xs text-slate-300">
                              {c.canonical_name || c.object_id}
                            </span>
                            {c.entity_type && <Badge color="slate">{c.entity_type}</Badge>}
                            {c.match_score !== undefined && (
                              <Badge color="amber">{(c.match_score * 100).toFixed(0)}%</Badge>
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
                </div>
              )}
            </div>
          </Card>

          {/* Selected sources */}
          <Card title="3. 已选起点" icon={<Layers className="h-4 w-4" />}>
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
          <Card title="4. 参数与输出" icon={<Brain className="h-4 w-4" />}>
            <div className="space-y-3">
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

              {!isFlowEngine && (
                <FormField label="拓扑扩展">
                  <label
                    className={cn(
                      "flex cursor-pointer items-center gap-2 rounded border px-2 py-1.5 text-xs transition-colors",
                      expandOntology
                        ? "border-cyan-700/50 bg-cyan-900/20 text-cyan-200"
                        : "border-slate-800 bg-slate-900 text-slate-400 hover:bg-slate-800"
                    )}
                  >
                    <input
                      type="checkbox"
                      checked={expandOntology}
                      onChange={() => setExpandOntology((v) => !v)}
                      className="h-3 w-3 rounded border-slate-600 bg-slate-800 text-cyan-500 focus:ring-0"
                    />
                    通过本体关系扩展起点（is_a / part_of）
                  </label>
                </FormField>
              )}

              <FormField label="输出内容">
                <div className="grid grid-cols-2 gap-2">
                  {(isFlowEngine
                    ? OUTPUT_OPTIONS.filter((o) => FLOW_OUTPUTS.includes(o.value))
                    : OUTPUT_OPTIONS
                  ).map((o) => (
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
                {isFlowEngine && (
                  <p className="mt-1 text-[10px] text-slate-500">
                    流程图引擎输出：临时推理图 / 路径 / 节点得分（主线-支线结构）
                  </p>
                )}
              </FormField>

              <FormField label="公司暴露">
                <div className="space-y-2">
                  <label
                    className={cn(
                      "flex cursor-pointer items-center gap-2 rounded border px-2 py-1.5 text-xs transition-colors",
                      includeCompanyExposures
                        ? "border-cyan-700/50 bg-cyan-900/20 text-cyan-200"
                        : "border-slate-800 bg-slate-900 text-slate-400 hover:bg-slate-800"
                    )}
                  >
                    <input
                      type="checkbox"
                      checked={includeCompanyExposures}
                      onChange={() => setIncludeCompanyExposures((v) => !v)}
                      className="h-3 w-3 rounded border-slate-600 bg-slate-800 text-cyan-500 focus:ring-0"
                    />
                    返回关联公司暴露（独立数据区，不混入节点）
                  </label>
                  {includeCompanyExposures && (
                    <div className="flex items-center gap-2 text-xs text-slate-400">
                      <span>最多返回</span>
                      <input
                        type="number"
                        min={1}
                        max={200}
                        value={maxCompanyExposures}
                        onChange={(e) => setMaxCompanyExposures(parseInt(e.target.value, 10) || 20)}
                        className="w-16 rounded border border-slate-700 bg-slate-800 px-2 py-1 text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
                      />
                      <span>条暴露记录</span>
                    </div>
                  )}
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
                title={sources.length === 0 ? "请先在上方搜索并添加至少一个起点" : undefined}
                className="flex w-full items-center justify-center gap-2 rounded bg-cyan-600 py-2 text-xs font-medium text-white hover:bg-cyan-500 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {executeMutation.isPending ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Play className="h-4 w-4" />
                )}
                运行推理（{sources.length} 个起点）
              </button>
              {sources.length === 0 && (
                <p className="text-center text-[10px] text-slate-600">
                  按钮不可用：还没有起点。请在“1. 搜索对象”中查询并点击“添加”。
                </p>
              )}
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
                  <li>选择任务（引擎 + 类型），按提示搜索并添加起点</li>
                  <li>调整遍历约束与输出内容，点击“运行推理”</li>
                  <li>在「解读」标签页阅读结果故事，或点“以此为起点深入”继续探索</li>
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
            <ReasoningResultViewer
              result={result}
              isFlowEngine={isFlowEngine}
              seedLabels={sources.map((s) => s.label)}
              onDeepDive={deepDive}
              onRunWithEngine={(eng) => {
                setEngine(eng);
                setExecuteError(null);
                executeMutation.mutate({
                  ...buildPayload(sources.map((s) => s.object_id)),
                  engine: eng,
                });
              }}
            />
          )}
        </div>
      </div>
    </div>
  );
}
