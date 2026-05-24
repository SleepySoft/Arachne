import { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  RotateCw,
  CheckCircle2,
  AlertCircle,
  Loader2,
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
  onClose?: () => void;
  onViewNetwork?: () => void;
}

export function CompanyViewVersions({ onViewNetwork }: CompanyViewVersionsProps) {
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
          if (job.status === "completed") {
            setToast("计算完成");
            onViewNetwork?.();
          }
        }
      } catch {
        setActiveJobId(null);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [activeJobId, queryClient, onViewNetwork]);

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
    });
  };

  return (
    <div className="flex h-full flex-col text-slate-200">
      {/* Recompute button */}
      <div className="border-b border-slate-800 p-2">
        <button
          onClick={() => setShowRecomputeConfirm(true)}
          disabled={createMutation.isPending || !!activeJobId}
          className="flex w-full items-center justify-center gap-1.5 rounded bg-cyan-900/40 px-2 py-1.5 text-[11px] font-medium text-cyan-300 hover:bg-cyan-900/60 disabled:opacity-50"
        >
          <RotateCw size={11} className={activeJobId ? "animate-spin" : ""} />
          {activeJobId ? "计算中..." : "重新计算"}
        </button>
      </div>

      {/* Confirm recompute */}
      {showRecomputeConfirm && (
        <div className="border-b border-slate-800 bg-amber-950/20 p-2">
          <p className="text-[10px] leading-relaxed text-amber-200">
            确认重新计算？将遍历所有公司对的产业图路径，可能需要数十秒。
          </p>
          <div className="mt-1.5 flex gap-1.5">
            <button
              onClick={() => createMutation.mutate()}
              className="rounded bg-amber-900/50 px-2 py-0.5 text-[10px] text-amber-300 hover:bg-amber-900/70"
            >
              确认
            </button>
            <button
              onClick={() => setShowRecomputeConfirm(false)}
              className="rounded px-2 py-0.5 text-[10px] text-slate-400 hover:bg-slate-800"
            >
              取消
            </button>
          </div>
        </div>
      )}

      {/* Confirm delete */}
      {deleteTarget !== null && (
        <div className="border-b border-slate-800 bg-rose-950/20 p-2">
          <p className="text-[10px] leading-relaxed text-rose-200">
            确认删除版本 #{deleteTarget}？不可恢复。
          </p>
          <div className="mt-1.5 flex gap-1.5">
            <button
              onClick={() => deleteMutation.mutate(deleteTarget)}
              disabled={deleteMutation.isPending}
              className="rounded bg-rose-900/50 px-2 py-0.5 text-[10px] text-rose-300 hover:bg-rose-900/70 disabled:opacity-50"
            >
              删除
            </button>
            <button
              onClick={() => setDeleteTarget(null)}
              className="rounded px-2 py-0.5 text-[10px] text-slate-400 hover:bg-slate-800"
            >
              取消
            </button>
          </div>
        </div>
      )}

      {/* Toast */}
      {toast && (
        <div className="border-b border-slate-800 bg-emerald-950/20 px-2 py-1 text-[10px] text-emerald-300">
          {toast}
        </div>
      )}

      {/* Progress */}
      {activeJobId && jobProgress && (
        <div className="border-b border-slate-800 bg-slate-800/30 px-2 py-1.5">
          <div className="flex items-center gap-1.5 text-[10px]">
            <Loader2 size={10} className="animate-spin text-cyan-400" />
            <span className="text-slate-300">
              {jobProgress.status === "pending" && "等待开始"}
              {jobProgress.status === "running" && `${jobProgress.processed}/${jobProgress.total}`}
              {jobProgress.status === "completed" && "已完成"}
              {jobProgress.status === "failed" && "失败"}
            </span>
          </div>
          {jobProgress.total > 0 && (
            <div className="mt-1 h-1 w-full overflow-hidden rounded-full bg-slate-700">
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

      {/* Version list — compact cards for narrow sidebar */}
      <div className="flex-1 overflow-auto">
        {versions.length === 0 && !isLoading && (
          <div className="px-3 py-6 text-center text-[11px] text-slate-500">
            暂无版本记录
          </div>
        )}
        <div className="divide-y divide-slate-800">
          {versions.map((v: CompanyViewVersion) => (
            <div key={v.version_id} className="group px-2 py-2 hover:bg-slate-800/40">
              <div className="flex items-center justify-between">
                <span className="font-mono text-[11px] text-slate-300">#{v.version_id}</span>
                <div className="flex items-center gap-1">
                  {v.status === "completed" ? (
                    <CheckCircle2 size={10} className="text-emerald-400" />
                  ) : v.status === "failed" ? (
                    <AlertCircle size={10} className="text-rose-400" />
                  ) : (
                    <Loader2 size={10} className="animate-spin text-amber-400" />
                  )}
                  <button
                    onClick={() => setDeleteTarget(v.version_id)}
                    className="rounded p-0.5 text-slate-600 opacity-0 hover:bg-rose-900/30 hover:text-rose-400 group-hover:opacity-100"
                    title="删除"
                  >
                    <Trash2 size={10} />
                  </button>
                </div>
              </div>
              <div className="mt-0.5 flex items-center justify-between text-[10px] text-slate-500">
                <span>{formatTime(v.created_at)}</span>
                {v.total_companies != null && (
                  <span>
                    {v.total_companies}公司 · {v.total_relations ?? 0}关系
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
