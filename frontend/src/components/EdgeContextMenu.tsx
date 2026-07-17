import { Move, Trash2 } from "lucide-react";
import { useLayoutEffect, useRef } from "react";

interface EdgeContextMenuProps {
  x: number;
  y: number;
  /** 删除连线；只读引擎下不传入即隐藏该项。 */
  onDelete?: () => void;
  onPull?: () => void;
  onClose: () => void;
}

export function EdgeContextMenu({ x, y, onDelete, onPull, onClose }: EdgeContextMenuProps) {
  const menuRef = useRef<HTMLDivElement>(null);
  useLayoutEffect(() => {
    const el = menuRef.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const vw = window.innerWidth;
    const vh = window.innerHeight;
    const padding = 8;
    let left = x;
    let top = y;
    if (left + rect.width > vw - padding) left = vw - rect.width - padding;
    if (left < padding) left = padding;
    if (top + rect.height > vh - padding) top = vh - rect.height - padding;
    if (top < padding) top = padding;
    el.style.left = `${left}px`;
    el.style.top = `${top}px`;
  }, [x, y]);

  return (
    <div
      ref={menuRef}
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
      {onDelete && (
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
      )}
    </div>
  );
}
