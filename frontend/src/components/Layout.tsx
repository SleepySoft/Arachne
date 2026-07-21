import { ReactNode } from "react";

interface LayoutProps {
  topBar?: ReactNode;
  leftSidebar: ReactNode;
  centerCanvas: ReactNode;
  searchPanel: ReactNode;
  rightPanel: ReactNode;
  /** Optional custom width for the right panel (px). */
  rightPanelWidth?: number;
  /** Called when the user drags the right-panel resize handle. */
  onRightPanelResize?: (width: number) => void;
}

export function Layout({
  topBar,
  leftSidebar,
  centerCanvas,
  searchPanel,
  rightPanel,
  rightPanelWidth,
  onRightPanelResize,
}: LayoutProps) {
  const width = rightPanelWidth ?? 320;
  return (
    <div className="flex h-full w-full flex-col bg-slate-950">
      {/* TopBar */}
      {topBar && (
        <div className="h-14 shrink-0 border-b border-slate-800 bg-slate-900">
          {topBar}
        </div>
      )}

      {/* Main area */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Sidebar */}
        <div className="w-56 shrink-0 border-r border-slate-800 bg-slate-900 overflow-y-auto">
          {leftSidebar}
        </div>

        {/* Center */}
        <div className="flex flex-1 flex-col min-w-0">
          {/* Search bar */}
          <div className="shrink-0 border-b border-slate-800 bg-slate-900 p-3">
            {searchPanel}
          </div>

          {/* Canvas */}
          <div className="relative flex-1 overflow-hidden">
            {centerCanvas}
          </div>
        </div>

        {/* Right Panel */}
        {rightPanel && (
          <div
            className="relative shrink-0 border-l border-slate-800 bg-slate-900 overflow-y-auto"
            style={{ width }}
          >
            {onRightPanelResize && (
              <div
                className="absolute left-0 top-0 z-10 h-full w-1 cursor-col-resize bg-transparent hover:bg-cyan-500/50"
                onMouseDown={(e) => {
                  e.preventDefault();
                  const startX = e.clientX;
                  const startWidth = width;
                  const onMove = (ev: MouseEvent) => {
                    const delta = startX - ev.clientX;
                    onRightPanelResize(Math.max(240, Math.min(900, startWidth + delta)));
                  };
                  const onUp = () => {
                    document.removeEventListener("mousemove", onMove);
                    document.removeEventListener("mouseup", onUp);
                  };
                  document.addEventListener("mousemove", onMove);
                  document.addEventListener("mouseup", onUp);
                }}
              />
            )}
            {rightPanel}
          </div>
        )}
      </div>
    </div>
  );
}
