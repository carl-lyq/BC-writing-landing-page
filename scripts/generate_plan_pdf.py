#!/usr/bin/env python3
"""Markdown → branded HTML → PDF (Chrome headless)."""

from __future__ import annotations

import base64
import mimetypes
import subprocess
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / "雅思写作学习提分方案.md"
OUT_PDF = ROOT / "雅思写作学习提分方案.pdf"
HTML_PATH = ROOT / "scripts" / ".plan-preview.html"

LOGO_LEFT = ROOT / "BC落地页交付开发/UI/assets/躺着学LOGO CHILLPREP.png"
LOGO_RIGHT = ROOT / "BC落地页交付开发/BC备考平台logo/Property 1=默认.png"
FONT_REGULAR = Path(__file__).resolve().parent / "fonts/NotoSansSC-400.woff2"
FONT_BOLD = Path(__file__).resolve().parent / "fonts/NotoSansSC-700.woff2"
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")


def img_data_uri(path: Path) -> str:
    mime, _ = mimetypes.guess_type(str(path))
    mime = mime or "image/png"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def build_html(body_html: str) -> str:
    left = img_data_uri(LOGO_LEFT)
    right = img_data_uri(LOGO_RIGHT)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <title>雅思写作学习提分方案</title>
  <style>
    @font-face {{
      font-family: "Plan CJK";
      src: url("fonts/NotoSansSC-400.woff2") format("woff2");
      font-weight: 400;
      font-style: normal;
    }}
    @font-face {{
      font-family: "Plan CJK";
      src: url("fonts/NotoSansSC-700.woff2") format("woff2");
      font-weight: 600 700;
      font-style: normal;
    }}
    @page {{
      size: A4;
      margin: 18mm 16mm 20mm;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      font-family: "Plan CJK", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      font-size: 11pt;
      line-height: 1.65;
      color: #0b1f3a;
      margin: 0;
      background: #fff;
    }}
    .doc-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding-bottom: 12px;
      margin-bottom: 8px;
      border-bottom: 2px solid #e7eef7;
    }}
    .doc-header img {{
      height: 34px;
      width: auto;
      object-fit: contain;
    }}
    .doc-header__right img {{
      height: 34px;
    }}
    .doc-subtitle {{
      margin: 0 0 20px;
      padding: 10px 14px;
      background: #f4f7fb;
      border-left: 4px solid #1e5fd6;
      border-radius: 0 8px 8px 0;
      font-size: 10pt;
      color: #3d5470;
    }}
    h1 {{
      font-size: 22pt;
      font-weight: 700;
      margin: 0 0 10px;
      color: #0b1f3a;
      letter-spacing: 0.02em;
    }}
    h2 {{
      font-size: 14pt;
      margin: 22px 0 10px;
      padding-bottom: 6px;
      border-bottom: 1px solid #d5e0ef;
      color: #153f99;
    }}
    h3 {{
      font-size: 12pt;
      margin: 16px 0 8px;
      color: #0b1f3a;
    }}
    p {{ margin: 8px 0; }}
    ul, ol {{ margin: 8px 0 12px; padding-left: 1.4em; }}
    li {{ margin: 4px 0; }}
    li::marker {{ color: #1e5fd6; }}
    hr {{
      border: none;
      border-top: 1px solid #e7eef7;
      margin: 18px 0;
    }}
    blockquote {{
      margin: 12px 0;
      padding: 10px 14px;
      background: #f4f7fb;
      border-left: 4px solid #1e5fd6;
      border-radius: 0 8px 8px 0;
      color: #153f99;
    }}
    code {{
      font-family: "JetBrains Mono", "SF Mono", Menlo, monospace;
      font-size: 0.92em;
      background: #eef3fa;
      padding: 0.1em 0.35em;
      border-radius: 4px;
    }}
    strong {{ color: #0b1f3a; }}
    .doc-footer {{
      margin-top: 28px;
      padding-top: 10px;
      border-top: 1px solid #e7eef7;
      font-size: 9pt;
      color: #6b7f99;
      text-align: center;
    }}
  </style>
</head>
<body>
  <header class="doc-header">
    <div class="doc-header__left"><img src="{left}" alt="躺着学" /></div>
    <div class="doc-header__right"><img src="{right}" alt="BC备考平台" /></div>
  </header>
  <main class="doc-body">
{body_html}
  </main>
  <footer class="doc-footer">躺着学 × BC备考平台 · 雅思写作学习方案</footer>
</body>
</html>"""


def md_to_html(md_text: str) -> str:
    return markdown.markdown(
        md_text,
        extensions=["extra", "nl2br", "sane_lists"],
    )


def print_pdf(html_path: Path, pdf_path: Path) -> None:
    if not CHROME.exists():
        raise SystemExit(f"Chrome not found at {CHROME}")
    cmd = [
        str(CHROME),
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--allow-file-access-from-files",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=10000",
        f"--print-to-pdf={pdf_path.resolve()}",
        html_path.resolve().as_uri(),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        raise SystemExit(
            f"Chrome PDF failed (code {result.returncode}):\n{result.stderr}"
        )


def main() -> None:
    if not MD_PATH.exists():
        raise SystemExit(f"Missing markdown: {MD_PATH}")
    for p in (LOGO_LEFT, LOGO_RIGHT, FONT_REGULAR, FONT_BOLD):
        if not p.exists():
            raise SystemExit(f"Missing asset: {p}")

    md_text = MD_PATH.read_text(encoding="utf-8")
    body = md_to_html(md_text)
    html = build_html(body)
    HTML_PATH.parent.mkdir(parents=True, exist_ok=True)
    HTML_PATH.write_text(html, encoding="utf-8")
    print_pdf(HTML_PATH, OUT_PDF)
    print(f"PDF written: {OUT_PDF}")
    print(f"HTML preview: {HTML_PATH}")


if __name__ == "__main__":
    main()
