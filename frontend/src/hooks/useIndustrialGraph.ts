import { useCallback, useEffect, useState } from "react";
import {
  GraphEdge,
  IndustrialNode,
  Industry,
  Company,
  PanelType,
} from "@/types";
import { EditMode } from "@/components/GraphCanvas";
import { getCompanySubgraph, getIndustrySubgraph } from "@/services/api";
import { useNodeNavigation } from "./useNodeNavigation";

export function useIndustrialGraph() {
  const [selectedNode, setSelectedNode] = useState<IndustrialNode | null>(null);
  const [selectedEdge, setSelectedEdge] = useState<GraphEdge | null>(null);
  const [selectedIndustry, setSelectedIndustry] = useState<Industry | null>(null);
  const [selectedCompany, setSelectedCompany] = useState<Company | null>(null);
  const [selectedIndustries, setSelectedIndustries] = useState<Industry[]>([]);
  const [selectedCompanies, setSelectedCompanies] = useState<Company[]>([]);
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

  const nav = useNodeNavigation();

  const handleNodeClick = useCallback(
    (node: IndustrialNode) => {
      setSelectedNode(node);
      setSelectedEdge(null);
      setPanel("node-detail");
      setContextMenu((prev) => ({ ...prev, visible: false }));
      nav.push(node);
    },
    [nav]
  );

  const handleNavBack = useCallback(() => {
    const node = nav.back();
    if (node) {
      setSelectedNode(node);
      setPanel("node-detail");
    }
  }, [nav]);

  const handleNavForward = useCallback(() => {
    const node = nav.forward();
    if (node) {
      setSelectedNode(node);
      setPanel("node-detail");
    }
  }, [nav]);

  const handleNavGoto = useCallback(
    (targetIndex: number) => {
      const node = nav.goto(targetIndex);
      if (node) {
        setSelectedNode(node);
        setPanel("node-detail");
      }
    },
    [nav]
  );

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

  const handleSelectIndustryDetail = useCallback((industry: Industry) => {
    setSelectedIndustry(industry);
    setPanel("industry-detail");
  }, []);

  const handleToggleCompanyIndustrial = useCallback((company: Company) => {
    setSelectedCompanies((prev) => {
      const exists = prev.some((c) => c.company_id === company.company_id);
      if (exists) {
        return prev.filter((c) => c.company_id !== company.company_id);
      }
      return [...prev, company];
    });
  }, []);

  const handleSelectCompanyDetail = useCallback((company: Company) => {
    setSelectedCompany(company);
    setPanel("company-detail");
  }, []);

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

  const resetSelections = useCallback(() => {
    setSelectedIndustries([]);
    setSelectedCompanies([]);
    setSubgraphData(undefined);
    setHighlightNodeIds(undefined);
    setGraphKey((k) => k + 1);
  }, []);

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
  }, []);

  const handleCloseCanvasMenu = useCallback(() => {
    setCanvasMenu((prev) => ({ ...prev, visible: false }));
    setPendingNodePosition(null);
  }, []);

  const handleEdgeContextMenu = useCallback(
    (edge: GraphEdge, x: number, y: number) => {
      setEdgeMenu({ visible: true, x, y, edge });
    },
    []
  );

  const handleCloseEdgeMenu = useCallback(() => {
    setEdgeMenu({ visible: false, x: 0, y: 0, edge: null });
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
      setPanel("edge-create");
    },
    []
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
    handleNodeClick,
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
    isProcessParentExpanded,
    canvasMenu,
    setCanvasMenu,
    handleCanvasContextMenu,
    handleCloseCanvasMenu,
    edgeMenu,
    setEdgeMenu,
    handleEdgeContextMenu,
    handleCloseEdgeMenu,
    pendingNodePosition,
    setPendingNodePosition,
    pendingEdgePrefill,
    setPendingEdgePrefill,
    handleOpenFullEdgeCreate,
    clearPendingEdgePrefill,
  };
}
