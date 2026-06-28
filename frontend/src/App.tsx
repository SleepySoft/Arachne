import { useCallback, useEffect, useRef, useState } from "react";
import { StatsBar, MainView } from "@/components/StatsBar";
import { DbChecksPage } from "@/pages/DbChecksPage";
import { Layout } from "@/components/Layout";
import { GraphCanvas, GraphCanvasRef } from "@/components/GraphCanvas";
import { CanvasToolbar } from "@/components/toolbar/CanvasToolbar";
import { ViewManagerModal } from "@/components/ViewManagerModal";
import { CompanyNetworkCanvas, CompanyNetworkCanvasRef } from "@/components/CompanyNetworkCanvas";
import { ExplorationCanvas, ExplorationCanvasRef } from "@/components/ExplorationCanvas";
import { NodeContextMenu } from "@/components/NodeContextMenu";
import { MultiNodeContextMenu } from "@/components/MultiNodeContextMenu";
import { CompanyGraphEmptyState } from "@/components/CompanyGraphEmptyState";
import { CompanyMaterialModal } from "@/components/CompanyMaterialModal";
import { MaterialConnectionPanel } from "@/components/MaterialConnectionPanel";
import { CanvasContextMenu } from "@/components/CanvasContextMenu";
import { EdgeContextMenu } from "@/components/EdgeContextMenu";
import { ConnectEdgePanel } from "@/components/ConnectEdgePanel";
import { QuickNodeForm } from "@/components/QuickNodeForm";
import { deleteEdge, listCompanies, listIndustries } from "@/services/api";
import { IndustrialSidebar } from "@/components/panels/IndustrialSidebar";
import { IndustrialSearchPanel } from "@/components/panels/IndustrialSearchPanel";
import { CompanySidebarPanel } from "@/components/panels/CompanySidebarPanel";
import { CompanySearchPanel } from "@/components/panels/CompanySearchPanel";
import { RightPanel } from "@/components/panels/RightPanel";
import { useIndustrialGraph } from "@/hooks/useIndustrialGraph";
import { useCompanyGraph } from "@/hooks/useCompanyGraph";
import { useSavedViews } from "@/hooks/useSavedViews";
import {
  buildIndustrialSnapshot,
  applyIndustrialSnapshot,
  buildCompanySnapshot,
  applyCompanySnapshot,
} from "@/lib/viewSerializer";

export default function App() {
  const [mainView, setMainView] = useState<MainView>("industrial_graph");

  const handleChangeMainView = (view: MainView) => {
    setMainView(view);
  };

  const industrial = useIndustrialGraph();
  const company = useCompanyGraph();
  const graphCanvasRef = useRef<GraphCanvasRef>(null);
  const companyNetworkCanvasRef = useRef<CompanyNetworkCanvasRef>(null);
  const explorationCanvasRef = useRef<ExplorationCanvasRef>(null);

  const [allIndustries, setAllIndustries] = useState<import("@/types").Industry[]>([]);
  const [allCompanies, setAllCompanies] = useState<import("@/types").Company[]>([]);
  const [industrialViewToRestore, setIndustrialViewToRestore] = useState<
    import("@/types/view").IndustrialViewState | null
  >(null);
  const [companyViewToRestore, setCompanyViewToRestore] = useState<
    import("@/types/view").CompanyViewState | null
  >(null);
  const [importMessage, setImportMessage] = useState<string | null>(null);
  const [viewManagerOpen, setViewManagerOpen] = useState(false);
  const [viewManagerWorkspace, setViewManagerWorkspace] = useState<import("@/types/view").WorkspaceType>("industrial");
  const savedViews = useSavedViews();

  useEffect(() => {
    let cancelled = false;
    Promise.all([listIndustries(1, 1000), listCompanies(1, 1000)])
      .then(([industries, companies]) => {
        if (cancelled) return;
        setAllIndustries(industries.items);
        setAllCompanies(companies.items);
      })
      .catch(() => {
        // ignore
      });
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (!importMessage) return;
    const timer = setTimeout(() => setImportMessage(null), 4000);
    return () => clearTimeout(timer);
  }, [importMessage]);

  useEffect(() => {
    if (!industrialViewToRestore) return;
    const timer = setTimeout(() => setIndustrialViewToRestore(null), 3000);
    return () => clearTimeout(timer);
  }, [industrialViewToRestore]);

  useEffect(() => {
    if (!companyViewToRestore) return;
    const timer = setTimeout(() => setCompanyViewToRestore(null), 3000);
    return () => clearTimeout(timer);
  }, [companyViewToRestore]);

  const handleSaveCurrentView = useCallback(() => {
    const name = window.prompt("为当前视图命名：");
    if (!name || !name.trim()) return;
    if (mainView === "industrial_graph") {
      const payload = buildIndustrialSnapshot(
        {
          selectedIndustries: industrial.selectedIndustries,
          selectedCompanies: industrial.selectedCompanies,
          activeFilters: industrial.activeFilters,
          expandedProcessParents: industrial.expandedProcessParents,
          canvasRef: graphCanvasRef,
        },
        name.trim()
      );
      savedViews.saveView(name.trim(), "industrial", payload);
    } else if (mainView === "company_graph") {
      const activeRef =
        company.companyDisplayMode === "local" && company.companyExploreMode === "manual"
          ? explorationCanvasRef
          : companyNetworkCanvasRef;
      const payload = buildCompanySnapshot(
        {
          companyDisplayMode: company.companyDisplayMode,
          companyExploreMode: company.companyExploreMode,
          orderedChain: company.orderedChain,
          fixedIds: company.fixedIds,
          currentFocusId: company.currentFocusId,
          explorationData: company.explorationData,
          canvasRef: activeRef,
        },
        name.trim()
      );
      savedViews.saveView(name.trim(), "company", payload);
    }
  }, [
    mainView,
    industrial.selectedIndustries,
    industrial.selectedCompanies,
    industrial.activeFilters,
    industrial.expandedProcessParents,
    company.companyDisplayMode,
    company.companyExploreMode,
    company.orderedChain,
    company.fixedIds,
    company.currentFocusId,
    company.explorationData,
    savedViews,
  ]);

  const handleOpenViewManager = useCallback(() => {
    setViewManagerWorkspace(mainView === "company_graph" ? "company" : "industrial");
    setViewManagerOpen(true);
  }, [mainView]);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement;
      if (
        target &&
        (target.tagName === "INPUT" || target.tagName === "TEXTAREA" || target.isContentEditable)
      ) {
        return;
      }
      if ((e.ctrlKey || e.metaKey) && !e.altKey) {
        if (e.key === "s" || e.key === "S") {
          e.preventDefault();
          handleSaveCurrentView();
        }
        if (e.key === "o" || e.key === "O") {
          e.preventDefault();
          handleOpenViewManager();
        }
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [handleSaveCurrentView, handleOpenViewManager]);

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
          graphCanvasRef.current?.addNode(node, position);
          industrial.setPendingNodePosition(null);
        }}
        onNodeUpdated={(node) => {
          graphCanvasRef.current?.updateNode(node);
        }}
        onNodeDeleted={(nodeId) => {
          graphCanvasRef.current?.removeNode(nodeId);
          if (industrial.selectedNode?.node_id === nodeId) {
            industrial.closePanel();
          }
        }}
        onEdgeCreated={(edge) => {
          graphCanvasRef.current?.addEdge(edge);
        }}
        onEdgeUpdated={(edge) => {
          graphCanvasRef.current?.updateEdge(edge);
        }}
        onEdgeDeleted={(edgeId) => {
          graphCanvasRef.current?.removeEdge(edgeId);
          if (industrial.selectedEdge?.edge_id === edgeId) {
            industrial.closePanel();
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
            onMultiNodeContextMenu={industrial.handleMultiNodeContextMenu}
            onCanvasContextMenu={industrial.handleCanvasContextMenu}
            onEdgeDelete={(edge) => {
              deleteEdge(edge.edge_id).then(() => {
                graphCanvasRef.current?.removeEdge(edge.edge_id);
                if (industrial.selectedEdge?.edge_id === edge.edge_id) {
                  industrial.closePanel();
                }
              });
            }}
            onClearSelection={industrial.handleClearSelection}
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
            wheelSensitivity={industrial.wheelSensitivity}
            restoredPositions={industrialViewToRestore?.nodePositions}
            restoredCamera={industrialViewToRestore?.camera}
          />
          <CanvasToolbar
            workspace="industrial"
            savedViews={savedViews}
            onSaveView={(name) =>
              buildIndustrialSnapshot(
                {
                  selectedIndustries: industrial.selectedIndustries,
                  selectedCompanies: industrial.selectedCompanies,
                  activeFilters: industrial.activeFilters,
                  expandedProcessParents: industrial.expandedProcessParents,
                  canvasRef: graphCanvasRef,
                },
                name
              )
            }
            onLoadView={(view) => {
              const result = applyIndustrialSnapshot(view, {
                setSelectedIndustries: industrial.setSelectedIndustries,
                setSelectedCompanies: industrial.setSelectedCompanies,
                setActiveFilters: industrial.setActiveFilters,
                setExpandedProcessParents: industrial.setExpandedProcessParents,
                setGraphKey: industrial.setGraphKey,
                setSubgraphData: industrial.setSubgraphData,
                setHighlightNodeIds: industrial.setHighlightNodeIds,
                allIndustries,
                allCompanies,
                onSetRestored: setIndustrialViewToRestore,
              });
              if (result.missingIndustryIds.length > 0 || result.missingCompanyIds.length > 0) {
                setImportMessage(
                  `已恢复视图。缺失 ${result.missingIndustryIds.length} 个行业、${result.missingCompanyIds.length} 个公司。`
                );
              }
            }}
            onManageViews={() => {
              setViewManagerWorkspace("industrial");
              setViewManagerOpen(true);
            }}
            zoomSensitivity={industrial.wheelSensitivity}
            onZoomSensitivityChange={industrial.setWheelSensitivity}
          />
        </div>
      }
      searchPanel={
        <IndustrialSearchPanel
          nav={industrial.nav}
          onNavBack={industrial.handleNavBack}
          onNavForward={industrial.handleNavForward}
          onNavGoto={industrial.handleNavGoto}
          onSelectNode={industrial.openNodeDetail}
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
          ref={explorationCanvasRef}
          nodes={company.explorationData?.nodes ?? []}
          edges={company.explorationData?.edges ?? []}
          onNodeClick={company.handleExplorationNodeClick}
          onEdgeClick={(edge) => company.setSelectedExplorationEdge(edge)}
          highlightNodeId={company.currentFocusId}
          restoredCamera={companyViewToRestore?.camera}
        />
      ) : (
        <CompanyNetworkCanvas
          ref={companyNetworkCanvasRef}
          nodes={company.allCompanyNodes}
          edges={company.allCompanyEdges}
          highlightCompanyId={company.currentFocusId}
          previewNodeIds={company.previewNodeIds}
          onNodeClick={company.handleCompanyNodeClick}
          onNodeDblClick={company.handleCompanyNodeDblClick}
          onEdgeClick={company.handleCompanyEdgeClick}
          restoredCamera={companyViewToRestore?.camera}
        />
      )
    ) : company.companyDisplayMode === "global" && company.companyNetworkData ? (
      <CompanyNetworkCanvas
        ref={companyNetworkCanvasRef}
        nodes={company.companyNetworkData.nodes}
        edges={company.companyNetworkData.edges}
        highlightCompanyId={company.currentFocusId}
        dimUnrelated={!!company.currentFocusId}
        onNodeClick={company.handleCompanyNodeClick}
        onNodeDblClick={company.handleCompanyNodeDblClick}
        onEdgeClick={company.handleCompanyEdgeClick}
        restoredCamera={companyViewToRestore?.camera}
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

  const activeCompanyCanvasRef =
    company.companyDisplayMode === "local" && company.companyExploreMode === "manual"
      ? explorationCanvasRef
      : companyNetworkCanvasRef;

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
      centerCanvas={
        <div className="relative h-full w-full">
          {companyCenterCanvas}
          <CanvasToolbar
            workspace="company"
            savedViews={savedViews}
            onSaveView={(name) =>
              buildCompanySnapshot(
                {
                  companyDisplayMode: company.companyDisplayMode,
                  companyExploreMode: company.companyExploreMode,
                  orderedChain: company.orderedChain,
                  fixedIds: company.fixedIds,
                  currentFocusId: company.currentFocusId,
                  explorationData: company.explorationData,
                  canvasRef: activeCompanyCanvasRef,
                },
                name
              )
            }
            onLoadView={(view) => {
              applyCompanySnapshot(view, {
                setCompanyDisplayMode: company.setCompanyDisplayMode,
                setCompanyExploreMode: company.setCompanyExploreMode,
                setOrderedChain: company.setOrderedChain,
                setFixedIds: company.setFixedIds,
                setCurrentFocusId: company.setCurrentFocusId,
                setExplorationData: company.setExplorationData,
                setPreviewData: company.setPreviewData,
                onSetRestored: setCompanyViewToRestore,
              });
            }}
            onManageViews={() => {
              setViewManagerWorkspace("company");
              setViewManagerOpen(true);
            }}
          />
        </div>
      }
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
            onShowUpstream={() => {
              const node = industrial.contextMenu.node;
              if (node) graphCanvasRef.current?.showNeighbors(node.node_id, "upstream");
              industrial.setContextMenu((prev) => ({ ...prev, visible: false }));
            }}
            onShowDownstream={() => {
              const node = industrial.contextMenu.node;
              if (node) graphCanvasRef.current?.showNeighbors(node.node_id, "downstream");
              industrial.setContextMenu((prev) => ({ ...prev, visible: false }));
            }}
            onHighlightUpstream={() => {
              const node = industrial.contextMenu.node;
              if (node) graphCanvasRef.current?.highlightNeighbors(node.node_id, "upstream");
              industrial.setContextMenu((prev) => ({ ...prev, visible: false }));
            }}
            onHighlightDownstream={() => {
              const node = industrial.contextMenu.node;
              if (node) graphCanvasRef.current?.highlightNeighbors(node.node_id, "downstream");
              industrial.setContextMenu((prev) => ({ ...prev, visible: false }));
            }}
            onPullUpstream={() => {
              const node = industrial.contextMenu.node;
              if (node) graphCanvasRef.current?.pullNeighborsIntoView(node.node_id, "upstream");
              industrial.setContextMenu((prev) => ({ ...prev, visible: false }));
            }}
            onPullDownstream={() => {
              const node = industrial.contextMenu.node;
              if (node) graphCanvasRef.current?.pullNeighborsIntoView(node.node_id, "downstream");
              industrial.setContextMenu((prev) => ({ ...prev, visible: false }));
            }}
            isGroup={
              industrial.contextMenu.node
                ? graphCanvasRef.current?.isCompoundGroupNode(
                    industrial.contextMenu.node.node_id
                  ) ?? false
                : false
            }
            isExpanded={
              industrial.contextMenu.node
                ? industrial.isProcessParentExpanded(
                    industrial.contextMenu.node.node_id
                  )
                : false
            }
            onToggleGroup={() => {
              const node = industrial.contextMenu.node;
              if (node) {
                industrial.toggleProcessParent(node.node_id);
              }
              industrial.setContextMenu((prev) => ({ ...prev, visible: false }));
            }}
            onClose={() =>
              industrial.setContextMenu((prev) => ({ ...prev, visible: false }))
            }
          />
        )}

      {mainView === "industrial_graph" &&
        industrial.multiNodeContextMenu.visible &&
        industrial.multiNodeContextMenu.nodes.length > 0 && (
          <MultiNodeContextMenu
            x={industrial.multiNodeContextMenu.x}
            y={industrial.multiNodeContextMenu.y}
            selectedCount={industrial.multiNodeContextMenu.nodes.length}
            onAutoArrange={() => {
              graphCanvasRef.current?.autoArrangeSelectedNodes();
              industrial.handleCloseMultiNodeContextMenu();
            }}
            onClearSelection={() => {
              graphCanvasRef.current?.clearNodeSelection();
            }}
            onClose={industrial.handleCloseMultiNodeContextMenu}
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
                });
              }
              industrial.handleCloseEdgeMenu();
            }}
            onPull={() => {
              const edge = industrial.edgeMenu.edge;
              if (edge) {
                graphCanvasRef.current?.pullEdgeEndpointsIntoView(edge.edge_id);
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

      {viewManagerOpen && (
        <ViewManagerModal
          workspace={viewManagerWorkspace}
          savedViews={savedViews}
          onLoad={(view) => {
            if (viewManagerWorkspace === "industrial") {
              const result = applyIndustrialSnapshot(view, {
                setSelectedIndustries: industrial.setSelectedIndustries,
                setSelectedCompanies: industrial.setSelectedCompanies,
                setActiveFilters: industrial.setActiveFilters,
                setExpandedProcessParents: industrial.setExpandedProcessParents,
                setGraphKey: industrial.setGraphKey,
                setSubgraphData: industrial.setSubgraphData,
                setHighlightNodeIds: industrial.setHighlightNodeIds,
                allIndustries,
                allCompanies,
                onSetRestored: setIndustrialViewToRestore,
              });
              if (result.missingIndustryIds.length > 0 || result.missingCompanyIds.length > 0) {
                setImportMessage(
                  `已恢复视图。缺失 ${result.missingIndustryIds.length} 个行业、${result.missingCompanyIds.length} 个公司。`
                );
              }
            } else {
              applyCompanySnapshot(view, {
                setCompanyDisplayMode: company.setCompanyDisplayMode,
                setCompanyExploreMode: company.setCompanyExploreMode,
                setOrderedChain: company.setOrderedChain,
                setFixedIds: company.setFixedIds,
                setCurrentFocusId: company.setCurrentFocusId,
                setExplorationData: company.setExplorationData,
                setPreviewData: company.setPreviewData,
                onSetRestored: setCompanyViewToRestore,
              });
            }
            setViewManagerOpen(false);
          }}
          onClose={() => setViewManagerOpen(false)}
        />
      )}

      {importMessage && (
        <div className="fixed bottom-4 left-1/2 z-50 -translate-x-1/2 rounded-lg border border-slate-700 bg-slate-900/95 px-4 py-2 text-xs text-slate-200 shadow-xl backdrop-blur">
          {importMessage}
        </div>
      )}
    </>
  );
}
