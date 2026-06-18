import { useState } from "react";
import { StatsBar, MainView } from "@/components/StatsBar";
import { DbChecksPage } from "@/pages/DbChecksPage";
import { Layout } from "@/components/Layout";
import { GraphCanvas } from "@/components/GraphCanvas";
import { GraphToolbar } from "@/components/GraphToolbar";
import { NodeContextMenu } from "@/components/NodeContextMenu";
import { CompanyGraphEmptyState } from "@/components/CompanyGraphEmptyState";
import { CompanyNetworkCanvas } from "@/components/CompanyNetworkCanvas";
import { ExplorationCanvas } from "@/components/ExplorationCanvas";
import { CompanyMaterialModal } from "@/components/CompanyMaterialModal";
import { MaterialConnectionPanel } from "@/components/MaterialConnectionPanel";
import { IndustrialSidebar } from "@/components/panels/IndustrialSidebar";
import { IndustrialSearchPanel } from "@/components/panels/IndustrialSearchPanel";
import { CompanySidebarPanel } from "@/components/panels/CompanySidebarPanel";
import { CompanySearchPanel } from "@/components/panels/CompanySearchPanel";
import { RightPanel } from "@/components/panels/RightPanel";
import { useIndustrialGraph } from "@/hooks/useIndustrialGraph";
import { useCompanyGraph } from "@/hooks/useCompanyGraph";

export default function App() {
  const [mainView, setMainView] = useState<MainView>("industrial_graph");

  const handleChangeMainView = (view: MainView) => {
    setMainView(view);
  };

  const industrial = useIndustrialGraph();
  const company = useCompanyGraph();

  if (mainView === "db_checks") {
    return (
      <div className="flex h-screen w-full flex-col bg-slate-950">
        <div className="h-14 shrink-0 border-b border-slate-800 bg-slate-900">
          <StatsBar mainView={mainView} onChangeMainView={handleChangeMainView} />
        </div>
        <div className="flex-1 overflow-hidden">
          <DbChecksPage />
        </div>
      </div>
    );
  }

  const industrialWorkspace = (
    <Layout
      topBar={
        <StatsBar mainView={mainView} onChangeMainView={handleChangeMainView} />
      }
      leftSidebar={
        <IndustrialSidebar
          selectedIndustries={industrial.selectedIndustries}
          selectedCompanies={industrial.selectedCompanies}
          activeFilters={industrial.activeFilters}
          onToggleIndustry={industrial.handleToggleIndustry}
          onSelectIndustry={industrial.handleSelectIndustryDetail}
          onToggleCompany={industrial.handleToggleCompany}
          onSelectCompany={industrial.handleSelectCompanyDetail}
          onCreateIndustry={() => industrial.setPanel("industry-create")}
          onCreateCompany={() => industrial.setPanel("company-create")}
          onChangeFilters={industrial.setActiveFilters}
        />
      }
      centerCanvas={
        <div className="relative h-full w-full">
          <GraphCanvas
            key={industrial.graphKey}
            onNodeClick={industrial.handleNodeClick}
            onEdgeClick={industrial.handleEdgeClick}
            onNodeContextMenu={industrial.handleNodeContextMenu}
            filters={industrial.activeFilters}
            highlightNodeId={industrial.selectedNode?.node_id}
            highlightNodeIds={industrial.highlightNodeIds}
            sourceData={industrial.subgraphData}
          />
          <GraphToolbar onRelayout={() => industrial.setGraphKey((k) => k + 1)} />
        </div>
      }
      searchPanel={
        <IndustrialSearchPanel
          nav={industrial.nav}
          onNavBack={industrial.handleNavBack}
          onNavForward={industrial.handleNavForward}
          onNavGoto={industrial.handleNavGoto}
          onSelectNode={(node) => {
            industrial.setSelectedNode(node);
            industrial.setPanel("node-detail");
          }}
          onCreateNode={() => industrial.setPanel("node-create")}
          onCreateEdge={() => industrial.setPanel("edge-create")}
          onUploadBatch={() => industrial.setPanel("batch-upload")}
          hasActiveSelection={
            industrial.selectedIndustries.length > 0 ||
            industrial.selectedCompanies.length > 0
          }
          onResetSelection={industrial.resetSelections}
        />
      }
      rightPanel={
        <RightPanel
          panel={industrial.panel}
          selectedNode={industrial.selectedNode}
          selectedEdge={industrial.selectedEdge}
          selectedIndustry={industrial.selectedIndustry}
          selectedCompany={industrial.selectedCompany}
          selectedRelation={null}
          contextMenuNode={industrial.contextMenu.node}
          refreshGraph={industrial.refreshGraph}
          setPanel={industrial.setPanel}
          setSelectedNode={industrial.setSelectedNode}
          setSelectedEdge={industrial.setSelectedEdge}
          setSelectedIndustry={industrial.setSelectedIndustry}
          setSelectedCompany={industrial.setSelectedCompany}
          onLoadSubgraph={industrial.handleLoadSubgraph}
          onHighlightNodes={industrial.handleHighlightNodes}
          onSelectNode={industrial.handleNodeClick}
          onSelectCompany={industrial.handleSelectCompanyDetail}
          onSelectIndustry={industrial.handleSelectIndustryDetail}
        />
      }
    />
  );

  const companyCenterCanvas =
    company.companyDisplayMode === "empty" ? (
      <CompanyGraphEmptyState
        companyCount={company.companyNetworkData?.nodes.length ?? 200}
        relationCount={company.companyNetworkData?.edges.length ?? 1142}
        onDrawGlobal={() => {
          alert("全局公司网络视图已移除。请使用探索接口。");
        }}
        isLoading={company.isDrawingGlobal}
      />
    ) : company.companyDisplayMode === "local" ? (
      company.companyExploreMode === "manual" ? (
        <ExplorationCanvas
          nodes={company.explorationData?.nodes ?? []}
          edges={company.explorationData?.edges ?? []}
          onNodeClick={company.handleExplorationNodeClick}
          onEdgeClick={(edge) => company.setSelectedExplorationEdge(edge)}
          highlightNodeId={company.currentFocusId}
        />
      ) : (
        <CompanyNetworkCanvas
          nodes={company.allCompanyNodes}
          edges={company.allCompanyEdges}
          highlightCompanyId={company.currentFocusId}
          previewNodeIds={company.previewNodeIds}
          onNodeClick={company.handleCompanyNodeClick}
          onNodeDblClick={company.handleCompanyNodeDblClick}
          onEdgeClick={company.handleCompanyEdgeClick}
        />
      )
    ) : company.companyDisplayMode === "global" && company.companyNetworkData ? (
      <CompanyNetworkCanvas
        nodes={company.companyNetworkData.nodes}
        edges={company.companyNetworkData.edges}
        highlightCompanyId={company.currentFocusId}
        dimUnrelated={!!company.currentFocusId}
        onNodeClick={company.handleCompanyNodeClick}
        onNodeDblClick={company.handleCompanyNodeDblClick}
        onEdgeClick={company.handleCompanyEdgeClick}
      />
    ) : (
      <div className="flex h-full w-full items-center justify-center bg-slate-950">
        <div className="text-sm text-slate-500">加载中...</div>
      </div>
    );

  const companyWorkspace = (
    <Layout
      topBar={
        <StatsBar mainView={mainView} onChangeMainView={handleChangeMainView} />
      }
      leftSidebar={
        <CompanySidebarPanel
          selectedId={company.selectedCompany?.company_id}
          companySubView="company_list"
          setCompanySubView={() => {}}
          onSelectCompany={company.handleSelectCompany}
          onCreateCompany={() => company.setPanel("company-create")}
        />
      }
      centerCanvas={companyCenterCanvas}
      searchPanel={
        <CompanySearchPanel
          companyExploreMode={company.companyExploreMode}
          setCompanyExploreMode={company.setCompanyExploreMode}
          companyDisplayMode={company.companyDisplayMode}
          orderedChain={company.orderedChain}
          fixedIds={company.fixedIds}
          nodeStore={company.nodeStore}
          currentFocusId={company.currentFocusId}
          previewData={company.previewData}
          selectedExplorationEdge={company.selectedExplorationEdge}
          onClear={company.clearView}
        />
      }
      rightPanel={
        <RightPanel
          panel={company.panel}
          selectedNode={null}
          selectedEdge={null}
          selectedIndustry={null}
          selectedCompany={company.selectedCompany}
          selectedRelation={company.selectedRelation}
          contextMenuNode={null}
          refreshGraph={() => {}}
          setPanel={company.setPanel}
          setSelectedNode={() => {}}
          setSelectedEdge={() => {}}
          setSelectedIndustry={() => {}}
          setSelectedCompany={company.setSelectedCompany}
          onLoadSubgraph={() => {}}
          onHighlightNodes={() => {}}
          onSelectNode={() => {}}
          onSelectCompany={() => {}}
          onSelectIndustry={() => {}}
          onFocusInGraph={(id) => company.setCurrentFocusId(id)}
          onOpenMaterialModal={() => company.setMaterialModalOpen(true)}
        />
      }
    />
  );

  return (
    <>
      {mainView === "company_graph" ? companyWorkspace : industrialWorkspace}

      {mainView === "industrial_graph" &&
        industrial.contextMenu.visible &&
        industrial.contextMenu.node && (
          <NodeContextMenu
            x={industrial.contextMenu.x}
            y={industrial.contextMenu.y}
            nodeName={industrial.contextMenu.node.canonical_name_zh}
            onShowCompanies={() => {
              industrial.setPanel("node-companies");
              industrial.setContextMenu((prev) => ({ ...prev, visible: false }));
            }}
            onShowIndustries={() => {
              industrial.setPanel("node-industries");
              industrial.setContextMenu((prev) => ({ ...prev, visible: false }));
            }}
            onClose={() =>
              industrial.setContextMenu((prev) => ({ ...prev, visible: false }))
            }
          />
        )}

      {mainView === "company_graph" &&
        company.selectedCompany &&
        company.materialModalOpen && (
          <CompanyMaterialModal
            companyId={company.selectedCompany.company_id}
            companyName={company.selectedCompany.name_zh}
            isOpen={company.materialModalOpen}
            onClose={() => company.setMaterialModalOpen(false)}
            onAddToView={(nodes, edges) => {
              company.handleAddToViewFromModal(nodes, edges);
              const selectedCompany = company.selectedCompany;
              if (!selectedCompany) return;
              company.setNodeStore((prev) => {
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
              company.setCurrentFocusId(selectedCompany.company_id);
            }}
          />
        )}

      {mainView === "company_graph" &&
        company.materialPanelOpen &&
        company.selectedMaterialNode &&
        company.selectedCompany && (
          <MaterialConnectionPanel
            nodeId={company.selectedMaterialNode.id}
            nodeName={company.selectedMaterialNode.name}
            anchorCompanyId={company.selectedCompany.company_id}
            isOpen={company.materialPanelOpen}
            onClose={() => company.setMaterialPanelOpen(false)}
            onAddCompanies={company.handleAddCompaniesToExploration}
          />
        )}
    </>
  );
}
