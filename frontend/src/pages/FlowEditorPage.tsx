import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { GraphCanvas, GraphCanvasRef } from "@/components/GraphCanvas";
import { adaptFlowEdge, adaptFlowNode } from "@/lib/flowAdapters";
import { collapsePreviewGraph } from "@/lib/flowCollapse";
import {
  createFlow,
  formatFlow,
  getFlowContent,
  listFlows,
  listNodes,
  previewFlow,
  saveFlow,
  FlowPreviewResult,
} from "@/services/api";
import {
  ARACHNE_FLOW_PREDICATES,
  FlowSummary,
} from "@/types";

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

interface NodeOption {
  node_id: string;
  label?: string;
}

interface NodeComboboxProps {
  label: string;
  value: string;
  nodes: NodeOption[];
  placeholder?: string;
  onChange: (value: string) => void;
}

function NodeCombobox({ label, value, nodes, placeholder, onChange }: NodeComboboxProps) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState(value);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => setQuery(value), [value]);

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return nodes.slice(0, 20);
    return nodes
      .filter(
        (n) =>
          n.node_id.toLowerCase().includes(q) ||
          (n.label || "").toLowerCase().includes(q)
      )
      .slice(0, 20);
  }, [nodes, query]);

  return (
    <div ref={containerRef} className="relative flex-1 min-w-0">
      <label className="mb-1 block text-[10px] font-medium text-slate-500">{label}</label>
      <input
        value={query}
        placeholder={placeholder}
        onFocus={() => setOpen(true)}
        onChange={(e) => {
          setQuery(e.target.value);
          onChange(e.target.value);
          setOpen(true);
        }}
        className="w-full rounded border border-slate-700 bg-slate-900 px-2 py-1 text-xs text-slate-200 outline-none focus:border-cyan-500"
      />
      {open && filtered.length > 0 && (
        <div className="absolute z-20 mt-1 max-h-48 w-full overflow-y-auto rounded border border-slate-700 bg-slate-900 shadow-lg">
          {filtered.map((n) => (
            <button
              key={n.node_id}
              type="button"
              onClick={() => {
                onChange(n.node_id);
                setQuery(n.node_id);
                setOpen(false);
              }}
              className="block w-full truncate px-2 py-1 text-left text-xs text-slate-300 hover:bg-slate-800"
              title={n.label}
            >
              <span className="text-slate-400">{n.node_id}</span>
              {n.label && n.label !== n.node_id && (
                <span className="ml-1 text-slate-500">({n.label})</span>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

interface FlowEditorPageProps {
  /** Whether to show the right-hand preview canvas (default true). */
  showPreview?: boolean;
  /** Called whenever the active preview result changes (valid or last-good). */
  onPreviewChange?: (result: FlowPreviewResult | null) => void;
  /** Optional close handler for panel mode. */
  onClose?: () => void;
  /** Called after a flow is successfully saved/created. */
  onSaved?: (flowId: string) => void;
  /** Compact layout for narrow side panels. */
  compact?: boolean;
}

export function FlowEditorPage({
  showPreview = true,
  onPreviewChange,
  onClose,
  onSaved,
  compact: _compact = false,
}: FlowEditorPageProps) {
  const [flows, setFlows] = useState<FlowSummary[]>([]);
  const [selectedFlowId, setSelectedFlowId] = useState<string>("");
  const [content, setContent] = useState<string>(DEFAULT_TEMPLATE);
  const [preview, setPreview] = useState<FlowPreviewResult | null>(null);
  const [lastGood, setLastGood] = useState<FlowPreviewResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [warnings, setWarnings] = useState<string[]>([]);
  const [loadingContent, setLoadingContent] = useState(false);
  const [previewing, setPreviewing] = useState(false);
  const [previewVersion, setPreviewVersion] = useState(0);
  const [collapseIncludes, setCollapseIncludes] = useState(false);
  const [nodeOptions, setNodeOptions] = useState<NodeOption[]>([]);
  const [saving, setSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState<string | null>(null);
  const [tripleDraft, setTripleDraft] = useState({
    source: "",
    predicate: "feedstock",
    target: "",
  });

  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const gutterRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<GraphCanvasRef>(null);

  // Load flow list
  useEffect(() => {
    listFlows()
      .then(setFlows)
      .catch(() => setFlows([]));
  }, []);

  // Load node options for pickers
  useEffect(() => {
    listNodes(1, 1000, undefined, undefined, undefined, undefined, "arachne_flow")
      .then((r) =>
        setNodeOptions(
          r.items.map((n) => ({
            node_id: n.node_id,
            label: n.canonical_name_zh || n.node_id,
          }))
        )
      )
      .catch(() => setNodeOptions([]));
  }, []);

  // Reset preview state when switching files so stale graphs don't linger.
  useEffect(() => {
    setPreview(null);
    setLastGood(null);
    setError(null);
    setWarnings([]);
  }, [selectedFlowId]);

  // Load selected file content
  useEffect(() => {
    if (!selectedFlowId) return;
    setLoadingContent(true);
    getFlowContent(selectedFlowId)
      .then((r) => setContent(r.content))
      .catch((e) => setError(String(e)))
      .finally(() => setLoadingContent(false));
  }, [selectedFlowId]);

  // Debounced live preview. Only trigger on content changes; ignore stale responses.
  const previewSeqRef = useRef(0);
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
            // Bump version to force GraphCanvas remount with the new data.
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
  }, [content, collapseIncludes]);

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

  // Notify parent when the active preview result changes (for highlight/diff).
  const activePreview = preview?.valid ? preview : lastGood;
  useEffect(() => {
    onPreviewChange?.(activePreview);
  }, [activePreview, onPreviewChange]);

  // Center the preview graph after each render.
  useEffect(() => {
    if (!graphData) return;
    const timer = setTimeout(() => {
      canvasRef.current?.fitToView(40);
    }, 500);
    return () => clearTimeout(timer);
  }, [graphData, previewVersion]);

  const lineCount = useMemo(() => content.split("\n").length, [content]);
  const lineNumbers = useMemo(
    () => Array.from({ length: lineCount }, (_, i) => i + 1),
    [lineCount]
  );

  const syncGutterScroll = useCallback(() => {
    if (textareaRef.current && gutterRef.current) {
      gutterRef.current.scrollTop = textareaRef.current.scrollTop;
    }
  }, []);

  const insertAtCursor = useCallback(
    (text: string) => {
      const textarea = textareaRef.current;
      if (!textarea) {
        setContent((c) => c + text);
        return;
      }
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const before = content.slice(0, start);
      const after = content.slice(end);
      const next = before + text + after;
      setContent(next);
      requestAnimationFrame(() => {
        textarea.focus();
        const pos = start + text.length;
        textarea.setSelectionRange(pos, pos);
      });
    },
    [content]
  );

  const appendTriple = useCallback(() => {
    const { source, predicate, target } = tripleDraft;
    if (!source || !target) return;
    const line = `- [${source}, ${predicate}, ${target}]`;
    setContent((c) => (c.endsWith("\n") ? c : c + "\n") + line + "\n");
    setTripleDraft((d) => ({ ...d, source: "", target: "" }));
  }, [tripleDraft]);

  const quickInsert = useCallback(
    (predicate: string) => {
      insertAtCursor(`- [source, ${predicate}, target]\n`);
    },
    [insertAtCursor]
  );

  const handleNewFlow = useCallback(() => {
    setSelectedFlowId("");
    setContent(DEFAULT_TEMPLATE);
    setPreview(null);
    setLastGood(null);
    setError(null);
    setWarnings([]);
    setSaveMessage(null);
  }, []);

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
          setSaveMessage(
            `已保存并编译：${result.flow_id}（${result.resources}资源/${result.actions}动作/${result.edges}边）`
          );
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
  }, [selectedFlowId, content, extractRootProduct]);

  // Auto-hide the save success message after a few seconds.
  useEffect(() => {
    if (!saveMessage) return;
    const timer = setTimeout(() => setSaveMessage(null), 3000);
    return () => clearTimeout(timer);
  }, [saveMessage]);

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

  return (
    <div className="flex h-full w-full bg-slate-950">
      {/* Left: editor */}
      <div className={`flex flex-col ${showPreview ? "w-1/2 border-r border-slate-800" : "flex-1"}`}>
        {/* Toolbar */}
        <div className="flex items-center gap-2 border-b border-slate-800 bg-slate-900 p-2">
          <select
            value={selectedFlowId}
            onChange={(e) => setSelectedFlowId(e.target.value)}
            className="h-8 rounded border border-slate-700 bg-slate-900 px-2 text-xs text-slate-200 outline-none focus:border-cyan-500"
          >
            <option value="">新建流程...</option>
            {Object.entries(
              flows.reduce<Record<string, FlowSummary[]>>((acc, f) => {
                const cat = f.category || "未分类";
                if (!acc[cat]) acc[cat] = [];
                acc[cat].push(f);
                return acc;
              }, {})
            ).map(([category, items]) => (
              <optgroup key={category} label={category}>
                {items.map((f) => (
                  <option key={f.flow_id} value={f.flow_id}>
                    {f.title || f.flow_id}
                  </option>
                ))}
              </optgroup>
            ))}
          </select>
          <button
            onClick={handleNewFlow}
            className="h-8 rounded border border-slate-700 bg-slate-800 px-2 text-xs text-slate-300 hover:bg-slate-700"
          >
            新建
          </button>
          <button
            onClick={handleFormat}
            className="h-8 rounded border border-slate-700 bg-slate-800 px-2 text-xs text-slate-300 hover:bg-slate-700"
          >
            整理格式
          </button>
          <button
            onClick={() => setCollapseIncludes((v) => !v)}
            className={`h-8 rounded border px-2 text-xs ${
              collapseIncludes
                ? "border-cyan-600 bg-cyan-900/40 text-cyan-200"
                : "border-slate-700 bg-slate-800 text-slate-300 hover:bg-slate-700"
            }`}
            title="将 include 的流程折叠成文件夹节点"
          >
            折叠 include
          </button>
          <button
            onClick={handleSave}
            disabled={saving}
            className="h-8 rounded bg-emerald-700 px-3 text-xs font-medium text-white hover:bg-emerald-600 disabled:opacity-40"
          >
            {saving ? "保存中..." : "保存"}
          </button>
          {loadingContent && (
            <span className="text-xs text-slate-500">加载文件...</span>
          )}
          {previewing && (
            <span className="text-xs text-cyan-500">预览中...</span>
          )}
          {onClose && (
            <button
              onClick={onClose}
              className="ml-auto h-8 rounded border border-slate-700 bg-slate-800 px-2 text-xs text-slate-300 hover:bg-slate-700"
              title="关闭编辑器"
            >
              关闭
            </button>
          )}
        </div>

        {/* Save success banner (auto-hides after 3s) */}
        {saveMessage && (
          <div className="border-b border-emerald-800 bg-emerald-950 px-3 py-2 text-xs text-emerald-200 transition-opacity duration-500">
            {saveMessage}
          </div>
        )}

        {/* Error banner */}
        {error && (
          <div className="border-b border-red-800 bg-red-950 px-3 py-2 text-xs text-red-200 whitespace-pre-wrap">
            {error}
          </div>
        )}

        {/* Warning banner */}
        {!error && warnings.length > 0 && (
          <div className="border-b border-amber-800 bg-amber-950 px-3 py-2 text-xs text-amber-200">
            {warnings.map((w, i) => (
              <div key={i}>{w}</div>
            ))}
          </div>
        )}

        {/* Editor with line numbers */}
        <div className="flex flex-1 overflow-hidden">
          <div
            ref={gutterRef}
            className="w-10 shrink-0 select-none overflow-hidden border-r border-slate-800 bg-slate-900 py-2 text-right font-mono text-[11px] leading-5 text-slate-600"
          >
            {lineNumbers.map((n) => (
              <div key={n} className="pr-2">
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
            className="flex-1 resize-none overflow-auto bg-slate-950 p-2 font-mono text-[12px] leading-5 text-slate-200 outline-none"
          />
        </div>

        {/* Triple composer */}
        <div className="border-t border-slate-800 bg-slate-900 p-2">
          <div className="mb-2 flex items-end gap-2">
            <NodeCombobox
              label="Source"
              value={tripleDraft.source}
              nodes={nodeOptions}
              placeholder="source_id"
              onChange={(v) => setTripleDraft((d) => ({ ...d, source: v }))}
            />
            <div className="w-28">
              <label className="mb-1 block text-[10px] font-medium text-slate-500">
                Predicate
              </label>
              <select
                value={tripleDraft.predicate}
                onChange={(e) =>
                  setTripleDraft((d) => ({ ...d, predicate: e.target.value }))
                }
                className="w-full rounded border border-slate-700 bg-slate-900 px-2 py-1 text-xs text-slate-200 outline-none focus:border-cyan-500"
              >
                {ARACHNE_FLOW_PREDICATES.map((p) => (
                  <option key={p} value={p}>
                    {p}
                  </option>
                ))}
              </select>
            </div>
            <NodeCombobox
              label="Target"
              value={tripleDraft.target}
              nodes={nodeOptions}
              placeholder="target_id"
              onChange={(v) => setTripleDraft((d) => ({ ...d, target: v }))}
            />
            <button
              onClick={appendTriple}
              disabled={!tripleDraft.source || !tripleDraft.target}
              className="h-8 rounded bg-cyan-700 px-3 text-xs font-medium text-white hover:bg-cyan-600 disabled:opacity-40"
            >
              插入
            </button>
          </div>
          <div className="flex flex-wrap gap-1">
            {["feedstock", "component", "tool", "primary_result", "ref", "next"].map(
              (p) => (
                <button
                  key={p}
                  onClick={() => quickInsert(p)}
                  className="rounded border border-slate-700 bg-slate-800 px-2 py-1 text-[11px] text-slate-300 hover:bg-slate-700"
                >
                  {p}
                </button>
              )
            )}
          </div>
        </div>
      </div>

      {/* Right: preview */}
      {showPreview && (
        <div className="relative w-1/2">
          {graphData ? (
            <GraphCanvas
              ref={canvasRef}
              key={`preview-${previewVersion}-${collapseIncludes ? "collapsed" : "full"}`}
              onNodeClick={() => {}}
              onEdgeClick={() => {}}
              filters={EDITOR_FILTERS}
              sourceData={graphData}
              engine="arachne_flow"
            />
          ) : (
            <div className="flex h-full w-full items-center justify-center text-sm text-slate-500">
              输入 YAML 后右侧将实时渲染预览图
            </div>
          )}
          {preview && !preview.valid && lastGood && (
            <div className="absolute bottom-2 left-2 rounded bg-slate-800/90 px-2 py-1 text-[11px] text-slate-400">
              当前显示：最后一次正确的图
            </div>
          )}
        </div>
      )}
    </div>
  );
}
