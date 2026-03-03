#!/usr/bin/env python3
"""
markdown-to-wechat converter
Converts Markdown files to WeChat Official Account HTML with configurable YAML styles.

Usage:
    # Single file
    python convert.py --input article.md

    # Single file with custom style
    python convert.py --input article.md --style my-style.yaml

    # Batch convert directory
    python convert.py --input "Oracle view/"

    # Upload images to Aliyun OSS
    python convert.py --input article.md --upload-images \
        --oss-access-key-id KEY --oss-access-key-secret SECRET \
        --oss-bucket s2-img --oss-endpoint oss-cn-shanghai.aliyuncs.com
"""

import argparse
import configparser
import os
import re
import sys
from pathlib import Path
from typing import Optional

import yaml

try:
    import mistune
except ImportError:
    print("ERROR: mistune not installed. Run: pip install mistune>=3.0.0")
    sys.exit(1)


# ─────────────────────────────────────────────
# Style loading
# ─────────────────────────────────────────────

DEFAULT_STYLE_PATH = Path(__file__).parent.parent / "config.yaml"


def load_style(style_path: Optional[str] = None) -> dict:
    """
    Load style config. Merge user config over default config.
    """
    with open(DEFAULT_STYLE_PATH, "r", encoding="utf-8") as f:
        style = yaml.safe_load(f)

    if style_path:
        override_path = Path(style_path)
        if override_path.exists():
            with open(override_path, "r", encoding="utf-8") as f:
                override = yaml.safe_load(f) or {}
            # Deep merge top-level keys
            for key, value in override.items():
                if isinstance(value, dict) and key in style:
                    style[key].update(value)
                else:
                    style[key] = value
        else:
            print(f"[WARNING] Style file not found: {style_path}, using defaults")

    return style


def _css(props: dict) -> str:
    """Convert a dict of CSS properties to an inline style string."""
    if not props:
        return ""

    parts = []
    for k, v in props.items():
        css_key = k.replace("_", "-")
        parts.append(f"{css_key}: {v}")
    return "; ".join(parts)


def post_process_html(html: str) -> str:
    """
    Perform final cleanup on generated HTML.
    Specifically: remove color styles from tags nested inside <thead> to ensure
    header text visibility against dark backgrounds.
    """
    def clean_header_colors(match):
        thead_content = match.group(0)
        # Remove color related styles from nested tags like <strong style="...">
        # We look for color: #[0-9a-fA-F]{3,6} or color: rgb(...)
        cleaned = re.sub(r'color:\s*#[0-9a-fA-F]{3,6};?\s*', '', thead_content)
        cleaned = re.sub(r'color:\s*rgb\([^)]+\);?\s*', '', cleaned)
        return cleaned

    # Find <thead>...</thead> blocks
    return re.sub(r'<thead>.*?</thead>', clean_header_colors, html, flags=re.DOTALL)


# ─────────────────────────────────────────────
# Custom Mistune renderer
# ─────────────────────────────────────────────

class WeChatRenderer(mistune.HTMLRenderer):
    """Renders Markdown to WeChat-compatible inline-styled HTML."""

    def __init__(self, style: dict):
        super().__init__(escape=False)
        self.s = style

    def heading(self, text, level, **attrs):
        tag = f"h{level}"
        props = self.s.get("headings", {}).get(tag, {})
        css = _css(props) if props else ""
        return f'<{tag} style="{css}">{text}</{tag}>\n'

    def paragraph(self, text):
        props = self.s.get("paragraph", {})
        css = _css(props) if props else ""
        return f'<p style="{css}">{text}</p>\n'

    def strong(self, text):
        props = self.s.get("strong", {})
        # Ensure color is always applied
        if "color" not in props:
            props["color"] = "#e67e22" 
        css = _css(props)
        return f'<strong style="{css}">{text}</strong>'

    def emphasis(self, text):
        props = self.s.get("em", {})
        if "color" not in props:
            props["color"] = "#16a085" 
        css = _css(props)
        return f'<em style="{css}">{text}</em>'

    def codespan(self, code):
        props = self.s.get("code_inline", {})
        css = _css(props) if props else ""
        return f'<code style="{css}">{code}</code>'

    def block_code(self, code, **attrs):
        info = attrs.get("info", "") or ""
        lang = info.split()[0] if info else ""
        props = dict(self.s.get("code_block", {}))
        
        # Determine background color - check both shorthand and longhand
        bg_color = props.get("background") or props.get("background-color") or "#282c34"
        border = props.get("border", "")
        text_color = props.get("color", "#abb2bf")
        
        # 1. Container for the whole "window"
        # WeChat strips divs, but preserves sections better.
        # Adding display: block and background-color redundantly.
        container_css = (
            f"margin: 18px 0; border-radius: 8px; overflow: hidden; "
            f"background-color: {bg_color}; display: block !important;"
        )
        if border:
            container_css += f" border: {border};"
        
        # 2. Decoration bar - Avoid display: flex as WeChat often strips it.
        # Use white-space: nowrap and vertical-align for compatibility.
        dot_bar_css = (
            f"display: block; height: 32px; padding: 0 14px; "
            f"line-height: 32px; background-color: {bg_color}; "
            f"white-space: nowrap; margin: 0; border: none;"
        )
        dot_style = 'display: inline-block; width: 12px; height: 12px; border-radius: 50%; vertical-align: middle; margin-right: 7px;'
        dot_red    = f'{dot_style} background-color: #ff5f57;'
        dot_yellow = f'{dot_style} background-color: #febc2e;'
        dot_green  = f'{dot_style} background-color: #28c840;'
        
        # Language label shown to the right of dots
        lang_label_html = ""
        if lang:
            lang_label_css = (
                f"display: inline-block; vertical-align: middle; font-size: 12px; "
                f"color: {text_color}; opacity: 0.6; font-family: Consolas, Monaco, monospace; "
                f"letter-spacing: 0.05em;"
            )
            lang_label_html = f'<span style="{lang_label_css}">{lang.upper()}</span>'
        
        # 3. Clean up pre tag properties
        # Redundantly apply background to pre/code in case container is stripped
        props["margin"] = "0"
        props["border"] = "none"
        props["border-radius"] = "0"
        props["background-color"] = bg_color
        props["padding-top"] = "0"
        props["display"] = "block"
        
        css = _css(props)
        lang_attr = f' class="language-{lang}"' if lang else ""
        
        return (
            f'<section style="{container_css}">'
            f'<section style="{dot_bar_css}">'
            f'<span style="{dot_red}"></span>'
            f'<span style="{dot_yellow}"></span>'
            f'<span style="{dot_green}"></span>'
            f'{lang_label_html}'
            f'</section>'
            f'<pre style="{css}"><code{lang_attr} style="background-color: {bg_color}; display: block;">{code}</code></pre>'
            f'</section>\n'
        )


    def block_quote(self, text):
        props = self.s.get("blockquote", {})
        css = _css(props) if props else ""
        return f'<blockquote style="{css}">{text}</blockquote>\n'

    def list(self, text, ordered, **attrs):
        tag = "ol" if ordered else "ul"
        lprops = dict(self.s.get("list", {}))
        # Remove non-CSS configuration keys
        lprops.pop("item_margin", None)
        lprops.pop("section", None)
        css = _css(lprops) if lprops else ""
        return f'<{tag} style="{css}">{text}</{tag}>\n'

    def list_item(self, text, **attrs):
        item_margin = self.s.get("list", {}).get("item_margin", "8px 0")
        
        # WeChat fix: The editor normalizes naked inline text + block elements 
        # (like <ul>) inside <li> into separate <p> tags, breaking trailing colons.
        # Solution: Wrap the leading inline text in a <section> manually.
        import re
        
        # 1. Normalize <p> to <section> with margin:0 to avoid WeChat line heights
        text = re.sub(r'<p([^>]*)>', r'<section\1 style="margin: 0; padding: 0;">', text)
        text = re.sub(r'</p>', r'</section>', text)

        # 2. Split leading inline text from the first block-level element.
        match = re.search(r'(.*?)(<(?:ul|ol|table|blockquote|pre|section)\b.*)', text, flags=re.DOTALL | re.IGNORECASE)
        
        if match:
            inline_part = match.group(1).strip()
            block_part = match.group(2)
            
            # If the inline part isn't explicitly wrapped, wrap it.
            if inline_part:
                inline_part = f'<section style="margin: 0; padding: 0; color: inherit;">{inline_part}</section>\n'
                
            clean_text = inline_part + block_part
        else:
            # No nested blocks. It's just a leaf tight list item.
            inline_part = text.strip()
            if inline_part and not inline_part.startswith('<section'):
                clean_text = f'<section style="margin: 0; padding: 0; color: inherit;">{inline_part}</section>\n'
            else:
                clean_text = text.strip()
        
        # Apply style properties to the li tag
        lprops = dict(self.s.get("list", {}))
        lprops.pop("item_margin", None)
        lprops.pop("section", None)
        # Ensure we don't have conflicting margins
        lprops.pop("margin", None)
        lprops.pop("padding-left", None)
        lprops.pop("padding_left", None)
        
        li_css = _css(lprops)
        li_style = f"margin: {item_margin};"
        if li_css:
            li_style += f" {li_css}"

        return f'<li style="{li_style}">{clean_text}</li>\n'

    def link(self, text, url, title=None):
        props = self.s.get("link", {})
        css = _css(props) if props else ""
        title_attr = f' title="{title}"' if title else ""
        return f'<a href="{url}"{title_attr} style="{css}">{text}</a>'

    def image(self, text, url, title=None):
        props = dict(self.s.get("image", {}))
        # Remove non-CSS config keys
        props.pop("upload_to_oss", None)
        props.pop("oss_dir", None)
        css = _css(props)
        alt = text or ""
        title_attr = f' title="{title}"' if title else ""
        return (
            f'<div style="text-align: center;">'
            f'<img src="{url}" alt="{alt}"{title_attr} style="{css}">'
            f'</div>\n'
        )

    def thematic_break(self):
        props = self.s.get("hr", {})
        css = _css(props) if props else "border: none; border-top: 1px solid #bdc3c7; margin: 24px 0"
        return f'<hr style="{css}">\n'

    def table(self, text):
        props = dict(self.s.get("table", {}))
        # Remove all possible non-standard style configuration keys
        border = props.pop("border", "1px solid #d5d8dc")
        font_size = props.pop("font_size", "14px")
        non_css_keys = [
            "header_bg", "header_color", "header_padding", 
            "cell_padding", "cell_border", "cell_color", 
            "alternate_row_bg"
        ]
        for key in non_css_keys:
            props.pop(key, None)

        # Default table styles
        props.setdefault("margin", "18px 0")
        props.setdefault("width", "100%")
        props.setdefault("border-collapse", "collapse")
        props.setdefault("font-size", font_size)

        css = _css(props)
        return (
            f'<table style="border: {border}; {css}">{text}</table>\n'
        )

    def table_head(self, text):
        return f'<thead>{text}</thead>\n'

    def table_body(self, text):
        return f'<tbody>{text}</tbody>\n'

    def table_row(self, text):
        return f'<tr>{text}</tr>\n'

    def table_cell(self, text, align=None, is_head=False, **attrs):
        # mistune 3.x may pass 'head' instead of 'is_head'
        is_head = is_head or attrs.get("head", False)
        props = self.s.get("table", {})
        if is_head:
            bg = props.get("header_bg", "#16a085")
            color = props.get("header_color", "#ffffff") # Explicit header text color
            padding = props.get("header_padding", "10px")
            border = props.get("border", "1px solid #d5d8dc")
            # Default to style alignment if provided
            style_align = props.get("text_align", "left")
            cell_align = align if align else style_align
            
            css = (
                f"padding: {padding}; text-align: {cell_align}; "
                f"border: {border}; font-weight: bold; "
                f"background: {bg}; color: {color};"
            )
            tag = "th"
        else:
            padding = props.get("cell_padding", "10px")
            cell_border = props.get("cell_border", "1px solid #d5d8dc")
            cell_color = props.get("cell_color", "#333333") # Explicit cell text color
            
            # Default to style alignment if provided
            style_align = props.get("text_align", "left")
            cell_align = align if align else style_align
            
            css = f"padding: {padding}; border: {cell_border}; color: {cell_color}; text-align: {cell_align};"
            tag = "td"
        align_attr = f' align="{align}"' if align else ""
        return f'<{tag} style="{css}"{align_attr}>{text}</{tag}>\n'


# ─────────────────────────────────────────────
# HTML wrapper
# ─────────────────────────────────────────────

def wrap_html(body: str, style: dict, title: str = "") -> str:
    """Wrap converted body in a complete HTML document."""
    c = style.get("container", {})
    max_width = c.get("max_width", "677px")
    font_size = c.get("font_size", "15px")
    line_height = c.get("line_height", "1.8")
    color = c.get("color", "#2c3e50")
    font_family = c.get("font_family",
        "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif")
    padding = c.get("padding", "0 20px")
    margin = c.get("margin", "20px auto")

    container_css = (
        f"margin: {margin}; padding: {padding}; max-width: {max_width}; "
        f"font-size: {font_size}; color: {color}; line-height: {line_height}; "
        f"font-family: {font_family};"
    )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
</head>
<body>
<section style="{container_css}">
{body}
</section>
</body>
</html>
"""


# ─────────────────────────────────────────────
# Main conversion logic
# ─────────────────────────────────────────────

def convert_file(
    input_path: str,
    style: dict,
    output_dir: Optional[str] = None,
    upload_images: bool = False,
    oss_kwargs: Optional[dict] = None,
) -> dict:
    """
    Convert a single Markdown file to WeChat-ready HTML.

    Returns:
        dict with keys:
          - output_path (str): path to the generated HTML file
          - oss_stats (dict | None): image upload stats if OSS was used
    """
    input_path = Path(input_path).resolve()
    article_dir = input_path.parent

    # Ensure standard directories exist in the article's path
    (article_dir / "img").mkdir(exist_ok=True)
    (article_dir / "output").mkdir(exist_ok=True)

    # Determine output path
    if output_dir:
        out_dir = Path(output_dir)
    else:
        out_dir = article_dir / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    html_filename = input_path.stem + ".html"
    output_path = out_dir / html_filename

    # Read Markdown
    with open(input_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Extract title from first H1 if present
    title_match = re.search(r"^#\s+(.+)$", md_content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else input_path.stem

    # Convert Markdown → HTML body
    renderer = WeChatRenderer(style=style)
    md = mistune.create_markdown(
        renderer=renderer,
        plugins=["strikethrough", "table", "task_lists"]
    )
    body = md(md_content)

    # Post-process to fix table header text color
    body = post_process_html(body)

    # Upload images to OSS if requested
    # NOTE: This must happen BEFORE the file:// path resolution below,
    # because the OSS uploader expects original relative/absolute paths.
    oss_stats = None
    if upload_images and oss_kwargs:
        from oss_uploader import upload_images_in_html
        print(f"  Uploading images to OSS...")
        oss_dir = style.get("image", {}).get("oss_dir", "wechat-articles")
        body, oss_stats = upload_images_in_html(
            body,
            article_dir=str(article_dir),
            oss_dir=oss_dir,
            **oss_kwargs,
        )

    # Resolve any remaining relative image paths to absolute file:// URLs
    # (local-preview fallback for images not uploaded to OSS)
    def resolve_img_src(match):
        url = match.group(1)
        # Only resolve local (non-http, non-data, non-file://) paths
        if not url.startswith(("http://", "https://", "data:", "file://")):
            abs_img = (article_dir / url).resolve()
            if abs_img.exists():
                return f'src="file://{abs_img}"'
        return match.group(0)

    body = re.sub(r'src="([^"]*)"', resolve_img_src, body)

    # Wrap in full HTML document
    html = wrap_html(body, style, title=title)

    # Write output
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return {"output_path": str(output_path), "oss_stats": oss_stats}


def convert_directory(
    input_dir: str,
    style: dict,
    output_dir: Optional[str] = None,
    upload_images: bool = False,
    oss_kwargs: Optional[dict] = None,
) -> list:
    """
    Batch-convert all .md files in a directory.

    Returns:
        List of result dicts (same structure as convert_file return value).
    """
    input_dir = Path(input_dir).resolve()
    md_files = sorted(input_dir.glob("*.md"))

    if not md_files:
        print(f"[WARNING] No .md files found in: {input_dir}")
        return []

    results = []
    for md_file in md_files:
        # Skip special files
        if md_file.name.lower() in ("readme.md", "title.md"):
            continue
        print(f"Converting: {md_file.name}")
        result = convert_file(
            str(md_file), style, output_dir,
            upload_images, oss_kwargs
        )
        print(f"  → {result['output_path']}")
        results.append(result)

    return results


# ─────────────────────────────────────────────
# CLI entry point
# ─────────────────────────────────────────────

def deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge `override` into `base`. Override wins on conflicts."""
    result = dict(base)
    for key, val in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(val, dict):
            result[key] = deep_merge(result[key], val)
        else:
            result[key] = val
    return result

def load_convert_cfg() -> dict:
    """读取 convert.cfg 默认配置文件。

    搜索顺序：
      1. 脚本同级目录的上一层（skill 根目录）： skills/markdown-to-wechat/convert.cfg
      2. 命令工作目录（项目根目录）： convert.cfg

    返回值：{'style': ..., 'config': ..., 'upload_images': bool}
    """
    # 脚本所在目录的上一层（skill 目录）
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent
    cwd = Path.cwd()

    candidates = [
        skill_dir / "convert.cfg",
        cwd / "convert.cfg",
    ]

    cfg = configparser.ConfigParser()
    for path in candidates:
        if path.exists():
            cfg.read(str(path), encoding="utf-8")
            break

    defaults = {}
    if cfg.has_section("defaults"):
        sec = cfg["defaults"]
        if "style" in sec:
            defaults["style"] = sec["style"].strip()
        if "config" in sec:
            defaults["config"] = sec["config"].strip()
        if "upload_images" in sec:
            defaults["upload_images"] = sec.getboolean("upload_images", fallback=False)
    return defaults



def main():
    # 读取 convert.cfg 默认配置
    cfg_defaults = load_convert_cfg()

    parser = argparse.ArgumentParser(
        description="Convert Markdown to WeChat Official Account HTML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
默认参数可在 skills/markdown-to-wechat/convert.cfg 中配置。
CLI 参数优先级高于配置文件。
        """
    )
    parser.add_argument(
        "--input", "-i", required=True,
        help="Input Markdown file or directory"
    )
    parser.add_argument(
        "--style", "-s", default=cfg_defaults.get("style"),
        help=f"Path to YAML style config (visual preset). "
             f"Default from convert.cfg: {cfg_defaults.get('style', 'none')}"
    )
    parser.add_argument(
        "--config", "-c", default=cfg_defaults.get("config"),
        help=f"Path to a local YAML config to deep-merge on top of --style. "
             f"Default from convert.cfg: {cfg_defaults.get('config', 'none')}"
    )
    parser.add_argument(
        "--output", "-o", default=None,
        help="Output directory (default: input_dir/output/)"
    )
    parser.add_argument(
        "--upload-images", action="store_true",
        default=cfg_defaults.get("upload_images", False),
        help="Upload local images to Aliyun OSS"
    )
    parser.add_argument(
        "--no-upload", action="store_true",
        help="强制禁用图片上传（即使 convert.cfg 中 upload_images=true）"
    )
    parser.add_argument("--oss-access-key-id", default=None)
    parser.add_argument("--oss-access-key-secret", default=None)
    parser.add_argument("--oss-bucket", default=None)
    parser.add_argument(
        "--oss-endpoint", default="oss-cn-shanghai.aliyuncs.com"
    )

    args = parser.parse_args()

    # --no-upload 可以覆盖 convert.cfg 中的 upload_images=true
    if args.no_upload:
        args.upload_images = False

    # Load base style, then deep-merge local config override (e.g. OSS credentials)
    style = load_style(args.style)
    if args.config and Path(args.config).exists():
        local_cfg = load_style(args.config)
        style = deep_merge(style, local_cfg)

    # Build OSS kwargs if needed
    # Credentials can come from CLI args OR from style.yaml image section
    oss_kwargs = None
    if args.upload_images:
        img_cfg = style.get("image", {})
        key_id = args.oss_access_key_id or img_cfg.get("oss_access_key_id", "")
        key_secret = args.oss_access_key_secret or img_cfg.get("oss_access_key_secret", "")
        bucket = args.oss_bucket or img_cfg.get("oss_bucket", "")
        endpoint = args.oss_endpoint or img_cfg.get("oss_endpoint", "oss-cn-shanghai.aliyuncs.com")

        # Reject placeholder values
        placeholders = {"YOUR_ACCESS_KEY_ID", "YOUR_ACCESS_KEY_SECRET", "YOUR_BUCKET_NAME", ""}
        if key_id in placeholders or key_secret in placeholders or bucket in placeholders:
            print(
                "ERROR: OSS credentials not configured.\n"
                "  Option 1: Pass --oss-access-key-id, --oss-access-key-secret, --oss-bucket\n"
                "  Option 2: Copy config-example.yaml to your series as config.yaml,\n"
                "            fill in oss_access_key_id / oss_access_key_secret / oss_bucket,\n"
                "            then run with --upload-images (no extra args needed)."
            )
            sys.exit(1)

        oss_kwargs = {
            "access_key_id": key_id,
            "access_key_secret": key_secret,
            "bucket_name": bucket,
            "endpoint": endpoint,
        }

    input_path = Path(args.input)

    if input_path.is_dir():
        # Batch mode
        print(f"\nBatch converting: {input_path}\n" + "─" * 40)

        # Look for series-level config.yaml
        series_style_path = args.style or str(input_path / "config.yaml")
        style = load_style(series_style_path if Path(series_style_path).exists()
                           else args.style)

        results = convert_directory(
            str(input_path), style, args.output,
            args.upload_images, oss_kwargs
        )

        # ── Summary report ──────────────────────────────────────────────────
        total_uploaded = sum(
            (r["oss_stats"]["uploaded"] if r["oss_stats"] else 0) for r in results
        )
        total_skipped = sum(
            (r["oss_stats"]["skipped"] if r["oss_stats"] else 0) for r in results
        )
        total_failed = sum(
            (r["oss_stats"]["failed"] if r["oss_stats"] else 0) for r in results
        )
        print("\n" + "═" * 50)
        print("  转换完成摘要")
        print("═" * 50)
        print(f"  ✅ 状态        : 成功")
        print(f"  📄 转换文件数  : {len(results)} 篇")
        if args.upload_images:
            print(f"  🖼  图片上传    : {total_uploaded} 张上传成功")
            if total_skipped:
                print(f"  📦 图片跳过    : {total_skipped} 张（已存在，无需重传）")
            if total_failed:
                print(f"  ❌ 图片失败    : {total_failed} 张上传失败")
        print("  📁 输出文件    :")
        for r in results:
            print(f"      {r['output_path']}")
        print("═" * 50)
        print("  提示：在浏览器中打开 HTML 文件，全选(Cmd+A)→复制→粘贴到微信公众号后台")
        print("═" * 50)

    elif input_path.is_file():
        # Single file mode
        print(f"Converting: {input_path.name}")

        # Look for config.yaml in same directory
        dir_style = input_path.parent / "config.yaml"
        resolved_style = args.style or (
            str(dir_style) if dir_style.exists() else None
        )
        style = load_style(resolved_style)

        result = convert_file(
            str(input_path), style, args.output,
            args.upload_images, oss_kwargs
        )

        # ── Summary report ──────────────────────────────────────────────────
        oss_stats = result.get("oss_stats")
        print("\n" + "═" * 50)
        print("  转换完成摘要")
        print("═" * 50)
        print(f"  ✅ 状态        : 成功")
        print(f"  📄 转换文件数  : 1 篇")
        if oss_stats is not None:
            print(f"  🖼  图片上传    : {oss_stats['uploaded']} 张上传成功")
            if oss_stats['skipped']:
                print(f"  📦 图片跳过    : {oss_stats['skipped']} 张（已存在，无需重传）")
            if oss_stats['failed']:
                print(f"  ❌ 图片失败    : {oss_stats['failed']} 张上传失败")
        print(f"  📁 输出文件    : {result['output_path']}")
        print("═" * 50)
        print("  提示：在浏览器中打开 HTML 文件，全选(Cmd+A)→复制→粘贴到微信公众号后台")
        print("═" * 50)

    else:
        print(f"ERROR: Input not found: {args.input}")
        sys.exit(1)


if __name__ == "__main__":
    main()
