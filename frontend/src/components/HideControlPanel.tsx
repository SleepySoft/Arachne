import { X, EyeOff } from "lucide-react";
import { HideState } from "@/types/view";

interface HideControlPanelProps {
  hideState: HideState;
  onClearHide: () => void;
}

export function HideControlPanel({ hideState, onClearHide }: HideControlPanelProps) {
  if (!hideState.active || hideState.hiddenNodeIds.length === 0) return null;

  return (
    <div className="pointer-events-auto absolute left-1/2 top-16 z-30 flex -translate-x-1/2 items-center gap-2 rounded-lg border border-slate-700 bg-slate-900/95 px-3 py-2 shadow-xl backdrop-blur">
      <EyeOff size={12} className="text-rose-400" />
      <span className="whitespace-nowrap text-xs text-slate-300">
        已隐藏 {hideState.hiddenNodeIds.length} 个节点
      </span>
      <div className="mx-1 h-4 w-px bg-slate-700" />
      <button
        onClick={onClearHide}
        title="取消隐藏"
        className="flex items-center gap-1 rounded px-2 py-1 text-xs text-slate-300 hover:bg-slate-800 hover:text-slate-100"
      >
        <X size={12} />
        取消隐藏
      </button>
    </div>
  );
}
