"""Report generation for crawler results.

Supports markdown, json, text, html, and png.
Inspired by wechat-group-report card layout.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from .markdown import to_markdown
import re
import html
import io

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

def _structured_sections(results: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group into fixed research-friendly sections."""
    sections = {
        "热点摘要": [],
        "待关注": [],
        "已结论": [],
        "其他": [],
    }
    for item in results:
        cat = (item.get("category") or "").lower()
        src = (item.get("source") or "").lower()
        if any(k in cat or k in src for k in ["ai", "arxiv", "github", "tech", "mit"]):
            sections["热点摘要"].append(item)
        elif any(k in cat or k in src for k in ["finance", "coin", "reuters", "cnbc", "yahoo"]):
            sections["待关注"].append(item)
        else:
            sections["其他"].append(item)
    # Move high-engagement to 已结论 if present
    return {k: v for k, v in sections.items() if v}

def _html_escape(text: Any) -> str:
    return html.escape(str(text)) if text is not None else ""

def _render_html(
    results: List[Dict[str, Any]],
    title: str,
    timestamp: str,
    dedupe: bool,
    structured: bool = False,
) -> str:
    if structured:
        groups = _structured_sections(results)
    else:
        groups = {}
        for item in results:
            cat = item.get("category") or item.get("source") or "other"
            groups.setdefault(cat, []).append(item)

    cards_html = []
    colors = {"热点摘要": "#fff", "待关注": "#fff8e6", "已结论": "#f0fff4", "其他": "#fff"}
    for cat, items in groups.items():
        bg = colors.get(cat, "#fff")
        cards = []
        for item in items:
            t = _html_escape(item.get("title", "Untitled"))
            src = _html_escape(item.get("source", ""))
            url = item.get("url", "")
            url_html = f'<a href="{_html_escape(url)}" target="_blank">查看原文</a>' if url else ""
            cards.append(f'''
            <article class="card" style="background:{bg}">
              <h3>{t}</h3>
              <p class="meta">{src}</p>
              {f'<p class="source">{url_html}</p>' if url_html else ""}
            </article>''')
        section = f'''
        <section>
          <h2>{_html_escape(cat)}</h2>
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
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
         background: #f6f7f9; color: #1a1a1a; margin: 0; padding: 24px; line-height: 1.5; }}
  .container {{ max-width: 800px; margin: 0 auto; }}
  h1 {{ font-size: 1.6rem; margin-bottom: 4px; }}
  .subtitle {{ color: #666; font-size: 0.9rem; margin-bottom: 24px; }}
  h2 {{ font-size: 1.15rem; margin: 28px 0 12px; color: #333; border-bottom: 1px solid #e5e5e5; padding-bottom: 6px; }}
  .card {{ border-radius: 10px; padding: 16px 18px; margin-bottom: 12px;
           box-shadow: 0 1px 3px rgba(0,0,0,0.06); }}
  .card h3 {{ margin: 0 0 6px; font-size: 1.05rem; }}
  .meta {{ color: #666; font-size: 0.85rem; margin: 0 0 6px; }}
  .source a {{ color: #0066cc; text-decoration: none; font-size: 0.85rem; }}
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

def _render_png(results: List[Dict[str, Any]], title: str, timestamp: str) -> bytes:
    """Render a simple long PNG using Pillow. Returns PNG bytes."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        raise RuntimeError("PNG export requires Pillow. Install with: pip install pillow")

    width = 800
    padding = 24
    line_height = 22
    card_pad = 12

    # Estimate height
    height = 120
    for item in results[:50]:
        height += 70
    height = max(height, 400)

    img = Image.new("RGB", (width, height), "#f6f7f9")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 16)
        font_bold = ImageFont.truetype("arial.ttf", 18)
        font_small = ImageFont.truetype("arial.ttf", 13)
    except Exception:
        font = ImageFont.load_default()
        font_bold = font
        font_small = font

    y = padding
    draw.text((padding, y), title, fill="#1a1a1a", font=font_bold)
    y += 30
    draw.text((padding, y), f"{timestamp} · {len(results)} items", fill="#666", font=font_small)
    y += 40

    for item in results[:40]:
        # card background
        draw.rectangle([padding, y, width - padding, y + 60], fill="#ffffff", outline="#e5e5e5")
        title_text = (item.get("title") or "")[:80]
        src = item.get("source") or ""
        draw.text((padding + card_pad, y + 8), title_text, fill="#1a1a1a", font=font)
        draw.text((padding + card_pad, y + 32), src, fill="#666", font=font_small)
        y += 70
        if y > height - 40:
            break

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def generate_report(
    results: List[Dict[str, Any]],
    title: str = "Crawler Report",
    format: str = "markdown",
    dedupe: bool = True,
    dedupe_key: str = "title",
    structured: bool = False,
) -> str | bytes:
    """Generate a report from crawler results.

    Supported formats: markdown, json, text, html, png
    structured=True uses fixed sections: 热点摘要 / 待关注 / 已结论
    PNG returns bytes; others return str.
    """
    if dedupe:
        results = deduplicate(results, key=dedupe_key)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    if format == "png":
        return _render_png(results, title, timestamp)

    if format == "html":
        return _render_html(results, title, timestamp, dedupe, structured=structured)

    if format == "json":
        import json
        return json.dumps({
            "title": title,
            "generated": timestamp,
            "count": len(results),
            "deduped": dedupe,
            "structured": structured,
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
    if structured:
        sections = _structured_sections(results)
        for sec, items in sections.items():
            md += f"## {sec}\n\n"
            md += to_markdown(items, title="")
            md += "\n"
    else:
        md += to_markdown(results, title="Details")
    return md
