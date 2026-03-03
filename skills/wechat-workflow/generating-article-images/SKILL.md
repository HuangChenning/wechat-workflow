---
name: generating-article-images
description: Use when generating images from image prompts in articles. Parses ```image-prompt code blocks, calls image generation APIs (Google Gemini 2.5 Flash Image Preview), saves images to img/ folder, replaces prompts with image links, and backs up original prompts to image-prompts.md. Supports filtering by filename for regeneration. Integrates with polishing-content workflow.
---

# Generating Article Images

This skill automates the image generation process for WeChat Official Account articles.

## Overview

When you use `polishing-content` to enhance your articles, it inserts image generation prompts in the format:
```image-prompt
```
This skill parses those prompts, generates images using the configured API, and updates your article with the actual image links.

## Workflow

```
[polishing-content]     # 生成图片提示词
       ↓
[generating-article-images]  # 解析提示词 → 生成图片 → 替换链接
       ↓
[converting-to-wechat]  # 转换为微信 HTML
```

## Quick Start

### 1. Installation

```bash
pip3 install -r skills/wechat-workflow/generating-article-images/scripts/requirements.txt
```

### 2. Configuration

Copy the example config and add your API key:

```bash
cd skills/wechat-workflow/generating-article-images/scripts
cp config.example.yaml config.yaml

# 编辑 config.yaml，填入您的 Gemini API Key
# api_key: "YOUR_GEMINI_API_KEY"
```

### 3. Basic Usage

Generate all images from an article:

```bash
python3 skills/wechat-workflow/generating-article-images/scripts/generate_images.py \
    --input "/path/to/article.md"
```

### 4. Regenerate Specific Images

Regenerate only specific images by filename pattern:

```bash
# Regenerate one specific image
python3 skills/wechat-workflow/generating-article-images/scripts/generate_images.py \
    --input "/path/to/article.md" \
    --filter "01-oracle-architecture.png"

# Regenerate multiple images matching pattern
python3 skills/wechat-workflow/generating-article-images/scripts/generate_images.py \
    --input "/path/to/article.md" \
    --filter "01-*.png"
```

## Features

### Image Prompt Format

The skill parses image prompts in this format:

``````image-prompt
用途：Oracle 内存架构演进图
工具：Midjourney / DALL-E 3 / Flux（生成 4K HD 质量图片）
图片路径：./img/01-oracle-memory-architecture.png

Prompt (英文):
Subject: A technical diagram showing Oracle Memory Architecture...
Details:
- Left section: Show SGA with Buffer Cache...
- Right section: Show PGA...
Style: Modern technical infographic...
Colors: Oracle red, blue, gold...
Visual Flow: Left-to-right...
Key Elements: Emphasize new components...
Technical: --ar 16:9 --v 6.0 --quality 2

中文释义：
技术图，展示 Oracle 内存架构从 11g 到 26ai 的演进...
``````

### Automatic Features

1. **Prompt Parsing**: Extracts all image-related information from the prompt block
2. **Parameter Extraction**: Parses size, aspect ratio, and other technical parameters
3. **Concurrent Generation**: Generates multiple images simultaneously (configurable limit)
4. **Auto Replacement**: Replaces prompt blocks with markdown image links
5. **Backup Creation**: Saves all original prompts to `image-prompts.md`

### Backup File Format (image-prompts.md)

```markdown
## 01-oracle-memory-architecture.png

**用途**：Oracle 内存架构演进图
**工具**：Midjourney / DALL-E 3 / Flux
**图片路径**：./img/01-oracle-memory-architecture.png

### 原始提示词

```image-prompt
用途：...
[完整提示词内容]
```

### 生成结果

![Oracle 内存架构演进图](./img/01-oracle-memory-architecture.png)

------
```

## Configuration

### API Support

The skill supports multiple image generation APIs:

| API | Status | Notes |
|-----|--------|-------|
| **Google Gemini 3.1 Flash** | ✅ Primary | Default, high quality |
| OpenAI DALL-E 3 | 🔧 Optional | Configure in config.yaml |
| Flux | 🔧 Optional | Configure in config.yaml |
| Stable Diffusion | 🔧 Optional | Local or cloud |

### Config File Structure

```yaml
# Default API
default_api: gemini

# API configurations
apis:
  gemini:
    enabled: true
    api_key: "YOUR_API_KEY"
    model: "gemini-3.1-flash-image-preview"
    timeout: 120
    concurrent_limit: 3

  openai:
    enabled: false
    # ... config

# Image settings
image:
  default_size: "2K"
  default_aspect_ratio: "16:9"
  output_dir: "img"

# Backup settings
backup:
  enabled: true
  filename: "image-prompts.md"
```

## Supported Parameters

### Image Size
- `512px` - Small, fast
- `1K` - Standard quality
- `2K` - High quality (default)
- `4K` - Ultra high quality

### Aspect Ratio
- `1:1` - Square
- `16:9` - Landscape (default)
- `9:16` - Portrait
- `21:9` - Ultra-wide
- And 10+ more options

### Parameter Extraction from Prompts

The skill automatically extracts parameters from the `Technical:` field:
- `--ar 16:9` → Sets aspect ratio to 16:9
- `4K`, `2K`, `1K` → Sets image size
- `--quality 2` → Sets generation quality

## Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--input` | `-i` | **(Required)** Input Markdown file path |
| `--config` | `-c` | Configuration file path |
| `--filter` | `-f` | Filename filter pattern (e.g., "01-*.png") |
| `--verbose` | `-v` | Show detailed output |

## Error Handling

### If Image Generation Fails

1. Error message is displayed
2. Original article is NOT modified
3. Other images continue to generate
4. Check your API key and quota

### Common Issues

| Problem | Solution |
|---------|----------|
| "API 未启用或配置不存在" | Check config.yaml and ensure the API is enabled |
| "未找到图片提示词" | Ensure article contains ```image-prompt code blocks |
| "生成失败" | Check API key validity, network connection, and quota |
| "图片已存在" | Existing files will be overwritten (add versioning if needed) |

## Related Skills

- **`wechat-workflow:polishing-content`** - Use before to generate image prompts in articles
- **`wechat-workflow:reviewing-technical-accuracy`** - Use before generating images to validate technical content
- **`wechat-workflow:converting-to-wechat`** - Use after generating images to convert to WeChat HTML
- **`wechat-workflow:using-wechat-workflow`** - Package overview and workflow guide

## Best Practices

1. **Order matters**: Use in this order: polish → review → generate images → convert
2. **Test first**: Generate a single image before batch processing
3. **Backup prompts**: Keep `image-prompts.md` for regeneration
4. **Check quota**: Monitor your API usage and costs
5. **Concurrent limit**: Adjust based on your API tier

## Example Workflow

```bash
# 1. Polish article (generates image prompts)
请润色 my-article.md

# 2. Review technical accuracy
请审查 my-article.md 的技术准确性

# 3. Generate images
python3 skills/wechat-workflow/generating-article-images/scripts/generate_images.py \
    --input "my-article.md"

# 4. Convert to WeChat HTML
python3 skills/wechat-workflow/converting-to-wechat/scripts/convert.py \
    --input "my-article.md"
```

## API Information

### Google Gemini 2.5 Flash Image Preview (nano-banana)

- **Model**: `gemini-2.5-flash-image-preview`
- **Documentation**: https://ai.google.dev/gemini-api/docs
- **Pricing**: Blaze pay-as-you-go (~$0.03/image)
- **Requirements**:
  - Google Cloud project with Gemini API enabled
  - Valid API key with Image Generation permission
  - Internet connectivity

### Getting an API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to `config.yaml`
4. Enable the Gemini API for your project

## Troubleshooting

### Debug Mode

```bash
python3 generate_images.py --input article.md --verbose
```

### Check Configuration

```bash
# Validate config file
python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"
```

### Test API Connection

```bash
# Test with a simple prompt first
python3 -c "
from generate_images import generate_image_with_gemini, load_config
config = load_config()
api_config = config['apis']['gemini']
result = generate_image_with_gemini('A red apple', config, api_config)
print(f'Generated {len(result)} bytes')
"
```
