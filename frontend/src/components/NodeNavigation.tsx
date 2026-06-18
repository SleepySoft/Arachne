import { useState } from "react";
import { ChevronLeft, ChevronRight, History, X, Trash2 } from "lucide-react";
import { IndustrialNode } from "@/types";

interface NodeNavigationProps {
  enabled: boolean;
  history: IndustrialNode[];
  currentIndex: number;
  canGoBack: boolean;
  canGoForward: boolean;
  onBack: () => void;
  onForward: () => void;
  onGoto: (index: number) => void;
  onToggleEnabled: () => void;
  onClear: () => void;
}

export function NodeNavigation({
  enabled,
  history,
  currentIndex,
  canGoBack,
  canGoForward,
  onBack,
  onForward,
  onGoto,
  onToggleEnabled,
  onClear,
}: NodeNavigationProps) {
  const [showHistory, setShowHistory] = useState(false);

  if (!enabled) {
    return (
      <button
        onClick={onToggleEnabled}
        className="rounded-md bg-slate-800 px-2 py-1 text-[10px] text-slate-400 hover:bg-slate-700 hover:text-cyan-400"
        title="开启节点导航"
      >
        开启节点导航
      </button>
    );
  }

  return (
    <>
      <div className="flex items-center gap-1 rounded-md border border-slate-700 bg-slate-800/50 p-0.5">
        <button
          onClick={onBack}
          disabled={!canGoBack}
          className="flex h-6 w-6 items-center justify-center rounded text-slate-300 hover:bg-slate-700 hover:text-cyan-400 disabled:cursor-not-allowed disabled:text-slate-600"
          title="上一个节点"
        >
          <ChevronLeft className="h-4 w-4" />
        </button>
        <button
          onClick={onForward}
          disabled={!canGoForward}
          className="flex h-6 w-6 items-center justify-center rounded text-slate-300 hover:bg-slate-700 hover:text-cyan-400 disabled:cursor-not-allowed disabled:text-slate-600"
          title="下一个节点"
        >
          <ChevronRight className="h-4 w-4" />
        </button>
        <button
          onClick={() => setShowHistory(true)}
          disabled={history.length === 0}
          className="flex h-6 w-6 items-center justify-center rounded text-slate-300 hover:bg-slate-700 hover:text-cyan-400 disabled:cursor-not-allowed disabled:text-slate-600"
          title="浏览历史"
        >
          <History className="h-3.5 w-3.5" />
        </button>
        <button
          onClick={onToggleEnabled}
          className="flex h-6 w-6 items-center justify-center rounded text-slate-400 hover:bg-slate-700 hover:text-red-400"
          title="关闭节点导航"
        >
          <X className="h-3 w-3" />
        </button>
      </div>

      {showHistory && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/70 backdrop-blur-sm">
          <div className="w-full max-w-md rounded-lg border border-slate-700 bg-slate-900 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-800 px-4 py-3">
              <h3 className="text-sm font-semibold text-slate-200">节点浏览历史</h3>
              <div className="flex items-center gap-1">
                <button
                  onClick={onClear}
                  disabled={history.length === 0}
                  className="flex h-6 w-6 items-center justify-center rounded text-slate-500 hover:bg-slate-800 hover:text-red-400 disabled:text-slate-700"
                  title="清空历史"
                >
                  <Trash2 className="h-3 w-3" />
                </button>
                <button
                  onClick={() => setShowHistory(false)}
                  className="flex h-6 w-6 items-center justify-center rounded text-slate-500 hover:bg-slate-800 hover:text-slate-200"
                >
                  <X className="h-3 w-3" />
                </button>
              </div>
            </div>
            <div className="max-h-[60vh] overflow-y-auto p-2">
              {history.length === 0 ? (
                <div className="py-4 text-center text-xs text-slate-500">暂无浏览记录</div>
              ) : (
                <div className="space-y-1">
                  {history.map((n, i) => (
                    <button
                      key={`${n.node_id}-${i}`}
                      onClick={() => {
                        onGoto(i);
                        setShowHistory(false);
                      }}
                      className={`flex w-full items-center gap-2 rounded px-2 py-1.5 text-left text-xs ${
                        i === currentIndex
                          ? "bg-cyan-600/20 text-cyan-400"
                          : "text-slate-300 hover:bg-slate-800"
                      }`}
                    >
                      <span className="w-5 shrink-0 text-[10px] text-slate-500">{i + 1}</span>
                      <span className="truncate font-medium">{n.canonical_name_zh}</span>
                      <span className="ml-auto shrink-0 text-[10px] text-slate-500">{n.node_id}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>
            <div className="border-t border-slate-800 px-4 py-2 text-[10px] text-slate-500">
              提示：点击新节点会截断当前位置之后的历史记录。
            </div>
          </div>
        </div>
      )}
    </>
  );
}
