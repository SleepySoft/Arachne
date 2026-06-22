import { forwardRef, useEffect, useImperativeHandle, useRef, useState } from "react";
import cytoscape from "cytoscape";
import dagre from "cytoscape-dagre";
import {
  CONFIDENCE_OPACITY,
  EDGE_NAMESPACE_STYLES,
  ENTITY_TYPE_COLORS,
  GraphEdge,
  IndustrialNode,
} from "@/types";
import { getNeighbors, getNode, listEdges, listNodes } from "@/services/api";

cytoscape.use(dagre);

/**
 * 混合布局：
 * 1. 先用 Dagre 对产业流（industrial_flow）做自上而下分层布局；
 * 2. 再对 ontology/is_a 关系做“环绕”修正，把子节点以同心圆方式排在父节点周围。
 */
function layoutExpandedCompound(cy: cytoscape.Core, parentId: string) {
  const parent = cy.getElementById(parentId);
  if (parent.length === 0) return;
  const center = parent.position();
  const children = parent.children();
  const count = children.length;
  if (count === 0) return;
  const radius = Math.max(160, count * 38);
  const angleStep = (2 * Math.PI) / count;
  children.forEach((child, index) => {
    const angle = index * angleStep;
    child.position({
      x: center.x + radius * Math.cos(angle),
      y: center.y + radius * Math.sin(angle),
    });
  });
}

function runHybridLayout(
  cy: cytoscape.Core,
  fit = true,
  expandedProcessParents: string[] = []
) {
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
    expandedParents.forEach((parent) => layoutExpandedCompound(cy, parent.id()));
    if (fit) {
      // 只 fit 到父节点及其子节点，不要把整个邻域拉进来导致缩放过小
      const fitCollection = expandedParents.union(expandedParents.descendants());
      cy.animate(
        { fit: { eles: fitCollection, padding: 40 } },
        { duration: 250, easing: "ease-in-out-cubic" }
      );
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

    if (fit) {
      cy.fit(cy.elements(), 40);
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
}

interface GraphCanvasProps {
  onNodeClick: (node: IndustrialNode) => void;
  onEdgeClick: (edge: GraphEdge) => void;
  onNodeContextMenu?: (node: IndustrialNode, x: number, y: number) => void;
  onEdgeContextMenu?: (edge: GraphEdge, x: number, y: number) => void;
  onCanvasContextMenu?: (x: number, y: number) => void;
  onEdgeDelete?: (edge: GraphEdge) => void;
  onConnectSourceSelect?: (node: IndustrialNode | null, position?: { x: number; y: number }) => void;
  onConnectTargetSelect?: (node: IndustrialNode, position?: { x: number; y: number }) => void;
  filters: {
    edgeNamespaces: string[];
    edgeTypes: string[];
    entityTypes: string[];
    status: string[];
    confidence: string[];
    showIsA: boolean;
    showWeakOntology: boolean;
  };
  highlightNodeId?: string;
  highlightNodeIds?: string[];
  sourceData?: { nodes: IndustrialNode[]; edges: GraphEdge[] };
  editMode?: EditMode;
  connectSourceNodeId?: string | null;
  expandedProcessParents?: string[];
  onToggleProcessExpansion?: (nodeId: string) => void;
}

function applyFilters(
  cy: cytoscape.Core,
  filters: GraphCanvasProps["filters"],
  expandedProcessParents: string[] = []
) {
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

  const visibleNodeIds = new Set<string>();

  cy.batch(() => {
    cy.nodes().forEach((node) => {
      const et = node.data("entity_type");
      const st = node.data("status");
      const cf = node.data("confidence");
      let show =
        (entityTypeSet.size === 0 || entityTypeSet.has(et)) &&
        (statusSet.size === 0 || statusSet.has(st)) &&
        (confidenceSet.size === 0 || confidenceSet.has(cf));
      // 如果节点是某个未展开父节点的子工艺，则隐藏
      if (show) {
        const parentId = childToParent.get(node.id());
        if (parentId && !expandedParentSet.has(parentId)) {
          show = false;
        }
      }
      node.toggleClass("hidden", !show);
      if (show) visibleNodeIds.add(node.id());
    });

    const weakOntologyTypes = new Set(["alias_of", "related_term", "variant_of"]);
    cy.edges().forEach((edge) => {
      const ns = edge.data("edge_namespace");
      const et = edge.data("edge_type");
      const isIsA = ns === "ontology" && et === "is_a";
      const isWeakOntology = ns === "ontology" && weakOntologyTypes.has(et);
      const show =
        visibleNodeIds.has(edge.source().id()) &&
        visibleNodeIds.has(edge.target().id()) &&
        (edgeNsSet.size === 0 || edgeNsSet.has(ns)) &&
        (edgeTypeSet.size === 0 || edgeTypeSet.has(et)) &&
        (!isIsA || filters.showIsA) &&
        (!isWeakOntology || filters.showWeakOntology);
      edge.toggleClass("hidden", !show);
    });

    // 当边被过滤后，把因此变得孤立的节点也隐藏起来
    cy.nodes().forEach((node) => {
      if (node.hasClass("hidden")) return;
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
  expandedProcessParents: string[]
) {
  const expandedSet = new Set(expandedProcessParents);
  const childToParent = new Map<string, string>();
  cy.edges('[edge_namespace = "ontology"][edge_type = "part_of"]').forEach(
    (edge) => {
      childToParent.set(edge.source().id(), edge.target().id());
    }
  );
  // eslint-disable-next-line no-console
  console.log("[syncCompoundParents] part_of edges:", childToParent.size, "expanded:", expandedProcessParents);

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
  });
}

export const GraphCanvas = forwardRef<GraphCanvasRef, GraphCanvasProps>(function GraphCanvas(
  {
    onNodeClick,
    onEdgeClick,
    onNodeContextMenu,
    onEdgeContextMenu,
    onCanvasContextMenu,
    onEdgeDelete,
    onConnectSourceSelect,
    onConnectTargetSelect,
    filters,
    highlightNodeId,
    highlightNodeIds,
    sourceData,
    editMode = "default",
    connectSourceNodeId = null,
    expandedProcessParents = [],
    onToggleProcessExpansion,
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
  const onCanvasContextMenuRef = useRef(onCanvasContextMenu);
  const onEdgeDeleteRef = useRef(onEdgeDelete);
  const onConnectSourceSelectRef = useRef(onConnectSourceSelect);
  const onConnectTargetSelectRef = useRef(onConnectTargetSelect);
  const filtersRef = useRef(filters);
  const sourceDataRef = useRef(sourceData);
  const editModeRef = useRef(editMode);
  const connectSourceNodeIdRef = useRef(connectSourceNodeId);
  const expandedProcessParentsRef = useRef(expandedProcessParents);
  const onToggleProcessExpansionRef = useRef(onToggleProcessExpansion);

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
    onConnectSourceSelectRef.current = onConnectSourceSelect;
  }, [onConnectSourceSelect]);

  useEffect(() => {
    onConnectTargetSelectRef.current = onConnectTargetSelect;
  }, [onConnectTargetSelect]);

  useEffect(() => {
    editModeRef.current = editMode;
  }, [editMode]);

  useEffect(() => {
    connectSourceNodeIdRef.current = connectSourceNodeId;
  }, [connectSourceNodeId]);

  useEffect(() => {
    expandedProcessParentsRef.current = expandedProcessParents;
  }, [expandedProcessParents]);

  useEffect(() => {
    onToggleProcessExpansionRef.current = onToggleProcessExpansion;
  }, [onToggleProcessExpansion]);

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
      applyFilters(cy, filtersRef.current, expandedProcessParentsRef.current);
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
      applyFilters(cy, filtersRef.current, expandedProcessParentsRef.current);
    },
    removeEdge: (edgeId) => {
      const cy = cyRef.current;
      if (!cy) return;
      const el = cy.getElementById(edgeId);
      if (el.length > 0) cy.remove(el);
      applyFilters(cy, filtersRef.current, expandedProcessParentsRef.current);
    },
    removeNode: (nodeId) => {
      const cy = cyRef.current;
      if (!cy) return;
      const el = cy.getElementById(nodeId);
      if (el.length > 0) cy.remove(el);
      applyFilters(cy, filtersRef.current, expandedProcessParentsRef.current);
    },
  }));

  // Initial load — only once
  useEffect(() => {
    let mounted = true;
    let keyHandler: ((e: KeyboardEvent) => void) | undefined;
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
                opacity: (ele: cytoscape.NodeSingular) =>
                  CONFIDENCE_OPACITY[ele.data("confidence") as keyof typeof CONFIDENCE_OPACITY] || 0.5,
              },
            },
            {
              selector: "edge",
              style: {
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
              },
            },
            {
              selector: ".hidden",
              style: {
                display: "none",
              },
            },
            {
              selector: ".highlighted",
              style: {
                "border-color": "#facc15",
                "border-width": 5,
                width: 38,
                height: 38,
                color: "#facc15",
                "text-background-color": "#422006",
                "text-background-opacity": 0.95,
                "text-background-padding": "3px 6px",
              },
            },
            {
              selector: ".dimmed",
              style: { opacity: 0.15 },
            },
            {
              selector: ".external",
              style: {
                opacity: 0.35,
                "background-color": "#475569",
                "line-color": "#475569",
                "target-arrow-color": "#475569",
                color: "#475569",
                "text-background-color": "#0f172a",
              },
            },
            {
              selector: ":parent, .compound-parent",
              style: {
                "background-opacity": 0.18,
                "background-color": "#0ea5e9",
                "border-color": "#38bdf8",
                "border-width": 3,
                "border-opacity": 0.9,
                "border-style": "dashed",
                shape: "rectangle",
                "padding-top": "24px",
                "padding-bottom": "24px",
                "padding-left": "24px",
                "padding-right": "24px",
                "min-width": "160px",
                "min-height": "160px",
                "text-valign": "top",
                "text-halign": "center",
                "text-margin-y": 10,
                color: "#e0f2fe",
                "font-size": "12px",
                "font-weight": "bold",
              },
            },
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
            {
              selector: ":selected",
              style: {
                "border-color": "#22d3ee",
                "border-width": 3,
              },
            },
          ],
          // 初始不启用默认 dagre，改为在数据加载后执行混合布局
          layout: { name: "preset" } as cytoscape.LayoutOptions,
          wheelSensitivity: 1.0,
          minZoom: 0.2,
          maxZoom: 3,
        });

        // ==========================================
        // 1. 节点单击事件：预览 (Peek) 与顺藤摸瓜 (Auto-Pin)
        // ==========================================
        cy.on("tap", "node", async (evt) => {
          const node = evt.target;
          const rawData = node.data("raw") as IndustrialNode;

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
            } catch (err) {
              console.error("Show external neighbors failed:", err);
            }
          }
        });

        // ==========================================
        // 2. 边单击事件：单纯透传数据
        // ==========================================
        cy.on("tap", "edge", (evt) => {
          onEdgeClickRef.current(evt.target.data("raw") as GraphEdge);
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
            // 点空白处取消所有高亮，并清理掉所有临时的半透明预览节点
            cy.elements().removeClass("highlighted dimmed");
            cy.elements(".external").remove();
          }
        });

        // ==========================================
        // 3.5 右键菜单事件：节点 / 边 / 空白画布
        // ==========================================
        cy.on("cxttap", "node", (evt) => {
          const node = evt.target;
          const rawData = node.data("raw") as IndustrialNode;
          const e = evt.originalEvent as MouseEvent;
          onNodeContextMenuRef.current?.(rawData, e.clientX, e.clientY);
        });

        cy.on("cxttap", "edge", (evt) => {
          const edge = evt.target;
          const rawData = edge.data("raw") as GraphEdge;
          const e = evt.originalEvent as MouseEvent;
          onEdgeContextMenuRef.current?.(rawData, e.clientX, e.clientY);
        });

        cy.on("cxttap", (evt) => {
          if (evt.target === cy) {
            const e = evt.originalEvent as MouseEvent;
            onCanvasContextMenuRef.current?.(e.clientX, e.clientY);
          }
        });

        // ==========================================
        // 4. 节点双击事件：展开、完全固化与重排
        // ==========================================
        cy.on("dbltap", "node", async (evt) => {
          const node = evt.target;
          const nodeId = node.id();

          // 如果该节点有 part_of 子工艺，双击用来展开/收起，不再走邻居展开
          const hasPartOfChildren =
            cy
              .edges('[edge_namespace = "ontology"][edge_type = "part_of"]')
              .filter((edge) => edge.target().id() === nodeId).length > 0;
          if (hasPartOfChildren) {
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
            applyFilters(cy, filtersRef.current, expandedProcessParentsRef.current);
            runHybridLayout(cy, false);

          } catch (err) {
            console.error("Expand failed:", err);
          }
        });

        // 键盘删除：选中边时按 Delete/Backspace 删除
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
          if (e.key !== "Delete" && e.key !== "Backspace") return;
          const selectedEdge = cy.$(":selected").filter("edge");
          if (selectedEdge.length > 0) {
            const rawData = selectedEdge.data("raw") as GraphEdge;
            onEdgeDeleteRef.current?.(rawData);
          }
        };
        window.addEventListener("keydown", keyHandler);

        cyRef.current = cy;
        // 使用混合布局：产业流自上而下，is_a 关系环绕父节点
        runHybridLayout(cy, true);
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
      if (cyRef.current) {
        cyRef.current.destroy();
        cyRef.current = null;
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Apply filters when they change
  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;
    applyFilters(cy, filters, expandedProcessParentsRef.current);
  }, [filters]);

  // Sync compound parents and re-layout when process expansion changes
  useEffect(() => {
    // eslint-disable-next-line no-console
    console.log("[GraphCanvas] expandedProcessParents changed:", expandedProcessParents);
    const cy = cyRef.current;
    if (!cy) return;
    syncCompoundParents(cy, expandedProcessParents);
    applyFilters(cy, filtersRef.current, expandedProcessParents);
    // 收起时（expandedProcessParents 为空）不再触发全局重排，避免视图乱跳；
    // 展开时再做局部径向布局并平滑动画 fit 到复合节点。
    if (expandedProcessParents.length > 0) {
      requestAnimationFrame(() => {
        runHybridLayout(cy, true, expandedProcessParents);
      });
    }
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
        target.addClass("highlighted");
        cy.elements().not(target).not(target.neighborhood()).addClass("dimmed");
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
        cy.animate({
          fit: { eles: targets, padding: 100 },
          duration: 500,
          easing: "ease-out",
        });
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
        className="h-full w-full"
        onContextMenu={(e) => e.preventDefault()}
      />
    </div>
  );
});
