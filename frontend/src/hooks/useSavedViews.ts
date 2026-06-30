import { useCallback, useState } from "react";
import { SavedView, SavedViewFile, WorkspaceType } from "@/types/view";

const STORAGE_KEY = "arachne-saved-views";
const CURRENT_VERSION = 2;

function migrateView(v: Partial<SavedView> & { id: string; workspace: WorkspaceType }): SavedView {
  const now = new Date().toISOString();
  return {
    version: v.version ?? 1,
    id: v.id,
    base: v.base ?? v.id,
    viewVersion: v.viewVersion ?? 1,
    name: v.name ?? "未命名视图",
    workspace: v.workspace,
    created_at: v.created_at ?? now,
    updated_at: v.updated_at ?? now,
    industrial: v.industrial,
    company: v.company,
  };
}

function loadViews(): SavedView[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as SavedView[];
    return Array.isArray(parsed)
      ? parsed
          .filter((v) => v && v.id && v.workspace)
          .map((v) => migrateView(v))
      : [];
  } catch {
    return [];
  }
}

function saveToStorage(views: SavedView[]) {
  if (typeof window === "undefined") return;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(views));
}

function generateId(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

export function useSavedViews() {
  const [views, setViews] = useState<SavedView[]>(() => loadViews());

  const saveView = useCallback(
    (
      name: string,
      workspace: WorkspaceType,
      payload: Omit<
        SavedView,
        "id" | "base" | "viewVersion" | "created_at" | "updated_at" | "version"
      >,
      parentView?: SavedView
    ): SavedView => {
      const now = new Date().toISOString();
      const base = parentView?.base ?? generateId();
      const viewVersion = parentView ? parentView.viewVersion + 1 : 1;
      const view: SavedView = {
        version: CURRENT_VERSION,
        id: generateId(),
        base,
        viewVersion,
        created_at: now,
        updated_at: now,
        ...payload,
        name: name.trim() || payload.name || `未命名视图 ${new Date().toLocaleString()}`,
        workspace,
      };
      setViews((prev) => {
        const next = [view, ...prev];
        saveToStorage(next);
        return next;
      });
      return view;
    },
    []
  );

  const deleteView = useCallback((id: string) => {
    setViews((prev) => {
      const next = prev.filter((v) => v.id !== id);
      saveToStorage(next);
      return next;
    });
  }, []);

  const renameView = useCallback((id: string, name: string) => {
    setViews((prev) => {
      const next = prev.map((v) =>
        v.id === id ? { ...v, name: name.trim() || v.name, updated_at: new Date().toISOString() } : v
      );
      saveToStorage(next);
      return next;
    });
  }, []);

  const exportViews = useCallback((targetViews?: SavedView[]) => {
    const exportList = targetViews ?? views;
    const data: SavedViewFile = {
      version: CURRENT_VERSION,
      views: exportList,
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `arachne-views-${new Date().toISOString().slice(0, 10)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    // Delay revoke to ensure the browser has started downloading.
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }, [views]);

  const importViews = useCallback(
    (file: File): Promise<{ imported: number; skipped: number; errors: string[] }> => {
      return new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = () => {
          try {
            const parsed = JSON.parse(reader.result as string) as SavedViewFile | SavedView[];
            const incoming: SavedView[] = Array.isArray(parsed)
              ? parsed
              : parsed?.views ?? [];
            if (!Array.isArray(incoming)) {
              resolve({ imported: 0, skipped: 0, errors: ["文件格式不正确"] });
              return;
            }

            const errors: string[] = [];
            let skipped = 0;
            const valid: SavedView[] = [];

            incoming.forEach((v, index) => {
              if (!v || !v.id || !v.workspace) {
                skipped++;
                return;
              }
              if ((v.version ?? 1) > CURRENT_VERSION) {
                errors.push(`第 ${index + 1} 个视图版本不兼容 (v${v.version})`);
                skipped++;
                return;
              }
              valid.push({
                ...migrateView(v),
                id: generateId(),
                updated_at: v.updated_at || new Date().toISOString(),
              });
            });

            setViews((prev) => {
              const existingIds = new Set(prev.map((v) => v.id));
              const deduped = valid.filter((v) => !existingIds.has(v.id));
              const next = [...deduped, ...prev];
              saveToStorage(next);
              return next;
            });

            resolve({ imported: valid.length, skipped, errors });
          } catch {
            resolve({ imported: 0, skipped: 0, errors: ["无法解析 JSON 文件"] });
          }
        };
        reader.onerror = () =>
          resolve({ imported: 0, skipped: 0, errors: ["读取文件失败"] });
        reader.readAsText(file);
      });
    },
    []
  );

  const viewsForWorkspace = useCallback(
    (workspace: WorkspaceType) => views.filter((v) => v.workspace === workspace),
    [views]
  );

  return {
    views,
    viewsForWorkspace,
    saveView,
    deleteView,
    renameView,
    exportViews,
    importViews,
  };
}
