import { forwardRef, useCallback, useEffect, useImperativeHandle, useRef } from "react";
import cytoscape from "cytoscape";
// dagre is already registered by CompanyNetworkCanvas

export interface ExplorationNode {
  id: string;
  type: "company" | "material";
  label: string;
  company_type?: string;
  node_type?: string;
  activity_type?: string;
  weight?: number;
}

export interface ExplorationEdge {
  source: string;
  target: string;
  type: "exposure" | "industrial_flow";
  label?: string;
  activity_type?: string;
  edge_type?: string;
  strength?: number;
}

interface ExplorationCanvasProps {
  restoredCamera?: { pan: { x: number; y: number }; zoom: number };
  nodes: ExplorationNode[];
  edges: ExplorationEdge[];
  onNodeClick?: (node: ExplorationNode) => void;
  onEdgeClick?: (edge: ExplorationEdge) => void;
  highlightNodeId?: string | null;
  onBeforeDragStart?: () => void;
  onBeforeCameraChange?: () => void;
}

const COMPANY_TYPE_COLORS: Record<string, string> = {
  public: "#22d3ee",
  private: "#a3e635",
  state_owned: "#f87171",
  startup: "#fbbf24",
  unknown: "#64748b",
};

function edgeKey(e: ExplorationEdge) {
  return `${e.source}→${e.target}`;
}

export interface ExplorationCanvasRef {
  getCamera: () => { pan: { x: number; y: number }; zoom: number } | null;
  setCamera: (camera: { pan: { x: number; y: number }; zoom: number }) => void;
  getNodePositions: () => Record<string, { x: number; y: number }>;
  setNodePositions: (positions: Record<string, { x: number; y: number }>) => void;
  getContainerSize: () => { width: number; height: number } | null;
}

export const ExplorationCanvas = forwardRef<ExplorationCanvasRef, ExplorationCanvasProps>(function ExplorationCanvas({
  nodes,
  edges,
  onNodeClick,
  onEdgeClick,
  highlightNodeId,
  restoredCamera,
  onBeforeDragStart,
  onBeforeCameraChange,
}, ref) {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<cytoscape.Core | null>(null);
  const onNodeClickRef = useRef(onNodeClick);
  const onEdgeClickRef = useRef(onEdgeClick);
  const highlightRef = useRef(highlightNodeId);
  const onBeforeDragStartRef = useRef(onBeforeDragStart);
  const onBeforeCameraChangeRef = useRef(onBeforeCameraChange);
  const pendingPositionsRef = useRef<Record<string, { x: number; y: number }> | null>(null);
  const pendingCameraRef = useRef<{ pan: { x: number; y: number }; zoom: number } | null>(null);

  const applyPendingViewState = useCallback((cy: cytoscape.Core) => {
    const positions = pendingPositionsRef.current;
    const camera = pendingCameraRef.current;

    if (positions && Object.keys(positions).length > 0) {
      cy.batch(() => {
        cy.nodes().forEach((n) => {
          const pos = positions[n.id()];
          if (pos) n.position(pos);
        });
      });
    }

    if (camera) {
      cy.pan(camera.pan);
      cy.zoom(camera.zoom);
    }

    pendingPositionsRef.current = null;
    pendingCameraRef.current = null;
  }, []);

  useImperativeHandle(ref, () => ({
    getCamera: () => {
      const cy = cyRef.current;
      if (!cy) return null;
      return { pan: cy.pan(), zoom: cy.zoom() };
    },
    setCamera: (camera) => {
      const cy = cyRef.current;
      if (cy) {
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
      pendingPositionsRef.current = positions;
      if (cy) applyPendingViewState(cy);
    },
  }));

  useEffect(() => {
    onNodeClickRef.current = onNodeClick;
  }, [onNodeClick]);

  useEffect(() => {
    onEdgeClickRef.current = onEdgeClick;
  }, [onEdgeClick]);

  useEffect(() => {
    highlightRef.current = highlightNodeId;
  }, [highlightNodeId]);

  useEffect(() => {
    onBeforeDragStartRef.current = onBeforeDragStart;
  }, [onBeforeDragStart]);

  useEffect(() => {
    onBeforeCameraChangeRef.current = onBeforeCameraChange;
  }, [onBeforeCameraChange]);

  // Initialize Cytoscape
  useEffect(() => {
    if (!containerRef.current) return;

    const cy = cytoscape({
      container: containerRef.current,
      elements: [],
      style: [
        {
          selector: "node",
          style: {
            "border-width": 2,
            "border-color": "#1e293b",
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
        // Company nodes: circle
        {
          selector: "node[type='company']",
          style: {
            shape: "ellipse",
            width: 36,
            height: 36,
            "background-color": (ele: cytoscape.NodeSingular) =>
              COMPANY_TYPE_COLORS[ele.data("company_type")] || "#64748b",
          },
        },
        // Material nodes: round-rectangle
        {
          selector: "node[type='material']",
          style: {
            shape: "roundrectangle",
            width: (ele: cytoscape.NodeSingular) => Math.max(80, (ele.data("label") || "").length * 8 + 16),
            height: 28,
            "background-color": "#f59e0b",
            "background-opacity": 0.2,
            "border-color": "#f59e0b",
            "border-width": 1.5,
            color: "#fbbf24",
            "font-size": "9px",
          },
        },
        // Anchor company: larger
        {
          selector: "node[anchor='true']",
          style: {
            width: 48,
            height: 48,
            "border-width": 3,
            "border-color": "#facc15",
            "font-size": "12px",
            "font-weight": "bold",
          },
        },
        {
          selector: "edge",
          style: {
            "arrow-scale": 0.8,
            width: 1.5,
            "curve-style": "bezier",
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
        // Exposure edge: dashed, no arrow
        {
          selector: "edge[type='exposure']",
          style: {
            "line-color": "#64748b",
            "line-style": "dashed",
            "target-arrow-shape": "none",
          },
        },
        // Industrial flow edge: solid with arrow
        {
          selector: "edge[type='industrial_flow']",
          style: {
            "line-color": "#38bdf8",
            "target-arrow-color": "#38bdf8",
            "target-arrow-shape": "triangle",
            "line-style": "solid",
          },
        },
        // Highlighted node
        {
          selector: ".highlighted",
          style: {
            "border-color": "#facc15",
            "border-width": 4,
            "z-index": 999,
          },
        },
        // Selected edge
        {
          selector: "edge:selected",
          style: {
            "line-color": "#facc15",
            "target-arrow-color": "#facc15",
            width: 3.5,
            opacity: 1,
            "z-index": 999,
          },
        },
      ],
      wheelSensitivity: 1.0,
      minZoom: 0.2,
      maxZoom: 3,
    });

    cy.on("tap", "node", (evt) => {
      const rawData = evt.target.data("raw") as ExplorationNode;
      if (onNodeClickRef.current) {
        onNodeClickRef.current(rawData);
      }
    });

    cy.on("tap", "edge", (evt) => {
      cy.edges().unselect();
      evt.target.select();
      const rawData = evt.target.data("raw") as ExplorationEdge;
      if (onEdgeClickRef.current) {
        onEdgeClickRef.current(rawData);
      }
    });

    cy.on("grab", "node", () => {
      onBeforeDragStartRef.current?.();
    });

    let cameraTimer: number | null = null;
    let cameraPushed = false;
    const notifyCameraChange = () => {
      if (!cameraPushed) {
        onBeforeCameraChangeRef.current?.();
        cameraPushed = true;
      }
      if (cameraTimer) window.clearTimeout(cameraTimer);
      cameraTimer = window.setTimeout(() => {
        cameraTimer = null;
        cameraPushed = false;
      }, 300);
    };
    cy.on("pan zoom", notifyCameraChange);

    cyRef.current = cy;

    return () => {
      cy.destroy();
      if (cameraTimer) window.clearTimeout(cameraTimer);
      cyRef.current = null;
    };
  }, []);

  // Update elements
  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;

    if (nodes.length === 0) {
      cy.elements().remove();
      return;
    }

    cy.stop(true, true);

    const newNodeIds = new Set(nodes.map((n) => n.id));
    const existingNodeIds = new Set(cy.nodes().map((n) => n.id()));

    cy.remove(cy.nodes().filter((n) => !newNodeIds.has(n.id())));

    const addedNodes = nodes.filter((n) => !existingNodeIds.has(n.id));
    if (addedNodes.length > 0) {
      cy.add(
        addedNodes.map((n) => ({
          data: {
            id: n.id,
            label: n.label,
            type: n.type,
            company_type: n.company_type,
            node_type: n.node_type,
            activity_type: n.activity_type,
            weight: n.weight,
            anchor: n.id === highlightRef.current,
            raw: n,
          },
        }))
      );
    }

    const newEdgeKeys = new Set(edges.map(edgeKey));
    cy.edges().forEach((edge) => {
      const key = `${edge.source().id()}→${edge.target().id()}`;
      if (!newEdgeKeys.has(key)) {
        cy.remove(edge);
      }
    });

    const existingEdgeKeys = new Set(
      cy.edges().map((e) => `${e.source().id()}→${e.target().id()}`)
    );
    const edgesToAdd = edges.filter((e) => !existingEdgeKeys.has(edgeKey(e)));
    if (edgesToAdd.length > 0) {
      cy.add(
        edgesToAdd.map((e) => ({
          data: {
            id: edgeKey(e),
            source: e.source,
            target: e.target,
            type: e.type,
            label: e.label,
            activity_type: e.activity_type,
            edge_type: e.edge_type,
            strength: e.strength,
            raw: e,
          },
        }))
      );
    }

    // Run dagre layout
    (cy.layout({
      name: "dagre",
      rankDir: "TB",
      nodeSep: 60,
      edgeSep: 20,
      rankSep: 100,
      padding: 20,
      fit: true,
      animate: true,
      animationDuration: 400,
      animationEasing: "ease-out",
    } as cytoscape.LayoutOptions)).run();

    // Highlight
    cy.nodes().removeClass("highlighted");
    if (highlightRef.current) {
      const target = cy.getElementById(highlightRef.current);
      if (target && target.length > 0) {
        target.addClass("highlighted");
      }
    }

    setTimeout(() => applyPendingViewState(cy), 450);
  }, [nodes, edges]);

  // Apply restored camera when provided.
  useEffect(() => {
    if (!restoredCamera) return;
    const cy = cyRef.current;
    pendingCameraRef.current = restoredCamera;
    if (cy) applyPendingViewState(cy);
  }, [restoredCamera]);

  // Highlight effect
  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;
    cy.nodes().removeClass("highlighted");
    if (highlightNodeId) {
      const target = cy.getElementById(highlightNodeId);
      if (target && target.length > 0) {
        target.addClass("highlighted");
      }
    }
  }, [highlightNodeId]);

    return (
      <div className="relative h-full w-full bg-slate-950">
        <div ref={containerRef} className="h-full w-full" />

        {nodes.length === 0 && (
          <div className="pointer-events-none absolute inset-0 flex items-center justify-center bg-slate-950">
            <div className="text-sm text-slate-500">选择一个公司开始探索</div>
          </div>
        )}
      </div>
    );
});
