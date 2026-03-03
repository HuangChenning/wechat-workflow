#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generating-article-images 图片生成脚本

功能：
1. 解析文章中的图片提示词（```image-prompt 代码块）
2. 调用图片生成 API（Gemini 3.1 Flash Image Preview）
3. 生成图片到 img/ 文件夹
4. 替换文章中的提示词为图片链接
5. 保留原始提示词到 image-prompts.md
6. 支持按文件名过滤重新生成

使用方法：
    # 生成所有图片
    python3 generate_images.py --input article.md

    # 只生成特定图片
    python3 generate_images.py --input article.md --filter "01-*.png"

    # 使用自定义配置
    python3 generate_images.py --input article.md --config config.yaml
"""

import os
import re
import sys
import yaml
import requests
import argparse
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional, Tuple

from google import genai
from google.genai import types

# ── 配置 ─────────────────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "config.yaml"
CONFIG_EXAMPLE = SCRIPT_DIR / "config.example.yaml"

# ── 图片提示词解析 ─────────────────────────────────────────────────────────────────────

def parse_image_prompts(content: str) -> List[Dict]:
    """
    解析文章中的图片提示词代码块

    Args:
        content: 文章内容（markdown 格式）

    Returns:
        提示词列表，每个包含：purpose, tool, image_path, prompt, chinese_definition
    """
    # 匹配 ```image-prompt 代码块
    pattern = r'```image-prompt\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)

    prompts = []
    for match in matches:
        prompt_data = {
            'raw': match.strip(),
            'purpose': '',
            'tool': '',
            'image_path': '',
            'prompt_english': '',
            'chinese_definition': ''
        }

        lines = match.strip().split('\n')

        # 解析各个字段
        for i, line in enumerate(lines):
            if line.startswith('用途：'):
                prompt_data['purpose'] = line.replace('用途：', '').strip()
            elif line.startswith('工具：'):
                prompt_data['tool'] = line.replace('工具：', '').strip()
            elif line.startswith('图片路径：'):
                prompt_data['image_path'] = line.replace('图片路径：', '').strip()
            elif line.startswith('Prompt (英文):'):
                # 收集英文提示词内容
                english_lines = []
                for j in range(i + 1, len(lines)):
                    next_line = lines[j].strip()
                    if next_line.startswith('中文释义：'):
                        break
                    if next_line and not next_line.startswith('Subject:') and not next_line.startswith('Details:'):
                        english_lines.append(next_line)

                prompt_data['prompt_english'] = '\n'.join(english_lines).strip()
                break
            elif line.startswith('中文释义：'):
                prompt_data['chinese_definition'] = line.replace('中文释义：', '').strip()

        # 提取 Subject 和 Details
        subject_match = re.search(r'Subject:\s*(.+)', prompt_data['prompt_english'])
        if subject_match:
            prompt_data['subject'] = subject_match.group(1).strip()

        details = []
        detail_match = re.search(r'Details:.*', prompt_data['prompt_english'], re.DOTALL)
        if detail_match:
            detail_lines = re.findall(r'-\s*(.+)', prompt_data['prompt_english'])
            details = [d.strip() for d in detail_lines]
        prompt_data['details'] = details

        # 提取 Technical 参数
        technical_match = re.search(r'Technical:\s*(.+)', prompt_data['prompt_english'])
        if technical_match:
            prompt_data['technical'] = technical_match.group(1).strip()
        else:
            prompt_data['technical'] = ''

        if prompt_data['image_path']:
            prompts.append(prompt_data)

    return prompts


def extract_generation_params(prompt_data: Dict, config: Dict) -> Dict:
    """
    从提示词数据中提取图片生成参数

    Args:
        prompt_data: 解析后的提示词数据
        config: 配置信息

    Returns:
        生成参数（包括 subject, details, size, aspect_ratio 等）
    """
    params = {
        'subject': prompt_data.get('subject', ''),
        'details': prompt_data.get('details', []),
        'purpose': prompt_data.get('purpose', ''),
        'size': config['image']['default_size'],
        'aspect_ratio': config['image']['default_aspect_ratio'],
        'quality': config['image']['quality']
    }

    # 从 Technical 参数中提取尺寸和宽高比
    technical = prompt_data.get('technical', '')

    # 解析 --ar 参数（宽高比）
    ar_match = re.search(r'--ar\s+([^\s]+)', technical)
    if ar_match:
        params['aspect_ratio'] = ar_match.group(1)

    # 解析尺寸参数
    if '4K' in technical or '3840x' in technical:
        params['size'] = '4K'
    elif '2K' in technical or '2048x' in technical:
        params['size'] = '2K'
    elif '1K' in technical or '1024x' in technical:
        params['size'] = '1K'
    elif '512px' in technical or '512x' in technical:
        params['size'] = '512px'

    return params


# ── API 调用 ─────────────────────────────────────────────────────────────────────────────

def get_gemini_client(api_config: Dict) -> genai.Client:
    """
    Initialize and return a google-genai client.
    Supports both config file API key and environment variable.
    """
    api_key = api_config.get('api_key')
    if api_key and api_key != "YOUR_GEMINI_API_KEY":
        return genai.Client(api_key=api_key)
    return genai.Client()  # Falls back to GEMINI_API_KEY env var


def generate_image_with_gemini(prompt_text: str, config: Dict, api_config: Dict) -> bytes:
    """
    使用 Gemini 3.1 Flash Image Preview API 生成图片 (Official SDK)

    Args:
        prompt_text: 图片生成提示词
        config: 配置信息
        api_config: API 配置

    Returns:
        图片二进制数据
    """
    model = api_config.get('model', 'gemini-3.1-flash-image-preview')

    # Initialize client
    client = get_gemini_client(api_config)

    # Build generation config
    generation_config = types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio=config['image']['default_aspect_ratio'],
        )
    )

    try:
        # Call the SDK
        response = client.models.generate_content(
            model=model,
            contents=prompt_text,
            config=generation_config,
        )

        # Extract image data from response
        for part in response.parts:
            if part.inline_data:
                img = part.as_image()
                if img and hasattr(img, 'image_bytes'):
                    return img.image_bytes
                # Fallback: access inline_data directly
                return part.inline_data.data

        raise Exception("未在响应中找到图片数据")

    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)

        # Enhanced error handling
        if "API key" in error_msg or "401" in error_msg:
            raise Exception(f"Gemini API 认证失败：请检查 API Key 配置。{error_msg}")
        elif "quota" in error_msg.lower() or "429" in error_msg:
            raise Exception(f"Gemini API 配额不足：{error_msg}")
        else:
            raise Exception(f"Gemini API 调用失败 [{error_type}]: {error_msg}")


def generate_image(prompt_data: Dict, config: Dict) -> Tuple[bytes, str]:
    """
    生成单张图片（支持重试）

    Args:
        prompt_data: 提示词数据
        config: 配置信息

    Returns:
        (图片数据, 文件名)
    """
    # 获取 API 配置
    default_api = config.get('default_api', 'gemini')
    api_config = config['apis'].get(default_api, {})

    if not api_config.get('enabled', False):
        raise Exception(f"API {default_api} 未启用或配置不存在")

    # 获取重试次数
    max_retries = api_config.get('max_retries', 3)

    # 提取生成参数
    params = extract_generation_params(prompt_data, config)

    # 构建提示词
    prompt_parts = [params['subject']]
    prompt_parts.extend([f"- {detail}" for detail in params['details']])

    if params.get('purpose'):
        prompt_parts.insert(0, f"用途：{params['purpose']}")

    prompt_text = '\n'.join(prompt_parts)

    # 提取文件名
    image_path = prompt_data['image_path']
    if './img/' in image_path:
        filename = image_path.split('./img/')[-1]
    else:
        filename = Path(image_path).name

    # 带重试机制的图片生成
    import time
    last_error = None

    for attempt in range(max_retries):
        try:
            # 调用 API 生成图片
            if default_api == 'gemini':
                image_data = generate_image_with_gemini(prompt_text, config, api_config)
            else:
                raise NotImplementedError(f"API {default_api} 尚未实现")

            # 成功生成，返回结果
            if attempt > 0:
                print(f"  ✅ 第 {attempt + 1} 次尝试成功")

            return image_data, filename

        except Exception as e:
            last_error = e
            error_type = type(e).__name__
            error_msg = str(e)

            # 判断是否应该重试
            should_retry = True
            if "API key" in error_msg or "401" in error_msg:
                # 认证错误不重试
                should_retry = False
            elif attempt < max_retries - 1:
                # 还有重试机会
                wait_time = (attempt + 1) * 2  # 指数退避：2秒、4秒、6秒
                print(f"  ⚠️  第 {attempt + 1} 次尝试失败：{error_type}")
                print(f"  🔄 {wait_time} 秒后重试...")
                time.sleep(wait_time)
            else:
                # 最后一次尝试也失败了
                should_retry = False

            if not should_retry:
                break

    # 所有重试都失败，抛出最后的错误
    raise last_error


# ── 文件操作 ─────────────────────────────────────────────────────────────────────────────

def save_image(image_data: bytes, filepath: Path) -> None:
    """
    保存图片到文件

    Args:
        image_data: 图片二进制数据
        filepath: 目标文件路径
    """
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'wb') as f:
        f.write(image_data)


def replace_prompts_with_images(content: str, prompts: List[Dict]) -> str:
    """
    将文章中的图片提示词替换为图片链接

    Args:
        content: 文章内容
        prompts: 提示词列表

    Returns:
        替换后的文章内容
    """
    result = content

    for prompt_data in prompts:
        # 找到并替换提示词代码块
        pattern = r'```image-prompt\n' + re.escape(prompt_data['raw']) + r'\n```'

        # 构建替换的图片 markdown
        image_path = prompt_data['image_path']
        purpose = prompt_data.get('purpose', '图片')

        replacement = f'![{purpose}]({image_path})'

        result = re.sub(pattern, replacement, result, flags=re.DOTALL)

    return result


def create_image_prompts_backup(article_path: Path, prompts: List[Dict], config: Dict) -> None:
    """
    创建图片提示词备份文件

    Args:
        article_path: 文章路径
        prompts: 提示词列表
        config: 配置信息
    """
    if not config['backup']['enabled']:
        return

    article_dir = article_path.parent
    backup_filename = config['backup']['filename']
    backup_path = article_dir / backup_filename

    # 检查是否已存在备份文件
    existing_content = ''
    if backup_path.exists():
        with open(backup_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()

    # 构建备份内容
    backup_content = existing_content
    if backup_content and not backup_content.endswith('\n'):
        backup_content += '\n\n'

    backup_content += f'<!-- 备份时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} -->\n'
    backup_content += f'<!-- 文章：{article_path.name} -->\n\n'

    for prompt_data in prompts:
        backup_content += f'## {Path(prompt_data["image_path"]).name}\n\n'
        backup_content += f'**用途**：{prompt_data.get("purpose", "")}\n'
        backup_content += f'**工具**：{prompt_data.get("tool", "")}\n'
        backup_content += f'**图片路径**：{prompt_data["image_path"]}\n\n'
        backup_content += '### 原始提示词\n\n'
        backup_content += f'```\n{prompt_data["raw"]}\n```\n\n'

        # 如果启用了包含图片且图片存在，添加图片预览
        if config['backup']['include_images']:
            full_image_path = article_dir / prompt_data['image_path']
            if full_image_path.exists():
                backup_content += f'### 生成结果\n\n'
                backup_content += f'![{prompt_data.get("purpose", "图片")}]({prompt_data["image_path"]})\n\n'

        backup_content += '------\n\n'

    # 写入备份文件
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(backup_content)


# ── 主流程 ─────────────────────────────────────────────────────────────────────────────

def process_article(article_path: Path, config: Dict, filter_pattern: str = None) -> Dict:
    """
    处理单篇文章：生成图片并替换

    Args:
        article_path: 文章路径
        config: 配置信息
        filter_pattern: 文件名过滤模式（可选）

    Returns:
        处理结果统计
    """
    print(f"\n{'='*60}")
    print(f"处理文章：{article_path}")
    print(f"{'='*60}")

    # 读取文章内容
    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 解析图片提示词
    prompts = parse_image_prompts(content)

    if not prompts:
        print("❌ 未找到图片提示词")
        return {'total': 0, 'success': 0, 'failed': 0, 'skipped': 0}

    # 过滤提示词
    if filter_pattern:
        import fnmatch
        filtered_prompts = []
        for prompt in prompts:
            filename = Path(prompt['image_path']).name
            if fnmatch.fnmatch(filename, filter_pattern):
                filtered_prompts.append(prompt)
        prompts = filtered_prompts

    print(f"📋 找到 {len(prompts)} 个图片提示词")

    # 统计
    stats = {'total': len(prompts), 'success': 0, 'failed': 0, 'skipped': 0}

    # 并发生成图片
    concurrent_limit = config['apis'][config['default_api']]['concurrent_limit']

    with ThreadPoolExecutor(max_workers=concurrent_limit) as executor:
        future_to_prompt = {}

        for prompt_data in prompts:
            future = executor.submit(generate_image, prompt_data, config)
            future_to_prompt[future] = prompt_data

        for future in as_completed(future_to_prompt):
            prompt_data = future_to_prompt[future]
            image_path = prompt_data['image_path']

            try:
                image_data, filename = future.result()

                # 保存图片
                article_dir = article_path.parent
                full_image_path = article_dir / image_path
                save_image(image_data, full_image_path)

                print(f"✅ 生成成功：{filename}")
                stats['success'] += 1

            except Exception as e:
                print(f"❌ 生成失败：{Path(image_path).name} - {str(e)}")
                stats['failed'] += 1

    # 只要有成功的图片，就替换文章中的提示词（部分成功也替换）
    if stats['success'] > 0:
        new_content = replace_prompts_with_images(content, prompts)

        # 备份文章（覆盖）
        with open(article_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        # 创建提示词备份
        create_image_prompts_backup(article_path, prompts, config)

        if stats['failed'] > 0:
            print(f"\n⚠️ 部分图片生成失败（{stats['failed']}/{stats['total']}），成功的图片已插入")
        else:
            print(f"\n🎉 处理完成！{stats['success']} 张图片已生成并插入")
    else:
        print(f"\n❌ 所有图片生成失败，未修改文章")

    return stats


# ── 配置文件加载 ─────────────────────────────────────────────────────────────────────

def load_config(config_path: Optional[Path] = None) -> Dict:
    """
    加载配置文件

    Args:
        config_path: 配置文件路径（可选）

    Returns:
        配置字典
    """
    if config_path is None:
        config_path = CONFIG_FILE

    if not config_path.exists():
        # 尝试使用示例配置
        if CONFIG_EXAMPLE.exists():
            print(f"⚠️ 配置文件不存在，使用示例配置：{CONFIG_EXAMPLE}")
            config_path = CONFIG_EXAMPLE
        else:
            raise FileNotFoundError(f"配置文件不存在：{CONFIG_FILE}")

    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    return config


# ── 主函数 ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='generating-article-images - 从图片提示词生成图片',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例：
  # 生成所有图片
  python3 generate_images.py --input article.md

  # 只生成特定图片
  python3 generate_images.py --input article.md --filter "01-*.png"

  # 使用自定义配置
  python3 generate_images.py --input article.md --config /path/to/config.yaml
        '''
    )

    parser.add_argument(
        '--input', '-i',
        required=True,
        help='输入的 Markdown 文件路径'
    )

    parser.add_argument(
        '--config', '-c',
        default=None,
        help='配置文件路径（默认：scripts/config.yaml）'
    )

    parser.add_argument(
        '--filter', '-f',
        default=None,
        help='文件名过滤模式（例如：01-*.png）'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细输出'
    )

    args = parser.parse_args()

    # 加载配置
    try:
        config = load_config(Path(args.config) if args.config else None)
    except Exception as e:
        print(f"❌ 加载配置失败：{e}")
        sys.exit(1)

    # 处理文章
    article_path = Path(args.input)

    if not article_path.exists():
        print(f"❌ 文章不存在：{article_path}")
        sys.exit(1)

    stats = process_article(article_path, config, args.filter)

    # 输出统计摘要
    print(f"\n{'='*60}")
    print("📊 图片生成统计")
    print(f"{'='*60}")
    print(f"  总计: {stats['total']} 张")
    print(f"  ✅ 成功: {stats['success']} 张")
    if stats['failed'] > 0:
        print(f"  ❌ 失败: {stats['failed']} 张")
    if stats['skipped'] > 0:
        print(f"  ⏭️  跳过: {stats['skipped']} 张")
    print(f"{'='*60}\n")

    # 返回退出码
    sys.exit(0 if stats['failed'] == 0 else 1)


if __name__ == '__main__':
    main()
