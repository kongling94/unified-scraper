"""Simple Markdown export helpers."""

from typing import List, Dict, Any

def to_markdown(items: List[Dict[str, Any]], title: str = "Results") -> str:
    """Convert a list of dicts to Markdown."""
    lines = [f"# {title}", ""]
    for i, item in enumerate(items, 1):
        lines.append(f"## Item {i}")
        for k, v in item.items():
            if v is not None:
                lines.append(f"- **{k}**: {v}")
        lines.append("")
    return "\n".join(lines)

def quotes_to_markdown(quotes: List[str], title: str = "Quotes") -> str:
    lines = [f"# {title}", ""]
    for q in quotes:
        lines.append(f"> {q}")
        lines.append("")
    return "\n".join(lines)
