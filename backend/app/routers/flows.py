"""Arachne-flow management endpoints.

These endpoints are intentionally separate from the legacy graph routes: they
let clients discover which flow files exist, see their compile status, and ask
the backend to (re)compile a flow into the Neo4j flow graph.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Set

import yaml
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database_postgres import get_postgres_pool
from app.engines.arachne_flow.parser import FlowParseError, parse_flow_file
from app.engines.arachne_flow.preview import preview_flow_graph
from app.engines.arachne_flow import storage
from app.models.core import GraphEdge, GraphNode, SubgraphResult

router = APIRouter()

ROOT = Path(__file__).resolve().parents[3]
FLOW_DIR = ROOT / "data" / "flows" / "semiconductor"
MANIFEST_FILE = FLOW_DIR / "manifest.yaml"


class FlowListItem(BaseModel):
    flow_id: str
    title: str
    root_product: str
    file: str
    triples: int
    status: Optional[str] = None
    md5: Optional[str] = None
    compiled_at: Optional[str] = None


class FlowCompileResult(BaseModel):
    flow_id: str
    resources: int
    actions: int
    methods: int
    edges: int
    dual: int


class FlowSubgraphRequest(BaseModel):
    flow_ids: List[str]
    # Deprecated: per-file view now returns exact file content; depth is ignored.
    depth: int = 3
    # "declared" (default): only triples written in the selected files.
    # "effective": selected files plus all transitively included flows.
    mode: str = "declared"


class FlowCompileBatchRequest(BaseModel):
    flow_ids: List[str]


class FlowPreviewRequest(BaseModel):
    content: str
    flow_id: str = "preview"
    collapse_includes: bool = False


class FlowPreviewResponse(BaseModel):
    valid: bool
    nodes: List[GraphNode] = []
    edges: List[GraphEdge] = []
    errors: List[str] = []
    warnings: List[str] = []


class FlowContentResponse(BaseModel):
    flow_id: str
    content: str


async def _scan_flow_files() -> List[dict]:
    """Return flow metadata from the manifest or by scanning YAML files."""
    if MANIFEST_FILE.exists():
        with MANIFEST_FILE.open("r", encoding="utf-8") as f:
            manifest = yaml.safe_load(f) or {}
        return manifest.get("files", [])

    files = []
    for path in sorted(FLOW_DIR.glob("*.yaml")):
        if path.name == "manifest.yaml":
            continue
        try:
            parsed = parse_flow_file(path)
            files.append(
                {
                    "product": parsed.flow_id,
                    "file": path.name,
                    "triples": len(parsed.triples),
                }
            )
        except FlowParseError:
            files.append({"product": path.stem, "file": path.name, "triples": 0})
    return files


async def _load_statuses(flow_ids: List[str]) -> dict:
    pool = await get_postgres_pool()
    if pool is None or not flow_ids:
        return {}
    rows = await pool.fetch(
        "SELECT flow_id, status, md5, compiled_at FROM arachne_flow_files WHERE flow_id = ANY($1)",
        flow_ids,
    )
    return {
        row["flow_id"]: {
            "status": row["status"],
            "md5": row["md5"],
            "compiled_at": row["compiled_at"].isoformat() if row["compiled_at"] else None,
        }
        for row in rows
    }


@router.get("", response_model=List[FlowListItem])
async def list_flows():
    """List all arachne-flow product files and their compile status."""
    files = await _scan_flow_files()
    statuses = await _load_statuses([f["product"] for f in files])

    result = []
    for item in files:
        flow_id = item["product"]
        status = statuses.get(flow_id, {})
        # Try to read the title from the file for non-manifest scans.
        title = flow_id
        file_path = FLOW_DIR / item["file"]
        if file_path.exists():
            try:
                with file_path.open("r", encoding="utf-8") as f:
                    doc = yaml.safe_load(f) or {}
                title = doc.get("title", flow_id)
            except Exception:
                pass
        result.append(
            FlowListItem(
                flow_id=flow_id,
                title=title,
                root_product=item.get("product", flow_id),
                file=item["file"],
                triples=item.get("triples", 0),
                status=status.get("status"),
                md5=status.get("md5"),
                compiled_at=status.get("compiled_at"),
            )
        )
    return result


@router.post("/{flow_id}/compile", response_model=FlowCompileResult)
async def compile_flow(flow_id: str):
    """Parse and compile a single flow file into the Neo4j flow graph."""
    file_path = FLOW_DIR / f"{flow_id}.yaml"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"flow file not found: {flow_id}")

    try:
        parsed = parse_flow_file(file_path)
    except FlowParseError as exc:
        raise HTTPException(status_code=400, detail=f"parse error: {exc}") from exc

    if parsed.flow_id != flow_id:
        raise HTTPException(
            status_code=400,
            detail=f"flow_id mismatch: file stem is {flow_id} but document says {parsed.flow_id}",
        )

    counts = await storage.compile_parsed_flow(parsed, clear_existing=True)
    return FlowCompileResult(
        flow_id=parsed.flow_id,
        resources=counts["resources"],
        actions=counts["actions"],
        methods=counts["methods"],
        edges=counts["edges"],
        dual=counts.get("dual", 0),
    )


@router.post("/subgraph", response_model=SubgraphResult)
async def get_flows_subgraph(request: FlowSubgraphRequest):
    """Return a subgraph for the selected flow files.

    ``mode="declared"`` (default): only the triples written in the selected
    files — "what you see is what the file declares".

    ``mode="effective"``: selected files plus all transitively included flows,
    so upstream chains through shared resources are preserved for tracing.
    """
    if not request.flow_ids:
        raise HTTPException(status_code=400, detail="flow_ids cannot be empty")

    for flow_id in request.flow_ids:
        file_path = FLOW_DIR / f"{flow_id}.yaml"
        if not file_path.exists():
            raise HTTPException(status_code=404, detail=f"flow file not found: {flow_id}")

    flow_ids = request.flow_ids
    if request.mode == "effective":
        flow_ids = _resolve_effective_flow_ids(request.flow_ids)

    nodes, edges = await storage.get_flow_file_graph(flow_ids)
    return SubgraphResult(
        center_node_id=request.flow_ids[0],
        depth=request.depth,
        nodes=nodes,
        edges=edges,
    )


_include_graph_cache: Optional[Dict[str, List[str]]] = None


def _get_include_graph() -> Dict[str, List[str]]:
    """Parse all flow files once to build the include dependency graph."""
    global _include_graph_cache
    if _include_graph_cache is not None:
        return _include_graph_cache
    graph: Dict[str, List[str]] = {}
    for path in sorted(FLOW_DIR.glob("*.yaml")):
        if path.name == "manifest.yaml":
            continue
        try:
            parsed = parse_flow_file(path)
            graph[parsed.flow_id] = [Path(name).stem for name in parsed.includes]
        except FlowParseError:
            graph[path.stem] = []
    _include_graph_cache = graph
    return graph


def _resolve_effective_flow_ids(flow_ids: List[str]) -> List[str]:
    """Expand selected flows to include all transitively included flows."""
    graph = _get_include_graph()
    seen: Set[str] = set()
    order: List[str] = []

    def visit(fid: str) -> None:
        if fid in seen:
            return
        seen.add(fid)
        order.append(fid)
        for dep in graph.get(fid, []):
            visit(dep)

    for fid in flow_ids:
        visit(fid)
    return order


@router.post("/preview", response_model=FlowPreviewResponse)
async def preview_flow(request: FlowPreviewRequest):
    """Parse and render arachne-flow YAML content without persisting.

    Returns the graph for the current document plus all transitively included
    files. On parse/validation errors, returns ``valid=false`` and the error
    list so the frontend can keep the last good graph.
    """
    nodes, edges, errors, warnings = await preview_flow_graph(
        request.content,
        flow_id=request.flow_id,
        collapse_includes=request.collapse_includes,
    )
    return FlowPreviewResponse(
        valid=len(errors) == 0,
        nodes=nodes,
        edges=edges,
        errors=errors,
        warnings=warnings,
    )


@router.get("/{flow_id}/content", response_model=FlowContentResponse)
async def get_flow_content(flow_id: str):
    """Return the raw YAML content of a flow file."""
    file_path = FLOW_DIR / f"{flow_id}.yaml"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"flow file not found: {flow_id}")
    return FlowContentResponse(flow_id=flow_id, content=file_path.read_text(encoding="utf-8"))


class MergedFlowGraphResult(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    merge_mode: str


@router.get("/graph", response_model=MergedFlowGraphResult)
async def get_flow_graph(merge: str = "method"):
    """Full flow graph for the no-selection view.

    ``merge=method`` (default) collapses cross-flow action occurrences with the
    same method into one action node and aggregates parallel edges (with
    ``flow_ids``/``count`` provenance), so the full graph reads as a clean
    shared backbone instead of per-flow duplication. ``merge=none`` returns the
    raw graph.
    """
    if merge == "none":
        nodes, _ = await storage.list_flow_nodes(skip=0, limit=10000)
        edges, _ = await storage.list_flow_edges(skip=0, limit=10000)
        return MergedFlowGraphResult(nodes=nodes, edges=edges, merge_mode="none")
    nodes, edges = await storage.get_merged_flow_graph()
    return MergedFlowGraphResult(nodes=nodes, edges=edges, merge_mode="method")


@router.post("/compile", response_model=List[FlowCompileResult])
async def compile_flows_batch(request: FlowCompileBatchRequest):
    """Parse and compile multiple flow files into the Neo4j flow graph."""
    if not request.flow_ids:
        raise HTTPException(status_code=400, detail="flow_ids cannot be empty")

    results: List[FlowCompileResult] = []
    for flow_id in request.flow_ids:
        file_path = FLOW_DIR / f"{flow_id}.yaml"
        if not file_path.exists():
            raise HTTPException(status_code=404, detail=f"flow file not found: {flow_id}")
        try:
            parsed = parse_flow_file(file_path)
        except FlowParseError as exc:
            raise HTTPException(status_code=400, detail=f"parse error in {flow_id}: {exc}") from exc

        if parsed.flow_id != flow_id:
            raise HTTPException(
                status_code=400,
                detail=f"flow_id mismatch: file stem is {flow_id} but document says {parsed.flow_id}",
            )

        counts = await storage.compile_parsed_flow(parsed, clear_existing=True)
        results.append(
            FlowCompileResult(
                flow_id=parsed.flow_id,
                resources=counts["resources"],
                actions=counts["actions"],
                methods=counts["methods"],
                edges=counts["edges"],
                dual=counts.get("dual", 0),
            )
        )
    return results
