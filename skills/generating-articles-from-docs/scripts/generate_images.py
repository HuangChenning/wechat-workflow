#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片生成集成模块 - 自动调用 generating-article-images skill

用法:
    python scripts/run.py generate_images.py --article ./output/articles/01_article.md
"""

import os
import sys
import re
import subprocess
import argparse
from pathlib import Path
from typing import List


def find_image_skill_path() -> Path:
    """查找 generating-article-images skill 路径（优先项目内）"""
    # 从当前脚本位置定位项目
    current_skill = Path(__file__).parent.parent  # generating-articles-from-docs
    project_skills = current_skill.parent  # skills/ 目录

    possible_paths = [
        # 优先：项目内的 wechat-workflow/generating-article-images
        project_skills / 'wechat-workflow' / 'generating-article-images',
        # 回退：全局技能
        Path.home() / '.claude' / 'skills' / 'generating-article-images',
        Path.home() / '.claude' / 'skills' / 'wechat-workflow' / 'generating-article-images',
    ]

    for path in possible_paths:
        if path.exists() and (path / 'scripts' / 'generate_images.py').exists():
            return path

    return None


def extract_image_prompts(article_path: Path) -> List[dict]:
    """
    从文章中提取 image-prompt 代码块

    Args:
        article_path: 文章文件路径

    Returns:
        图片提示词列表
    """
    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 匹配 ```image-prompt 代码块
    pattern = r'```image-prompt\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)

    prompts = []

    for i, match in enumerate(matches):
        prompt_data = {'raw': match, 'index': i}

        lines = match.strip().split('\n')
        for line in lines:
            if line.startswith('图片路径：'):
                prompt_data['image_path'] = line.replace('图片路径：', '').strip()
            elif line.startswith('Prompt (英文):'):
                # 收集英文提示词
                prompt_lines = []
                for j in range(i + 1, len(lines)):
                    next_line = lines[j].strip()
                    if next_line.startswith('中文释义：') or next_line.startswith('Technical:') or not next_line:
                        break
                    if next_line and next_line not in ['Subject:', 'Details:']:
                        prompt_lines.append(next_line)
                prompt_data['prompt_english'] = '\n'.join(prompt_lines).strip()

        if 'image_path' in prompt_data:
            prompts.append(prompt_data)

    return prompts


def generate_images(article_path: Path, skill_path: Path) -> bool:
    """
    调用 generating-article-images skill 生成图片

    Args:
        article_path: 文章文件路径
        skill_path: skill 路径

    Returns:
        是否成功
    """
    script_path = skill_path / 'scripts' / 'generate_images.py'

    if not script_path.exists():
        print(f"❌ 找不到图片生成脚本: {script_path}")
        return False

    # 构建输出目录（img/ 相对于文章所在目录）
    article_dir = article_path.parent
    img_dir = article_dir / 'img'

    try:
        cmd = [
            sys.executable,
            str(script_path),
            '--input', str(article_path),
            '--config', str(skill_path / 'scripts' / 'config.yaml')
        ]

        print(f"   执行: python3 generate_images.py --input {article_path.name}")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(script_path.parent),
            timeout=600  # 10分钟超时
        )

        if result.returncode == 0:
            # 检查是否生成了图片
            if img_dir.exists():
                images = list(img_dir.glob('*.png'))
                print(f"   ✅ 生成了 {len(images)} 张图片")
                for img in images:
                    print(f"      - {img.name}")
            else:
                print(f"   ⚠️  脚本执行成功，但未找到生成的图片")
            return True
        else:
            print(f"   ❌ 图片生成失败: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("   ❌ 图片生成超时")
        return False
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='自动生成文章配图',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--article', '-a',
        required=True,
        help='文章文件路径'
    )

    parser.add_argument(
        '--skill-path',
        default=None,
        help='generating-article-images skill 路径'
    )

    parser.add_argument(
        '--check-only',
        action='store_true',
        help='只检查图片提示词，不生成'
    )

    args = parser.parse_args()

    article_path = Path(args.article).expanduser().resolve()

    if not article_path.exists():
        print(f"❌ 文章不存在: {article_path}")
        return 1

    print(f"\n{'='*60}")
    print(f"📸 图片生成器")
    print(f"{'='*60}")
    print(f"\n文章: {article_path}")

    # 查找 skill
    skill_path = Path(args.skill_path) if args.skill_path else find_image_skill_path()

    if not skill_path:
        print("❌ 未找到 generating-article-images skill")
        print("\n💡 请安装 skill 或指定路径:")
        print("   --skill-path /path/to/generating-article-images")
        return 1

    print(f"Skill 路径: {skill_path}")

    # 提取图片提示词
    prompts = extract_image_prompts(article_path)

    if not prompts:
        print("\n⚠️  文章中没有找到 image-prompt 代码块")
        print("💡 提示: 文章中需要包含以下格式的代码块:")
        print('''
```image-prompt
用途：封面图
工具：Gemini 3.1 Flash Image Preview
图片路径：./img/cover.png
Prompt (英文):
Subject: 封面图描述
Details:
- 风格1
- 风格2
 Technical: 4K, cinematic lighting --ar 16:9
```
''')
        return 0

    print(f"\n📋 找到 {len(prompts)} 个图片提示词:")
    for p in prompts:
        print(f"   - {p.get('image_path', '未命名')}")

    if args.check_only:
        return 0

    # 生成图片
    print(f"\n⏳ 开始生成图片...\n")

    success = generate_images(article_path, skill_path)

    print(f"\n{'='*60}")
    if success:
        print("✅ 图片生成完成")
    else:
        print("❌ 图片生成失败")

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
