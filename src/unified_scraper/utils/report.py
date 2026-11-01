"""Report generation for crawler results."""

from typing import List, Dict, Any
from datetime import datetime
from .markdown import to_markdown

def generate_report(
    results: List[Dict[str, Any]],
    title: str = "Crawler Report",
    format: str = "markdown",
) -> str:
    """Generate a report from crawler results.

    Supported formats: markdown, json, text
    """
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    header = f"{title}\nGenerated: {timestamp}\nItems: {len(results)}\n"

    if format == "json":
        import json
        return json.dumps({"title": title, "generated": timestamp, "count": len(results), "items": results}, ensure_ascii=False, indent=2)

    if format == "text":
        lines = [header, "=" * 40]
        for i, item in enumerate(results, 1):
            lines.append(f"\n[{i}]")
            for k, v in item.items():
                if v is not None:
                    lines.append(f"  {k}: {v}")
        return "\n".join(lines)

    # default markdown
    md = f"# {title}\n\n**Generated**: {timestamp}  \n**Items**: {len(results)}\n\n"
    md += to_markdown(results, title="Details")
    return md
