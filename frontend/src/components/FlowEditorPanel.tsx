import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { X } from "lucide-react";
import { GraphCanvas, GraphCanvasRef } from "@/components/GraphCanvas";
import { adaptFlowEdge, adaptFlowNode } from "@/lib/flowAdapters";
import { collapsePreviewGraph } from "@/lib/flowCollapse";
import {
  createFlow,
  formatFlow,
  getFlowContent,
  listFlows,
  previewFlow,
  saveFlow,
  FlowPreviewResult,
} from "@/services/api";
import { ARACHNE_FLOW_PREDICATES, FlowSummary } from "@/types";

const EDITOR_FILTERS = {
  edgeNamespaces: ["arachne_flow"],
  edgeTypes: [...ARACHNE_FLOW_PREDICATES],
  entityTypes: [
    "arachne_flow:resource",
    "arachne_flow:action",
    "arachne_flow:method",
    "arachne_flow:dual",
    "arachne_flow:folder",
  ],
  status: ["ACTIVE", "PENDING"],
  confidence: ["HIGH", "MEDIUM", "LOW"],
  showIsA: true,
  showPartOf: true,
  showWeakOntology: true,
  showDerivedFrom: false,
};

const DEFAULT_TEMPLATE = `schema: arachne-flow/v0.1
title: 'New flow'
root_product: your_product
include: []
local: {}
edges:
- [your_resource, feedstock, act_your_action]
- [act_your_action, ref, your_method]
- [act_your_action, primary_result, your_product]
`;

interface FlowEditorPanelProps {
  onClose: () => void;
  onSaved?: (flowId: string) => void;
}

/**
 * Inline arachne-flow YAML editor shown as a side panel inside the main graph
 * workspace. It does not navigate away, so the total graph remains visible.
 */
export function FlowEditorPanel({ onClose, onSaved }: FlowEditorPanelProps) {
  const [flows, setFlows] = useState<FlowSummary[]>([]);
  const [selectedFlowId, setSelectedFlowId] = useState<string>("");
  const [content, setContent] = useState<string>(DEFAULT_TEMPLATE);
  const [preview, setPreview] = useState<FlowPreviewResult | null>(null);
  const [lastGood, setLastGood] = useState<FlowPreviewResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [warnings, setWarnings] = useState<string[]>([]);
  const [previewing, setPreviewing] = useState(false);
  const [previewVersion, setPreviewVersion] = useState(0);
  const [collapseIncludes, setCollapseIncludes] = useState(false);
  const [saving, setSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState<string | null>(null);

  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const gutterRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<GraphCanvasRef>(null);
  const previewSeqRef = useRef(0);

  useEffect(() => {
    listFlows().then(setFlows).catch(() => setFlows([]));
  }, []);

  useEffect(() => {
    setPreview(null);
    setLastGood(null);
    setError(null);
    setWarnings([]);
    setSaveMessage(null);
  }, [selectedFlowId]);

  useEffect(() => {
    if (!selectedFlowId) return;
    getFlowContent(selectedFlowId)
      .then((r) => setContent(r.content))
      .catch((e) => setError(String(e)));
  }, [selectedFlowId]);

  useEffect(() => {
    const seq = ++previewSeqRef.current;
    const handle = setTimeout(() => {
      setPreviewing(true);
      previewFlow(content, selectedFlowId || "preview")
        .then((result) => {
          if (seq !== previewSeqRef.current) return;
          setPreviewing(false);
          if (result.valid) {
            setPreview(result);
            setLastGood(result);
            setError(null);
            setPreviewVersion((v) => v + 1);
          } else {
            setError(result.errors.join("\n"));
          }
          setWarnings(result.warnings || []);
        })
        .catch((e) => {
          if (seq !== previewSeqRef.current) return;
          setPreviewing(false);
          setError(String(e));
        });
    }, 500);
    return () => clearTimeout(handle);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [content]);

  const graphData = useMemo(() => {
    const active = preview?.valid ? preview : lastGood;
    if (!active) return null;
    const currentFlowId = selectedFlowId || "preview";
    const display = collapseIncludes
      ? collapsePreviewGraph(
          active.nodes,
          active.edges,
          active.includes || [],
          currentFlowId
        )
      : { nodes: active.nodes, edges: active.edges };
    return {
      nodes: display.nodes.map(adaptFlowNode),
      edges: display.edges.map(adaptFlowEdge),
    };
  }, [preview, lastGood, collapseIncludes, selectedFlowId]);

  const lineCount = useMemo(() => content.split("\n").length, [content]);
  const lineNumbers = useMemo(() => Array.from({ length: lineCount }, (_, i) => i + 1), [lineCount]);

  const syncGutterScroll = useCallback(() => {
    if (textareaRef.current && gutterRef.current) {
      gutterRef.current.scrollTop = textareaRef.current.scrollTop;
    }
  }, []);

  const handleFormat = useCallback(() => {
    formatFlow(content)
      .then((r) => {
        if (r.valid) {
          setContent(r.formatted);
          setError(null);
        } else {
          setError(r.errors.join("\n"));
        }
      })
      .catch((e) => setError(String(e)));
  }, [content]);

  const extractRootProduct = useCallback((text: string): string | null => {
    const match = text.match(/^root_product:\s*([a-z][a-z0-9_]*)\s*$/m);
    return match ? match[1] : null;
  }, []);

  const handleSave = useCallback(async () => {
    setSaving(true);
    setSaveMessage(null);
    try {
      if (selectedFlowId) {
        const result = await saveFlow(selectedFlowId, content);
        if (result.valid) {
          setSaveMessage(`已保存并编译：${result.flow_id}`);
          listFlows().then(setFlows).catch(() => {});
          onSaved?.(result.flow_id);
        } else {
          setError(result.errors.join("\n"));
        }
      } else {
        const suggested = extractRootProduct(content) || "new_flow";
        const flowId = window.prompt("请输入新流程的 flow_id（蛇形命名）", suggested);
        if (!flowId) return;
        const result = await createFlow(flowId.trim(), content);
        if (result.valid) {
          setSaveMessage(`已创建并编译：${result.flow_id}`);
          setSelectedFlowId(result.flow_id);
          listFlows().then(setFlows).catch(() => {});
          onSaved?.(result.flow_id);
        } else {
          setError(result.errors.join("\n"));
        }
      }
    } catch (e) {
      setError(String(e));
    } finally {
      setSaving(false);
    }
  }, [selectedFlowId, content, extractRootProduct, onSaved]);

  return (
    <div className="flex h-full flex-col bg-slate-900">
      {/* Header */}
      <div className="flex items-center gap-1.5 border-b border-slate-800 bg-slate-900 p-2">
        <select
          value={selectedFlowId}
          onChange={(e) => setSelectedFlowId(e.target.value)}
          className="h-7 flex-1 rounded border border-slate-700 bg-slate-900 px-2 text-xs text-slate-200 outline-none focus:border-cyan-500"
        >
          <option value="">新建流程...</option>
          {flows.map((f) => (
            <option key={f.flow_id} value={f.flow_id}>
              {f.title || f.flow_id}
            </option>
          ))}
        </select>
        <button
          onClick={handleFormat}
          className="h-7 rounded border border-slate-700 bg-slate-800 px-2 text-[11px] text-slate-300 hover:bg-slate-700"
        >
          格式
        </button>
        <button
          onClick={() => setCollapseIncludes((v) => !v)}
          className={`h-7 rounded border px-2 text-[11px] ${
            collapseIncludes
              ? "border-cyan-600 bg-cyan-900/40 text-cyan-200"
              : "border-slate-700 bg-slate-800 text-slate-300 hover:bg-slate-700"
          }`}
          title="折叠 include"
        >
          折叠
        </button>
        <button
          onClick={handleSave}
          disabled={saving}
          className="h-7 rounded bg-emerald-700 px-2 text-[11px] font-medium text-white hover:bg-emerald-600 disabled:opacity-40"
        >
          {saving ? "保存中" : "保存"}
        </button>
        <button
          onClick={onClose}
          className="h-7 rounded border border-slate-700 bg-slate-800 px-2 text-[11px] text-slate-300 hover:bg-slate-700"
          title="关闭编辑器"
        >
          <X className="h-3 w-3" />
        </button>
      </div>

      {/* Disabled graph-edit placeholder */}
      <div className="border-b border-slate-800 bg-slate-900 px-2 py-1">
        <button
          disabled
          title="图级编辑（预留）：从总图直接添加/修改定义，最终落到单个文件"
          className="w-full rounded border border-dashed border-slate-700 bg-slate-800/50 px-2 py-1 text-[10px] text-slate-500"
        >
          从图添加（预留）
        </button>
      </div>

      {/* Messages */}
      {error && (
        <div className="border-b border-red-800 bg-red-950 px-2 py-1.5 text-[11px] text-red-200 whitespace-pre-wrap">
          {error}
        </div>
      )}
      {!error && warnings.length > 0 && (
        <div className="border-b border-amber-800 bg-amber-950 px-2 py-1.5 text-[11px] text-amber-200">
          {warnings.map((w, i) => (
            <div key={i}>{w}</div>
          ))}
        </div>
      )}
      {saveMessage && (
        <div className="border-b border-emerald-800 bg-emerald-950 px-2 py-1.5 text-[11px] text-emerald-200">
          {saveMessage}
        </div>
      )}

      {/* Editor */}
      <div className="flex flex-1 overflow-hidden">
        <div
          ref={gutterRef}
          className="w-8 shrink-0 select-none overflow-hidden border-r border-slate-800 bg-slate-900 py-2 text-right font-mono text-[10px] leading-5 text-slate-600"
        >
          {lineNumbers.map((n) => (
            <div key={n} className="pr-1">
              {n}
            </div>
          ))}
        </div>
        <textarea
          ref={textareaRef}
          value={content}
          onChange={(e) => setContent(e.target.value)}
          onScroll={syncGutterScroll}
          spellCheck={false}
          className="flex-1 resize-none overflow-auto bg-slate-950 p-2 font-mono text-[11px] leading-5 text-slate-200 outline-none"
        />
      </div>

      {/* Preview */}
      <div className="h-56 shrink-0 border-t border-slate-800">
        {graphData ? (
          <GraphCanvas
            ref={canvasRef}
            key={`panel-preview-${previewVersion}-${collapseIncludes ? "collapsed" : "full"}`}
            onNodeClick={() => {}}
            onEdgeClick={() => {}}
            filters={EDITOR_FILTERS}
            sourceData={graphData}
            engine="arachne_flow"
          />
        ) : (
          <div className="flex h-full w-full items-center justify-center text-xs text-slate-500">
            {previewing ? "预览中..." : "输入 YAML 后显示预览"}
          </div>
        )}
      </div>
    </div>
  );
}
