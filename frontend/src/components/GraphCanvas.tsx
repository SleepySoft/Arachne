import { useEffect, useRef, useState } from "react";
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
function runHybridLayout(cy: cytoscape.Core, fit = true) {
  const dagreLayout = cy.layout({
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
    // 只处理 ontology/is_a 边（source 是子类，target 是父类）
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
        // 半径根据子节点数量动态调整，避免拥挤
        const radius = Math.max(90, count * 22);
        const angleStep = (2 * Math.PI) / count;
        // 以父节点相对画布中心的角度为起点，让环有一定方向感
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

interface GraphCanvasProps {
  onNodeClick: (node: IndustrialNode) => void;
  onEdgeClick: (edge: GraphEdge) => void;
  onNodeContextMenu?: (node: IndustrialNode, x: number, y: number) => void;
  filters: {
    edgeNamespaces: string[];
    edgeTypes: string[];
    entityTypes: string[];
    status: string[];
    confidence: string[];
  };
  highlightNodeId?: string;
  highlightNodeIds?: string[];
  sourceData?: { nodes: IndustrialNode[]; edges: GraphEdge[] };
}

function applyFilters(
  cy: cytoscape.Core,
  filters: GraphCanvasProps["filters"]
) {
  const entityTypeSet = new Set(filters.entityTypes);
  const statusSet = new Set(filters.status);
  const confidenceSet = new Set(filters.confidence);
  const edgeNsSet = new Set(filters.edgeNamespaces);
  const edgeTypeSet = new Set(filters.edgeTypes);

  const visibleNodeIds = new Set<string>();

  cy.batch(() => {
    cy.nodes().forEach((node) => {
      const et = node.data("entity_type");
      const st = node.data("status");
      const cf = node.data("confidence");
      const show =
        (entityTypeSet.size === 0 || entityTypeSet.has(et)) &&
        (statusSet.size === 0 || statusSet.has(st)) &&
        (confidenceSet.size === 0 || confidenceSet.has(cf));
      node.toggleClass("hidden", !show);
      if (show) visibleNodeIds.add(node.id());
    });

    cy.edges().forEach((edge) => {
      const ns = edge.data("edge_namespace");
      const et = edge.data("edge_type");
      const show =
        visibleNodeIds.has(edge.source().id()) &&
        visibleNodeIds.has(edge.target().id()) &&
        (edgeNsSet.size === 0 || edgeNsSet.has(ns)) &&
        (edgeTypeSet.size === 0 || edgeTypeSet.has(et));
      edge.toggleClass("hidden", !show);
    });
  });
}

export function GraphCanvas({
  onNodeClick,
  onEdgeClick,
  onNodeContextMenu,
  filters,
  highlightNodeId,
  highlightNodeIds,
  sourceData,
}: GraphCanvasProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<cytoscape.Core | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const onNodeClickRef = useRef(onNodeClick);
  const onEdgeClickRef = useRef(onEdgeClick);
  const onNodeContextMenuRef = useRef(onNodeContextMenu);
  const filtersRef = useRef(filters);
  const sourceDataRef = useRef(sourceData);

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

  // Initial load — only once
  useEffect(() => {
    let mounted = true;
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
        // 3. 画布空白处单击事件：重置图谱状态
        // ==========================================
        cy.on("tap", (evt) => {
          if (evt.target === cy) {
            // 【设计理由: 提供安全的撤退路径】
            // 点空白处取消所有高亮，并清理掉所有临时的半透明预览节点
            cy.elements().removeClass("highlighted dimmed");
            cy.elements(".external").remove();
          }
        });

        // ==========================================
        // 4. 节点双击事件：展开、完全固化与重排
        // ==========================================
        cy.on("dbltap", "node", async (evt) => {
          const node = evt.target;
          const nodeId = node.id();

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
            applyFilters(cy, filtersRef.current);
            runHybridLayout(cy, false);

          } catch (err) {
            console.error("Expand failed:", err);
          }
        });

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
    applyFilters(cy, filters);
  }, [filters]);

  // Highlight single node
  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;
    cy.elements().removeClass("highlighted dimmed");
    if (highlightNodeId) {
      const target = cy.getElementById(highlightNodeId);
      if (target.length) {
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
        onContextMenu={(e) => {
          e.preventDefault();
          const cy = cyRef.current;
          if (!cy || cy.nodes().length === 0) return;

          const rect = containerRef.current!.getBoundingClientRect();
          const mouseX = e.clientX - rect.left;
          const mouseY = e.clientY - rect.top;

          // 找到鼠标位置下的节点（使用渲染坐标 hit-test）
          const clickedNode = cy.nodes().toArray().find((node) => {
            const bb = node.renderedBoundingBox({
              includeOverlays: false,
              includeLabels: false,
            });
            return (
              mouseX >= bb.x1 &&
              mouseX <= bb.x2 &&
              mouseY >= bb.y1 &&
              mouseY <= bb.y2
            );
          });

          if (clickedNode && onNodeContextMenuRef.current) {
            const rawData = clickedNode.data("raw") as IndustrialNode;
            onNodeContextMenuRef.current(rawData, e.clientX, e.clientY);
          }
        }}
      />
    </div>
  );
}
