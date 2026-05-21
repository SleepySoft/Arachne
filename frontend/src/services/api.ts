import axios from "axios";
import {
  GraphEdge,
  GraphRegistrationBatch,
  GraphStats,
  IndustrialFlowEdgeCreate,
  IndustrialNode,
  IndustrialNodeCreate,
  IndustrialNodeUpdate,
  OntologyEdgeCreate,
  PaginatedEdges,
  PaginatedNodes,
  SubgraphResult,
} from "@/types";

const API_BASE = "/api/v1";

const client = axios.create({
  baseURL: API_BASE,
  headers: {
    "Content-Type": "application/json",
  },
});

// Nodes
export const listNodes = async (
  page = 1,
  pageSize = 20,
  entityType?: string,
  status?: string,
  search?: string
): Promise<PaginatedNodes> => {
  const params: Record<string, unknown> = { page, page_size: pageSize };
  if (entityType) params.entity_type = entityType;
  if (status) params.status = status;
  if (search) params.search = search;
  const res = await client.get("/nodes", { params });
  return res.data;
};

export const getNode = async (nodeId: string): Promise<IndustrialNode> => {
  const res = await client.get(`/nodes/${nodeId}`);
  return res.data;
};

export const createNode = async (data: IndustrialNodeCreate): Promise<IndustrialNode> => {
  const res = await client.post("/nodes", data);
  return res.data;
};

export const updateNode = async (
  nodeId: string,
  data: IndustrialNodeUpdate
): Promise<IndustrialNode> => {
  const res = await client.put(`/nodes/${nodeId}`, data);
  return res.data;
};

export const deleteNode = async (nodeId: string): Promise<void> => {
  await client.delete(`/nodes/${nodeId}`);
};

// Edges
export const listEdges = async (
  page = 1,
  pageSize = 20,
  edgeNamespace?: string,
  edgeType?: string,
  fromNode?: string,
  toNode?: string
): Promise<PaginatedEdges> => {
  const params: Record<string, unknown> = { page, page_size: pageSize };
  if (edgeNamespace) params.edge_namespace = edgeNamespace;
  if (edgeType) params.edge_type = edgeType;
  if (fromNode) params.from_node = fromNode;
  if (toNode) params.to_node = toNode;
  const res = await client.get("/edges", { params });
  return res.data;
};

export const getEdge = async (edgeId: string): Promise<GraphEdge> => {
  const res = await client.get(`/edges/${edgeId}`);
  return res.data;
};

export const createEdge = async (
  data: IndustrialFlowEdgeCreate | OntologyEdgeCreate
): Promise<GraphEdge> => {
  const res = await client.post("/edges", data);
  return res.data;
};

export const updateEdge = async (edgeId: string, data: Partial<GraphEdge>): Promise<GraphEdge> => {
  const res = await client.put(`/edges/${edgeId}`, data);
  return res.data;
};

export const deleteEdge = async (edgeId: string): Promise<void> => {
  await client.delete(`/edges/${edgeId}`);
};

// Batches
export const submitBatch = async (
  batch: GraphRegistrationBatch
): Promise<{
  batch_id: string;
  nodes_created: number;
  nodes_updated: number;
  edges_created: number;
  edges_updated: number;
  rejected_or_pending_stored: number;
  errors: unknown[];
}> => {
  const res = await client.post("/batches", batch);
  return res.data;
};

// Query
export const getSubgraph = async (
  nodeId: string,
  depth = 2
): Promise<SubgraphResult> => {
  const res = await client.get(`/query/subgraph/${nodeId}`, { params: { depth } });
  return res.data;
};

export const getNeighbors = async (
  nodeId: string
): Promise<{ nodes: IndustrialNode[]; edges: GraphEdge[] }> => {
  const res = await client.get(`/query/neighbors/${nodeId}`);
  return res.data;
};

export const getPaths = async (
  fromNode: string,
  toNode: string,
  maxDepth = 5
): Promise<{
  from_node: string;
  to_node: string;
  paths: unknown[];
}> => {
  const res = await client.get("/query/path", {
    params: { from_node: fromNode, to_node: toNode, max_depth: maxDepth },
  });
  return res.data;
};

export const getStats = async (): Promise<GraphStats> => {
  const res = await client.get("/query/stats");
  return res.data;
};

export const getConflicts = async (): Promise<unknown[]> => {
  const res = await client.get("/query/conflicts");
  return res.data;
};
