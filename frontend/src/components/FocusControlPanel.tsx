import { RefObject } from "react";
import { X, Undo2, ArrowUp, ArrowDown, ArrowLeftRight } from "lucide-react";
import { GraphCanvasRef } from "@/components/GraphCanvas";
import { FocusState } from "@/types/view";

interface FocusControlPanelProps {
  graphCanvasRef: RefObject<GraphCanvasRef | null>;
  focusState: FocusState;
}

export function FocusControlPanel({ graphCanvasRef, focusState }: FocusControlPanelProps) {
  if (!focusState.active) return null;

  const visibleCount = focusState.visibleNodeIds.length;
  const canUndo = focusState.history.length > 0;

  return (
    <div className="pointer-events-auto absolute left-1/2 top-4 z-30 flex -translate-x-1/2 items-center gap-2 rounded-lg border border-slate-700 bg-slate-900/95 px-3 py-2 shadow-xl backdrop-blur">
      <span className="whitespace-nowrap text-xs text-slate-300">
        聚焦 {focusState.seedNodeIds.length} 个节点 · 显示 {visibleCount} 个
      </span>
      <div className="mx-1 h-4 w-px bg-slate-700" />
      <button
        onClick={() => graphCanvasRef.current?.undoFocus()}
        disabled={!canUndo}
        title="撤销一步"
        className="flex items-center gap-1 rounded px-2 py-1 text-xs text-slate-300 hover:bg-slate-800 hover:text-slate-100 disabled:cursor-not-allowed disabled:opacity-40"
      >
        <Undo2 size={12} />
        撤销
      </button>
      <button
        onClick={() => graphCanvasRef.current?.revealMore("upstream", 1)}
        title="从当前边界整体展开一层上游"
        className="flex items-center gap-1 rounded px-2 py-1 text-xs text-slate-300 hover:bg-slate-800 hover:text-slate-100"
      >
        <ArrowUp size={12} className="text-emerald-400" />
        上游 +1
      </button>
      <button
        onClick={() => graphCanvasRef.current?.revealMore("downstream", 1)}
        title="从当前边界整体展开一层下游"
        className="flex items-center gap-1 rounded px-2 py-1 text-xs text-slate-300 hover:bg-slate-800 hover:text-slate-100"
      >
        <ArrowDown size={12} className="text-emerald-400" />
        下游 +1
      </button>
      <button
        onClick={() => graphCanvasRef.current?.revealMore("both", 1)}
        title="从当前边界整体展开一层双向"
        className="flex items-center gap-1 rounded px-2 py-1 text-xs text-slate-300 hover:bg-slate-800 hover:text-slate-100"
      >
        <ArrowLeftRight size={12} className="text-emerald-400" />
        双向 +1
      </button>
      <div className="mx-1 h-4 w-px bg-slate-700" />
      <button
        onClick={() => graphCanvasRef.current?.exitFocus()}
        title="退出聚焦模式"
        className="flex items-center gap-1 rounded px-2 py-1 text-xs text-red-400 hover:bg-slate-800 hover:text-red-300"
      >
        <X size={12} />
        退出
      </button>
    </div>
  );
}
