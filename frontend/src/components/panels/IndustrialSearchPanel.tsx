import { NodeNavigation } from "@/components/NodeNavigation";
import { SearchPanel } from "@/components/SearchPanel";
import { IndustrialNode } from "@/types";
import { useNodeNavigation } from "@/hooks/useNodeNavigation";

interface IndustrialSearchPanelProps {
  nav: ReturnType<typeof useNodeNavigation>;
  onNavBack: () => void;
  onNavForward: () => void;
  onNavGoto: (index: number) => void;
  onSelectNode: (node: IndustrialNode) => void;
  onCreateNode: () => void;
  onCreateEdge: () => void;
  onUploadBatch: () => void;
  hasActiveSelection: boolean;
  onResetSelection: () => void;
}

export function IndustrialSearchPanel({
  nav,
  onNavBack,
  onNavForward,
  onNavGoto,
  onSelectNode,
  onCreateNode,
  onCreateEdge,
  onUploadBatch,
  hasActiveSelection,
  onResetSelection,
}: IndustrialSearchPanelProps) {
  return (
    <div className="flex items-center gap-2">
      <NodeNavigation
        enabled={nav.enabled}
        history={nav.history}
        currentIndex={nav.index}
        canGoBack={nav.canGoBack}
        canGoForward={nav.canGoForward}
        onBack={onNavBack}
        onForward={onNavForward}
        onGoto={onNavGoto}
        onToggleEnabled={nav.toggleEnabled}
        onClear={nav.clear}
      />
      <SearchPanel
        onSelectNode={onSelectNode}
        onCreateNode={onCreateNode}
        onCreateEdge={onCreateEdge}
        onUploadBatch={onUploadBatch}
      />
      {hasActiveSelection && (
        <button
          onClick={onResetSelection}
          className="ml-auto flex items-center gap-1 rounded-md bg-amber-600/20 px-2.5 py-1 text-xs font-medium text-amber-400 hover:bg-amber-600/30 transition-colors"
        >
          返回全图
        </button>
      )}
    </div>
  );
}
