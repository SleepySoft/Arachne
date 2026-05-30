import axios from "axios";
import {
  Company,
  CompanyNodeExposure,
  ComputationJob,
  GraphEdge,
  GraphRegistrationBatch,
  GraphStats,
  IndustrialFlowEdgeCreate,
  IndustrialNode,
  IndustrialNodeCreate,
  IndustrialNodeUpdate,
  Industry,
  IndustryNodeMapping,
  OntologyEdgeCreate,
  PaginatedCompanies,
  PaginatedEdges,
  PaginatedExposures,
  PaginatedIndustries,
  PaginatedMappings,
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

// ============================================================
// Industries
// ============================================================

export const listIndustries = async (
  page = 1,
  pageSize = 20,
  industryType?: string,
  status?: string,
  search?: string
): Promise<PaginatedIndustries> => {
  const params: Record<string, unknown> = { page, page_size: pageSize };
  if (industryType) params.industry_type = industryType;
  if (status) params.status = status;
  if (search) params.search = search;
  const res = await client.get("/industries", { params });
  return res.data;
};

export const getIndustry = async (industryId: string): Promise<Industry> => {
  const res = await client.get(`/industries/${industryId}`);
  return res.data;
};

export const createIndustry = async (data: Partial<Industry>): Promise<Industry> => {
  const res = await client.post("/industries", data);
  return res.data;
};

export const updateIndustry = async (
  industryId: string,
  data: Partial<Industry>
): Promise<Industry> => {
  const res = await client.put(`/industries/${industryId}`, data);
  return res.data;
};

export const deleteIndustry = async (industryId: string): Promise<void> => {
  await client.delete(`/industries/${industryId}`);
};

export const getIndustrySubgraph = async (
  industryId: string
): Promise<{ nodes: IndustrialNode[]; edges: GraphEdge[] }> => {
  const res = await client.get(`/industries/${industryId}/subgraph`);
  return res.data;
};

export const listIndustryMappings = async (
  industryId: string,
  page = 1,
  pageSize = 20
): Promise<PaginatedMappings> => {
  const res = await client.get(`/industries/${industryId}/mappings`, {
    params: { page, page_size: pageSize },
  });
  return res.data;
};

export const createIndustryMapping = async (
  industryId: string,
  data: Partial<IndustryNodeMapping>
): Promise<IndustryNodeMapping> => {
  const res = await client.post(`/industries/${industryId}/mappings`, data);
  return res.data;
};

export const deleteIndustryMapping = async (industryId: string, mappingId: string): Promise<void> => {
  await client.delete(`/industries/${industryId}/mappings/${mappingId}`);
};

// ============================================================
// Companies
// ============================================================

export const listCompanies = async (
  page = 1,
  pageSize = 20,
  country?: string,
  companyType?: string,
  status?: string,
  search?: string
): Promise<PaginatedCompanies> => {
  const params: Record<string, unknown> = { page, page_size: pageSize };
  if (country) params.country = country;
  if (companyType) params.company_type = companyType;
  if (status) params.status = status;
  if (search) params.search = search;
  const res = await client.get("/companies", { params });
  return res.data;
};

export const getCompany = async (companyId: string): Promise<Company> => {
  const res = await client.get(`/companies/${companyId}`);
  return res.data;
};

export const createCompany = async (data: Partial<Company>): Promise<Company> => {
  const res = await client.post("/companies", data);
  return res.data;
};

export const updateCompany = async (
  companyId: string,
  data: Partial<Company>
): Promise<Company> => {
  const res = await client.put(`/companies/${companyId}`, data);
  return res.data;
};

export const deleteCompany = async (companyId: string): Promise<void> => {
  await client.delete(`/companies/${companyId}`);
};

export const getCompanySubgraph = async (
  companyId: string
): Promise<{ nodes: IndustrialNode[]; edges: GraphEdge[] }> => {
  const res = await client.get(`/companies/${companyId}/subgraph`);
  return res.data;
};

export const listCompanyExposures = async (
  companyId: string,
  page = 1,
  pageSize = 20
): Promise<PaginatedExposures> => {
  const res = await client.get(`/companies/${companyId}/exposures`, {
    params: { page, page_size: pageSize },
  });
  return res.data;
};

export const createCompanyExposure = async (
  companyId: string,
  data: Partial<CompanyNodeExposure>
): Promise<CompanyNodeExposure> => {
  const res = await client.post(`/companies/${companyId}/exposures`, data);
  return res.data;
};

export const deleteCompanyExposure = async (companyId: string, exposureId: string): Promise<void> => {
  await client.delete(`/companies/${companyId}/exposures/${exposureId}`);
};

export const getCompaniesByNode = async (nodeId: string): Promise<{
  node_id: string;
  companies: Company[];
  exposures: CompanyNodeExposure[];
}> => {
  const res = await client.get(`/companies/by-node/${nodeId}`);
  return res.data;
};

export const getIndustriesByNode = async (nodeId: string): Promise<{
  node_id: string;
  industries: Industry[];
  mappings: IndustryNodeMapping[];
}> => {
  const res = await client.get(`/industries/by-node/${nodeId}`);
  return res.data;
};

export const getComputationJob = async (jobId: string): Promise<ComputationJob> => {
  const res = await client.get(`/computation-jobs/${jobId}`);
  return res.data;
};

export interface ExplorationGraph {
  nodes: {
    id: string;
    type: "company" | "material";
    label: string;
    company_type?: string;
    node_type?: string;
  }[];
  edges: {
    source: string;
    target: string;
    type: "exposure" | "industrial_flow";
    label?: string;
    activity_type?: string;
    edge_type?: string;
    strength?: number;
  }[];
}

export const getExplorationGraph = async (companyId: string): Promise<ExplorationGraph> => {
  const res = await client.get(`/companies/${companyId}/exploration-graph`);
  return res.data;
};

export interface MaterialConnection {
  company_id: string;
  company_name: string;
  exposures: {
    node_id: string;
    node_name: string;
    activity_type: string;
    weight: number;
    role?: string;
    peers: { company_id: string; name_zh: string; activity_type: string; weight: number }[];
    upstream: { company_id: string; name_zh: string; node_id: string; node_name: string; activity_type: string; weight: number }[];
    downstream: { company_id: string; name_zh: string; node_id: string; node_name: string; activity_type: string; weight: number }[];
  }[];
}

export const getMaterialConnections = async (companyId: string): Promise<MaterialConnection> => {
  const res = await client.get(`/companies/${companyId}/material-connections`);
  return res.data;
};

export interface ConnectedCompanies {
  node_id: string;
  node_name: string;
  peers: { id: string; type: string; label: string; activity_type: string; weight: number }[];
  upstream: { id: string; type: string; label: string; via_node_id: string; via_node_name: string; activity_type: string; weight: number }[];
  downstream: { id: string; type: string; label: string; via_node_id: string; via_node_name: string; activity_type: string; weight: number }[];
}

export const getMaterialCompanies = async (nodeId: string, excludeCompanyId?: string): Promise<ConnectedCompanies> => {
  const res = await client.get(`/companies/nodes/${nodeId}/connected-companies`, {
    params: excludeCompanyId ? { exclude_company_id: excludeCompanyId } : undefined,
  });
  return res.data;
};
