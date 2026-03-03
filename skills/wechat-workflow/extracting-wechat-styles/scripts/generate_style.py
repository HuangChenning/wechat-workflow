import os
import re
import yaml
import argparse
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional

class StyleGenerator:
    def __init__(self, html_content: str):
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.style_config = {
            "basic": {},
            "paragraph": {},
            "heading": {
                "h1": {"content": {}},
                "h2": {"content": {}},
                "h3": {"content": {}},
                "h4": {"content": {}},
            },
            "blockquote": {"container": {}, "p": {}},
            "list": {"ul": {}, "ol": {}, "li": {}, "section": {}},
            "code": {"pre": {}, "code": {}},
            "table": {"container": {}, "table": {}, "th": {}, "td": {}},
            "hr": {},
            "image": {"oss_dir": "wechat-articles", "upload_to_oss": False}
        }

    def _parse_inline_style(self, style_str: Optional[str]) -> Dict[str, str]:
        if not style_str:
            return {}
        styles = {}
        for item in style_str.split(';'):
            if ':' in item:
                key, value = item.split(':', 1)
                styles[key.strip()] = value.strip()
        return styles

    def extract(self):
        # 1. Basic Style (from #nice section)
        nice_section = self.soup.find('section', id='nice')
        if nice_section:
            basic_styles = self._parse_inline_style(nice_section.get('style'))
            self.style_config["basic"] = basic_styles

        # 2. Paragraphs
        p_tag = self.soup.find('p', style=True)
        if p_tag:
            self.style_config["paragraph"] = self._parse_inline_style(p_tag.get('style'))

        # 3. Headings
        for level in range(1, 5):
            h_tag = self.soup.find(f'h{level}', style=True)
            if h_tag:
                tag_name = f'h{level}'
                self.style_config["heading"][tag_name] = self._parse_inline_style(h_tag.get('style'))
                # Handle .content span if exists
                content_span = h_tag.find('span', class_='content')
                if content_span:
                    self.style_config["heading"][tag_name]["content"] = self._parse_inline_style(content_span.get('style'))

        # 4. Blockquote
        bq_tag = self.soup.find('blockquote', style=True)
        if bq_tag:
            self.style_config["blockquote"]["container"] = self._parse_inline_style(bq_tag.get('style'))
            bq_p = bq_tag.find('p', style=True)
            if bq_p:
                self.style_config["blockquote"]["p"] = self._parse_inline_style(bq_p.get('style'))

        # 5. Lists
        ul_tag = self.soup.find('ul', style=True)
        if ul_tag:
            self.style_config["list"]["ul"] = self._parse_inline_style(ul_tag.get('style'))
        ol_tag = self.soup.find('ol', style=True)
        if ol_tag:
            self.style_config["list"]["ol"] = self._parse_inline_style(ol_tag.get('style'))
        li_tag = self.soup.find('li', style=True)
        if li_tag:
            # mdnice often has a section inside li
            li_styles = self._parse_inline_style(li_tag.get('style'))
            self.style_config["list"]["li"] = li_styles
            li_section = li_tag.find('section', style=True)
            if li_section:
                self.style_config["list"]["section"] = self._parse_inline_style(li_section.get('style'))

        # 6. Tables
        table_container = self.soup.find('section', class_='table-container')
        if table_container:
            self.style_config["table"]["container"] = self._parse_inline_style(table_container.get('style'))
        table_tag = self.soup.find('table', style=True)
        if table_tag:
            self.style_config["table"]["table"] = self._parse_inline_style(table_tag.get('style'))
        th_tag = self.soup.find('th', style=True)
        if th_tag:
            self.style_config["table"]["th"] = self._parse_inline_style(th_tag.get('style'))
        td_tag = self.soup.find('td', style=True)
        if td_tag:
            self.style_config["table"]["td"] = self._parse_inline_style(td_tag.get('style'))

        # 7. HR
        hr_tag = self.soup.find('hr', style=True)
        if hr_tag:
            self.style_config["hr"] = self._parse_inline_style(hr_tag.get('style'))

        # 8. Code
        pre_tag = self.soup.find('pre', style=True)
        if pre_tag:
            self.style_config["code"]["pre"] = self._parse_inline_style(pre_tag.get('style'))
        code_tag = self.soup.find('code', style=True)
        if code_tag:
            self.style_config["code"]["code"] = self._parse_inline_style(code_tag.get('style'))

    def save(self, output_path: str):
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.style_config, f, allow_unicode=True, sort_keys=False)
        print(f"Style saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate WeChat style YAML from HTML")
    parser.add_argument("--input", required=True, help="Input HTML file path")
    parser.add_argument("--name", required=True, help="Style name (will be saved as <name>.yaml)")
    parser.add_argument("--output-dir", default="../../markdown-to-wechat/styles", help="Output directory")
    
    args = parser.parse_args()
    
    input_path = os.path.abspath(args.input)
    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    generator = StyleGenerator(html_content)
    generator.extract()
    
    output_filename = f"{args.name}.yaml"
    # Ensure output_dir is relative to script location OR absolute
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.abspath(os.path.join(script_dir, args.output_dir))
    output_path = os.path.join(output_dir, output_filename)
    
    generator.save(output_path)

if __name__ == "__main__":
    main()
