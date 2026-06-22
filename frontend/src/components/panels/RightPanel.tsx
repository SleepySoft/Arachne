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
  setSelectedNode: (node: IndustrialNode | null) => void;
  setSelectedEdge: (edge: GraphEdge | null) => void;
  setSelectedIndustry: (industry: Industry | null) => void;
  setSelectedCompany: (company: Company | null) => void;
  onLoadSubgraph: (nodes: unknown[], edges: unknown[]) => void;
  onHighlightNodes: (nodeIds: string[]) => void;
  onSelectNode: (node: IndustrialNode) => void;
  onSelectCompany: (company: Company) => void;
  onSelectIndustry: (industry: Industry) => void;
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
  pendingNodePosition,
  edgePrefillData,
  clearPendingEdgePrefill,
  setPanel,
  setSelectedNode,
  setSelectedEdge,
  setSelectedIndustry,
  setSelectedCompany,
  onLoadSubgraph,
  onHighlightNodes,
  onSelectNode,
  onSelectCompany,
  onSelectIndustry,
  onFocusInGraph,
  onOpenMaterialModal,
  onAddExposure,
}: RightPanelProps) {
  if (panel === "node-detail" && selectedNode) {
    return (
      <NodeDetail
        node={selectedNode}
        onEdit={() => setPanel("node-edit")}
        onClose={() => {
          setPanel("none");
          setSelectedNode(null);
        }}
        onRefresh={refreshGraph}
        onSelectNode={onSelectNode}
        onSelectCompany={onSelectCompany}
        onSelectIndustry={onSelectIndustry}
      />
    );
  }

  if (panel === "edge-detail" && selectedEdge) {
    return (
      <EdgeDetail
        edge={selectedEdge}
        onEdit={() => setPanel("edge-edit")}
        onClose={() => {
          setPanel("none");
          setSelectedEdge(null);
        }}
        onRefresh={refreshGraph}
      />
    );
  }

  if (panel === "node-create") {
    return (
      <NodeForm
        mode="create"
        onClose={() => setPanel("none")}
        onSuccess={(node) => {
          setSelectedNode(node);
          setPanel("node-detail");
          if (pendingNodePosition) {
            onNodeCreated?.(node, pendingNodePosition);
          } else {
            refreshGraph();
          }
        }}
      />
    );
  }

  if (panel === "node-edit" && selectedNode) {
    return (
      <NodeForm
        mode="edit"
        node={selectedNode}
        onClose={() => setPanel("node-detail")}
        onSuccess={(node) => {
          setSelectedNode(node);
          setPanel("node-detail");
          refreshGraph();
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
          setPanel("none");
        }}
        onSuccess={(edge) => {
          setSelectedEdge(edge);
          setPanel("edge-detail");
          clearPendingEdgePrefill?.();
          refreshGraph();
        }}
      />
    );
  }

  if (panel === "edge-edit" && selectedEdge) {
    return (
      <EdgeForm
        mode="edit"
        edge={selectedEdge}
        onClose={() => setPanel("edge-detail")}
        onSuccess={(edge) => {
          setSelectedEdge(edge);
          setPanel("edge-detail");
          refreshGraph();
        }}
      />
    );
  }

  if (panel === "batch-upload") {
    return (
      <BatchUploader
        onClose={() => setPanel("none")}
        onSuccess={refreshGraph}
      />
    );
  }

  if (panel === "industry-detail" && selectedIndustry) {
    return (
      <IndustryDetail
        industry={selectedIndustry}
        onEdit={() => setPanel("industry-edit")}
        onClose={() => {
          setPanel("none");
          setSelectedIndustry(null);
        }}
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
        onClose={() => setPanel("none")}
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
        onClose={() => setPanel("industry-detail")}
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
          onClick={() => {
            setPanel("none");
          }}
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
        onEdit={() => setPanel("company-edit")}
        onClose={() => {
          setPanel("none");
          setSelectedCompany(null);
        }}
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
        onClose={() => setPanel("none")}
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
        onClose={() => setPanel("company-detail")}
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
        onClose={() => setPanel("none")}
        onSelectCompany={(company) => {
          setSelectedCompany(company);
          setPanel("company-detail");
        }}
      />
    );
  }

  if (panel === "node-industries" && contextMenuNode) {
    return (
      <NodeIndustriesPanel
        nodeId={contextMenuNode.node_id}
        nodeName={contextMenuNode.canonical_name_zh}
        onClose={() => setPanel("none")}
        onSelectIndustry={(industry) => {
          setSelectedIndustry(industry);
          setPanel("industry-detail");
        }}
      />
    );
  }

  return null;
}
