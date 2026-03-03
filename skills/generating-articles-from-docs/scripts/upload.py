#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档上传模块 - 扫描并处理上传的文档

用法:
    python scripts/run.py upload.py --source ./documents --name "知识库"
"""

import os
import sys
import argparse
import shutil
from pathlib import Path
from typing import List, Dict
import hashlib


SUPPORTED_FORMATS = {
    '.pdf', '.md', '.txt', '.docx', '.markdown', '.rst'
}


def scan_directory(source_dir: Path, recursive: bool = True) -> List[Path]:
    """
    扫描目录查找支持的文档

    Args:
        source_dir: 源目录路径
        recursive: 是否递归扫描子目录

    Returns:
        找到的文档路径列表
    """
    documents = []

    if recursive:
        for ext in SUPPORTED_FORMATS:
            documents.extend(source_dir.rglob(f'*{ext}'))
    else:
        for ext in SUPPORTED_FORMATS:
            documents.extend(source_dir.glob(f'*{ext}'))

    return sorted(documents)


def get_file_hash(filepath: Path) -> str:
    """计算文件的 SHA256 哈希值"""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()[:16]


def copy_documents(documents: List[Path], target_dir: Path, name: str) -> Dict:
    """
    复制文档到目标目录

    Args:
        documents: 文档路径列表
        target_dir: 目标目录
        name: 知识库名称

    Returns:
        处理结果统计
    """
    # 创建目标目录
    knowledge_dir = target_dir / name
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    results = {
        'success': [],
        'skipped': [],
        'errors': []
    }

    # 创建索引文件
    index_file = knowledge_dir / 'index.txt'

    for doc in documents:
        try:
            # 计算文件哈希避免重复
            file_hash = get_file_hash(doc)
            dest_name = f"{file_hash}_{doc.name}"
            dest_path = knowledge_dir / dest_name

            # 复制文件
            shutil.copy2(doc, dest_path)

            results['success'].append({
                'source': str(doc),
                'dest': str(dest_path),
                'size': doc.stat().st_size,
                'hash': file_hash
            })

            print(f"✅ {doc.name} → {dest_name}")

        except Exception as e:
            results['errors'].append({
                'file': str(doc),
                'error': str(e)
            })
            print(f"❌ {doc.name}: {e}")

    # 写入索引
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(f"# 文档索引: {name}\n\n")
        for item in results['success']:
            f.write(f"- {item['source']}\n")
            f.write(f"  → {item['dest']}\n")
            f.write(f"  大小: {item['size']:,} bytes\n\n")

    return results


def main():
    parser = argparse.ArgumentParser(
        description='上传文档到知识库',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--source', '-s',
        required=True,
        help='源文档目录路径'
    )

    parser.add_argument(
        '--name', '-n',
        required=True,
        help='知识库名称'
    )

    parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        default=True,
        help='递归扫描子目录 (默认: True)'
    )

    parser.add_argument(
        '--output', '-o',
        default=None,
        help='输出目录 (默认: ./data)'
    )

    args = parser.parse_args()

    # 路径处理
    source_dir = Path(args.source).expanduser().resolve()

    if args.output:
        skill_dir = Path(args.output)
    else:
        skill_dir = Path(__file__).parent.parent

    target_dir = skill_dir / 'data'

    # 验证源目录
    if not source_dir.exists():
        print(f"❌ 源目录不存在: {source_dir}")
        return 1

    if not source_dir.is_dir():
        print(f"❌ 源路径不是目录: {source_dir}")
        return 1

    print(f"\n{'='*60}")
    print(f"📁 扫描目录: {source_dir}")
    print(f"{'='*60}\n")

    # 扫描文档
    documents = scan_directory(source_dir, args.recursive)

    if not documents:
        print("⚠️  未找到支持的文档")
        print(f"支持的格式: {', '.join(SUPPORTED_FORMATS)}")
        return 0

    print(f"📋 找到 {len(documents)} 个文档:\n")
    for doc in documents:
        size = doc.stat().st_size
        size_mb = size / 1024 / 1024
        print(f"  - {doc.relative_to(source_dir)} ({size_mb:.2f} MB)")

    print(f"\n{'='*60}")
    print(f"📦 复制到知识库: {args.name}")
    print(f"{'='*60}\n")

    # 复制文档
    results = copy_documents(documents, target_dir, args.name)

    # 输出结果
    print(f"\n{'='*60}")
    print(f"✅ 处理完成!")
    print(f"{'='*60}")
    print(f"成功: {len(results['success'])}")
    print(f"跳过: {len(results['skipped'])}")
    print(f"错误: {len(results['errors'])}")
    print(f"\n知识库路径: {target_dir / args.name}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
