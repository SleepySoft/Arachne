import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Plus, Search, Upload } from "lucide-react";
import { IndustrialNode } from "@/types";
import { listNodes } from "@/services/api";

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
  const { data } = useQuery({
    queryKey: ["nodes", 1, 10, undefined, undefined, query],
    queryFn: () => listNodes(1, 10, undefined, undefined, query),
    enabled: query.length >= 1,
  });

  return (
    <div className="flex items-center gap-2">
      <div className="relative flex-1">
        <Search className="absolute left-2.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="搜索节点（名称/别名）..."
          className="w-full rounded-md border border-slate-700 bg-slate-800 py-1.5 pl-8 pr-3 text-sm text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none focus:ring-1 focus:ring-cyan-500"
        />
        {data && query && (
          <div className="absolute z-50 mt-1 w-full rounded-md border border-slate-700 bg-slate-800 shadow-lg">
            {data.items.length === 0 ? (
              <div className="px-3 py-2 text-sm text-slate-500">无结果</div>
            ) : (
              data.items.map((node) => (
                <button
                  key={node.node_id}
                  onClick={() => {
                    onSelectNode(node);
                    setQuery("");
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
          </div>
        )}
      </div>

      <button
        onClick={onCreateNode}
        title="创建节点"
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
  );
}
