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
  FocusState,
  HideState,
} from "@/types/view";

export interface GraphCameraController {
  getCamera: () => CameraState | null;
  setCamera: (camera: CameraState) => void;
  getNodePositions: () => NodePositions;
  setNodePositions: (positions: NodePositions) => void;
  getContainerSize: () => { width: number; height: number } | null;
}

/** 跨容器适配比例的安全区间，避免保存时容器尺寸异常导致 zoom 过大/过小。 */
const MIN_VIEW_SCALE = 0.25;
const MAX_VIEW_SCALE = 4;

/**
 * 计算跨容器（跨屏幕/系统缩放）适配比例：取较小方向的比例以保持宽高比，
 * 并钳制在 [MIN_VIEW_SCALE, MAX_VIEW_SCALE] 区间。无效输入返回 null。
 */
function computeViewScale(
  fromSize?: { width: number; height: number },
  toSize?: { width: number; height: number }
): number | null {
  if (!fromSize || !toSize || fromSize.width <= 0 || fromSize.height <= 0) return null;
  // Use the smaller scale to preserve aspect ratio and avoid distorting the layout.
  const scale = Math.min(toSize.width / fromSize.width, toSize.height / fromSize.height);
  if (!isFinite(scale) || scale <= 0) return null;
  return Math.min(MAX_VIEW_SCALE, Math.max(MIN_VIEW_SCALE, scale));
}

/**
 * 按容器尺寸差异缩放相机（纯函数，不修改入参）。
 *
 * 注意：配套地，nodePositions 不应被缩放——节点尺寸是固定模型单位（样式里写死的
 * width/height），缩放坐标会改变节点大小与间距的相对关系，导致在不同分辨率/系统
 * 缩放的电脑上载入后节点变“挤”。只缩放相机（pan + zoom），让整个画面按比例映射
 * 到新容器，取景效果与缩放坐标等价，但布局几何保持不变。
 */
export function scaleCameraToContainer(
  camera: CameraState,
  fromSize?: { width: number; height: number },
  toSize?: { width: number; height: number }
): CameraState {
  const scale = computeViewScale(fromSize, toSize);
  if (scale === null) return camera;
  return {
    pan: { x: camera.pan.x * scale, y: camera.pan.y * scale },
    zoom: camera.zoom * scale,
  };
}

export interface IndustrialSnapshotDeps {
  engine?: string;
  selectedFlowIds?: string[];
  selectedIndustries: Industry[];
  selectedCompanies: Company[];
  activeFilters: IndustrialViewState["activeFilters"];
  expandedProcessParents: string[];
  focusState: FocusState;
  hideState: HideState;
  canvasRef: React.RefObject<GraphCameraController | null>;
}

export interface IndustrialRestoreDeps {
  setSelectedIndustries: (industries: Industry[]) => void;
  setSelectedCompanies: (companies: Company[]) => void;
  setSelectedFlowIds: (ids: string[]) => void;
  setActiveFilters: (filters: IndustrialViewState["activeFilters"]) => void;
  setExpandedProcessParents: (ids: string[]) => void;
  setGraphKey: (fn: (k: number) => number) => void;
  setSubgraphData: (data: { nodes: IndustrialNode[]; edges: GraphEdge[] } | undefined) => void;
  setHighlightNodeIds: (ids: string[] | undefined) => void;
  setFocusState: (state: FocusState) => void;
  setHideState: (state: HideState) => void;
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
): Omit<SavedView, "id" | "base" | "viewVersion" | "created_at" | "updated_at" | "version"> {
  const canvas = deps.canvasRef.current;
  const nodePositions = canvas?.getNodePositions();
  const camera = canvas?.getCamera();
  const containerSize = canvas?.getContainerSize();

  return {
    name,
    workspace: "industrial",
    industrial: {
      engine: deps.engine,
      selectedFlowIds: deps.selectedFlowIds ? [...deps.selectedFlowIds] : undefined,
      selectedIndustryIds: deps.selectedIndustries.map((i) => i.industry_id),
      selectedCompanyIds: deps.selectedCompanies.map((c) => c.company_id),
      activeFilters: { ...deps.activeFilters },
      expandedProcessParentIds: [...deps.expandedProcessParents],
      camera: camera ?? { pan: { x: 0, y: 0 }, zoom: 1 },
      nodePositions: nodePositions && Object.keys(nodePositions).length > 0 ? nodePositions : undefined,
      containerSize: containerSize ?? undefined,
      focus: deps.focusState.active
        ? {
            active: deps.focusState.active,
            seedNodeIds: [...deps.focusState.seedNodeIds],
            visibleNodeIds: [...deps.focusState.visibleNodeIds],
            history: deps.focusState.history.map((h) => ({ ...h, addedNodeIds: [...h.addedNodeIds] })),
          }
        : undefined,
      hide: deps.hideState.active
        ? {
            active: deps.hideState.active,
            hiddenNodeIds: [...deps.hideState.hiddenNodeIds],
          }
        : undefined,
    },
  };
}

export function applyIndustrialSnapshot(
  view: SavedView,
  deps: IndustrialRestoreDeps,
  toContainerSize?: { width: number; height: number }
): { restored: boolean; missingIndustryIds: string[]; missingCompanyIds: string[]; engine?: string } {
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
  deps.setSelectedFlowIds([...(state.selectedFlowIds ?? [])]);

  // Restore focus state, filtering out missing node IDs
  if (state.focus?.active) {
    // We don't have direct access to current graph nodes here; the canvas will
    // trim missing IDs on its own when applying focus. We just restore the state.
    deps.setFocusState({
      active: true,
      seedNodeIds: state.focus.seedNodeIds,
      visibleNodeIds: state.focus.visibleNodeIds,
      history: state.focus.history.map((h) => ({
        ...h,
        addedNodeIds: [...h.addedNodeIds],
      })),
    });
  } else {
    deps.setFocusState({
      active: false,
      seedNodeIds: [],
      visibleNodeIds: [],
      history: [],
    });
  }

  // Restore hide state
  if (state.hide?.active) {
    deps.setHideState({
      active: true,
      hiddenNodeIds: [...state.hide.hiddenNodeIds],
    });
  } else {
    deps.setHideState({
      active: false,
      hiddenNodeIds: [],
    });
  }

  // Bump graph key to force canvas re-init with the new merged subgraph / full graph.
  deps.setGraphKey((k) => k + 1);

  // Scale the camera to the current container so the view looks similar across
  // different screen sizes and OS display scaling. Node positions are NOT scaled
  // (see scaleCameraToContainer). Use a copied state so the cached SavedView is
  // never mutated and repeated loads stay idempotent.
  const scaledCamera = scaleCameraToContainer(state.camera, state.containerSize, toContainerSize);
  deps.onSetRestored({ ...state, camera: scaledCamera });

  return {
    restored: true,
    missingIndustryIds,
    missingCompanyIds,
    engine: state.engine,
  };
}

export function buildCompanySnapshot(
  deps: CompanySnapshotDeps,
  name: string
): Omit<SavedView, "id" | "base" | "viewVersion" | "created_at" | "updated_at" | "version"> {
  const canvas = deps.canvasRef?.current;
  const camera = canvas?.getCamera();
  const containerSize = canvas?.getContainerSize();

  return {
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
      containerSize: containerSize ?? undefined,
    },
  };
}

export function applyCompanySnapshot(
  view: SavedView,
  deps: CompanyRestoreDeps,
  toContainerSize?: { width: number; height: number }
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

  // Scale the camera to the current container so the view looks similar across
  // different screen sizes and OS display scaling. Node positions are NOT scaled
  // (see scaleCameraToContainer). Use a copied state so the cached SavedView is
  // never mutated and repeated loads stay idempotent.
  const scaledCamera = scaleCameraToContainer(state.camera, state.containerSize, toContainerSize);
  deps.onSetRestored({ ...state, camera: scaledCamera });

  return { restored: true };
}
