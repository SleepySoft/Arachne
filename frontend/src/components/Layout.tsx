import { ReactNode } from "react";

interface LayoutProps {
  topBar: ReactNode;
  leftSidebar: ReactNode;
  centerCanvas: ReactNode;
  searchPanel: ReactNode;
  rightPanel: ReactNode;
}

export function Layout({
  topBar,
  leftSidebar,
  centerCanvas,
  searchPanel,
  rightPanel,
}: LayoutProps) {
  return (
    <div className="flex h-full w-full flex-col bg-slate-950">
      {/* TopBar */}
      <div className="h-14 shrink-0 border-b border-slate-800 bg-slate-900">
        {topBar}
      </div>

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
          <div className="w-80 shrink-0 border-l border-slate-800 bg-slate-900 overflow-y-auto">
            {rightPanel}
          </div>
        )}
      </div>
    </div>
  );
}
