import { useQuery } from "@tanstack/react-query";
import { getNeighbors, getSubgraph, listEdges, listNodes } from "@/services/api";

export function useGraphData(centerNodeId?: string, depth = 2) {
  return useQuery({
    queryKey: ["subgraph", centerNodeId, depth],
    queryFn: () =>
      centerNodeId ? getSubgraph(centerNodeId, depth) : Promise.resolve(null),
    enabled: !!centerNodeId,
  });
}

export function useNeighbors(nodeId?: string) {
  return useQuery({
    queryKey: ["neighbors", nodeId],
    queryFn: () => (nodeId ? getNeighbors(nodeId) : Promise.resolve(null)),
    enabled: !!nodeId,
  });
}

export function useNodes(
  page = 1,
  pageSize = 20,
  entityType?: string,
  status?: string,
  search?: string
) {
  return useQuery({
    queryKey: ["nodes", page, pageSize, entityType, status, search],
    queryFn: () => listNodes(page, pageSize, entityType, status, search),
  });
}

export function useEdges(
  page = 1,
  pageSize = 20,
  edgeNamespace?: string,
  edgeType?: string
) {
  return useQuery({
    queryKey: ["edges", page, pageSize, edgeNamespace, edgeType],
    queryFn: () => listEdges(page, pageSize, edgeNamespace, edgeType),
  });
}
