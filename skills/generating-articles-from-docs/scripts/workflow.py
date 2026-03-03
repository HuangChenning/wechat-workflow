#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整工作流 - 从文档到生成文章的端到端流程

用法:
    python scripts/run.py workflow.py --source ./documents --count 3 --topic "AI"
"""

import os
import sys
import json
import argparse
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List


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


def print_step(step_num: int, total: int, title: str):
    """打印步骤标题"""
    print(f"\n{'='*60}")
    print(f"步骤 {step_num}/{total}: {title}")
    print(f"{'='*60}\n")


def step_1_upload(source: Path, output_dir: Path) -> Dict:
    """步骤 1: 上传文档"""
    print_step(1, 5, "上传文档")

    import importlib.util
    upload_script = Path(__file__).parent / 'upload.py'
    spec = importlib.util.spec_from_file_location("upload", upload_script)
    upload_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(upload_module)

    documents = upload_module.scan_directory(source, recursive=True)

    if not documents:
        print("⚠️  未找到文档")
        return {'documents': []}

    print(f"📋 找到 {len(documents)} 个文档")
    for doc in documents[:5]:
        print(f"   - {doc.name}")
    if len(documents) > 5:
        print(f"   ... 还有 {len(documents) - 5} 个")

    knowledge_dir = output_dir / 'data' / 'uploaded'
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    results = upload_module.copy_documents(
        documents,
        knowledge_dir,
        datetime.now().strftime('%Y%m%d_%H%M%S')
    )

    return {
        'documents': [d['source'] for d in results['success']],
        'knowledge_dir': str(knowledge_dir),
        'count': len(results['success'])
    }


def step_2_analyze(upload_result: Dict, config: Dict) -> Dict:
    """步骤 2: 使用 NotebookLM 分析内容"""
    print_step(2, 5, "NotebookLM 内容分析")

    notebook_url = config.get('notebooklm', {}).get('notebook_url')

    if not notebook_url:
        print("⚠️  未配置 NotebookLM URL")
        print("   请在 config.yaml 中配置 notebooklm.notebook_url")
        print("   或通过 --notebook-url 参数指定")
        return {'analyzed': False}

    print("📝 提示: 请确保文档已上传到 NotebookLM")
    print(f"   Notebook URL: {notebook_url}")

    return {
        'analyzed': True,
        'notebook_url': notebook_url
    }


def step_3_plan(upload_result: Dict, args, config: Dict) -> Dict:
    """步骤 3: 生成文章规划"""
    print_step(3, 5, "生成文章规划")

    import importlib.util
    planner_script = Path(__file__).parent / 'planner.py'
    spec = importlib.util.spec_from_file_location("planner", planner_script)
    planner_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(planner_module)

    # 生成提示词
    prompt = planner_module.generate_plan_prompt(
        source_name="知识库",
        count=args.count,
        topic=args.topic,
        style=config.get('generation', {}).get('style', 'professional')
    )

    print(f"文章数量: {args.count}")
    if args.topic:
        print(f"主题方向: {args.topic}")

    # 调用 NotebookLM
    try:
        notebook_url = args.notebook_url or config.get('notebooklm', {}).get('notebook_url')
        response = planner_module.call_notebooklm(prompt, notebook_url)

        # 解析响应 - 限制返回数量为请求的数量 + 2（允许一些误差）
        articles = planner_module.extract_articles_from_response(response, max_count=args.count + 2)

        if not articles:
            print("⚠️  未能解析文章，使用默认规划")
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
        output_dir = Path(args.output) if args.output else Path(__file__).parent.parent / 'output'
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_path = output_dir / f'plan_{timestamp}.json'
        planner_module.save_plan(plan, json_path)

        print(f"✅ 规划已保存: {json_path}")

        print(f"\n📝 规划包含 {len(articles)} 篇文章:")
        for article in articles:
            print(f"   {article.get('index', '?')}. {article.get('title', '未命名')}")

        return {
            'planned': True,
            'plan': plan,
            'plan_path': str(json_path)
        }

    except Exception as e:
        print(f"⚠️  规划生成失败: {e}")
        print("   将使用默认规划")

        # 使用默认规划
        plan = {
            'overview': '默认规划',
            'articles': [
                {
                    'index': i + 1,
                    'title': f'文章 {i + 1}',
                    'subtitle': '基于文档内容生成',
                    'target_audience': '一般读者',
                    'key_points': ['要点1', '要点2', '要点3'],
                    'outline': [],
                    'suggested_images': ['配图1', '配图2']
                }
                for i in range(args.count)
            ]
        }

        return {
            'planned': False,
            'plan': plan
        }


def step_4_generate(plan_result: Dict, config: Dict) -> Dict:
    """步骤 4: 生成文章内容"""
    print_step(4, 5, "生成文章内容")

    plan = plan_result.get('plan', {})
    articles = plan.get('articles', [])

    if not articles:
        print("⚠️  没有文章规划")
        return {'generated': []}

    print(f"📝 将生成 {len(articles)} 篇文章")

    output_dir = Path(__file__).parent.parent / 'output' / 'articles'
    output_dir.mkdir(parents=True, exist_ok=True)

    generated = []

    for article in articles:
        index = article.get('index', 0)
        title = article.get('title', f'文章{index}')

        # 清理文件名中的特殊字符
        safe_title = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in title)
        filename = f"{index:02d}_{safe_title[:30]}.md"
        filepath = output_dir / filename

        # 生成 Markdown 内容
        content = generate_article_markdown(article, config)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"   ✅ {filename}")
        generated.append(str(filepath))

    return {
        'generated': generated,
        'output_dir': str(output_dir)
    }


def generate_article_markdown(article: Dict, config: Dict) -> str:
    """生成文章 Markdown 内容"""
    lines = [
        f"# {article.get('title', '未命名')}\n",
        f"## {article.get('subtitle', '')}\n",
        f"> 目标读者: {article.get('target_audience', '一般读者')}\n",
        f"---\n"
    ]

    # 大纲内容
    for item in article.get('outline', []):
        section = item.get('section', '')
        content = item.get('content', '')
        lines.append(f"## {section}\n\n{content}\n")

    # 关键点
    if article.get('key_points'):
        lines.append("\n## 关键要点\n\n")
        for point in article['key_points']:
            lines.append(f"- {point}\n")

    # 图片占位符
    if article.get('suggested_images'):
        lines.append("\n## 配图\n\n")
        for i, img_desc in enumerate(article['suggested_images'], 1):
            img_path = f"./img/{article.get('index', 1):02d}_{i}.png"
            lines.append(f'\n```image-prompt\n')
            lines.append(f'用途：{img_desc}\n')
            lines.append(f'工具：Gemini 3.1 Flash Image Preview\n')
            lines.append(f'图片路径：{img_path}\n')
            lines.append(f'Prompt (英文):\n')
            lines.append(f'Subject: {img_desc}\n')
            lines.append(f'Details:\n')
            lines.append(f'- High quality, detailed\n')
            lines.append(f'- Professional photography style\n')
            lines.append(f' Technical: 4K, cinematic lighting --ar 16:9\n')
            lines.append(f'```\n\n')

    return ''.join(lines)


def step_5_images(generate_result: Dict, config: Dict) -> Dict:
    """步骤 5: 生成图片"""
    print_step(5, 5, "生成配图")

    images_enabled = config.get('images', {}).get('enabled', True)

    if not images_enabled:
        print("⏭️  图片生成已禁用")
        return {'skipped': True}

    # 导入图片生成模块
    import importlib.util
    images_script = Path(__file__).parent / 'generate_images.py'
    spec = importlib.util.spec_from_file_location("generate_images", images_script)
    images_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(images_module)

    # 从当前脚本位置定位项目
    current_skill = Path(__file__).parent.parent  # generating-articles-from-docs
    project_skills = current_skill.parent  # skills/ 目录

    skill_paths = [
        # 优先：项目内的 wechat-workflow/generating-article-images
        project_skills / 'wechat-workflow' / 'generating-article-images',
        # 回退：全局技能
        Path.home() / '.claude' / 'skills' / 'generating-article-images',
        Path.home() / '.claude' / 'skills' / 'wechat-workflow' / 'generating-article-images',
    ]

    images_skill = None
    for path in skill_paths:
        if path.exists():
            images_skill = path
            break

    if not images_skill:
        print("⚠️  未找到 generating-article-images skill")
        return {'skipped': True}

    generated_articles = generate_result.get('generated', [])
    if not generated_articles:
        print("⚠️  没有生成文章，跳过图片生成")
        return {'skipped': True}

    print(f"📸 使用 skill: {images_skill.name}")
    print(f"📝 待处理文章: {len(generated_articles)}")

    successful = 0
    failed = 0

    for article_path in generated_articles:
        article_path = Path(article_path)

        print(f"\n   处理: {article_path.name}")

        # 检查是否有 image-prompt 代码块
        prompts = images_module.extract_image_prompts(article_path)

        if not prompts:
            print(f"   ⏭️  跳过 (无图片提示词)")
            continue

        print(f"   📋 找到 {len(prompts)} 个图片提示词")

        # 调用图片生成
        success = images_module.generate_images(article_path, images_skill)

        if success:
            successful += 1
        else:
            failed += 1

    print(f"\n📊 图片生成统计:")
    print(f"   成功: {successful}")
    print(f"   失败: {failed}")

    return {
        'skipped': False,
        'images_skill': str(images_skill),
        'successful': successful,
        'failed': failed
    }


def main():
    parser = argparse.ArgumentParser(
        description='从文档生成文章的完整工作流',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--source', '-s',
        required=True,
        help='源文档目录路径'
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
        '--output', '-o',
        default=None,
        help='输出目录 (默认: ./output)'
    )

    parser.add_argument(
        '--notebook-url',
        default=None,
        help='NotebookLM notebook URL'
    )

    parser.add_argument(
        '--steps',
        default=None,
        help='要执行的步骤 (逗号分隔，如: 1,2,3,4,5)'
    )

    args = parser.parse_args()

    config = load_config()

    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = Path(__file__).parent.parent / 'output'

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'🚀'*30}")
    print(f"   从文档生成文章 - 完整工作流")
    print(f"{'🚀'*30}")
    print(f"\n源目录: {args.source}")
    print(f"文章数量: {args.count}")
    if args.topic:
        print(f"主题方向: {args.topic}")
    print(f"输出目录: {output_dir}")

    if args.steps:
        steps_to_run = [int(s.strip()) for s in args.steps.split(',')]
    else:
        steps_to_run = [1, 2, 3, 4, 5]

    results = {}

    try:
        if 1 in steps_to_run:
            source_path = Path(args.source).expanduser().resolve()
            results['upload'] = step_1_upload(source_path, output_dir)

        if 2 in steps_to_run:
            results['analyze'] = step_2_analyze(results.get('upload', {}), config)

        if 3 in steps_to_run:
            results['plan'] = step_3_plan(results.get('upload', {}), args, config)

        if 4 in steps_to_run:
            results['generate'] = step_4_generate(results.get('plan', {}), config)

        if 5 in steps_to_run:
            results['images'] = step_5_images(results.get('generate', {}), config)

        print(f"\n{'='*60}")
        print(f"✅ 工作流完成!")
        print(f"{'='*60}")

        if 'upload' in results:
            print(f"\n📁 上传文档: {results['upload'].get('count', 0)} 个")

        if 'generate' in results:
            print(f"📝 生成文章: {len(results['generate'].get('generated', []))} 篇")

        print(f"\n📂 输出目录: {output_dir}")

        return 0

    except KeyboardInterrupt:
        print(f"\n\n⚠️  用户中断")
        return 1
    except Exception as e:
        print(f"\n\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
