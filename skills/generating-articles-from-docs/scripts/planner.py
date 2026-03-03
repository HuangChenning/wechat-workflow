#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文章规划器 - 使用 NotebookLM 分析文档并生成文章规划

用法:
    python scripts/run.py planner.py --source "知识库" --count 3 --topic "AI技术"
"""

import os
import sys
import json
import argparse
import yaml
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import re


def load_config(config_path: Path = None) -> Dict:
    """加载配置文件"""
    if config_path is None:
        config_path = Path(__file__).parent.parent / 'config.yaml'

    example_path = Path(__file__).parent.parent / 'config.example.yaml'

    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    elif example_path.exists():
        with open(example_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    else:
        return {}


def generate_plan_prompt(
    source_name: str,
    count: int,
    topic: str = None,
    style: str = "professional"
) -> str:
    """
    生成用于 NotebookLM 的提示词

    Args:
        source_name: 知识库名称
        count: 文章数量
        topic: 主题方向
        style: 文章风格

    Returns:
        提示词字符串
    """
    topic_clause = f"关于'{topic}'" if topic else "基于这些文档"

    # 简化提示词，要求返回清晰的列表格式
    prompt = f"""Based on these documents{topic_clause}, suggest exactly {count} article titles.

Return ONLY a numbered list like this:
1. Article Title One
2. Article Title Two
3. Article Title Three

Keep it {style} style and concise."""

    return prompt


def call_notebooklm(question: str, notebook_url: str = None) -> str:
    """
    调用 NotebookLM 获取答案

    Args:
        question: 要问的问题
        notebook_url: NotebookLM notebook URL

    Returns:
        NotebookLM 的回答
    """
    # 检查项目内的 notebooklm skill（优先）
    # 从当前脚本位置定位项目根目录
    current_skill = Path(__file__).parent.parent  # generating-articles-from-docs
    project_skills = current_skill.parent  # skills/ 目录
    notebooklm_skill = project_skills / 'notebooklm'

    # 如果项目内不存在，回退到全局技能
    if not notebooklm_skill.exists():
        notebooklm_skill = Path.home() / '.claude' / 'skills' / 'notebooklm'

    if not notebooklm_skill.exists():
        raise FileNotFoundError(
            f"NotebookLM skill 未找到。\n"
            f"预期位置: {project_skills / 'notebooklm'}\n"
            f"请确保 notebooklm 技能在项目的 skills/ 目录下"
        )

    # 使用 notebooklm skill 的 run.py
    import subprocess

    run_script = notebooklm_skill / 'scripts' / 'run.py'

    cmd = [
        sys.executable,
        str(run_script),
        'ask_question.py',
        '--question', question
    ]

    if notebook_url:
        cmd.extend(['--notebook-url', notebook_url])

    # 在 notebooklm skill 目录下运行，确保使用正确的 venv
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(notebooklm_skill),
        timeout=180  # 3分钟超时
    )

    if result.returncode != 0:
        raise RuntimeError(f"NotebookLM 调用失败: {result.stderr}")

    return result.stdout.strip()


def extract_articles_from_response(response: str, max_count: int = 10) -> List[Dict]:
    """
    从 NotebookLM 响应中提取文章标题

    Args:
        response: NotebookLM 的原始响应
        max_count: 最大返回文章数量

    Returns:
        文章列表
    """
    # 移除 "EXTREMELY IMPORTANT" 及其后面的内容
    if "EXTREMELY IMPORTANT" in response:
        response = response.split("EXTREMELY IMPORTANT")[0]

    # 提取主要答案部分
    lines = response.split('\n')
    content_lines = []

    skip_header = True
    for line in lines:
        if '====' in line and skip_header:
            skip_header = False
            continue
        if not skip_header and line.strip():
            # 跳过无关行 - 扩展过滤词列表
            skip_phrases = [
                'Would you like', 'Here is', 'Question:', 'Based on',
                'finalized', 'concise', 'professional', 'structure',
                'incorporates', 'requirements', 'suggest', 'article'
            ]
            if not any(phrase.lower() in line.lower() for phrase in skip_phrases):
                content_lines.append(line.strip())

    content = '\n'.join(content_lines).strip()

    articles = []
    seen_titles = set()  # 避免重复

    lines_list = [l for l in content.split('\n') if l.strip()]

    for line in lines_list:
        # 如果已经达到最大数量，停止
        if len(articles) >= max_count:
            break

        line = line.strip()

        # 清理引用标记
        line = re.sub(r'\[\d+\]', '', line)

        # 主要格式: "数字. 标题" 或 "数字 标题." 或 "标题数字."
        # 格式1: "1. Title" 或 "1.Title"
        match1 = re.match(r'^(\d+)[.\s]+(.+)$', line, re.IGNORECASE)
        if match1:
            title = match1.group(2).strip()
            # 清理标题末尾的数字和标点
            title = re.sub(r'\d+\.$', '', title).strip()
            title = re.sub(r'\s*[-–—]\s*.*$', '', title).strip()  # 移除后面描述

            if title and 10 < len(title) < 150 and title not in seen_titles:
                seen_titles.add(title)
                articles.append(create_article_dict(len(articles) + 1, title))
                continue

        # 格式2: "Title1." 或 "Title 1." - 数字在末尾，可能带空格
        match2 = re.match(r'^(.+?)\s*(\d+)\.$', line)
        if match2:
            title = match2.group(1).strip()

            # 只有当标题看起来合理时才添加
            if title and 10 < len(title) < 150 and title not in seen_titles:
                seen_titles.add(title)
                articles.append(create_article_dict(len(articles) + 1, title))
                continue

    return articles


def create_article_dict(index: int, title: str) -> Dict:
    """创建文章字典结构"""
    return {
        'index': index,
        'title': title,
        'subtitle': '基于 NotebookLM 分析',
        'target_audience': '一般读者',
        'key_points': ['待使用 LLM 生成详细内容'],
        'outline': [
            {'section': '引言', 'content': '引入主题背景'},
            {'section': '正文', 'content': '详细展开要点'},
            {'section': '结论', 'content': '总结和展望'}
        ],
        'estimated_length': 1500,
        'suggested_images': [
            f'{title[:30]}...相关配图',
            '概念图解'
        ],
        'source_references': ['NotebookLM 分析']
    }


def save_plan(plan: Dict, output_path: Path) -> None:
    """保存文章规划到文件"""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    # 同时生成 Markdown 版本
    md_path = output_path.with_suffix('.md')
    generate_plan_markdown(plan, md_path)


def generate_plan_markdown(plan: Dict, output_path: Path) -> None:
    """生成 Markdown 版本的文章规划"""
    lines = [
        "# 文章生成规划",
        f"\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"\n## 概述\n\n{plan.get('overview', '暂无概述')}",
        f"\n## 文章列表 ({len(plan.get('articles', []))} 篇)\n"
    ]

    for article in plan.get('articles', []):
        lines.extend([
            f"\n### {article.get('index', '?')}. {article.get('title', '未命名')}",
            f"\n**副标题**: {article.get('subtitle', '无')}",
            f"\n**目标读者**: {article.get('target_audience', '一般读者')}",
            f"\n**预估长度**: {article.get('estimated_length', 1000)} 字",
            f"\n**关键要点**:"
        ])

        for point in article.get('key_points', []):
            lines.append(f"  - {point}")

        lines.extend([
            f"\n**建议配图**:"
        ])

        for img in article.get('suggested_images', []):
            lines.append(f"  - {img}")

    # 添加阅读顺序建议
    if plan.get('suggested_read_order'):
        lines.extend([
            f"\n## 建议阅读顺序\n\n"
            f"{' → '.join(map(str, plan['suggested_read_order']))}"
        ])

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def main():
    parser = argparse.ArgumentParser(
        description='使用 NotebookLM 生成文章规划',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--source', '-s',
        required=True,
        help='知识库名称或 NotebookLM notebook URL'
    )

    parser.add_argument(
        '--count', '-c',
        type=int,
        default=3,
        help='文章数量 (默认: 3)'
    )

    parser.add_argument(
        '--topic', '-t',
        default=None,
        help='主题方向 (可选)'
    )

    parser.add_argument(
        '--style',
        default='professional',
        choices=['professional', 'casual', 'technical', 'creative'],
        help='文章风格 (默认: professional)'
    )

    parser.add_argument(
        '--output', '-o',
        default=None,
        help='输出目录 (默认: ./output)'
    )

    parser.add_argument(
        '--notebook-url',
        default=None,
        help='NotebookLM notebook URL (覆盖配置文件)'
    )

    args = parser.parse_args()

    # 加载配置
    config = load_config()

    # 确定输出目录
    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = Path(__file__).parent.parent / 'output'

    output_dir.mkdir(parents=True, exist_ok=True)

    # 确定 notebook URL
    notebook_url = args.notebook_url or config.get('notebooklm', {}).get('notebook_url')

    # 生成提示词
    prompt = generate_plan_prompt(
        source_name=args.source,
        count=args.count,
        topic=args.topic,
        style=args.style
    )

    print(f"\n{'='*60}")
    print(f"📋 文章规划器")
    print(f"{'='*60}")
    print(f"\n知识库: {args.source}")
    print(f"文章数量: {args.count}")
    if args.topic:
        print(f"主题方向: {args.topic}")
    print(f"文章风格: {args.style}")
    print(f"\n{'='*60}\n")
    print(f"⏳ 正在调用 NotebookLM 分析...")

    try:
        # 调用 NotebookLM
        response = call_notebooklm(prompt, notebook_url)

        print(f"✅ NotebookLM 响应完成\n")

        # 解析响应
        articles = extract_articles_from_response(response)

        if not articles:
            print("⚠️  未能解析出文章标题，使用默认标题")
            for i in range(args.count):
                articles.append({
                    'index': i + 1,
                    'title': f'文章 {i + 1}: {args.topic or "基于文档分析"}',
                    'subtitle': '基于文档内容生成',
                    'target_audience': '一般读者',
                    'key_points': ['关键要点'],
                    'outline': [],
                    'estimated_length': 1500,
                    'suggested_images': ['配图1'],
                    'source_references': ['默认生成']
                })

        # 构建规划
        plan = {
            'overview': f"基于 NotebookLM 分析生成的 {len(articles)} 篇文章规划",
            'articles': articles,
            'suggested_read_order': list(range(1, len(articles) + 1)),
            'raw_response': response[:500] if len(response) > 500 else response
        }

        # 保存规划
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_path = output_dir / f'plan_{timestamp}.json'

        save_plan(plan, json_path)

        print(f"✅ 规划已保存:")
        print(f"   JSON: {json_path}")
        print(f"   Markdown: {json_path.with_suffix('.md')}")

        # 输出摘要
        print(f"\n📝 规划包含 {len(articles)} 篇文章:")
        for article in articles:
            print(f"   {article.get('index', '?')}. {article.get('title', '未命名')}")

        return 0

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
