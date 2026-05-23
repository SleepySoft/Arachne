import { useCallback, useEffect, useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { X } from "lucide-react";
import { GraphEdge, IndustrialNode, Industry, Company } from "@/types";
import { BatchUploader } from "@/components/BatchUploader";
import { CompanyDetail } from "@/components/CompanyDetail";
import { CompanyForm } from "@/components/CompanyForm";
import { CompanySubgraphPanel } from "@/components/CompanySubgraphPanel";
import { CompanyNetworkCanvas } from "@/components/CompanyNetworkCanvas";
import { CompanySidebar } from "@/components/CompanySidebar";
import { getCompany, getCompanyNetwork, computeAllCompanyRelations } from "@/services/api";
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
import { StatsBar, ViewMode } from "@/components/StatsBar";

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
  | "company-subgraphs"
  | "node-companies"
  | "node-industries";

function GlobalRecomputeButton() {
  const mutation = useMutation({
    mutationFn: computeAllCompanyRelations,
    onSuccess: (data) => {
      alert("全局关系重算任务已启动，job_id: " + data.job_id);
    },
    onError: (err: unknown) => {
      alert("重算失败: " + (err instanceof Error ? err.message : String(err)));
    },
  });

  return (
    <button
      onClick={() => mutation.mutate()}
      disabled={mutation.isPending}
      className="rounded px-2 py-0.5 text-[10px] text-amber-400 hover:bg-amber-900/20 disabled:opacity-50"
    >
      {mutation.isPending ? "重算中..." : "全局重算关系"}
    </button>
  );
}

export default function App() {
  const [viewMode, setViewMode] = useState<ViewMode>("graph");

  // Graph selection state
  const [selectedNode, setSelectedNode] = useState<IndustrialNode | null>(null);
  const [selectedEdge, setSelectedEdge] = useState<GraphEdge | null>(null);

  // Industry state
  const [selectedIndustry, setSelectedIndustry] = useState<Industry | null>(null);

  // Company state
  const [selectedCompany, setSelectedCompany] = useState<Company | null>(null);

  // Panel state
  const [panel, setPanel] = useState<PanelType>("none");

  // Context menu state
  const [contextMenu, setContextMenu] = useState<{
    visible: boolean;
    x: number;
    y: number;
    node: IndustrialNode | null;
  }>({ visible: false, x: 0, y: 0, node: null });

  // Filters
  const [activeFilters, setActiveFilters] = useState({
    edgeNamespaces: ["industrial_flow", "ontology"] as string[],
    edgeTypes: [] as string[],
    entityTypes: [] as string[],
    status: [] as string[],
    confidence: [] as string[],
  });

  // Graph refresh key
  const [graphKey, setGraphKey] = useState(0);

  // Subgraph data for industry/company views
  const [subgraphData, setSubgraphData] = useState<{ nodes: IndustrialNode[]; edges: GraphEdge[] } | undefined>(
    undefined
  );

  // Highlight node ids for industry/company focus on full graph
  const [highlightNodeIds, setHighlightNodeIds] = useState<string[] | undefined>(undefined);

  // Company network view state
  const [companyNetworkVisible, setCompanyNetworkVisible] = useState(false);
  const [companyNetworkData, setCompanyNetworkData] = useState<{
    nodes: { company_id: string; name_zh: string; company_type: string; status: string }[];
    edges: { from_company_id: string; to_company_id: string; relation_type: string; relation_subtype: string | null; strength: number; confidence: string }[];
  } | null>(null);

  const handleNodeClick = useCallback((node: IndustrialNode) => {
    setSelectedNode(node);
    setSelectedEdge(null);
    setPanel("node-detail");
    setContextMenu((prev) => ({ ...prev, visible: false }));
  }, []);

  const handleNodeContextMenu = useCallback(
    (node: IndustrialNode, x: number, y: number) => {
      setContextMenu({ visible: true, x, y, node });
    },
    []
  );

  const handleEdgeClick = useCallback((edge: GraphEdge) => {
    setSelectedEdge(edge);
    setSelectedNode(null);
    setPanel("edge-detail");
  }, []);

  const refreshGraph = () => {
    setGraphKey((k) => k + 1);
  };

  const handleViewChange = (mode: ViewMode) => {
    setViewMode(mode);
    setPanel("none");
    setSelectedNode(null);
    setSelectedEdge(null);
    setSelectedIndustry(null);
    setSelectedCompany(null);
    setCompanyNetworkVisible(mode === "companies");
    if (mode === "graph") {
      setSubgraphData(undefined);
    }
  };

  // Load company network data when entering companies view
  useEffect(() => {
    if (viewMode === "companies") {
      getCompanyNetwork().then(setCompanyNetworkData).catch(() => setCompanyNetworkData(null));
    }
  }, [viewMode]);

  const handleSelectIndustry = (industry: Industry) => {
    setSelectedIndustry(industry);
    setPanel("industry-detail");
    setHighlightNodeIds(undefined);
  };

  const handleSelectCompany = (company: Company) => {
    setSelectedCompany(company);
    setPanel("company-detail");
    setHighlightNodeIds(undefined);
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
    // Clear subgraph to show full graph with highlights
    setSubgraphData(undefined);
  };

  return (
    <>
      <Layout
        topBar={
          <StatsBar
            viewMode={viewMode}
            onChangeView={handleViewChange}
            isSubgraphView={subgraphData !== undefined || highlightNodeIds !== undefined}
            onResetToFullGraph={() => {
              setSubgraphData(undefined);
              setHighlightNodeIds(undefined);
              setGraphKey((k) => k + 1);
            }}
          />
        }
      leftSidebar={
        viewMode === "graph" ? (
          <FilterPanel filters={activeFilters} onChange={setActiveFilters} />
        ) : viewMode === "industries" ? (
          <IndustrySidebar
            selectedId={selectedIndustry?.industry_id}
            onSelect={handleSelectIndustry}
            onCreate={() => setPanel("industry-create")}
          />
        ) : (
          <CompanySidebar
            selectedId={selectedCompany?.company_id}
            onSelect={handleSelectCompany}
            onCreate={() => setPanel("company-create")}
          />
        )
      }
      centerCanvas={
        viewMode === "companies" && companyNetworkVisible && companyNetworkData ? (
          <CompanyNetworkCanvas
            nodes={companyNetworkData.nodes}
            edges={companyNetworkData.edges}
            onNodeClick={async (company) => {
              try {
                const full = await getCompany(company.company_id);
                setSelectedCompany(full);
              } catch {
                setSelectedCompany(company as unknown as Company);
              }
              setPanel("company-detail");
            }}
          />
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
        )
      }
      searchPanel={
        viewMode === "graph" ? (
          <SearchPanel
            onSelectNode={(node) => {
              setSelectedNode(node);
              setPanel("node-detail");
            }}
            onCreateNode={() => setPanel("node-create")}
            onCreateEdge={() => setPanel("edge-create")}
            onUploadBatch={() => setPanel("batch-upload")}
          />
        ) : viewMode === "industries" ? (
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-500">
              点击左侧行业在图谱中查看其子图
            </span>
          </div>
        ) : (
          <div className="flex items-center gap-2">
            <button
              onClick={() => setCompanyNetworkVisible(true)}
              className={`rounded px-2 py-0.5 text-[10px] ${companyNetworkVisible ? "bg-cyan-900/30 text-cyan-400" : "text-slate-400 hover:bg-slate-800"}`}
            >
              公司关系网络
            </button>
            <button
              onClick={() => setCompanyNetworkVisible(false)}
              className={`rounded px-2 py-0.5 text-[10px] ${!companyNetworkVisible ? "bg-cyan-900/30 text-cyan-400" : "text-slate-400 hover:bg-slate-800"}`}
            >
              产业图
            </button>
            <button
              onClick={() => {
                if (selectedCompany) {
                  setPanel("company-subgraphs");
                } else {
                  alert("请先选择一个公司");
                }
              }}
              className={`rounded px-2 py-0.5 text-[10px] ${panel === "company-subgraphs" ? "bg-cyan-900/30 text-cyan-400" : "text-slate-400 hover:bg-slate-800"}`}
            >
              子图版本
            </button>
            <GlobalRecomputeButton />
          </div>
        )
      }
      rightPanel={
        panel === "node-detail" && selectedNode ? (
          <NodeDetail
            node={selectedNode}
            onEdit={() => setPanel("node-edit")}
            onClose={() => {
              setPanel("none");
              setSelectedNode(null);
            }}
            onRefresh={refreshGraph}
          />
        ) : panel === "edge-detail" && selectedEdge ? (
          <EdgeDetail
            edge={selectedEdge}
            onEdit={() => setPanel("edge-edit")}
            onClose={() => {
              setPanel("none");
              setSelectedEdge(null);
            }}
            onRefresh={refreshGraph}
          />
        ) : panel === "node-create" ? (
          <NodeForm
            mode="create"
            onClose={() => setPanel("none")}
            onSuccess={(node) => {
              setSelectedNode(node);
              setPanel("node-detail");
              refreshGraph();
            }}
          />
        ) : panel === "node-edit" && selectedNode ? (
          <NodeForm
            mode="edit"
            node={selectedNode}
            onClose={() => setPanel("node-detail")}
            onSuccess={(node) => {
              setSelectedNode(node);
              setPanel("node-detail");
              refreshGraph();
            }}
          />
        ) : panel === "edge-create" ? (
          <EdgeForm
            mode="create"
            onClose={() => setPanel("none")}
            onSuccess={(edge) => {
              setSelectedEdge(edge);
              setPanel("edge-detail");
              refreshGraph();
            }}
          />
        ) : panel === "edge-edit" && selectedEdge ? (
          <EdgeForm
            mode="edit"
            edge={selectedEdge}
            onClose={() => setPanel("edge-detail")}
            onSuccess={(edge) => {
              setSelectedEdge(edge);
              setPanel("edge-detail");
              refreshGraph();
            }}
          />
        ) : panel === "batch-upload" ? (
          <BatchUploader onClose={() => setPanel("none")} onSuccess={refreshGraph} />
        ) : panel === "industry-detail" && selectedIndustry ? (
          <IndustryDetail
            industry={selectedIndustry}
            onEdit={() => setPanel("industry-edit")}
            onClose={() => {
              setPanel("none");
              setSelectedIndustry(null);
            }}
            onRefresh={refreshGraph}
            onLoadSubgraph={handleLoadSubgraph}
            onHighlightNodes={handleHighlightNodes}
            onAddMapping={() => alert("添加映射功能待实现")}
          />
        ) : panel === "industry-create" ? (
          <IndustryForm
            mode="create"
            onClose={() => setPanel("none")}
            onSuccess={(ind) => {
              setSelectedIndustry(ind);
              setPanel("industry-detail");
            }}
          />
        ) : panel === "industry-edit" && selectedIndustry ? (
          <IndustryForm
            mode="edit"
            industry={selectedIndustry}
            onClose={() => setPanel("industry-detail")}
            onSuccess={(ind) => {
              setSelectedIndustry(ind);
              setPanel("industry-detail");
            }}
          />
        ) : panel === "company-detail" && selectedCompany ? (
          <CompanyDetail
            company={selectedCompany}
            onEdit={() => setPanel("company-edit")}
            onClose={() => {
              setPanel("none");
              setSelectedCompany(null);
            }}
            onRefresh={refreshGraph}
            onLoadSubgraph={handleLoadSubgraph}
            onHighlightNodes={handleHighlightNodes}
            onAddExposure={() => alert("添加暴露功能待实现")}
          />
        ) : panel === "company-create" ? (
          <CompanyForm
            mode="create"
            onClose={() => setPanel("none")}
            onSuccess={(co) => {
              setSelectedCompany(co);
              setPanel("company-detail");
            }}
          />
        ) : panel === "company-edit" && selectedCompany ? (
          <CompanyForm
            mode="edit"
            company={selectedCompany}
            onClose={() => setPanel("company-detail")}
            onSuccess={(co) => {
              setSelectedCompany(co);
              setPanel("company-detail");
            }}
          />
        ) : panel === "company-subgraphs" && selectedCompany ? (
          <div className="flex h-full flex-col">
            <div className="flex items-center justify-between border-b border-slate-800 px-4 py-3">
              <h3 className="truncate pr-2 text-sm font-semibold text-slate-100">
                {selectedCompany.name_zh} — 子图版本
              </h3>
              <button
                onClick={() => setPanel("none")}
                className="flex h-7 w-7 items-center justify-center rounded text-slate-400 hover:bg-slate-800 hover:text-slate-200"
              >
                <X className="h-3.5 w-3.5" />
              </button>
            </div>
            <div className="flex-1 overflow-y-auto p-4">
              <CompanySubgraphPanel
                companyId={selectedCompany.company_id}
                onLoadSubgraph={handleLoadSubgraph}
              />
            </div>
          </div>
        ) : panel === "node-companies" && contextMenu.node ? (
          <NodeCompaniesPanel
            nodeId={contextMenu.node.node_id}
            nodeName={contextMenu.node.canonical_name_zh}
            onClose={() => setPanel("none")}
            onSelectCompany={(company) => {
              setSelectedCompany(company);
              setPanel("company-detail");
            }}
          />
        ) : panel === "node-industries" && contextMenu.node ? (
          <NodeIndustriesPanel
            nodeId={contextMenu.node.node_id}
            nodeName={contextMenu.node.canonical_name_zh}
            onClose={() => setPanel("none")}
            onSelectIndustry={(industry) => {
              setSelectedIndustry(industry);
              setPanel("industry-detail");
            }}
          />
        ) : null
      }
    />
    {contextMenu.visible && contextMenu.node && (
      <NodeContextMenu
        x={contextMenu.x}
        y={contextMenu.y}
        nodeName={contextMenu.node.canonical_name_zh}
        onShowCompanies={() => {
          setPanel("node-companies");
          setContextMenu((prev) => ({ ...prev, visible: false }));
        }}
        onShowIndustries={() => {
          setPanel("node-industries");
          setContextMenu((prev) => ({ ...prev, visible: false }));
        }}
        onClose={() => setContextMenu((prev) => ({ ...prev, visible: false }))}
      />
    )}
  </>
  );
}
