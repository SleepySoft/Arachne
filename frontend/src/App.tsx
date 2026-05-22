import { useCallback, useState } from "react";
import { GraphEdge, IndustrialNode, Industry, Company } from "@/types";
import { BatchUploader } from "@/components/BatchUploader";
import { CompanyDetail } from "@/components/CompanyDetail";
import { CompanyForm } from "@/components/CompanyForm";
import { CompanySidebar } from "@/components/CompanySidebar";
import { EdgeDetail } from "@/components/EdgeDetail";
import { EdgeForm } from "@/components/EdgeForm";
import { FilterPanel } from "@/components/FilterPanel";
import { GraphCanvas } from "@/components/GraphCanvas";
import { IndustryDetail } from "@/components/IndustryDetail";
import { IndustryForm } from "@/components/IndustryForm";
import { IndustrySidebar } from "@/components/IndustrySidebar";
import { Layout } from "@/components/Layout";
import { NodeDetail } from "@/components/NodeDetail";
import { NodeForm } from "@/components/NodeForm";
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
  | "company-edit";

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

  const handleNodeClick = useCallback((node: IndustrialNode) => {
    setSelectedNode(node);
    setSelectedEdge(null);
    setPanel("node-detail");
  }, []);

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
    if (mode === "graph") {
      setSubgraphData(undefined);
    }
  };

  const handleSelectIndustry = (industry: Industry) => {
    setSelectedIndustry(industry);
    setPanel("industry-detail");
  };

  const handleSelectCompany = (company: Company) => {
    setSelectedCompany(company);
    setPanel("company-detail");
  };

  const handleLoadSubgraph = (nodes: unknown[], edges: unknown[]) => {
    setSubgraphData({
      nodes: nodes as IndustrialNode[],
      edges: edges as GraphEdge[],
    });
    setGraphKey((k) => k + 1);
  };

  return (
    <Layout
      topBar={<StatsBar viewMode={viewMode} onChangeView={handleViewChange} />}
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
        <GraphCanvas
          key={graphKey}
          onNodeClick={handleNodeClick}
          onEdgeClick={handleEdgeClick}
          filters={activeFilters}
          highlightNodeId={selectedNode?.node_id}
          sourceData={subgraphData}
        />
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
        ) : (
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-500">
              {viewMode === "industries"
                ? "点击左侧行业在图谱中查看其子图"
                : "点击左侧公司在图谱中查看其临时子图"}
            </span>
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
        ) : null
      }
    />
  );
}
