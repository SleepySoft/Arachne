import { useCallback, useEffect, useLayoutEffect, useRef, useState } from "react";
import { ChevronLeft, ChevronRight, GripVertical, Undo2 } from "lucide-react";
import { ViewToolbar } from "@/components/ViewToolbar";
import { GraphToolbar } from "@/components/GraphToolbar";
import { ZoomSensitivitySlider } from "./ZoomSensitivitySlider";
import { SavedView, WorkspaceType } from "@/types/view";

interface CanvasToolbarProps {
  workspace: WorkspaceType;
  savedViews: {
    viewsForWorkspace: (workspace: WorkspaceType) => SavedView[];
    saveView: (
      name: string,
      workspace: WorkspaceType,
      payload: Omit<SavedView, "id" | "base" | "viewVersion" | "created_at" | "updated_at" | "version">,
      parentView?: SavedView
    ) => SavedView;
    importViews: (file: File) => Promise<{ imported: number; skipped: number; errors: string[] }>;
    exportViews: (views?: SavedView[]) => void;
  };
  onSaveView: (name: string) => Omit<SavedView, "id" | "base" | "viewVersion" | "created_at" | "updated_at" | "version"> | null;
  onLoadView: (view: SavedView) => void;
  onManageViews?: () => void;
  zoomSensitivity?: number;
  onZoomSensitivityChange?: (value: number) => void;
  parentView?: SavedView;
  onViewSaved?: (view: SavedView) => void;
  canUndo?: boolean;
  onUndo?: () => void;
}

// 收起/展开后始终保留可见的最小区域（像素），确保能被拖回来
const MIN_VISIBLE_W = 60;
const MIN_VISIBLE_H = 28;

export function CanvasToolbar({
  workspace,
  savedViews,
  onSaveView,
  onLoadView,
  onManageViews,
  zoomSensitivity,
  onZoomSensitivityChange,
  parentView,
  onViewSaved,
  canUndo,
  onUndo,
}: CanvasToolbarProps) {
  const [collapsed, setCollapsed] = useState(false);
  const [position, setPosition] = useState({ x: 12, y: 12 });
  const [dragging, setDragging] = useState(false);
  const dragOffsetRef = useRef({ x: 0, y: 0 });
  const toolbarRef = useRef<HTMLDivElement>(null);

  const clampPosition = useCallback((pos: { x: number; y: number }): { x: number; y: number } => {
    const toolbar = toolbarRef.current;
    const container = toolbar?.parentElement;
    if (!toolbar || !container) return pos;

    const containerW = container.clientWidth;
    const containerH = container.clientHeight;
    const toolbarW = toolbar.offsetWidth;
    const toolbarH = toolbar.offsetHeight;

    // 容器很小时，允许工具栏部分移出，但要保留最小可见区域
    const minX = Math.min(0, containerW - MIN_VISIBLE_W);
    const minY = Math.min(0, containerH - MIN_VISIBLE_H);
    const maxX = containerW - toolbarW;
    const maxY = containerH - toolbarH;

    return {
      x: Math.max(minX, Math.min(maxX, pos.x)),
      y: Math.max(minY, Math.min(maxY, pos.y)),
    };
  }, []);

  // 收起/展开或窗口大小变化时，确保工具栏仍在可见区域
  useLayoutEffect(() => {
    setPosition((prev) => clampPosition(prev));
  }, [collapsed, clampPosition]);

  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    // 只有左键能拖动
    if (e.button !== 0) return;
    // 避免点击按钮时触发拖动（事件从 drag handle 冒泡过来时已经过滤 target）
    if (!(e.target as HTMLElement).closest("[data-drag-handle]")) return;
    e.preventDefault();
    e.stopPropagation();

    const rect = toolbarRef.current?.getBoundingClientRect();
    if (!rect) return;

    dragOffsetRef.current = {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    };
    setDragging(true);
  }, []);

  useEffect(() => {
    if (!dragging) return;

    const handleMouseMove = (e: MouseEvent) => {
      const container = toolbarRef.current?.parentElement;
      if (!container) return;
      const containerRect = container.getBoundingClientRect();
      const raw = {
        x: e.clientX - containerRect.left - dragOffsetRef.current.x,
        y: e.clientY - containerRect.top - dragOffsetRef.current.y,
      };
      setPosition(clampPosition(raw));
    };

    const handleMouseUp = () => {
      setDragging(false);
    };

    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  }, [dragging, clampPosition]);

  return (
    <div
      ref={toolbarRef}
      className={`absolute z-20 flex items-center gap-1 rounded-lg border border-slate-700 bg-slate-900/90 p-1 shadow-lg backdrop-blur ${
        dragging ? "cursor-grabbing" : "cursor-default"
      }`}
      style={{
        left: position.x,
        top: position.y,
        userSelect: "none",
      }}
    >
      <button
        data-drag-handle
        onMouseDown={handleMouseDown}
        title="拖动工具栏"
        className="flex cursor-grab items-center rounded-md p-1 text-slate-500 hover:bg-slate-800 hover:text-slate-300"
      >
        <GripVertical className="h-3.5 w-3.5" />
      </button>

      {!collapsed && (
        <>
          <div className="h-4 w-px bg-slate-700" />

          <ViewToolbar
            workspace={workspace}
            variant="inline"
            savedViews={savedViews}
            onSave={onSaveView}
            onLoad={onLoadView}
            onManage={onManageViews}
            parentView={parentView}
            onViewSaved={onViewSaved}
            canUndo={canUndo}
            onUndo={onUndo}
            showUndo={false}
          />

          <GraphToolbar variant="inline" />

          {canUndo !== undefined && onUndo && (
            <>
              <div className="h-4 w-px bg-slate-700" />
              <button
                onClick={onUndo}
                disabled={!canUndo}
                title={canUndo ? "恢复到上一个布局状态 (Ctrl+Z)" : "无可用布局状态"}
                className="flex items-center gap-1 rounded-md px-2 py-1 text-xs font-medium transition-colors disabled:cursor-not-allowed disabled:opacity-40 text-slate-400 hover:bg-slate-800 hover:text-slate-200"
              >
                <Undo2 className="h-3.5 w-3.5" />
                <span>恢复上一个布局</span>
              </button>
            </>
          )}

          {zoomSensitivity !== undefined && onZoomSensitivityChange && (
            <>
              <div className="h-4 w-px bg-slate-700" />
              <ZoomSensitivitySlider
                value={zoomSensitivity}
                onChange={onZoomSensitivityChange}
              />
            </>
          )}
        </>
      )}

      <button
        onClick={() => setCollapsed((v) => !v)}
        title={collapsed ? "展开工具栏" : "收起工具栏"}
        className="flex items-center rounded-md p-1 text-slate-500 hover:bg-slate-800 hover:text-slate-300"
      >
        {collapsed ? (
          <ChevronRight className="h-3.5 w-3.5" />
        ) : (
          <ChevronLeft className="h-3.5 w-3.5" />
        )}
      </button>
    </div>
  );
}
