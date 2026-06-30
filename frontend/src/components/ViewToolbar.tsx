import { useCallback, useRef, useState } from "react";
import { Download, FolderOpen, Save, Settings2, Upload } from "lucide-react";
import { SavedView, WorkspaceType } from "@/types/view";

interface ViewToolbarProps {
  workspace: WorkspaceType;
  variant?: "boxed" | "inline";
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
  onSave: (name: string) => Omit<SavedView, "id" | "base" | "viewVersion" | "created_at" | "updated_at" | "version"> | null;
  onLoad: (view: SavedView) => void;
  onManage?: () => void;
}

export function ViewToolbar({
  workspace,
  variant = "boxed",
  savedViews,
  onSave,
  onLoad,
  onManage,
}: ViewToolbarProps) {
  const { viewsForWorkspace, saveView, importViews, exportViews } = savedViews;
  const views = viewsForWorkspace(workspace);
  const [open, setOpen] = useState(false);
  const [savePromptOpen, setSavePromptOpen] = useState(false);
  const [name, setName] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSave = useCallback(() => {
    const payload = onSave(name);
    if (payload) {
      saveView(name, workspace, payload);
    }
    setName("");
    setSavePromptOpen(false);
  }, [name, onSave, saveView, workspace]);

  const handleImport = useCallback(
    async (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (!file) return;
      const result = await importViews(file);
      // eslint-disable-next-line no-console
      console.log("Import views:", result);
      if (e.target) e.target.value = "";
    },
    [importViews]
  );

  const buttons = (
    <>
      <button
        onClick={() => setSavePromptOpen(true)}
        title="保存当前视图"
        className="flex items-center gap-1 rounded-md px-2 py-1 text-xs font-medium text-slate-400 transition-colors hover:bg-slate-800 hover:text-slate-200"
      >
        <Save className="h-3.5 w-3.5" />
        <span>保存</span>
      </button>

      <button
        onClick={() => setOpen((v) => !v)}
        title="载入视图"
        className="flex items-center gap-1 rounded-md px-2 py-1 text-xs font-medium text-slate-400 transition-colors hover:bg-slate-800 hover:text-slate-200"
      >
        <FolderOpen className="h-3.5 w-3.5" />
        <span>载入</span>
        {views.length > 0 && (
          <span className="ml-0.5 rounded-full bg-slate-700 px-1.5 py-0 text-[10px] text-slate-300">
            {views.length}
          </span>
        )}
      </button>

      <button
        onClick={() => exportViews(views)}
        title="导出视图"
        className="flex items-center gap-1 rounded-md px-2 py-1 text-xs font-medium text-slate-400 transition-colors hover:bg-slate-800 hover:text-slate-200"
      >
        <Download className="h-3.5 w-3.5" />
        <span>导出</span>
      </button>

      <button
        onClick={() => fileInputRef.current?.click()}
        title="导入视图"
        className="flex items-center gap-1 rounded-md px-2 py-1 text-xs font-medium text-slate-400 transition-colors hover:bg-slate-800 hover:text-slate-200"
      >
        <Upload className="h-3.5 w-3.5" />
        <span>导入</span>
      </button>

      {onManage && (
        <button
          onClick={() => {
            setOpen(false);
            onManage();
          }}
          title="管理视图"
          className="flex items-center gap-1 rounded-md px-2 py-1 text-xs font-medium text-slate-400 transition-colors hover:bg-slate-800 hover:text-slate-200"
        >
          <Settings2 className="h-3.5 w-3.5" />
          <span>管理</span>
        </button>
      )}

      <input
        ref={fileInputRef}
        type="file"
        accept="application/json"
        className="hidden"
        onChange={handleImport}
      />
    </>
  );

  const dropdowns = (
    <>
      {open && (
        <div className="absolute left-0 top-full z-50 mt-2 w-64 rounded-lg border border-slate-700 bg-slate-900/95 p-2 shadow-xl backdrop-blur">
          <div className="mb-1 px-1 text-xs font-medium text-slate-400">已保存视图</div>
          {views.length === 0 ? (
            <div className="px-1 py-2 text-xs text-slate-500">暂无保存的视图</div>
          ) : (
            <ul className="max-h-60 overflow-auto">
              {views.map((view) => (
                <li key={view.id}>
                  <button
                    onClick={() => {
                      onLoad(view);
                      setOpen(false);
                    }}
                    className="w-full rounded-md px-2 py-1.5 text-left text-xs text-slate-300 transition-colors hover:bg-slate-800 hover:text-slate-100"
                    title={`创建于 ${new Date(view.created_at).toLocaleString()}`}
                  >
                    <div className="truncate font-medium">{view.name}</div>
                    <div className="truncate text-[10px] text-slate-500">
                      {new Date(view.updated_at).toLocaleString()}
                    </div>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      {savePromptOpen && (
        <div className="absolute left-0 top-full z-50 mt-2 w-64 rounded-lg border border-slate-700 bg-slate-900/95 p-3 shadow-xl backdrop-blur">
          <div className="mb-2 text-xs font-medium text-slate-300">保存当前视图</div>
          <input
            autoFocus
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleSave();
              if (e.key === "Escape") {
                setName("");
                setSavePromptOpen(false);
              }
            }}
            placeholder="视图名称"
            className="mb-2 w-full rounded-md border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 outline-none placeholder:text-slate-500 focus:border-cyan-600"
          />
          <div className="flex justify-end gap-2">
            <button
              onClick={() => {
                setName("");
                setSavePromptOpen(false);
              }}
              className="rounded-md px-2 py-1 text-xs text-slate-400 hover:text-slate-200"
            >
              取消
            </button>
            <button
              onClick={handleSave}
              disabled={!name.trim()}
              className="rounded-md bg-cyan-700 px-2 py-1 text-xs text-white hover:bg-cyan-600 disabled:opacity-50"
            >
              保存
            </button>
          </div>
        </div>
      )}
    </>
  );

  if (variant === "inline") {
    return (
      <div className="relative flex items-center gap-1">
        {buttons}
        {dropdowns}
      </div>
    );
  }

  return (
    <div className="relative">
      <div className="flex items-center gap-1 rounded-lg border border-slate-700 bg-slate-900/90 p-1 shadow-lg backdrop-blur">
        {buttons}
      </div>
      {dropdowns}
    </div>
  );
}
