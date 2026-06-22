import { Link2, MousePointer2, RefreshCw } from "lucide-react";
import { EditMode } from "./GraphCanvas";

interface GraphToolbarProps {
  onRelayout?: () => void;
  editMode?: EditMode;
  onToggleEditMode?: () => void;
}

export function GraphToolbar({
  onRelayout,
  editMode = "default",
  onToggleEditMode,
}: GraphToolbarProps) {
  return (
    <div className="absolute left-3 top-3 z-10 flex items-center gap-2 rounded-lg border border-slate-700 bg-slate-900/90 p-1.5 shadow-lg backdrop-blur">
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
      {onToggleEditMode && (
        <button
          onClick={onToggleEditMode}
          title={editMode === "connect" ? "退出连线模式" : "进入连线模式"}
          className={`flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-xs font-medium transition-colors ${
            editMode === "connect"
              ? "bg-cyan-600/20 text-cyan-400 hover:bg-cyan-600/30"
              : "text-slate-400 hover:bg-slate-800 hover:text-slate-200"
          }`}
        >
          {editMode === "connect" ? (
            <>
              <Link2 className="h-3.5 w-3.5" />
              <span>连线中…</span>
            </>
          ) : (
            <>
              <MousePointer2 className="h-3.5 w-3.5" />
              <span>连线</span>
            </>
          )}
        </button>
      )}
    </div>
  );
}
