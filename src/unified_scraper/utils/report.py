"""Report generation for crawler results."""

from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
from .markdown import to_markdown
import re

def _normalize(text: Optional[str]) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text.lower().strip())

def deduplicate(
    results: List[Dict[str, Any]],
    key: str = "title",
    threshold: float = 0.85,
) -> List[Dict[str, Any]]:
    """Remove near-duplicate items by title (or custom key).

    Uses simple normalized string matching + length similarity.
    """
    seen = []
    unique = []
    for item in results:
        val = _normalize(item.get(key, ""))
        if not val:
            unique.append(item)
            continue
        is_dup = False
        for s in seen:
            # exact or high overlap
            if val == s or (len(val) > 20 and (val in s or s in val)):
                is_dup = True
                break
            # simple Jaccard-like on words
            words_a = set(val.split())
            words_b = set(s.split())
            if words_a and words_b:
                inter = len(words_a & words_b)
                union = len(words_a | words_b)
                if union and inter / union >= threshold:
                    is_dup = True
                    break
        if not is_dup:
            seen.append(val)
            unique.append(item)
    return unique

def generate_report(
    results: List[Dict[str, Any]],
    title: str = "Crawler Report",
    format: str = "markdown",
    dedupe: bool = True,
    dedupe_key: str = "title",
) -> str:
    """Generate a report from crawler results.

    Supported formats: markdown, json, text
    Set dedupe=True to remove near-duplicate titles.
    """
    if dedupe:
        results = deduplicate(results, key=dedupe_key)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    header = f"{title}\nGenerated: {timestamp}\nItems: {len(results)}\n"

    if format == "json":
        import json
        return json.dumps({
            "title": title,
            "generated": timestamp,
            "count": len(results),
            "deduped": dedupe,
            "items": results,
        }, ensure_ascii=False, indent=2)

    if format == "text":
        lines = [header, "=" * 40]
        for i, item in enumerate(results, 1):
            lines.append(f"\n[{i}]")
            for k, v in item.items():
                if v is not None:
                    lines.append(f"  {k}: {v}")
        return "\n".join(lines)

    # default markdown
    md = f"# {title}\n\n**Generated**: {timestamp}  \n**Items**: {len(results)}  \n**Deduped**: {dedupe}\n\n"
    md += to_markdown(results, title="Details")
    return md
