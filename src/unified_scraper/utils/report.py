"""Report generation for crawler results.

Supports markdown, json, text, and HTML card layout
(inspired by wechat-group-report presentation).
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from .markdown import to_markdown
import re
import html

def _normalize(text: Optional[str]) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text.lower().strip())

def deduplicate(
    results: List[Dict[str, Any]],
    key: str = "title",
    threshold: float = 0.85,
) -> List[Dict[str, Any]]:
    """Remove near-duplicate items by title (or custom key)."""
    seen = []
    unique = []
    for item in results:
        val = _normalize(item.get(key, ""))
        if not val:
            unique.append(item)
            continue
        is_dup = False
        for s in seen:
            if val == s or (len(val) > 20 and (val in s or s in val)):
                is_dup = True
                break
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

def _group_by_category(results: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    groups: Dict[str, List] = {}
    for item in results:
        cat = item.get("category") or item.get("source") or "other"
        groups.setdefault(cat, []).append(item)
    return groups

def _html_escape(text: Any) -> str:
    return html.escape(str(text)) if text is not None else ""

def _render_html(
    results: List[Dict[str, Any]],
    title: str,
    timestamp: str,
    dedupe: bool,
) -> str:
    groups = _group_by_category(results)
    cards_html = []
    for cat, items in groups.items():
        cards = []
        for item in items:
            t = _html_escape(item.get("title", "Untitled"))
            src = _html_escape(item.get("source", ""))
            url = item.get("url", "")
            url_html = f'<a href="{_html_escape(url)}" target="_blank">查看原文</a>' if url else ""
            extra = []
            if item.get("published_at"):
                extra.append(f"时间：{_html_escape(item['published_at'])}")
            if item.get("engagement"):
                eng = item["engagement"]
                if isinstance(eng, dict):
                    extra.append(" · ".join(f"{k}: {v}" for k, v in eng.items() if v))
            meta = " · ".join(extra)
            cards.append(f'''
            <article class="card">
              <h3>{t}</h3>
              <p class="meta">{_html_escape(src)}{(" · " + meta) if meta else ""}</p>
              {f'<p class="source">{url_html}</p>' if url_html else ""}
            </article>''')
        section = f'''
        <section>
          <h2>{_html_escape(cat.upper())}</h2>
          {"".join(cards)}
        </section>'''
        cards_html.append(section)

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_html_escape(title)}</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
         background: #f6f7f9; color: #1a1a1a; margin: 0; padding: 24px; line-height: 1.5; }}
  .container {{ max-width: 800px; margin: 0 auto; }}
  h1 {{ font-size: 1.6rem; margin-bottom: 4px; }}
  .subtitle {{ color: #666; font-size: 0.9rem; margin-bottom: 24px; }}
  h2 {{ font-size: 1.15rem; margin: 28px 0 12px; color: #333; border-bottom: 1px solid #e5e5e5; padding-bottom: 6px; }}
  .card {{ background: #fff; border-radius: 10px; padding: 16px 18px; margin-bottom: 12px;
           box-shadow: 0 1px 3px rgba(0,0,0,0.06); }}
  .card h3 {{ margin: 0 0 6px; font-size: 1.05rem; }}
  .meta {{ color: #666; font-size: 0.85rem; margin: 0 0 6px; }}
  .source a {{ color: #0066cc; text-decoration: none; font-size: 0.85rem; }}
  .source a:hover {{ text-decoration: underline; }}
  footer {{ margin-top: 32px; color: #888; font-size: 0.8rem; }}
</style>
</head>
<body>
<div class="container">
  <h1>{_html_escape(title)}</h1>
  <p class="subtitle">生成时间：{timestamp} · 共 {len(results)} 条 · 去重：{"是" if dedupe else "否"}</p>
  {"".join(cards_html)}
  <footer>由 Unified Scraper 生成 · 数据仅供研究参考</footer>
</div>
</body>
</html>'''

def generate_report(
    results: List[Dict[str, Any]],
    title: str = "Crawler Report",
    format: str = "markdown",
    dedupe: bool = True,
    dedupe_key: str = "title",
) -> str:
    """Generate a report from crawler results.

    Supported formats: markdown, json, text, html
    Set dedupe=True to remove near-duplicate titles.
    """
    if dedupe:
        results = deduplicate(results, key=dedupe_key)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    if format == "html":
        return _render_html(results, title, timestamp, dedupe)

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
        header = f"{title}\nGenerated: {timestamp}\nItems: {len(results)}\n"
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
