import { Building2, Factory, X } from "lucide-react";

interface NodeContextMenuProps {
  x: number;
  y: number;
  nodeName: string;
  onShowCompanies: () => void;
  onShowIndustries: () => void;
  onClose: () => void;
}

export function NodeContextMenu({
  x,
  y,
  nodeName,
  onShowCompanies,
  onShowIndustries,
  onClose,
}: NodeContextMenuProps) {
  return (
    <>
      {/* Backdrop to capture clicks outside */}
      <div
        className="fixed inset-0 z-40"
        onClick={onClose}
        onContextMenu={(e) => {
          e.preventDefault();
          onClose();
        }}
      />
      <div
        className="fixed z-50 w-56 rounded-lg border border-slate-700 bg-slate-900 shadow-xl"
        style={{ left: x, top: y }}
      >
        <div className="flex items-center justify-between border-b border-slate-700 px-3 py-2">
          <span className="truncate text-xs font-medium text-slate-200">
            {nodeName}
          </span>
          <button
            onClick={onClose}
            className="rounded p-0.5 text-slate-400 hover:bg-slate-800 hover:text-slate-200"
          >
            <X size={12} />
          </button>
        </div>
        <div className="py-1">
          <button
            onClick={() => {
              onShowCompanies();
              onClose();
            }}
            className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100"
          >
            <Building2 size={14} className="text-cyan-400" />
            查看关联公司
          </button>
          <button
            onClick={() => {
              onShowIndustries();
              onClose();
            }}
            className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm text-slate-300 hover:bg-slate-800 hover:text-slate-100"
          >
            <Factory size={14} className="text-amber-400" />
            查看关联行业
          </button>
        </div>
      </div>
    </>
  );
}
