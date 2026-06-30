import { useMemo, useState } from "react";
import { SavedView, WorkspaceType } from "@/types/view";

interface ViewManagerModalProps {
  workspace: WorkspaceType;
  savedViews: {
    viewsForWorkspace: (workspace: WorkspaceType) => SavedView[];
    deleteView: (id: string) => void;
    renameView: (id: string, name: string) => void;
    exportViews: (views?: SavedView[]) => void;
    importViews: (file: File) => Promise<{ imported: number; skipped: number; errors: string[] }>;
  };
  onLoad: (view: SavedView) => void;
  onClose: () => void;
}

function formatTime(iso: string) {
  try {
    return new Date(iso).toLocaleString();
  } catch {
    return iso;
  }
}

function shortId(id: string) {
  return id.slice(0, 8);
}

export function ViewManagerModal({ workspace, savedViews, onLoad, onClose }: ViewManagerModalProps) {
  const { viewsForWorkspace, deleteView, renameView, exportViews, importViews } = savedViews;
  const views = viewsForWorkspace(workspace);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editingName, setEditingName] = useState("");
  const [importResult, setImportResult] = useState<string | null>(null);
  const [expandedBases, setExpandedBases] = useState<Set<string>>(() => new Set());

  const grouped = useMemo(() => {
    const map = new Map<string, SavedView[]>();
    views.forEach((v) => {
      const list = map.get(v.base) ?? [];
      list.push(v);
      map.set(v.base, list);
    });
    map.forEach((list) => {
      list.sort((a, b) => {
        if (a.viewVersion !== b.viewVersion) {
          return a.viewVersion - b.viewVersion;
        }
        return new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
      });
    });
    return map;
  }, [views]);

  const toggleBase = (base: string) => {
    setExpandedBases((prev) => {
      const next = new Set(prev);
      if (next.has(base)) {
        next.delete(base);
      } else {
        next.add(base);
      }
      return next;
    });
  };

  const startRename = (view: SavedView) => {
    setEditingId(view.id);
    setEditingName(view.name);
  };

  const confirmRename = (id: string) => {
    renameView(id, editingName);
    setEditingId(null);
  };

  const handleImport = async (file: File) => {
    const result = await importViews(file);
    const parts: string[] = [];
    if (result.imported > 0) parts.push(`导入 ${result.imported} 个`);
    if (result.skipped > 0) parts.push(`跳过 ${result.skipped} 个`);
    if (result.errors.length > 0) parts.push(`${result.errors.length} 个错误`);
    setImportResult(parts.join("，") || "无变化");
    setTimeout(() => setImportResult(null), 4000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <div className="w-full max-w-lg rounded-xl border border-slate-700 bg-slate-900 p-5 shadow-2xl">
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-sm font-semibold text-slate-200">
            {workspace === "industrial" ? "产业图视图" : "公司图视图"}管理
          </h3>
          <button
            onClick={onClose}
            className="text-xs text-slate-400 hover:text-slate-200"
          >
            关闭
          </button>
        </div>

        {views.length === 0 ? (
          <div className="py-6 text-center text-xs text-slate-500">暂无保存的视图</div>
        ) : (
          <ul className="mb-4 max-h-80 overflow-auto rounded-lg border border-slate-800">
            {Array.from(grouped.entries()).map(([base, groupViews]) => {
              const isExpanded = expandedBases.has(base);
              return (
                <li key={base} className="border-b border-slate-800 last:border-b-0">
                  <button
                    onClick={() => toggleBase(base)}
                    className="flex w-full items-center justify-between px-3 py-2 text-left hover:bg-slate-800/50"
                  >
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-medium text-slate-300">
                        {isExpanded ? "▼" : "▶"}
                      </span>
                      <span className="text-xs font-medium text-slate-200">
                        版本链 {shortId(base)}
                      </span>
                      <span className="rounded bg-slate-800 px-1.5 py-0.5 text-[10px] text-slate-400">
                        {groupViews.length} 个版本
                      </span>
                    </div>
                    <span className="text-[10px] text-slate-500">base: {base}</span>
                  </button>
                  {isExpanded && (
                    <ul className="border-t border-slate-800/50 bg-slate-900/50">
                      {groupViews.map((view) => (
                        <li
                          key={view.id}
                          className="flex items-center justify-between gap-2 px-5 py-2 hover:bg-slate-800/30"
                        >
                          <div className="min-w-0 flex-1">
                            {editingId === view.id ? (
                              <input
                                autoFocus
                                type="text"
                                value={editingName}
                                onChange={(e) => setEditingName(e.target.value)}
                                onBlur={() => confirmRename(view.id)}
                                onKeyDown={(e) => {
                                  if (e.key === "Enter") confirmRename(view.id);
                                  if (e.key === "Escape") setEditingId(null);
                                }}
                                className="w-full rounded border border-cyan-700 bg-slate-800 px-1.5 py-0.5 text-xs text-slate-200 outline-none"
                              />
                            ) : (
                              <button
                                onClick={() => startRename(view)}
                                className="block w-full truncate text-left text-xs text-slate-200 hover:text-cyan-400"
                                title="点击重命名"
                              >
                                {view.name}
                              </button>
                            )}
                            <div className="flex flex-wrap items-center gap-x-2 text-[10px] text-slate-500">
                              <span>v{view.viewVersion}</span>
                              <span>uuid: {shortId(view.id)}</span>
                              <span>{formatTime(view.updated_at)}</span>
                            </div>
                          </div>
                          <div className="flex shrink-0 items-center gap-1">
                            <button
                              onClick={() => {
                                onLoad(view);
                                onClose();
                              }}
                              className="rounded bg-cyan-700/20 px-2 py-1 text-[10px] text-cyan-400 hover:bg-cyan-700/30"
                            >
                              载入
                            </button>
                            <button
                              onClick={() => {
                                if (confirm(`删除视图 "${view.name}"？`)) deleteView(view.id);
                              }}
                              className="rounded bg-red-900/20 px-2 py-1 text-[10px] text-red-400 hover:bg-red-900/30"
                            >
                              删除
                            </button>
                          </div>
                        </li>
                      ))}
                    </ul>
                  )}
                </li>
              );
            })}
          </ul>
        )}

        <div className="flex items-center justify-between gap-2">
          <label className="cursor-pointer rounded-md border border-slate-700 bg-slate-800 px-3 py-1.5 text-xs text-slate-300 hover:bg-slate-700">
            导入
            <input
              type="file"
              accept="application/json"
              className="hidden"
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) handleImport(file);
                if (e.target) e.target.value = "";
              }}
            />
          </label>
          <button
            onClick={() => exportViews(views)}
            disabled={views.length === 0}
            className="rounded-md border border-slate-700 bg-slate-800 px-3 py-1.5 text-xs text-slate-300 hover:bg-slate-700 disabled:opacity-40"
          >
            导出
          </button>
        </div>

        {importResult && (
          <div className="mt-3 text-xs text-slate-400">{importResult}</div>
        )}
      </div>
    </div>
  );
}
