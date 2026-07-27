import {
  LayoutGrid,
  Network,
  X,
  MousePointerClick,
  Eye,
  EyeOff,
  Building2,
  AlignVerticalJustifyCenter,
  AlignHorizontalJustifyCenter,
  AlignVerticalSpaceBetween,
  AlignHorizontalSpaceBetween,
} from "lucide-react";
import { useLayoutEffect, useRef } from "react";

interface MultiNodeContextMenuProps {
  x: number;
  y: number;
  selectedCount: number;
  onAutoArrange: () => void;
  onSmartArrange?: () => void;
  onAlignHorizontal?: () => void;
  onAlignVertical?: () => void;
  onDistributeHorizontal?: () => void;
  onDistributeVertical?: () => void;
  onClearSelection?: () => void;
  onFocusSelected?: () => void;
  onHideSelected?: () => void;
  onShowCompanies?: () => void;
  onClose: () => void;
}

export function MultiNodeContextMenu({
  x,
  y,
  selectedCount,
  onAutoArrange,
  onSmartArrange,
  onAlignHorizontal,
  onAlignVertical,
  onDistributeHorizontal,
  onDistributeVertical,
  onClearSelection,
  onFocusSelected,
  onHideSelected,
  onShowCompanies,
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

  const canAlign = selectedCount >= 2;
  const canDistribute = selectedCount >= 3;

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
          {onHideSelected && (
            <button
              onClick={() => {
                onHideSelected();
                onClose();
              }}
              className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100"
            >
              <EyeOff size={14} className="text-rose-400" />
              隐藏选中节点 ({selectedCount})
            </button>
          )}

          {onShowCompanies && (
            <button
              onClick={() => {
                onShowCompanies();
                onClose();
              }}
              className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100"
            >
              <Building2 size={14} className="text-cyan-400" />
              查看关联公司
            </button>
          )}

          <div className="my-1 border-t border-slate-800" />

          {onSmartArrange && (
            <button
              onClick={() => {
                onSmartArrange();
                onClose();
              }}
              className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100"
              title="按上下游关系分层排列（Sugiyama/dagre），METHOD 与其 ACTION 同行，未选中节点不动"
            >
              <Network size={14} className="text-cyan-400" />
              智能排列（分层布局）
            </button>
          )}

          <button
            onClick={() => {
              onAutoArrange();
              onClose();
            }}
            className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100"
            title="软斥力去重叠，保持大致位置"
          >
            <LayoutGrid size={14} className="text-emerald-400" />
            自动排列（去重叠）
          </button>

          <button
            disabled={!canAlign}
            onClick={() => {
              onAlignHorizontal?.();
              onClose();
            }}
            className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100 disabled:cursor-not-allowed disabled:opacity-40"
            title={canAlign ? "沿水平线对齐" : "至少需要选择 2 个节点"}
          >
            <AlignVerticalJustifyCenter size={14} className="text-amber-400" />
            水平对齐
          </button>

          <button
            disabled={!canAlign}
            onClick={() => {
              onAlignVertical?.();
              onClose();
            }}
            className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100 disabled:cursor-not-allowed disabled:opacity-40"
            title={canAlign ? "沿垂直线对齐" : "至少需要选择 2 个节点"}
          >
            <AlignHorizontalJustifyCenter size={14} className="text-amber-400" />
            垂直对齐
          </button>

          <button
            disabled={!canDistribute}
            onClick={() => {
              onDistributeHorizontal?.();
              onClose();
            }}
            className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100 disabled:cursor-not-allowed disabled:opacity-40"
            title={canDistribute ? "在水平方向均匀分布" : "至少需要选择 3 个节点"}
          >
            <AlignVerticalSpaceBetween size={14} className="text-violet-400" />
            水平均匀分布
          </button>

          <button
            disabled={!canDistribute}
            onClick={() => {
              onDistributeVertical?.();
              onClose();
            }}
            className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100 disabled:cursor-not-allowed disabled:opacity-40"
            title={canDistribute ? "在垂直方向均匀分布" : "至少需要选择 3 个节点"}
          >
            <AlignHorizontalSpaceBetween size={14} className="text-violet-400" />
            垂直均匀分布
          </button>

          {onClearSelection && (
            <>
              <div className="my-1 border-t border-slate-800" />
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
            </>
          )}
        </div>
      </div>
    </>
  );
}
