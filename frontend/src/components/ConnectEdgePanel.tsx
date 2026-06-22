import { X } from "lucide-react";
import { GraphEdge, IndustrialNode } from "@/types";
import { QuickEdgeForm } from "./QuickEdgeForm";

interface ConnectEdgePanelProps {
  source: IndustrialNode;
  target: IndustrialNode;
  x: number;
  y: number;
  onSuccess?: (edge: GraphEdge) => void;
  onClose?: () => void;
  onExpand?: (draft: {
    from_node: string;
    to_node: string;
    edge_type: string;
    description?: string;
    notes?: string;
  }) => void;
}

export function ConnectEdgePanel({
  source,
  target,
  x,
  y,
  onSuccess,
  onClose,
  onExpand,
}: ConnectEdgePanelProps) {
  return (
    <div
      className="fixed z-50 w-80 rounded-lg border border-slate-700 bg-slate-900/95 p-3 shadow-xl backdrop-blur"
      style={{ left: x, top: y }}
    >
      <div className="mb-2 flex items-center justify-between">
        <div className="text-xs font-medium text-cyan-400">创建连线</div>
        {onClose && (
          <button
            onClick={onClose}
            className="rounded p-0.5 text-slate-500 hover:bg-slate-800 hover:text-slate-300"
          >
            <X className="h-3.5 w-3.5" />
          </button>
        )}
      </div>
      <QuickEdgeForm
        anchorNodeId={source.node_id}
        direction="downstream"
        initialTargetNodeId={target.node_id}
        initialTargetNode={target}
        onSuccess={onSuccess}
        onCancel={onClose}
        onExpand={onExpand}
      />
    </div>
  );
}
