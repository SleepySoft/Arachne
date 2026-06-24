import {
  Company,
  Industry,
  GraphEdge,
  IndustrialNode,
} from "@/types";
import {
  SavedView,
  IndustrialViewState,
  CompanyViewState,
  CameraState,
  NodePositions,
} from "@/types/view";

export interface GraphCameraController {
  getCamera: () => CameraState | null;
  setCamera: (camera: CameraState) => void;
  getNodePositions: () => NodePositions;
  setNodePositions: (positions: NodePositions) => void;
}

export interface IndustrialSnapshotDeps {
  selectedIndustries: Industry[];
  selectedCompanies: Company[];
  activeFilters: IndustrialViewState["activeFilters"];
  expandedProcessParents: string[];
  canvasRef: React.RefObject<GraphCameraController | null>;
}

export interface IndustrialRestoreDeps {
  setSelectedIndustries: (industries: Industry[]) => void;
  setSelectedCompanies: (companies: Company[]) => void;
  setActiveFilters: (filters: IndustrialViewState["activeFilters"]) => void;
  setExpandedProcessParents: (ids: string[]) => void;
  setGraphKey: (fn: (k: number) => number) => void;
  setSubgraphData: (data: { nodes: IndustrialNode[]; edges: GraphEdge[] } | undefined) => void;
  setHighlightNodeIds: (ids: string[] | undefined) => void;
  allIndustries: Industry[];
  allCompanies: Company[];
  onSetRestored: (state: IndustrialViewState) => void;
}

export type ExplorationNode = import("@/components/ExplorationCanvas").ExplorationNode;
export type ExplorationEdge = import("@/components/ExplorationCanvas").ExplorationEdge;

export interface CompanySnapshotDeps {
  companyDisplayMode: CompanyViewState["displayMode"];
  companyExploreMode: CompanyViewState["exploreMode"];
  orderedChain: string[];
  fixedIds: Set<string>;
  currentFocusId: string | null;
  explorationData: { nodes: ExplorationNode[]; edges: ExplorationEdge[] } | null;
  canvasRef: React.RefObject<GraphCameraController | null> | undefined;
}

export interface CompanyRestoreDeps {
  setCompanyDisplayMode: (mode: CompanyViewState["displayMode"]) => void;
  setCompanyExploreMode: (mode: CompanyViewState["exploreMode"]) => void;
  setOrderedChain: (ids: string[]) => void;
  setFixedIds: (ids: Set<string>) => void;
  setCurrentFocusId: (id: string | null) => void;
  setExplorationData: (data: { nodes: ExplorationNode[]; edges: ExplorationEdge[] } | null) => void;
  setPreviewData: (data: { centerId: string; nodes: import("@/types").CompanyNetworkNode[]; edges: import("@/types").CompanyNetworkEdge[] } | null) => void;
  onSetRestored: (state: CompanyViewState) => void;
}

export function buildIndustrialSnapshot(
  deps: IndustrialSnapshotDeps,
  name: string
): Omit<SavedView, "id" | "created_at" | "updated_at"> {
  const canvas = deps.canvasRef.current;
  const nodePositions = canvas?.getNodePositions();
  const camera = canvas?.getCamera();

  return {
    version: 1,
    name,
    workspace: "industrial",
    industrial: {
      selectedIndustryIds: deps.selectedIndustries.map((i) => i.industry_id),
      selectedCompanyIds: deps.selectedCompanies.map((c) => c.company_id),
      activeFilters: { ...deps.activeFilters },
      expandedProcessParentIds: [...deps.expandedProcessParents],
      camera: camera ?? { pan: { x: 0, y: 0 }, zoom: 1 },
      nodePositions: nodePositions && Object.keys(nodePositions).length > 0 ? nodePositions : undefined,
    },
  };
}

export function applyIndustrialSnapshot(
  view: SavedView,
  deps: IndustrialRestoreDeps
): { restored: boolean; missingIndustryIds: string[]; missingCompanyIds: string[] } {
  if (view.workspace !== "industrial" || !view.industrial) {
    return { restored: false, missingIndustryIds: [], missingCompanyIds: [] };
  }

  const state = view.industrial;
  const industryById = new Map(deps.allIndustries.map((i) => [i.industry_id, i]));
  const companyById = new Map(deps.allCompanies.map((c) => [c.company_id, c]));

  const foundIndustries: Industry[] = [];
  const missingIndustryIds: string[] = [];
  state.selectedIndustryIds.forEach((id) => {
    const ind = industryById.get(id);
    if (ind) foundIndustries.push(ind);
    else missingIndustryIds.push(id);
  });

  const foundCompanies: Company[] = [];
  const missingCompanyIds: string[] = [];
  state.selectedCompanyIds.forEach((id) => {
    const comp = companyById.get(id);
    if (comp) foundCompanies.push(comp);
    else missingCompanyIds.push(id);
  });

  // Clear any transient subgraph/highlight so the merged-subgraph effect recomputes cleanly.
  deps.setSubgraphData(undefined);
  deps.setHighlightNodeIds(undefined);

  deps.setActiveFilters({ ...state.activeFilters });
  deps.setExpandedProcessParents([...state.expandedProcessParentIds]);
  deps.setSelectedIndustries(foundIndustries);
  deps.setSelectedCompanies(foundCompanies);

  // Bump graph key to force canvas re-init with the new merged subgraph / full graph.
  deps.setGraphKey((k) => k + 1);

  // Hand the saved camera/positions up to the parent so the canvas can apply them
  // after it has re-initialized and finished its layout.
  deps.onSetRestored(state);

  return {
    restored: true,
    missingIndustryIds,
    missingCompanyIds,
  };
}

export function buildCompanySnapshot(
  deps: CompanySnapshotDeps,
  name: string
): Omit<SavedView, "id" | "created_at" | "updated_at"> {
  const canvas = deps.canvasRef?.current;
  const camera = canvas?.getCamera();

  return {
    version: 1,
    name,
    workspace: "company",
    company: {
      displayMode: deps.companyDisplayMode,
      exploreMode: deps.companyExploreMode,
      orderedChain: [...deps.orderedChain],
      fixedIds: [...deps.fixedIds],
      currentFocusId: deps.currentFocusId,
      exploration: deps.explorationData
        ? {
            nodes: deps.explorationData.nodes.map((n) => ({ ...n })),
            edges: deps.explorationData.edges.map((e) => ({ ...e })),
          }
        : undefined,
      camera: camera ?? { pan: { x: 0, y: 0 }, zoom: 1 },
    },
  };
}

export function applyCompanySnapshot(
  view: SavedView,
  deps: CompanyRestoreDeps
): { restored: boolean } {
  if (view.workspace !== "company" || !view.company) {
    return { restored: false };
  }

  const state = view.company;

  deps.setCompanyDisplayMode(state.displayMode);
  deps.setCompanyExploreMode(state.exploreMode);
  deps.setOrderedChain([...state.orderedChain]);
  deps.setFixedIds(new Set(state.fixedIds));
  deps.setCurrentFocusId(state.currentFocusId);

  if (state.exploration) {
    deps.setExplorationData({
      nodes: state.exploration.nodes.map((n) => ({ ...n })),
      edges: state.exploration.edges.map((e) => ({ ...e })),
    });
  } else {
    deps.setExplorationData(null);
  }

  // Preview data is derived; clear it so it can be recomputed if needed.
  deps.setPreviewData(null);

  // Hand camera/positions up to the parent to apply after the canvas is ready.
  deps.onSetRestored(state);

  return { restored: true };
}
