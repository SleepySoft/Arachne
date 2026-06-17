import { Eye, EyeOff, RefreshCw } from "lucide-react";

interface GraphToolbarProps {
  showWeakOntology: boolean;
  onToggleWeakOntology: () => void;
  onRelayout?: () => void;
}

export function GraphToolbar({
  showWeakOntology,
  onToggleWeakOntology,
  onRelayout,
}: GraphToolbarProps) {
  return (
    <div className="absolute left-3 top-3 z-10 flex items-center gap-2 rounded-lg border border-slate-700 bg-slate-900/90 p-1.5 shadow-lg backdrop-blur">
      <button
        onClick={onToggleWeakOntology}
        title={showWeakOntology ? "隐藏弱本体关系" : "显示弱本体关系"}
        className={`flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-xs font-medium transition-colors ${
          showWeakOntology
            ? "bg-amber-500/20 text-amber-300 hover:bg-amber-500/30"
            : "text-slate-400 hover:bg-slate-800 hover:text-slate-200"
        }`}
      >
        {showWeakOntology ? (
          <Eye className="h-3.5 w-3.5" />
        ) : (
          <EyeOff className="h-3.5 w-3.5" />
        )}
        <span>弱本体关系</span>
      </button>

      {onRelayout && (
        <button
          onClick={onRelayout}
          title="重新布局"
          className="flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-xs font-medium text-slate-400 transition-colors hover:bg-slate-800 hover:text-slate-200"
        >
          <RefreshCw className="h-3.5 w-3.5" />
          <span>重排</span>
        </button>
      )}
    </div>
  );
}
