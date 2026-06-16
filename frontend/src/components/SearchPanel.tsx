import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Plus, Search, Upload, Zap, AlertCircle } from "lucide-react";
import { IndustrialNode } from "@/types";
import { listNodes } from "@/services/api";
import { QuickNodeForm } from "./QuickNodeForm";

interface SearchPanelProps {
  onSelectNode: (node: IndustrialNode) => void;
  onCreateNode: () => void;
  onCreateEdge: () => void;
  onUploadBatch: () => void;
}

export function SearchPanel({
  onSelectNode,
  onCreateNode,
  onCreateEdge,
  onUploadBatch,
}: SearchPanelProps) {
  const [query, setQuery] = useState("");
  const [showQuickAdd, setShowQuickAdd] = useState(false);
  const [showDrafts, setShowDrafts] = useState(false);

  const { data: searchData } = useQuery({
    queryKey: ["nodes", 1, 10, undefined, undefined, query],
    queryFn: () => listNodes(1, 10, undefined, undefined, query),
    enabled: query.length >= 1,
  });

  const { data: draftData, refetch: refetchDrafts } = useQuery({
    queryKey: ["nodes", 1, 50, undefined, undefined, undefined, true],
    queryFn: () => listNodes(1, 50, undefined, undefined, undefined, true),
    enabled: showDrafts,
  });

  const hasDrafts = (draftData?.items.length ?? 0) > 0;

  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-center gap-2">
        <div className="relative flex-1">
          <Search className="absolute left-2.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
          <input
            type="text"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              if (e.target.value) setShowDrafts(false);
            }}
            placeholder="搜索节点（名称/别名）..."
            className="w-full rounded-md border border-slate-700 bg-slate-800 py-1.5 pl-8 pr-3 text-sm text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500"
          />
          {searchData && query && !showDrafts && (
            <div className="absolute z-50 mt-1 w-full rounded-md border border-slate-700 bg-slate-800 shadow-lg">
              {searchData.items.length === 0 ? (
                <div className="px-3 py-2 text-sm text-slate-500">无结果</div>
              ) : (
                searchData.items.map((node) => (
                  <button
                    key={node.node_id}
                    onClick={() => {
                      onSelectNode(node);
                      setQuery("");
                      setShowQuickAdd(false);
                    }}
                    className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm hover:bg-slate-700"
                  >
                    <span className="font-medium text-slate-200">
                      {node.canonical_name_zh}
                    </span>
                    <span className="text-xs text-slate-500">{node.node_id}</span>
                    <span className="ml-auto rounded-full bg-slate-700 px-2 py-0.5 text-[10px] text-slate-400">
                      {node.entity_type}
                    </span>
                  </button>
                ))
              )}
              {searchData.items.length === 0 && (
                <button
                  onClick={() => setShowQuickAdd(true)}
                  className="flex w-full items-center gap-1 border-t border-slate-700 px-3 py-2 text-left text-sm text-cyan-400 hover:bg-slate-700"
                >
                  <Zap className="h-3.5 w-3.5" />
                  未找到？快速添加草稿节点
                </button>
              )}
            </div>
          )}

          {showDrafts && (
            <div className="absolute z-50 mt-1 max-h-64 w-full overflow-auto rounded-md border border-slate-700 bg-slate-800 shadow-lg">
              <div className="sticky top-0 flex items-center justify-between border-b border-slate-700 bg-slate-800 px-3 py-2">
                <span className="flex items-center gap-1 text-xs font-medium text-amber-400">
                  <AlertCircle className="h-3.5 w-3.5" />
                  草稿 / 待完善节点
                </span>
                <button
                  onClick={() => setShowDrafts(false)}
                  className="text-[10px] text-slate-500 hover:text-slate-300"
                >
                  关闭
                </button>
              </div>
              {draftData?.items.length === 0 ? (
                <div className="px-3 py-4 text-center text-sm text-slate-500">暂无草稿节点</div>
              ) : (
                draftData?.items.map((node) => (
                  <button
                    key={node.node_id}
                    onClick={() => {
                      onSelectNode(node);
                      setShowDrafts(false);
                    }}
                    className="flex w-full flex-col gap-0.5 border-b border-slate-800 px-3 py-2 text-left text-sm hover:bg-slate-700 last:border-b-0"
                  >
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-slate-200">{node.canonical_name_zh || node.canonical_name_en}</span>
                      <span className="text-[10px] text-slate-500">{node.node_id}</span>
                    </div>
                    <div className="flex items-center gap-2 text-[10px] text-slate-500">
                      <span>{node.entity_type}</span>
                      <span>·</span>
                      <span>{node.status}</span>
                      {!node.definition && <span className="text-amber-500">· 待补定义</span>}
                    </div>
                  </button>
                ))
              )}
            </div>
          )}
        </div>

        <button
          onClick={() => {
            setShowQuickAdd((v) => !v);
            setShowDrafts(false);
            setQuery("");
          }}
          title="快速添加节点"
          className={`flex h-8 w-8 items-center justify-center rounded-md border border-slate-700 bg-slate-800 text-slate-400 transition-colors ${
            showQuickAdd
              ? "border-cyan-600 text-cyan-400"
              : "hover:border-cyan-600 hover:text-cyan-400"
          }`}
        >
          <Zap className="h-4 w-4" />
        </button>

        <button
          onClick={() => {
            setShowDrafts((v) => !v);
            if (!showDrafts) refetchDrafts();
            setShowQuickAdd(false);
            setQuery("");
          }}
          title="查看草稿节点"
          className={`relative flex h-8 w-8 items-center justify-center rounded-md border border-slate-700 bg-slate-800 text-slate-400 transition-colors ${
            showDrafts
              ? "border-amber-600 text-amber-400"
              : "hover:border-amber-600 hover:text-amber-400"
          }`}
        >
          <AlertCircle className="h-4 w-4" />
          {hasDrafts && (
            <span className="absolute -right-1 -top-1 flex h-3.5 w-3.5 items-center justify-center rounded-full bg-amber-500 text-[8px] font-bold text-slate-900">
              {draftData!.items.length > 9 ? "9+" : draftData!.items.length}
            </span>
          )}
        </button>

        <button
          onClick={onCreateNode}
          title="完整创建节点"
          className="flex h-8 w-8 items-center justify-center rounded-md border border-slate-700 bg-slate-800 text-slate-400 hover:border-emerald-600 hover:text-emerald-400"
        >
          <Plus className="h-4 w-4" />
        </button>
        <button
          onClick={onCreateEdge}
          title="创建关系"
          className="flex h-8 w-8 items-center justify-center rounded-md border border-slate-700 bg-slate-800 text-slate-400 hover:border-cyan-600 hover:text-cyan-400"
        >
          <Plus className="h-4 w-4 rotate-45" />
        </button>
        <button
          onClick={onUploadBatch}
          title="批量上传"
          className="flex h-8 w-8 items-center justify-center rounded-md border border-slate-700 bg-slate-800 text-slate-400 hover:border-amber-600 hover:text-amber-400"
        >
          <Upload className="h-4 w-4" />
        </button>
      </div>

      {showQuickAdd && (
        <QuickNodeForm
          initialName={query}
          onSuccess={(node) => {
            onSelectNode(node);
            setShowQuickAdd(false);
            setQuery("");
          }}
          onCancel={() => setShowQuickAdd(false)}
        />
      )}
    </div>
  );
}
