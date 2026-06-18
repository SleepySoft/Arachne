import { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import {
  AlertTriangle,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  Loader2,
  Play,
  RefreshCw,
  ShieldAlert,
  Trash2,
  Wrench,
} from "lucide-react";
import { DbCheckResult, DbCheckIssue, DbFixResult } from "@/types";
import { listDbChecks, runAllDbChecks, runDbCheck, fixDbCheck } from "@/services/api";

const severityStyles = {
  ERROR: "text-red-400 bg-red-400/10 border-red-400/20",
  WARNING: "text-amber-400 bg-amber-400/10 border-amber-400/20",
  INFO: "text-cyan-400 bg-cyan-400/10 border-cyan-400/20",
};

const severityIcon = {
  ERROR: <ShieldAlert className="h-4 w-4" />,
  WARNING: <AlertTriangle className="h-4 w-4" />,
  INFO: <CheckCircle2 className="h-4 w-4" />,
};

export function DbChecksPage() {
  const [results, setResults] = useState<DbCheckResult[]>([]);
  const [expandedChecks, setExpandedChecks] = useState<Record<string, boolean>>({});
  const [expandedIssues, setExpandedIssues] = useState<Record<string, boolean>>({});
  const [fixing, setFixing] = useState<Record<string, boolean>>({});
  const [fixResults, setFixResults] = useState<Record<string, DbFixResult>>({});

  const { data: checkers, isLoading: checkersLoading } = useQuery({
    queryKey: ["db-checks-meta"],
    queryFn: listDbChecks,
  });

  const runAllMutation = useMutation({
    mutationFn: runAllDbChecks,
    onSuccess: (data) => {
      setResults(data);
      const expanded: Record<string, boolean> = {};
      data.forEach((r) => {
        expanded[r.check_id] = r.issue_count > 0;
      });
      setExpandedChecks(expanded);
      setFixResults({});
    },
  });

  const runOneMutation = useMutation({
    mutationFn: runDbCheck,
    onSuccess: (data) => {
      setResults((prev) => {
        const filtered = prev.filter((r) => r.check_id !== data.check_id);
        return [...filtered, data];
      });
      setExpandedChecks((prev) => ({ ...prev, [data.check_id]: data.issue_count > 0 }));
    },
  });

  const toggleCheck = (checkId: string) => {
    setExpandedChecks((prev) => ({ ...prev, [checkId]: !prev[checkId] }));
  };

  const toggleIssue = (issueId: string) => {
    setExpandedIssues((prev) => ({ ...prev, [issueId]: !prev[issueId] }));
  };

  const handleFix = async (checkId: string, issueIds?: string[]) => {
    if (!confirm(issueIds ? "确定修复选中的问题吗？" : "确定修复该检查器发现的所有可修复问题吗？")) {
      return;
    }
    setFixing((prev) => ({ ...prev, [checkId]: true }));
    try {
      const res = await fixDbCheck(checkId, issueIds);
      setFixResults((prev) => ({ ...prev, [checkId]: res }));
      const refreshed = await runDbCheck(checkId);
      setResults((prev) => {
        const filtered = prev.filter((r) => r.check_id !== refreshed.check_id);
        return [...filtered, refreshed];
      });
    } finally {
      setFixing((prev) => ({ ...prev, [checkId]: false }));
    }
  };

  const totalIssues = results.reduce((sum, r) => sum + r.issue_count, 0);

  return (
    <div className="flex h-full flex-col overflow-hidden bg-slate-950 text-slate-200">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 bg-slate-900 px-6 py-4">
        <div>
          <h1 className="text-lg font-semibold text-slate-100">数据库检查与清理</h1>
          <p className="mt-1 text-xs text-slate-500">
            可扩展的数据质量检查工具。当前注册 {checkers?.length ?? 0} 个检查器。
          </p>
        </div>
        <button
          onClick={() => runAllMutation.mutate()}
          disabled={runAllMutation.isPending}
          className="flex items-center gap-2 rounded-md bg-cyan-600/20 px-4 py-2 text-sm font-medium text-cyan-400 hover:bg-cyan-600/30 disabled:opacity-50"
        >
          {runAllMutation.isPending ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <Play className="h-4 w-4" />
          )}
          运行全部检查
        </button>
      </div>

      {/* Summary */}
      {results.length > 0 && (
        <div className="grid grid-cols-3 gap-4 border-b border-slate-800 bg-slate-900/50 px-6 py-3">
          <div className="rounded border border-slate-800 bg-slate-900 p-3">
            <div className="text-[10px] uppercase text-slate-500">已运行检查器</div>
            <div className="text-xl font-semibold text-slate-200">{results.length}</div>
          </div>
          <div className="rounded border border-slate-800 bg-slate-900 p-3">
            <div className="text-[10px] uppercase text-slate-500">发现问题总数</div>
            <div className="text-xl font-semibold text-slate-200">{totalIssues}</div>
          </div>
          <div className="rounded border border-slate-800 bg-slate-900 p-3">
            <div className="text-[10px] uppercase text-slate-500">可自动修复</div>
            <div className="text-xl font-semibold text-slate-200">
              {results.filter((r) => r.fixable && r.issue_count > 0).length}
            </div>
          </div>
        </div>
      )}

      {/* Checkers list */}
      <div className="flex-1 overflow-y-auto px-6 py-4">
        {checkersLoading ? (
          <div className="flex items-center justify-center gap-2 py-12 text-sm text-slate-500">
            <Loader2 className="h-4 w-4 animate-spin" />
            加载检查器...
          </div>
        ) : (
          <div className="space-y-3">
            {checkers?.map((checker) => {
              const result = results.find((r) => r.check_id === checker.check_id);
              return (
                <div
                  key={checker.check_id}
                  className="rounded-lg border border-slate-800 bg-slate-900/60 overflow-hidden"
                >
                  <div className="flex items-center gap-3 px-4 py-3">
                    <button
                      onClick={() => toggleCheck(checker.check_id)}
                      className="text-slate-500 hover:text-slate-300"
                    >
                      {expandedChecks[checker.check_id] ? (
                        <ChevronDown className="h-4 w-4" />
                      ) : (
                        <ChevronRight className="h-4 w-4" />
                      )}
                    </button>
                    <div
                      className={`rounded border px-2 py-0.5 text-[10px] font-medium ${
                        severityStyles[checker.severity]
                      }`}
                    >
                      {checker.severity}
                    </div>
                    <div className="min-w-0 flex-1">
                      <div className="text-sm font-medium text-slate-200">{checker.name}</div>
                      <div className="text-[10px] text-slate-500">{checker.description}</div>
                    </div>
                    <div className="flex items-center gap-2">
                      {result && (
                        <span
                          className={`text-xs font-medium ${
                            result.issue_count > 0 ? "text-amber-400" : "text-emerald-400"
                          }`}
                        >
                          {result.issue_count} 个问题
                        </span>
                      )}
                      <button
                        onClick={() => runOneMutation.mutate(checker.check_id)}
                        disabled={runOneMutation.isPending && runOneMutation.variables === checker.check_id}
                        className="flex h-7 items-center gap-1 rounded bg-slate-800 px-2 text-[10px] text-slate-300 hover:bg-slate-700 hover:text-cyan-400 disabled:opacity-50"
                      >
                        {runOneMutation.isPending && runOneMutation.variables === checker.check_id ? (
                          <Loader2 className="h-3 w-3 animate-spin" />
                        ) : (
                          <RefreshCw className="h-3 w-3" />
                        )}
                        检查
                      </button>
                      {checker.fixable && result && result.issue_count > 0 && (
                        <button
                          onClick={() => handleFix(checker.check_id)}
                          disabled={fixing[checker.check_id]}
                          className="flex h-7 items-center gap-1 rounded bg-red-600/10 px-2 text-[10px] text-red-400 hover:bg-red-600/20 disabled:opacity-50"
                        >
                          {fixing[checker.check_id] ? (
                            <Loader2 className="h-3 w-3 animate-spin" />
                          ) : (
                            <Wrench className="h-3 w-3" />
                          )}
                          修复全部
                        </button>
                      )}
                    </div>
                  </div>

                  {expandedChecks[checker.check_id] && result && (
                    <div className="border-t border-slate-800 bg-slate-950/30 px-4 py-3">
                      {fixResults[checker.check_id] && (
                        <div className="mb-3 rounded border border-emerald-800/30 bg-emerald-900/10 px-3 py-2 text-xs text-emerald-400">
                          {fixResults[checker.check_id].messages.join("；")}
                        </div>
                      )}

                      {result.issues.length === 0 ? (
                        <div className="py-2 text-center text-xs text-slate-500">未发现异常</div>
                      ) : (
                        <div className="space-y-2">
                          {result.issues.map((issue) => (
                            <IssueItem
                              key={issue.issue_id}
                              issue={issue}
                              expanded={!!expandedIssues[issue.issue_id]}
                              onToggle={() => toggleIssue(issue.issue_id)}
                              onFix={() => handleFix(checker.check_id, [issue.issue_id])}
                              fixing={!!fixing[checker.check_id]}
                            />
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

function IssueItem({
  issue,
  expanded,
  onToggle,
  onFix,
  fixing,
}: {
  issue: DbCheckIssue;
  expanded: boolean;
  onToggle: () => void;
  onFix: () => void;
  fixing: boolean;
}) {
  return (
    <div className="rounded border border-slate-800 bg-slate-900/40">
      <button
        onClick={onToggle}
        className="flex w-full items-center gap-2 px-3 py-2 text-left"
      >
        <span className="text-slate-500">
          {expanded ? <ChevronDown className="h-3 w-3" /> : <ChevronRight className="h-3 w-3" />}
        </span>
        <span className={`${severityStyles[issue.severity]} rounded border px-1.5 py-0.5 text-[10px]`}>
          {severityIcon[issue.severity]}
        </span>
        <span className="min-w-0 flex-1 truncate text-xs text-slate-200">{issue.summary}</span>
        {issue.fixable && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              onFix();
            }}
            disabled={fixing}
            className="flex h-6 items-center gap-1 rounded bg-red-600/10 px-1.5 text-[10px] text-red-400 hover:bg-red-600/20 disabled:opacity-50"
          >
            <Trash2 className="h-3 w-3" />
            修复
          </button>
        )}
      </button>
      {expanded && (
        <div className="border-t border-slate-800 px-3 py-2">
          <div className="mb-1 text-[10px] font-medium uppercase text-slate-500">详情</div>
          <pre className="max-h-40 overflow-auto rounded bg-slate-950 p-2 text-[10px] text-slate-400">
            {JSON.stringify(issue.details, null, 2)}
          </pre>
          {issue.affected_ids.length > 0 && (
            <div className="mt-2">
              <div className="text-[10px] font-medium uppercase text-slate-500">受影响 ID</div>
              <div className="mt-1 flex flex-wrap gap-1">
                {issue.affected_ids.map((id) => (
                  <span key={id} className="rounded bg-slate-800 px-1.5 py-0.5 text-[10px] text-slate-400">
                    {id}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
