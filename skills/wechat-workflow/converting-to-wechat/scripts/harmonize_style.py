#!/usr/bin/env python3
import argparse
import colorsys
import yaml
from pathlib import Path

def hex_to_hsl(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    r, g, b = r/255.0, g/255.0, b/255.0
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h, l, s

def hsl_to_hex(h, l, s):
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))

def get_contrast_color(hex_color):
    """Return #ffffff or #000000 based on the brightness of the input color."""
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    # Relative luminance formula
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "#ffffff" if luminance < 0.5 else "#000000"

def harmonize_style(base_hex, name):
    h, l, s = hex_to_hsl(base_hex)
    
    # Generate variations
    primary = base_hex
    # Darker version for headings
    heading_color = hsl_to_hex(h, max(0, l - 0.1), s)
    # Lighter/Desaturated for background
    bg_light = hsl_to_hex(h, 0.97, min(s, 0.2))
    # Border color - slightly darker for better visibility
    border_color = hsl_to_hex(h, 0.85, min(s, 0.3))
    # Header text color - contrast aware
    header_text_color = get_contrast_color(primary)
    # Alternate row color - slightly darker for better visibility
    alt_row_bg = hsl_to_hex(h, 0.98, min(s, 0.1))
    # Accent (Strong) - Professional Gold/Orange often works well with Blue
    # Or just a much more saturated/different hue
    strong_h = (h + 0.5) % 1.0 # Complementary
    strong_color = hsl_to_hex(strong_h, 0.45, 0.8) 
    if abs(h - strong_h) < 0.1 or abs(h - strong_h) > 0.9: # If too close
         strong_color = "#e67e22" # Safe fallback orange
    
    # Let's fix strong_color to be a high-contrast warm color if base is blue-ish
    if 0.5 < h < 0.7: # Blue range
        strong_color = "#e67e22" # Oracle-style orange/gold
    
    em_color = primary
    code_inline_color = hsl_to_hex(0, 0.2, 0) # Neutral dark or specialized? Let's use a standard "berry" or neutral
    code_inline_color = "#c7254e" # Common standard, or harmonize
    code_inline_color = hsl_to_hex(h, 0.4, 0.8)

    style = {
        "theme": name,
        "container": {
            "max_width": "677px",
            "font_size": "15px",
            "line_height": "1.8",
            "color": "#333333",
            "font_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
            "padding": "0 20px",
            "margin": "20px auto"
        },
        "headings": {
            "h1": {
                "font_size": "24px",
                "color": heading_color,
                "margin": "35px 0 18px",
                "font_weight": "bold",
                "border_bottom": f"2px solid {primary}",
                "padding_bottom": "8px"
            },
            "h2": {
                "font_size": "20px",
                "color": heading_color,
                "margin": "35px 0 15px",
                "font_weight": "bold"
            },
            "h3": {
                "font_size": "17px",
                "color": "#333333",
                "margin": "28px 0 12px",
                "font_weight": "bold"
            }
        },
        "paragraph": {
            "margin": "14px 0",
            "color": "#333333"
        },
        "strong": {
            "color": strong_color,
            "font_weight": "700"
        },
        "em": {
            "color": em_color,
            "font_style": "italic"
        },
        "code_inline": {
            "padding": "2px 5px",
            "background": "#f8f9fa",
            "border_radius": "3px",
            "font_size": "13px",
            "color": code_inline_color,
            "border": "1px solid #f0f0f0",
            "font_family": "'SF Mono', Monaco, Consolas, monospace"
        },
        "code_block": {
            "margin": "14px 0",
            "padding": "14px",
            "background": "#282c34",
            "border_radius": "4px",
            "border": "1px solid #e9ecef",
            "font_size": "13px",
            "line_height": "1.6",
            "font_family": "Operator Mono, Consolas, Monaco, Menlo, monospace",
            "white_space": "pre-wrap",
            "word_wrap": "break-word",
            "color": "#abb2bf"
        },
        "blockquote": {
            "margin": "18px 0",
            "padding": "14px 18px",
            "background": bg_light,
            "border_left": f"4px solid {primary}",
            "color": "#666666",
            "border_radius": "0 4px 4px 0"
        },
        "list": {
            "margin": "14px 0",
            "padding_left": "20px",
            "color": "#333333",
            "item_margin": "8px 0"
        },
        "table": {
            "margin": "18px 0",
            "width": "100%",
            "border_collapse": "collapse",
            "border": f"1px solid {border_color}",
            "font_size": "14px",
            "header_bg": "#ffffff",
            "header_color": primary,
            "header_padding": "10px",
            "cell_padding": "10px",
            "cell_border": f"1px solid {border_color}",
            "cell_color": "#333333",
            "alternate_row_bg": alt_row_bg
        },
        "hr": {
            "border": "none",
            "border_top": "1px solid #e0e0e0",
            "margin": "24px 0"
        },
        "link": {
            "color": primary,
            "text_decoration": "none"
        },
        "image": {
            "max_width": "100%",
            "height": "auto",
            "border": f"1px solid {border_color}",
            "border_radius": "4px",
            "box_shadow": "0 2px 8px rgba(0,0,0,0.05)",
            "display": "block",
            "margin": "18px auto",
            "upload_to_oss": False,
            "oss_dir": "wechat-articles"
        }
    }
    return style

def main():
    parser = argparse.ArgumentParser(description="Generate a harmonious WeChat style YAML.")
    parser.add_argument("--base", required=True, help="Base hex color (e.g. #007aff)")
    parser.add_argument("--name", default="harmonized", help="Theme name")
    parser.add_argument("--output", help="Output YAML path")
    
    args = parser.parse_args()
    
    style = harmonize_style(args.base, args.name)
    
    if args.output:
        out_path = Path(args.output)
    else:
        out_path = Path(__file__).parent.parent / "styles" / f"{args.name}.yaml"
    
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.dump(style, f, allow_unicode=True, sort_keys=False)
    
    print(f"Harmonized style generated at: {out_path}")

if __name__ == "__main__":
    main()
