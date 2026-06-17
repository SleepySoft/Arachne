import { RefreshCw } from "lucide-react";

interface GraphToolbarProps {
  onRelayout?: () => void;
}

export function GraphToolbar({
  onRelayout,
}: GraphToolbarProps) {
  if (!onRelayout) return null;

  return (
    <div className="absolute left-3 top-3 z-10 flex items-center gap-2 rounded-lg border border-slate-700 bg-slate-900/90 p-1.5 shadow-lg backdrop-blur">
      <button
        onClick={onRelayout}
        title="重新布局"
        className="flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-xs font-medium text-slate-400 transition-colors hover:bg-slate-800 hover:text-slate-200"
      >
        <RefreshCw className="h-3.5 w-3.5" />
        <span>重排</span>
      </button>
    </div>
  );
}
