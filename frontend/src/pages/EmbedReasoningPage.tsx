import { useCallback, useEffect, useRef, useState } from "react";
import { useQuery } from "@tanstack/react-query";
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
  getDefaultServerView,
  queryReasoningObjects,
  getPublishedView,
} from "@/services/api";
import { FLOW_OUTPUTS, DEFAULT_OUTPUTS } from "@/components/reasoning/config";
import { cn, Badge } from "@/components/reasoning/ui";
import { ReasoningResultViewer } from "@/components/reasoning/ReasoningResultViewer";
import { GraphCanvas, type GraphCanvasRef } from "@/components/GraphCanvas";
import { ViewToolbar } from "@/components/ViewToolbar";
import { ViewManagerModal } from "@/components/ViewManagerModal";
import { useSavedViews } from "@/hooks/useSavedViews";
import { useAuth } from "@/contexts/AuthContext";
import type { IndustrialViewState, SavedView } from "@/types/view";

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

const EMBED_GRAPH_FILTERS = {
  edgeNamespaces: [],
  edgeTypes: [],
  entityTypes: [],
  status: [],
  confidence: [],
  showIsA: true,
  showPartOf: true,
  showWeakOntology: true,
  showDerivedFrom: true,
};

function companyHighlightNodeIds(result: ReasoningResultEnvelope): string[] {
  const context = result.result_payload.company_context as
    | { categories?: { seed_nodes?: unknown } }
    | undefined;
  const nodes = context?.categories?.seed_nodes;
  return Array.isArray(nodes) ? nodes.filter((node): node is string => typeof node === "string") : [];
}

function EmbeddedCompanyGraph({ nodeIds }: { nodeIds: string[] }) {
  const canvasRef = useRef<GraphCanvasRef>(null);
  const savedViews = useSavedViews();
  const { isReadOnly } = useAuth();
  const [managerOpen, setManagerOpen] = useState(false);
  const [restoredView, setRestoredView] = useState<IndustrialViewState | null>(null);
  const appliedDefault = useRef(false);
  const { data: defaultServerView } = useQuery({
    queryKey: ["server-view-default", "industrial"],
    queryFn: () => getDefaultServerView("industrial"),
    retry: false,
  });

  // The embedded graph is deliberately always the complete industrial graph.
  // A view changes the layout and camera only, so a default configured in the
  // main Arachne workspace can never hide the company context or trim nodes.
  const loadView = useCallback((view: SavedView) => {
    const state = view.industrial;
    if (!state) return;
    setRestoredView({
      ...state,
      camera: { ...state.camera, pan: { ...state.camera.pan } },
      nodePositions: state.nodePositions ? { ...state.nodePositions } : undefined,
    });
  }, []);

  useEffect(() => {
    if (appliedDefault.current || !defaultServerView?.view) return;
    appliedDefault.current = true;
    loadView(defaultServerView.view);
  }, [defaultServerView, loadView]);

  const snapshot = useCallback(
    (name: string): Omit<SavedView, "id" | "base" | "viewVersion" | "created_at" | "updated_at" | "version"> => {
      const camera = canvasRef.current?.getCamera() ?? { pan: { x: 0, y: 0 }, zoom: 1 };
      const positions = canvasRef.current?.getNodePositions() ?? {};
      const containerSize = canvasRef.current?.getContainerSize() ?? undefined;
      return {
        name,
        workspace: "industrial",
        industrial: {
          engine: "legacy",
          selectedFlowIds: [],
          selectedIndustryIds: [],
          selectedCompanyIds: [],
          activeFilters: { ...EMBED_GRAPH_FILTERS },
          expandedProcessParentIds: [],
          camera,
          nodePositions: Object.keys(positions).length > 0 ? positions : undefined,
          containerSize,
        },
      };
    },
    [],
  );

  return (
    <div className="flex h-full min-h-[420px] flex-col gap-2">
      <div className="flex flex-wrap items-center justify-between gap-2 rounded-lg border border-slate-800 bg-slate-900/60 px-3 py-2 text-xs text-slate-400">
        <span>显示 Arachne 首页产业图的全部节点；黄色边框标记该公司的产业暴露节点（{nodeIds.length} 个）。</span>
        <ViewToolbar
          workspace="industrial"
          variant="inline"
          savedViews={savedViews}
          onSave={snapshot}
          onLoad={loadView}
          onManage={() => setManagerOpen(true)}
          showUndo={false}
        />
      </div>
      <div className="min-h-0 flex-1 overflow-hidden rounded-lg border border-slate-800 bg-slate-900/60 p-2">
        <GraphCanvas
          ref={canvasRef}
          engine="legacy"
          filters={EMBED_GRAPH_FILTERS}
          highlightNodeIds={nodeIds}
          preserveContextOnHighlight
          restoredPositions={restoredView?.nodePositions}
          restoredCamera={restoredView?.camera}
          onNodeClick={() => undefined}
          onEdgeClick={() => undefined}
        />
      </div>
      {managerOpen && (
        <ViewManagerModal
          workspace="industrial"
          savedViews={savedViews}
          onLoad={(view) => {
            loadView(view);
            setManagerOpen(false);
          }}
          canManageServerViews={!isReadOnly}
          onClose={() => setManagerOpen(false)}
        />
      )}
    </div>
  );
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
  const highlightNodeIds = result ? companyHighlightNodeIds(result) : [];
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
            fullGraph={
              isFlowEngine && config?.taskType === "cross_graph_context"
                ? <EmbeddedCompanyGraph nodeIds={highlightNodeIds} />
                : undefined
            }
            preferFullGraph={isFlowEngine && config?.taskType === "cross_graph_context"}
          />
        )}
      </div>
    </div>
  );
}
