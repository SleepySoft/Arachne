"""Lightweight fuzzy node search without vector DB.

Approach:
- No external dependencies (pure Python stdlib).
- Combines substring containment, character bigram Jaccard, and
  Levenshtein-like similarity via difflib.SequenceMatcher.
- Works for both Chinese and English; Chinese is handled at the
  character level because word segmentation is not required for
  short technical terms.
"""

from difflib import SequenceMatcher
from typing import List, Optional

from app.models.schemas import IndustrialNode
from app.services import neo4j_storage


def _normalize(text: Optional[str]) -> str:
    if not text:
        return ""
    return text.lower().strip().replace(" ", "").replace("\u3000", "")


def _char_ngrams(text: str, n: int = 2) -> set[str]:
    if len(text) < n:
        return {text} if text else set()
    return {text[i : i + n] for i in range(len(text) - n + 1)}


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union)


def _levenshtein_ratio(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def _score_field(query: str, field: str) -> float:
    """Return similarity score between query and a single field."""
    if not query or not field:
        return 0.0

    if query == field:
        return 1.0

    # Substring match bonus, scaled by query length relative to field length
    # so short queries matching long fields don't dominate.
    if query in field:
        ratio = len(query) / len(field)
        return min(0.95, 0.55 + 0.45 * ratio)
    if field in query:
        return 0.9

    # Token / alias partial overlap (comma/space separated)
    q_tokens = set(query.replace(",", " ").split())
    f_tokens = set(field.replace(",", " ").split())
    if q_tokens and f_tokens and (q_tokens & f_tokens):
        overlap = len(q_tokens & f_tokens) / max(len(q_tokens), len(f_tokens))
        return max(0.7, overlap * 0.9)

    lev = _levenshtein_ratio(query, field)
    ngram = _jaccard(_char_ngrams(query, 2), _char_ngrams(field, 2))

    # Combined score; ngram helps with Chinese, Levenshtein helps with typos
    combined = max(lev, ngram)
    return combined * 0.85


def _score_node(query: str, node: IndustrialNode) -> float:
    """Return the best similarity score across all node name fields."""
    fields = [
        _normalize(node.canonical_name_zh),
        _normalize(node.canonical_name_en),
        *[_normalize(a) for a in (node.aliases or [])],
    ]
    return max((_score_field(query, f) for f in fields if f), default=0.0)


async def fuzzy_search_nodes(
    query: str,
    limit: int = 10,
    score_threshold: float = 0.4,
    max_candidates: int = 1000,
) -> List[dict]:
    """Search nodes by fuzzy similarity.

    1. Pull candidates via Neo4j substring search (fast).
    2. If too few candidates, broaden by fetching active nodes.
    3. Score candidates using combined text similarity.
    4. Return top results above the threshold.
    """
    q = _normalize(query)
    if len(q) < 2:
        return []

    # Step 1: substring candidates (usually the most relevant)
    candidates, _ = await neo4j_storage.list_nodes(
        skip=0,
        limit=max_candidates,
        search=query,
    )

    # Step 2: broaden the pool if we got very few hits
    if len(candidates) < 50:
        broad, _ = await neo4j_storage.list_nodes(
            skip=0,
            limit=max_candidates,
            status="ACTIVE",
        )
        seen = {n.node_id for n in candidates}
        candidates.extend([n for n in broad if n.node_id not in seen])

    # Step 3: score and rank
    scored = []
    for node in candidates:
        score = _score_node(q, node)
        if score >= score_threshold:
            scored.append({"node": node, "score": score})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:limit]
