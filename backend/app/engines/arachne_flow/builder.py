"""In-memory flow graph builder and analyzer.

This module sits between the per-file YAML parser and the Neo4j storage layer:
all flow files are first loaded into a single in-memory ``FlowGraph`` where
shared resources/methods are deduplicated, actions are namespaced by flow,
conflicts are detected, and statistics are computed. Only then is the graph
persisted to Neo4j.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from app.engines.arachne_flow.parser import parse_flow_file
from app.engines.arachne_flow.schemas import (
    FlowAction,
    FlowMethod,
    FlowResource,
    FlowTriple,
    InputRole,
    OutputRole,
    ParsedFlow,
    SpecialRole,
)
from app.services import node_storage


@dataclass
class SharedNodeStat:
    node_id: str
    flow_count: int
    flow_ids: List[str]


@dataclass
class MethodActionStat:
    method_id: str
    action_count: int
    action_ids: List[str]
    flow_ids: List[str]


@dataclass
class MissingInPgStat:
    resources: List[str]
    methods: List[str]
    actions_with_missing_method_ref: List[str]


@dataclass
class CommonPathStat:
    path: List[str]
    flow_count: int
    flow_ids: List[str]


@dataclass
class FlowGraphStatistics:
    flow_count: int = 0
    resource_count: int = 0
    method_count: int = 0
    action_count: int = 0
    triple_count: int = 0
    edge_type_counts: Dict[str, int] = field(default_factory=dict)

    # Cross-flow sharing
    shared_resources: List[SharedNodeStat] = field(default_factory=list)
    shared_methods: List[SharedNodeStat] = field(default_factory=list)
    methods_referenced_by_multiple_actions: List[MethodActionStat] = field(
        default_factory=list
    )

    # PG metadata coverage
    missing_in_pg: MissingInPgStat = field(
        default_factory=lambda: MissingInPgStat([], [], [])
    )

    # Process backbone for future merge optimization
    common_paths: List[CommonPathStat] = field(default_factory=list)
    common_path_signature_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "flow_count": self.flow_count,
            "resource_count": self.resource_count,
            "method_count": self.method_count,
            "action_count": self.action_count,
            "triple_count": self.triple_count,
            "edge_type_counts": self.edge_type_counts,
            "shared_resources": [
                {"node_id": s.node_id, "flow_count": s.flow_count, "flow_ids": s.flow_ids}
                for s in self.shared_resources
            ],
            "shared_methods": [
                {"node_id": s.node_id, "flow_count": s.flow_count, "flow_ids": s.flow_ids}
                for s in self.shared_methods
            ],
            "methods_referenced_by_multiple_actions": [
                {
                    "method_id": m.method_id,
                    "action_count": m.action_count,
                    "action_ids": m.action_ids,
                    "flow_ids": m.flow_ids,
                }
                for m in self.methods_referenced_by_multiple_actions
            ],
            "missing_in_pg": {
                "resources": self.missing_in_pg.resources,
                "methods": self.missing_in_pg.methods,
                "actions_with_missing_method_ref": self.missing_in_pg.actions_with_missing_method_ref,
            },
            "common_paths": [
                {"path": p.path, "flow_count": p.flow_count, "flow_ids": p.flow_ids}
                for p in self.common_paths
            ],
            "common_path_signature_count": self.common_path_signature_count,
        }


@dataclass
class FlowGraph:
    """A unified, in-memory arachne-flow graph built from one or more files."""

    resources: Dict[str, FlowResource] = field(default_factory=dict)
    methods: Dict[str, FlowMethod] = field(default_factory=dict)
    actions: Dict[str, FlowAction] = field(default_factory=dict)
    triples: List[Tuple[FlowTriple, str]] = field(default_factory=list)
    flow_ids: List[str] = field(default_factory=list)
    # flow_id -> [included flow_id stems]; include is a dependency declaration
    includes: Dict[str, List[str]] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def resource_node_ids(self) -> Set[str]:
        return set(self.resources.keys())

    def method_node_ids(self) -> Set[str]:
        return set(self.methods.keys())

    def dual_node_ids(self) -> Set[str]:
        return set(self.resources.keys()) & set(self.actions.keys())


class FlowGraphBuilder:
    """Build a ``FlowGraph`` by accumulating parsed flow documents."""

    def __init__(self) -> None:
        self.graph = FlowGraph()

    @classmethod
    def from_directory(
        cls,
        directory: Path,
        exclude: Optional[Set[str]] = None,
    ) -> "FlowGraphBuilder":
        """Parse all ``*.yaml`` files under a directory (recursively) and build a unified graph."""
        builder = cls()
        exclude = exclude or {"manifest.yaml"}
        paths = sorted(
            p
            for p in directory.rglob("*.yaml")
            if p.name not in exclude and "legacy" not in p.parts
        )
        for path in paths:
            parsed = parse_flow_file(path)
            builder.add_parsed_flow(parsed)
        return builder

    def add_parsed_flow(self, parsed: ParsedFlow) -> None:
        """Incorporate one parsed flow into the global in-memory graph."""
        flow_id = parsed.flow_id
        self.graph.flow_ids.append(flow_id)
        # include is a dependency declaration; normalize to flow_id stems.
        self.graph.includes[flow_id] = [
            Path(name).stem for name in (parsed.includes or [])
        ]

        dual_ids = set(parsed.resources.keys()) & set(parsed.actions.keys())

        # Resources are global singletons keyed by resource_id.
        for res in parsed.resources.values():
            existing = self.graph.resources.get(res.resource_id)
            if existing is None:
                self.graph.resources[res.resource_id] = res
            else:
                if existing.resource_type != res.resource_type:
                    self.graph.warnings.append(
                        f"resource '{res.resource_id}' has conflicting resource_type "
                        f"across flows: {existing.resource_type.value} vs {res.resource_type.value}"
                    )
                if res.local_name and not existing.local_name:
                    existing.local_name = res.local_name

        # Methods are global singletons keyed by method_id.
        for method in parsed.methods.values():
            existing = self.graph.methods.get(method.method_id)
            if existing is None:
                self.graph.methods[method.method_id] = method
            else:
                if method.method_name and not existing.method_name:
                    existing.method_name = method.method_name

        # Actions are unique occurrences namespaced by flow_id, except dual-role
        # nodes which are shared like resources.
        for action in parsed.actions.values():
            if action.action_id in dual_ids:
                ns_id = action.action_id
            else:
                ns_id = f"{flow_id}:{action.action_id}"

            if ns_id in self.graph.actions:
                self.graph.warnings.append(
                    f"duplicate action '{ns_id}' encountered in flow '{flow_id}'"
                )
                continue

            self.graph.actions[ns_id] = FlowAction(
                action_id=action.action_id,
                action_type=action.action_type,
                flow_id=flow_id,
                method_ref=action.method_ref,
            )

        # Triples: resolve action IDs to their namespaced form.
        method_ids = set(parsed.methods.keys())
        for triple in parsed.triples:
            ns_triple = self._namespace_triple(triple, flow_id, dual_ids, method_ids)
            self.graph.triples.append((ns_triple, flow_id))

    def _namespace_triple(
        self,
        triple: FlowTriple,
        flow_id: str,
        dual_ids: Set[str],
        method_ids: Set[str],
    ) -> FlowTriple:
        """Namespace ACTION nodes per-flow; leave RESOURCE and METHOD nodes as-is."""
        input_roles = {r.value for r in InputRole}
        output_roles = {r.value for r in OutputRole}
        pred = triple.predicate

        def resolve(raw_id: str, role: str) -> str:
            # RESOURCE and METHOD nodes are global — never namespace them.
            if raw_id in dual_ids or raw_id in method_ids:
                return raw_id
            if role == "target" and pred in input_roles:
                return f"{flow_id}:{raw_id}"
            if role == "source" and pred in output_roles:
                return f"{flow_id}:{raw_id}"
            if pred == SpecialRole.NEXT.value:
                return f"{flow_id}:{raw_id}"
            if pred == SpecialRole.REF.value and role == "source":
                return f"{flow_id}:{raw_id}"
            return raw_id

        return FlowTriple(
            source=resolve(triple.source, "source"),
            predicate=triple.predicate,
            target=resolve(triple.target, "target"),
        )

    def effective_flow_ids(self, flow_id: str) -> List[str]:
        """Return ``flow_id`` plus all transitively included flow ids."""
        seen: Set[str] = set()
        order: List[str] = []

        def visit(fid: str) -> None:
            if fid in seen:
                return
            seen.add(fid)
            order.append(fid)
            for dep in self.graph.includes.get(fid, []):
                visit(dep)

        visit(flow_id)
        return order

    def validate_global(self) -> bool:
        """Run global consistency checks and populate ``self.graph.errors``."""
        self.graph.errors.clear()

        # Detect a node used as both resource and method (should never happen).
        resource_method_conflicts = set(self.graph.resources.keys()) & set(
            self.graph.methods.keys()
        )
        if resource_method_conflicts:
            for node_id in sorted(resource_method_conflicts):
                self.graph.errors.append(
                    f"node '{node_id}' is used both as a RESOURCE and as a METHOD"
                )

        # Detect action IDs that collide with resource IDs outside of dual nodes.
        action_resource_conflicts = (
            set(self.graph.actions.keys()) & set(self.graph.resources.keys())
        ) - self.graph.dual_node_ids()
        if action_resource_conflicts:
            for node_id in sorted(action_resource_conflicts):
                self.graph.errors.append(
                    f"action '{node_id}' collides with a RESOURCE node outside dual roles"
                )

        # Validate include graph: referenced flows must exist, no cycles.
        include_graph = self.graph.includes
        for flow_id, deps in include_graph.items():
            for dep in deps:
                if dep not in include_graph:
                    self.graph.errors.append(
                        f"flow '{flow_id}' includes unknown flow '{dep}'"
                    )

        def visit_include(fid: str, stack: List[str]) -> None:
            if fid in stack:
                cycle = " -> ".join(stack + [fid])
                self.graph.errors.append(f"circular include detected: {cycle}")
                return
            for dep in include_graph.get(fid, []):
                visit_include(dep, stack + [fid])

        for fid in include_graph:
            visit_include(fid, [])

        # Producer/consumer analysis for RESOURCEs.
        producers: Dict[str, Set[str]] = {}  # resource_id -> set of producing flows
        for triple, flow_id in self.graph.triples:
            if triple.predicate in {r.value for r in OutputRole}:
                producers.setdefault(triple.target, set()).add(flow_id)

        # Warn when the same RESOURCE is produced by multiple flows (ambiguous).
        for rid, flows in producers.items():
            if len(flows) > 1:
                self.graph.warnings.append(
                    f"resource '{rid}' is produced by multiple flows: {sorted(flows)}"
                )

        # Check that external inputs are either produced by an included flow or
        # are genuine leaf inputs (not produced anywhere).
        for flow_id in self.graph.flow_ids:
            consumed: Set[str] = set()
            produced: Set[str] = set()
            for triple, fid in self.graph.triples:
                if fid != flow_id:
                    continue
                if triple.predicate in {r.value for r in InputRole}:
                    consumed.add(triple.source)
                if triple.predicate in {r.value for r in OutputRole}:
                    produced.add(triple.target)
            external_inputs = consumed - produced
            deps = set(self.effective_flow_ids(flow_id)) - {flow_id}
            for rid in sorted(external_inputs):
                if rid not in producers:
                    # leaf input / raw material; allowed.
                    continue
                producer_flows = producers.get(rid, set())
                if not producer_flows & deps:
                    self.graph.warnings.append(
                        f"flow '{flow_id}' consumes '{rid}' produced by {sorted(producer_flows)} "
                        f"but does not include any of them"
                    )

        return len(self.graph.errors) == 0

    async def compute_statistics(
        self,
        max_path_length: int = 3,
        top_k: int = 10,
    ) -> FlowGraphStatistics:
        """Compute statistics on the in-memory graph, including PG coverage."""
        stats = FlowGraphStatistics()
        stats.flow_count = len(self.graph.flow_ids)
        stats.resource_count = len(self.graph.resources)
        stats.method_count = len(self.graph.methods)
        stats.action_count = len(self.graph.actions)
        stats.triple_count = len(self.graph.triples)

        # Edge type counts
        for triple, _ in self.graph.triples:
            stats.edge_type_counts[triple.predicate] = (
                stats.edge_type_counts.get(triple.predicate, 0) + 1
            )

        # Cross-flow reference counts for resources and methods
        resource_flows: Dict[str, Set[str]] = {rid: set() for rid in self.graph.resources}
        method_flows: Dict[str, Set[str]] = {mid: set() for mid in self.graph.methods}
        method_actions: Dict[str, List[Tuple[str, str]]] = {
            mid: [] for mid in self.graph.methods
        }  # method_id -> [(action_ns_id, flow_id)]

        for triple, flow_id in self.graph.triples:
            src, tgt, pred = triple.source, triple.target, triple.predicate
            if pred in {r.value for r in InputRole} and src in resource_flows:
                resource_flows[src].add(flow_id)
            if pred in {r.value for r in OutputRole} and tgt in resource_flows:
                resource_flows[tgt].add(flow_id)
            if pred == SpecialRole.REF.value:
                if tgt in method_flows:
                    method_flows[tgt].add(flow_id)
                if tgt in method_actions:
                    method_actions[tgt].append((src, flow_id))

        stats.shared_resources = [
            SharedNodeStat(node_id=rid, flow_count=len(flows), flow_ids=sorted(flows))
            for rid, flows in resource_flows.items()
            if len(flows) > 1
        ]
        stats.shared_resources.sort(key=lambda x: (-x.flow_count, x.node_id))

        stats.shared_methods = [
            SharedNodeStat(node_id=mid, flow_count=len(flows), flow_ids=sorted(flows))
            for mid, flows in method_flows.items()
            if len(flows) > 1
        ]
        stats.shared_methods.sort(key=lambda x: (-x.flow_count, x.node_id))

        stats.methods_referenced_by_multiple_actions = [
            MethodActionStat(
                method_id=mid,
                action_count=len(action_refs),
                action_ids=[a[0] for a in action_refs],
                flow_ids=sorted({a[1] for a in action_refs}),
            )
            for mid, action_refs in method_actions.items()
            if len(action_refs) > 1
        ]
        stats.methods_referenced_by_multiple_actions.sort(
            key=lambda x: (-x.action_count, x.method_id)
        )

        # PostgreSQL coverage
        pg_existing = await node_storage.get_nodes_by_ids(
            list(set(self.graph.resources.keys()) | set(self.graph.methods.keys()))
        )
        missing_resources = [
            rid for rid in self.graph.resources if rid not in pg_existing
        ]
        missing_methods = [
            mid for mid in self.graph.methods if mid not in pg_existing
        ]
        missing_action_methods = [
            aid
            for aid, action in self.graph.actions.items()
            if action.method_ref and action.method_ref not in pg_existing
        ]
        stats.missing_in_pg = MissingInPgStat(
            resources=missing_resources,
            methods=missing_methods,
            actions_with_missing_method_ref=missing_action_methods,
        )

        # Common action paths (by method_ref) across flows
        stats.common_paths, stats.common_path_signature_count = self._find_common_paths(
            max_path_length=max_path_length,
            top_k=top_k,
        )

        return stats

    def _find_common_paths(
        self,
        max_path_length: int,
        top_k: int,
    ) -> Tuple[List[CommonPathStat], int]:
        """Find action-method sequences that appear in multiple flows.

        Paths are abstracted by each ACTION's ``method_ref`` so that the same
        process fragment used in different products can be identified.
        """
        input_roles = {r.value for r in InputRole}
        output_roles = {r.value for r in OutputRole}

        # Build per-flow action graphs.
        flow_action_graphs: Dict[str, Dict[str, Set[str]]] = {}
        flow_action_methods: Dict[str, Dict[str, Optional[str]]] = {}

        for triple, flow_id in self.graph.triples:
            src, tgt, pred = triple.source, triple.target, triple.predicate

            # Ensure flow graph exists.
            if flow_id not in flow_action_graphs:
                flow_action_graphs[flow_id] = {}
                flow_action_methods[flow_id] = {}

            # Register action method_refs.
            if src in self.graph.actions:
                flow_action_methods[flow_id][src] = self.graph.actions[src].method_ref
            if tgt in self.graph.actions:
                flow_action_methods[flow_id][tgt] = self.graph.actions[tgt].method_ref

            # Direct next edge between two actions.
            if pred == SpecialRole.NEXT.value:
                if src in self.graph.actions and tgt in self.graph.actions:
                    flow_action_graphs[flow_id].setdefault(src, set()).add(tgt)
                continue

            # Output edge: remember action -> resource.
            if pred in output_roles and src in self.graph.actions:
                flow_action_graphs[flow_id].setdefault(src, set())
                # We will link to a following input edge via resource node below.

            # Input edge: resource -> action. Try to connect a preceding output.
            if pred in input_roles and tgt in self.graph.actions:
                # Find any earlier output edge in the same flow that produced this resource.
                for prior_triple, prior_flow_id in self.graph.triples:
                    if prior_flow_id != flow_id:
                        continue
                    p_pred = prior_triple.predicate
                    p_src = prior_triple.source
                    p_tgt = prior_triple.target
                    if p_pred in output_roles and p_src in self.graph.actions and p_tgt == src:
                        flow_action_graphs[flow_id].setdefault(p_src, set()).add(tgt)

        # Enumerate simple paths per flow and count signatures across flows.
        signature_flows: Dict[Tuple[str, ...], Set[str]] = {}

        for flow_id, adj in flow_action_graphs.items():
            nodes = list(adj.keys())
            max_nodes = max(2, max_path_length)

            def dfs(current: str, visited: List[str]):
                if len(visited) >= max_nodes:
                    return
                for nxt in adj.get(current, set()):
                    if nxt in visited:
                        continue
                    path = visited + [nxt]
                    signature = tuple(
                        flow_action_methods[flow_id].get(node, node) or node
                        for node in path
                    )
                    signature_flows.setdefault(signature, set()).add(flow_id)
                    dfs(nxt, path)

            for start in nodes:
                dfs(start, [start])

        # Filter signatures that appear in more than one flow and sort by coverage.
        common = [
            CommonPathStat(
                path=list(signature),
                flow_count=len(flows),
                flow_ids=sorted(flows),
            )
            for signature, flows in signature_flows.items()
            if len(flows) > 1
        ]
        common.sort(key=lambda x: (-x.flow_count, x.path))
        return common[:top_k], len(signature_flows)
