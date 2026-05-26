import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { X, Users, ArrowUp, ArrowDown, Check } from "lucide-react";
import { getMaterialCompanies } from "@/services/api";

interface SelectedCompany {
  id: string;
  label: string;
  direction: "peer" | "upstream" | "downstream";
  via_node_id?: string;
  via_node_name?: string;
  activity_type: string;
}

interface MaterialConnectionPanelProps {
  nodeId: string;
  nodeName: string;
  anchorCompanyId: string;
  isOpen: boolean;
  onClose: () => void;
  onAddCompanies: (companies: SelectedCompany[]) => void;
}

export function MaterialConnectionPanel({
  nodeId,
  nodeName,
  anchorCompanyId,
  isOpen,
  onClose,
  onAddCompanies,
}: MaterialConnectionPanelProps) {
  const { data, isLoading } = useQuery({
    queryKey: ["material-companies", nodeId, anchorCompanyId],
    queryFn: () => getMaterialCompanies(nodeId, anchorCompanyId),
    enabled: isOpen,
  });

  const [selected, setSelected] = useState<Map<string, SelectedCompany>>(new Map());

  if (!isOpen) return null;

  const toggleCompany = (
    id: string,
    label: string,
    direction: "peer" | "upstream" | "downstream",
    activity_type: string,
    via_node_id?: string,
    via_node_name?: string
  ) => {
    setSelected((prev) => {
      const next = new Map(prev);
      const key = `${id}:${direction}`;
      if (next.has(key)) {
        next.delete(key);
      } else {
        next.set(key, { id, label, direction, via_node_id, via_node_name, activity_type });
      }
      return next;
    });
  };

  const handleAdd = () => {
    onAddCompanies(Array.from(selected.values()));
    setSelected(new Map());
    onClose();
  };

  const renderList = (
    items: { id: string; label: string; activity_type: string; weight: number; via_node_id?: string; via_node_name?: string }[],
    direction: "peer" | "upstream" | "downstream"
  ) => {
    if (items.length === 0) {
      return <div className="py-3 text-center text-[10px] text-slate-500">暂无数据</div>;
    }
    return (
      <div className="space-y-0.5">
        {items.map((item) => {
          const key = `${item.id}:${direction}`;
          const isChecked = selected.has(key);
          return (
            <label
              key={key}
              className={`flex cursor-pointer items-center gap-2 rounded px-2 py-1.5 transition-colors ${
                isChecked ? "bg-cyan-900/20" : "hover:bg-slate-800"
              }`}
            >
              <input
                type="checkbox"
                checked={isChecked}
                onChange={() =>
                  toggleCompany(
                    item.id,
                    item.label,
                    direction,
                    item.activity_type,
                    item.via_node_id,
                    item.via_node_name
                  )
                }
                className="h-3.5 w-3.5 rounded border-slate-600 bg-slate-800 text-cyan-500"
              />
              <span className="flex-1 text-xs text-slate-200">{item.label}</span>
              <span className="text-[10px] text-slate-500">{item.activity_type}</span>
              {item.weight !== undefined && (
                <span className="text-[10px] text-slate-600">{(item.weight * 100).toFixed(0)}%</span>
              )}
            </label>
          );
        })}
      </div>
    );
  };

  const peers = data?.peers ?? [];
  const upstream = data?.upstream ?? [];
  const downstream = data?.downstream ?? [];

  return (
    <div className="fixed right-0 top-0 z-40 flex h-full w-80 flex-col border-l border-slate-700 bg-slate-900/95 shadow-xl">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-700 px-4 py-3">
        <div>
          <h3 className="text-sm font-semibold text-slate-100">{nodeName}</h3>
          <p className="text-[10px] text-slate-500">选择关联公司添加到视图</p>
        </div>
        <button
          onClick={onClose}
          className="flex h-7 w-7 items-center justify-center rounded text-slate-400 hover:bg-slate-800 hover:text-slate-200"
        >
          <X className="h-4 w-4" />
        </button>
      </div>

      {/* Body */}
      <div className="flex-1 overflow-y-auto p-3 space-y-3">
        {isLoading ? (
          <div className="py-4 text-center text-xs text-slate-500">加载中...</div>
        ) : (
          <>
            {/* Peers */}
            <div className="rounded border border-slate-800">
              <div className="flex items-center gap-1.5 border-b border-slate-800 bg-slate-800/30 px-3 py-2">
                <Users className="h-3.5 w-3.5 text-purple-400" />
                <span className="text-xs font-medium text-slate-200">同行</span>
                <span className="ml-auto text-[10px] text-slate-500">{peers.length}</span>
              </div>
              <div className="p-2">{renderList(peers, "peer")}</div>
            </div>

            {/* Upstream */}
            <div className="rounded border border-slate-800">
              <div className="flex items-center gap-1.5 border-b border-slate-800 bg-slate-800/30 px-3 py-2">
                <ArrowUp className="h-3.5 w-3.5 text-amber-400" />
                <span className="text-xs font-medium text-slate-200">上游</span>
                <span className="ml-auto text-[10px] text-slate-500">{upstream.length}</span>
              </div>
              <div className="p-2">{renderList(upstream, "upstream")}</div>
            </div>

            {/* Downstream */}
            <div className="rounded border border-slate-800">
              <div className="flex items-center gap-1.5 border-b border-slate-800 bg-slate-800/30 px-3 py-2">
                <ArrowDown className="h-3.5 w-3.5 text-emerald-400" />
                <span className="text-xs font-medium text-slate-200">下游</span>
                <span className="ml-auto text-[10px] text-slate-500">{downstream.length}</span>
              </div>
              <div className="p-2">{renderList(downstream, "downstream")}</div>
            </div>
          </>
        )}
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between border-t border-slate-700 px-4 py-3">
        <span className="text-xs text-slate-400">
          已选 <span className="font-medium text-cyan-400">{selected.size}</span>
        </span>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setSelected(new Map())}
            className="rounded px-3 py-1.5 text-xs text-slate-400 hover:bg-slate-800"
          >
            清空
          </button>
          <button
            onClick={handleAdd}
            disabled={selected.size === 0}
            className="flex items-center gap-1 rounded bg-cyan-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-cyan-500 disabled:opacity-40"
          >
            <Check className="h-3 w-3" />
            添加
          </button>
        </div>
      </div>
    </div>
  );
}
