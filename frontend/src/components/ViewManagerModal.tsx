import { useMemo, useState } from "react";
import { useServerViews } from "@/hooks/useServerViews";
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
  canManageServerViews: boolean;
}

function formatTime(iso: string | null) {
  if (!iso) return "--";
  try {
    return new Date(iso).toLocaleString();
  } catch {
    return iso;
  }
}

function shortId(id: string) {
  return id.slice(0, 8);
}

export function ViewManagerModal({
  workspace,
  savedViews,
  onLoad,
  onClose,
  canManageServerViews,
}: ViewManagerModalProps) {
  const { viewsForWorkspace, deleteView, renameView, exportViews, importViews } = savedViews;
  const views = viewsForWorkspace(workspace);
  const serverViews = useServerViews(workspace);
  const [tab, setTab] = useState<"local" | "server">("local");
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editingName, setEditingName] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [expandedBases, setExpandedBases] = useState<Set<string>>(() => new Set());

  const grouped = useMemo(() => {
    const map = new Map<string, SavedView[]>();
    views.forEach((view) => {
      const list = map.get(view.base) ?? [];
      list.push(view);
      map.set(view.base, list);
    });
    map.forEach((list) => list.sort((a, b) => a.viewVersion - b.viewVersion));
    return map;
  }, [views]);

  const runServerAction = async (action: () => Promise<unknown>, success: string) => {
    try {
      await action();
      setMessage(success);
    } catch {
      setMessage("操作失败，请检查登录权限或服务状态");
    }
  };

  const handleImport = async (file: File) => {
    const result = await importViews(file);
    const parts: string[] = [];
    if (result.imported > 0) parts.push(`导入 ${result.imported} 个`);
    if (result.skipped > 0) parts.push(`跳过 ${result.skipped} 个`);
    if (result.errors.length > 0) parts.push(`${result.errors.length} 个错误`);
    setMessage(parts.join("，") || "无变化");
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <div className="w-full max-w-2xl rounded-xl border border-slate-700 bg-slate-900 p-5 shadow-2xl">
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-sm font-semibold text-slate-200">
            {workspace === "industrial" ? "产业图视图" : "公司图视图"}管理
          </h3>
          <button onClick={onClose} className="text-xs text-slate-400 hover:text-slate-200">
            关闭
          </button>
        </div>

        <div className="mb-4 flex gap-1 rounded-lg bg-slate-950 p-1">
          {(["local", "server"] as const).map((value) => (
            <button
              key={value}
              onClick={() => setTab(value)}
              className={`flex-1 rounded-md px-3 py-1.5 text-xs ${
                tab === value ? "bg-slate-700 text-slate-100" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {value === "local" ? `本地视图 (${views.length})` : `服务端视图 (${serverViews.data?.length ?? 0})`}
            </button>
          ))}
        </div>

        {tab === "local" ? (
          <>
            {views.length === 0 ? (
              <div className="py-8 text-center text-xs text-slate-500">暂无本地视图</div>
            ) : (
              <ul className="mb-4 max-h-80 overflow-auto rounded-lg border border-slate-800">
                {Array.from(grouped.entries()).map(([base, groupViews]) => {
                  const isExpanded = expandedBases.has(base);
                  return (
                    <li key={base} className="border-b border-slate-800 last:border-b-0">
                      <button
                        onClick={() =>
                          setExpandedBases((previous) => {
                            const next = new Set(previous);
                            if (next.has(base)) next.delete(base);
                            else next.add(base);
                            return next;
                          })
                        }
                        className="flex w-full items-center justify-between px-3 py-2 text-left hover:bg-slate-800/50"
                      >
                        <span className="text-xs text-slate-200">
                          {isExpanded ? "▼" : "▶"} 版本链 {shortId(base)}
                        </span>
                        <span className="text-[10px] text-slate-500">{groupViews.length} 个版本</span>
                      </button>
                      {isExpanded && (
                        <ul className="border-t border-slate-800/50">
                          {groupViews.map((view) => (
                            <li key={view.id} className="flex items-center gap-2 px-5 py-2 hover:bg-slate-800/30">
                              <div className="min-w-0 flex-1">
                                {editingId === view.id ? (
                                  <input
                                    autoFocus
                                    value={editingName}
                                    onChange={(event) => setEditingName(event.target.value)}
                                    onBlur={() => {
                                      renameView(view.id, editingName);
                                      setEditingId(null);
                                    }}
                                    onKeyDown={(event) => {
                                      if (event.key === "Enter") event.currentTarget.blur();
                                      if (event.key === "Escape") setEditingId(null);
                                    }}
                                    className="w-full rounded border border-cyan-700 bg-slate-800 px-1.5 py-0.5 text-xs text-slate-200 outline-none"
                                  />
                                ) : (
                                  <button
                                    onClick={() => {
                                      setEditingId(view.id);
                                      setEditingName(view.name);
                                    }}
                                    className="block w-full truncate text-left text-xs text-slate-200 hover:text-cyan-400"
                                  >
                                    {view.name}
                                  </button>
                                )}
                                <div className="text-[10px] text-slate-500">
                                  v{view.viewVersion} · {formatTime(view.updated_at)}
                                </div>
                              </div>
                              <button
                                onClick={() => { onLoad(view); onClose(); }}
                                className="rounded bg-cyan-700/20 px-2 py-1 text-[10px] text-cyan-400 hover:bg-cyan-700/30"
                              >载入</button>
                              {canManageServerViews && (
                                <button
                                  disabled={serverViews.isMutating}
                                  onClick={() => runServerAction(() => serverViews.createView(view), "已推送到服务端")}
                                  className="rounded bg-emerald-700/20 px-2 py-1 text-[10px] text-emerald-400 hover:bg-emerald-700/30 disabled:opacity-40"
                                >推送</button>
                              )}
                              <button
                                onClick={() => confirm(`删除视图 "${view.name}"？`) && deleteView(view.id)}
                                className="rounded bg-red-900/20 px-2 py-1 text-[10px] text-red-400 hover:bg-red-900/30"
                              >删除</button>
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
                  onChange={(event) => {
                    const file = event.target.files?.[0];
                    if (file) handleImport(file);
                    event.target.value = "";
                  }}
                />
              </label>
              <button
                onClick={() => exportViews(views)}
                disabled={views.length === 0}
                className="rounded-md border border-slate-700 bg-slate-800 px-3 py-1.5 text-xs text-slate-300 hover:bg-slate-700 disabled:opacity-40"
              >导出</button>
            </div>
          </>
        ) : serverViews.isLoading ? (
          <div className="py-8 text-center text-xs text-slate-500">正在加载服务端视图…</div>
        ) : serverViews.isError ? (
          <div className="py-8 text-center text-xs text-red-400">服务端视图加载失败</div>
        ) : (serverViews.data?.length ?? 0) === 0 ? (
          <div className="py-8 text-center text-xs text-slate-500">暂无服务端视图，可从本地视图页推送</div>
        ) : (
          <ul className="max-h-96 overflow-auto rounded-lg border border-slate-800">
            {serverViews.data?.map((serverView) => (
              <li key={serverView.view_id} className="flex items-center gap-2 border-b border-slate-800 px-3 py-3 last:border-b-0 hover:bg-slate-800/30">
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <span className="truncate text-xs font-medium text-slate-200">{serverView.name}</span>
                    {serverView.is_default && (
                      <span className="rounded bg-amber-700/20 px-1.5 py-0.5 text-[10px] text-amber-300">默认</span>
                    )}
                  </div>
                  <div className="text-[10px] text-slate-500">
                    {shortId(serverView.view_id)} · {formatTime(serverView.updated_at)}
                  </div>
                </div>
                <button
                  onClick={() => { onLoad(serverView.view); onClose(); }}
                  className="rounded bg-cyan-700/20 px-2 py-1 text-[10px] text-cyan-400 hover:bg-cyan-700/30"
                >载入</button>
                {canManageServerViews && (
                  <>
                    <button
                      disabled={serverViews.isMutating || serverView.is_default}
                      onClick={() => runServerAction(() => serverViews.setDefaultView(serverView.view_id), "已设为默认视图")}
                      className="rounded bg-amber-700/20 px-2 py-1 text-[10px] text-amber-300 hover:bg-amber-700/30 disabled:opacity-40"
                    >设为默认</button>
                    <button
                      disabled={serverViews.isMutating}
                      onClick={() => {
                        const name = prompt("服务端视图名称：", serverView.name)?.trim();
                        if (name) runServerAction(() => serverViews.renameView(serverView.view_id, name), "已重命名");
                      }}
                      className="rounded bg-slate-700 px-2 py-1 text-[10px] text-slate-300 hover:bg-slate-600 disabled:opacity-40"
                    >重命名</button>
                    <button
                      disabled={serverViews.isMutating}
                      onClick={() => confirm(`删除服务端视图 "${serverView.name}"？`) && runServerAction(() => serverViews.deleteView(serverView.view_id), "已删除")}
                      className="rounded bg-red-900/20 px-2 py-1 text-[10px] text-red-400 hover:bg-red-900/30 disabled:opacity-40"
                    >删除</button>
                  </>
                )}
              </li>
            ))}
          </ul>
        )}

        {message && <div className="mt-3 text-xs text-slate-400">{message}</div>}
        {!canManageServerViews && tab === "server" && (
          <div className="mt-3 text-[10px] text-slate-500">当前账号可载入服务端视图；管理操作需要写权限。</div>
        )}
      </div>
    </div>
  );
}
