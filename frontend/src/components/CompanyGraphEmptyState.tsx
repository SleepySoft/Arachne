import { Network, Globe } from "lucide-react";

interface CompanyGraphEmptyStateProps {
  companyCount?: number;
  relationCount?: number;
  onDrawGlobal: () => void;
  isLoading?: boolean;
}

export function CompanyGraphEmptyState({
  companyCount,
  relationCount,
  onDrawGlobal,
  isLoading,
}: CompanyGraphEmptyStateProps) {
  return (
    <div className="flex h-full w-full flex-col items-center justify-center bg-slate-950 px-6">
      <div className="flex flex-col items-center gap-4 text-center">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-slate-800">
          <Network className="h-6 w-6 text-cyan-400" />
        </div>

        <div>
          <h3 className="text-sm font-semibold text-slate-200">公司关系网络</h3>
          <p className="mt-1 text-xs text-slate-500">
            {companyCount != null && relationCount != null
              ? `当前包含 ${companyCount} 家公司和 ${relationCount} 条推断关系`
              : "全局公司供应链关系网络"}
          </p>
        </div>

        <div className="max-w-xs text-[11px] leading-relaxed text-slate-600">
          绘制全局图需要遍历所有公司对的产业图路径，数据量较大时可能需要一些时间。
          您也可以从左侧<strong>公司列表</strong>中选择一个公司开始局部浏览。
        </div>

        <button
          onClick={onDrawGlobal}
          disabled={isLoading}
          className="flex items-center gap-2 rounded-lg bg-cyan-900/40 px-4 py-2 text-xs font-medium text-cyan-300 hover:bg-cyan-900/60 disabled:opacity-50"
        >
          <Globe size={14} className={isLoading ? "animate-spin" : ""} />
          {isLoading ? "正在绘制..." : "绘制全局图"}
        </button>
      </div>
    </div>
  );
}
