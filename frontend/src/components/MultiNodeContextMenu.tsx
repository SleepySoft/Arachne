import { LayoutGrid, X, MousePointerClick, Eye } from "lucide-react";
import { useLayoutEffect, useRef } from "react";

interface MultiNodeContextMenuProps {
  x: number;
  y: number;
  selectedCount: number;
  onAutoArrange: () => void;
  onClearSelection?: () => void;
  onFocusSelected?: () => void;
  onClose: () => void;
}

export function MultiNodeContextMenu({
  x,
  y,
  selectedCount,
  onAutoArrange,
  onClearSelection,
  onFocusSelected,
  onClose,
}: MultiNodeContextMenuProps) {
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
    <>
      {/* Backdrop to capture clicks outside */}
      <div
        className="fixed inset-0 z-40"
        onClick={onClose}
        onContextMenu={() => {
          onClose();
        }}
      />
      <div
        ref={menuRef}
        className="fixed z-50 w-56 rounded-lg border border-slate-700 bg-slate-900 shadow-xl"
        style={{ left: x, top: y }}
      >
        <div className="flex items-center justify-between border-b border-slate-700 px-3 py-2">
          <span className="truncate text-xs font-medium text-slate-200">
            已选择 {selectedCount} 个节点
          </span>
          <button
            onClick={onClose}
            className="rounded p-0.5 text-slate-400 hover:bg-slate-800 hover:text-slate-200"
          >
            <X size={12} />
          </button>
        </div>
        <div className="py-1">
          {onFocusSelected && (
            <button
              onClick={() => {
                onFocusSelected();
                onClose();
              }}
              className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100"
            >
              <Eye size={14} className="text-cyan-400" />
              聚焦选中节点 ({selectedCount})
            </button>
          )}
          <button
            onClick={() => {
              onAutoArrange();
              onClose();
            }}
            className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100"
          >
            <LayoutGrid size={14} className="text-emerald-400" />
            自动排列
          </button>
          {onClearSelection && (
            <button
              onClick={() => {
                onClearSelection();
                onClose();
              }}
              className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100"
            >
              <MousePointerClick size={14} className="text-slate-400" />
              取消选择
            </button>
          )}
        </div>
      </div>
    </>
  );
}
