import { Move, Trash2 } from "lucide-react";

interface EdgeContextMenuProps {
  x: number;
  y: number;
  onDelete: () => void;
  onPull?: () => void;
  onClose: () => void;
}

export function EdgeContextMenu({ x, y, onDelete, onPull, onClose }: EdgeContextMenuProps) {
  return (
    <div
      className="fixed z-50 min-w-[120px] rounded-lg border border-slate-700 bg-slate-900/95 py-1 shadow-xl backdrop-blur"
      style={{ left: x, top: y }}
      onMouseLeave={onClose}
    >
      {onPull && (
        <button
          onClick={() => {
            onPull();
            onClose();
          }}
          className="flex w-full items-center gap-2 px-3 py-2 text-left text-xs text-slate-300 hover:bg-slate-800"
        >
          <Move className="h-3.5 w-3.5" />
          拉近节点
        </button>
      )}
      <button
        onClick={() => {
          onDelete();
          onClose();
        }}
        className="flex w-full items-center gap-2 px-3 py-2 text-left text-xs text-red-300 hover:bg-slate-800"
      >
        <Trash2 className="h-3.5 w-3.5" />
        删除连线
      </button>
    </div>
  );
}
