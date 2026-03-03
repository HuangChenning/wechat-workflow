#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容生成模块 - 使用 Claude API 生成完整文章内容

用法:
    python scripts/run.py generate_content.py --plan ./output/plan.json
"""

import os
import sys
import argparse
import json
from pathlib import Path
from typing import List, Dict


def get_claude_client():
    """获取 Claude 客户端"""
    try:
        from anthropic import Anthropic
    except ImportError:
        print("⚠️  需要安装 anthropic 包: pip install anthropic")
        return None

    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("⚠️  未设置 ANTHROPIC_API_KEY 环境变量")
        return None

    return Anthropic(api_key=api_key)


def generate_article_content(article: Dict, style: str = 'professional') -> str:
    """
    使用 Claude API 生成完整文章内容

    Args:
        article: 文章规划信息
        style: 文章风格

    Returns:
        文章内容 (Markdown 格式)
    """
    client = get_claude_client()
    if not client:
        return None

    title = article.get('title', '')
    subtitle = article.get('subtitle', '')
    outline = article.get('outline', [])
    key_points = article.get('key_points', [])

    # 构建生成提示
    system_prompt = f"""你是一位专业的文章作者，擅长撰写{style}风格的技术文章。

写作要求：
1. 文章结构清晰，有引言、正文、结论
2. 内容详实，有深度，避免泛泛而谈
3. 语言流畅，专业但不晦涩
4. 适当使用例子和比喻帮助理解
5. 保持客观中立的态度"""

    user_prompt = f"""请根据以下规划生成一篇完整的文章：

标题：{title}
副标题：{subtitle}

关键要点：
{chr(10).join(f'- {p}' for p in key_points)}

大纲：
{chr(10).join(f'{i+1}. {o["section"]}: {o["content"]}' for i, o in enumerate(outline))}

要求：
- 文章长度约 {article.get('estimated_length', 1500)} 字
- 使用 Markdown 格式
- 直接输出文章内容，不要有任何其他说明
- 不要包含图片占位符或代码块标记"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8192,
            temperature=0.7,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )

        content = response.content[0].text
        return content

    except Exception as e:
        print(f"⚠️  Claude API 调用失败: {e}")
        return None


def save_article(article: Dict, content: str, output_dir: Path, index: int) -> Path:
    """
    保存文章到文件

    Args:
        article: 文章信息
        content: 文章内容
        output_dir: 输出目录
        index: 文章索引

    Returns:
        文件路径
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # 清理文件名
    safe_title = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in article['title'][:50])
    filename = f"{index:02d}_{safe_title}.md"
    filepath = output_dir / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filepath


def main():
    parser = argparse.ArgumentParser(
        description='使用 Claude API 生成文章内容',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--plan', '-p',
        required=True,
        help='文章规划 JSON 文件路径'
    )

    parser.add_argument(
        '--output', '-o',
        default=None,
        help='输出目录 (默认: ./output/articles)'
    )

    parser.add_argument(
        '--style',
        default='professional',
        choices=['professional', 'casual', 'technical', 'creative'],
        help='文章风格 (默认: professional)'
    )

    parser.add_argument(
        '--index', '-i',
        type=int,
        default=None,
        help='只生成指定索引的文章'
    )

    args = parser.parse_args()

    # 加载规划
    plan_path = Path(args.plan)
    if not plan_path.exists():
        print(f"❌ 规划文件不存在: {plan_path}")
        return 1

    with open(plan_path, 'r', encoding='utf-8') as f:
        plan = json.load(f)

    articles = plan.get('articles', [])
    if not articles:
        print("❌ 规划中没有文章")
        return 1

    # 确定输出目录
    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = Path(__file__).parent.parent / 'output' / 'articles'

    # 筛选要生成的文章
    if args.index is not None:
        articles = [a for a in articles if a.get('index') == args.index]
        if not articles:
            print(f"❌ 未找到索引为 {args.index} 的文章")
            return 1

    print(f"\n{'='*60}")
    print(f"📝 生成文章内容")
    print(f"{'='*60}")
    print(f"\n规划文件: {plan_path}")
    print(f"文章数量: {len(articles)}")
    print(f"文章风格: {args.style}")

    # 检查 API
    client = get_claude_client()
    if not client:
        print("\n💡 提示: 设置环境变量以使用 Claude API")
        print("   export ANTHROPIC_API_KEY=your-api-key")
        print("   pip install anthropic")
        return 1

    print(f"\n⏳ 开始生成...\n")

    generated = []

    for article in articles:
        index = article.get('index', 0)
        title = article.get('title', '未命名')

        print(f"   [{index}/{len(articles)}] {title}...")

        content = generate_article_content(article, args.style)

        if content:
            filepath = save_article(article, content, output_dir, index)
            print(f"   ✅ 已保存: {filepath.name}")
            generated.append(str(filepath))
        else:
            print(f"   ❌ 生成失败")

    print(f"\n{'='*60}")
    print(f"✅ 生成完成: {len(generated)}/{len(articles)}")
    print(f"📂 输出目录: {output_dir}")

    return 0 if len(generated) == len(articles) else 1


if __name__ == '__main__':
    sys.exit(main())
