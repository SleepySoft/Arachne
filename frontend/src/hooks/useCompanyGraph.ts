import { useCallback, useMemo, useState } from "react";
import { CompanyNetworkEdge, CompanyNetworkNode, Company, PanelType } from "@/types";
import { getCompany, getExplorationGraph } from "@/services/api";
import {
  ExplorationEdge as EEdge,
  ExplorationNode as ENode,
} from "@/components/ExplorationCanvas";

export function useCompanyGraph() {
  const [panel, setPanel] = useState<PanelType>("none");
  const [selectedCompany, setSelectedCompany] = useState<Company | null>(null);
  const [selectedRelation, setSelectedRelation] = useState<CompanyNetworkEdge | null>(null);

  const [companyDisplayMode, setCompanyDisplayMode] = useState<
    "empty" | "global" | "local"
  >("empty");
  const [companyNetworkData] = useState<{ nodes: CompanyNetworkNode[]; edges: CompanyNetworkEdge[] } | null>(null);

  // orderedChain: exploration path (max 2, oldest auto-removed)
  const [orderedChain, setOrderedChain] = useState<string[]>([]);
  // fixedIds: double-click pinned nodes, never auto-removed
  const [fixedIds, setFixedIds] = useState<Set<string>>(new Set());
  // nodeStore: cache of all nodes ever loaded
  const [nodeStore, setNodeStore] = useState<Map<string, CompanyNetworkNode>>(new Map());
  // permanentEdges: edges between visible permanent nodes
  const [permanentEdges, setPermanentEdges] = useState<CompanyNetworkEdge[]>([]);

  // Current focus: the node whose upstream/downstream are shown as preview
  const [currentFocusId, setCurrentFocusId] = useState<string | null>(null);

  // Preview: temporary translucent nodes/edges for the current focus
  const [previewData, setPreviewData] = useState<{
    centerId: string;
    nodes: CompanyNetworkNode[];
    edges: CompanyNetworkEdge[];
  } | null>(null);

  const [isDrawingGlobal] = useState(false);

  const [companyExploreMode, setCompanyExploreMode] = useState<"bulk" | "manual">("bulk");

  // Exploration graph data (for manual mode)
  const [explorationData, setExplorationData] = useState<{
    nodes: ENode[];
    edges: EEdge[];
  } | null>(null);

  // Material panel state (for manual exploration mode)
  const [materialPanelOpen, setMaterialPanelOpen] = useState(false);
  const [selectedMaterialNode, setSelectedMaterialNode] = useState<{
    id: string;
    name: string;
  } | null>(null);

  // Material modal state
  const [materialModalOpen, setMaterialModalOpen] = useState(false);

  // Selected exploration edge for detail display
  const [selectedExplorationEdge, setSelectedExplorationEdge] = useState<EEdge | null>(null);

  const permanentIds = useMemo(() => {
    const ids = new Set<string>([...orderedChain, ...fixedIds]);
    return ids;
  }, [orderedChain, fixedIds]);

  const allCompanyNodes = useMemo(() => {
    const map = new Map<string, CompanyNetworkNode>();
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
    const edges: CompanyNetworkEdge[] = [];
    const key = (e: CompanyNetworkEdge) => `${e.from_company_id}->${e.to_company_id}`;
    // Permanent edges (both ends still visible)
    permanentEdges.forEach((e) => {
      if (
        permanentIds.has(e.from_company_id) &&
        permanentIds.has(e.to_company_id)
      ) {
        if (!seen.has(key(e))) {
          seen.add(key(e));
          edges.push(e);
        }
      }
    });
    previewData?.edges.forEach((e) => {
      if (!seen.has(key(e))) {
        seen.add(key(e));
        edges.push(e);
      }
    });
    return edges;
  }, [permanentEdges, permanentIds, previewData]);

  const previewNodeIds = useMemo(() => {
    return (
      previewData?.nodes
        .map((n) => n.company_id)
        .filter((id) => !permanentIds.has(id)) ?? []
    );
  }, [previewData, permanentIds]);

  const clearView = useCallback(() => {
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
    setSelectedMaterialNode(null);
  }, []);

  // Start a new investigation chain from a company
  const startInvestigation = useCallback(
    (company: Company, autoPreview: boolean = true) => {
      const node: CompanyNetworkNode = {
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
      setExplorationData(null);
      if (autoPreview) loadPreview(company.company_id);
    },
    []
  );

  // Load preview (temporary translucent network) for a given company
  const loadPreview = useCallback(async (_companyId: string) => {
    // Company view upstream/downstream APIs have been removed.
    // Preview based on inferred industrial relations is no longer available.
    // Use /api/v1/explore endpoints for cross-domain exploration instead.
    setPreviewData(null);
  }, []);

  // Load exploration graph (heterogeneous: company + material nodes)
  const loadExplorationGraph = useCallback(async (companyId: string) => {
    try {
      const data = await getExplorationGraph(companyId);
      setExplorationData(data);
    } catch {
      setExplorationData(null);
    }
  }, []);

  // Select company from sidebar (company graph view)
  const handleSelectCompany = useCallback(
    (company: Company) => {
      setSelectedCompany(company);
      setPanel("company-detail");

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
        if (
          orderedChain.includes(company.company_id) ||
          fixedIds.has(company.company_id)
        ) {
          setCurrentFocusId(company.company_id);
          loadPreview(company.company_id);
        } else {
          startInvestigation(company, true);
        }
      }
    },
    [companyDisplayMode, companyExploreMode, fixedIds, loadExplorationGraph, loadPreview, orderedChain, startInvestigation]
  );

  // Click on a node inside the exploration canvas (manual mode)
  const handleExplorationNodeClick = useCallback(
    async (node: ENode) => {
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
    },
    []
  );

  // Add selected companies to the exploration graph
  const handleAddCompaniesToExploration = useCallback(
    (
      companies: {
        id: string;
        label: string;
        direction: "peer" | "upstream" | "downstream";
        via_node_id?: string;
        via_node_name?: string;
        activity_type: string;
      }[]
    ) => {
      if (!explorationData || !selectedMaterialNode) return;

      const newNodes: ENode[] = [];
      const newEdges: EEdge[] = [];
      const existingNodeIds = new Set(explorationData.nodes.map((n) => n.id));
      const existingEdgeKeys = new Set(
        explorationData.edges.map((e) => `${e.source}→${e.target}`)
      );

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
            label:
              c.direction === "peer"
                ? undefined
                : c.direction === "upstream"
                ? `原料: ${c.via_node_name || c.via_node_id}`
                : `下游: ${c.via_node_name || c.via_node_id}`,
          });
          existingEdgeKeys.add(edgeKey);
        }
      });

      setExplorationData({
        nodes: [...explorationData.nodes, ...newNodes],
        edges: [...explorationData.edges, ...newEdges],
      });
    },
    [explorationData, selectedMaterialNode]
  );

  // Click on a node inside the company network canvas
  const handleCompanyNodeClick = useCallback(
    async (companyNode: CompanyNetworkNode) => {
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
        const newEdges = previewData.edges.filter(
          (e) =>
            (e.from_company_id === cid && visibleIds.has(e.to_company_id)) ||
            (e.to_company_id === cid && visibleIds.has(e.from_company_id))
        );
        if (newEdges.length > 0) {
          setPermanentEdges((prev) => {
            const seen = new Set(
              prev.map((e) => `${e.from_company_id}->${e.to_company_id}`)
            );
            return [
              ...prev,
              ...newEdges.filter(
                (e) => !seen.has(`${e.from_company_id}->${e.to_company_id}`)
              ),
            ];
          });
        }

        setCurrentFocusId(cid);
        loadPreview(cid);
      }
    },
    [
      companyDisplayMode,
      companyExploreMode,
      currentFocusId,
      fixedIds,
      loadPreview,
      orderedChain,
      previewData,
      startInvestigation,
    ]
  );

  // Double-click on a node inside the company network canvas
  const handleCompanyNodeDblClick = useCallback(
    async (companyNode: CompanyNetworkNode) => {
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
          const seen = new Set(
            prev.map((e) => `${e.from_company_id}->${e.to_company_id}`)
          );
          const newEdges = previewData.edges.filter(
            (e) => !seen.has(`${e.from_company_id}->${e.to_company_id}`)
          );
          return [...prev, ...newEdges];
        });

        setPreviewData(null);
      }
    },
    [companyDisplayMode, previewData, startInvestigation]
  );

  // Click on an edge inside the company network canvas
  const handleCompanyEdgeClick = useCallback((edge: CompanyNetworkEdge) => {
    setSelectedRelation(edge);
    setPanel("company-relation-detail");
  }, []);

  const handleAddToViewFromModal = useCallback(
    (nodes: CompanyNetworkNode[], edges: CompanyNetworkEdge[]) => {
      setNodeStore((prev) => {
        const next = new Map(prev);
        nodes.forEach((n) => {
          if (!next.has(n.company_id)) next.set(n.company_id, n);
        });
        return next;
      });
      setPermanentEdges((prev) => {
        const seen = new Set(
          prev.map((e) => `${e.from_company_id}->${e.to_company_id}`)
        );
        const newEdges = edges.filter(
          (e) => !seen.has(`${e.from_company_id}->${e.to_company_id}`)
        );
        return [...prev, ...newEdges];
      });
      setCompanyDisplayMode("local");
    },
    []
  );

  return {
    panel,
    setPanel,
    selectedCompany,
    setSelectedCompany,
    selectedRelation,
    setSelectedRelation,
    companyDisplayMode,
    setCompanyDisplayMode,
    companyNetworkData,
    orderedChain,
    setOrderedChain,
    fixedIds,
    setFixedIds,
    nodeStore,
    setNodeStore,
    permanentEdges,
    setPermanentEdges,
    currentFocusId,
    setCurrentFocusId,
    previewData,
    setPreviewData,
    isDrawingGlobal,
    companyExploreMode,
    setCompanyExploreMode,
    explorationData,
    setExplorationData,
    materialPanelOpen,
    setMaterialPanelOpen,
    selectedMaterialNode,
    setSelectedMaterialNode,
    materialModalOpen,
    setMaterialModalOpen,
    selectedExplorationEdge,
    setSelectedExplorationEdge,
    permanentIds,
    allCompanyNodes,
    allCompanyEdges,
    previewNodeIds,
    clearView,
    startInvestigation,
    loadExplorationGraph,
    loadPreview,
    handleSelectCompany,
    handleExplorationNodeClick,
    handleAddCompaniesToExploration,
    handleCompanyNodeClick,
    handleCompanyNodeDblClick,
    handleCompanyEdgeClick,
    handleAddToViewFromModal,
  };
}
