import { GraphEdge, GraphNode } from "@/types";

/**
 * Collapse included flows in a preview graph into per-flow folder nodes.
 *
 * The backend tags each node with `properties.flow_ids` (which flows reference
 * it) and each edge with `properties.flow_id` (which flow it belongs to). The
 * frontend uses these tags to hide nodes/edges that belong exclusively to
 * included flows and redirects cross-boundary edges to folder nodes.
 *
 * Shared nodes (referenced by both the current flow and included flows, or by
 * multiple flows) stay visible, which is why a node that is hard to assign to a
 * single group is never hidden.
 */
export function collapsePreviewGraph(
  nodes: GraphNode[],
  edges: GraphEdge[],
  includes: string[],
  currentFlowId: string
): { nodes: GraphNode[]; edges: GraphEdge[] } {
  if (!includes.length) return { nodes, edges };
  const includeSet = new Set(includes);

  // Interface nodes are endpoints of the current flow's own edges.
  const interfaceNodeIds = new Set<string>();
  for (const e of edges) {
    if ((e.properties?.flow_id as string) === currentFlowId) {
      interfaceNodeIds.add(e.from_node);
      interfaceNodeIds.add(e.to_node);
    }
  }

  // Partition nodes into visible vs hidden (exclusive to included flows).
  const visibleNodeIds = new Set<string>();
  const hiddenNodeIds = new Set<string>();
  for (const n of nodes) {
    if (interfaceNodeIds.has(n.node_id)) {
      visibleNodeIds.add(n.node_id);
      continue;
    }
    const flowIds = (n.properties?.flow_ids as string[]) || [];
    const belongsToCurrent = flowIds.includes(currentFlowId);
    const belongsToOther = flowIds.some(
      (fid) => fid !== currentFlowId && !includeSet.has(fid)
    );
    if (belongsToCurrent || belongsToOther || flowIds.length === 0) {
      visibleNodeIds.add(n.node_id);
    } else {
      hiddenNodeIds.add(n.node_id);
    }
  }

  // Hide edges that belong to included flows; keep current-flow edges.
  const hiddenEdgeIds = new Set<string>();
  for (const e of edges) {
    const fid = (e.properties?.flow_id as string) || "";
    if (includeSet.has(fid)) {
      hiddenEdgeIds.add(e.edge_id);
    }
  }

  // For each included flow, find interface nodes it connects to.
  const flowToInterface = new Map<string, Set<string>>();
  for (const e of edges) {
    const fid = (e.properties?.flow_id as string) || "";
    if (!includeSet.has(fid)) continue;
    if (interfaceNodeIds.has(e.from_node)) {
      if (!flowToInterface.has(fid)) flowToInterface.set(fid, new Set());
      flowToInterface.get(fid)!.add(e.from_node);
    }
    if (interfaceNodeIds.has(e.to_node)) {
      if (!flowToInterface.has(fid)) flowToInterface.set(fid, new Set());
      flowToInterface.get(fid)!.add(e.to_node);
    }
  }

  const folderNodes: GraphNode[] = [];
  const folderEdges: GraphEdge[] = [];
  for (const [fid, interfaceIds] of flowToInterface) {
    const folderId = `flow_folder:${fid}`;
    folderNodes.push({
      node_id: folderId,
      label: `📁 ${fid}`,
      entity_type: "arachne_flow:folder",
      properties: {
        node_kind: "folder",
        is_flow_folder: true,
        flow_id: fid,
        flow_ids: [fid],
      },
    } as GraphNode);

    for (const nid of interfaceIds) {
      // Determine whether the included flow produces or consumes the interface node.
      const produces = edges.some(
        (e) =>
          (e.properties?.flow_id as string) === fid &&
          e.to_node === nid &&
          e.from_node !== nid
      );
      const consumes = edges.some(
        (e) => (e.properties?.flow_id as string) === fid && e.from_node === nid
      );
      if (produces) {
        folderEdges.push({
          edge_id: `${folderId}->${nid}:primary_result`,
          from_node: folderId,
          to_node: nid,
          edge_namespace: "arachne_flow",
          edge_type: "primary_result",
          edge_type_label: "主产物",
          properties: { flow_id: currentFlowId, is_folder_edge: true },
        } as unknown as GraphEdge);
      } else if (consumes) {
        folderEdges.push({
          edge_id: `${nid}->${folderId}:feedstock`,
          from_node: nid,
          to_node: folderId,
          edge_namespace: "arachne_flow",
          edge_type: "feedstock",
          edge_type_label: "原料",
          properties: { flow_id: currentFlowId, is_folder_edge: true },
        } as unknown as GraphEdge);
      }
    }
  }

  const visibleNodes = nodes
    .filter((n) => visibleNodeIds.has(n.node_id))
    .concat(folderNodes);
  const visibleEdges = edges
    .filter(
      (e) =>
        !hiddenEdgeIds.has(e.edge_id) &&
        visibleNodeIds.has(e.from_node) &&
        visibleNodeIds.has(e.to_node)
    )
    .concat(folderEdges);

  return { nodes: visibleNodes, edges: visibleEdges };
}
