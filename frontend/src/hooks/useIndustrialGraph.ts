import { useCallback, useEffect, useState } from "react";
import {
  GraphEdge,
  IndustrialNode,
  Industry,
  Company,
  PanelType,
} from "@/types";
import { EditMode } from "@/components/GraphCanvas";

import { HideState } from "@/types/view";
import {
  getCompanySubgraph,
  getIndustrySubgraph,
  listNodes,
  listEdges,
} from "@/services/api";
import type { GraphCanvasRef } from "@/components/GraphCanvas";
import { useNodeNavigation } from "./useNodeNavigation";
import { PanelState, usePanelStack } from "./usePanelStack";

export function useIndustrialGraph() {
  const ps = usePanelStack();
  const panel = ps.panel;
  const selectedNode = ps.selectedNode;
  const selectedEdge = ps.selectedEdge;
  const selectedIndustry = ps.selectedIndustry;
  const selectedCompany = ps.selectedCompany;
  const contextMenuNode = ps.contextMenuNode;

  const setPanel = useCallback(
    (next: PanelType) => ps.replace({ panel: next }),
    [ps]
  );
  const pushPanel = useCallback(
    (patch: Partial<PanelState>) => ps.push(patch),
    [ps]
  );
  const popPanel = ps.pop;
  const closePanel = ps.clear;

  const setSelectedNode = ps.setSelectedNode;
  const setSelectedEdge = ps.setSelectedEdge;
  const setSelectedIndustry = ps.setSelectedIndustry;
  const setSelectedCompany = ps.setSelectedCompany;

  const [selectedIndustries, setSelectedIndustries] = useState<Industry[]>([]);
  const [selectedCompanies, setSelectedCompanies] = useState<Company[]>([]);
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
    showIsA: true,
    showWeakOntology: false,
  });
  const [graphKey, setGraphKey] = useState(0);
  const [editMode, setEditMode] = useState<EditMode>("default");
  const [connectSource, setConnectSource] = useState<IndustrialNode | null>(null);
  const [connectTarget, setConnectTarget] = useState<IndustrialNode | null>(null);
  const [connectFormPosition, setConnectFormPosition] = useState<{ x: number; y: number } | null>(null);
  const [canvasMenu, setCanvasMenu] = useState<{
    visible: boolean;
    x: number;
    y: number;
  }>({ visible: false, x: 0, y: 0 });
  const [edgeMenu, setEdgeMenu] = useState<{
    visible: boolean;
    x: number;
    y: number;
    edge: GraphEdge | null;
  }>({ visible: false, x: 0, y: 0, edge: null });
  const [multiNodeContextMenu, setMultiNodeContextMenu] = useState<{
    visible: boolean;
    x: number;
    y: number;
    nodes: IndustrialNode[];
  }>({ visible: false, x: 0, y: 0, nodes: [] });
  const [pendingNodePosition, setPendingNodePosition] = useState<{
    x: number;
    y: number;
  } | null>(null);
  const [pendingEdgePrefill, setPendingEdgePrefill] = useState<{
    from_node: string;
    to_node: string;
    edge_type: string;
    description?: string;
    notes?: string;
  } | null>(null);
  const [subgraphData, setSubgraphData] = useState<
    { nodes: IndustrialNode[]; edges: GraphEdge[] } | undefined
  >(undefined);
  const [highlightNodeIds, setHighlightNodeIds] = useState<
    string[] | undefined
  >(undefined);
  const [expandedProcessParents, setExpandedProcessParents] = useState<string[]>([]);
  const [wheelSensitivity, setWheelSensitivity] = useState<number>(0.1);
  const [focusState, setFocusState] = useState<import("@/types/view").FocusState>({
    active: false,
    seedNodeIds: [],
    visibleNodeIds: [],
    history: [],
  });

  const setFocusActive = useCallback((active: boolean) => {
    setFocusState((prev) => ({ ...prev, active }));
  }, []);

  const clearFocusState = useCallback(() => {
    setFocusState({
      active: false,
      seedNodeIds: [],
      visibleNodeIds: [],
      history: [],
    });
  }, []);

  const [hideState, setHideState] = useState<HideState>({
    active: false,
    hiddenNodeIds: [],
  });

  const hideNodes = useCallback((nodeIds: string[]) => {
    setHideState((prev) => {
      const hidden = new Set([...prev.hiddenNodeIds, ...nodeIds]);
      return { active: hidden.size > 0, hiddenNodeIds: Array.from(hidden) };
    });
  }, []);

  const unhideNodes = useCallback((nodeIds: string[]) => {
    setHideState((prev) => {
      const hidden = new Set(prev.hiddenNodeIds);
      nodeIds.forEach((id) => hidden.delete(id));
      return { active: hidden.size > 0, hiddenNodeIds: Array.from(hidden) };
    });
  }, []);

  const clearHideState = useCallback(() => {
    setHideState({ active: false, hiddenNodeIds: [] });
  }, []);

  const nav = useNodeNavigation();

  const openNodeDetail = useCallback(
    (node: IndustrialNode) => {
      closePanel();
      pushPanel({
        panel: "node-detail",
        selectedNode: node,
        selectedEdge: null,
        selectedIndustry: null,
        selectedCompany: null,
      });
    },
    [closePanel, pushPanel]
  );

  const openEdgeDetail = useCallback(
    (edge: GraphEdge) => {
      closePanel();
      pushPanel({
        panel: "edge-detail",
        selectedEdge: edge,
        selectedNode: null,
        selectedIndustry: null,
        selectedCompany: null,
      });
    },
    [closePanel, pushPanel]
  );

  const handleNodeClick = useCallback(
    (node: IndustrialNode) => {
      openNodeDetail(node);
      setContextMenu((prev) => ({ ...prev, visible: false }));
      nav.push(node);
    },
    [nav, openNodeDetail]
  );

  const handleClearSelection = useCallback(() => {
    closePanel();
    setContextMenu((prev) => ({ ...prev, visible: false }));
    setCanvasMenu((prev) => ({ ...prev, visible: false }));
    setEdgeMenu((prev) => ({ ...prev, visible: false }));
    setMultiNodeContextMenu((prev) => ({ ...prev, visible: false }));
  }, [closePanel]);

  const handleNavBack = useCallback(() => {
    const node = nav.back();
    if (node) {
      openNodeDetail(node);
    }
  }, [nav, openNodeDetail]);

  const handleNavForward = useCallback(() => {
    const node = nav.forward();
    if (node) {
      openNodeDetail(node);
    }
  }, [nav, openNodeDetail]);

  const handleNavGoto = useCallback(
    (targetIndex: number) => {
      const node = nav.goto(targetIndex);
      if (node) {
        openNodeDetail(node);
      }
    },
    [nav, openNodeDetail]
  );

  const handleNodeContextMenu = useCallback(
    (node: IndustrialNode, x: number, y: number) => {
      setContextMenu({ visible: true, x, y, node });
      setCanvasMenu((prev) => ({ ...prev, visible: false }));
      setEdgeMenu({ visible: false, x: 0, y: 0, edge: null });
    },
    []
  );

  const handleEdgeClick = useCallback(
    (edge: GraphEdge) => {
      openEdgeDetail(edge);
    },
    [openEdgeDetail]
  );

  const refreshGraph = useCallback(() => setGraphKey((k) => k + 1), []);

  const handleToggleIndustry = useCallback((industry: Industry) => {
    setSelectedIndustries((prev) => {
      const exists = prev.some((i) => i.industry_id === industry.industry_id);
      if (exists) {
        return prev.filter((i) => i.industry_id !== industry.industry_id);
      }
      return [...prev, industry];
    });
  }, []);

  const handleSelectIndustryDetail = useCallback(
    (industry: Industry) => {
      pushPanel({
        panel: "industry-detail",
        selectedIndustry: industry,
        selectedNode: null,
        selectedCompany: null,
      });
    },
    [pushPanel]
  );

  const handleToggleCompanyIndustrial = useCallback((company: Company) => {
    setSelectedCompanies((prev) => {
      const exists = prev.some((c) => c.company_id === company.company_id);
      if (exists) {
        return prev.filter((c) => c.company_id !== company.company_id);
      }
      return [...prev, company];
    });
  }, []);

  const handleSelectCompanyDetail = useCallback(
    (company: Company) => {
      pushPanel({
        panel: "company-detail",
        selectedCompany: company,
        selectedNode: null,
        selectedIndustry: null,
      });
    },
    [pushPanel]
  );

  const handleLoadSubgraph = useCallback(
    (nodes: unknown[], edges: unknown[]) => {
      setSubgraphData({
        nodes: nodes as IndustrialNode[],
        edges: edges as GraphEdge[],
      });
      setGraphKey((k) => k + 1);
      setHighlightNodeIds(undefined);
    },
    []
  );

  const handleHighlightNodes = useCallback((nodeIds: string[]) => {
    setHighlightNodeIds(nodeIds);
    setSubgraphData(undefined);
  }, []);

  const resetSelections = useCallback(
    (options?: { remount?: boolean }) => {
      setSelectedIndustries([]);
      setSelectedCompanies([]);
      setSubgraphData(undefined);
      setHighlightNodeIds(undefined);
      if (options?.remount !== false) {
        setGraphKey((k) => k + 1);
      }
    },
    []
  );

  // 将后端最新全图数据合并到当前画布，不重建、不重排已有节点。
  // 新增的节点放在其已有邻居的重心附近；孤立新节点放在当前视野中心。
  // 同时会把旧视图加载后仍堆在 (0,0) 的节点重新定位到邻居重心，避免展开工艺组时乱跳。
  const mergeFullGraphData = useCallback(
    async (canvasRef: React.RefObject<GraphCanvasRef | null>) => {
      const canvas = canvasRef.current;
      if (!canvas) return;

      const [{ items: allNodes }, { items: allEdges }] = await Promise.all([
        listNodes(1, 1000),
        listEdges(1, 1000),
      ]);

      const currentPositions = canvas.getNodePositions();
      const currentNodeIds = new Set(Object.keys(currentPositions));

      // 先添加缺失的节点
      const nodesToAdd: IndustrialNode[] = [];
      allNodes.forEach((node) => {
        if (!currentNodeIds.has(node.node_id)) {
          nodesToAdd.push(node);
        }
      });

      // 建立节点id到邻接边的快速索引，用于定位
      const edgesByNode = new Map<string, GraphEdge[]>();
      allEdges.forEach((edge) => {
        const list = edgesByNode.get(edge.from_node) || [];
        list.push(edge);
        edgesByNode.set(edge.from_node, list);
        const list2 = edgesByNode.get(edge.to_node) || [];
        list2.push(edge);
        edgesByNode.set(edge.to_node, list2);
      });

      const camera = canvas.getCamera();
      const containerSize = canvas.getContainerSize();
      const centerX =
        camera && containerSize
          ? (containerSize.width / 2 - camera.pan.x) / camera.zoom
          : 0;
      const centerY =
        camera && containerSize
          ? (containerSize.height / 2 - camera.pan.y) / camera.zoom
          : 0;

      // 旧视图加载后，后端新增的节点可能已经被 GraphCanvas init 以默认位置 (0,0) 加进来。
      // 这些节点不应被视为“已定位”，否则新节点/其它 orphan 节点会参考 (0,0) 互相拉扯。
      const orphanNodeIds = Array.from(currentNodeIds).filter((id) => {
        const pos = currentPositions[id];
        if (!pos || pos.x !== 0 || pos.y !== 0) return false;
        const edges = edgesByNode.get(id) || [];
        return edges.some((e) => {
          const otherId = e.from_node === id ? e.to_node : e.from_node;
          const otherPos = currentPositions[otherId];
          return otherPos && (otherPos.x !== 0 || otherPos.y !== 0);
        });
      });
      const orphanIdSet = new Set(orphanNodeIds);

      // 给节点在视野中心或邻居重心附近分配位置
      let placementIndex = 0;
      const placeNode = (
        nodeId: string,
        add?: (pos: { x: number; y: number }) => void
      ): { x: number; y: number } => {
        const connectedEdges = edgesByNode.get(nodeId) || [];
        const neighborIds = connectedEdges
          .map((e) =>
            e.from_node === nodeId ? e.to_node : e.from_node
          )
          .filter((id) => positionedNodeIds.has(id));

        let x = centerX;
        let y = centerY;
        if (neighborIds.length > 0) {
          const positions = neighborIds
            .map((id) => placedPositions[id])
            .filter((p): p is { x: number; y: number } => !!p);
          if (positions.length > 0) {
            x = positions.reduce((sum, p) => sum + p.x, 0) / positions.length;
            y = positions.reduce((sum, p) => sum + p.y, 0) / positions.length;
          }
        }
        const offset = 60;
        const angle = (placementIndex * 137.5 * Math.PI) / 180;
        placementIndex += 1;
        const pos = {
          x: x + offset * Math.cos(angle),
          y: y + offset * Math.sin(angle),
        };
        if (add) add(pos);
        placedPositions[nodeId] = pos;
        positionedNodeIds.add(nodeId);
        return pos;
      };

      // 按拓扑顺序添加：优先添加与已有图相连的新节点，这样后续节点能利用已添加节点的位置
      const positionedNodeIds = new Set(
        Object.keys(currentPositions).filter((id) => !orphanIdSet.has(id))
      );
      const placedPositions: Record<string, { x: number; y: number }> = {
        ...currentPositions,
      };

      nodesToAdd.forEach((node) => {
        placeNode(node.node_id, (pos) => canvas.addNode(node, pos));
      });

      // 再添加缺失的边（addEdge 内部会检查端点是否存在并跳过已存在边）
      allEdges.forEach((edge) => {
        canvas.addEdge(edge);
      });

      // 把堆在 (0,0) 的 orphan 节点重新定位到已有邻居的重心，避免展开工艺组时乱跳。
      orphanNodeIds.forEach((nodeId) => {
        placeNode(nodeId, (pos) => canvas.setNodePosition(nodeId, pos));
      });

      // 同步工艺组：把 part_of 子节点移入 compound parent
      canvas.syncProcessGroups();
    },
    []
  );

  // Load merged subgraph whenever selected industries/companies change
  useEffect(() => {
    async function loadMergedSubgraph() {
      if (selectedIndustries.length === 0 && selectedCompanies.length === 0) {
        setSubgraphData(undefined);
        return;
      }
      try {
        const [industrySubgraphs, companySubgraphs] = await Promise.all([
          Promise.all(selectedIndustries.map((i) => getIndustrySubgraph(i.industry_id))),
          Promise.all(selectedCompanies.map((c) => getCompanySubgraph(c.company_id))),
        ]);
        const nodeMap = new Map<string, IndustrialNode>();
        const edgeMap = new Map<string, GraphEdge>();
        industrySubgraphs.forEach((sg) => {
          sg.nodes.forEach((n) => nodeMap.set(n.node_id, n as IndustrialNode));
          sg.edges.forEach((e) => edgeMap.set(e.edge_id, e as GraphEdge));
        });
        companySubgraphs.forEach((sg) => {
          sg.nodes.forEach((n) => nodeMap.set(n.node_id, n as IndustrialNode));
          sg.edges.forEach((e) => edgeMap.set(e.edge_id, e as GraphEdge));
        });
        setSubgraphData({
          nodes: Array.from(nodeMap.values()),
          edges: Array.from(edgeMap.values()),
        });
        setGraphKey((k) => k + 1);
      } catch {
        // Silently ignore
      }
    }
    loadMergedSubgraph();
  }, [selectedIndustries, selectedCompanies]);

  // ===== Edit mode helpers =====
  const toggleEditMode = useCallback(() => {
    setEditMode((prev) => {
      const next = prev === "default" ? "connect" : "default";
      if (next === "default") {
        setConnectSource(null);
        setConnectTarget(null);
      }
      return next;
    });
  }, []);

  const exitEditMode = useCallback(() => {
    setEditMode("default");
    setConnectSource(null);
    setConnectTarget(null);
    setConnectFormPosition(null);
  }, []);

  const handleCanvasContextMenu = useCallback((x: number, y: number) => {
    setCanvasMenu({ visible: true, x, y });
    setPendingNodePosition({ x, y });
    setContextMenu((prev) => ({ ...prev, visible: false }));
    setEdgeMenu({ visible: false, x: 0, y: 0, edge: null });
  }, []);

  const handleCloseCanvasMenu = useCallback(() => {
    setCanvasMenu((prev) => ({ ...prev, visible: false }));
    setPendingNodePosition(null);
  }, []);

  const handleEdgeContextMenu = useCallback(
    (edge: GraphEdge, x: number, y: number) => {
      setEdgeMenu({ visible: true, x, y, edge });
      setContextMenu((prev) => ({ ...prev, visible: false }));
      setCanvasMenu((prev) => ({ ...prev, visible: false }));
    },
    []
  );

  const handleCloseEdgeMenu = useCallback(() => {
    setEdgeMenu({ visible: false, x: 0, y: 0, edge: null });
  }, []);

  const handleMultiNodeContextMenu = useCallback(
    (nodes: IndustrialNode[], x: number, y: number) => {
      setMultiNodeContextMenu({ visible: true, x, y, nodes });
      setContextMenu((prev) => ({ ...prev, visible: false }));
      setCanvasMenu((prev) => ({ ...prev, visible: false }));
      setEdgeMenu({ visible: false, x: 0, y: 0, edge: null });
    },
    []
  );

  const handleCloseMultiNodeContextMenu = useCallback(() => {
    setMultiNodeContextMenu((prev) => ({ ...prev, visible: false }));
  }, []);

  const handleConnectSourceSelect = useCallback(
    (node: IndustrialNode | null, position?: { x: number; y: number }) => {
      setConnectSource(node);
      setConnectTarget(null);
      if (position) setConnectFormPosition(position);
    },
    []
  );

  const handleConnectTargetSelect = useCallback(
    (node: IndustrialNode, position?: { x: number; y: number }) => {
      setConnectTarget(node);
      if (position) setConnectFormPosition(position);
    },
    []
  );

  const toggleProcessParent = useCallback((nodeId: string) => {
    setExpandedProcessParents((prev) =>
      prev.includes(nodeId) ? prev.filter((id) => id !== nodeId) : [...prev, nodeId]
    );
  }, []);

  const isProcessParentExpanded = useCallback(
    (nodeId: string) => expandedProcessParents.includes(nodeId),
    [expandedProcessParents]
  );

  const handleCancelConnect = useCallback(() => {
    setConnectSource(null);
    setConnectTarget(null);
    setConnectFormPosition(null);
  }, []);

  const handleOpenFullEdgeCreate = useCallback(
    (draft: {
      from_node: string;
      to_node: string;
      edge_type: string;
      description?: string;
      notes?: string;
    }) => {
      setPendingEdgePrefill(draft);
      pushPanel({
        panel: "edge-create",
        selectedNode: null,
        selectedEdge: null,
        selectedIndustry: null,
        selectedCompany: null,
      });
    },
    [pushPanel]
  );

  const clearPendingEdgePrefill = useCallback(() => {
    setPendingEdgePrefill(null);
  }, []);

  return {
    selectedNode,
    setSelectedNode,
    selectedEdge,
    setSelectedEdge,
    selectedIndustry,
    setSelectedIndustry,
    selectedCompany,
    setSelectedCompany,
    selectedIndustries,
    setSelectedIndustries,
    selectedCompanies,
    setSelectedCompanies,
    panel,
    setPanel,
    pushPanel,
    popPanel,
    closePanel,
    canGoBackPanel: ps.canGoBack,
    contextMenuNode,
    contextMenu,
    setContextMenu,
    activeFilters,
    setActiveFilters,
    graphKey,
    setGraphKey,
    subgraphData,
    setSubgraphData,
    highlightNodeIds,
    setHighlightNodeIds,
    nav,
    openNodeDetail,
    openEdgeDetail,
    handleNodeClick,
    handleClearSelection,
    handleNavBack,
    handleNavForward,
    handleNavGoto,
    handleNodeContextMenu,
    handleEdgeClick,
    refreshGraph,
    handleToggleIndustry,
    handleSelectIndustryDetail,
    handleToggleCompanyIndustrial,
    handleToggleCompany: handleToggleCompanyIndustrial,
    handleSelectCompanyDetail,
    handleLoadSubgraph,
    handleHighlightNodes,
    resetSelections,
    mergeFullGraphData,
    // edit mode
    editMode,
    setEditMode,
    toggleEditMode,
    exitEditMode,
    connectSource,
    connectTarget,
    connectFormPosition,
    handleConnectSourceSelect,
    handleConnectTargetSelect,
    handleCancelConnect,
    expandedProcessParents,
    setExpandedProcessParents,
    toggleProcessParent,
    wheelSensitivity,
    setWheelSensitivity,
    isProcessParentExpanded,
    focusState,
    setFocusState,
    setFocusActive,
    clearFocusState,
    hideState,
    setHideState,
    hideNodes,
    unhideNodes,
    clearHideState,
    canvasMenu,
    setCanvasMenu,
    handleCanvasContextMenu,
    handleCloseCanvasMenu,
    edgeMenu,
    setEdgeMenu,
    handleEdgeContextMenu,
    handleCloseEdgeMenu,
    multiNodeContextMenu,
    setMultiNodeContextMenu,
    handleMultiNodeContextMenu,
    handleCloseMultiNodeContextMenu,
    pendingNodePosition,
    setPendingNodePosition,
    pendingEdgePrefill,
    setPendingEdgePrefill,
    handleOpenFullEdgeCreate,
    clearPendingEdgePrefill,
  };
}
