import { useQuery } from "@tanstack/react-query";
import { ArrowRight, FileText, History, X } from "lucide-react";
import { listProvStatementsByNode } from "@/services/api";

interface NodeProvPanelProps {
  nodeId: string;
  nodeName: string;
  onClose: () => void;
}

const relationLabel: Record<string, string> = {
  used: "使用了",
  wasGeneratedBy: "由…生成",
  wasDerivedFrom: "派生自",
  wasAttributedTo: "归因于",
  wasAssociatedWith: "关联于",
  actedOnBehalfOf: "代表",
};

export function NodeProvPanel({ nodeId, nodeName, onClose }: NodeProvPanelProps) {
  const { data, isLoading } = useQuery({
    queryKey: ["prov-statements", nodeId],
    queryFn: () => listProvStatementsByNode(nodeId, 1, 100),
    staleTime: 60_000,
  });

  // PROV-N support is deprecated. The raw source view used to call
  // getProvNByNode(nodeId); it is no longer available.
  // const { data: provnText, isLoading: provnLoading } = useQuery({...});

  const items = data?.items ?? [];

  return (
    <div className="flex h-full flex-col bg-slate-900 p-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-slate-200">PROV 来源视图</h3>
        <button
          onClick={onClose}
          className="rounded p-1 text-slate-400 hover:bg-slate-800 hover:text-slate-200"
        >
          <X className="h-3.5 w-3.5" />
        </button>
      </div>

      <div className="mt-2 text-xs text-slate-400">
        节点：
        <span className="font-medium text-slate-300">{nodeName}</span>
        <span className="ml-2 font-mono text-slate-500">{nodeId}</span>
      </div>

      {isLoading && (
        <div className="mt-6 text-center text-xs text-slate-500">加载中…</div>
      )}

      {!isLoading && items.length === 0 && (
        <div className="mt-6 rounded border border-slate-800 bg-slate-850 p-3 text-center text-xs text-slate-500">
          该节点暂无 PROV 声明。
        </div>
      )}

      <div className="mt-4 flex-1 space-y-2 overflow-auto">
        {items.map((stmt) => (
          <div
            key={stmt.statement_id}
            className="rounded border border-slate-800 bg-slate-850 p-2.5"
          >
            <div className="flex items-center gap-2 text-xs">
              <span className="rounded bg-slate-800 px-1.5 py-0.5 font-mono text-slate-300">
                {stmt.node_role}
              </span>
              <span className="font-medium text-cyan-400">
                {relationLabel[stmt.prov_relation] ?? stmt.prov_relation}
              </span>
              <span className="rounded bg-slate-800 px-1.5 py-0.5 font-mono text-slate-300">
                {stmt.target_role}
              </span>
            </div>
            <div className="mt-1.5 flex items-center gap-1.5 font-mono text-xs text-slate-300">
              <span>{stmt.node_id}</span>
              <ArrowRight className="h-3 w-3 text-slate-500" />
              <span>{stmt.target_node_id}</span>
            </div>
            {stmt.notes && (
              <div className="mt-1.5 text-[10px] text-slate-500">{stmt.notes}</div>
            )}
            {stmt.evidence.length > 0 && (
              <div className="mt-2 space-y-1.5 border-t border-slate-800 pt-2">
                {stmt.evidence.map((ev, i) => (
                  <div key={i} className="flex items-start gap-1.5">
                    <FileText className="mt-0.5 h-3 w-3 shrink-0 text-slate-500" />
                    <div className="min-w-0">
                      <div className="text-[10px] font-medium text-slate-400">
                        {ev.source_title}
                      </div>
                      <div className="text-[10px] italic text-slate-600">
                        &ldquo;{ev.quote}&rdquo;
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="mt-3 border-t border-slate-800 pt-2 text-[10px] text-slate-600">
        <History className="mr-1 inline h-3 w-3" />
        PROV 声明为类型级溯源断言，以 JSON 文件形式存储于文件，与产业图边独立。
      </div>
    </div>
  );
}
