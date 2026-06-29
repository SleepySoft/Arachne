import {
  Building2,
  Factory,
  X,
  ArrowUp,
  ArrowDown,
  Eye,
  Highlighter,
  FolderOpen,
  Folder,
} from "lucide-react";
import { useLayoutEffect, useRef } from "react";

interface NodeContextMenuProps {
  x: number;
  y: number;
  nodeName: string;
  onShowCompanies: () => void;
  onShowIndustries: () => void;
  onShowUpstream: () => void;
  onShowDownstream: () => void;
  onHighlightUpstream: () => void;
  onHighlightDownstream: () => void;
  onPullUpstream: () => void;
  onPullDownstream: () => void;
  onClose: () => void;
  isGroup?: boolean;
  isExpanded?: boolean;
  onToggleGroup?: () => void;
  inFocusMode?: boolean;
  onFocusNode?: () => void;
  onRevealUpstream?: () => void;
  onRevealDownstream?: () => void;
  onExitFocus?: () => void;
}

export function NodeContextMenu({
  x,
  y,
  nodeName,
  onShowCompanies,
  onShowIndustries,
  onShowUpstream,
  onShowDownstream,
  onHighlightUpstream,
  onHighlightDownstream,
  onPullUpstream,
  onPullDownstream,
  onClose,
  isGroup = false,
  isExpanded = false,
  onToggleGroup,
  inFocusMode = false,
  onFocusNode,
  onRevealUpstream,
  onRevealDownstream,
  onExitFocus,
}: NodeContextMenuProps) {
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
            {nodeName}
          </span>
          <button
            onClick={onClose}
            className="rounded p-0.5 text-slate-400 hover:bg-slate-800 hover:text-slate-200"
          >
            <X size={12} />
          </button>
        </div>
        <div className="py-1">
          {isGroup && (
            <button
              onClick={() => {
                onToggleGroup?.();
                onClose();
              }}
              className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100"
            >
              {isExpanded ? (
                <FolderOpen size={14} className="text-amber-400" />
              ) : (
                <Folder size={14} className="text-amber-400" />
              )}
              {isExpanded ? "收起组" : "展开组"}
            </button>
          )}
          {isGroup && <div className="my-1 border-t border-slate-700" />}
          {!inFocusMode && onFocusNode && (
            <button
              onClick={() => {
                onFocusNode();
                onClose();
              }}
              className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100"
            >
              <Eye size={14} className="text-cyan-400" />
              聚焦此节点
            </button>
          )}
          {inFocusMode && (
            <>
              {onRevealUpstream && (
                <button
                  onClick={() => {
                    onRevealUpstream();
                    onClose();
                  }}
                  className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100"
                >
                  <ArrowUp size={14} className="text-emerald-400" />
                  展开上游一层
                </button>
              )}
              {onRevealDownstream && (
                <button
                  onClick={() => {
                    onRevealDownstream();
                    onClose();
                  }}
                  className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100"
                >
                  <ArrowDown size={14} className="text-emerald-400" />
                  展开下游一层
                </button>
              )}
              {onExitFocus && (
                <button
                  onClick={() => {
                    onExitFocus();
                    onClose();
                  }}
                  className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100"
                >
                  <X size={14} className="text-red-400" />
                  退出聚焦
                </button>
              )}
            </>
          )}
          <div className="my-1 border-t border-slate-700" />
          <button
            onClick={() => {
              onShowUpstream();
              onClose();
            }}
            className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100"
          >
            <ArrowUp size={14} className="text-emerald-400" />
            {inFocusMode ? "展开上游一层" : "显示上游节点"}
          </button>
          <button
            onClick={() => {
              onShowDownstream();
              onClose();
            }}
            className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100"
          >
            <ArrowDown size={14} className="text-emerald-400" />
            {inFocusMode ? "展开下游一层" : "显示下游节点"}
          </button>
          <button
            onClick={() => {
              onHighlightUpstream();
              onClose();
            }}
            className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100"
          >
            <Highlighter size={14} className="text-yellow-400" />
            高亮上游节点
          </button>
          <button
            onClick={() => {
              onHighlightDownstream();
              onClose();
            }}
            className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100"
          >
            <Highlighter size={14} className="text-yellow-400" />
            高亮下游节点
          </button>
          <button
            onClick={() => {
              onPullUpstream();
              onClose();
            }}
            className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100"
          >
            <Eye size={14} className="text-purple-400" />
            拉近上游节点
          </button>
          <button
            onClick={() => {
              onPullDownstream();
              onClose();
            }}
            className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100"
          >
            <Eye size={14} className="text-purple-400" />
            拉近下游节点
          </button>
          <div className="my-1 border-t border-slate-700" />
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
          <button
            onClick={() => {
              onShowIndustries();
              onClose();
            }}
            className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100"
          >
            <Factory size={14} className="text-amber-400" />
            查看关联行业
          </button>
        </div>
      </div>
    </>
  );
}
