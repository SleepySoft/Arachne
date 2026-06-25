import { FilePlus, PlusCircle } from "lucide-react";
import { useLayoutEffect, useRef } from "react";

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
