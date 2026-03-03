---
name: extracting-wechat-styles
description: Use when creating new WeChat style presets from existing HTML templates (e.g., mdnice exports). Parses HTML with BeautifulSoup and extracts CSS styles into YAML format compatible with converting-to-wechat. Outputs to wechat-workflow/converting-to-wechat/styles/ directory.
---

# Extracting WeChat Styles

**Formerly known as**: `wechat-style-generator`

Automate the extraction of WeChat article styles from exported HTML files (e.g., from mdnice).

## Overview

This skill provides a tool to parse an HTML file and extract its CSS styles into a YAML format compatible with the `converting-to-wechat` skill. This allows you to easily "borrow" beautiful styles from other platforms and use them in your own automated conversion workflow.

## Usage

### Prerequisites

Install dependencies:
```bash
pip install beautifulsoup4 pyyaml
```

### Running the Generator

Execute the script from the `scripts` directory:

```bash
python3 generate_style.py --input <path_to_html> --name <style_name>
```

Arguments:
- `--input`: Path to the HTML file containing the desired styles.
- `--name`: The name for your new style. It will be saved as `styles/<name>.yaml` in the `converting-to-wechat` skill.
- `--output-dir`: (Optional) Custom output directory for the YAML file.

## How it Works

The script uses `BeautifulSoup` to locate key HTML elements used by common WeChat editors (like mdnice) and extracts their inline `style` attributes. These styles are then mapped to the structured YAML format used by `converting-to-wechat`:

1.  **Basic**: Global settings like font family and container padding.
2.  **Paragraph**: Default paragraph styling.
3.  **Heading**: H1-H4 styles, including special "content" span styling.
4.  **Blockquote**: Container and internal paragraph styling.
5.  **List**: Styles for UL, OL, LI, and internal sections.
6.  **Table**: Styles for table containers, headers, and cells.
7.  **Code**: Styles for code blocks and inline code.
8.  **HR**: Horizontal rule styling.

## Example

To extract styles from `example/test.html` and name it `mdnice-blue`:

```bash
python3 scripts/generate_style.py --input ../../example/test.html --name mdnice-blue
```

The resulting file will be available at `../converting-to-wechat/styles/mdnice-blue.yaml`.

## Related Skills

- **`wechat-workflow:converting-to-wechat`** - Use the extracted styles to convert Markdown articles to WeChat HTML format. The output from this skill is designed to work with converting-to-wechat's style system.
