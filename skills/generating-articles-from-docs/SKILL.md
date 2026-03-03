---
name: generating-articles-from-docs
description: Generate articles from uploaded documents using NotebookLM analysis. Upload PDFs/Markdown/text files, analyze content, and generate structured articles with images. Integrates with NotebookLM for source-grounded content generation and generating-article-images for image creation.
---

# Generating Articles From Documents

从上传的文档生成系列文章，使用 NotebookLM 进行内容分析，生成结构化文章并配图。

## 工作流程

```
文档上传 → NotebookLM分析 → 文章规划 → 内容生成 → 图片生成 → 最终输出
```

## 核心功能

1. **文档上传**: 支持 PDF、Markdown、纯文本批量上传
2. **内容分析**: 调用 NotebookLM 进行深度分析
3. **文章规划**: 根据用户需求生成文章大纲和数量
4. **内容生成**: 基于分析结果生成文章草稿
5. **图片生成**: 自动生成配图（集成 generating-article-images skill）

## 何时使用

- 用户说"根据这些文档生成文章"
- 用户说"分析这个PDF并写几篇文章"
- 用户说"从文档中提取内容生成系列文章"
- 用户提供文档路径或URL

## 命令使用

### 文档上传与分析
```bash
python scripts/run.py upload.py --source ./documents --name "知识库"
```

### 生成文章规划
```bash
python scripts/run.py planner.py --source "知识库" --count 3 --topic "AI技术趋势"
```

### 生成文章内容
```bash
python scripts/run.py generate.py --plan ./output/plan.json
```

### 完整工作流
```bash
python scripts/run.py workflow.py \
    --source ./documents \
    --count 3 \
    --topic "AI技术趋势" \
    --output ./output
```

## 配置文件

配置位于 `config.yaml`：
- `notebooklm`: NotebookLM 相关配置
- `generation`: 文章生成参数
- `images`: 图片生成配置
