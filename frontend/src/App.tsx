import { useCallback, useEffect, useRef, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { StatsBar, MainView, GraphEngine } from "@/components/StatsBar";
import { DbChecksPage } from "@/pages/DbChecksPage";
import { FlowEditorPage } from "@/pages/FlowEditorPage";
import { FlowEditorPanel } from "@/components/FlowEditorPanel";
import { ReasoningPage } from "@/pages/ReasoningPage";
import { Layout } from "@/components/Layout";
import { GraphCanvas, GraphCanvasRef } from "@/components/GraphCanvas";
import { CanvasToolbar } from "@/components/toolbar/CanvasToolbar";
import { FocusControlPanel } from "@/components/FocusControlPanel";
import { HideControlPanel } from "@/components/HideControlPanel";
import { ViewManagerModal } from "@/components/ViewManagerModal";
import { CompanyNetworkCanvas, CompanyNetworkCanvasRef } from "@/components/CompanyNetworkCanvas";
import { ExplorationCanvas, ExplorationCanvasRef } from "@/components/ExplorationCanvas";
import { NodeContextMenu } from "@/components/NodeContextMenu";
import { MultiNodeContextMenu } from "@/components/MultiNodeContextMenu";
import { CompanyFilterPanel } from "@/components/CompanyFilterPanel";
import { CompanyGraphEmptyState } from "@/components/CompanyGraphEmptyState";
import { CompanyMaterialModal } from "@/components/CompanyMaterialModal";
import { MaterialConnectionPanel } from "@/components/MaterialConnectionPanel";
import { CanvasContextMenu } from "@/components/CanvasContextMenu";
import { EdgeContextMenu } from "@/components/EdgeContextMenu";
import { ConnectEdgePanel } from "@/components/ConnectEdgePanel";
import { QuickNodeForm } from "@/components/QuickNodeForm";
import { deleteEdge, listCompanies, listEngines, listIndustries, listProvStatementsByNode } from "@/services/api";
import type { EngineInfo } from "@/types";
import { IndustrialSidebar } from "@/components/panels/IndustrialSidebar";
import { FlowSidebarPanel } from "@/components/panels/FlowSidebarPanel";
import { IndustrialSearchPanel } from "@/components/panels/IndustrialSearchPanel";
import { CompanySidebarPanel } from "@/components/panels/CompanySidebarPanel";
import { CompanySearchPanel } from "@/components/panels/CompanySearchPanel";
import { RightPanel } from "@/components/panels/RightPanel";
import { useIndustrialGraph } from "@/hooks/useIndustrialGraph";
import { useCompanyGraph } from "@/hooks/useCompanyGraph";
import { useSavedViews } from "@/hooks/useSavedViews";
import { useViewStateHistory } from "@/hooks/useViewStateHistory";
import {
  buildIndustrialSnapshot,
  applyIndustrialSnapshot,
  buildCompanySnapshot,
  applyCompanySnapshot,
  GraphCameraController,
} from "@/lib/viewSerializer";
import { IndustrialViewState, CompanyViewState, SavedView } from "@/types/view";

function getInitialMainView(): MainView {
  const params = new URLSearchParams(window.location.search);
  const view = params.get("view");
  const valid: MainView[] = [
    "industrial_graph",
    "company_graph",
    "db_checks",
    "reasoning",
    "flow_editor",
  ];
  return valid.includes(view as MainView) ? (view as MainView) : "industrial_graph";
}

function getInitialEngine(): GraphEngine {
  const params = new URLSearchParams(window.location.search);
  return params.get("engine") || "legacy";
}

export default function App() {
  const [mainView, setMainView] = useState<MainView>(getInitialMainView);
  const [graphEngine, setGraphEngine] = useState<GraphEngine>(getInitialEngine);

  const { data: enginesData } = useQuery({
    queryKey: ["engines"],
    queryFn: listEngines,
    staleTime: 60000,
  });

  const engineList = enginesData?.engines ?? [];
  const defaultEngine = enginesData?.default ?? "legacy";

  // Sync the initial engine to the backend-reported default once it loads,
  // but do not override an explicit ?engine= URL parameter.
  useEffect(() => {
    if (!enginesData) return;
    const urlEngine = new URLSearchParams(window.location.search).get("engine");
    if (urlEngine) return;
    setGraphEngine((current) => {
      const exists = engineList.some((e) => e.name === current);
      return exists ? current : defaultEngine;
    });
  }, [enginesData, defaultEngine, engineList]);

  // Persist main view and engine selection to the URL for sharing/refresh.
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    params.set("view", mainView);
    params.set("engine", graphEngine);
    const url = `${window.location.pathname}?${params.toString()}`;
    window.history.replaceState(null, "", url);
  }, [mainView, graphEngine]);

  const getEngineInfo = useCallback(
    (name: string): EngineInfo | undefined => engineList.find((e) => e.name === name),
    [engineList]
  );

  const currentEngineInfo = getEngineInfo(graphEngine);
  const isReadOnlyEngine = currentEngineInfo?.is_read_only ?? false;
  const isFlowEngine = currentEngineInfo?.supports_flows ?? graphEngine === "arachne_flow";

  const industrial = useIndustrialGraph(graphEngine);
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
  const [flowEditorOpen, setFlowEditorOpen] = useState(false);
  const [flowEditorWidth, setFlowEditorWidth] = useState(384);
  const [editorHighlightIds, setEditorHighlightIds] = useState<string[]>([]);
  const [viewManagerOpen, setViewManagerOpen] = useState(false);
  const [viewManagerWorkspace, setViewManagerWorkspace] = useState<import("@/types/view").WorkspaceType>("industrial");
  const [loadedIndustrialView, setLoadedIndustrialView] = useState<import("@/types/view").SavedView | null>(null);
  const [loadedCompanyView, setLoadedCompanyView] = useState<import("@/types/view").SavedView | null>(null);
  const savedViews = useSavedViews();
  const viewHistory = useViewStateHistory();

  const handleChangeMainView = useCallback(
    (view: MainView) => {
      setMainView(view);
      setFlowEditorOpen(false);
      viewHistory.reset(view === "company_graph" ? "company" : "industrial");
    },
    [viewHistory.reset]
  );

  const handleChangeGraphEngine = useCallback(
    (engine: GraphEngine) => {
      if (engine === graphEngine) return;
      setGraphEngine(engine);
      setFlowEditorOpen(false);
      // 主界面保持不变，只切换数据源；选择/过滤/子图重置为该引擎默认状态。
      industrial.switchEngine(engine);
      // 引擎切换后回到图工作区，方便看到新引擎的图。
      setMainView((view) => (view === "company_graph" ? view : "industrial_graph"));
      viewHistory.reset("industrial");
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [graphEngine, industrial.switchEngine, viewHistory.reset]
  );

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
    const timer = setTimeout(() => setIndustrialViewToRestore(null), 15000);
    return () => clearTimeout(timer);
  }, [industrialViewToRestore]);

  useEffect(() => {
    if (!companyViewToRestore) return;
    const timer = setTimeout(() => setCompanyViewToRestore(null), 15000);
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
          focusState: graphCanvasRef.current?.getFocusState() ?? {
            active: false,
            seedNodeIds: [],
            visibleNodeIds: [],
            history: [],
          },
          hideState: industrial.hideState,
          canvasRef: graphCanvasRef,
        },
        name.trim()
      );
      const view = savedViews.saveView(name.trim(), "industrial", payload, loadedIndustrialView ?? undefined);
      setLoadedIndustrialView(view);
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
      const view = savedViews.saveView(name.trim(), "company", payload, loadedCompanyView ?? undefined);
      setLoadedCompanyView(view);
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
    loadedIndustrialView,
    loadedCompanyView,
  ]);

  const getActiveCompanyCanvasRef = useCallback((): React.RefObject<GraphCameraController | null> | undefined => {
    if (mainView !== "company_graph") return undefined;
    return company.companyDisplayMode === "local" && company.companyExploreMode === "manual"
      ? explorationCanvasRef
      : companyNetworkCanvasRef;
  }, [mainView, company.companyDisplayMode, company.companyExploreMode]);

  const captureIndustrialState = useCallback((): IndustrialViewState | undefined => {
    const payload = buildIndustrialSnapshot(
      {
        selectedIndustries: industrial.selectedIndustries,
        selectedCompanies: industrial.selectedCompanies,
        activeFilters: industrial.activeFilters,
        expandedProcessParents: industrial.expandedProcessParents,
        focusState: graphCanvasRef.current?.getFocusState() ?? {
          active: false,
          seedNodeIds: [],
          visibleNodeIds: [],
          history: [],
        },
        hideState: industrial.hideState,
        canvasRef: graphCanvasRef,
      },
      "history"
    );
    return payload.industrial;
  }, [
    industrial.selectedIndustries,
    industrial.selectedCompanies,
    industrial.activeFilters,
    industrial.expandedProcessParents,
    industrial.hideState,
  ]);

  const captureCompanyState = useCallback((): CompanyViewState | undefined => {
    const activeRef = getActiveCompanyCanvasRef();
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
      "history"
    );
    return payload.company;
  }, [
    company.companyDisplayMode,
    company.companyExploreMode,
    company.orderedChain,
    company.fixedIds,
    company.currentFocusId,
    company.explorationData,
    getActiveCompanyCanvasRef,
  ]);

  function scaleCameraAndPositions(
    state: IndustrialViewState | CompanyViewState,
    toSize?: { width: number; height: number }
  ) {
    const fromSize = state.containerSize;
    if (!fromSize || !toSize || fromSize.width <= 0 || fromSize.height <= 0) {
      return { camera: state.camera, nodePositions: state.nodePositions };
    }
    const scaleX = toSize.width / fromSize.width;
    const scaleY = toSize.height / fromSize.height;
    const scale = Math.min(scaleX, scaleY);
    if (!isFinite(scale) || scale <= 0) {
      return { camera: state.camera, nodePositions: state.nodePositions };
    }
    const scaledPositions: import("@/types/view").NodePositions = {};
    if (state.nodePositions) {
      Object.entries(state.nodePositions).forEach(([id, pos]) => {
        scaledPositions[id] = { x: pos.x * scale, y: pos.y * scale };
      });
    }
    return {
      camera: {
        pan: { x: state.camera.pan.x * scale, y: state.camera.pan.y * scale },
        zoom: state.camera.zoom,
      },
      nodePositions: state.nodePositions ? scaledPositions : undefined,
    };
  }

  const handleUndo = useCallback(() => {
    if (mainView === "company_graph") {
      const entry = viewHistory.undo("company");
      if (!entry) return;
      const state = entry.state;
      const activeRef = getActiveCompanyCanvasRef();
      const containerSize = activeRef?.current?.getContainerSize();
      if (entry.layoutOnly) {
        const { nodePositions } = scaleCameraAndPositions(state, containerSize ?? undefined);
        if (nodePositions) {
          activeRef?.current?.setNodePositions(nodePositions);
        }
        return;
      }
      applyCompanySnapshot(
        {
          version: 1,
          id: "undo",
          base: "undo",
          viewVersion: 1,
          name: "undo",
          workspace: "company",
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          company: state,
        } as SavedView,
        {
          setCompanyDisplayMode: company.setCompanyDisplayMode,
          setCompanyExploreMode: company.setCompanyExploreMode,
          setOrderedChain: company.setOrderedChain,
          setFixedIds: company.setFixedIds,
          setCurrentFocusId: company.setCurrentFocusId,
          setExplorationData: company.setExplorationData,
          setPreviewData: company.setPreviewData,
          onSetRestored: setCompanyViewToRestore,
        },
        containerSize ?? undefined
      );
    } else {
      const entry = viewHistory.undo("industrial");
      if (!entry) return;
      const state = entry.state;
      const containerSize = graphCanvasRef.current?.getContainerSize();
      if (entry.layoutOnly) {
        const { nodePositions } = scaleCameraAndPositions(state, containerSize ?? undefined);
        if (nodePositions) {
          graphCanvasRef.current?.setNodePositions(nodePositions);
        }
        return;
      }
      applyIndustrialSnapshot(
        {
          version: 1,
          id: "undo",
          base: "undo",
          viewVersion: 1,
          name: "undo",
          workspace: "industrial",
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          industrial: state,
        } as SavedView,
        {
          setSelectedIndustries: industrial.setSelectedIndustries,
          setSelectedCompanies: industrial.setSelectedCompanies,
          setSelectedFlowIds: industrial.setSelectedFlowIds,
          setActiveFilters: industrial.setActiveFilters,
          setExpandedProcessParents: industrial.setExpandedProcessParents,
          setFocusState: industrial.setFocusState,
          setHideState: industrial.setHideState,
          setGraphKey: industrial.setGraphKey,
          setSubgraphData: industrial.setSubgraphData,
          setHighlightNodeIds: industrial.setHighlightNodeIds,
          allIndustries,
          allCompanies,
          onSetRestored: setIndustrialViewToRestore,
        },
        containerSize ?? undefined
      );
    }
  }, [
    mainView,
    viewHistory,
    captureIndustrialState,
    captureCompanyState,
    industrial.setSelectedIndustries,
    industrial.setSelectedCompanies,
    industrial.setSelectedFlowIds,
    industrial.setActiveFilters,
    industrial.setExpandedProcessParents,
    industrial.setFocusState,
    industrial.setHideState,
    industrial.setGraphKey,
    industrial.setSubgraphData,
    industrial.setHighlightNodeIds,
    allIndustries,
    allCompanies,
    company.setCompanyDisplayMode,
    company.setCompanyExploreMode,
    company.setOrderedChain,
    company.setFixedIds,
    company.setCurrentFocusId,
    company.setExplorationData,
    company.setPreviewData,
    getActiveCompanyCanvasRef,
  ]);

  const pushIndustrialHistory = useCallback(
    (layoutOnly = false) => {
      const state = captureIndustrialState();
      if (state) viewHistory.push("industrial", state, layoutOnly);
    },
    [captureIndustrialState, viewHistory]
  );

  const pushCompanyHistory = useCallback(
    (layoutOnly = false) => {
      const state = captureCompanyState();
      if (state) viewHistory.push("company", state, layoutOnly);
    },
    [captureCompanyState, viewHistory]
  );

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
        if (e.key === "z" || e.key === "Z") {
          e.preventDefault();
          handleUndo();
        }
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [handleSaveCurrentView, handleOpenViewManager, handleUndo]);

  const [quickNodeAt, setQuickNodeAt] = useState<{
    node: { x: number; y: number };
    visible: boolean;
  } | null>(null);

  const industrialRightPanel =
    industrial.panel !== "none" ? (
      <RightPanel
        panel={industrial.panel}
        selectedNode={industrial.selectedNode}
        selectedEdge={industrial.selectedEdge}
        selectedIndustry={industrial.selectedIndustry}
        selectedCompany={industrial.selectedCompany}
        selectedNodes={industrial.selectedNodes}
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
        readOnly={isReadOnlyEngine}
        engine={graphEngine}
      />
    ) : null;

  const industrialWorkspace = (
    <Layout
      leftSidebar={
        isFlowEngine ? (
          <FlowSidebarPanel
            selectedFlowIds={industrial.selectedFlowIds}
            onToggleFlow={(flowId) => {
              viewHistory.reset("industrial");
              industrial.toggleFlowId(flowId);
            }}
            onRecompile={industrial.recompileSelectedFlows}
            recompiling={industrial.recompilingFlows}
            activeFilters={industrial.activeFilters}
            onChangeFilters={(filters) => {
              viewHistory.reset("industrial");
              industrial.setActiveFilters(filters);
            }}
            engine={graphEngine}
            onOpenFlowEditor={() => setFlowEditorOpen(true)}
          />
        ) : (
          <IndustrialSidebar
            selectedIndustries={industrial.selectedIndustries}
            selectedCompanies={industrial.selectedCompanies}
            activeFilters={industrial.activeFilters}
            onToggleIndustry={(industry) => {
              viewHistory.reset("industrial");
              industrial.handleToggleIndustry(industry);
            }}
            onSelectIndustry={industrial.handleSelectIndustryDetail}
            onToggleCompany={(company) => {
              viewHistory.reset("industrial");
              industrial.handleToggleCompany(company);
            }}
            onSelectCompany={industrial.handleSelectCompanyDetail}
            onCreateIndustry={() => industrial.pushPanel({ panel: "industry-create" })}
            onCreateCompany={() => industrial.pushPanel({ panel: "company-create" })}
            onChangeFilters={(filters) => {
              viewHistory.reset("industrial");
              industrial.setActiveFilters(filters);
            }}
          />
        )
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
              if (isReadOnlyEngine) return;
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
            onCancelConnect={industrial.exitEditMode}
            connectTargetNodeId={industrial.connectTarget?.node_id || null}
            filters={industrial.activeFilters}
            highlightNodeId={industrial.selectedNode?.node_id}
            highlightNodeIds={
              flowEditorOpen && editorHighlightIds.length > 0
                ? editorHighlightIds
                : industrial.highlightNodeIds
            }
            sourceData={industrial.subgraphData}
            editMode={industrial.editMode}
            connectSourceNodeId={industrial.connectSource?.node_id || null}
            expandedProcessParents={industrial.expandedProcessParents}
            onToggleProcessExpansion={(nodeId) => {
              industrial.toggleProcessParent(nodeId);
            }}
            wheelSensitivity={industrial.wheelSensitivity}
            restoredPositions={industrialViewToRestore?.nodePositions}
            restoredCamera={industrialViewToRestore?.camera}
            focusState={industrial.focusState}
            onFocusChange={industrial.setFocusState}
            hideState={industrial.hideState}
            onBeforeDragStart={() => pushIndustrialHistory(true)}
            onBeforeManualLayout={() => pushIndustrialHistory(true)}
            engine={graphEngine}
          />
          <FocusControlPanel
            graphCanvasRef={graphCanvasRef}
            focusState={industrial.focusState}
          />
          <HideControlPanel
            hideState={industrial.hideState}
            onClearHide={industrial.clearHideState}
          />
          <CanvasToolbar
            workspace="industrial"
            savedViews={savedViews}
            onSaveView={(name) =>
              buildIndustrialSnapshot(
                {
                  engine: graphEngine,
                  selectedFlowIds: industrial.selectedFlowIds,
                  selectedIndustries: industrial.selectedIndustries,
                  selectedCompanies: industrial.selectedCompanies,
                  activeFilters: industrial.activeFilters,
                  expandedProcessParents: industrial.expandedProcessParents,
                  focusState: graphCanvasRef.current?.getFocusState() ?? {
                    active: false,
                    seedNodeIds: [],
                    visibleNodeIds: [],
                    history: [],
                  },
                  hideState: industrial.hideState,
                  canvasRef: graphCanvasRef,
                },
                name
              )
            }
            onLoadView={(view) => {
              viewHistory.reset("industrial");
              setLoadedIndustrialView(view);
              // 视图记录了自己的引擎；与当前不一致时先切换引擎（重置工作区），
              // 再应用视图状态（后面的 setter 会覆盖重置结果）。
              const viewEngine = view.industrial?.engine ?? "legacy";
              if (viewEngine !== graphEngine) {
                setGraphEngine(viewEngine);
                industrial.switchEngine(viewEngine);
              }
              const containerSize = graphCanvasRef.current?.getContainerSize();
              const result = applyIndustrialSnapshot(
                view,
                {
                  setSelectedIndustries: industrial.setSelectedIndustries,
                  setSelectedCompanies: industrial.setSelectedCompanies,
                  setSelectedFlowIds: industrial.setSelectedFlowIds,
                  setActiveFilters: industrial.setActiveFilters,
                  setExpandedProcessParents: industrial.setExpandedProcessParents,
                  setFocusState: industrial.setFocusState,
                  setHideState: industrial.setHideState,
                  setGraphKey: industrial.setGraphKey,
                  setSubgraphData: industrial.setSubgraphData,
                  setHighlightNodeIds: industrial.setHighlightNodeIds,
                  allIndustries,
                  allCompanies,
                  onSetRestored: setIndustrialViewToRestore,
                },
                containerSize ?? undefined
              );
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
            parentView={loadedIndustrialView ?? undefined}
            onViewSaved={(view) => setLoadedIndustrialView(view)}
            canUndo={viewHistory.canUndo("industrial")}
            onUndo={handleUndo}
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
          engine={graphEngine}
          readOnly={isReadOnlyEngine}
          hasActiveSelection={
            industrial.selectedIndustries.length > 0 ||
            industrial.selectedCompanies.length > 0 ||
            industrial.selectedFlowIds.length > 0 ||
            industrial.focusState.active ||
            industrial.hideState.active ||
            !!industrial.subgraphData ||
            !!industrial.highlightNodeIds
          }
          onResetSelection={() => {
            // 返回全图：不清空已有节点，只把后端最新的节点/边合并进来，
            // 并在原地显示。已有节点位置和相机保持不变。
            viewHistory.reset("industrial");
            industrial.resetSelections({ remount: false });
            industrial.mergeFullGraphData(graphCanvasRef);
          }}
        />
      }
      rightPanel={
        isFlowEngine && flowEditorOpen ? (
          <FlowEditorPanel
            onClose={() => setFlowEditorOpen(false)}
            onSaved={() => {
              // Refresh the flow graph after save so the main canvas reflects changes.
              industrial.recompileSelectedFlows();
            }}
            onPreviewChange={(result) => {
              if (!result) {
                setEditorHighlightIds([]);
                return;
              }
              const includeSet = new Set(result.includes || []);
              const ids = new Set<string>();
              for (const e of result.edges) {
                const fid = (e.properties?.flow_id as string) || "";
                // Current flow edges are those not belonging to included flows.
                if (!includeSet.has(fid)) {
                  ids.add(e.from_node);
                  ids.add(e.to_node);
                }
              }
              setEditorHighlightIds(Array.from(ids));
            }}
          />
        ) : (
          industrialRightPanel
        )
      }
      rightPanelWidth={isFlowEngine && flowEditorOpen ? flowEditorWidth : undefined}
      onRightPanelResize={
        isFlowEngine && flowEditorOpen ? setFlowEditorWidth : undefined
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
          ref={explorationCanvasRef}
          nodes={company.explorationData?.nodes ?? []}
          edges={company.explorationData?.edges ?? []}
          onNodeClick={company.handleExplorationNodeClick}
          onEdgeClick={(edge) => company.setSelectedExplorationEdge(edge)}
          highlightNodeId={company.currentFocusId}
          restoredCamera={companyViewToRestore?.camera}
          onBeforeDragStart={() => pushCompanyHistory(true)}
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
          onBeforeDragStart={() => pushCompanyHistory(true)}
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
        onBeforeDragStart={() => pushCompanyHistory(true)}
        onNodeDblClick={company.handleCompanyNodeClick}
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
        selectedNodes={null}
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
              viewHistory.reset("company");
              setLoadedCompanyView(view);
              const containerSize = activeCompanyCanvasRef.current?.getContainerSize();
              applyCompanySnapshot(
                view,
                {
                  setCompanyDisplayMode: company.setCompanyDisplayMode,
                  setCompanyExploreMode: company.setCompanyExploreMode,
                  setOrderedChain: company.setOrderedChain,
                  setFixedIds: company.setFixedIds,
                  setCurrentFocusId: company.setCurrentFocusId,
                  setExplorationData: company.setExplorationData,
                  setPreviewData: company.setPreviewData,
                  onSetRestored: setCompanyViewToRestore,
                },
                containerSize ?? undefined
              );
            }}
            onManageViews={() => {
              setViewManagerWorkspace("company");
              setViewManagerOpen(true);
            }}
            parentView={loadedCompanyView ?? undefined}
            onViewSaved={(view) => setLoadedCompanyView(view)}
            canUndo={viewHistory.canUndo("company")}
            onUndo={handleUndo}
          />
        </div>
      }
      searchPanel={
        <CompanySearchPanel
          companyExploreMode={company.companyExploreMode}
          setCompanyExploreMode={(mode) => {
            viewHistory.reset("company");
            company.setCompanyExploreMode(mode);
          }}
          companyDisplayMode={company.companyDisplayMode}
          orderedChain={company.orderedChain}
          fixedIds={company.fixedIds}
          nodeStore={company.nodeStore}
          currentFocusId={company.currentFocusId}
          previewData={company.previewData}
          selectedExplorationEdge={company.selectedExplorationEdge}
          onClear={() => {
            viewHistory.reset("company");
            company.clearView();
          }}
        />
      }
      rightPanel={companyRightPanel}
    />
  );

  const isGraphView = mainView === "industrial_graph" || mainView === "company_graph";

  const contextMenuNodeId = industrial.contextMenu.node?.node_id;
  const { data: provCountData } = useQuery({
    queryKey: ["prov-count", contextMenuNodeId],
    queryFn: () => listProvStatementsByNode(contextMenuNodeId!, 1, 1),
    enabled: !!contextMenuNodeId,
    staleTime: 60_000,
  });
  const provCount = provCountData?.total ?? 0;

  return (
    <div className="flex h-screen w-full flex-col bg-slate-950">
      <div className="h-14 shrink-0 border-b border-slate-800 bg-slate-900">
        <StatsBar
          mainView={mainView}
          onChangeMainView={handleChangeMainView}
          graphEngine={graphEngine}
          onChangeGraphEngine={handleChangeGraphEngine}
        />
      </div>

      <div className="relative flex-1 overflow-hidden">
        {/* Graph workspace — keep mounted so switching back does not reload the canvas */}
        <div className={`absolute inset-0 ${isGraphView ? "" : "hidden"}`}>
          {mainView === "company_graph" ? companyWorkspace : industrialWorkspace}
        </div>

        {/* DbChecks page — mounted but hidden when not active */}
        <div className={`absolute inset-0 ${mainView === "db_checks" ? "" : "hidden"}`}>
          <DbChecksPage />
        </div>

        {/* Reasoning page — mounted but hidden when not active */}
        <div className={`absolute inset-0 ${mainView === "reasoning" ? "" : "hidden"}`}>
          <ReasoningPage />
        </div>

        {/* Flow editor page — mounted but hidden when not active */}
        <div className={`absolute inset-0 ${mainView === "flow_editor" ? "" : "hidden"}`}>
          <FlowEditorPage />
        </div>
      </div>

      {mainView === "industrial_graph" &&
        industrial.contextMenu.visible &&
        industrial.contextMenu.node && (
          <NodeContextMenu
            x={industrial.contextMenu.x}
            y={industrial.contextMenu.y}
            nodeName={industrial.contextMenu.node.canonical_name_zh}
            provCount={provCount}
            onViewProv={() => {
              industrial.pushPanel({
                panel: "node-prov",
                selectedNode: industrial.contextMenu.node,
              });
              industrial.setContextMenu((prev) => ({ ...prev, visible: false }));
            }}
            onShowCompanies={() => {
              if (industrial.contextMenu.node) {
                industrial.showCompanyFilter([industrial.contextMenu.node]);
              }
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
              if (!node) return;
              if (industrial.focusState.active) {
                graphCanvasRef.current?.revealNeighbors(node.node_id, "upstream", 1);
              } else {
                graphCanvasRef.current?.showNeighbors(node.node_id, "upstream");
              }
              industrial.setContextMenu((prev) => ({ ...prev, visible: false }));
            }}
            onShowDownstream={() => {
              const node = industrial.contextMenu.node;
              if (!node) return;
              if (industrial.focusState.active) {
                graphCanvasRef.current?.revealNeighbors(node.node_id, "downstream", 1);
              } else {
                graphCanvasRef.current?.showNeighbors(node.node_id, "downstream");
              }
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
              if (node) {
                pushIndustrialHistory(true);
                graphCanvasRef.current?.pullNeighborsIntoView(node.node_id, "upstream");
              }
              industrial.setContextMenu((prev) => ({ ...prev, visible: false }));
            }}
            onPullDownstream={() => {
              const node = industrial.contextMenu.node;
              if (node) {
                pushIndustrialHistory(true);
                graphCanvasRef.current?.pullNeighborsIntoView(node.node_id, "downstream");
              }
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
            inFocusMode={industrial.focusState.active}
            onFocusNode={() => {
              const node = industrial.contextMenu.node;
              if (node) graphCanvasRef.current?.enterFocus([node.node_id]);
            }}
            onHideNode={() => {
              const node = industrial.contextMenu.node;
              if (node) industrial.hideNodes([node.node_id]);
            }}
            onRevealInternal={() => {
              const node = industrial.contextMenu.node;
              if (node) graphCanvasRef.current?.revealInternal(node.node_id);
            }}
            onExitFocus={() => graphCanvasRef.current?.exitFocus()}
            onConnect={
              isReadOnlyEngine
                ? undefined
                : () => {
                    const node = industrial.contextMenu.node;
                    if (!node) return;
                    industrial.setEditMode("connect");
                    industrial.handleConnectSourceSelect(node, {
                      x: industrial.contextMenu.x,
                      y: industrial.contextMenu.y,
                    });
                    industrial.setContextMenu((prev) => ({ ...prev, visible: false }));
                  }
            }
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
            onAlignHorizontal={() => graphCanvasRef.current?.alignSelectedNodes("y")}
            onAlignVertical={() => graphCanvasRef.current?.alignSelectedNodes("x")}
            onDistributeHorizontal={() => graphCanvasRef.current?.distributeSelectedNodes("x")}
            onDistributeVertical={() => graphCanvasRef.current?.distributeSelectedNodes("y")}
            onClearSelection={() => {
              graphCanvasRef.current?.clearNodeSelection();
            }}
            onFocusSelected={() => {
              const nodes = industrial.multiNodeContextMenu.nodes;
              if (nodes.length > 0) {
                graphCanvasRef.current?.enterFocus(nodes.map((n) => n.node_id));
              }
            }}
            onHideSelected={() => {
              const nodes = industrial.multiNodeContextMenu.nodes;
              if (nodes.length > 0) {
                industrial.hideNodes(nodes.map((n) => n.node_id));
              }
            }}
            onShowCompanies={() => {
              const nodes = industrial.multiNodeContextMenu.nodes;
              if (nodes.length > 0) {
                industrial.showCompanyFilter(nodes);
              }
              industrial.handleCloseMultiNodeContextMenu();
            }}
            onClose={industrial.handleCloseMultiNodeContextMenu}
          />
        )}

      {mainView === "industrial_graph" && (
        <CompanyFilterPanel
          visible={industrial.companyFilter.visible}
          nodes={industrial.companyFilter.nodes}
          onClose={() => {
            industrial.closeCompanyFilter();
            industrial.handleHighlightNodes([]);
          }}
          onHighlightNodes={industrial.handleHighlightNodes}
          onViewCompanyDetail={(company) =>
            industrial.pushPanel({
              panel: "company-detail",
              selectedCompany: company,
              selectedNode: null,
              selectedIndustry: null,
            })
          }
        />
      )}

      {mainView === "industrial_graph" && industrial.canvasMenu.visible && !isReadOnlyEngine && (
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
            onDelete={
              isReadOnlyEngine
                ? undefined
                : () => {
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
                  }
            }
            onPull={() => {
              const edge = industrial.edgeMenu.edge;
              if (edge) {
                pushIndustrialHistory(true);
                graphCanvasRef.current?.pullEdgeEndpointsIntoView(edge.edge_id);
              }
              industrial.handleCloseEdgeMenu();
            }}
            onClose={industrial.handleCloseEdgeMenu}
          />
        )}

      {mainView === "industrial_graph" &&
        !isReadOnlyEngine &&
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
          className="fixed z-50 w-80 max-w-[calc(100vw-2rem)] rounded-lg border border-slate-700 bg-slate-900/95 p-3 shadow-xl backdrop-blur"
          style={{
            left: Math.min(quickNodeAt.node.x, Math.max(16, window.innerWidth - 320 - 16)),
            top: Math.min(quickNodeAt.node.y, Math.max(16, window.innerHeight - 420 - 16)),
          }}
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
              viewHistory.reset("industrial");
              setLoadedIndustrialView(view);
              // 与工具栏加载视图一致：视图记录的引擎与当前不一致时先切换引擎。
              const viewEngine = view.industrial?.engine ?? "legacy";
              if (viewEngine !== graphEngine) {
                setGraphEngine(viewEngine);
                industrial.switchEngine(viewEngine);
              }
              const containerSize = graphCanvasRef.current?.getContainerSize();
              const result = applyIndustrialSnapshot(
                view,
                {
                  setSelectedIndustries: industrial.setSelectedIndustries,
                  setSelectedCompanies: industrial.setSelectedCompanies,
                  setSelectedFlowIds: industrial.setSelectedFlowIds,
                  setActiveFilters: industrial.setActiveFilters,
                  setExpandedProcessParents: industrial.setExpandedProcessParents,
                  setFocusState: industrial.setFocusState,
                  setHideState: industrial.setHideState,
                  setGraphKey: industrial.setGraphKey,
                  setSubgraphData: industrial.setSubgraphData,
                  setHighlightNodeIds: industrial.setHighlightNodeIds,
                  allIndustries,
                  allCompanies,
                  onSetRestored: setIndustrialViewToRestore,
                },
                containerSize ?? undefined
              );
              if (result.missingIndustryIds.length > 0 || result.missingCompanyIds.length > 0) {
                setImportMessage(
                  `已恢复视图。缺失 ${result.missingIndustryIds.length} 个行业、${result.missingCompanyIds.length} 个公司。`
                );
              }
            } else {
              viewHistory.reset("company");
              setLoadedCompanyView(view);
              const containerSize = activeCompanyCanvasRef.current?.getContainerSize();
              applyCompanySnapshot(
                view,
                {
                  setCompanyDisplayMode: company.setCompanyDisplayMode,
                  setCompanyExploreMode: company.setCompanyExploreMode,
                  setOrderedChain: company.setOrderedChain,
                  setFixedIds: company.setFixedIds,
                  setCurrentFocusId: company.setCurrentFocusId,
                  setExplorationData: company.setExplorationData,
                  setPreviewData: company.setPreviewData,
                  onSetRestored: setCompanyViewToRestore,
                },
                containerSize ?? undefined
              );
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
    </div>
  );
}
