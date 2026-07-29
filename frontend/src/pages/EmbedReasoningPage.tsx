import { useCallback, useEffect, useState } from "react";
import { AlertTriangle, Loader2, RefreshCw } from "lucide-react";
import {
  OutputType,
  QueryScope,
  ReasoningResultEnvelope,
  ReasoningTask,
  TaskType,
  TraversalDirection,
} from "@/types";
import {
  executeReasoning,
  queryReasoningObjects,
  getPublishedView,
} from "@/services/api";
import { FLOW_OUTPUTS, DEFAULT_OUTPUTS } from "@/components/reasoning/config";
import { cn, Badge } from "@/components/reasoning/ui";
import { ReasoningResultViewer } from "@/components/reasoning/ReasoningResultViewer";

interface SeedItem {
  object_id: string;
  label: string;
}

interface EmbedConfig {
  seeds: string[];
  resolve: boolean;
  scope: QueryScope;
  taskType: TaskType;
  engine: string;
  maxDepth: number;
  maxNodes: number;
  maxPaths: number;
  direction: TraversalDirection;
  outputs: OutputType[];
  includeCompanyExposures: boolean;
  maxCompanyExposures: number;
  title: string | null;
}

function deriveScope(taskType: TaskType, engine: string): QueryScope {
  if (engine === "arachne_flow" && taskType === "cross_graph_context")
    return "factual_node";
  return "industrial_node";
}

function parseParams(p: URLSearchParams): EmbedConfig | null {
  const seed = p.get("seed");
  if (!seed) return null;
  const engine = p.get("engine") || "arachne_flow";
  const taskType = (p.get("task_type") || "association") as TaskType;
  const isFlow = engine === "arachne_flow";
  return {
    seeds: seed.split(",").map((s) => s.trim()).filter(Boolean),
    resolve: p.get("resolve") === "1",
    scope: (p.get("scope") as QueryScope) || deriveScope(taskType, engine),
    taskType,
    engine,
    maxDepth: parseInt(p.get("max_depth") || "2", 10),
    maxNodes: parseInt(p.get("max_nodes") || (isFlow ? "120" : "200"), 10),
    maxPaths: parseInt(p.get("max_paths") || "50", 10),
    direction: (p.get("direction") || "forward") as TraversalDirection,
    outputs: p.get("outputs")
      ? (p.get("outputs")!.split(",") as OutputType[])
      : isFlow
        ? FLOW_OUTPUTS
        : DEFAULT_OUTPUTS,
    includeCompanyExposures: p.get("company_exposures") !== "0",
    maxCompanyExposures: parseInt(p.get("max_companies") || "30", 10),
    title: p.get("title"),
  };
}

function toSearchParams(obj: Record<string, unknown>): URLSearchParams {
  const sp = new URLSearchParams();
  for (const [k, v] of Object.entries(obj)) {
    if (v != null) sp.set(k, String(v));
  }
  return sp;
}

export function EmbedReasoningPage() {
  const [config, setConfig] = useState<EmbedConfig | null>(null);
  const [result, setResult] = useState<ReasoningResultEnvelope | null>(null);
  const [seeds, setSeeds] = useState<SeedItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const runReasoning = useCallback(async (cfg: EmbedConfig) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      let seedItems: SeedItem[];
      if (cfg.resolve) {
        const resolved: SeedItem[] = [];
        for (const s of cfg.seeds) {
          const qr = await queryReasoningObjects({
            query_id: `embed_${s}`,
            query_text: s,
            query_scope: cfg.scope,
            limit: 1,
          });
          const c = qr.candidates[0];
          if (!c) throw new Error(`无法解析起点: ${s}`);
          resolved.push({
            object_id: c.object_id,
            label: c.canonical_name || c.object_id,
          });
        }
        seedItems = resolved;
      } else {
        seedItems = cfg.seeds.map((s) => ({ object_id: s, label: s }));
      }
      setSeeds(seedItems);

      const task: ReasoningTask = {
        task_id: `embed_${Date.now()}`,
        task_type: cfg.taskType,
        source_nodes: seedItems.map((s) => s.object_id),
        parameters: {
          include_company_exposures: cfg.includeCompanyExposures,
          max_company_exposures: cfg.maxCompanyExposures,
        },
        constraints: {
          max_depth: cfg.maxDepth,
          max_paths: cfg.maxPaths,
          max_nodes: cfg.maxNodes,
          traversal_direction: cfg.direction,
        },
        requested_outputs: cfg.outputs,
        engine: cfg.engine,
      };
      const res = await executeReasoning(task);
      setResult(res);
    } catch (e: unknown) {
      const err = e as { response?: { data?: { detail?: string } }; message?: string };
      setError(err?.response?.data?.detail || err?.message || "推理执行失败");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const viewId = urlParams.get("view");
    const refresh = urlParams.get("refresh") === "1";

    if (viewId) {
      getPublishedView(viewId)
        .then((v) => {
          const merged = v.params && typeof v.params === "object"
            ? toSearchParams(v.params as Record<string, unknown>)
            : new URLSearchParams();
          for (const [k, val] of urlParams.entries()) merged.set(k, val);
          const cfg = parseParams(merged);
          if (!cfg) {
            setError("视图配置无效：缺少 seed 参数");
            setLoading(false);
            return;
          }
          setConfig(cfg);
          setSeeds(cfg.seeds.map((s) => ({ object_id: s, label: s })));
          if (v.result_snapshot && !refresh) {
            setResult(v.result_snapshot as unknown as ReasoningResultEnvelope);
            setLoading(false);
          } else {
            runReasoning(cfg);
          }
        })
        .catch((e: unknown) => {
          const err = e as { response?: { data?: { detail?: string } }; message?: string };
          setError(err?.response?.data?.detail || err?.message || "加载发布视图失败");
          setLoading(false);
        });
    } else {
      const cfg = parseParams(urlParams);
      if (cfg) {
        setConfig(cfg);
        runReasoning(cfg);
      } else {
        setError("缺少必要参数：seed（起点节点 ID 或名称）");
        setLoading(false);
      }
    }
  }, [runReasoning]);

  const handleDeepDive = useCallback(
    (nodeId: string, label: string) => {
      if (!config) return;
      const newCfg: EmbedConfig = {
        ...config,
        seeds: [nodeId],
        resolve: false,
        title: label,
      };
      setConfig(newCfg);
      runReasoning(newCfg);
    },
    [config, runReasoning],
  );

  const handleRunWithEngine = useCallback(
    (eng: string) => {
      if (!config) return;
      const newCfg: EmbedConfig = { ...config, engine: eng };
      setConfig(newCfg);
      runReasoning(newCfg);
    },
    [config, runReasoning],
  );

  const isFlowEngine = config?.engine === "arachne_flow";
  const title =
    config?.title ||
    (seeds.length > 0 ? seeds.map((s) => s.label).join("、") : "Arachne 推理");

  return (
    <div className="flex h-screen flex-col bg-slate-950 text-slate-200">
      <header className="flex items-center gap-2 border-b border-slate-800 bg-slate-900/80 px-4 py-2">
        <h1 className="truncate text-sm font-medium text-slate-200">{title}</h1>
        {config && (
          <>
            <Badge color="cyan">{isFlowEngine ? "流程图" : "产业图"}</Badge>
            <Badge color="slate">{config.taskType}</Badge>
          </>
        )}
        <button
          onClick={() => config && runReasoning(config)}
          disabled={loading}
          className={cn(
            "ml-auto flex items-center gap-1 rounded px-2 py-1 text-xs text-slate-400 transition hover:bg-slate-800 hover:text-slate-200",
            loading && "opacity-50",
          )}
        >
          <RefreshCw className={cn("h-3.5 w-3.5", loading && "animate-spin")} />
          刷新
        </button>
      </header>

      <div className="relative flex-1 overflow-hidden">
        {loading && (
          <div className="flex h-full flex-col items-center justify-center gap-3 text-slate-400">
            <Loader2 className="h-8 w-8 animate-spin" />
            <p className="text-sm">推理运行中...</p>
          </div>
        )}

        {!loading && error && (
          <div className="flex h-full flex-col items-center justify-center gap-3 px-8 text-center">
            <AlertTriangle className="h-8 w-8 text-amber-400" />
            <p className="text-sm text-amber-300">{error}</p>
          </div>
        )}

        {!loading && !error && result && (
          <ReasoningResultViewer
            result={result}
            isFlowEngine={!!isFlowEngine}
            seedLabels={seeds.map((s) => s.label)}
            onDeepDive={handleDeepDive}
            onRunWithEngine={handleRunWithEngine}
          />
        )}
      </div>
    </div>
  );
}
