import { useCallback, useState } from "react";
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
  | "node-industries";

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
  const [companyNetworkData, setCompanyNetworkData] = useState<{
    nodes: { company_id: string; name_zh: string; company_type: string; status: string }[];
    edges: { from_company_id: string; to_company_id: string; path_count: number; strength: number; confidence: string }[];
  } | null>(null);
  const [localNetworkData, setLocalNetworkData] = useState<{
    nodes: { company_id: string; name_zh: string; company_type: string; status: string }[];
    edges: { from_company_id: string; to_company_id: string; path_count: number; strength: number; confidence: string }[];
  } | null>(null);
  const [focusCompanyId, setFocusCompanyId] = useState<string | null>(null);
  const [isDrawingGlobal, setIsDrawingGlobal] = useState(false);

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
      // Reset company view state when switching to company graph
      setCompanyDisplayMode("empty");
      setFocusCompanyId(null);
      setLocalNetworkData(null);
    }
  };

  const handleSelectIndustry = (industry: Industry) => {
    setSelectedIndustry(industry);
    setPanel("industry-detail");
    setHighlightNodeIds(undefined);
  };

  // Select company from sidebar (context-aware)
  const handleSelectCompany = (company: Company) => {
    setSelectedCompany(company);
    setPanel("company-detail");
    setHighlightNodeIds(undefined);

    if (mainView === "company_graph") {
      if (companyDisplayMode === "empty" || companyDisplayMode === "local") {
        loadLocalNetwork(company);
      } else if (companyDisplayMode === "global") {
        setFocusCompanyId(company.company_id);
      }
    }
  };

  // Load local network centered on a company
  const loadLocalNetwork = async (company: Company) => {
    try {
      const [upstream, downstream] = await Promise.all([
        getCompanyUpstream(company.company_id),
        getCompanyDownstream(company.company_id),
      ]);

      const nodeMap = new Map<string, { company_id: string; name_zh: string; company_type: string; status: string }>();

      // Add center company
      nodeMap.set(company.company_id, {
        company_id: company.company_id,
        name_zh: company.name_zh,
        company_type: company.company_type || "unknown",
        status: "ACTIVE",
      });

      // Add upstream companies
      upstream.forEach((u) => {
        if (!nodeMap.has(u.company_id)) {
          nodeMap.set(u.company_id, {
            company_id: u.company_id,
            name_zh: u.name_zh,
            company_type: u.company_type || "unknown",
            status: "ACTIVE",
          });
        }
      });

      // Add downstream companies
      downstream.forEach((d) => {
        if (!nodeMap.has(d.company_id)) {
          nodeMap.set(d.company_id, {
            company_id: d.company_id,
            name_zh: d.name_zh,
            company_type: d.company_type || "unknown",
            status: "ACTIVE",
          });
        }
      });

      const localEdges: {
        from_company_id: string;
        to_company_id: string;
        path_count: number;
        strength: number;
        confidence: string;
      }[] = [];

      upstream.forEach((u) => {
        localEdges.push({
          from_company_id: u.company_id,
          to_company_id: company.company_id,
          path_count: u.path_count,
          strength: u.strength,
          confidence: "MEDIUM",
        });
      });

      downstream.forEach((d) => {
        localEdges.push({
          from_company_id: company.company_id,
          to_company_id: d.company_id,
          path_count: d.path_count,
          strength: d.strength,
          confidence: "MEDIUM",
        });
      });

      setLocalNetworkData({
        nodes: Array.from(nodeMap.values()),
        edges: localEdges,
      });
      setCompanyDisplayMode("local");
      setFocusCompanyId(company.company_id);
    } catch {
      // Fallback: show just the company node
      setLocalNetworkData({
        nodes: [{
          company_id: company.company_id,
          name_zh: company.name_zh,
          company_type: company.company_type || "unknown",
          status: "ACTIVE",
        }],
        edges: [],
      });
      setCompanyDisplayMode("local");
      setFocusCompanyId(company.company_id);
    }
  };

  // Click on a node inside the company network canvas
  const handleCompanyNodeClick = async (companyNode: { company_id: string; name_zh: string; company_type: string; status: string }) => {
    try {
      const full = await getCompany(companyNode.company_id);
      setSelectedCompany(full);
    } catch {
      setSelectedCompany(companyNode as unknown as Company);
    }
    setPanel("company-detail");

    if (companyDisplayMode === "global") {
      setFocusCompanyId(companyNode.company_id);
    } else if (companyDisplayMode === "local") {
      // Expand local network by loading the clicked company's neighbors
      const centerCompany = selectedCompany;
      if (centerCompany && centerCompany.company_id !== companyNode.company_id) {
        loadLocalNetwork(companyNode as unknown as Company);
      }
    }
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
              // After recompute completes, stay in empty mode — user must click "Draw Global" manually
              setCompanyDisplayMode("empty");
              setFocusCompanyId(null);
              setLocalNetworkData(null);
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
      {companyDisplayMode === "empty" && (
        <span className="text-xs text-slate-500">选择一个公司开始浏览，或绘制全局图</span>
      )}
      {companyDisplayMode === "local" && (
        <span className="text-xs text-slate-500">局部网络视图 — 点击节点可切换中心公司</span>
      )}
      {companyDisplayMode === "global" && (
        <span className="text-xs text-slate-500">全局网络视图 — 点击节点高亮其关联关系</span>
      )}
      {companyDisplayMode !== "empty" && (
        <button
          onClick={() => {
            setCompanyDisplayMode("empty");
            setFocusCompanyId(null);
            setLocalNetworkData(null);
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
    ) : panel === "company-detail" && selectedCompany ? (
      <CompanyDetail
        company={selectedCompany}
        onEdit={() => setPanel("company-edit")}
        onClose={() => { setPanel("none"); setSelectedCompany(null); }}
        onRefresh={refreshGraph}
        onLoadSubgraph={handleLoadSubgraph}
        onHighlightNodes={handleHighlightNodes}
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
                setFocusCompanyId(null);
                setIsDrawingGlobal(false);
              })
              .catch(() => {
                setIsDrawingGlobal(false);
              });
          }}
          isLoading={isDrawingGlobal}
        />
      ) : companyDisplayMode === "local" && localNetworkData ? (
        <CompanyNetworkCanvas
          nodes={localNetworkData.nodes}
          edges={localNetworkData.edges}
          highlightCompanyId={focusCompanyId}
          onNodeClick={handleCompanyNodeClick}
        />
      ) : companyDisplayMode === "global" && companyNetworkData ? (
        <CompanyNetworkCanvas
          nodes={companyNetworkData.nodes}
          edges={companyNetworkData.edges}
          highlightCompanyId={focusCompanyId}
          dimUnrelated={!!focusCompanyId}
          onNodeClick={handleCompanyNodeClick}
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
