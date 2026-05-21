import { useMutation } from "@tanstack/react-query";
import { useState } from "react";
import { X, Upload } from "lucide-react";
import { submitBatch } from "@/services/api";

interface BatchUploaderProps {
  onClose: () => void;
  onSuccess: () => void;
}

const EXAMPLE_JSON = JSON.stringify(
  {
    batch_id: "demo_batch_001",
    task_description: "示例批量注册",
    nodes_to_upsert: [
      {
        node_id: "demo_node_1",
        canonical_name_zh: "示例节点一",
        definition: "这是一个示例节点。",
        entity_type: "system",
        confidence: "MEDIUM",
        status: "ACTIVE",
        evidence: [
          {
            source_title: "示例资料",
            quote: "示例节点一是某系统。",
          },
        ],
      },
    ],
    edges_to_upsert: [],
    rejected_or_pending: [],
  },
  null,
  2
);

export function BatchUploader({ onClose, onSuccess }: BatchUploaderProps) {
  const [jsonText, setJsonText] = useState("");
  const [error, setError] = useState("");
  const [result, setResult] = useState<string | null>(null);

  const mutation = useMutation({
    mutationFn: async () => {
      const batch = JSON.parse(jsonText);
      return submitBatch(batch);
    },
    onSuccess: (data) => {
      setResult(
        `节点: 创建 ${data.nodes_created} / 更新 ${data.nodes_updated}\n关系: 创建 ${data.edges_created} / 更新 ${data.edges_updated}\n拒绝/待确认: ${data.rejected_or_pending_stored}`
      );
      if (data.errors.length > 0) {
        setResult((prev) => prev + `\n错误: ${data.errors.length} 项`);
      }
      onSuccess();
    },
    onError: (err: Error) => {
      setError(err.message);
    },
  });

  const handleSubmit = () => {
    setError("");
    setResult(null);
    mutation.mutate();
  };

  const handleFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      setJsonText(String(ev.target?.result || ""));
    };
    reader.readAsText(file);
  };

  return (
    <div className="space-y-4 p-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-slate-200">批量上传</h3>
        <button onClick={onClose} className="rounded p-1 text-slate-400 hover:bg-slate-800">
          <X className="h-3.5 w-3.5" />
        </button>
      </div>

      <div className="space-y-2">
        <div className="flex items-center gap-2">
          <label className="cursor-pointer rounded border border-slate-700 bg-slate-800 px-3 py-1.5 text-xs text-slate-300 hover:border-slate-600">
            <Upload className="mr-1 inline h-3 w-3" />
            选择 JSON 文件
            <input type="file" accept=".json" className="hidden" onChange={handleFile} />
          </label>
          <button
            onClick={() => setJsonText(EXAMPLE_JSON)}
            className="text-xs text-cyan-400 hover:underline"
          >
            插入示例
          </button>
        </div>

        <textarea
          rows={16}
          value={jsonText}
          onChange={(e) => setJsonText(e.target.value)}
          placeholder="粘贴 GraphRegistrationBatch JSON..."
          className="w-full rounded border border-slate-700 bg-slate-800 px-2 py-1.5 font-mono text-xs text-slate-200 focus:border-cyan-500 focus:outline-none"
        />
      </div>

      {error && (
        <div className="rounded bg-red-900/20 p-2 text-xs text-red-400 whitespace-pre-wrap">
          {error}
        </div>
      )}

      {result && (
        <div className="rounded bg-emerald-900/20 p-2 text-xs text-emerald-400 whitespace-pre-wrap">
          {result}
        </div>
      )}

      <button
        onClick={handleSubmit}
        disabled={mutation.isPending || !jsonText.trim()}
        className="w-full rounded bg-amber-600 py-2 text-sm font-medium text-white hover:bg-amber-500 disabled:opacity-50"
      >
        {mutation.isPending ? "提交中..." : "提交批量注册"}
      </button>
    </div>
  );
}
