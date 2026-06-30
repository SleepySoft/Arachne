import { ExplorationEdge, ExplorationNode } from "@/components/ExplorationCanvas";

export type WorkspaceType = "industrial" | "company";

export interface CameraState {
  pan: { x: number; y: number };
  zoom: number;
}

export interface NodePositions {
  [nodeId: string]: { x: number; y: number };
}

export interface IndustrialFiltersState {
  edgeNamespaces: string[];
  edgeTypes: string[];
  entityTypes: string[];
  status: string[];
  confidence: string[];
  showIsA: boolean;
  showWeakOntology: boolean;
}

export interface FocusStep {
  nodeId: string;
  direction: "upstream" | "downstream" | "both";
  depthAdded: number;
  addedNodeIds: string[];
}

export interface FocusState {
  active: boolean;
  seedNodeIds: string[];
  visibleNodeIds: string[];
  history: FocusStep[];
}

export interface HideState {
  active: boolean;
  hiddenNodeIds: string[];
}

export interface IndustrialViewState {
  selectedIndustryIds: string[];
  selectedCompanyIds: string[];
  activeFilters: IndustrialFiltersState;
  expandedProcessParentIds: string[];
  camera: CameraState;
  nodePositions?: NodePositions;
  focus?: FocusState;
  hide?: HideState;
  containerSize?: { width: number; height: number };
}

export interface CompanyViewState {
  displayMode: "empty" | "global" | "local";
  exploreMode: "bulk" | "manual";
  orderedChain: string[];
  fixedIds: string[];
  currentFocusId: string | null;
  exploration?: {
    nodes: ExplorationNode[];
    edges: ExplorationEdge[];
  };
  camera: CameraState;
  // Company canvas currently uses deterministic layouts; positions are optional.
  nodePositions?: NodePositions;
  containerSize?: { width: number; height: number };
}

export interface SavedView {
  version: number;
  id: string;
  base: string;
  viewVersion: number;
  name: string;
  workspace: WorkspaceType;
  created_at: string;
  updated_at: string;
  industrial?: IndustrialViewState;
  company?: CompanyViewState;
}

export interface SavedViewFile {
  version: number;
  views: SavedView[];
}
