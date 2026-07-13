import { forwardRef, useCallback, useEffect, useImperativeHandle, useRef, useState } from "react";
import cytoscape from "cytoscape";
import dagre from "cytoscape-dagre";
import {
  CONFIDENCE_OPACITY,
  EDGE_NAMESPACE_STYLES,
  ENTITY_TYPE_COLORS,
  GraphEdge,
  IndustrialNode,
} from "@/types";
import { FocusState, FocusStep, HideState } from "@/types/view";
import { getNeighbors, getNode, listEdges, listNodes } from "@/services/api";

cytoscape.use(dagre);

/**
 * =============================================================================
 * 节点/边视觉状态层级说明
 * =============================================================================
 * 下面这套 class/state 优先级从高到低排列。Cytoscape 的样式是“后定义覆盖先
 * 定义”，因此代码里按优先级升序书写，让高优先级样式出现在后面。
 *
 * 1. .hidden
 *    触发：过滤器（entity/status/confidence/edge type）或工艺组折叠。
 *    效果：display: none，彻底不渲染。会覆盖所有其他视觉状态。
 *
 * 2. .connect-source
 *    触发：连线模式（connect mode）第一次点击选中的源节点。
 *    效果：蓝色填充 + 青色粗边框，最醒目的临时态。
 *
 * 3. .highlighted
 *    触发：右键菜单 → 高亮上游/下游/两者。
 *    效果：黄色粗边框 + 黄色阴影（glow）。优先级高于 :selected，保证当前
 *    关注的邻居最显眼。
 *
 * 4. :selected
 *    触发：Cytoscape 原生，单击或框选节点/边。
 *    效果：青色边框。与高亮同时存在时会被高亮的黄色覆盖，但仍然保留选中
 *    逻辑（可 Delete、可作为连线起点等）。
 *
 * 5. .process-group / :parent / .compound-parent
 *    触发：节点有 part_of 子工艺。收起态为 .process-group，展开态成为
 *    compound parent（:parent / .compound-parent）。
 *    效果：琥珀色文件夹样式，展开后变成半透明容器。
 *
 * 6. .external
 *    触发：“顺藤摸瓜”从外部子图拉进来的节点/边。
 *    效果：灰色、半透明，提示用户这不是当前主视图的固有节点。
 *
 * 7. 数据状态
 *    触发：节点自身数据。
 *    效果：entity_type 决定背景色，confidence 决定基础透明度，status 决定
 *    是否被过滤器排除。
 *
 * opacity 统一策略：
 * - 不在 .dimmed / .external 的 class 样式里直接写 opacity，避免与 confidence
 *   的透明度叠加。
 * - 在 base node/edge style 的 opacity 函数中统一计算：
 *   dimmed > external > confidence。
 * - .dimmed 只在“高亮邻居”时使用，表示当前不关注的元素。
 *
 * 注意：.dimmed 与 .highlighted 是互斥的。highlightNeighbors 给目标邻居加
 * .highlighted，其余元素加 .dimmed。
 * =============================================================================
 */

/**
 * 计算一组节点的包围盒中心
 */
function getBoundingBoxCenter(nodes: cytoscape.NodeCollection): cytoscape.Position | null {
  if (nodes.length === 0) return null;
  const bb = nodes.boundingBox({ includeLabels: false, includeOverlays: false });
  return { x: (bb.x1 + bb.x2) / 2, y: (bb.y1 + bb.y2) / 2 };
}

/**
 * 混合布局：
 * 1. 先用 Dagre 对产业流（industrial_flow）做自上而下分层布局；
 * 2. 再对 ontology/is_a 关系做“环绕”修正，把子节点以同心圆方式排在父节点周围。
 *
 * 对已经展开过的复合组（子节点已有分散位置），只把父节点重新居中到子节点
 * 包围盒，不强制把子节点拉成圆。只有首次展开或子节点还堆在一起时，才使用
 * 径向布局。
 */
function layoutExpandedCompound(
  cy: cytoscape.Core,
  parentId: string,
  dragPositions?: Map<string, cytoscape.Position>,
  forceRadial = false
) {
  if (!cy || (cy as unknown as { _private?: { destroyed?: boolean } })._private?.destroyed) return;
  const parent = cy.getElementById(parentId);
  if (parent.length === 0) return;
  const dragPos = dragPositions?.get(parentId);
  const currentCenter = dragPos ? { ...dragPos } : { ...parent.position() };
  const children = parent.children();
  // In focus/hide mode most children may be hidden. Laying them out at the
  // parent center keeps the compound container tight and avoids a giant group
  // box when only one or two children are actually visible.
  const visibleChildren = children.filter((c) => !c.hasClass("hidden"));
  const hiddenChildren = children.filter((c) => c.hasClass("hidden"));
  const count = visibleChildren.length;

  // 判断子节点是否已经有分散的位置：计算可见子节点的包围盒跨度。
  // 如果跨度很小（说明还堆在一起），则使用径向布局；否则保留现有位置。
  let shouldPreserve = false;
  if (count > 0 && !forceRadial) {
    const bb = visibleChildren.boundingBox({ includeLabels: false, includeOverlays: false });
    const spread = Math.max(bb.w, bb.h);
    shouldPreserve = spread > 20;
  }

  if (count > 0) {
    if (shouldPreserve) {
      // 子节点已有布局：保留它们的位置，把父节点移到包围盒中心
      const childCenter = getBoundingBoxCenter(visibleChildren);
      if (childCenter) {
        parent.position(childCenter);
      }
    } else {
      // 首次展开或子节点还堆在一起：使用径向布局
      const radius = Math.max(160, count * 38);
      const angleStep = (2 * Math.PI) / count;
      visibleChildren.forEach((child, index) => {
        const angle = index * angleStep;
        child.position({
          x: currentCenter.x + radius * Math.cos(angle),
          y: currentCenter.y + radius * Math.sin(angle),
        });
      });
      parent.position(currentCenter);
    }
  }
  // Keep hidden children stacked at the parent center so they don't inflate the
  // compound parent's bounding box or pull the camera during focus reveal.
  const finalCenter = parent.position();
  hiddenChildren.forEach((child) => {
    child.position({ x: finalCenter.x, y: finalCenter.y });
  });
  // 把父节点固定到布局中心，防止 Cytoscape 自动把它拉到子节点旧位置
  if (count === 0) {
    parent.position(currentCenter);
  }
}

function runHybridLayout(
  cy: cytoscape.Core,
  fit = true,
  expandedProcessParents: string[] = [],
  dragPositions?: Map<string, cytoscape.Position>,
  onComplete?: () => void,
  parentsToLayout?: string[]
) {
  if (!cy || (cy as unknown as { _private?: { destroyed?: boolean } })._private?.destroyed) {
    onComplete?.();
    return;
  }
  // 如果存在 compound parent（part_of 展开），用简单的径向布局把子工艺排在父节点周围
  // 不依赖 :parent 选择器（隐藏子节点时可能无法命中），直接用 expandedProcessParents 选择父节点
  const expandedParents =
    expandedProcessParents.length > 0
      ? cy.collection().union(
          expandedProcessParents
            .map((id) => cy.getElementById(id))
            .filter((ele) => ele.length > 0)
        )
      : cy.nodes(":parent");
  if (expandedParents.length > 0) {
    // 默认只布局当前发生变化的组；如果调用方没有指定，则回退到所有已展开组（兼容旧行为）
    const layoutParentIds = parentsToLayout ?? expandedProcessParents;
    const targets =
      layoutParentIds.length > 0
        ? layoutParentIds
            .map((id) => cy.getElementById(id))
            .filter((ele) => ele.length > 0)
            .map((ele) => ele.id())
        : expandedParents.map((p) => p.id());
    targets.forEach((parentId) => layoutExpandedCompound(cy, parentId, dragPositions));
    if (fit) {
      // 只 fit 到父节点及其子节点，不要把整个邻域拉进来导致缩放过小
      const fitCollection = expandedParents.union(expandedParents.descendants());
      cy.animate(
        { fit: { eles: fitCollection, padding: 40 } },
        { duration: 250, easing: "ease-in-out-cubic" }
      );
      if (onComplete) {
        setTimeout(() => {
          if (!cy || (cy as unknown as { _private?: { destroyed?: boolean } })._private?.destroyed) return;
          onComplete();
        }, 300);
      }
    } else {
      onComplete?.();
    }
    return;
  }

  // 先把 ontology 边排除在 Dagre 计算之外，避免 is_a/alias 等关系打乱产业流分层
  const ontologyEdges = cy.edges('[edge_namespace = "ontology"]');
  const layoutElements = cy.elements().not(ontologyEdges);

  const dagreLayout = layoutElements.layout({
    name: "dagre",
    rankDir: "TB",
    nodeSep: 40,
    edgeSep: 20,
    rankSep: 80,
    padding: 20,
    fit,
    animate: false,
  } as cytoscape.LayoutOptions);

  dagreLayout.one("layoutstop", () => {
    if (!cy || (cy as unknown as { _private?: { destroyed?: boolean } })._private?.destroyed) {
      onComplete?.();
      return;
    }
    // Dagre 完成后，对 is_a 关系做环绕修正（source 是子类，target 是父类）
    const isAEdges = cy.edges(
      '[edge_namespace = "ontology"][edge_type = "is_a"]'
    );
    if (isAEdges.length === 0) return;

    // 按父节点分组
    const childrenByParent = new Map<string, cytoscape.NodeCollection>();
    isAEdges.forEach((edge) => {
      const parent = edge.target();
      const child = edge.source();
      const key = parent.id();
      const existing = childrenByParent.get(key);
      childrenByParent.set(
        key,
        existing ? existing.union(child) : cy.collection().union(child)
      );
    });

    cy.batch(() => {
      childrenByParent.forEach((children, parentId) => {
        const parent = cy.getElementById(parentId);
        if (!parent || parent.length === 0) return;
        const center = parent.position();
        const count = children.length;
        // 更大的环绕半径，效果更明显
        const radius = Math.max(140, count * 32);
        const angleStep = (2 * Math.PI) / count;
        // 以父节点相对画布中心的角度为起点，不同父节点的环方向不同，减少重叠
        const extent = cy.extent();
        const canvasCenterX = (extent.x1 + extent.x2) / 2;
        const canvasCenterY = (extent.y1 + extent.y2) / 2;
        const startAngle = Math.atan2(
          center.y - canvasCenterY,
          center.x - canvasCenterX
        );

        children.forEach((child, index) => {
          const angle = startAngle + index * angleStep;
          child.position({
            x: center.x + radius * Math.cos(angle),
            y: center.y + radius * Math.sin(angle),
          });
        });
      });
    });

    if (!cy || (cy as unknown as { _private?: { destroyed?: boolean } })._private?.destroyed) {
      onComplete?.();
      return;
    }
    if (fit) {
      cy.fit(cy.elements(), 40);
    }
    if (onComplete) {
      // Allow fit animation to settle before notifying completion
      setTimeout(() => {
        if (!cy || (cy as unknown as { _private?: { destroyed?: boolean } })._private?.destroyed) return;
        onComplete();
      }, fit ? 300 : 0);
    }
  });

  dagreLayout.run();
}

export type EditMode = "default" | "connect";

export interface GraphCanvasRef {
  addNode: (node: IndustrialNode, position?: { x: number; y: number }) => void;
  addEdge: (edge: GraphEdge) => void;
  removeEdge: (edgeId: string) => void;
  removeNode: (nodeId: string) => void;
  updateNode: (node: IndustrialNode) => void;
  updateEdge: (edge: GraphEdge) => void;
  getCamera: () => { pan: { x: number; y: number }; zoom: number } | null;
  setCamera: (camera: { pan: { x: number; y: number }; zoom: number }) => void;
  getNodePositions: () => Record<string, { x: number; y: number }>;
  setNodePositions: (positions: Record<string, { x: number; y: number }>) => void;
  setNodePosition: (nodeId: string, position: { x: number; y: number }) => void;
  getContainerSize: () => { width: number; height: number } | null;
  syncProcessGroups: () => void;
  pullEdgeEndpointsIntoView: (edgeId: string) => void;
  highlightNeighbors: (
    nodeId: string,
    direction: "upstream" | "downstream" | "both"
  ) => void;
  showNeighbors: (nodeId: string, direction: "upstream" | "downstream") => Promise<void>;
  pullNeighborsIntoView: (
    nodeId: string,
    direction: "upstream" | "downstream" | "both"
  ) => void;
  isCompoundGroupNode: (nodeId: string) => boolean;
  getSelectedNodeIds: () => string[];
  clearNodeSelection: () => void;
  autoArrangeSelectedNodes: () => void;
  alignSelectedNodes: (axis: "x" | "y") => void;
  distributeSelectedNodes: (axis: "x" | "y") => void;
  // Focus / reveal mode
  enterFocus: (nodeIds: string[]) => void;
  revealNeighbors: (
    nodeId: string,
    direction: "upstream" | "downstream" | "both",
    depth?: number
  ) => void;
  revealMore: (direction: "upstream" | "downstream" | "both", depth?: number) => void;
  revealInternal: (nodeId: string) => void;
  undoFocus: () => void;
  exitFocus: () => void;
  getFocusState: () => FocusState;
}

interface GraphCanvasProps {
  restoredPositions?: Record<string, { x: number; y: number }>;
  restoredCamera?: { pan: { x: number; y: number }; zoom: number };
  onNodeClick: (node: IndustrialNode) => void;
  onEdgeClick: (edge: GraphEdge) => void;
  onNodeContextMenu?: (node: IndustrialNode, x: number, y: number) => void;
  onEdgeContextMenu?: (edge: GraphEdge, x: number, y: number) => void;
  onMultiNodeContextMenu?: (nodes: IndustrialNode[], x: number, y: number) => void;
  onCanvasContextMenu?: (x: number, y: number) => void;
  onEdgeDelete?: (edge: GraphEdge) => void;
  onClearSelection?: () => void;
  onConnectSourceSelect?: (node: IndustrialNode | null, position?: { x: number; y: number }) => void;
  onConnectTargetSelect?: (node: IndustrialNode, position?: { x: number; y: number }) => void;
  onCancelConnect?: () => void;
  filters: {
    edgeNamespaces: string[];
    edgeTypes: string[];
    entityTypes: string[];
    status: string[];
    confidence: string[];
    showIsA: boolean;
    showPartOf: boolean;
    showWeakOntology: boolean;
    showDerivedFrom?: boolean;
  };
  highlightNodeId?: string;
  highlightNodeIds?: string[];
  sourceData?: { nodes: IndustrialNode[]; edges: GraphEdge[] };
  editMode?: EditMode;
  connectSourceNodeId?: string | null;
  connectTargetNodeId?: string | null;
  expandedProcessParents?: string[];
  onToggleProcessExpansion?: (nodeId: string) => void;
  wheelSensitivity?: number;
  focusState?: FocusState;
  onFocusChange?: (state: FocusState) => void;
  hideState?: HideState;
  onBeforeDragStart?: () => void;
  onBeforeManualLayout?: () => void;
  onBeforeCameraChange?: () => void;
}

function suppressInternalPartOfEdges(
  cy: cytoscape.Core,
  expandedProcessParents: string[] = []
) {
  if (!cy || (cy as unknown as { _private?: { destroyed?: boolean } })._private?.destroyed) return;
  const expandedSet = new Set(expandedProcessParents);
  cy.batch(() => {
    cy.edges('[edge_namespace = "ontology"][edge_type = "part_of"]').forEach((edge) => {
      if (expandedSet.has(edge.target().id())) {
        edge.addClass("hidden");
      }
    });
  });
}

function getChildToParentMap(cy: cytoscape.Core): Map<string, string> {
  const map = new Map<string, string>();
  if (!cy || (cy as unknown as { _private?: { destroyed?: boolean } })._private?.destroyed) return map;
  cy.edges('[edge_namespace = "ontology"][edge_type = "part_of"]').forEach((edge) => {
    map.set(edge.source().id(), edge.target().id());
  });
  return map;
}

function ensureParentsVisible(
  nodeIds: Set<string>,
  childToParent: Map<string, string>
): Set<string> {
  const result = new Set(nodeIds);
  nodeIds.forEach((id) => {
    const parentId = childToParent.get(id);
    if (parentId) result.add(parentId);
  });
  return result;
}

function expandParentsForVisibleNodes(
  visibleNodeIds: string[],
  childToParent: Map<string, string>,
  expandedProcessParents: string[]
): string[] {
  const expandedSet = new Set(expandedProcessParents);
  const parentsToExpand = new Set<string>();
  visibleNodeIds.forEach((id) => {
    const parentId = childToParent.get(id);
    if (parentId && !expandedSet.has(parentId)) {
      parentsToExpand.add(parentId);
    }
  });
  return Array.from(parentsToExpand);
}

function bfsReveal(
  cy: cytoscape.Core,
  currentVisible: Set<string>,
  startIds: string[],
  direction: "upstream" | "downstream" | "both",
  depth: number,
  traverseHiddenEdges = false
): string[] {
  if (!cy || (cy as unknown as { _private?: { destroyed?: boolean } })._private?.destroyed) return [];
  const discovered = new Set<string>();
  let frontier = new Set<string>(startIds.filter((id) => currentVisible.has(id)));

  for (let d = 0; d < depth; d++) {
    const nextFrontier = new Set<string>();
    frontier.forEach((id) => {
      const node = cy.getElementById(id);
      if (node.length === 0) return;

      const connected = node.connectedEdges('[edge_namespace = "industrial_flow"]');
      let edges = cy.collection();
      if (direction === "upstream" || direction === "both") {
        edges = edges.union(connected.filter((e: cytoscape.EdgeSingular) => e.target().id() === id));
      }
      if (direction === "downstream" || direction === "both") {
        edges = edges.union(connected.filter((e: cytoscape.EdgeSingular) => e.source().id() === id));
      }

      edges.forEach((edge: cytoscape.EdgeSingular) => {
        if (!traverseHiddenEdges && (edge.hasClass("hidden") || edge.hasClass("aggregated-edge"))) return;
        const neighborId = edge.source().id() === id ? edge.target().id() : edge.source().id();
        if (!currentVisible.has(neighborId) && !discovered.has(neighborId)) {
          discovered.add(neighborId);
          nextFrontier.add(neighborId);
        }
      });
    });
    if (nextFrontier.size === 0) break;
    frontier = nextFrontier;
  }

  return Array.from(discovered);
}

function applyFilters(
  cy: cytoscape.Core,
  filters: GraphCanvasProps["filters"],
  expandedProcessParents: string[] = [],
  focusState?: FocusState,
  hideState?: HideState
) {
  if (!cy || (cy as unknown as { _private?: { destroyed?: boolean } })._private?.destroyed) return;
  const focusActive = focusState?.active ?? false;
  const focusVisibleSet = focusActive && focusState ? new Set(focusState.visibleNodeIds) : null;
  const hideActive = hideState?.active ?? false;
  const hiddenSet = hideActive && hideState ? new Set(hideState.hiddenNodeIds) : null;
  const entityTypeSet = new Set(filters.entityTypes);
  const statusSet = new Set(filters.status);
  const confidenceSet = new Set(filters.confidence);
  const edgeNsSet = new Set(filters.edgeNamespaces);
  const edgeTypeSet = new Set(filters.edgeTypes);
  const expandedParentSet = new Set(expandedProcessParents);

  // part_of 边：source 是子节点，target 是父节点
  const childToParent = new Map<string, string>();
  cy.edges().forEach((edge) => {
    if (
      edge.data("edge_namespace") === "ontology" &&
      edge.data("edge_type") === "part_of"
    ) {
      childToParent.set(edge.source().id(), edge.target().id());
    }
  });

  cy.batch(() => {
    // 清除上一次折叠产生的聚合边
    cy.edges(".aggregated-edge").remove();

    const visibleNodeIds = new Set<string>();
    let hiddenChildren = cy.collection();

    cy.nodes().forEach((node) => {
      const et = node.data("entity_type");
      const st = node.data("status");
      const cf = node.data("confidence");
      let show =
        (entityTypeSet.size === 0 || entityTypeSet.has(et)) &&
        (statusSet.size === 0 || statusSet.has(st)) &&
        (confidenceSet.size === 0 || confidenceSet.has(cf));
      // Focus mode: only show nodes in the visible set
      if (show && focusVisibleSet) {
        show = focusVisibleSet.has(node.id());
      }
      // Hide mode: hide explicitly hidden nodes
      if (show && hiddenSet) {
        show = !hiddenSet.has(node.id());
      }
      // 如果节点是某个未展开父节点的子工艺，则隐藏
      if (show) {
        const parentId = childToParent.get(node.id());
        if (parentId && !expandedParentSet.has(parentId)) {
          show = false;
          hiddenChildren = hiddenChildren.union(node);
        }
      }
      node.toggleClass("hidden", !show);
      if (show) visibleNodeIds.add(node.id());
    });

    // In focus mode, keep compound parents visible if they have any visible child
    if (focusVisibleSet) {
      cy.nodes().forEach((node) => {
        if (node.hasClass("hidden") && node.isParent()) {
          const hasVisibleChild = node.children().filter((n) => !n.hasClass("hidden")).length > 0;
          if (hasVisibleChild) {
            node.removeClass("hidden");
            visibleNodeIds.add(node.id());
          }
        }
      });
    }

    // 为被折叠的子工艺创建“聚合边”，让外部连接指向父节点，避免上游节点变成孤立点
    if (hiddenChildren.length > 0) {
      hiddenChildren.forEach((child) => {
        const parentId = childToParent.get(child.id());
        if (!parentId) return;
        child.connectedEdges().forEach((edge) => {
          // 跳过 part_of 父子边本身
          if (
            edge.data("edge_namespace") === "ontology" &&
            edge.data("edge_type") === "part_of"
          ) {
            return;
          }
          const other = edge.source().id() === child.id() ? edge.target() : edge.source();
          // 只处理另一端当前可见且不是父节点的边
          if (other.id() === parentId || !visibleNodeIds.has(other.id())) return;

          const isOutgoing = edge.source().id() === child.id();
          const aggSource = isOutgoing ? parentId : other.id();
          const aggTarget = isOutgoing ? other.id() : parentId;
          const aggId = `agg:${edge.id()}`;
          if (cy.getElementById(aggId).length > 0) return;

          cy.add({
            group: "edges",
            data: {
              id: aggId,
              source: aggSource,
              target: aggTarget,
              edge_namespace: edge.data("edge_namespace"),
              edge_type: edge.data("edge_type"),
              label: edge.data("label"),
              aggregated: true,
              original_edge_id: edge.id(),
            },
            classes: "aggregated-edge",
            selectable: false,
            grabbable: false,
          });
        });
      });
    }

    // `related_term` is deprecated but kept here so legacy edges are still hidden by default.
    const weakOntologyTypes = new Set(["alias_of", "related_term", "variant_of"]);
    cy.edges().forEach((edge) => {
      const ns = edge.data("edge_namespace");
      const et = edge.data("edge_type");
      const isIsA = ns === "ontology" && et === "is_a";
      const isPartOf = ns === "ontology" && et === "part_of";
      const isWeakOntology = ns === "ontology" && weakOntologyTypes.has(et);
      // 展开 process group 后，不显示父节点到子节点的 part_of 边，关系已用复合节点表达
      const isInternalPartOf =
        ns === "ontology" &&
        et === "part_of" &&
        expandedParentSet.has(edge.target().id());
      const isDerivedFrom = ns === "industrial_flow" && et === "derived_from";
      const show =
        visibleNodeIds.has(edge.source().id()) &&
        visibleNodeIds.has(edge.target().id()) &&
        (edgeNsSet.size === 0 || edgeNsSet.has(ns)) &&
        (edgeTypeSet.size === 0 || edgeTypeSet.has(et)) &&
        (!isIsA || filters.showIsA) &&
        (!isPartOf || filters.showPartOf) &&
        (!isWeakOntology || filters.showWeakOntology) &&
        (!isDerivedFrom || filters.showDerivedFrom) &&
        !isInternalPartOf;
      edge.toggleClass("hidden", !show);
    });

    // 当边被过滤后，把因此变得孤立的节点也隐藏起来
    // 但展开后的复合父节点（process group）即使没有可见边，也要保留，因为子节点在里面
    // 聚焦模式下，所有显式标记为可见的节点也要保留（即使它们暂时没有可见边）
    cy.nodes().forEach((node) => {
      if (node.hasClass("hidden")) return;
      if (focusActive && focusVisibleSet?.has(node.id())) return;
      const isCompoundParent = node.isParent() || node.hasClass("compound-parent");
      if (isCompoundParent) {
        const hasVisibleChild = node.children().filter((n) => !n.hasClass("hidden")).length > 0;
        if (hasVisibleChild) return;
      }
      const hasVisibleEdge =
        node.connectedEdges().filter((e) => !e.hasClass("hidden")).length > 0;
      if (!hasVisibleEdge) {
        node.addClass("hidden");
      }
    });
  });
}

function syncCompoundParents(
  cy: cytoscape.Core,
  expandedProcessParents: string[],
  dragPositions?: Map<string, cytoscape.Position>,
  parentsToLayout?: string[]
) {
  if (!cy || (cy as unknown as { _private?: { destroyed?: boolean } })._private?.destroyed) return;
  const expandedSet = new Set(expandedProcessParents);
  const childToParent = new Map<string, string>();
  cy.edges('[edge_namespace = "ontology"][edge_type = "part_of"]').forEach(
    (edge) => {
      childToParent.set(edge.source().id(), edge.target().id());
    }
  );
  const parentIds = new Set(childToParent.values());

  // 记录已展开父节点的当前位置，避免 move 子节点后父节点被 Cytoscape 拉回子节点旧位置
  // 优先使用拖拽时记录的渲染位置转换后的模型位置，因为 Cytoscape 对空 compound parent 的 position() 可能不更新
  const savedPositions = new Map<string, cytoscape.Position>();
  expandedProcessParents.forEach((parentId) => {
    const parent = cy.getElementById(parentId);
    if (parent.length === 0) return;
    const dragPos = dragPositions?.get(parentId);
    const chosen = dragPos ? { ...dragPos } : { ...parent.position() };
    savedPositions.set(parentId, chosen);
  });

  cy.batch(() => {
    cy.nodes().forEach((node) => {
      const parentId = childToParent.get(node.id());
      if (!parentId) return;
      const parent = cy.getElementById(parentId);
      if (parent.length === 0) return;

      if (expandedSet.has(parentId)) {
        if (node.data("parent") !== parentId) {
          // 在 move 前先把 hidden 去掉，避免 Cytoscape 在子节点不可见时无法识别 parent
          node.removeClass("hidden");
          node.move({ parent: parentId });
          parent.addClass("compound-parent");
        }
      } else {
        if (node.data("parent")) {
          node.move({ parent: null });
          parent.removeClass("compound-parent");
        }
      }
    });

    // 恢复父节点位置，确保用户拖拽后的位置不变
    savedPositions.forEach((pos, parentId) => {
      cy.getElementById(parentId).position(pos);
    });

    // 只对真正发生变化的组（或调用方明确指定的组）做局部布局。
    // 已经展开的外层组不再被重新径向布局，避免“展开光刻工艺”时把晶圆制造也撑开变乱。
    const layoutTargets = parentsToLayout
      ? parentsToLayout.filter((id) => expandedSet.has(id))
      : Array.from(savedPositions.keys());
    layoutTargets.forEach((parentId) => {
      layoutExpandedCompound(cy, parentId, savedPositions);
    });

    // 给所有拥有 part_of 子工艺的父节点打上“可展开”标记（即使当前收起）
    parentIds.forEach((parentId) => {
      const parent = cy.getElementById(parentId);
      if (parent.length > 0) parent.addClass("process-group");
    });
    cy.nodes(".process-group").forEach((node) => {
      if (!parentIds.has(node.id())) node.removeClass("process-group");
    });
  });
}

export const GraphCanvas = forwardRef<GraphCanvasRef, GraphCanvasProps>(function GraphCanvas(
  {
    onNodeClick,
    onEdgeClick,
    onNodeContextMenu,
    onEdgeContextMenu,
    onMultiNodeContextMenu,
    onCanvasContextMenu,
    onEdgeDelete,
    onClearSelection,
    onConnectSourceSelect,
    onConnectTargetSelect,
    onCancelConnect,
    filters,
    highlightNodeId,
    highlightNodeIds,
    sourceData,
    restoredPositions,
    restoredCamera,
    editMode = "default",
    connectSourceNodeId = null,
    connectTargetNodeId = null,
    expandedProcessParents = [],
    onToggleProcessExpansion,
    wheelSensitivity = 1.0,
    focusState,
    onFocusChange,
    hideState,
    onBeforeDragStart,
    onBeforeManualLayout,
    onBeforeCameraChange,
  },
  ref
) {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<cytoscape.Core | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const onNodeClickRef = useRef(onNodeClick);
  const onEdgeClickRef = useRef(onEdgeClick);
  const onNodeContextMenuRef = useRef(onNodeContextMenu);
  const onEdgeContextMenuRef = useRef(onEdgeContextMenu);
  const onMultiNodeContextMenuRef = useRef(onMultiNodeContextMenu);
  const onCanvasContextMenuRef = useRef(onCanvasContextMenu);
  const selectedNodeIdsRef = useRef<string[]>([]);
  const onEdgeDeleteRef = useRef(onEdgeDelete);
  const onClearSelectionRef = useRef(onClearSelection);
  const onConnectSourceSelectRef = useRef(onConnectSourceSelect);
  const onConnectTargetSelectRef = useRef(onConnectTargetSelect);
  const onCancelConnectRef = useRef(onCancelConnect);
  const filtersRef = useRef(filters);
  const sourceDataRef = useRef(sourceData);
  const editModeRef = useRef(editMode);
  const connectSourceNodeIdRef = useRef(connectSourceNodeId);
  const connectTargetNodeIdRef = useRef(connectTargetNodeId);
  const expandedProcessParentsRef = useRef(expandedProcessParents);
  const prevExpandedProcessParentsRef = useRef<string[]>([]);
  // 恢复已保存视图时，需要跳过 expandedProcessParents effect 触发的自动布局，
  // 否则在初始化完成后该 effect 会立即重新计算 compound group 位置，破坏用户保存的布局。
  const skipLayoutOnExpandForRestoreRef = useRef(false);
  const onToggleProcessExpansionRef = useRef(onToggleProcessExpansion);
  const wheelSensitivityRef = useRef(wheelSensitivity);
  const focusStateRef = useRef(focusState);
  const onFocusChangeRef = useRef(onFocusChange);
  const hideStateRef = useRef(hideState);
  const onBeforeDragStartRef = useRef(onBeforeDragStart);
  const onBeforeManualLayoutRef = useRef(onBeforeManualLayout);
  const onBeforeCameraChangeRef = useRef(onBeforeCameraChange);
  const preDragNodePositionsRef = useRef<Record<string, { x: number; y: number }> | null>(null);
  const dragHistoryPushedRef = useRef(false);

  const processGroupDragPositionsRef = useRef<Map<string, cytoscape.Position>>(new Map());
  const pendingPositionsRef = useRef<Record<string, { x: number; y: number }> | null>(null);
  const pendingCameraRef = useRef<{ pan: { x: number; y: number }; zoom: number } | null>(null);
  const connectSvgRef = useRef<SVGSVGElement | null>(null);
  const connectLineRef = useRef<SVGLineElement | null>(null);
  const connectMousePosRef = useRef<{ x: number; y: number } | null>(null);
  const connectMouseVisibleRef = useRef(true);

  useEffect(() => {
    onNodeClickRef.current = onNodeClick;
  }, [onNodeClick]);

  useEffect(() => {
    onEdgeClickRef.current = onEdgeClick;
  }, [onEdgeClick]);

  useEffect(() => {
    onNodeContextMenuRef.current = onNodeContextMenu;
  }, [onNodeContextMenu]);

  useEffect(() => {
    onMultiNodeContextMenuRef.current = onMultiNodeContextMenu;
  }, [onMultiNodeContextMenu]);

  useEffect(() => {
    filtersRef.current = filters;
  }, [filters]);

  useEffect(() => {
    sourceDataRef.current = sourceData;
  }, [sourceData]);

  useEffect(() => {
    onEdgeContextMenuRef.current = onEdgeContextMenu;
  }, [onEdgeContextMenu]);

  useEffect(() => {
    onCanvasContextMenuRef.current = onCanvasContextMenu;
  }, [onCanvasContextMenu]);

  useEffect(() => {
    onEdgeDeleteRef.current = onEdgeDelete;
  }, [onEdgeDelete]);

  useEffect(() => {
    onClearSelectionRef.current = onClearSelection;
  }, [onClearSelection]);

  useEffect(() => {
    onConnectSourceSelectRef.current = onConnectSourceSelect;
  }, [onConnectSourceSelect]);

  useEffect(() => {
    onConnectTargetSelectRef.current = onConnectTargetSelect;
  }, [onConnectTargetSelect]);

  useEffect(() => {
    onCancelConnectRef.current = onCancelConnect;
  }, [onCancelConnect]);

  useEffect(() => {
    editModeRef.current = editMode;
  }, [editMode]);

  useEffect(() => {
    connectSourceNodeIdRef.current = connectSourceNodeId;
  }, [connectSourceNodeId]);

  useEffect(() => {
    connectTargetNodeIdRef.current = connectTargetNodeId;
  }, [connectTargetNodeId]);

  useEffect(() => {
    expandedProcessParentsRef.current = expandedProcessParents;
  }, [expandedProcessParents]);

  useEffect(() => {
    onToggleProcessExpansionRef.current = onToggleProcessExpansion;
  }, [onToggleProcessExpansion]);

  useEffect(() => {
    wheelSensitivityRef.current = wheelSensitivity;
  }, [wheelSensitivity]);

  useEffect(() => {
    focusStateRef.current = focusState;
  }, [focusState]);

  useEffect(() => {
    onFocusChangeRef.current = onFocusChange;
  }, [onFocusChange]);

  useEffect(() => {
    hideStateRef.current = hideState;
  }, [hideState]);

  useEffect(() => {
    onBeforeDragStartRef.current = onBeforeDragStart;
  }, [onBeforeDragStart]);

  useEffect(() => {
    onBeforeManualLayoutRef.current = onBeforeManualLayout;
  }, [onBeforeManualLayout]);

  useEffect(() => {
    onBeforeCameraChangeRef.current = onBeforeCameraChange;
  }, [onBeforeCameraChange]);

  const applyPendingViewState = useCallback(() => {
    const cy = cyRef.current;
    if (!cy || (cy as unknown as { _private?: { destroyed?: boolean } })._private?.destroyed) return;
    const positions = pendingPositionsRef.current;
    const camera = pendingCameraRef.current;

    if (positions && Object.keys(positions).length > 0) {
      const visibleIds = new Set(cy.nodes().map((n) => n.id()));
      const matched = new Set<string>();
      // 1. 先定位非 compound-parent 节点，让 compound parent 自动根据子节点包围盒居中。
      //    如果直接设置 parent 位置，Cytoscape 会连带平移所有子节点，破坏已保存的子节点布局。
      cy.batch(() => {
        cy.nodes()
          .filter((n) => !n.isParent())
          .forEach((n) => {
            const pos = positions[n.id()];
            if (pos) {
              n.position(pos);
              matched.add(n.id());
            }
          });
      });
      // 2. 对没有可见子节点的 orphan parent，直接应用保存的位置。
      cy.batch(() => {
        cy.nodes()
          .filter((n) => n.isParent() && n.children().length === 0)
          .forEach((n) => {
            const pos = positions[n.id()];
            if (pos) {
              n.position(pos);
              matched.add(n.id());
            }
          });
      });
      const missingRatio = visibleIds.size > 0 ? (visibleIds.size - matched.size) / visibleIds.size : 0;
      // If too many saved positions are missing, fall back to a full relayout.
      if (missingRatio > 0.5) {
        runHybridLayout(cy, true, expandedProcessParentsRef.current, processGroupDragPositionsRef.current);
      }
    }

    if (camera) {
      // Apply camera synchronously; cy.animate with duration 0 does not take effect immediately.
      cy.pan(camera.pan);
      cy.zoom(camera.zoom);
    }

    pendingPositionsRef.current = null;
    pendingCameraRef.current = null;
  }, []);

  useImperativeHandle(ref, () => ({
    addNode: (node, position) => {
      const cy = cyRef.current;
      if (!cy) return;
      const existing = cy.getElementById(node.node_id);
      if (existing.length > 0) {
        if (position) existing.position(position);
        return;
      }
      let pos = position;
      if (!pos) {
        const extent = cy.extent();
        pos = { x: (extent.x1 + extent.x2) / 2, y: (extent.y1 + extent.y2) / 2 };
      }
      cy.add({
        data: {
          id: node.node_id,
          label: node.canonical_name_zh,
          entity_type: node.entity_type,
          status: node.status,
          confidence: node.confidence,
          raw: node,
        },
        position: pos,
      });
      applyFilters(cy, filtersRef.current, expandedProcessParentsRef.current, focusStateRef.current, hideStateRef.current);
      // 新创建的节点即使暂时没有边也要显示出来，避免被过滤器隐藏
      const added = cy.getElementById(node.node_id);
      if (added.length > 0) added.removeClass("hidden");
    },
    addEdge: (edge) => {
      const cy = cyRef.current;
      if (!cy) return;
      if (cy.getElementById(edge.edge_id).length > 0) return;
      const sourceInGraph = cy.getElementById(edge.from_node).length > 0;
      const targetInGraph = cy.getElementById(edge.to_node).length > 0;
      if (!sourceInGraph || !targetInGraph) return;
      cy.add({
        data: {
          id: edge.edge_id,
          source: edge.from_node,
          target: edge.to_node,
          edge_namespace: edge.edge_namespace,
          edge_type: edge.edge_type,
          label: edge.edge_type_label || edge.edge_type,
          raw: edge,
        },
      });
      applyFilters(cy, filtersRef.current, expandedProcessParentsRef.current, focusStateRef.current, hideStateRef.current);
    },
    removeEdge: (edgeId) => {
      const cy = cyRef.current;
      if (!cy) return;
      const el = cy.getElementById(edgeId);
      if (el.length > 0) cy.remove(el);
      applyFilters(cy, filtersRef.current, expandedProcessParentsRef.current, focusStateRef.current, hideStateRef.current);
    },
    removeNode: (nodeId) => {
      const cy = cyRef.current;
      if (!cy) return;
      const el = cy.getElementById(nodeId);
      if (el.length > 0) cy.remove(el);
      applyFilters(cy, filtersRef.current, expandedProcessParentsRef.current, focusStateRef.current, hideStateRef.current);
    },
    updateNode: (node) => {
      const cy = cyRef.current;
      if (!cy) return;
      const el = cy.getElementById(node.node_id);
      if (el.length === 0) return;
      el.data({
        label: node.canonical_name_zh,
        entity_type: node.entity_type,
        status: node.status,
        confidence: node.confidence,
        raw: node,
      });
      applyFilters(cy, filtersRef.current, expandedProcessParentsRef.current, focusStateRef.current, hideStateRef.current);
    },
    updateEdge: (edge) => {
      const cy = cyRef.current;
      if (!cy) return;
      const el = cy.getElementById(edge.edge_id);
      if (el.length === 0) return;
      el.data({
        source: edge.from_node,
        target: edge.to_node,
        edge_namespace: edge.edge_namespace,
        edge_type: edge.edge_type,
        label: edge.edge_type_label || edge.edge_type,
        raw: edge,
      });
      applyFilters(cy, filtersRef.current, expandedProcessParentsRef.current, focusStateRef.current, hideStateRef.current);
    },
    getCamera: () => {
      const cy = cyRef.current;
      if (!cy) return null;
      return { pan: cy.pan(), zoom: cy.zoom() };
    },
    setCamera: (camera) => {
      const cy = cyRef.current;
      if (cy) {
        // Use direct pan/zoom instead of animate({ duration: 0 }) because Cytoscape
        // does not apply the animation synchronously, causing the camera to be lost.
        cy.pan(camera.pan);
        cy.zoom(camera.zoom);
      } else {
        pendingCameraRef.current = camera;
      }
    },
    getNodePositions: () => {
      const cy = cyRef.current;
      if (!cy) return {};
      const positions: Record<string, { x: number; y: number }> = {};
      cy.nodes().forEach((n) => {
        positions[n.id()] = { ...n.position() };
      });
      return positions;
    },
    getContainerSize: () => {
      const el = containerRef.current;
      if (!el) return null;
      return { width: el.clientWidth, height: el.clientHeight };
    },
    setNodePositions: (positions) => {
      const cy = cyRef.current;
      if (cy) {
        pendingPositionsRef.current = positions;
        applyPendingViewState();
      } else {
        pendingPositionsRef.current = positions;
      }
    },
    setNodePosition: (nodeId, position) => {
      const cy = cyRef.current;
      if (!cy) return;
      const node = cy.getElementById(nodeId);
      if (node.length > 0) node.position(position);
    },
    syncProcessGroups: () => {
      const cy = cyRef.current;
      if (!cy) return;
      syncCompoundParents(cy, expandedProcessParentsRef.current, processGroupDragPositionsRef.current, []);
      applyFilters(cy, filtersRef.current, expandedProcessParentsRef.current, focusStateRef.current, hideStateRef.current);
    },
    pullEdgeEndpointsIntoView: (edgeId) => {
      const cy = cyRef.current;
      if (!cy) return;
      const edge = cy.getElementById(edgeId);
      if (!edge || edge.length === 0 || edge.hasClass("aggregated-edge")) return;
      const source = edge.source();
      const target = edge.target();
      if (!source || !target || source.length === 0 || target.length === 0) return;

      const extent = cy.extent();
      const zoom = cy.zoom();
      const marginScreen = 80;
      const marginModel = marginScreen / zoom;
      const minX = extent.x1 + marginModel;
      const maxX = extent.x2 - marginModel;
      const minY = extent.y1 + marginModel;
      const maxY = extent.y2 - marginModel;

      const isVisible = (node: cytoscape.NodeSingular) => {
        const p = node.position();
        return p.x >= minX && p.x <= maxX && p.y >= minY && p.y <= maxY;
      };

      const clampToViewport = (p: cytoscape.Position) => ({
        x: Math.max(minX, Math.min(maxX, p.x)),
        y: Math.max(minY, Math.min(maxY, p.y)),
      });

      const normalize = (p: cytoscape.Position) => {
        const len = Math.sqrt(p.x * p.x + p.y * p.y) || 1;
        return { x: p.x / len, y: p.y / len };
      };

      const sourceVisible = isVisible(source);
      const targetVisible = isVisible(target);
      if (sourceVisible && targetVisible) return;

      const desiredScreenDistance = 200;
      const desiredModelDistance = desiredScreenDistance / zoom;

      if (sourceVisible && !targetVisible) {
        const dir = normalize({
          x: target.position().x - source.position().x,
          y: target.position().y - source.position().y,
        });
        target.animate(
          {
            position: clampToViewport({
              x: source.position().x + dir.x * desiredModelDistance,
              y: source.position().y + dir.y * desiredModelDistance,
            }),
          },
          { duration: 200, easing: "ease-out" }
        );
      } else if (!sourceVisible && targetVisible) {
        const dir = normalize({
          x: source.position().x - target.position().x,
          y: source.position().y - target.position().y,
        });
        source.animate(
          {
            position: clampToViewport({
              x: target.position().x + dir.x * desiredModelDistance,
              y: target.position().y + dir.y * desiredModelDistance,
            }),
          },
          { duration: 200, easing: "ease-out" }
        );
      } else {
        const center = { x: (extent.x1 + extent.x2) / 2, y: (extent.y1 + extent.y2) / 2 };
        const dirSource = normalize({
          x: source.position().x - center.x,
          y: source.position().y - center.y,
        });
        const dirTarget = normalize({
          x: target.position().x - center.x,
          y: target.position().y - center.y,
        });
        source.animate(
          {
            position: clampToViewport({
              x: center.x + dirSource.x * desiredModelDistance,
              y: center.y + dirSource.y * desiredModelDistance,
            }),
          },
          { duration: 200, easing: "ease-out" }
        );
        target.animate(
          {
            position: clampToViewport({
              x: center.x + dirTarget.x * desiredModelDistance,
              y: center.y + dirTarget.y * desiredModelDistance,
            }),
          },
          { duration: 200, easing: "ease-out" }
        );
      }
    },
    highlightNeighbors: (nodeId, direction) => {
      const cy = cyRef.current;
      if (!cy) return;
      const node = cy.getElementById(nodeId);
      if (node.length === 0) return;

      cy.elements().removeClass("highlighted dimmed");

      let edges = cy.collection();
      if (direction === "upstream" || direction === "both") {
        edges = edges.union(node.incomers("edge"));
      }
      if (direction === "downstream" || direction === "both") {
        edges = edges.union(node.outgoers("edge"));
      }
      edges = edges.filter((e: cytoscape.EdgeSingular) => !e.hasClass("aggregated-edge") && !e.hasClass("hidden"));

      const nodes = edges.connectedNodes().filter((n: cytoscape.NodeSingular) => n.id() !== nodeId && !n.hasClass("hidden"));

      node.addClass("highlighted");
      nodes.addClass("highlighted");
      edges.addClass("highlighted");
      cy.elements().not(node).not(nodes).not(edges).addClass("dimmed");
    },
    showNeighbors: async (nodeId, direction) => {
      const cy = cyRef.current;
      if (!cy) return;
      const node = cy.getElementById(nodeId);
      if (node.length === 0) return;

      try {
        const { nodes, edges } = await getNeighbors(nodeId);
        if (!cyRef.current || cyRef.current !== cy) {
          return;
        }
        const nodeIdSet = new Set(cy.nodes().map((n) => n.id()));

        const upstreamNodeIds = new Set<string>();
        const downstreamNodeIds = new Set<string>();
        edges.forEach((e) => {
          // “显示上/下游”只展示产业流关系，避免把工艺组的 part_of 子工序也当作上下游拉出来
          if (e.edge_namespace !== "industrial_flow") return;
          if (e.from_node === nodeId) downstreamNodeIds.add(e.to_node);
          if (e.to_node === nodeId) upstreamNodeIds.add(e.from_node);
        });

        const targetNodeIds = new Set<string>();
        if (direction === "upstream") upstreamNodeIds.forEach((id) => targetNodeIds.add(id));
        if (direction === "downstream") downstreamNodeIds.forEach((id) => targetNodeIds.add(id));

        const centerPos = node.position();
        const candidates = nodes.filter((n) => targetNodeIds.has(n.node_id));
        const radius = Math.max(120, candidates.length * 15);
        const angleStep = candidates.length > 0 ? (2 * Math.PI) / candidates.length : 0;
        let angle = 0;

        cy.batch(() => {
          candidates.forEach((n) => {
            if (!nodeIdSet.has(n.node_id)) {
              cy.add({
                data: {
                  id: n.node_id,
                  label: n.canonical_name_zh,
                  entity_type: n.entity_type,
                  status: n.status,
                  confidence: n.confidence,
                  raw: n,
                },
                classes: "external",
                position: {
                  x: centerPos.x + radius * Math.cos(angle),
                  y: centerPos.y + radius * Math.sin(angle),
                },
              });
              angle += angleStep;
            }
          });

          edges.forEach((e) => {
            if (!cy.getElementById(e.edge_id).length) {
              const sourceInGraph = cy.getElementById(e.from_node).length > 0;
              const targetInGraph = cy.getElementById(e.to_node).length > 0;
              if (sourceInGraph && targetInGraph) {
                const isMatch =
                  (direction === "upstream" && e.to_node === nodeId) ||
                  (direction === "downstream" && e.from_node === nodeId);
                if (isMatch) {
                  cy.add({
                    data: {
                      id: e.edge_id,
                      source: e.from_node,
                      target: e.to_node,
                      edge_namespace: e.edge_namespace,
                      edge_type: e.edge_type,
                      label: e.edge_type_label || e.edge_type,
                      raw: e,
                    },
                    classes: "external",
                  });
                }
              }
            }
          });
        });

        suppressInternalPartOfEdges(cy, expandedProcessParentsRef.current);

        // 高亮刚显示的邻居
        const addedNodes = cy.collection();
        candidates.forEach((n) => {
          const el = cy.getElementById(n.node_id);
          if (el.length) addedNodes.merge(el);
        });
        const addedEdges = node.connectedEdges().filter((e: cytoscape.EdgeSingular) => {
          const other = e.source().id() === nodeId ? e.target() : e.source();
          return addedNodes.has(other);
        });

        cy.elements().removeClass("highlighted dimmed");
        node.addClass("highlighted");
        addedNodes.addClass("highlighted");
        addedEdges.addClass("highlighted");
        cy.elements().not(node).not(addedNodes).not(addedEdges).addClass("dimmed");

        // 把相机 fit 到新拉进来的节点，确保用户能看到效果
        if (addedNodes.length > 0) {
          const fitNodes = addedNodes.union(node);
          cy.animate(
            {
              fit: {
                eles: fitNodes,
                padding: 80,
              },
            },
            { duration: 250, easing: "ease-out" }
          );
        }
      } catch (err) {
        // eslint-disable-next-line no-console
        console.error("showNeighbors failed:", err);
      }
    },
    isCompoundGroupNode: (nodeId) => {
      const cy = cyRef.current;
      if (!cy) return false;
      return (
        cy
          .edges('[edge_namespace = "ontology"][edge_type = "part_of"]')
          .filter((edge) => edge.target().id() === nodeId).length > 0
      );
    },
    getSelectedNodeIds: () => {
      const cy = cyRef.current;
      if (!cy) return [];
      return cy.nodes(":selected").map((n) => n.id());
    },
    clearNodeSelection: () => {
      const cy = cyRef.current;
      if (!cy) return;
      cy.elements().unselect();
    },
    autoArrangeSelectedNodes: () => {
      onBeforeManualLayoutRef.current?.();
      const cy = cyRef.current;
      if (!cy) return;
      const selectedIds = cy.nodes(":selected").map((n) => n.id());
      if (selectedIds.length < 2) return;

      const selectedSet = new Set(selectedIds);
      const nodes = selectedIds
        .map((id) => cy.getElementById(id))
        .filter((n) => n.length > 0 && !n.hasClass("hidden") && !selectedSet.has(n.data("parent")));
      if (nodes.length < 2) return;

      // 软斥力参数：目标间距、刚度、最大单步速度
      const iterations = 120;
      const targetDist = 100;
      const repulsionK = 0.08;
      const centerAttraction = 0.015;
      const anchorK = 0.025;
      const damping = 0.88;
      const maxSpeed = 18;

      const originalPos = new Map<string, { x: number; y: number }>();
      const pos = new Map<string, { x: number; y: number }>();
      const vel = new Map<string, { x: number; y: number }>();
      let centroid = { x: 0, y: 0 };
      nodes.forEach((n) => {
        const p = { ...n.position() };
        originalPos.set(n.id(), p);
        pos.set(n.id(), p);
        vel.set(n.id(), { x: 0, y: 0 });
        centroid.x += p.x;
        centroid.y += p.y;
      });
      centroid.x /= nodes.length;
      centroid.y /= nodes.length;

      // 限制在视口内，留出边距
      const extent = cy.extent();
      const margin = 60;
      const boundMinX = extent.x1 + margin;
      const boundMaxX = extent.x2 - margin;
      const boundMinY = extent.y1 + margin;
      const boundMaxY = extent.y2 - margin;

      for (let i = 0; i < iterations; i++) {
        // 节点间软斥力：只在距离小于目标间距时推开，力度与重叠量成正比
        for (let a = 0; a < nodes.length; a++) {
          for (let b = a + 1; b < nodes.length; b++) {
            const na = nodes[a];
            const nb = nodes[b];
            const pa = pos.get(na.id())!;
            const pb = pos.get(nb.id())!;
            let dx = pa.x - pb.x;
            let dy = pa.y - pb.y;
            let dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < 0.001) {
              const angle = Math.random() * 2 * Math.PI;
              dx = Math.cos(angle);
              dy = Math.sin(angle);
              dist = 0.001;
            }
            if (dist < targetDist) {
              const force = (targetDist - dist) * repulsionK;
              const fx = (dx / dist) * force;
              const fy = (dy / dist) * force;
              const va = vel.get(na.id())!;
              const vb = vel.get(nb.id())!;
              va.x += fx;
              va.y += fy;
              vb.x -= fx;
              vb.y -= fy;
            }
          }
        }

        // 弱中心吸引力 + 锚点弹簧，防止整体漂移并温柔地保持原位置
        nodes.forEach((n) => {
          const p = pos.get(n.id())!;
          const orig = originalPos.get(n.id())!;
          const v = vel.get(n.id())!;
          v.x += (centroid.x - p.x) * centerAttraction;
          v.y += (centroid.y - p.y) * centerAttraction;
          v.x += (orig.x - p.x) * anchorK;
          v.y += (orig.y - p.y) * anchorK;
        });

        // 应用速度并限制最大速度，最后 clamp 到视口
        nodes.forEach((n) => {
          const v = vel.get(n.id())!;
          v.x *= damping;
          v.y *= damping;
          const speed = Math.sqrt(v.x * v.x + v.y * v.y) || 1;
          if (speed > maxSpeed) {
            v.x = (v.x / speed) * maxSpeed;
            v.y = (v.y / speed) * maxSpeed;
          }
          const p = pos.get(n.id())!;
          p.x += v.x;
          p.y += v.y;
          p.x = Math.max(boundMinX, Math.min(boundMaxX, p.x));
          p.y = Math.max(boundMinY, Math.min(boundMaxY, p.y));
        });
      }

      // 动画移动到最终位置，不改变相机
      nodes.forEach((n) => {
        const target = pos.get(n.id())!;
        n.animate({ position: target }, { duration: 300, easing: "ease-out" });
      });
    },
    alignSelectedNodes: (axis) => {
      onBeforeManualLayoutRef.current?.();
      const cy = cyRef.current;
      if (!cy) return;
      const selectedIds = cy.nodes(":selected").map((n) => n.id());
      const nodes = selectedIds
        .map((id) => cy.getElementById(id))
        .filter((n) => n.length > 0 && !n.hasClass("hidden"));
      if (nodes.length < 2) return;

      const positions = nodes.map((n) => n.position());
      if (axis === "x") {
        const avgX = positions.reduce((sum, p) => sum + p.x, 0) / positions.length;
        nodes.forEach((n) => {
          n.animate({ position: { x: avgX, y: n.position().y } }, { duration: 250, easing: "ease-out" });
        });
      } else {
        const avgY = positions.reduce((sum, p) => sum + p.y, 0) / positions.length;
        nodes.forEach((n) => {
          n.animate({ position: { x: n.position().x, y: avgY } }, { duration: 250, easing: "ease-out" });
        });
      }
    },
    distributeSelectedNodes: (axis) => {
      onBeforeManualLayoutRef.current?.();
      const cy = cyRef.current;
      if (!cy) return;
      const selectedIds = cy.nodes(":selected").map((n) => n.id());
      const nodes = selectedIds
        .map((id) => cy.getElementById(id))
        .filter((n) => n.length > 0 && !n.hasClass("hidden"));
      if (nodes.length < 3) return;

      const sorted = nodes.sort((a, b) => {
        return axis === "x" ? a.position().x - b.position().x : a.position().y - b.position().y;
      });
      const firstPos = sorted[0].position();
      const lastPos = sorted[sorted.length - 1].position();

      if (axis === "x") {
        const minX = firstPos.x;
        const maxX = lastPos.x;
        const step = (maxX - minX) / (sorted.length - 1);
        sorted.forEach((n, i) => {
          n.animate({ position: { x: minX + step * i, y: n.position().y } }, { duration: 250, easing: "ease-out" });
        });
      } else {
        const minY = firstPos.y;
        const maxY = lastPos.y;
        const step = (maxY - minY) / (sorted.length - 1);
        sorted.forEach((n, i) => {
          n.animate({ position: { x: n.position().x, y: minY + step * i } }, { duration: 250, easing: "ease-out" });
        });
      }
    },
    pullNeighborsIntoView: (nodeId, direction) => {
      const cy = cyRef.current;
      if (!cy) return;
      const node = cy.getElementById(nodeId);
      if (node.length === 0) return;

      let edges = cy.collection();
      if (direction === "upstream" || direction === "both") {
        edges = edges.union(node.incomers("edge"));
      }
      if (direction === "downstream" || direction === "both") {
        edges = edges.union(node.outgoers("edge"));
      }
      edges = edges.filter((e: cytoscape.EdgeSingular) => !e.hasClass("aggregated-edge") && !e.hasClass("hidden"));

      const neighbors = edges.connectedNodes().filter((n: cytoscape.NodeSingular) => n.id() !== nodeId && !n.hasClass("hidden"));
      if (neighbors.length === 0) return;

      const extent = cy.extent();
      const zoom = cy.zoom();
      const marginScreen = 80;
      const marginModel = marginScreen / zoom;
      const minX = extent.x1 + marginModel;
      const maxX = extent.x2 - marginModel;
      const minY = extent.y1 + marginModel;
      const maxY = extent.y2 - marginModel;

      const isVisible = (p: cytoscape.Position) =>
        p.x >= minX && p.x <= maxX && p.y >= minY && p.y <= maxY;

      const clampToViewport = (p: cytoscape.Position) => ({
        x: Math.max(minX, Math.min(maxX, p.x)),
        y: Math.max(minY, Math.min(maxY, p.y)),
      });

      neighbors.forEach((neighbor) => {
        const p = neighbor.position();
        if (!isVisible(p)) {
          neighbor.animate(
            { position: clampToViewport(p) },
            { duration: 200, easing: "ease-out" }
          );
        }
      });
    },
    // Focus / reveal mode
    enterFocus: (nodeIds) => {
      const cy = cyRef.current;
      if (!cy || nodeIds.length === 0) return;
      const childToParent = getChildToParentMap(cy);
      const visibleSet = ensureParentsVisible(new Set(nodeIds), childToParent);
      const newState: FocusState = {
        active: true,
        seedNodeIds: nodeIds,
        visibleNodeIds: Array.from(visibleSet),
        history: [],
      };
      onFocusChangeRef.current?.(newState);
      // Auto-expand any process group whose child is now visible so the child can be seen
      expandParentsForVisibleNodes(
        newState.visibleNodeIds,
        childToParent,
        expandedProcessParentsRef.current
      ).forEach((parentId) => onToggleProcessExpansionRef.current?.(parentId));
    },
    revealNeighbors: (nodeId, direction, depth = 1) => {
      const cy = cyRef.current;
      if (!cy) return;
      const current = focusStateRef.current;
      if (!current?.active) return;
      const visibleSet = new Set<string>(current.visibleNodeIds);
      const discovered = bfsReveal(cy, visibleSet, [nodeId], direction, depth, true);
      if (discovered.length === 0) return;
      const childToParent = getChildToParentMap(cy);
      const newVisibleSet = ensureParentsVisible(
        new Set<string>([...visibleSet, ...discovered]),
        childToParent
      );
      const step: FocusStep = {
        nodeId,
        direction,
        depthAdded: depth,
        addedNodeIds: discovered,
      };
      const newState: FocusState = {
        active: true,
        seedNodeIds: current.seedNodeIds,
        visibleNodeIds: Array.from(newVisibleSet),
        history: [...current.history, step],
      };
      onFocusChangeRef.current?.(newState);
      expandParentsForVisibleNodes(
        newState.visibleNodeIds,
        childToParent,
        expandedProcessParentsRef.current
      ).forEach((parentId) => onToggleProcessExpansionRef.current?.(parentId));
    },
    revealMore: (direction, depth = 1) => {
      const cy = cyRef.current;
      if (!cy) return;
      const current = focusStateRef.current;
      if (!current?.active) return;
      const visibleSet = new Set<string>(current.visibleNodeIds);
      // Frontier = nodes that were added in the last step, or seeds if no history
      let frontier: string[];
      if (current.history.length > 0) {
        const lastStep = current.history[current.history.length - 1];
        frontier = lastStep.addedNodeIds;
      } else {
        frontier = current.seedNodeIds;
      }
      const discovered = bfsReveal(cy, visibleSet, frontier, direction, depth, true);
      if (discovered.length === 0) return;
      const childToParent = getChildToParentMap(cy);
      const newVisibleSet = ensureParentsVisible(
        new Set<string>([...visibleSet, ...discovered]),
        childToParent
      );
      const step: FocusStep = {
        nodeId: "__multiple__",
        direction,
        depthAdded: depth,
        addedNodeIds: discovered,
      };
      const newState: FocusState = {
        active: true,
        seedNodeIds: current.seedNodeIds,
        visibleNodeIds: Array.from(newVisibleSet),
        history: [...current.history, step],
      };
      onFocusChangeRef.current?.(newState);
      expandParentsForVisibleNodes(
        newState.visibleNodeIds,
        childToParent,
        expandedProcessParentsRef.current
      ).forEach((parentId) => onToggleProcessExpansionRef.current?.(parentId));
    },
    revealInternal: (nodeId) => {
      const cy = cyRef.current;
      if (!cy) return;
      const current = focusStateRef.current;
      if (!current?.active) return;
      const node = cy.getElementById(nodeId);
      if (node.length === 0) return;
      const visibleSet = new Set<string>(current.visibleNodeIds);
      const discovered: string[] = [];
      node.connectedEdges('[edge_namespace = "ontology"][edge_type = "part_of"]').forEach((edge) => {
        if (edge.target().id() === nodeId) {
          const childId = edge.source().id();
          if (!visibleSet.has(childId)) discovered.push(childId);
        }
      });
      if (discovered.length === 0) return;
      const childToParent = getChildToParentMap(cy);
      const newVisibleSet = ensureParentsVisible(
        new Set<string>([...visibleSet, ...discovered]),
        childToParent
      );
      const step: FocusStep = {
        nodeId,
        direction: "both",
        depthAdded: 1,
        addedNodeIds: discovered,
      };
      const newState: FocusState = {
        active: true,
        seedNodeIds: current.seedNodeIds,
        visibleNodeIds: Array.from(newVisibleSet),
        history: [...current.history, step],
      };
      onFocusChangeRef.current?.(newState);
      expandParentsForVisibleNodes(
        newState.visibleNodeIds,
        childToParent,
        expandedProcessParentsRef.current
      ).forEach((parentId) => onToggleProcessExpansionRef.current?.(parentId));
    },
    undoFocus: () => {
      const current = focusStateRef.current;
      if (!current?.active || current.history.length === 0) return;
      const newHistory = current.history.slice(0, -1);
      const removedStep = current.history[current.history.length - 1];
      const removedSet = new Set<string>(removedStep.addedNodeIds);
      const newVisible = current.visibleNodeIds.filter((id: string) => !removedSet.has(id));
      // Also remove any parent that no longer has visible children
      const cy = cyRef.current;
      if (cy) {
        const childToParent = getChildToParentMap(cy);
        const neededParents = new Set<string>();
        newVisible.forEach((id: string) => {
          const parentId = childToParent.get(id);
          if (parentId) neededParents.add(parentId);
        });
        const finalVisible = newVisible.filter((id: string) => {
          if (!neededParents.has(id)) return true;
          // It's a parent; keep only if it has a visible child
          return newVisible.some((childId: string) => childToParent.get(childId) === id);
        });
        const newState: FocusState = {
          active: finalVisible.length > 0,
          seedNodeIds: current.seedNodeIds,
          visibleNodeIds: finalVisible,
          history: newHistory,
        };
        onFocusChangeRef.current?.(newState);
      } else {
        const newState: FocusState = {
          active: newVisible.length > 0,
          seedNodeIds: current.seedNodeIds,
          visibleNodeIds: newVisible,
          history: newHistory,
        };
        onFocusChangeRef.current?.(newState);
      }
    },
    exitFocus: () => {
      const current = focusStateRef.current;
      if (!current?.active) return;
      const newState: FocusState = {
        active: false,
        seedNodeIds: [],
        visibleNodeIds: [],
        history: [],
      };
      onFocusChangeRef.current?.(newState);
    },
    getFocusState: () => {
      return (
        focusStateRef.current ?? {
          active: false,
          seedNodeIds: [],
          visibleNodeIds: [],
          history: [],
        }
      );
    },
  }));

  // Initial load — only once
  useEffect(() => {
    let mounted = true;
    let keyHandler: ((e: KeyboardEvent) => void) | undefined;
    let cleanupPanHandlers: (() => void) | null = null;

    function setupPanHandlers(cy: cytoscape.Core, containerEl: HTMLElement) {
      const isInputTarget = (target: EventTarget | null) => {
        if (!(target instanceof HTMLElement)) return false;
        return (
          target.tagName === "INPUT" ||
          target.tagName === "TEXTAREA" ||
          target.isContentEditable
        );
      };

      // 统一在此处控制平移方向和幅度；1 表示内容跟随鼠标移动，-1 表示视口跟随鼠标移动
      const PAN_DIRECTION = 1;
      const PAN_SENSITIVITY = 1.0;

      let panModifierDown = false;
      let middlePanActive = false;
      let modifierPanActive = false;
      let lastPointer: { x: number; y: number } | null = null;

      const updatePanModifier = (down: boolean) => {
        if (down === panModifierDown) return;
        panModifierDown = down;
        if (down) {
          cy.autoungrabify(true);
          cy.boxSelectionEnabled(false);
          containerEl.classList.add("canvas-pan-modifier");
        } else {
          cy.autoungrabify(false);
          cy.boxSelectionEnabled(true);
          containerEl.classList.remove("canvas-pan-modifier");
        }
      };

      const startPan = (e: PointerEvent) => {
        markCameraChangeStart();
        lastPointer = { x: e.clientX, y: e.clientY };
        try {
          containerEl.setPointerCapture(e.pointerId);
        } catch {
          // ignore
        }
      };

      // 视图历史：标记当前是否已在本次相机手势中 push 过
      let cameraPushedForGesture = false;
      let wheelGestureTimer: number | null = null;
      const markCameraChangeStart = () => {
        if (!cameraPushedForGesture) {
          onBeforeCameraChangeRef.current?.();
          cameraPushedForGesture = true;
        }
        if (wheelGestureTimer) window.clearTimeout(wheelGestureTimer);
        wheelGestureTimer = window.setTimeout(() => {
          wheelGestureTimer = null;
          cameraPushedForGesture = false;
        }, 300);
      };

      const doPan = (e: PointerEvent) => {
        if (!lastPointer) return;
        e.preventDefault();
        const dx = e.clientX - lastPointer.x;
        const dy = e.clientY - lastPointer.y;
        const panX = dx * PAN_DIRECTION * PAN_SENSITIVITY;
        const panY = dy * PAN_DIRECTION * PAN_SENSITIVITY;
        cy.panBy({ x: panX, y: panY });
        lastPointer = { x: e.clientX, y: e.clientY };
      };

      const endPan = (e: PointerEvent) => {
        lastPointer = null;
        cameraPushedForGesture = false;
        try {
          containerEl.releasePointerCapture(e.pointerId);
        } catch {
          // ignore
        }
      };

      const handlePanKeyDown = (e: KeyboardEvent) => {
        if (isInputTarget(e.target)) return;
        if (e.ctrlKey || e.metaKey) updatePanModifier(true);
      };
      const handlePanKeyUp = (e: KeyboardEvent) => {
        if (!(e.ctrlKey || e.metaKey) && !modifierPanActive) updatePanModifier(false);
      };
      const handleWindowBlur = () => {
        modifierPanActive = false;
        middlePanActive = false;
        updatePanModifier(false);
        containerEl.classList.remove("canvas-middle-panning");
      };

      const handlePointerDown = (e: PointerEvent) => {
        if (e.button === 1) {
          e.preventDefault();
          e.stopImmediatePropagation();
          middlePanActive = true;
          containerEl.classList.add("canvas-middle-panning");
          startPan(e);
          return;
        }
        if (e.button === 0 && (e.ctrlKey || e.metaKey)) {
          e.preventDefault();
          e.stopImmediatePropagation();
          modifierPanActive = true;
          updatePanModifier(true);
          startPan(e);
          return;
        }
      };
      const handlePointerMove = (e: PointerEvent) => {
        if (!lastPointer) return;
        if (!middlePanActive && !modifierPanActive) return;
        doPan(e);
      };
      const handlePointerUp = (e: PointerEvent) => {
        if (middlePanActive) {
          middlePanActive = false;
          containerEl.classList.remove("canvas-middle-panning");
          endPan(e);
        }
        if (modifierPanActive) {
          modifierPanActive = false;
          endPan(e);
          if (!(e.ctrlKey || e.metaKey)) {
            updatePanModifier(false);
          }
        }
      };

      const handleWheel = (e: WheelEvent) => {
        if (isInputTarget(e.target)) return;
        // 阻止页面滚动，并阻止 Cytoscape 内置 wheel handler（它要求 userPanningEnabled 才缩放）
        e.preventDefault();
        e.stopPropagation();

        if (!cy.zoomingEnabled() || !cy.userZoomingEnabled()) return;
        if (e.deltaY === 0) return;

        try {
          const renderer = (cy as unknown as { renderer?: () => { projectIntoViewport: (x: number, y: number) => [number, number] } }).renderer?.();
          if (!renderer) return;

          const zoom = cy.zoom();
          const pan = cy.pan();
          const pos = renderer.projectIntoViewport(e.clientX, e.clientY);
          const rpos = {
            x: pos[0] * zoom + pan.x,
            y: pos[1] * zoom + pan.y,
          };

          const sensitivity = wheelSensitivityRef.current;
          const diff = (e.deltaY / -250) * sensitivity;
          let newZoom = zoom * Math.pow(10, diff);
          newZoom = Math.max(cy.minZoom(), Math.min(cy.maxZoom(), newZoom));

          markCameraChangeStart();
          cy.zoom({ level: newZoom, renderedPosition: rpos });
        } catch (err) {
          // eslint-disable-next-line no-console
          console.error("[GraphCanvas] wheel zoom failed", err);
        }
      };

      const handleContextMenu = (e: MouseEvent) => {
        // 只在画布容器内拦截右键菜单
        if (!containerEl.contains(e.target as Node)) return;
        if (isInputTarget(e.target)) return;
        e.preventDefault();
        e.stopPropagation();

        try {
          const renderer = (cy as unknown as { renderer?: () => { projectIntoViewport: (x: number, y: number) => [number, number]; findNearestElement: (x: number, y: number, interactiveOnly?: boolean, isTouch?: boolean) => cytoscape.SingularElementReturnValue | null } }).renderer?.();
          if (!renderer) return;

          const pos = renderer.projectIntoViewport(e.clientX, e.clientY);
          const near = renderer.findNearestElement(pos[0], pos[1], true, false) as any;

          const selectedNodeIds = selectedNodeIdsRef.current;
          if (selectedNodeIds.length >= 2) {
            const selectedNodes = selectedNodeIds
              .map((id) => cy.getElementById(id).data("raw") as IndustrialNode | undefined)
              .filter((n): n is IndustrialNode => !!n);
            onMultiNodeContextMenuRef.current?.(selectedNodes, e.clientX, e.clientY);
          } else if (near && near.isNode()) {
            const rawData = near.data("raw") as IndustrialNode;
            onNodeContextMenuRef.current?.(rawData, e.clientX, e.clientY);
          } else if (near && near.isEdge()) {
            if (!near.hasClass("aggregated-edge")) {
              const rawData = near.data("raw") as GraphEdge;
              onEdgeContextMenuRef.current?.(rawData, e.clientX, e.clientY);
            }
          } else {
            onCanvasContextMenuRef.current?.(e.clientX, e.clientY);
          }
        } catch (err) {
          // eslint-disable-next-line no-console
          console.error("[GraphCanvas] contextmenu hit-test failed", err);
        }
      };

      window.addEventListener("keydown", handlePanKeyDown);
      window.addEventListener("keyup", handlePanKeyUp);
      window.addEventListener("blur", handleWindowBlur);
      containerEl.addEventListener("pointerdown", handlePointerDown, true);
      containerEl.addEventListener("pointermove", handlePointerMove);
      containerEl.addEventListener("pointerup", handlePointerUp);
      containerEl.addEventListener("pointercancel", handlePointerUp);
      containerEl.addEventListener("wheel", handleWheel, { passive: false, capture: true });
      document.addEventListener("contextmenu", handleContextMenu, true);

      return () => {
        window.removeEventListener("keydown", handlePanKeyDown);
        window.removeEventListener("keyup", handlePanKeyUp);
        window.removeEventListener("blur", handleWindowBlur);
        containerEl.removeEventListener("pointerdown", handlePointerDown, true);
        containerEl.removeEventListener("pointermove", handlePointerMove);
        containerEl.removeEventListener("pointerup", handlePointerUp);
        containerEl.removeEventListener("pointercancel", handlePointerUp);
        containerEl.removeEventListener("wheel", handleWheel, { capture: true });
        document.removeEventListener("contextmenu", handleContextMenu, true);
        containerEl.classList.remove("canvas-pan-modifier", "canvas-middle-panning");
        if (wheelGestureTimer) window.clearTimeout(wheelGestureTimer);
      };
    }

    async function init() {
      try {
        setLoading(true);
        let nodesData: { items: IndustrialNode[] };
        let edgesData: { items: GraphEdge[] };
        if (sourceData) {
          nodesData = { items: sourceData.nodes };
          edgesData = { items: sourceData.edges };
        } else {
          [nodesData, edgesData] = await Promise.all([
            listNodes(1, 1000),
            listEdges(1, 1000),
          ]);
        }
        if (!mounted) return;
        if (!containerRef.current) return;

        const nodeIdSet = new Set(nodesData.items.map((n) => n.node_id));
        const validEdges = edgesData.items.filter((e) => {
          const ok = nodeIdSet.has(e.from_node) && nodeIdSet.has(e.to_node);
          if (!ok) {
            // eslint-disable-next-line no-console
            console.warn(
              `Skipping edge \`${e.edge_id}\`: source or target node not in loaded node set`
            );
          }
          return ok;
        });
        const skippedEdges = edgesData.items.length - validEdges.length;
        if (skippedEdges > 0) {
          // eslint-disable-next-line no-console
          console.warn(
            `${skippedEdges} edge(s) skipped because their endpoint nodes were not loaded (increase page_size or implement full pagination)`
          );
        }

        const cy = cytoscape({
          container: containerRef.current,
          elements: [
            ...nodesData.items.map((n) => ({
              data: {
                id: n.node_id,
                label: n.canonical_name_zh,
                entity_type: n.entity_type,
                status: n.status,
                confidence: n.confidence,
                raw: n,
              },
            })),
            ...validEdges.map((e) => ({
              data: {
                id: e.edge_id,
                source: e.from_node,
                target: e.to_node,
                edge_namespace: e.edge_namespace,
                edge_type: e.edge_type,
                label: e.edge_type_label || e.edge_type,
                raw: e,
              },
            })),
          ],
          style: [
            // 7. 数据状态：entity_type / confidence / edge_namespace
            {
              selector: "node",
              style: {
                "background-color": (ele: cytoscape.NodeSingular) =>
                  ENTITY_TYPE_COLORS[ele.data("entity_type") as keyof typeof ENTITY_TYPE_COLORS] || "#64748b",
                "border-width": 2,
                "border-color": "#1e293b",
                width: 28,
                height: 28,
                label: "data(label)",
                "font-size": "10px",
                "text-valign": "bottom",
                "text-halign": "center",
                "text-margin-y": 4,
                color: "#cbd5e1",
                "text-background-color": "#0f172a",
                "text-background-opacity": 0.85,
                "text-background-padding": "2px 4px",
                "text-background-shape": "roundrectangle",
                opacity: (ele: cytoscape.NodeSingular) => {
                  if (ele.hasClass("dimmed")) return 0.15;
                  if (ele.hasClass("external")) return 0.35;
                  return CONFIDENCE_OPACITY[ele.data("confidence") as keyof typeof CONFIDENCE_OPACITY] || 0.5;
                },
              },
            },
            {
              selector: "edge",
              style: {
                selectable: false,
                "line-color": (ele: cytoscape.EdgeSingular) =>
                  EDGE_NAMESPACE_STYLES[ele.data("edge_namespace") as keyof typeof EDGE_NAMESPACE_STYLES]?.color || "#94a3b8",
                "target-arrow-color": (ele: cytoscape.EdgeSingular) =>
                  EDGE_NAMESPACE_STYLES[ele.data("edge_namespace") as keyof typeof EDGE_NAMESPACE_STYLES]?.color || "#94a3b8",
                "target-arrow-shape": "triangle",
                "arrow-scale": 0.8,
                width: 1.5,
                "curve-style": "bezier",
                "line-style": (ele: cytoscape.EdgeSingular) =>
                  (EDGE_NAMESPACE_STYLES[ele.data("edge_namespace") as keyof typeof EDGE_NAMESPACE_STYLES]?.lineStyle || "solid") as cytoscape.Css.LineStyle,
                label: "data(label)",
                "font-size": "8px",
                color: "#94a3b8",
                "text-background-color": "#0f172a",
                "text-background-opacity": 0.85,
                "text-background-padding": "1px 3px",
                "text-rotation": "autorotate",
                "text-margin-y": -6,
                opacity: (ele: cytoscape.EdgeSingular) => {
                  if (ele.hasClass("dimmed")) return 0.15;
                  if (ele.hasClass("external")) return 0.35;
                  if (ele.hasClass("aggregated-edge")) return 0.65;
                  return 1;
                },
              },
            },
            // adopts 边（Usage -> general process/technology）：弱化显示，避免和主产业流混淆
            {
              selector: 'edge[edge_type = "adopts"]',
              style: {
                width: 1,
                "line-style": "dotted",
                "line-color": "#64748b",
                "target-arrow-color": "#64748b",
                color: "#64748b",
                "font-size": "7px",
                opacity: 0.45,
              },
            },
            // 6. external（顺藤摸瓜拉入的外部节点/边）
            {
              selector: ".external",
              style: {
                "background-color": "#475569",
                "line-color": "#475569",
                "target-arrow-color": "#475569",
                color: "#475569",
                "text-background-color": "#0f172a",
              },
            },
            // 5. aggregated-edge（工艺组折叠时的代理边）
            {
              selector: ".aggregated-edge",
              style: {
                "line-style": "dashed",
                width: 1,
                "target-arrow-shape": "triangle",
                "arrow-scale": 0.6,
              },
            },
            // 5. process-group（可展开工艺组，收起态）
            {
              selector: ".process-group",
              style: {
                shape: "round-rectangle",
                width: 46,
                height: 46,
                "background-opacity": 0.35,
                "background-color": "#fbbf24",
                "border-color": "#78350f",
                "border-width": 3,
                "border-opacity": 0.95,
                "border-style": "solid",
                color: "#fef3c7",
                "font-weight": "bold",
                label: (ele: cytoscape.NodeSingular) => `📁 ${ele.data("label") || ele.id()}`,
                "text-background-color": "#451a03",
                "text-background-opacity": 0.9,
                "text-background-padding": "2px 6px",
                "text-background-shape": "roundrectangle",
              },
            },
            // 5. compound-parent（工艺组展开态）
            {
              selector: ":parent, .compound-parent",
              style: {
                "background-opacity": 0.22,
                "border-width": 3,
                "border-opacity": 0.95,
                "padding-top": "28px",
                "padding-bottom": "24px",
                "padding-left": "24px",
                "padding-right": "24px",
                "min-width": "160px",
                "min-height": "160px",
                "text-valign": "top",
                "text-halign": "center",
                "text-margin-y": 10,
                "font-size": "12px",
                label: (ele: cytoscape.NodeSingular) => `📁 ${ele.data("label") || ele.id()}`,
              },
            },
            // 4. selected（Cytoscape 原生选中）
            {
              selector: ":selected",
              style: {
                "border-color": "#22d3ee",
                "border-width": 3,
                "line-color": "#22d3ee",
                "target-arrow-color": "#22d3ee",
              },
            },
            // 3. highlighted（高亮上游/下游）
            {
              selector: "node.highlighted",
              style: {
                "border-color": "#facc15",
                "border-width": 5,
                width: 38,
                height: 38,
                color: "#facc15",
                "text-background-color": "#422006",
                "text-background-opacity": 0.95,
                "text-background-padding": "3px 6px",
                opacity: 1,
                // Cytoscape 运行支持 shadow-*，但 @types/cytoscape 未包含这些属性
                "shadow-blur": 12,
                "shadow-color": "#facc15",
                "shadow-opacity": 0.8,
              } as any,
            },
            {
              selector: "edge.highlighted",
              style: {
                "line-color": "#facc15",
                "target-arrow-color": "#facc15",
                color: "#facc15",
                width: 3,
                "text-background-color": "#422006",
                "text-background-opacity": 0.95,
                "text-background-padding": "2px 4px",
                opacity: 1,
                "shadow-blur": 8,
                "shadow-color": "#facc15",
                "shadow-opacity": 0.6,
              } as any,
            },
            // 2. connect-source（连线模式源节点）
            {
              selector: ".connect-source",
              style: {
                "border-color": "#22d3ee",
                "border-width": 4,
                "background-color": "#0ea5e9",
                color: "#e0f2fe",
                "text-background-color": "#0c4a6e",
              },
            },
            // 1. hidden（最高优先级：彻底不显示）
            {
              selector: ".hidden",
              style: {
                display: "none",
              },
            },
          ],
          // 初始不启用默认 dagre，改为在数据加载后执行混合布局
          layout: { name: "preset" } as cytoscape.LayoutOptions,
          wheelSensitivity: 0.1,
          minZoom: 0.2,
          maxZoom: 3,
          userPanningEnabled: false,
          boxSelectionEnabled: true,
          selectionType: "additive",
        });

        // ==========================================
        // 1. 节点单击事件：预览 (Peek) 与顺藤摸瓜 (Auto-Pin)
        // ==========================================
        cy.on("tap", "node", async (evt) => {
          const node = evt.target;
          const rawData = node.data("raw") as IndustrialNode;

          // 非修饰键单击时，只保留当前节点为单选，保持单选体验
          const originalEvent = evt.originalEvent as MouseEvent;
          const modifier = originalEvent.ctrlKey || originalEvent.metaKey || originalEvent.shiftKey;
          if (!modifier) {
            cy.elements().unselect();
            node.select();
          }

          // 连线模式：第一次点击选起点，第二次点击选终点
          if (editModeRef.current === "connect") {
            const sourceId = connectSourceNodeIdRef.current;
            const clickPos = {
              x: (evt.originalEvent as MouseEvent).clientX,
              y: (evt.originalEvent as MouseEvent).clientY,
            };
            if (!sourceId) {
              onConnectSourceSelectRef.current?.(rawData, clickPos);
            } else if (sourceId === node.id()) {
              onConnectSourceSelectRef.current?.(null);
            } else {
              onConnectTargetSelectRef.current?.(rawData, clickPos);
            }
            return;
          }

          onNodeClickRef.current(rawData);

          // 仅在存在源数据(子图模式)时，开启探索视野功能
          if (sourceDataRef.current) {
            try {
              // 【设计理由: 顺藤摸瓜与防孤岛】
              // 如果用户点击了一个半透明(external)的预览节点，说明他对此路径感兴趣。
              // 我们在此刻将该节点及其与主图相连的边 "转正" (固化)，防止后续清理时断链产生孤岛。
              if (node.hasClass("external")) {
                node.removeClass("external");
                node.connectedEdges().forEach((edge: cytoscape.EdgeSingular) => {
                  const source = edge.source();
                  const target = edge.target();
                  // 如果边的两端有任何一端是实体节点(转正节点)，说明这是一条有效通路，将边也转正
                  if (!source.hasClass("external") || !target.hasClass("external")) {
                    edge.removeClass("external");
                  }
                });
              }

              const nodeId = node.id();
              const { nodes, edges } = await getNeighbors(nodeId);

              // 【设计理由: 保持视野清晰】
              // 每次新的单击预览，都会清理掉之前没有被固化的半透明节点，防止画面被杂乱的虚线填满。
              // 注意：因为上面的 Auto-Pin 逻辑，当前点击的节点如果原本是 external，已经被转正了，所以这里不会误杀它。
              cy.elements(".external").remove();

              // 必须在清理完旧 external 之后再计算 existingIds，防止共用节点被排除。
              const existingIds = new Set(cy.nodes().map((n) => n.id()));

              // 【设计理由: 环状局部布局 (Radial Layout)】
              // 为了不触发全局重排(会致使画面剧烈跳动)，我们将新节点以环状均匀分布在被点击节点的周围。
              const centerPos = node.position();
              const radius = Math.max(120, nodes.length * 15); // 根据节点数量动态调整半径，防止拥挤
              let angle = 0;
              const angleStep = nodes.length > 0 ? (2 * Math.PI) / nodes.length : 0;

              cy.batch(() => {
                // 渲染邻居节点
                nodes.forEach((n) => {
                  if (!existingIds.has(n.node_id)) {
                    cy.add({
                      data: {
                        id: n.node_id,
                        label: n.canonical_name_zh,
                        entity_type: n.entity_type,
                        status: n.status,
                        confidence: n.confidence,
                        raw: n,
                      },
                      classes: "external", // 标记为半透明预览节点
                      position: {
                        x: centerPos.x + radius * Math.cos(angle),
                        y: centerPos.y + radius * Math.sin(angle),
                      },
                    });
                    angle += angleStep;
                  }
                });

                // 渲染连接边
                edges.forEach((e) => {
                  if (!cy.getElementById(e.edge_id).length) {
                    const sourceInGraph = cy.getElementById(e.from_node).length > 0;
                    const targetInGraph = cy.getElementById(e.to_node).length > 0;
                    // 只有边的两端节点都在画布上时，才渲染这条边
                    if (sourceInGraph && targetInGraph) {
                      cy.add({
                        data: {
                          id: e.edge_id,
                          source: e.from_node,
                          target: e.to_node,
                          edge_namespace: e.edge_namespace,
                          edge_type: e.edge_type,
                          label: e.edge_type_label || e.edge_type,
                          raw: e,
                        },
                        classes: "external",
                      });
                    }
                  }
                });
              });

              // 预览边也要遵守“展开后的 process group 内部不显示 part_of 线”
              suppressInternalPartOfEdges(cy, expandedProcessParentsRef.current);
            } catch (err) {
              console.error("Show external neighbors failed:", err);
            }
          }
        });

        // ==========================================
        // 2. 边单击事件：单纯透传数据
        // ==========================================
        cy.on("tap", "edge", (evt) => {
          const edge = evt.target;
          if (edge.hasClass("aggregated-edge")) return;
          onEdgeClickRef.current(edge.data("raw") as GraphEdge);
        });

        // ==========================================
        // 3. 画布空白处单击事件：重置图谱状态 / 取消连线
        // ==========================================
        cy.on("tap", (evt) => {
          if (evt.target === cy) {
            // 连线模式下点空白处取消当前选中的起点
            if (editModeRef.current === "connect" && connectSourceNodeIdRef.current) {
              onConnectSourceSelectRef.current?.(null);
            }
            // 【设计理由: 提供安全的撤退路径】
            // 点空白处取消所有选择、高亮，并清理掉所有临时的半透明预览节点
            cy.elements().unselect();
            cy.elements().removeClass("highlighted dimmed");
            cy.elements(".external").remove();
            onClearSelectionRef.current?.();
          }
        });

        // ==========================================
        // 3.5 框选与多选状态跟踪
        // ==========================================
        // 框选只选节点、不选边（edge style 已设 selectable: false）
        const updateSelectedNodeIds = () => {
          selectedNodeIdsRef.current = cy.nodes(":selected").map((n) => n.id());
        };
        cy.on("select", "node", updateSelectedNodeIds);
        cy.on("unselect", "node", updateSelectedNodeIds);
        cy.on("boxend", updateSelectedNodeIds);

        // ==========================================
        // 3.6 右键菜单事件：节点 / 边 / 空白画布
        // ==========================================
        // 右键菜单统一由原生 document contextmenu 事件处理，不再依赖 Cytoscape cxttap

        // 记录 process-group 节点被拖拽后的实际渲染位置，因为空 compound parent 的 position() 可能不更新
        cy.on("dragfree", "node.process-group", (evt) => {
          const node = evt.target;
          const rendered = node.renderedPosition();
          const pan = cy.pan();
          const zoom = cy.zoom();
          const modelPos = {
            x: (rendered.x - pan.x) / zoom,
            y: (rendered.y - pan.y) / zoom,
          };
          processGroupDragPositionsRef.current.set(node.id(), modelPos);
          // eslint-disable-next-line no-console
          console.log("[dragfree] node:", node.id(), "rendered:", rendered, "pan:", pan, "zoom:", zoom, "modelPos:", modelPos);
        });

        // 视图历史：在节点被 grab 时保存当前状态（上一状态）。
        // 多选拖拽时 grab 会对每个节点触发，用 dragHistoryPushedRef 保证同一个手势只入栈一次。
        cy.on("grab", "node", () => {
          const positions: Record<string, { x: number; y: number }> = {};
          cy.nodes().forEach((n) => {
            positions[n.id()] = { ...n.position() };
          });
          preDragNodePositionsRef.current = positions;
          if (!dragHistoryPushedRef.current) {
            dragHistoryPushedRef.current = true;
            onBeforeDragStartRef.current?.();
          }
        });
        cy.on("dragfree", "node", () => {
          preDragNodePositionsRef.current = null;
          if (cy.nodes(":grabbed").length === 0) {
            dragHistoryPushedRef.current = false;
          }
        });

        // ==========================================
        // 4. 节点双击事件：展开、完全固化与重排
        // ==========================================
        // 在嵌套 compound 组中，双击应命中光标下最内层的可展开工艺组，
        // 而不是最外层。这里用渲染坐标下的 bounding box 做精确命中测试。
        const resolveInnermostProcessParentAt = (
          clickRendered: cytoscape.Position
        ): cytoscape.NodeSingular | null => {
          const partOfEdges = cy.edges('[edge_namespace = "ontology"][edge_type = "part_of"]');
          const expandable = cy.nodes().filter((n) => {
            const nid = n.id();
            return partOfEdges.toArray().some((edge) => (edge as cytoscape.EdgeSingular).target().id() === nid);
          });
          const containing = expandable.filter((n) => {
            const bb = n.renderedBoundingBox({ includeLabels: false, includeOverlays: false });
            return (
              clickRendered.x >= bb.x1 &&
              clickRendered.x <= bb.x2 &&
              clickRendered.y >= bb.y1 &&
              clickRendered.y <= bb.y2
            );
          });
          if (containing.length === 0) return null;
          // 面积越小越内层
          const area = (n: cytoscape.NodeSingular) => {
            const bb = n.renderedBoundingBox({ includeLabels: false, includeOverlays: false });
            return (bb.x2 - bb.x1) * (bb.y2 - bb.y1);
          };
          const sorted = containing.sort((a: cytoscape.NodeSingular, b: cytoscape.NodeSingular) => area(a) - area(b));
          return sorted[0];
        };

        cy.on("dbltap", "node", async (evt) => {
          const clickRendered = evt.renderedPosition;
          const innermost = resolveInnermostProcessParentAt(clickRendered);
          const node = innermost ?? evt.target;
          const nodeId = node.id();

          // 如果该节点有 part_of 子工艺，双击用来展开/收起，不再走邻居展开
          const hasPartOfChildren =
            cy
              .edges('[edge_namespace = "ontology"][edge_type = "part_of"]')
              .filter((edge) => edge.target().id() === nodeId).length > 0;
          if (hasPartOfChildren) {
            // 双击展开/收起前，记录当前实际渲染位置；空 compound parent 的 position() 不可信
            const rendered = node.renderedPosition();
            const pan = cy.pan();
            const zoom = cy.zoom();
            const modelPos = {
              x: (rendered.x - pan.x) / zoom,
              y: (rendered.y - pan.y) / zoom,
            };
            processGroupDragPositionsRef.current.set(nodeId, modelPos);
            // eslint-disable-next-line no-console
            console.log("[dbltap expand] nodeId:", nodeId, "rendered:", rendered, "pan:", pan, "zoom:", zoom, "modelPos:", modelPos, "current position():", node.position());
            onToggleProcessExpansionRef.current?.(nodeId);
            return;
          }

          // 【设计理由: 双击即固化】
          // 无论这个节点之前是不是预览节点，既然用户双击了它，就立刻把它变成主图实体。
          node.removeClass("external");

          try {
            const { nodes, edges } = await getNeighbors(nodeId);

            cy.batch(() => {
              nodes.forEach((n) => {
                const existingNode = cy.getElementById(n.node_id);
                if (existingNode.length > 0) {
                  // 如果节点已存在(比如刚才还是半透明的)，剥夺其 external 标记使其永久化
                  existingNode.removeClass("external");
                } else {
                  // 如果完全是新节点，直接作为实体节点加入 (不带 classes)
                  cy.add({
                    data: {
                      id: n.node_id,
                      label: n.canonical_name_zh,
                      entity_type: n.entity_type,
                      status: n.status,
                      confidence: n.confidence,
                      raw: n,
                    },
                  });
                }
              });

              edges.forEach((e) => {
                const existingEdge = cy.getElementById(e.edge_id);
                if (existingEdge.length > 0) {
                  // 存在的边同样转正
                  existingEdge.removeClass("external");
                } else {
                  cy.add({
                    data: {
                      id: e.edge_id,
                      source: e.from_node,
                      target: e.to_node,
                      edge_namespace: e.edge_namespace,
                      edge_type: e.edge_type,
                      label: e.edge_type_label || e.edge_type,
                      raw: e,
                    },
                  });
                }
              });
            });

            // 【设计理由: 重整骨架】
            // 双击代表一次完整的子图合并操作，此时重新应用过滤器，并触发 dagre 全局重排，
            // 把之前由于“顺藤摸瓜”可能拉扯乱的局部拓扑结构重新梳理平整。
            syncCompoundParents(cy, expandedProcessParentsRef.current, processGroupDragPositionsRef.current);
            applyFilters(cy, filtersRef.current, expandedProcessParentsRef.current, focusStateRef.current, hideStateRef.current);
            runHybridLayout(cy, false);

          } catch (err) {
            console.error("Expand failed:", err);
          }
        });

        // 键盘事件：ESC 取消选择并关闭详情面板；Delete/Backspace 删除选中边
        keyHandler = (e: KeyboardEvent) => {
          const target = e.target as HTMLElement;
          if (
            target &&
            (target.tagName === "INPUT" ||
              target.tagName === "TEXTAREA" ||
              target.isContentEditable)
          ) {
            return;
          }
          if (e.key === "Escape") {
            if (editModeRef.current === "connect" && connectSourceNodeIdRef.current) {
              onCancelConnectRef.current?.();
              return;
            }
            cy.elements().unselect();
            cy.elements().removeClass("highlighted dimmed");
            cy.elements(".external").remove();
            onClearSelectionRef.current?.();
            return;
          }
          if (e.key !== "Delete" && e.key !== "Backspace") return;
          const selectedEdge = cy.$(":selected").filter("edge");
          if (selectedEdge.length > 0) {
            const rawData = selectedEdge.data("raw") as GraphEdge;
            onEdgeDeleteRef.current?.(rawData);
          }
        };
        window.addEventListener("keydown", keyHandler);

        cyRef.current = cy;

        // 在 layout 动画前就注册平移/右键处理器，避免右击等待 layout 时无响应
        if (containerRef.current) {
          cleanupPanHandlers = setupPanHandlers(cy, containerRef.current);
        }

        // 防止组件在初始化期间卸载后继续操作已销毁的 Cytoscape 实例
        if (!cyRef.current || cyRef.current !== cy) {
          cy.destroy();
          return;
        }

        // 如果正在恢复已保存视图，把展开工艺组的父节点位置预置到拖拽记录中，
        // 这样 syncCompoundParents 会以该位置为中心创建 compound parent，
        // 而不是让 Cytoscape 根据子节点重新计算父节点位置。
        if (restoredPositions) {
          skipLayoutOnExpandForRestoreRef.current = true;
          expandedProcessParentsRef.current.forEach((parentId) => {
            const pos = restoredPositions[parentId];
            if (pos) processGroupDragPositionsRef.current.set(parentId, pos);
          });
        }
        // 初始标记所有可展开工艺组，并应用过滤器隐藏 part_of 子节点。
        // 恢复视图时跳过局部布局（parentsToLayout 传空数组），因为保存的节点位置随后会由 applyPendingViewState 应用。
        syncCompoundParents(
          cy,
          expandedProcessParentsRef.current,
          processGroupDragPositionsRef.current,
          restoredPositions ? [] : undefined
        );

        if (!cyRef.current || cyRef.current !== cy) {
          cy.destroy();
          return;
        }

        applyFilters(cy, filtersRef.current, expandedProcessParentsRef.current, focusStateRef.current, hideStateRef.current);
        if (restoredPositions) {
          // 如果正在恢复已保存视图，直接使用保存的节点位置，避免重新布局破坏用户布局。
          applyPendingViewState();
        } else {
          // 使用混合布局：产业流自上而下，is_a 关系环绕父节点
          runHybridLayout(cy, true, expandedProcessParentsRef.current, processGroupDragPositionsRef.current, () => {
            if (!cyRef.current || cyRef.current !== cy || (cy as unknown as { _private?: { destroyed?: boolean } })._private?.destroyed) return;
            applyPendingViewState();
          });
        }
        setLoading(false);
      } catch (err) {
        if (mounted) {
          setError(err instanceof Error ? err.message : "加载失败");
          setLoading(false);
        }
      }
    }
    init();

    return () => {
      mounted = false;
      if (keyHandler) window.removeEventListener("keydown", keyHandler);
      cleanupPanHandlers?.();
      const cyToDestroy = cyRef.current;
      cyRef.current = null;
      if (cyToDestroy && !(cyToDestroy as unknown as { _private?: { destroyed?: boolean } })._private?.destroyed) {
        cyToDestroy.autoungrabify(false);
        cyToDestroy.destroy();
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Apply filters when they change
  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;
    applyFilters(cy, filters, expandedProcessParentsRef.current, focusState, hideState);
  }, [filters, focusState, hideState]);

  // Apply filters when focus/hide state changes (from imperative API)
  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;
    applyFilters(cy, filtersRef.current, expandedProcessParentsRef.current, focusState, hideState);
  }, [focusState, hideState]);

  // Sync compound parents and re-layout when process expansion changes
  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;

    // 如果是从已保存视图恢复后的第一次 expandedProcessParents effect，直接应用保存的状态，
    // 不要重新布局，避免破坏用户保存的节点位置。
    if (skipLayoutOnExpandForRestoreRef.current) {
      skipLayoutOnExpandForRestoreRef.current = false;
      prevExpandedProcessParentsRef.current = [...expandedProcessParents];
      syncCompoundParents(cy, expandedProcessParents, processGroupDragPositionsRef.current, []);
      applyFilters(cy, filtersRef.current, expandedProcessParents, focusStateRef.current, hideStateRef.current);
      applyPendingViewState();
      return;
    }

    // 计算本次真正发生状态变化的组：只对新展开的组做局部布局，已经展开的外层组
    // （如晶圆制造）保持原状，避免展开内层组时把整个图撑乱。
    const prev = prevExpandedProcessParentsRef.current;
    const newlyExpanded = expandedProcessParents.filter((id) => !prev.includes(id));
    prevExpandedProcessParentsRef.current = [...expandedProcessParents];

    syncCompoundParents(
      cy,
      expandedProcessParents,
      processGroupDragPositionsRef.current,
      newlyExpanded.length > 0 ? newlyExpanded : undefined
    );
    applyFilters(cy, filtersRef.current, expandedProcessParents, focusStateRef.current, hideStateRef.current);

    // 收起时（expandedProcessParents 为空）不再触发全局重排，避免视图乱跳；
    // 展开时只对真正新展开的组做局部布局，不 fit，保证 group 原地展开。
    let rafId: number | null = null;
    if (expandedProcessParents.length > 0) {
      rafId = requestAnimationFrame(() => {
        rafId = null;
        const currentCy = cyRef.current;
        if (!currentCy) return;
        runHybridLayout(
          currentCy,
          false,
          expandedProcessParents,
          processGroupDragPositionsRef.current,
          () => applyPendingViewState(),
          newlyExpanded.length > 0 ? newlyExpanded : undefined
        );
      });
    } else {
      // Collapse: still try to apply any queued view state (camera is independent of layout)
      applyPendingViewState();
    }
    return () => {
      if (rafId !== null) cancelAnimationFrame(rafId);
    };
  }, [expandedProcessParents]);

  // Connect mode source highlight
  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;
    cy.nodes().removeClass("connect-source");
    if (connectSourceNodeId) {
      const source = cy.getElementById(connectSourceNodeId);
      if (source.length > 0) source.addClass("connect-source");
    }
  }, [connectSourceNodeId]);

  // Connect mode dynamic edge from source node to mouse cursor
  useEffect(() => {
    const cy = cyRef.current;
    const container = containerRef.current;
    if (!cy || !container) return;
    if (editMode !== "connect" || !connectSourceNodeId || connectTargetNodeId) {
      connectMousePosRef.current = null;
      connectMouseVisibleRef.current = true;
      return;
    }

    const line = connectLineRef.current;
    if (!line) return;

    const updateLine = () => {
      const source = cy.getElementById(connectSourceNodeId);
      if (source.length === 0 || source.hasClass("hidden")) {
        line.style.display = "none";
        return;
      }
      const rect = container.getBoundingClientRect();
      const sourcePos = source.renderedPosition();
      line.setAttribute("x1", String(sourcePos.x));
      line.setAttribute("y1", String(sourcePos.y));
      if (connectMousePosRef.current && connectMouseVisibleRef.current) {
        line.setAttribute("x2", String(connectMousePosRef.current.x - rect.left));
        line.setAttribute("y2", String(connectMousePosRef.current.y - rect.top));
        line.style.display = "block";
      } else {
        line.style.display = "none";
      }
    };

    const handlePointerMove = (e: PointerEvent) => {
      connectMousePosRef.current = { x: e.clientX, y: e.clientY };
      updateLine();
    };

    const handlePointerLeave = () => {
      connectMouseVisibleRef.current = false;
      updateLine();
    };

    const handlePointerEnter = () => {
      connectMouseVisibleRef.current = true;
      updateLine();
    };

    const handleWindowMouseOut = (e: MouseEvent) => {
      if (e.relatedTarget === null) {
        connectMouseVisibleRef.current = false;
        updateLine();
      }
    };

    const handleWindowMouseOver = (e: MouseEvent) => {
      if (e.relatedTarget === null) {
        connectMouseVisibleRef.current = true;
        updateLine();
      }
    };

    const handleRender = () => {
      updateLine();
    };

    container.addEventListener("pointermove", handlePointerMove);
    container.addEventListener("pointerleave", handlePointerLeave);
    container.addEventListener("pointerenter", handlePointerEnter);
    window.addEventListener("mouseout", handleWindowMouseOut);
    window.addEventListener("mouseover", handleWindowMouseOver);
    cy.on("render", handleRender);

    updateLine();

    return () => {
      container.removeEventListener("pointermove", handlePointerMove);
      container.removeEventListener("pointerleave", handlePointerLeave);
      container.removeEventListener("pointerenter", handlePointerEnter);
      window.removeEventListener("mouseout", handleWindowMouseOut);
      window.removeEventListener("mouseover", handleWindowMouseOver);
      cy.off("render", handleRender);
    };
  }, [editMode, connectSourceNodeId, connectTargetNodeId]);

  // Queue restored view state (positions + camera) to be applied after the next layout finishes.
  useEffect(() => {
    if (!restoredPositions && !restoredCamera) return;
    if (restoredPositions) pendingPositionsRef.current = restoredPositions;
    if (restoredCamera) pendingCameraRef.current = restoredCamera;
    // If the graph is already initialized and no layout is in progress, apply immediately;
    // otherwise the pending state will be picked up by the layout completion callback.
    const cy = cyRef.current;
    if (cy && !cy.animated()) {
      applyPendingViewState();
    }
  }, [restoredPositions, restoredCamera]);

  // Highlight single node
  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;
    cy.elements().removeClass("highlighted dimmed");
    if (highlightNodeId) {
      const target = cy.getElementById(highlightNodeId);
      if (target.length) {
        target.removeClass("hidden");
        // 若关联边因另一端被隐藏而隐藏，当另一端可见时重新显示该边
        target.connectedEdges().forEach((edge) => {
          const other = edge.source().id() === target.id() ? edge.target() : edge.source();
          if (!other.hasClass("hidden")) {
            edge.removeClass("hidden");
          }
        });
        const neighborhood = target.neighborhood();
        target.addClass("highlighted");
        neighborhood.edges().addClass("highlighted");
        cy.elements().not(target).not(neighborhood).addClass("dimmed");
        // 平移到视野中心，不改变缩放级别
        cy.animate({
          center: { eles: target },
          duration: 400,
          easing: "ease-out",
        });
      } else {
        // 节点未在当前图谱中加载：单独获取并添加到视野中心
        getNode(highlightNodeId).then((node) => {
          if (!cyRef.current) return;
          const cy2 = cyRef.current;
          if (cy2.getElementById(node.node_id).length) return;
          const extent = cy2.extent();
          const x = (extent.x1 + extent.x2) / 2;
          const y = (extent.y1 + extent.y2) / 2;
          cy2.add({
            data: {
              id: node.node_id,
              label: node.canonical_name_zh,
              entity_type: node.entity_type,
              status: node.status,
              confidence: node.confidence,
              raw: node,
            },
            position: { x, y },
          });
          const added = cy2.getElementById(node.node_id);
          added.removeClass("hidden");
          added.addClass("highlighted");
          cy2.elements().not(added).addClass("dimmed");
          cy2.animate({
            center: { eles: added },
            duration: 400,
            easing: "ease-out",
          });
        }).catch(() => {
          // 节点不存在或网络错误，静默忽略
        });
      }
    }
  }, [highlightNodeId]);

  // Highlight multiple nodes (industry/company focus)
  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;
    cy.elements().removeClass("highlighted dimmed");
    if (highlightNodeIds && highlightNodeIds.length > 0) {
      const targets = cy.collection();
      highlightNodeIds.forEach((id) => {
        const el = cy.getElementById(id);
        if (el.length) targets.merge(el);
      });
      if (targets.length > 0) {
        targets.addClass("highlighted");
        // Also highlight edges between selected nodes
        const targetEdges = targets.edgesWith(targets);
        targetEdges.addClass("highlighted");
        cy.elements().not(targets).not(targetEdges).addClass("dimmed");
        // 仅高亮，不移动/缩放相机
      }
    }
  }, [highlightNodeIds]);

  return (
    <div className="relative h-full w-full bg-slate-950">
      {loading && (
        <div className="absolute inset-0 z-10 flex items-center justify-center bg-slate-950">
          <div className="text-sm text-slate-400">加载图谱中...</div>
        </div>
      )}
      {error && (
        <div className="absolute inset-0 z-10 flex items-center justify-center bg-slate-950">
          <div className="text-sm text-red-400">错误: {error}</div>
        </div>
      )}
      <div
        ref={containerRef}
        className="relative h-full w-full"
        onContextMenu={(e) => e.preventDefault()}
      >
        {editMode === "connect" && connectSourceNodeId && !connectTargetNodeId && (
          <svg
            ref={connectSvgRef}
            className="pointer-events-none absolute inset-0 z-20 h-full w-full"
          >
            <line
              ref={connectLineRef}
              x1="0"
              y1="0"
              x2="0"
              y2="0"
              stroke="#22d3ee"
              strokeWidth="2"
              strokeDasharray="6,4"
              opacity="0.85"
            />
          </svg>
        )}
      </div>
    </div>
  );
});
