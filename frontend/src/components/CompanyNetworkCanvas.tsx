import { forwardRef, useCallback, useEffect, useImperativeHandle, useRef } from "react";
import cytoscape from "cytoscape";
import dagre from "cytoscape-dagre";
import { CompanyNetworkNode, CompanyNetworkEdge } from "@/types";

cytoscape.use(dagre);

interface CompanyNetworkCanvasProps {
  restoredCamera?: { pan: { x: number; y: number }; zoom: number };
  nodes: CompanyNetworkNode[];
  edges: CompanyNetworkEdge[];
  onNodeClick?: (company: CompanyNetworkNode) => void;
  onNodeDblClick?: (company: CompanyNetworkNode) => void;
  onEdgeClick?: (edge: CompanyNetworkEdge) => void;
  highlightCompanyId?: string | null;
  dimUnrelated?: boolean;
  previewNodeIds?: string[];
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

/** Map relation_type -> visual style config */
const RELATION_STYLE_MAP: Record<
  string,
  {
    color: string;
    lineStyle: "solid" | "dashed" | "dotted";
    arrowShape: string;
    label: (e: CompanyNetworkEdge) => string;
  }
> = {
  inferred_industrial: {
    color: "#22d3ee",
    lineStyle: "dashed",
    arrowShape: "triangle",
    label: (e) => `产业上游 (${e.path_count})`,
  },
  evidenced_business: {
    color: "#a3e635",
    lineStyle: "solid",
    arrowShape: "triangle",
    label: (e) => {
      const map: Record<string, string> = {
        supplier: "供应商",
        customer: "客户",
        partner: "合作伙伴",
      };
      return `${map[e.relation_subtype || ""] || "业务关系"}${e.path_count > 1 ? ` (${e.path_count})` : ""}`;
    },
  },
  person_relation: {
    color: "#f472b6",
    lineStyle: "dotted",
    arrowShape: "vee",
    label: () => "人事关联",
  },
};

function getRelationStyle(e: CompanyNetworkEdge) {
  return RELATION_STYLE_MAP[e.relation_type || "inferred_industrial"] || RELATION_STYLE_MAP.inferred_industrial;
}

function edgeKey(e: CompanyNetworkEdge) {
  return `${e.from_company_id}→${e.to_company_id}`;
}

function computeManualLayout(
  nodes: CompanyNetworkNode[],
  edges: CompanyNetworkEdge[],
  focusId: string
): Record<string, { x: number; y: number }> {
  const positions: Record<string, { x: number; y: number }> = {};
  const upstreamIds: string[] = [];
  const downstreamIds: string[] = [];

  edges.forEach((e) => {
    if (e.from_company_id === focusId && !downstreamIds.includes(e.to_company_id)) {
      downstreamIds.push(e.to_company_id);
    }
    if (e.to_company_id === focusId && !upstreamIds.includes(e.from_company_id)) {
      upstreamIds.push(e.from_company_id);
    }
  });

  positions[focusId] = { x: 0, y: 0 };

  upstreamIds.forEach((id, i) => {
    const count = upstreamIds.length;
    const spacing = 160;
    const totalWidth = (count - 1) * spacing;
    positions[id] = { x: -totalWidth / 2 + i * spacing, y: -260 };
  });

  downstreamIds.forEach((id, i) => {
    const count = downstreamIds.length;
    const spacing = 160;
    const totalWidth = (count - 1) * spacing;
    positions[id] = { x: -totalWidth / 2 + i * spacing, y: 260 };
  });

  const otherIds = nodes
    .map((n) => n.company_id)
    .filter((id) => id !== focusId && !upstreamIds.includes(id) && !downstreamIds.includes(id));

  otherIds.forEach((id, i) => {
    const row = Math.floor(i / 2);
    const offsetY = i % 2 === 0 ? -90 : 90;
    positions[id] = { x: -420 - row * 220, y: offsetY + row * 40 };
  });

  return positions;
}

export interface CompanyNetworkCanvasRef {
  getCamera: () => { pan: { x: number; y: number }; zoom: number } | null;
  setCamera: (camera: { pan: { x: number; y: number }; zoom: number }) => void;
  getNodePositions: () => Record<string, { x: number; y: number }>;
  setNodePositions: (positions: Record<string, { x: number; y: number }>) => void;
  getContainerSize: () => { width: number; height: number } | null;
}

export const CompanyNetworkCanvas = forwardRef<CompanyNetworkCanvasRef, CompanyNetworkCanvasProps>(function CompanyNetworkCanvas({
  nodes,
  edges,
  onNodeClick,
  onNodeDblClick,
  onEdgeClick,
  highlightCompanyId,
  dimUnrelated,
  previewNodeIds,
  restoredCamera,
  onBeforeDragStart,
  onBeforeCameraChange,
}, ref) {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<cytoscape.Core | null>(null);
  const onNodeClickRef = useRef(onNodeClick);
  const onNodeDblClickRef = useRef(onNodeDblClick);
  const onEdgeClickRef = useRef(onEdgeClick);
  const highlightRef = useRef(highlightCompanyId);
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
    onNodeDblClickRef.current = onNodeDblClick;
  }, [onNodeDblClick]);

  useEffect(() => {
    onEdgeClickRef.current = onEdgeClick;
  }, [onEdgeClick]);

  useEffect(() => {
    highlightRef.current = highlightCompanyId;
  }, [highlightCompanyId]);

  useEffect(() => {
    onBeforeDragStartRef.current = onBeforeDragStart;
  }, [onBeforeDragStart]);

  useEffect(() => {
    onBeforeCameraChangeRef.current = onBeforeCameraChange;
  }, [onBeforeCameraChange]);

  // 初始化 Cytoscape 实例
  useEffect(() => {
    if (!containerRef.current) return;

    const cy = cytoscape({
      container: containerRef.current,
      elements: [],
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
        // Relation types — permanent line styles
        {
          selector: ".relation-inferred_industrial",
          style: {
            "line-color": "#22d3ee",
            "target-arrow-color": "#22d3ee",
            "target-arrow-shape": "triangle",
            "line-style": "dashed",
          },
        },
        {
          selector: ".relation-evidenced_business",
          style: {
            "line-color": "#a3e635",
            "target-arrow-color": "#a3e635",
            "target-arrow-shape": "triangle",
            "line-style": "solid",
          },
        },
        {
          selector: ".relation-person_relation",
          style: {
            "line-color": "#f472b6",
            "target-arrow-color": "#f472b6",
            "target-arrow-shape": "vee",
            "line-style": "dotted",
          },
        },
        // Preview state — only opacity, never line-style
        {
          selector: ".preview",
          style: {
            opacity: 0.35,
            "border-color": "#475569",
          },
        },
        {
          selector: "edge.preview",
          style: {
            opacity: 0.25,
          },
        },
        // Highlighted node
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
        // Dimmed
        {
          selector: ".dimmed",
          style: {
            opacity: 0.08,
          },
        },
        {
          selector: "edge.dimmed",
          style: {
            opacity: 0.03,
          },
        },
        // Selected edge — bright and thick, overrides everything
        {
          selector: "edge:selected",
          style: {
            "line-color": "#facc15",
            "target-arrow-color": "#facc15",
            width: 3.5,
            opacity: 1,
            "z-index": 999,
            "text-background-color": "#1e293b",
            "text-background-opacity": 1,
          },
        },
      ],
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

    cy.on("tap", "edge", (evt) => {
      // Unselect all other edges so only one is highlighted at a time
      cy.edges().unselect();
      evt.target.select();
      const rawData = evt.target.data("raw") as CompanyNetworkEdge;
      if (onEdgeClickRef.current) {
        onEdgeClickRef.current(rawData);
      }
    });

    cy.on("dbltap", "node", (evt) => {
      const rawData = evt.target.data("raw") as CompanyNetworkNode;
      if (onNodeDblClickRef.current) {
        onNodeDblClickRef.current(rawData);
      }
    });

    // 视图历史：拖拽/相机变化通知
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

    return () => {
      cy.destroy();
      cyRef.current = null;
    };
  }, []);

  // 核心变更：节点增删与局部布局动画
  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;

    if (nodes.length === 0) {
      cy.elements().remove();
      return;
    }

    const isLocalMode = !!previewNodeIds && previewNodeIds.length > 0;

    // 清除视图和节点的已有动画队列，防止乱跳
    cy.stop(true, true);
    cy.nodes().stop(true, true);

    const oldPositions: Record<string, { x: number; y: number }> = {};
    cy.nodes().forEach((n) => {
      oldPositions[n.id()] = { ...n.position() };
    });

    const newNodeIds = new Set(nodes.map((n) => n.company_id));
    const existingNodeIds = new Set(cy.nodes().map((n) => n.id()));

    cy.remove(cy.nodes().filter((n) => !newNodeIds.has(n.id())));

    const addedNodes = nodes.filter((n) => !existingNodeIds.has(n.company_id));
    if (addedNodes.length > 0) {
      cy.add(
        addedNodes.map((n) => ({
          data: {
            id: n.company_id,
            label: n.name_zh,
            company_type: n.company_type,
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
        edgesToAdd.map((e) => {
          const style = getRelationStyle(e);
          return {
            data: {
              id: edgeKey(e),
              source: e.from_company_id,
              target: e.to_company_id,
              path_count: e.path_count,
              strength: e.strength,
              label: style.label(e),
              raw: e,
            },
            classes: `relation-${e.relation_type || "inferred_industrial"}`,
          };
        })
      );
    }

    if (isLocalMode && highlightRef.current) {
      const positions = computeManualLayout(nodes, edges, highlightRef.current);

      cy.nodes().forEach((n) => {
        const id = n.id();
        const target = positions[id];
        if (!target) return;

        const current = oldPositions[id];
        if (!current) {
          n.position(target);
        } else {
          n.animate({
            position: target,
            duration: 400,
            easing: "ease-out",
          });
        }
      });

      // 核心修改：只适应焦点和它的上下游节点，不要去 fit 全局，防止随着链条变长画面越缩越小
      const focusNode = cy.getElementById(highlightRef.current);
      const elementsToFit = focusNode.length > 0
        ? focusNode.union(focusNode.neighborhood())
        : cy.nodes();

      cy.animate({
        fit: { eles: elementsToFit, padding: 100 },
        duration: 400,
        easing: "ease-out",
      });
    } else if (!isLocalMode) {
      cy.layout({
        name: "dagre",
        rankDir: "TB",
        nodeSep: 50,
        edgeSep: 20,
        rankSep: 80,
        padding: 20,
        fit: true,
        animate: true,
        animationDuration: 400,
        animationEasing: "ease-out",
      } as cytoscape.LayoutOptions).run();
    }

    // Apply any queued view state after layout animations have had a chance to start/finish.
    setTimeout(() => applyPendingViewState(cy), 450);
  }, [nodes, edges]);

  // Apply restored camera when provided.
  useEffect(() => {
    if (!restoredCamera) return;
    const cy = cyRef.current;
    pendingCameraRef.current = restoredCamera;
    if (cy) applyPendingViewState(cy);
  }, [restoredCamera]);

  // 高亮控制
  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;

    cy.nodes().removeClass("highlighted dimmed");
    cy.edges().removeClass("dimmed");

    if (!highlightCompanyId) return;

    const targetNode = cy.getElementById(highlightCompanyId);
    if (!targetNode || targetNode.length === 0) return;

    targetNode.addClass("highlighted");

    if (dimUnrelated) {
      const neighborhood = targetNode.neighborhood();
      cy.nodes().not(targetNode).not(neighborhood).addClass("dimmed");
      cy.edges().not(neighborhood).addClass("dimmed");
    }

    // 判断是否在局部考察模式中
    const isLocalMode = !!previewNodeIds && previewNodeIds.length > 0;

    // 如果在局部考察模式中，相机移动的控制权完全交给 Layout Hook 避免冲突跳跃
    // 只有在全局模式中单纯点击高亮时，才由 Highlight Hook 进行相机聚焦
    if (!isLocalMode) {
      cy.stop(true, true); // 触发前同样清空队列
      cy.animate({
        fit: { eles: targetNode.union(targetNode.neighborhood()), padding: 80 },
        duration: 400,
        easing: "ease-out",
      });
    }
  }, [highlightCompanyId, dimUnrelated, previewNodeIds]);

  useEffect(() => {
    const cy = cyRef.current;
    if (!cy) return;

    cy.nodes().removeClass("preview");
    cy.edges().removeClass("preview");

    if (!previewNodeIds || previewNodeIds.length === 0) return;

    previewNodeIds.forEach((id) => {
      const node = cy.getElementById(id);
      if (node && node.length > 0) {
        node.addClass("preview");
      }
    });

    cy.edges().forEach((edge) => {
      const src = edge.source().id();
      const tgt = edge.target().id();
      if (previewNodeIds.includes(src) || previewNodeIds.includes(tgt)) {
        edge.addClass("preview");
      }
    });
  }, [previewNodeIds]);

  if (nodes.length === 0) {
    return (
      <div className="flex h-full w-full items-center justify-center bg-slate-950">
        <div className="text-sm text-slate-500">暂无公司数据</div>
      </div>
    );
  }

  return <div ref={containerRef} className="h-full w-full bg-slate-950" />;
});
