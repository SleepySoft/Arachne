import { useEffect, useMemo, useRef, useState } from "react";
import { AlertTriangle, Loader2, RefreshCw } from "lucide-react";
import { GraphCanvas, type GraphCanvasRef } from "@/components/GraphCanvas";
import {
  getCompany,
  getCompanySubgraph,
  getNeighbors,
  listCompanyExposures,
} from "@/services/api";
import type {
  Company,
  CompanyNodeExposure,
  GraphEdge,
  IndustrialNode,
} from "@/types";

const MAX_CONTEXT_NODES = 80;
const MAX_CONTEXT_PER_EXPOSURE = 12;

const EMBED_FILTERS = {
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

interface ExposureGraph {
  company: Company;
  exposures: CompanyNodeExposure[];
  nodes: IndustrialNode[];
  edges: GraphEdge[];
  contextNodeCount: number;
}

const ACTIVITY_LABELS: Record<string, string> = {
  rnd: "研发",
  design: "设计",
  manufacture: "制造",
  produce: "生产",
  integrate: "集成",
  operate: "运营",
  provide_service: "服务",
  procure: "采购",
  use: "使用",
  unknown: "参与",
};

function fullWorkspaceUrl(companyId: string): string {
  const url = new URL("./", window.location.href);
  url.searchParams.set("view", "industrial_graph");
  url.searchParams.set("company", companyId);
  return url.toString();
}

async function loadExposureGraph(companyId: string): Promise<ExposureGraph> {
  const [company, exposurePage, companyGraph] = await Promise.all([
    getCompany(companyId),
    listCompanyExposures(companyId, 1, 1000),
    getCompanySubgraph(companyId),
  ]);
  const exposures = exposurePage.items;
  const exposureIds = new Set(exposures.map((item) => item.node_id));
  const nodeMap = new Map(companyGraph.nodes.map((node) => [node.node_id, node]));
  // The compact embed is about the company's position in the value chain.
  // Ontology edges can turn exposed systems into collapsed compound parents,
  // which hides the very nodes this view needs to foreground.
  const edgeMap = new Map<string, GraphEdge>(
    companyGraph.edges
      .filter((edge) => edge.edge_namespace === "industrial_flow")
      .map((edge) => [edge.edge_id, edge]),
  );

  const neighborResults = await Promise.allSettled(
    Array.from(exposureIds).map((nodeId) => getNeighbors(nodeId)),
  );
  let contextNodeCount = 0;
  const candidateEdges: GraphEdge[] = [];

  neighborResults.forEach((result) => {
    if (result.status !== "fulfilled") return;
    let addedForExposure = 0;
    result.value.nodes.forEach((node) => {
      if (nodeMap.has(node.node_id)) return;
      if (
        !exposureIds.has(node.node_id) &&
        (contextNodeCount >= MAX_CONTEXT_NODES ||
          addedForExposure >= MAX_CONTEXT_PER_EXPOSURE)
      ) {
        return;
      }
      nodeMap.set(node.node_id, node);
      if (!exposureIds.has(node.node_id)) {
        contextNodeCount += 1;
        addedForExposure += 1;
      }
    });
    candidateEdges.push(
      ...result.value.edges.filter((edge) => edge.edge_namespace === "industrial_flow"),
    );
  });

  candidateEdges.forEach((edge) => {
    if (nodeMap.has(edge.from_node) && nodeMap.has(edge.to_node)) {
      edgeMap.set(edge.edge_id, edge);
    }
  });

  return {
    company,
    exposures,
    nodes: Array.from(nodeMap.values()),
    edges: Array.from(edgeMap.values()),
    contextNodeCount,
  };
}

export function EmbedCompanyExposurePage({ companyId }: { companyId: string }) {
  const canvasRef = useRef<GraphCanvasRef>(null);
  const [data, setData] = useState<ExposureGraph | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    loadExposureGraph(companyId)
      .then((result) => {
        if (!cancelled) setData(result);
      })
      .catch((reason: unknown) => {
        if (cancelled) return;
        const err = reason as { response?: { data?: { detail?: string } }; message?: string };
        setError(err.response?.data?.detail || err.message || "公司产业暴露加载失败");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [companyId, reloadKey]);

  const exposureIds = useMemo(
    () => data?.exposures.map((item) => item.node_id) ?? [],
    [data],
  );
  const nodeNames = useMemo(
    () => new Map(data?.nodes.map((node) => [node.node_id, node.canonical_name_zh || node.canonical_name_en || node.node_id])),
    [data],
  );

  useEffect(() => {
    if (!data || exposureIds.length === 0) return;
    const timer = window.setTimeout(() => {
      const canvas = canvasRef.current;
      if (!canvas) return;
      const positions: Record<string, { x: number; y: number }> = {};
      const exposureSet = new Set(exposureIds);
      const exposedNodes = data.nodes.filter((node) => exposureSet.has(node.node_id));
      const contextNodes = data.nodes.filter((node) => !exposureSet.has(node.node_id));
      const exposureColumns = Math.min(5, Math.max(1, exposedNodes.length));
      exposedNodes.forEach((node, index) => {
        positions[node.node_id] = {
          x: (index % exposureColumns) * 180,
          y: Math.floor(index / exposureColumns) * 150,
        };
      });
      const exposureRows = Math.ceil(exposedNodes.length / exposureColumns);
      const contextColumns = Math.min(6, Math.max(1, contextNodes.length));
      contextNodes.forEach((node, index) => {
        positions[node.node_id] = {
          x: (index % contextColumns) * 150,
          y: exposureRows * 150 + 100 + Math.floor(index / contextColumns) * 130,
        };
      });
      canvas.setNodePositions(positions);
      canvas.fitToView(48);
    }, 450);
    return () => window.clearTimeout(timer);
  }, [data, exposureIds]);

  if (loading) {
    return (
      <div className="flex h-screen flex-col items-center justify-center gap-3 bg-slate-950 text-slate-400">
        <Loader2 className="h-8 w-8 animate-spin" />
        <span className="text-sm">加载公司产业暴露…</span>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex h-screen flex-col items-center justify-center gap-3 bg-slate-950 px-8 text-center">
        <AlertTriangle className="h-8 w-8 text-amber-400" />
        <p className="text-sm text-amber-300">{error || "公司产业暴露不存在"}</p>
        <button
          className="rounded bg-slate-800 px-3 py-1.5 text-xs text-slate-200 hover:bg-slate-700"
          onClick={() => setReloadKey((key) => key + 1)}
        >
          重试
        </button>
      </div>
    );
  }

  return (
    <main className="flex h-screen min-h-[420px] flex-col overflow-hidden bg-slate-950 text-slate-200">
      <header className="flex min-h-12 items-center gap-3 border-b border-slate-800 bg-slate-900/90 px-3 py-2">
        <div className="min-w-0">
          <h1 className="truncate text-sm font-semibold">{data.company.name_zh || data.company.name_en}</h1>
          <p className="truncate text-[11px] text-slate-400">
            {data.exposures.length} 个产业暴露 · {data.contextNodeCount} 个一跳上下游实体
          </p>
        </div>
        <div className="ml-auto flex shrink-0 items-center gap-1">
          <button
            className="rounded p-1.5 text-slate-400 hover:bg-slate-800 hover:text-slate-200"
            title="刷新"
            onClick={() => setReloadKey((key) => key + 1)}
          >
            <RefreshCw className="h-3.5 w-3.5" />
          </button>
          <a
            className="rounded px-2 py-1 text-xs text-sky-400 hover:bg-slate-800"
            href={fullWorkspaceUrl(companyId)}
            target="_blank"
            rel="noopener noreferrer"
          >
            打开完整图谱 ↗
          </a>
        </div>
      </header>

      {data.exposures.length === 0 ? (
        <div className="flex flex-1 items-center justify-center px-8 text-center text-sm text-slate-400">
          该公司已收录，但尚未登记产业暴露。
        </div>
      ) : (
        <>
          <section className="min-h-0 flex-1">
            <GraphCanvas
              ref={canvasRef}
              key={reloadKey}
              engine="legacy"
              filters={EMBED_FILTERS}
              sourceData={{ nodes: data.nodes, edges: data.edges }}
              highlightNodeIds={exposureIds}
              focusState={{
                active: true,
                seedNodeIds: exposureIds,
                visibleNodeIds: data.nodes.map((node) => node.node_id),
                history: [],
              }}
              onNodeClick={() => undefined}
              onEdgeClick={() => undefined}
            />
          </section>
          <footer className="flex shrink-0 gap-2 overflow-x-auto border-t border-slate-800 bg-slate-900/90 px-3 py-2">
            {data.exposures.map((exposure) => (
              <div
                key={exposure.exposure_id}
                className="flex shrink-0 items-center gap-1.5 rounded-full border border-amber-500/40 bg-amber-950/30 px-2.5 py-1 text-[11px]"
                title={exposure.role || exposure.node_id}
              >
                <span className="font-medium text-amber-200">
                  {nodeNames.get(exposure.node_id) || exposure.node_id}
                </span>
                <span className="text-slate-400">
                  {ACTIVITY_LABELS[exposure.activity_type] || exposure.activity_type}
                </span>
              </div>
            ))}
          </footer>
        </>
      )}
    </main>
  );
}
