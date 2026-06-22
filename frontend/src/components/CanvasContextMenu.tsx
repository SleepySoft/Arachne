import { FilePlus, PlusCircle } from "lucide-react";

interface CanvasContextMenuProps {
  x: number;
  y: number;
  onQuickCreate: () => void;
  onFullCreate: () => void;
  onClose: () => void;
}

export function CanvasContextMenu({
  x,
  y,
  onQuickCreate,
  onFullCreate,
  onClose,
}: CanvasContextMenuProps) {
  return (
    <div
      className="fixed z-50 min-w-[140px] rounded-lg border border-slate-700 bg-slate-900/95 py-1 shadow-xl backdrop-blur"
      style={{ left: x, top: y }}
      onMouseLeave={onClose}
    >
      <button
        onClick={() => {
          onQuickCreate();
          onClose();
        }}
        className="flex w-full items-center gap-2 px-3 py-2 text-left text-xs text-slate-200 hover:bg-slate-800"
      >
        <PlusCircle className="h-3.5 w-3.5 text-cyan-400" />
        快速创建节点
      </button>
      <button
        onClick={() => {
          onFullCreate();
          onClose();
        }}
        className="flex w-full items-center gap-2 px-3 py-2 text-left text-xs text-slate-200 hover:bg-slate-800"
      >
        <FilePlus className="h-3.5 w-3.5 text-slate-400" />
        完整创建节点
      </button>
    </div>
  );
}
