import { FlowEditorPage } from "@/pages/FlowEditorPage";
import { FlowPreviewResult } from "@/services/api";

interface FlowEditorPanelProps {
  onClose: () => void;
  onSaved?: (flowId: string) => void;
  onPreviewChange?: (result: FlowPreviewResult | null) => void;
}

/**
 * Inline arachne-flow YAML editor shown as a side panel inside the main graph
 * workspace. It reuses the full FlowEditorPage editor (without the right-hand
 * preview canvas) so the total graph remains visible next to it.
 */
export function FlowEditorPanel({ onClose, onSaved, onPreviewChange }: FlowEditorPanelProps) {
  return (
    <div className="h-full w-full">
      <FlowEditorPage
        showPreview={false}
        compact
        onClose={onClose}
        onSaved={onSaved}
        onPreviewChange={onPreviewChange}
      />
    </div>
  );
}
