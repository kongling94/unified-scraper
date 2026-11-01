"""Report generation for crawler results.

Supports markdown, json, text, html, and png.
Features: dedupe, structured sections, custom sections, auto-save.
"""

from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from pathlib import Path
from .markdown import to_markdown
import re
import html
import io
import os

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

def _default_structured_sections(results: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Default fixed sections."""
    sections = {
        "热点摘要": [],
        "待关注": [],
        "已结论": [],
        "其他": [],
    }
    ai_tech_keys = ["ai", "arxiv", "github", "tech", "mit", "verge", "wired", "ars", "venture", "hacker"]
    finance_keys = ["finance", "coin", "reuters", "cnbc", "yahoo", "seeking", "telegraph"]
    video_keys = ["youtube", "bilibili", "video"]

    for item in results:
        cat = (item.get("category") or "").lower()
        src = (item.get("source") or "").lower()
        text = f"{cat} {src}"

        if any(k in text for k in ai_tech_keys) or any(k in text for k in video_keys):
            sections["热点摘要"].append(item)
        elif any(k in text for k in finance_keys):
            sections["待关注"].append(item)
        else:
            sections["其他"].append(item)

    return {k: v for k, v in sections.items() if v}

def apply_custom_sections(
    results: List[Dict[str, Any]],
    section_rules: Dict[str, List[str]],
) -> Dict[str, List[Dict[str, Any]]]:
    """Group items by custom section rules.

    section_rules example:
    {
      "AI 热点": ["ai", "arxiv", "github"],
      "金融动态": ["finance", "coin", "reuters"],
      "视频趋势": ["youtube", "bilibili"]
    }
    An item is placed in the first matching section; unmatched go to "其他".
    """
    sections: Dict[str, List] = {name: [] for name in section_rules}
    sections["其他"] = []

    for item in results:
        cat = (item.get("category") or "").lower()
        src = (item.get("source") or "").lower()
        text = f"{cat} {src}"
        placed = False
        for sec_name, keywords in section_rules.items():
            if any(k.lower() in text for k in keywords):
                sections[sec_name].append(item)
                placed = True
                break
        if not placed:
            sections["其他"].append(item)

    return {k: v for k, v in sections.items() if v}

def _html_escape(text: Any) -> str:
    return html.escape(str(text)) if text is not None else ""

def _render_html(
    results: List[Dict[str, Any]],
    title: str,
    timestamp: str,
    dedupe: bool,
    groups: Optional[Dict[str, List]] = None,
) -> str:
    if groups is None:
        groups = {}
        for item in results:
            cat = item.get("category") or item.get("source") or "other"
            groups.setdefault(cat, []).append(item)

    cards_html = []
    default_colors = {"热点摘要": "#fff", "待关注": "#fff8e6", "已结论": "#f0fff4", "其他": "#fff"}
    for cat, items in groups.items():
        bg = default_colors.get(cat, "#fff")
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
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        raise RuntimeError("PNG export requires Pillow. Install with: pip install pillow")

    width = 800
    padding = 24
    card_pad = 12
    height = 120 + len(results[:50]) * 70
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

def _auto_save(content: Union[str, bytes], title: str, fmt: str, output_dir: str = "reports") -> str:
    """Save report to disk and return the file path."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    safe_title = re.sub(r"[^\w\u4e00-\u9fff-]", "_", title)[:40]
    ext = {"html": "html", "markdown": "md", "json": "json", "text": "txt", "png": "png"}.get(fmt, "txt")
    filename = f"{ts}_{safe_title}.{ext}"
    path = os.path.join(output_dir, filename)

    mode = "wb" if isinstance(content, bytes) else "w"
    encoding = None if isinstance(content, bytes) else "utf-8"
    with open(path, mode, encoding=encoding) as f:
        f.write(content)
    return path

def generate_report(
    results: List[Dict[str, Any]],
    title: str = "Crawler Report",
    format: str = "markdown",
    dedupe: bool = True,
    dedupe_key: str = "title",
    structured: bool = False,
    custom_sections: Optional[Dict[str, List[str]]] = None,
    auto_save: bool = False,
    output_dir: str = "reports",
) -> Union[str, bytes, Dict[str, Any]]:
    """Generate a report from crawler results.

    Supported formats: markdown, json, text, html, png
    custom_sections: dict of section_name -> list of keywords
    auto_save: if True, also write to disk and return dict with path
    """
    if dedupe:
        results = deduplicate(results, key=dedupe_key)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    groups = None
    if custom_sections:
        groups = apply_custom_sections(results, custom_sections)
    elif structured:
        groups = _default_structured_sections(results)

    if format == "png":
        content = _render_png(results, title, timestamp)
    elif format == "html":
        content = _render_html(results, title, timestamp, dedupe, groups=groups)
    elif format == "json":
        import json
        content = json.dumps({
            "title": title,
            "generated": timestamp,
            "count": len(results),
            "deduped": dedupe,
            "items": results,
        }, ensure_ascii=False, indent=2)
    elif format == "text":
        header = f"{title}\nGenerated: {timestamp}\nItems: {len(results)}\n"
        lines = [header, "=" * 40]
        for i, item in enumerate(results, 1):
            lines.append(f"\n[{i}]")
            for k, v in item.items():
                if v is not None:
                    lines.append(f"  {k}: {v}")
        content = "\n".join(lines)
    else:
        # markdown
        md = f"# {title}\n\n**Generated**: {timestamp}  \n**Items**: {len(results)}  \n**Deduped**: {dedupe}\n\n"
        if groups:
            for sec, items in groups.items():
                md += f"## {sec}\n\n"
                md += to_markdown(items, title="")
                md += "\n"
        else:
            md += to_markdown(results, title="Details")
        content = md

    if auto_save:
        path = _auto_save(content, title, format, output_dir)
        return {"content": content, "saved_path": path, "format": format}

    return content
