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
import { getNeighbors, listEdges, listNodes } from "@/services/api";

cytoscape.use(dagre);

interface GraphCanvasProps {
  onNodeClick: (node: IndustrialNode) => void;
  onEdgeClick: (edge: GraphEdge) => void;
  filters: {
    edgeNamespaces: string[];
    edgeTypes: string[];
    entityTypes: string[];
    status: string[];
    confidence: string[];
  };
  highlightNodeId?: string;
}

export function GraphCanvas({
  onNodeClick,
  onEdgeClick,
  filters,
  highlightNodeId,
}: GraphCanvasProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<cytoscape.Core | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Initial load
  useEffect(() => {
    let mounted = true;
    async function init() {
      try {
        setLoading(true);
        const [nodesData, edgesData] = await Promise.all([
          listNodes(1, 200),
          listEdges(1, 500),
        ]);
        if (!mounted) return;

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
            ...edgesData.items.map((e) => ({
              data: {
                id: e.edge_id,
                source: e.from_node,
                target: e.to_node,
                edge_namespace: e.edge_namespace,
                edge_type: e.edge_type,
                label: e.edge_type,
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
              selector: ".highlighted",
              style: {
                "border-color": "#facc15",
                "border-width": 4,
              },
            },
            {
              selector: ".dimmed",
              style: { opacity: 0.15 },
            },
            {
              selector: ":selected",
              style: {
                "border-color": "#22d3ee",
                "border-width": 3,
              },
            },
          ],
          layout: {
            name: "dagre",
            rankDir: "TB",
            nodeSep: 40,
            edgeSep: 20,
            rankSep: 80,
            padding: 20,
          } as cytoscape.LayoutOptions,
          wheelSensitivity: 0.3,
          minZoom: 0.2,
          maxZoom: 3,
        });

        cy.on("tap", "node", (evt) => {
          onNodeClick(evt.target.data("raw") as IndustrialNode);
        });
        cy.on("tap", "edge", (evt) => {
          onEdgeClick(evt.target.data("raw") as GraphEdge);
        });
        cy.on("tap", (evt) => {
          if (evt.target === cy) {
            cy.elements().removeClass("highlighted dimmed");
          }
        });
        cy.on("dbltap", "node", async (evt) => {
          const nodeId = evt.target.id();
          try {
            const { nodes, edges } = await getNeighbors(nodeId);
            const existingIds = new Set(cy.nodes().map((n) => n.id()));
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
                });
              }
            });
            edges.forEach((e) => {
              if (!cy.getElementById(e.edge_id).length) {
                cy.add({
                  data: {
                    id: e.edge_id,
                    source: e.from_node,
                    target: e.to_node,
                    edge_namespace: e.edge_namespace,
                    edge_type: e.edge_type,
                    label: e.edge_type,
                    raw: e,
                  },
                });
              }
            });
            cy.layout({ name: "dagre", rankDir: "TB", fit: false } as cytoscape.LayoutOptions).run();
          } catch (err) {
            console.error("Expand failed:", err);
          }
        });

        cyRef.current = cy;
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
  }, [onNodeClick, onEdgeClick]);

  // Apply filters
  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;

    cy.batch(() => {
      cy.nodes().forEach((node) => {
        const et = node.data("entity_type");
        const st = node.data("status");
        const cf = node.data("confidence");
        const show =
          (filters.entityTypes.length === 0 || filters.entityTypes.includes(et)) &&
          (filters.status.length === 0 || filters.status.includes(st)) &&
          (filters.confidence.length === 0 || filters.confidence.includes(cf));
        node.style("display", show ? "element" : "none");
      });
      cy.edges().forEach((edge) => {
        const ns = edge.data("edge_namespace");
        const et = edge.data("edge_type");
        const show =
          (filters.edgeNamespaces.length === 0 || filters.edgeNamespaces.includes(ns)) &&
          (filters.edgeTypes.length === 0 || filters.edgeTypes.includes(et));
        edge.style("display", show ? "element" : "none");
      });
    });
  }, [filters]);

  // Highlight node
  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;
    cy.elements().removeClass("highlighted dimmed");
    if (highlightNodeId) {
      const target = cy.getElementById(highlightNodeId);
      if (target.length) {
        target.addClass("highlighted");
        cy.elements().not(target).not(target.neighborhood()).addClass("dimmed");
        cy.animate({
          fit: { eles: target, padding: 80 },
          duration: 400,
          easing: "ease-out",
        });
      }
    }
  }, [highlightNodeId]);

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
      <div ref={containerRef} className="h-full w-full" />
    </div>
  );
}
