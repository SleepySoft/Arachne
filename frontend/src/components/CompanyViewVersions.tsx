import { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  RotateCw,
  X,
  CheckCircle2,
  AlertCircle,
  Loader2,
  Eye,
  Trash2,
} from "lucide-react";
import {
  listCompanyViewVersions,
  createCompanyViewVersion,
  deleteCompanyViewVersion,
  getComputationJob,
} from "@/services/api";
import type { CompanyViewVersion } from "@/types";

interface CompanyViewVersionsProps {
  onClose: () => void;
  onViewNetwork: () => void;
}

export function CompanyViewVersions({ onClose, onViewNetwork }: CompanyViewVersionsProps) {
  const queryClient = useQueryClient();
  const [activeJobId, setActiveJobId] = useState<string | null>(null);
  const [jobProgress, setJobProgress] = useState<{
    status: string;
    processed: number;
    total: number;
  } | null>(null);
  const [showRecomputeConfirm, setShowRecomputeConfirm] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState<number | null>(null);
  const [toast, setToast] = useState<string | null>(null);

  // Fetch versions with react-query
  const { data: versionsData, isLoading } = useQuery({
    queryKey: ["company-view-versions"],
    queryFn: () => listCompanyViewVersions(1, 50),
    refetchInterval: activeJobId ? 2000 : false,
  });

  const versions = versionsData?.items ?? [];
  const total = versionsData?.total ?? 0;

  // Auto-hide toast
  useEffect(() => {
    if (!toast) return;
    const t = setTimeout(() => setToast(null), 3000);
    return () => clearTimeout(t);
  }, [toast]);

  // Poll active job progress
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
          queryClient.invalidateQueries({ queryKey: ["company-view-versions"] });
        }
      } catch {
        setActiveJobId(null);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [activeJobId, queryClient]);

  const createMutation = useMutation({
    mutationFn: createCompanyViewVersion,
    onSuccess: (data) => {
      setActiveJobId(data.job_id);
      setJobProgress({ status: "pending", processed: 0, total: 0 });
      setShowRecomputeConfirm(false);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: deleteCompanyViewVersion,
    onSuccess: () => {
      setDeleteTarget(null);
      queryClient.invalidateQueries({ queryKey: ["company-view-versions"] });
      setToast("版本已删除");
    },
    onError: () => {
      setDeleteTarget(null);
      setToast("删除失败");
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
        <h2 className="text-sm font-semibold text-slate-100">公司视图版本</h2>
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
          onClick={() => setShowRecomputeConfirm(true)}
          disabled={createMutation.isPending || !!activeJobId}
          className="flex items-center gap-1.5 rounded bg-cyan-900/40 px-3 py-1.5 text-xs font-medium text-cyan-300 hover:bg-cyan-900/60 disabled:opacity-50"
        >
          <RotateCw size={12} className={activeJobId ? "animate-spin" : ""} />
          {activeJobId ? "计算中..." : "重新计算"}
        </button>
        <button
          onClick={() => queryClient.invalidateQueries({ queryKey: ["company-view-versions"] })}
          disabled={isLoading}
          className="rounded px-2 py-1.5 text-xs text-slate-400 hover:bg-slate-800 hover:text-slate-200 disabled:opacity-50"
        >
          刷新
        </button>
        <span className="ml-auto text-xs text-slate-500">共 {total} 个版本</span>
      </div>

      {/* Confirm recompute */}
      {showRecomputeConfirm && (
        <div className="border-b border-slate-700 bg-amber-950/30 px-4 py-3">
          <p className="text-xs text-amber-200">
            确认重新计算公司关系网络？这将遍历所有公司对的产业图路径，可能需要数十秒。
          </p>
          <div className="mt-2 flex gap-2">
            <button
              onClick={() => createMutation.mutate()}
              className="rounded bg-amber-900/50 px-3 py-1 text-xs text-amber-300 hover:bg-amber-900/70"
            >
              确认
            </button>
            <button
              onClick={() => setShowRecomputeConfirm(false)}
              className="rounded px-3 py-1 text-xs text-slate-400 hover:bg-slate-800"
            >
              取消
            </button>
          </div>
        </div>
      )}

      {/* Confirm delete */}
      {deleteTarget !== null && (
        <div className="border-b border-slate-700 bg-rose-950/30 px-4 py-3">
          <p className="text-xs text-rose-200">
            确认删除版本 #{deleteTarget}？此操作不可恢复。
          </p>
          <div className="mt-2 flex gap-2">
            <button
              onClick={() => deleteMutation.mutate(deleteTarget)}
              disabled={deleteMutation.isPending}
              className="rounded bg-rose-900/50 px-3 py-1 text-xs text-rose-300 hover:bg-rose-900/70 disabled:opacity-50"
            >
              删除
            </button>
            <button
              onClick={() => setDeleteTarget(null)}
              className="rounded px-3 py-1 text-xs text-slate-400 hover:bg-slate-800"
            >
              取消
            </button>
          </div>
        </div>
      )}

      {/* Toast */}
      {toast && (
        <div className="border-b border-slate-700 bg-emerald-950/30 px-4 py-2 text-xs text-emerald-300">
          {toast}
        </div>
      )}

      {/* Progress */}
      {activeJobId && jobProgress && (
        <div className="border-b border-slate-700 bg-slate-800/50 px-4 py-2">
          <div className="flex items-center gap-2 text-xs">
            <Loader2 size={12} className="animate-spin text-cyan-400" />
            <span className="text-slate-300">
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
              <th className="px-2 py-2 font-medium">版本</th>
              <th className="px-2 py-2 font-medium">状态</th>
              <th className="px-2 py-2 font-medium">公司</th>
              <th className="px-2 py-2 font-medium">关系</th>
              <th className="px-2 py-2 font-medium">时间</th>
              <th className="px-2 py-2 font-medium text-right">操作</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {versions.length === 0 && !isLoading && (
              <tr>
                <td colSpan={6} className="px-2 py-8 text-center text-slate-500">
                  暂无版本记录
                </td>
              </tr>
            )}
            {versions.map((v: CompanyViewVersion) => (
              <tr key={v.version_id} className="hover:bg-slate-800/50">
                <td className="px-2 py-2 font-mono text-slate-300">#{v.version_id}</td>
                <td className="px-2 py-2">
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
                <td className="px-2 py-2 text-slate-300">{v.total_companies ?? "-"}</td>
                <td className="px-2 py-2 text-slate-300">{v.total_relations ?? "-"}</td>
                <td className="px-2 py-2 text-slate-400">{formatTime(v.created_at)}</td>
                <td className="px-2 py-2 text-right">
                  <div className="flex items-center justify-end gap-1">
                    {v.status === "completed" && (
                      <button
                        onClick={() => {
                          setToast("正在加载关系网络...");
                          onClose();
                          onViewNetwork();
                        }}
                        className="inline-flex items-center gap-1 rounded px-1.5 py-0.5 text-[10px] text-cyan-400 hover:bg-cyan-900/30"
                        title="查看该版本的关系网络"
                      >
                        <Eye size={10} />
                        查看
                      </button>
                    )}
                    <button
                      onClick={() => setDeleteTarget(v.version_id)}
                      className="inline-flex items-center gap-1 rounded px-1.5 py-0.5 text-[10px] text-rose-400 hover:bg-rose-900/30"
                      title="删除此版本"
                    >
                      <Trash2 size={10} />
                      删除
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
