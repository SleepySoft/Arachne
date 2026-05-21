import { useState } from "react";
import { GraphEdge, IndustrialNode } from "@/types";
import { BatchUploader } from "@/components/BatchUploader";
import { EdgeDetail } from "@/components/EdgeDetail";
import { EdgeForm } from "@/components/EdgeForm";
import { FilterPanel } from "@/components/FilterPanel";
import { GraphCanvas } from "@/components/GraphCanvas";
import { Layout } from "@/components/Layout";
import { NodeDetail } from "@/components/NodeDetail";
import { NodeForm } from "@/components/NodeForm";
import { SearchPanel } from "@/components/SearchPanel";
import { StatsBar } from "@/components/StatsBar";

export type PanelType =
  | "none"
  | "node-detail"
  | "edge-detail"
  | "node-create"
  | "node-edit"
  | "edge-create"
  | "edge-edit"
  | "batch-upload";

export default function App() {
  const [selectedNode, setSelectedNode] = useState<IndustrialNode | null>(null);
  const [selectedEdge, setSelectedEdge] = useState<GraphEdge | null>(null);
  const [panel, setPanel] = useState<PanelType>("none");
  const [activeFilters, setActiveFilters] = useState<{
    edgeNamespaces: string[];
    edgeTypes: string[];
    entityTypes: string[];
    status: string[];
    confidence: string[];
  }>({
    edgeNamespaces: ["industrial_flow", "ontology"],
    edgeTypes: [],
    entityTypes: [],
    status: [],
    confidence: [],
  });
  const [graphKey, setGraphKey] = useState(0);

  const handleNodeClick = (node: IndustrialNode) => {
    setSelectedNode(node);
    setSelectedEdge(null);
    setPanel("node-detail");
  };

  const handleEdgeClick = (edge: GraphEdge) => {
    setSelectedEdge(edge);
    setSelectedNode(null);
    setPanel("edge-detail");
  };

  const refreshGraph = () => {
    setGraphKey((k) => k + 1);
  };

  return (
    <Layout
      topBar={<StatsBar />}
      leftSidebar={
        <FilterPanel
          filters={activeFilters}
          onChange={setActiveFilters}
        />
      }
      centerCanvas={
        <GraphCanvas
          key={graphKey}
          onNodeClick={handleNodeClick}
          onEdgeClick={handleEdgeClick}
          filters={activeFilters}
          highlightNodeId={selectedNode?.node_id}
        />
      }
      searchPanel={
        <SearchPanel
          onSelectNode={(node) => {
            setSelectedNode(node);
            setPanel("node-detail");
          }}
          onCreateNode={() => setPanel("node-create")}
          onCreateEdge={() => setPanel("edge-create")}
          onUploadBatch={() => setPanel("batch-upload")}
        />
      }
      rightPanel={
        panel === "node-detail" && selectedNode ? (
          <NodeDetail
            node={selectedNode}
            onEdit={() => setPanel("node-edit")}
            onClose={() => {
              setPanel("none");
              setSelectedNode(null);
            }}
            onRefresh={refreshGraph}
          />
        ) : panel === "edge-detail" && selectedEdge ? (
          <EdgeDetail
            edge={selectedEdge}
            onEdit={() => setPanel("edge-edit")}
            onClose={() => {
              setPanel("none");
              setSelectedEdge(null);
            }}
            onRefresh={refreshGraph}
          />
        ) : panel === "node-create" ? (
          <NodeForm
            mode="create"
            onClose={() => setPanel("none")}
            onSuccess={(node) => {
              setSelectedNode(node);
              setPanel("node-detail");
              refreshGraph();
            }}
          />
        ) : panel === "node-edit" && selectedNode ? (
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
        ) : panel === "edge-create" ? (
          <EdgeForm
            mode="create"
            onClose={() => setPanel("none")}
            onSuccess={(edge) => {
              setSelectedEdge(edge);
              setPanel("edge-detail");
              refreshGraph();
            }}
          />
        ) : panel === "edge-edit" && selectedEdge ? (
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
        ) : panel === "batch-upload" ? (
          <BatchUploader
            onClose={() => setPanel("none")}
            onSuccess={refreshGraph}
          />
        ) : null
      }
    />
  );
}
