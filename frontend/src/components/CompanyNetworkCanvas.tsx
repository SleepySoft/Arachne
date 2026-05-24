import { useEffect, useRef } from "react";
import cytoscape from "cytoscape";
import dagre from "cytoscape-dagre";

cytoscape.use(dagre);

interface CompanyNetworkNode {
  company_id: string;
  name_zh: string;
  company_type: string;
  status: string;
}

interface CompanyNetworkEdge {
  from_company_id: string;
  to_company_id: string;
  path_count: number;
  strength: number;
  confidence: string;
}

interface CompanyNetworkCanvasProps {
  nodes: CompanyNetworkNode[];
  edges: CompanyNetworkEdge[];
  onNodeClick?: (company: CompanyNetworkNode) => void;
  highlightCompanyId?: string | null;
  dimUnrelated?: boolean;
}

const COMPANY_TYPE_COLORS: Record<string, string> = {
  public: "#22d3ee",
  private: "#a3e635",
  state_owned: "#f87171",
  startup: "#fbbf24",
  unknown: "#64748b",
};

const UPSTREAM_COLOR = "#22d3ee";

export function CompanyNetworkCanvas({
  nodes,
  edges,
  onNodeClick,
  highlightCompanyId,
  dimUnrelated,
}: CompanyNetworkCanvasProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<cytoscape.Core | null>(null);
  const onNodeClickRef = useRef(onNodeClick);

  useEffect(() => {
    onNodeClickRef.current = onNodeClick;
  }, [onNodeClick]);

  // Build / rebuild cytoscape instance when nodes/edges change
  useEffect(() => {
    if (!containerRef.current) return;
    if (nodes.length === 0) return;

    const cy = cytoscape({
      container: containerRef.current,
      elements: [
        ...nodes.map((n) => ({
          data: {
            id: n.company_id,
            label: n.name_zh,
            company_type: n.company_type,
            raw: n,
          },
        })),
        ...edges.map((e, i) => ({
          data: {
            id: `rel_${e.from_company_id}_${e.to_company_id}_${i}`,
            source: e.from_company_id,
            target: e.to_company_id,
            path_count: e.path_count,
            strength: e.strength,
            label: `上游 (${e.path_count})`,
            raw: e,
          },
        })),
      ],
      style: [
        {
          selector: "node",
          style: {
            "background-color": (ele: cytoscape.NodeSingular) =>
              COMPANY_TYPE_COLORS[ele.data("company_type")] || "#64748b",
            "border-width": 2,
            "border-color": "#1e293b",
            width: 32,
            height: 32,
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

          },
        },
        {
          selector: "edge",
          style: {
            "line-color": UPSTREAM_COLOR,
            "target-arrow-color": UPSTREAM_COLOR,
            "target-arrow-shape": "triangle",
            "arrow-scale": 0.8,
            width: 1.5,
            "curve-style": "bezier",
            "line-style": "solid",
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
            width: 48,
            height: 48,
            "font-size": "12px",
            "font-weight": "bold",
            "z-index": 999,
          },
        },
        {
          selector: ".dimmed",
          style: {
            opacity: 0.1,
          },
        },
        {
          selector: "edge.dimmed",
          style: {
            opacity: 0.04,
          },
        },
      ],
      layout: {
        name: "dagre",
        rankDir: "TB",
        nodeSep: 50,
        edgeSep: 20,
        rankSep: 80,
        padding: 20,
      } as cytoscape.LayoutOptions,
      wheelSensitivity: 1.0,
      minZoom: 0.2,
      maxZoom: 3,
    });

    cy.on("tap", "node", (evt) => {
      const rawData = evt.target.data("raw") as CompanyNetworkNode;
      if (onNodeClickRef.current) {
        onNodeClickRef.current(rawData);
      }
    });

    cyRef.current = cy;

    return () => {
      cy.destroy();
      cyRef.current = null;
    };
  }, [nodes, edges]);

  // Apply highlight / dim when highlightCompanyId or dimUnrelated changes
  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;

    // Reset all classes
    cy.nodes().removeClass("highlighted dimmed");
    cy.edges().removeClass("dimmed");

    if (!highlightCompanyId) return;

    const targetNode = cy.getElementById(highlightCompanyId);
    if (!targetNode || targetNode.length === 0) return;

    targetNode.addClass("highlighted");

    if (dimUnrelated) {
      // Neighborhood = connected nodes + edges
      const neighborhood = targetNode.neighborhood();
      cy.nodes()
        .not(targetNode)
        .not(neighborhood)
        .addClass("dimmed");
      cy.edges().not(neighborhood).addClass("dimmed");
    }

    // Center view on highlighted node smoothly
    cy.animate({
      fit: { eles: targetNode.union(targetNode.neighborhood()), padding: 80 },
      duration: 400,
      easing: "ease-out",
    });
  }, [highlightCompanyId, dimUnrelated]);

  if (nodes.length === 0) {
    return (
      <div className="flex h-full w-full items-center justify-center bg-slate-950">
        <div className="text-sm text-slate-500">暂无公司数据</div>
      </div>
    );
  }

  return <div ref={containerRef} className="h-full w-full bg-slate-950" />;
}
