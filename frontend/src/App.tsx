import { useRef, useState } from "react";
import { StatsBar, MainView } from "@/components/StatsBar";
import { DbChecksPage } from "@/pages/DbChecksPage";
import { Layout } from "@/components/Layout";
import { GraphCanvas, GraphCanvasRef } from "@/components/GraphCanvas";
import { GraphToolbar } from "@/components/GraphToolbar";
import { NodeContextMenu } from "@/components/NodeContextMenu";
import { CompanyGraphEmptyState } from "@/components/CompanyGraphEmptyState";
import { CompanyNetworkCanvas } from "@/components/CompanyNetworkCanvas";
import { ExplorationCanvas } from "@/components/ExplorationCanvas";
import { CompanyMaterialModal } from "@/components/CompanyMaterialModal";
import { MaterialConnectionPanel } from "@/components/MaterialConnectionPanel";
import { CanvasContextMenu } from "@/components/CanvasContextMenu";
import { EdgeContextMenu } from "@/components/EdgeContextMenu";
import { ConnectEdgePanel } from "@/components/ConnectEdgePanel";
import { QuickNodeForm } from "@/components/QuickNodeForm";
import { deleteEdge } from "@/services/api";
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
  const graphCanvasRef = useRef<GraphCanvasRef>(null);
  const [quickNodeAt, setQuickNodeAt] = useState<{
    node: { x: number; y: number };
    visible: boolean;
  } | null>(null);

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

  const industrialRightPanel =
    industrial.panel !== "none" ? (
      <RightPanel
        panel={industrial.panel}
        selectedNode={industrial.selectedNode}
        selectedEdge={industrial.selectedEdge}
        selectedIndustry={industrial.selectedIndustry}
        selectedCompany={industrial.selectedCompany}
        selectedRelation={null}
        contextMenuNode={industrial.contextMenuNode}
        refreshGraph={industrial.refreshGraph}
        onNodeCreated={(node, position) => {
          if (position) {
            graphCanvasRef.current?.addNode(node, position);
            industrial.setPendingNodePosition(null);
          }
        }}
        pendingNodePosition={industrial.pendingNodePosition}
        edgePrefillData={industrial.pendingEdgePrefill}
        clearPendingEdgePrefill={industrial.clearPendingEdgePrefill}
        setPanel={industrial.setPanel}
        onPushPanel={industrial.pushPanel}
        onBackPanel={industrial.popPanel}
        setSelectedNode={industrial.setSelectedNode}
        setSelectedEdge={industrial.setSelectedEdge}
        setSelectedIndustry={industrial.setSelectedIndustry}
        setSelectedCompany={industrial.setSelectedCompany}
        onLoadSubgraph={industrial.handleLoadSubgraph}
        onHighlightNodes={industrial.handleHighlightNodes}
        onSelectNode={industrial.handleNodeClick}
        onSelectCompany={industrial.handleSelectCompanyDetail}
        onSelectIndustry={industrial.handleSelectIndustryDetail}
        isProcessExpanded={
          industrial.selectedNode
            ? industrial.isProcessParentExpanded(industrial.selectedNode.node_id)
            : false
        }
        onToggleProcessExpansion={() => {
          if (industrial.selectedNode) {
            industrial.toggleProcessParent(industrial.selectedNode.node_id);
          }
        }}
      />
    ) : null;

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
          onCreateIndustry={() => industrial.pushPanel({ panel: "industry-create" })}
          onCreateCompany={() => industrial.pushPanel({ panel: "company-create" })}
          onChangeFilters={industrial.setActiveFilters}
        />
      }
      centerCanvas={
        <div className="relative h-full w-full">
          <GraphCanvas
            ref={graphCanvasRef}
            key={industrial.graphKey}
            onNodeClick={industrial.handleNodeClick}
            onEdgeClick={industrial.handleEdgeClick}
            onNodeContextMenu={industrial.handleNodeContextMenu}
            onEdgeContextMenu={industrial.handleEdgeContextMenu}
            onCanvasContextMenu={industrial.handleCanvasContextMenu}
            onEdgeDelete={(edge) => {
              deleteEdge(edge.edge_id).then(() => {
                graphCanvasRef.current?.removeEdge(edge.edge_id);
                if (industrial.selectedEdge?.edge_id === edge.edge_id) {
                  industrial.closePanel();
                }
                industrial.refreshGraph();
              });
            }}
            onConnectSourceSelect={industrial.handleConnectSourceSelect}
            onConnectTargetSelect={industrial.handleConnectTargetSelect}
            filters={industrial.activeFilters}
            highlightNodeId={industrial.selectedNode?.node_id}
            highlightNodeIds={industrial.highlightNodeIds}
            sourceData={industrial.subgraphData}
            editMode={industrial.editMode}
            connectSourceNodeId={industrial.connectSource?.node_id || null}
            expandedProcessParents={industrial.expandedProcessParents}
            onToggleProcessExpansion={industrial.toggleProcessParent}
          />
          <GraphToolbar
            onRelayout={() => industrial.setGraphKey((k) => k + 1)}
            editMode={industrial.editMode}
            onToggleEditMode={industrial.toggleEditMode}
          />
        </div>
      }
      searchPanel={
        <IndustrialSearchPanel
          nav={industrial.nav}
          onNavBack={industrial.handleNavBack}
          onNavForward={industrial.handleNavForward}
          onNavGoto={industrial.handleNavGoto}
          onSelectNode={(node) =>
            industrial.pushPanel({
              panel: "node-detail",
              selectedNode: node,
              selectedEdge: null,
              selectedIndustry: null,
              selectedCompany: null,
            })
          }
          onCreateNode={() => industrial.pushPanel({ panel: "node-create" })}
          onCreateEdge={() => industrial.pushPanel({ panel: "edge-create" })}
          onUploadBatch={() => industrial.pushPanel({ panel: "batch-upload" })}
          hasActiveSelection={
            industrial.selectedIndustries.length > 0 ||
            industrial.selectedCompanies.length > 0
          }
          onResetSelection={industrial.resetSelections}
        />
      }
      rightPanel={industrialRightPanel}
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

  const companyRightPanel =
    company.panel !== "none" ? (
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
        onPushPanel={company.pushPanel}
        onBackPanel={company.popPanel}
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
    ) : null;

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
          onCreateCompany={() => company.pushPanel({ panel: "company-create" })}
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
      rightPanel={companyRightPanel}
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
              industrial.pushPanel({
                panel: "node-companies",
                contextMenuNode: industrial.contextMenu.node,
              });
              industrial.setContextMenu((prev) => ({ ...prev, visible: false }));
            }}
            onShowIndustries={() => {
              industrial.pushPanel({
                panel: "node-industries",
                contextMenuNode: industrial.contextMenu.node,
              });
              industrial.setContextMenu((prev) => ({ ...prev, visible: false }));
            }}
            onClose={() =>
              industrial.setContextMenu((prev) => ({ ...prev, visible: false }))
            }
          />
        )}

      {mainView === "industrial_graph" && industrial.canvasMenu.visible && (
        <CanvasContextMenu
          x={industrial.canvasMenu.x}
          y={industrial.canvasMenu.y}
          onQuickCreate={() => {
            if (industrial.pendingNodePosition) {
              setQuickNodeAt({
                node: industrial.pendingNodePosition,
                visible: true,
              });
            }
            industrial.handleCloseCanvasMenu();
          }}
          onFullCreate={() => {
            industrial.pushPanel({ panel: "node-create" });
            industrial.handleCloseCanvasMenu();
          }}
          onClose={industrial.handleCloseCanvasMenu}
        />
      )}

      {mainView === "industrial_graph" &&
        industrial.edgeMenu.visible &&
        industrial.edgeMenu.edge && (
          <EdgeContextMenu
            x={industrial.edgeMenu.x}
            y={industrial.edgeMenu.y}
            onDelete={() => {
              const edge = industrial.edgeMenu.edge;
              if (edge) {
                deleteEdge(edge.edge_id).then(() => {
                  graphCanvasRef.current?.removeEdge(edge.edge_id);
                  if (industrial.selectedEdge?.edge_id === edge.edge_id) {
                    industrial.closePanel();
                  }
                  industrial.refreshGraph();
                });
              }
              industrial.handleCloseEdgeMenu();
            }}
            onClose={industrial.handleCloseEdgeMenu}
          />
        )}

      {mainView === "industrial_graph" &&
        industrial.editMode === "connect" &&
        industrial.connectSource &&
        industrial.connectTarget && (
          <ConnectEdgePanel
            source={industrial.connectSource}
            target={industrial.connectTarget}
            x={industrial.connectFormPosition?.x ?? industrial.canvasMenu.x}
            y={industrial.connectFormPosition?.y ?? industrial.canvasMenu.y}
            onSuccess={(edge) => {
              graphCanvasRef.current?.addEdge(edge);
              industrial.exitEditMode();
            }}
            onClose={() => {
              industrial.handleCancelConnect();
            }}
            onExpand={(draft) => {
              industrial.handleOpenFullEdgeCreate(draft);
              industrial.handleCancelConnect();
            }}
          />
        )}

      {mainView === "industrial_graph" && quickNodeAt?.visible && (
        <div
          className="fixed z-50 w-80 rounded-lg border border-slate-700 bg-slate-900/95 p-3 shadow-xl backdrop-blur"
          style={{ left: quickNodeAt.node.x, top: quickNodeAt.node.y }}
        >
          <QuickNodeForm
            onCancel={() => setQuickNodeAt(null)}
            onSuccess={(node) => {
              graphCanvasRef.current?.addNode(node, quickNodeAt.node);
              setQuickNodeAt(null);
            }}
          />
        </div>
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
