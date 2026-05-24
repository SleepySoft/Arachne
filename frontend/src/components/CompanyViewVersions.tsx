import { useState, useEffect, useCallback } from "react";
import { useMutation } from "@tanstack/react-query";
import { RotateCw, X, CheckCircle2, AlertCircle, Loader2 } from "lucide-react";
import {
  listCompanyViewVersions,
  createCompanyViewVersion,
  getComputationJob,
} from "@/services/api";
import type { CompanyViewVersion } from "@/types";

interface CompanyViewVersionsProps {
  onClose: () => void;
}

export function CompanyViewVersions({ onClose }: CompanyViewVersionsProps) {
  const [versions, setVersions] = useState<CompanyViewVersion[]>([]);
  const [total, setTotal] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [activeJobId, setActiveJobId] = useState<string | null>(null);
  const [jobProgress, setJobProgress] = useState<{
    status: string;
    processed: number;
    total: number;
  } | null>(null);

  const fetchVersions = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await listCompanyViewVersions(1, 50);
      setVersions(data.items);
      setTotal(data.total);
    } catch {
      // ignore
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchVersions();
  }, [fetchVersions]);

  // Poll job progress
  useEffect(() => {
    if (!activeJobId) return;

    const interval = setInterval(async () => {
      try {
        const job = await getComputationJob(activeJobId);
        setJobProgress({
          status: job.status,
          processed: job.processed_items || 0,
          total: job.total_items || 0,
        });
        if (job.status === "completed" || job.status === "failed") {
          setActiveJobId(null);
          fetchVersions();
        }
      } catch {
        setActiveJobId(null);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [activeJobId, fetchVersions]);

  const mutation = useMutation({
    mutationFn: createCompanyViewVersion,
    onSuccess: (data) => {
      setActiveJobId(data.job_id);
      setJobProgress({ status: "pending", processed: 0, total: 0 });
    },
  });

  const formatTime = (iso?: string) => {
    if (!iso) return "-";
    const d = new Date(iso);
    return d.toLocaleString("zh-CN", {
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  };

  return (
    <div className="flex h-full flex-col bg-slate-900 text-slate-200">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-700 px-4 py-3">
        <h2 className="text-sm font-semibold text-slate-100">公司视图版本管理</h2>
        <button
          onClick={onClose}
          className="rounded p-1 text-slate-400 hover:bg-slate-800 hover:text-slate-200"
        >
          <X size={16} />
        </button>
      </div>

      {/* Toolbar */}
      <div className="flex items-center gap-2 border-b border-slate-700 px-4 py-2">
        <button
          onClick={() => mutation.mutate()}
          disabled={mutation.isPending || !!activeJobId}
          className="flex items-center gap-1.5 rounded bg-cyan-900/40 px-3 py-1.5 text-xs font-medium text-cyan-300 hover:bg-cyan-900/60 disabled:opacity-50"
        >
          <RotateCw size={12} className={activeJobId ? "animate-spin" : ""} />
          {activeJobId ? "计算中..." : "重新计算关系"}
        </button>
        <button
          onClick={fetchVersions}
          disabled={isLoading}
          className="rounded px-2 py-1.5 text-xs text-slate-400 hover:bg-slate-800 hover:text-slate-200 disabled:opacity-50"
        >
          刷新列表
        </button>
        <span className="ml-auto text-xs text-slate-500">共 {total} 个版本</span>
      </div>

      {/* Progress */}
      {activeJobId && jobProgress && (
        <div className="border-b border-slate-700 bg-slate-800/50 px-4 py-2">
          <div className="flex items-center gap-2 text-xs">
            <Loader2 size={12} className="animate-spin text-cyan-400" />
            <span className="text-slate-300">
              任务 {activeJobId.slice(-12)}: {" "}
              {jobProgress.status === "pending" && "等待开始"}
              {jobProgress.status === "running" && `计算中 ${jobProgress.processed}/${jobProgress.total}`}
              {jobProgress.status === "completed" && "已完成"}
              {jobProgress.status === "failed" && "失败"}
            </span>
          </div>
          {jobProgress.total > 0 && (
            <div className="mt-1 h-1.5 w-full overflow-hidden rounded-full bg-slate-700">
              <div
                className="h-full bg-cyan-500 transition-all duration-500"
                style={{
                  width: `${Math.min(100, (jobProgress.processed / jobProgress.total) * 100)}%`,
                }}
              />
            </div>
          )}
        </div>
      )}

      {/* Table */}
      <div className="flex-1 overflow-auto">
        <table className="w-full text-left text-xs">
          <thead className="sticky top-0 bg-slate-800 text-slate-400">
            <tr>
              <th className="px-3 py-2 font-medium">版本</th>
              <th className="px-3 py-2 font-medium">状态</th>
              <th className="px-3 py-2 font-medium">公司数</th>
              <th className="px-3 py-2 font-medium">关系数</th>
              <th className="px-3 py-2 font-medium">处理对数</th>
              <th className="px-3 py-2 font-medium">创建时间</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {versions.length === 0 && !isLoading && (
              <tr>
                <td colSpan={6} className="px-3 py-8 text-center text-slate-500">
                  暂无版本记录
                </td>
              </tr>
            )}
            {versions.map((v) => (
              <tr key={v.version_id} className="hover:bg-slate-800/50">
                <td className="px-3 py-2 font-mono text-slate-300">#{v.version_id}</td>
                <td className="px-3 py-2">
                  {v.status === "completed" ? (
                    <span className="inline-flex items-center gap-1 text-emerald-400">
                      <CheckCircle2 size={10} />
                      完成
                    </span>
                  ) : v.status === "failed" ? (
                    <span className="inline-flex items-center gap-1 text-rose-400" title={v.error_message}>
                      <AlertCircle size={10} />
                      失败
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 text-amber-400">
                      <Loader2 size={10} className="animate-spin" />
                      计算中
                    </span>
                  )}
                </td>
                <td className="px-3 py-2 text-slate-300">{v.total_companies ?? "-"}</td>
                <td className="px-3 py-2 text-slate-300">{v.total_relations ?? "-"}</td>
                <td className="px-3 py-2 text-slate-400">
                  {v.processed_pairs != null && v.total_pairs != null
                    ? `${v.processed_pairs}/${v.total_pairs}`
                    : "-"}
                </td>
                <td className="px-3 py-2 text-slate-400">{formatTime(v.created_at)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
