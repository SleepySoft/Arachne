import { BatchUploader } from "@/components/BatchUploader";
import { CompanyDetail } from "@/components/CompanyDetail";
import { CompanyForm } from "@/components/CompanyForm";
import { EdgeDetail } from "@/components/EdgeDetail";
import { EdgeForm } from "@/components/EdgeForm";
import { IndustryDetail } from "@/components/IndustryDetail";
import { IndustryForm } from "@/components/IndustryForm";
import { NodeDetail } from "@/components/NodeDetail";
import { NodeCompaniesPanel } from "@/components/NodeCompaniesPanel";
import { NodeForm } from "@/components/NodeForm";
import { NodeIndustriesPanel } from "@/components/NodeIndustriesPanel";
import {
  CompanyNetworkEdge,
  Company,
  GraphEdge,
  IndustrialNode,
  Industry,
  PanelType,
} from "@/types";

export type OnNodeDeleted = (nodeId: string) => void;
export type OnEdgeDeleted = (edgeId: string) => void;
import { PanelState } from "@/hooks/usePanelStack";

interface RightPanelProps {
  panel: PanelType;
  selectedNode: IndustrialNode | null;
  selectedEdge: GraphEdge | null;
  selectedIndustry: Industry | null;
  selectedCompany: Company | null;
  selectedRelation: CompanyNetworkEdge | null;
  contextMenuNode: IndustrialNode | null;
  refreshGraph: () => void;
  onNodeCreated?: (node: IndustrialNode, position?: { x: number; y: number }) => void;
  onNodeUpdated?: (node: IndustrialNode) => void;
  onNodeDeleted?: OnNodeDeleted;
  onEdgeCreated?: (edge: GraphEdge) => void;
  onEdgeUpdated?: (edge: GraphEdge) => void;
  onEdgeDeleted?: OnEdgeDeleted;
  pendingNodePosition?: { x: number; y: number } | null;
  edgePrefillData?: {
    from_node?: string;
    to_node?: string;
    edge_type?: string;
    description?: string;
    notes?: string;
  } | null;
  clearPendingEdgePrefill?: () => void;
  setPanel: (panel: PanelType) => void;
  onPushPanel: (state: Partial<PanelState>) => void;
  onBackPanel: () => void;
  setSelectedNode: (node: IndustrialNode | null) => void;
  setSelectedEdge: (edge: GraphEdge | null) => void;
  setSelectedIndustry: (industry: Industry | null) => void;
  setSelectedCompany: (company: Company | null) => void;
  onLoadSubgraph: (nodes: unknown[], edges: unknown[]) => void;
  onHighlightNodes: (nodeIds: string[]) => void;
  onSelectNode: (node: IndustrialNode) => void;
  onSelectCompany: (company: Company) => void;
  onSelectIndustry: (industry: Industry) => void;
  isProcessExpanded?: boolean;
  onToggleProcessExpansion?: () => void;
  onFocusInGraph?: (companyId: string) => void;
  onOpenMaterialModal?: () => void;
  onAddExposure?: () => void;
}

export function RightPanel({
  panel,
  selectedNode,
  selectedEdge,
  selectedIndustry,
  selectedCompany,
  selectedRelation,
  contextMenuNode,
  refreshGraph,
  onNodeCreated,
  onNodeUpdated,
  onNodeDeleted,
  onEdgeCreated,
  onEdgeUpdated,
  onEdgeDeleted,
  pendingNodePosition,
  edgePrefillData,
  clearPendingEdgePrefill,
  setPanel,
  onPushPanel,
  onBackPanel,
  setSelectedNode,
  setSelectedEdge,
  setSelectedIndustry,
  setSelectedCompany,
  onLoadSubgraph,
  onHighlightNodes,
  onSelectNode,
  onSelectCompany,
  onSelectIndustry,
  isProcessExpanded,
  onToggleProcessExpansion,
  onFocusInGraph,
  onOpenMaterialModal,
  onAddExposure,
}: RightPanelProps) {
  if (panel === "node-detail" && selectedNode) {
    return (
      <NodeDetail
        node={selectedNode}
        onEdit={() => onPushPanel({ panel: "node-edit", selectedNode })}
        onClose={onBackPanel}
        onNodeDeleted={onNodeDeleted}
        onEdgeCreated={onEdgeCreated}
        onEdgeUpdated={onEdgeUpdated}
        onEdgeDeleted={onEdgeDeleted}
        onSelectNode={onSelectNode}
        onSelectCompany={onSelectCompany}
        onSelectIndustry={onSelectIndustry}
        isProcessExpanded={isProcessExpanded}
        onToggleProcessExpansion={onToggleProcessExpansion}
      />
    );
  }

  if (panel === "edge-detail" && selectedEdge) {
    return (
      <EdgeDetail
        edge={selectedEdge}
        onEdit={() => onPushPanel({ panel: "edge-edit", selectedEdge })}
        onClose={onBackPanel}
        onEdgeDeleted={onEdgeDeleted}
        onSelectNode={onSelectNode}
      />
    );
  }

  if (panel === "node-create") {
    return (
      <NodeForm
        mode="create"
        onClose={onBackPanel}
        onSuccess={(node) => {
          setSelectedNode(node);
          setPanel("node-detail");
          onNodeCreated?.(node, pendingNodePosition ?? undefined);
        }}
      />
    );
  }

  if (panel === "node-edit" && selectedNode) {
    return (
      <NodeForm
        mode="edit"
        node={selectedNode}
        onClose={onBackPanel}
        onSuccess={(node) => {
          setSelectedNode(node);
          setPanel("node-detail");
          onNodeUpdated?.(node);
        }}
      />
    );
  }

  if (panel === "edge-create") {
    return (
      <EdgeForm
        mode="create"
        prefillData={edgePrefillData || undefined}
        onClose={() => {
          clearPendingEdgePrefill?.();
          onBackPanel();
        }}
        onSuccess={(edge) => {
          setSelectedEdge(edge);
          setPanel("edge-detail");
          clearPendingEdgePrefill?.();
          onEdgeCreated?.(edge);
        }}
      />
    );
  }

  if (panel === "edge-edit" && selectedEdge) {
    return (
      <EdgeForm
        mode="edit"
        edge={selectedEdge}
        onClose={onBackPanel}
        onSuccess={(edge) => {
          setSelectedEdge(edge);
          setPanel("edge-detail");
          onEdgeUpdated?.(edge);
        }}
      />
    );
  }

  if (panel === "batch-upload") {
    return (
      <BatchUploader
        onClose={onBackPanel}
        onSuccess={() => {
          refreshGraph();
          onBackPanel();
        }}
      />
    );
  }

  if (panel === "industry-detail" && selectedIndustry) {
    return (
      <IndustryDetail
        industry={selectedIndustry}
        onEdit={() => onPushPanel({ panel: "industry-edit", selectedIndustry })}
        onClose={onBackPanel}
        onRefresh={refreshGraph}
        onLoadSubgraph={onLoadSubgraph}
        onHighlightNodes={onHighlightNodes}
      />
    );
  }

  if (panel === "industry-create") {
    return (
      <IndustryForm
        mode="create"
        onClose={onBackPanel}
        onSuccess={(ind) => {
          setSelectedIndustry(ind);
          setPanel("industry-detail");
        }}
      />
    );
  }

  if (panel === "industry-edit" && selectedIndustry) {
    return (
      <IndustryForm
        mode="edit"
        industry={selectedIndustry}
        onClose={onBackPanel}
        onSuccess={(ind) => {
          setSelectedIndustry(ind);
          setPanel("industry-detail");
        }}
      />
    );
  }

  if (panel === "company-relation-detail" && selectedRelation) {
    return (
      <div className="flex h-full flex-col items-center justify-center bg-slate-900 text-slate-400">
        <p className="text-sm">公司视图已重构</p>
        <p className="mt-1 text-xs">此功能已移除，请使用探索接口</p>
        <button
          onClick={onBackPanel}
          className="mt-3 rounded bg-slate-800 px-3 py-1 text-xs hover:bg-slate-700"
        >
          关闭
        </button>
      </div>
    );
  }

  if (panel === "company-detail" && selectedCompany) {
    return (
      <CompanyDetail
        company={selectedCompany}
        onEdit={() => onPushPanel({ panel: "company-edit", selectedCompany })}
        onClose={onBackPanel}
        onRefresh={refreshGraph}
        onFocusInGraph={onFocusInGraph}
        onOpenMaterialModal={onOpenMaterialModal}
        onAddExposure={onAddExposure || (() => alert("添加暴露功能待实现"))}
      />
    );
  }

  if (panel === "company-create") {
    return (
      <CompanyForm
        mode="create"
        onClose={onBackPanel}
        onSuccess={(co) => {
          setSelectedCompany(co);
          setPanel("company-detail");
        }}
      />
    );
  }

  if (panel === "company-edit" && selectedCompany) {
    return (
      <CompanyForm
        mode="edit"
        company={selectedCompany}
        onClose={onBackPanel}
        onSuccess={(co) => {
          setSelectedCompany(co);
          setPanel("company-detail");
        }}
      />
    );
  }

  if (panel === "node-companies" && contextMenuNode) {
    return (
      <NodeCompaniesPanel
        nodeId={contextMenuNode.node_id}
        nodeName={contextMenuNode.canonical_name_zh}
        onClose={onBackPanel}
        onSelectCompany={(company) =>
          onPushPanel({
            panel: "company-detail",
            selectedCompany: company,
            selectedNode: null,
            selectedIndustry: null,
          })
        }
      />
    );
  }

  if (panel === "node-industries" && contextMenuNode) {
    return (
      <NodeIndustriesPanel
        nodeId={contextMenuNode.node_id}
        nodeName={contextMenuNode.canonical_name_zh}
        onClose={onBackPanel}
        onSelectIndustry={(industry) =>
          onPushPanel({
            panel: "industry-detail",
            selectedIndustry: industry,
            selectedNode: null,
            selectedCompany: null,
          })
        }
      />
    );
  }

  return null;
}
