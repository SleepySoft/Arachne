import { useCallback, useMemo, useState } from "react";
import { GraphEdge, IndustrialNode, Industry, Company } from "@/types";
import { BatchUploader } from "@/components/BatchUploader";
import { CompanyDetail } from "@/components/CompanyDetail";
import { CompanyForm } from "@/components/CompanyForm";
import { CompanyGraphEmptyState } from "@/components/CompanyGraphEmptyState";
import { CompanyNetworkCanvas } from "@/components/CompanyNetworkCanvas";
import { CompanySidebar } from "@/components/CompanySidebar";
import {
  getCompany,
  getCompanyNetwork,
  getCompanyUpstream,
  getCompanyDownstream,
  getExplorationGraph,
} from "@/services/api";
import { EdgeDetail } from "@/components/EdgeDetail";
import { EdgeForm } from "@/components/EdgeForm";
import { FilterPanel } from "@/components/FilterPanel";
import { GraphCanvas } from "@/components/GraphCanvas";
import { IndustryDetail } from "@/components/IndustryDetail";
import { IndustryForm } from "@/components/IndustryForm";
import { IndustrySidebar } from "@/components/IndustrySidebar";
import { Layout } from "@/components/Layout";
import { NodeDetail } from "@/components/NodeDetail";
import { NodeContextMenu } from "@/components/NodeContextMenu";
import { NodeCompaniesPanel } from "@/components/NodeCompaniesPanel";
import { NodeForm } from "@/components/NodeForm";
import { NodeIndustriesPanel } from "@/components/NodeIndustriesPanel";
import { SearchPanel } from "@/components/SearchPanel";
import { StatsBar, MainView } from "@/components/StatsBar";
import { CompanyViewVersions } from "@/components/CompanyViewVersions";
import { CompanyMaterialModal } from "@/components/CompanyMaterialModal";
import { ExplorationCanvas, ExplorationNode as ENode, ExplorationEdge as EEdge } from "@/components/ExplorationCanvas";
import { MaterialConnectionPanel } from "@/components/MaterialConnectionPanel";
import { CompanyRelationDetail } from "@/components/CompanyRelationDetail";

export type PanelType =
  | "none"
  | "node-detail"
  | "edge-detail"
  | "node-create"
  | "node-edit"
  | "edge-create"
  | "edge-edit"
  | "batch-upload"
  | "industry-detail"
  | "industry-create"
  | "industry-edit"
  | "company-detail"
  | "company-create"
  | "company-edit"
  | "node-companies"
  | "node-industries"
  | "company-relation-detail";

// Company network node type used for canvas
interface CNode {
  company_id: string;
  name_zh: string;
  company_type: string;
  status: string;
}

interface CEdge {
  from_company_id: string;
  to_company_id: string;
  path_count: number;
  strength: number;
  confidence: string;
  relation_type?: string;
  relation_subtype?: string;
}

export default function App() {
  // ------------------------------------------------------------------
  // Top-level workspace state
  // ------------------------------------------------------------------
  const [mainView, setMainView] = useState<MainView>("industrial_graph");
  const [industrialSubView, setIndustrialSubView] = useState<"filter" | "industry" | "company">("filter");
  const [companySubView, setCompanySubView] = useState<"version" | "company_list">("company_list");

  // ------------------------------------------------------------------
  // Industrial graph state
  // ------------------------------------------------------------------
  const [selectedNode, setSelectedNode] = useState<IndustrialNode | null>(null);
  const [selectedEdge, setSelectedEdge] = useState<GraphEdge | null>(null);
  const [selectedIndustry, setSelectedIndustry] = useState<Industry | null>(null);
  const [selectedCompany, setSelectedCompany] = useState<Company | null>(null);
  const [selectedRelation, setSelectedRelation] = useState<CEdge | null>(null);
  const [panel, setPanel] = useState<PanelType>("none");
  const [contextMenu, setContextMenu] = useState<{
    visible: boolean;
    x: number;
    y: number;
    node: IndustrialNode | null;
  }>({ visible: false, x: 0, y: 0, node: null });
  const [activeFilters, setActiveFilters] = useState({
    edgeNamespaces: ["industrial_flow", "ontology"] as string[],
    edgeTypes: [] as string[],
    entityTypes: [] as string[],
    status: [] as string[],
    confidence: [] as string[],
  });
  const [graphKey, setGraphKey] = useState(0);
  const [subgraphData, setSubgraphData] = useState<{ nodes: IndustrialNode[]; edges: GraphEdge[] } | undefined>(undefined);
  const [highlightNodeIds, setHighlightNodeIds] = useState<string[] | undefined>(undefined);

  // ------------------------------------------------------------------
  // Company graph state
  // ------------------------------------------------------------------
  const [companyDisplayMode, setCompanyDisplayMode] = useState<"empty" | "global" | "local">("empty");
  const [companyNetworkData, setCompanyNetworkData] = useState<{ nodes: CNode[]; edges: CEdge[] } | null>(null);

  // orderedChain: exploration path (max 2, oldest auto-removed)
  const [orderedChain, setOrderedChain] = useState<string[]>([]);
  // fixedIds: double-click pinned nodes, never auto-removed
  const [fixedIds, setFixedIds] = useState<Set<string>>(new Set());
  // nodeStore: cache of all nodes ever loaded
  const [nodeStore, setNodeStore] = useState<Map<string, CNode>>(new Map());
  // permanentEdges: edges between visible permanent nodes
  const [permanentEdges, setPermanentEdges] = useState<CEdge[]>([]);

  // Current focus: the node whose upstream/downstream are shown as preview
  const [currentFocusId, setCurrentFocusId] = useState<string | null>(null);

  // Preview: temporary translucent nodes/edges for the current focus
  const [previewData, setPreviewData] = useState<{ centerId: string; nodes: CNode[]; edges: CEdge[] } | null>(null);

  const [isDrawingGlobal, setIsDrawingGlobal] = useState(false);

  // Company explore mode: "bulk" = auto-load all upstream/downstream (current behavior)
  // "manual" = heterogeneous graph exploration (company + material nodes)
  const [companyExploreMode, setCompanyExploreMode] = useState<"bulk" | "manual">("bulk");

  // Exploration graph data (for manual mode)
  const [explorationData, setExplorationData] = useState<{ nodes: ENode[]; edges: EEdge[] } | null>(null);

  // Material panel state (for manual exploration mode)
  const [materialPanelOpen, setMaterialPanelOpen] = useState(false);
  const [selectedMaterialNode, setSelectedMaterialNode] = useState<{ id: string; name: string } | null>(null);

  // Material modal state
  const [materialModalOpen, setMaterialModalOpen] = useState(false);

  // Selected exploration edge for detail display
  const [selectedExplorationEdge, setSelectedExplorationEdge] = useState<EEdge | null>(null);

  // ------------------------------------------------------------------
  // Derived data for canvas
  // ------------------------------------------------------------------
  const permanentIds = useMemo(() => {
    const ids = new Set<string>([...orderedChain, ...fixedIds]);
    return ids;
  }, [orderedChain, fixedIds]);

  const allCompanyNodes = useMemo(() => {
    const map = new Map<string, CNode>();
    permanentIds.forEach((id) => {
      const node = nodeStore.get(id);
      if (node) map.set(id, node);
    });
    previewData?.nodes.forEach((n) => {
      if (!map.has(n.company_id)) map.set(n.company_id, n);
    });
    return Array.from(map.values());
  }, [permanentIds, nodeStore, previewData]);

  const allCompanyEdges = useMemo(() => {
    const seen = new Set<string>();
    const edges: CEdge[] = [];
    const key = (e: CEdge) => `${e.from_company_id}->${e.to_company_id}`;
    // Permanent edges (both ends still visible)
    permanentEdges.forEach((e) => {
      if (permanentIds.has(e.from_company_id) && permanentIds.has(e.to_company_id)) {
        if (!seen.has(key(e))) { seen.add(key(e)); edges.push(e); }
      }
    });
    previewData?.edges.forEach((e) => {
      if (!seen.has(key(e))) { seen.add(key(e)); edges.push(e); }
    });
    return edges;
  }, [permanentEdges, permanentIds, previewData]);

  const previewNodeIds = useMemo(() => {
    return previewData?.nodes.map((n) => n.company_id).filter((id) => !permanentIds.has(id)) ?? [];
  }, [previewData, permanentIds]);

  // ------------------------------------------------------------------
  // Handlers
  // ------------------------------------------------------------------
  const handleNodeClick = useCallback((node: IndustrialNode) => {
    setSelectedNode(node);
    setSelectedEdge(null);
    setPanel("node-detail");
    setContextMenu((prev) => ({ ...prev, visible: false }));
  }, []);

  const handleNodeContextMenu = useCallback((node: IndustrialNode, x: number, y: number) => {
    setContextMenu({ visible: true, x, y, node });
  }, []);

  const handleEdgeClick = useCallback((edge: GraphEdge) => {
    setSelectedEdge(edge);
    setSelectedNode(null);
    setPanel("edge-detail");
  }, []);

  const refreshGraph = () => setGraphKey((k) => k + 1);

  const handleChangeMainView = (view: MainView) => {
    setMainView(view);
    setPanel("none");
    setSelectedNode(null);
    setSelectedEdge(null);
    setSelectedIndustry(null);
    setSelectedCompany(null);
    if (view === "industrial_graph") {
      setSubgraphData(undefined);
      setHighlightNodeIds(undefined);
    } else {
      setCompanyDisplayMode("empty");
      setOrderedChain([]);
      setFixedIds(new Set());
      setNodeStore(new Map());
      setPermanentEdges([]);
      setCurrentFocusId(null);
      setPreviewData(null);
      setExplorationData(null);
    }
  };

  const handleSelectIndustry = (industry: Industry) => {
    setSelectedIndustry(industry);
    setPanel("industry-detail");
    setHighlightNodeIds(undefined);
  };

  // Select company from sidebar
  const handleSelectCompany = (company: Company) => {
    setSelectedCompany(company);
    setPanel("company-detail");
    setHighlightNodeIds(undefined);

    if (mainView !== "company_graph") return;

    const isManual = companyExploreMode === "manual";

    if (isManual) {
      // Manual/exploration mode: load heterogeneous graph centered on this company
      setCompanyDisplayMode("local");
      setCurrentFocusId(company.company_id);
      loadExplorationGraph(company.company_id);
      return;
    }

    if (companyDisplayMode === "empty") {
      startInvestigation(company, true);
    } else if (companyDisplayMode === "global") {
      setCurrentFocusId(company.company_id);
      loadPreview(company.company_id);
    } else if (companyDisplayMode === "local") {
      if (orderedChain.includes(company.company_id) || fixedIds.has(company.company_id)) {
        setCurrentFocusId(company.company_id);
        loadPreview(company.company_id);
      } else {
        startInvestigation(company, true);
      }
    }
  };

  // Start a new investigation chain from a company
  const startInvestigation = (company: Company, autoPreview: boolean = true) => {
    const node: CNode = {
      company_id: company.company_id,
      name_zh: company.name_zh,
      company_type: company.company_type || "unknown",
      status: "ACTIVE",
    };
    setOrderedChain([company.company_id]);
    setFixedIds(new Set());
    setNodeStore(new Map([[company.company_id, node]]));
    setPermanentEdges([]);
    setCurrentFocusId(company.company_id);
    setCompanyDisplayMode("local");
    setPreviewData(null);
    if (autoPreview) loadPreview(company.company_id);
  };

  // Load exploration graph (heterogeneous: company + material nodes)
  const loadExplorationGraph = async (companyId: string) => {
    try {
      const data = await getExplorationGraph(companyId);
      setExplorationData(data);
    } catch {
      setExplorationData(null);
    }
  };

  // Load preview (temporary translucent network) for a given company
  const loadPreview = async (companyId: string) => {
    try {
      const [upstream, downstream] = await Promise.all([
        getCompanyUpstream(companyId),
        getCompanyDownstream(companyId),
      ]);

      const nodeMap = new Map<string, CNode>();

      // Ensure the center company itself is in the node map
      const existingNode = nodeStore.get(companyId) || previewData?.nodes.find((n) => n.company_id === companyId);
      nodeMap.set(companyId, existingNode || { company_id: companyId, name_zh: companyId, company_type: "unknown", status: "ACTIVE" });

      upstream.forEach((u) => {
        if (!nodeMap.has(u.company_id)) {
          nodeMap.set(u.company_id, { company_id: u.company_id, name_zh: u.name_zh, company_type: u.company_type || "unknown", status: "ACTIVE" });
        }
      });
      downstream.forEach((d) => {
        if (!nodeMap.has(d.company_id)) {
          nodeMap.set(d.company_id, { company_id: d.company_id, name_zh: d.name_zh, company_type: d.company_type || "unknown", status: "ACTIVE" });
        }
      });

      const edges: CEdge[] = [];
      upstream.forEach((u) => {
        edges.push({ from_company_id: u.company_id, to_company_id: companyId, path_count: u.path_count, strength: u.strength, confidence: "MEDIUM" });
      });
      downstream.forEach((d) => {
        edges.push({ from_company_id: companyId, to_company_id: d.company_id, path_count: d.path_count, strength: d.strength, confidence: "MEDIUM" });
      });

      // Cache preview nodes in nodeStore
      setNodeStore((prev) => {
        const next = new Map(prev);
        nodeMap.forEach((n, id) => {
          if (!next.has(id)) next.set(id, n);
        });
        return next;
      });

      setPreviewData({ centerId: companyId, nodes: Array.from(nodeMap.values()), edges });
    } catch {
      setPreviewData(null);
    }
  };

  // Click on a node inside the exploration canvas (manual mode)
  const handleExplorationNodeClick = async (node: ENode) => {
    if (node.type === "company") {
      try {
        const full = await getCompany(node.id);
        setSelectedCompany(full);
      } catch {
        setSelectedCompany({
          company_id: node.id,
          name_zh: node.label,
          company_type: node.company_type || "unknown",
        } as Company);
      }
      setPanel("company-detail");
      setCurrentFocusId(node.id);
      setMaterialPanelOpen(false);
    } else {
      // Material node clicked: open connection panel
      setCurrentFocusId(node.id);
      setSelectedMaterialNode({ id: node.id, name: node.label });
      setMaterialPanelOpen(true);
    }
  };

  // Add selected companies to the exploration graph
  const handleAddCompaniesToExploration = (companies: { id: string; label: string; direction: "peer" | "upstream" | "downstream"; via_node_id?: string; via_node_name?: string; activity_type: string }[]) => {
    if (!explorationData || !selectedMaterialNode) return;

    const newNodes: ENode[] = [];
    const newEdges: EEdge[] = [];
    const existingNodeIds = new Set(explorationData.nodes.map((n) => n.id));
    const existingEdgeKeys = new Set(explorationData.edges.map((e) => `${e.source}→${e.target}`));

    companies.forEach((c) => {
      // Add company node if not exists
      if (!existingNodeIds.has(c.id)) {
        newNodes.push({
          id: c.id,
          type: "company",
          label: c.label,
          company_type: "unknown",
          activity_type: c.activity_type,
        });
        existingNodeIds.add(c.id);
      }

      // All directions connect directly to the selected material node
      const edgeKey = `${c.id}→${selectedMaterialNode.id}`;
      if (!existingEdgeKeys.has(edgeKey)) {
        newEdges.push({
          source: c.id,
          target: selectedMaterialNode.id,
          type: "exposure",
          activity_type: c.activity_type,
          label: c.direction === "peer" ? undefined : `via ${c.via_node_name || c.via_node_id || c.direction}`,
        });
        existingEdgeKeys.add(edgeKey);
      }
    });

    setExplorationData({
      nodes: [...explorationData.nodes, ...newNodes],
      edges: [...explorationData.edges, ...newEdges],
    });
  };

  // Click on a node inside the company network canvas
  const handleCompanyNodeClick = async (companyNode: CNode) => {
    const cid = companyNode.company_id;
    const isManual = companyExploreMode === "manual";

    // Always update detail panel
    try {
      const full = await getCompany(cid);
      setSelectedCompany(full);
    } catch {
      setSelectedCompany(companyNode as unknown as Company);
    }
    setPanel("company-detail");

    if (companyDisplayMode === "global") {
      if (currentFocusId === cid) {
        startInvestigation(companyNode as unknown as Company, !isManual);
      } else {
        setCurrentFocusId(cid);
        if (!isManual) loadPreview(cid);
      }
      return;
    }

    if (companyDisplayMode !== "local") return;

    const chainIndex = orderedChain.indexOf(cid);

    if (chainIndex >= 0) {
      // Click a chain node: truncate to this node
      const newChain = orderedChain.slice(0, chainIndex + 1);
      setOrderedChain(newChain);
      setCurrentFocusId(cid);
      if (!isManual) loadPreview(cid);
    } else if (previewData && cid !== previewData.centerId) {
      // Click a preview node: append to chain
      const newChain = [...orderedChain, cid];
      setOrderedChain(newChain);

      // Cache node
      setNodeStore((prev) => {
        const next = new Map(prev);
        next.set(cid, companyNode);
        return next;
      });

      // Add connecting edges to permanentEdges
      const visibleIds = new Set([...orderedChain, ...fixedIds]);
      const newEdges = previewData.edges.filter((e) =>
        (e.from_company_id === cid && visibleIds.has(e.to_company_id)) ||
        (e.to_company_id === cid && visibleIds.has(e.from_company_id))
      );
      if (newEdges.length > 0) {
        setPermanentEdges((prev) => {
          const seen = new Set(prev.map((e) => `${e.from_company_id}->${e.to_company_id}`));
          return [...prev, ...newEdges.filter((e) => !seen.has(`${e.from_company_id}->${e.to_company_id}`))];
        });
      }

      setCurrentFocusId(cid);
      loadPreview(cid);
    }
  };

  // Double-click on a node inside the company network canvas
  const handleCompanyNodeDblClick = async (companyNode: CNode) => {
    const cid = companyNode.company_id;

    if (companyDisplayMode === "global") {
      startInvestigation(companyNode as unknown as Company);
      return;
    }

    if (companyDisplayMode !== "local") return;

    if (previewData && previewData.centerId === cid) {
      // Double-click the current focus node: pin all current preview nodes
      const previewNodeIds = previewData.nodes.map((n) => n.company_id);
      setFixedIds((prev) => {
        const next = new Set(prev);
        previewNodeIds.forEach((id) => next.add(id));
        return next;
      });

      setNodeStore((prev) => {
        const next = new Map(prev);
        previewData.nodes.forEach((n) => {
          if (!next.has(n.company_id)) next.set(n.company_id, n);
        });
        return next;
      });

      setPermanentEdges((prev) => {
        const seen = new Set(prev.map((e) => `${e.from_company_id}->${e.to_company_id}`));
        const newEdges = previewData.edges.filter((e) => !seen.has(`${e.from_company_id}->${e.to_company_id}`));
        return [...prev, ...newEdges];
      });

      setPreviewData(null);
    }
  };

  // Click on an edge inside the company network canvas
  const handleCompanyEdgeClick = (edge: CEdge) => {
    setSelectedRelation(edge);
    setPanel("company-relation-detail");
  };

  const handleLoadSubgraph = (nodes: unknown[], edges: unknown[]) => {
    setSubgraphData({
      nodes: nodes as IndustrialNode[],
      edges: edges as GraphEdge[],
    });
    setGraphKey((k) => k + 1);
    setHighlightNodeIds(undefined);
  };

  const handleHighlightNodes = (nodeIds: string[]) => {
    setHighlightNodeIds(nodeIds);
    setSubgraphData(undefined);
  };

  // ------------------------------------------------------------------
  // Industrial Graph — Left Sidebar with sub-tabs
  // ------------------------------------------------------------------
  const industrialLeftSidebar = (
    <div className="flex h-full flex-col">
      <div className="flex border-b border-slate-700">
        <SubTab active={industrialSubView === "filter"} onClick={() => setIndustrialSubView("filter")} label="过滤" />
        <SubTab active={industrialSubView === "industry"} onClick={() => setIndustrialSubView("industry")} label="行业" />
        <SubTab active={industrialSubView === "company"} onClick={() => setIndustrialSubView("company")} label="公司" />
      </div>
      <div className="flex-1 overflow-auto">
        {industrialSubView === "filter" && (
          <FilterPanel filters={activeFilters} onChange={setActiveFilters} />
        )}
        {industrialSubView === "industry" && (
          <IndustrySidebar
            selectedId={selectedIndustry?.industry_id}
            onSelect={handleSelectIndustry}
            onCreate={() => setPanel("industry-create")}
          />
        )}
        {industrialSubView === "company" && (
          <CompanySidebar
            selectedId={selectedCompany?.company_id}
            onSelect={handleSelectCompany}
            onCreate={() => setPanel("company-create")}
          />
        )}
      </div>
    </div>
  );

  // ------------------------------------------------------------------
  // Company Graph — Left Sidebar with sub-tabs
  // ------------------------------------------------------------------
  const companyLeftSidebar = (
    <div className="flex h-full flex-col">
      <div className="flex border-b border-slate-700">
        <SubTab active={companySubView === "company_list"} onClick={() => setCompanySubView("company_list")} label="公司列表" />
        <SubTab active={companySubView === "version"} onClick={() => setCompanySubView("version")} label="版本" />
      </div>
      <div className="flex-1 overflow-auto">
        {companySubView === "company_list" && (
          <CompanySidebar
            selectedId={selectedCompany?.company_id}
            onSelect={handleSelectCompany}
            onCreate={() => setPanel("company-create")}
          />
        )}
        {companySubView === "version" && (
          <CompanyViewVersions
            onViewNetwork={() => {
              setCompanyDisplayMode("empty");
              setOrderedChain([]);
              setFixedIds(new Set());
              setNodeStore(new Map());
              setPermanentEdges([]);
              setCurrentFocusId(null);
              setPreviewData(null);
            }}
          />
        )}
      </div>
    </div>
  );

  // ------------------------------------------------------------------
  // Search panel / Toolbar area
  // ------------------------------------------------------------------
  const industrialSearchPanel = (
    <div className="flex items-center gap-2">
      {industrialSubView === "filter" && (
        <SearchPanel
          onSelectNode={(node) => {
            setSelectedNode(node);
            setPanel("node-detail");
          }}
          onCreateNode={() => setPanel("node-create")}
          onCreateEdge={() => setPanel("edge-create")}
          onUploadBatch={() => setPanel("batch-upload")}
        />
      )}
      {industrialSubView === "industry" && (
        <span className="text-xs text-slate-500">点击左侧行业在图谱中查看其子图</span>
      )}
      {industrialSubView === "company" && (
        <span className="text-xs text-slate-500">点击左侧公司在图谱中高亮其暴露节点</span>
      )}
      {(subgraphData !== undefined || highlightNodeIds !== undefined) && (
        <button
          onClick={() => {
            setSubgraphData(undefined);
            setHighlightNodeIds(undefined);
            setGraphKey((k) => k + 1);
          }}
          className="ml-auto flex items-center gap-1 rounded-md bg-amber-600/20 px-2.5 py-1 text-xs font-medium text-amber-400 hover:bg-amber-600/30 transition-colors"
        >
          返回全图
        </button>
      )}
    </div>
  );

  const companySearchPanel = (
    <div className="flex items-center gap-2">
      <div className="flex items-center rounded border border-slate-700 bg-slate-800/50 overflow-hidden">
        <button
          onClick={() => setCompanyExploreMode("bulk")}
          className={`px-2 py-1 text-[10px] font-medium transition-colors ${
            companyExploreMode === "bulk"
              ? "bg-cyan-600/20 text-cyan-400"
              : "text-slate-500 hover:text-slate-300"
          }`}
          title="自动加载全部上下游关联"
        >
          全量
        </button>
        <button
          onClick={() => setCompanyExploreMode("manual")}
          className={`px-2 py-1 text-[10px] font-medium transition-colors ${
            companyExploreMode === "manual"
              ? "bg-cyan-600/20 text-cyan-400"
              : "text-slate-500 hover:text-slate-300"
          }`}
          title="只显示通过物料关联面板选择的公司"
        >
          探索
        </button>
      </div>
      {companyDisplayMode === "empty" && (
        <span className="text-xs text-slate-500">选择一个公司开始浏览，或绘制全局图</span>
      )}
      {companyDisplayMode === "local" && (
        <div className="flex items-center gap-1 overflow-hidden">
          {companyExploreMode === "manual" ? (
            selectedExplorationEdge ? (
              <span className="text-xs text-slate-300">
                {selectedExplorationEdge.type === "exposure"
                  ? `${selectedExplorationEdge.source} exposes ${selectedExplorationEdge.target} (${selectedExplorationEdge.activity_type || ""})`
                  : `${selectedExplorationEdge.source} → ${selectedExplorationEdge.target} (${selectedExplorationEdge.edge_type || "industrial_flow"})`}
              </span>
            ) : (
              <span className="text-xs text-slate-500">点击物料节点探索关联公司，点击边查看连接详情</span>
            )
          ) : (
            <>
              {orderedChain.map((id, idx) => (
                <span key={id} className="flex items-center gap-1">
                  {idx > 0 && <span className="text-slate-600">→</span>}
                  <span className={`text-xs ${id === currentFocusId ? "text-cyan-400 font-medium" : "text-slate-400"}`}>
                    {nodeStore.get(id)?.name_zh || id}
                  </span>
                </span>
              ))}
              {fixedIds.size > 0 && (
                <span className="text-xs text-amber-500 ml-1">
                  (+{fixedIds.size} 固定)
                </span>
              )}
              {previewData && (
                <span className="text-xs text-slate-500 ml-1">— 关联节点临时显示</span>
              )}
            </>
          )}
        </div>
      )}
      {companyDisplayMode === "global" && (
        <span className="text-xs text-slate-500">全局网络视图 — 点击节点高亮，双击开始考察</span>
      )}
      {companyDisplayMode !== "empty" && (
        <button
          onClick={() => {
            setCompanyDisplayMode("empty");
            setOrderedChain([]);
            setFixedIds(new Set());
            setNodeStore(new Map());
            setPermanentEdges([]);
            setCurrentFocusId(null);
            setPreviewData(null);
            setExplorationData(null);
            setSelectedExplorationEdge(null);
            setMaterialPanelOpen(false);
          }}
          className="ml-auto flex items-center gap-1 rounded-md bg-amber-600/20 px-2.5 py-1 text-xs font-medium text-amber-400 hover:bg-amber-600/30 transition-colors"
        >
          清空视图
        </button>
      )}
    </div>
  );

  // ------------------------------------------------------------------
  // Right Panel (shared detail panels)
  // ------------------------------------------------------------------
  const rightPanel =
    panel === "node-detail" && selectedNode ? (
      <NodeDetail
        node={selectedNode}
        onEdit={() => setPanel("node-edit")}
        onClose={() => { setPanel("none"); setSelectedNode(null); }}
        onRefresh={refreshGraph}
      />
    ) : panel === "edge-detail" && selectedEdge ? (
      <EdgeDetail
        edge={selectedEdge}
        onEdit={() => setPanel("edge-edit")}
        onClose={() => { setPanel("none"); setSelectedEdge(null); }}
        onRefresh={refreshGraph}
      />
    ) : panel === "node-create" ? (
      <NodeForm
        mode="create"
        onClose={() => setPanel("none")}
        onSuccess={(node) => { setSelectedNode(node); setPanel("node-detail"); refreshGraph(); }}
      />
    ) : panel === "node-edit" && selectedNode ? (
      <NodeForm
        mode="edit"
        node={selectedNode}
        onClose={() => setPanel("node-detail")}
        onSuccess={(node) => { setSelectedNode(node); setPanel("node-detail"); refreshGraph(); }}
      />
    ) : panel === "edge-create" ? (
      <EdgeForm
        mode="create"
        onClose={() => setPanel("none")}
        onSuccess={(edge) => { setSelectedEdge(edge); setPanel("edge-detail"); refreshGraph(); }}
      />
    ) : panel === "edge-edit" && selectedEdge ? (
      <EdgeForm
        mode="edit"
        edge={selectedEdge}
        onClose={() => setPanel("edge-detail")}
        onSuccess={(edge) => { setSelectedEdge(edge); setPanel("edge-detail"); refreshGraph(); }}
      />
    ) : panel === "batch-upload" ? (
      <BatchUploader onClose={() => setPanel("none")} onSuccess={refreshGraph} />
    ) : panel === "industry-detail" && selectedIndustry ? (
      <IndustryDetail
        industry={selectedIndustry}
        onEdit={() => setPanel("industry-edit")}
        onClose={() => { setPanel("none"); setSelectedIndustry(null); }}
        onRefresh={refreshGraph}
        onLoadSubgraph={handleLoadSubgraph}
        onHighlightNodes={handleHighlightNodes}
        onAddMapping={() => alert("添加映射功能待实现")}
      />
    ) : panel === "industry-create" ? (
      <IndustryForm
        mode="create"
        onClose={() => setPanel("none")}
        onSuccess={(ind) => { setSelectedIndustry(ind); setPanel("industry-detail"); }}
      />
    ) : panel === "industry-edit" && selectedIndustry ? (
      <IndustryForm
        mode="edit"
        industry={selectedIndustry}
        onClose={() => setPanel("industry-detail")}
        onSuccess={(ind) => { setSelectedIndustry(ind); setPanel("industry-detail"); }}
      />
    ) : panel === "company-relation-detail" && selectedRelation ? (
      <CompanyRelationDetail
        fromCompanyId={selectedRelation.from_company_id}
        toCompanyId={selectedRelation.to_company_id}
        relationType={selectedRelation.relation_type}
        relationSubtype={selectedRelation.relation_subtype}
        pathCount={selectedRelation.path_count}
        onClose={() => { setPanel("none"); setSelectedRelation(null); }}
      />
    ) : panel === "company-detail" && selectedCompany ? (
      <CompanyDetail
        company={selectedCompany}
        onEdit={() => setPanel("company-edit")}
        onClose={() => { setPanel("none"); setSelectedCompany(null); }}
        onRefresh={refreshGraph}
        onFocusInGraph={(id) => setCurrentFocusId(id)}
        onOpenMaterialModal={() => setMaterialModalOpen(true)}
        onAddExposure={() => alert("添加暴露功能待实现")}
      />
    ) : panel === "company-create" ? (
      <CompanyForm
        mode="create"
        onClose={() => setPanel("none")}
        onSuccess={(co) => { setSelectedCompany(co); setPanel("company-detail"); }}
      />
    ) : panel === "company-edit" && selectedCompany ? (
      <CompanyForm
        mode="edit"
        company={selectedCompany}
        onClose={() => setPanel("company-detail")}
        onSuccess={(co) => { setSelectedCompany(co); setPanel("company-detail"); }}
      />
    ) : panel === "node-companies" && contextMenu.node ? (
      <NodeCompaniesPanel
        nodeId={contextMenu.node.node_id}
        nodeName={contextMenu.node.canonical_name_zh}
        onClose={() => setPanel("none")}
        onSelectCompany={(company) => { setSelectedCompany(company); setPanel("company-detail"); }}
      />
    ) : panel === "node-industries" && contextMenu.node ? (
      <NodeIndustriesPanel
        nodeId={contextMenu.node.node_id}
        nodeName={contextMenu.node.canonical_name_zh}
        onClose={() => setPanel("none")}
        onSelectIndustry={(industry) => { setSelectedIndustry(industry); setPanel("industry-detail"); }}
      />
    ) : null;

  // ------------------------------------------------------------------
  // Center Canvas
  // ------------------------------------------------------------------
  const centerCanvas =
    mainView === "company_graph" ? (
      companyDisplayMode === "empty" ? (
        <CompanyGraphEmptyState
          companyCount={companyNetworkData?.nodes.length ?? 200}
          relationCount={companyNetworkData?.edges.length ?? 1142}
          onDrawGlobal={() => {
            setIsDrawingGlobal(true);
            getCompanyNetwork()
              .then((data) => {
                setCompanyNetworkData(data);
                setCompanyDisplayMode("global");
                setCurrentFocusId(null);
                setIsDrawingGlobal(false);
              })
              .catch(() => setIsDrawingGlobal(false));
          }}
          isLoading={isDrawingGlobal}
        />
      ) : companyDisplayMode === "local" ? (
        companyExploreMode === "manual" ? (
          <ExplorationCanvas
            nodes={explorationData?.nodes ?? []}
            edges={explorationData?.edges ?? []}
            onNodeClick={handleExplorationNodeClick}
            onEdgeClick={(edge) => setSelectedExplorationEdge(edge)}
            highlightNodeId={currentFocusId}
          />
        ) : (
          <CompanyNetworkCanvas
            nodes={allCompanyNodes}
            edges={allCompanyEdges}
            highlightCompanyId={currentFocusId}
            previewNodeIds={previewNodeIds}
            onNodeClick={handleCompanyNodeClick}
            onNodeDblClick={handleCompanyNodeDblClick}
            onEdgeClick={handleCompanyEdgeClick}
          />
        )
      ) : companyDisplayMode === "global" && companyNetworkData ? (
        <CompanyNetworkCanvas
          nodes={companyNetworkData.nodes}
          edges={companyNetworkData.edges}
          highlightCompanyId={currentFocusId}
          dimUnrelated={!!currentFocusId}
          onNodeClick={handleCompanyNodeClick}
          onNodeDblClick={handleCompanyNodeDblClick}
          onEdgeClick={handleCompanyEdgeClick}
        />
      ) : (
        <div className="flex h-full w-full items-center justify-center bg-slate-950">
          <div className="text-sm text-slate-500">加载中...</div>
        </div>
      )
    ) : (
      <GraphCanvas
        key={graphKey}
        onNodeClick={handleNodeClick}
        onEdgeClick={handleEdgeClick}
        onNodeContextMenu={handleNodeContextMenu}
        filters={activeFilters}
        highlightNodeId={selectedNode?.node_id}
        highlightNodeIds={highlightNodeIds}
        sourceData={subgraphData}
      />
    );

  // ------------------------------------------------------------------
  // Render
  // ------------------------------------------------------------------
  return (
    <>
      <Layout
        topBar={<StatsBar mainView={mainView} onChangeMainView={handleChangeMainView} />}
        leftSidebar={mainView === "industrial_graph" ? industrialLeftSidebar : companyLeftSidebar}
        centerCanvas={centerCanvas}
        searchPanel={mainView === "industrial_graph" ? industrialSearchPanel : companySearchPanel}
        rightPanel={rightPanel}
      />
      {contextMenu.visible && contextMenu.node && (
        <NodeContextMenu
          x={contextMenu.x}
          y={contextMenu.y}
          nodeName={contextMenu.node.canonical_name_zh}
          onShowCompanies={() => { setPanel("node-companies"); setContextMenu((prev) => ({ ...prev, visible: false })); }}
          onShowIndustries={() => { setPanel("node-industries"); setContextMenu((prev) => ({ ...prev, visible: false })); }}
          onClose={() => setContextMenu((prev) => ({ ...prev, visible: false }))}
        />
      )}
      {selectedCompany && materialModalOpen && (
        <CompanyMaterialModal
          companyId={selectedCompany.company_id}
          companyName={selectedCompany.name_zh}
          isOpen={materialModalOpen}
          onClose={() => setMaterialModalOpen(false)}
          onAddToView={(nodes, edges) => {
            setNodeStore((prev) => {
              const next = new Map(prev);
              nodes.forEach((n) => {
                if (!next.has(n.company_id)) next.set(n.company_id, n);
              });
              return next;
            });
            setPermanentEdges((prev) => {
              const seen = new Set(prev.map((e) => `${e.from_company_id}->${e.to_company_id}`));
              const newEdges = edges.filter((e) => !seen.has(`${e.from_company_id}->${e.to_company_id}`));
              return [...prev, ...newEdges];
            });
            if (selectedCompany) {
              setNodeStore((prev) => {
                const next = new Map(prev);
                if (!next.has(selectedCompany.company_id)) {
                  next.set(selectedCompany.company_id, {
                    company_id: selectedCompany.company_id,
                    name_zh: selectedCompany.name_zh,
                    company_type: selectedCompany.company_type || "unknown",
                    status: "ACTIVE",
                  });
                }
                return next;
              });
            }
            setCompanyDisplayMode("local");
            setCurrentFocusId(selectedCompany.company_id);
          }}
        />
      )}
      {materialPanelOpen && selectedMaterialNode && selectedCompany && (
        <MaterialConnectionPanel
          nodeId={selectedMaterialNode.id}
          nodeName={selectedMaterialNode.name}
          anchorCompanyId={selectedCompany.company_id}
          isOpen={materialPanelOpen}
          onClose={() => setMaterialPanelOpen(false)}
          onAddCompanies={handleAddCompaniesToExploration}
        />
      )}
    </>
  );
}

// ---------------------------------------------------------------------------
// Sub-tab component for left sidebar
// ---------------------------------------------------------------------------
function SubTab({
  active,
  onClick,
  label,
}: {
  active: boolean;
  onClick: () => void;
  label: string;
}) {
  return (
    <button
      onClick={onClick}
      className={`flex-1 px-2 py-2 text-[11px] font-medium transition-colors ${
        active
          ? "border-b-2 border-cyan-500 text-cyan-400"
          : "text-slate-500 hover:text-slate-300"
      }`}
    >
      {label}
    </button>
  );
}
