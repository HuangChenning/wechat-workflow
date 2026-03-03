---
name: using-wechat-workflow
description: Use when starting any WeChat Official Account content creation task. Provides overview of available skills and guides users to the appropriate skill for their needs. Includes quick start guide, common workflows, and skill dependency diagram.
---

# Using WeChat Workflow

Welcome to the **wechat-workflow** package - a comprehensive skill collection for creating professional content for WeChat Official Accounts (微信公众号).

## Available Skills

This package provides 5 specialized skills for your WeChat content creation workflow:

| Skill | Purpose | Best For |
|-------|---------|----------|
| `polishing-content` | Enhance technical articles with literary techniques and image prompts | Making dry technical content more engaging |
| `reviewing-technical-accuracy` | Perform comprehensive technical audit using WebSearch | Validating claims before publication |
| `generating-article-images` | Generate images from prompts using Gemini 3.1 Flash API | Auto-generating article images from prompts |
| `converting-to-wechat` | Convert Markdown to WeChat HTML with configurable styles (6 presets) | Automated bulk conversion |
| `extracting-wechat-styles` | Extract styles from HTML templates (e.g., mdnice) | Creating custom style presets |

## Quick Start Guide

### For New Articles

If you're starting with a rough draft or technical content:

1. **Polish your content** first (adds image prompts and candidate titles)
   ```
   Please polish my article at /path/to/article.md
   ```

2. **Review for technical accuracy** (recommended for technical content)
   ```
   Please review the technical accuracy of /path/to/article.md
   ```

3. **Generate images from prompts** (new step!)
   ```bash
   python3 skills/wechat-workflow/generating-article-images/scripts/generate_images.py \
       --input "/path/to/article.md"
   ```

4. **Convert to WeChat format**
   ```bash
   python3 skills/wechat-workflow/converting-to-wechat/scripts/convert.py \
       --input "/path/to/article.md"
   ```

### For Existing Markdown Articles

If you already have well-written Markdown articles:

- **Direct conversion**: Use `converting-to-wechat` for automated conversion
- **With image generation**: Run `generating-article-images` first if your article has image prompts

### For Custom Styles

If you want to use a style from mdnice or other platforms:

1. **Extract the style**
   ```bash
   python3 skills/wechat-workflow/extracting-wechat-styles/scripts/generate_style.py \
       --input exported.html --name my-custom-style
   ```

2. **Use the extracted style** in your conversion
   ```bash
   python3 skills/wechat-workflow/converting-to-wechat/scripts/convert.py \
       --input article.md \
       --style skills/wechat-workflow/converting-to-wechat/styles/my-custom-style.yaml
   ```

## Common Workflows

### Workflow 1: Technical Article Publication (Recommended)

**Use this workflow for technical blog posts, tutorials, or documentation**

```
[Draft Article]
       ↓
[polishing-content]     # Add literary techniques & image prompts
       ↓
[reviewing-technical-accuracy]  # Validate technical claims
       ↓
[generating-article-images]     # ✨ Generate images from prompts
       ↓
[converting-to-wechat]  # Convert to WeChat HTML
       ↓
[Published to WeChat]
```

**Steps:**
1. Use `polishing-content` to enhance readability with literary techniques and add image generation prompts
2. Use `reviewing-technical-accuracy` to verify all technical claims
3. Use `generating-article-images` to generate actual images from the prompts
4. Use `converting-to-wechat` to convert the validated article to WeChat HTML

### Workflow 2: Bulk Article Conversion

**Use this workflow when converting multiple articles at once**

```bash
# Generate images for all articles in a directory
for file in /path/to/articles/*.md; do
    python3 skills/wechat-workflow/generating-article-images/scripts/generate_images.py \
        --input "$file"
done

# Convert all Markdown files in a directory
python3 skills/wechat-workflow/converting-to-wechat/scripts/convert.py \
    --input "/path/to/articles/"
```

### Workflow 3: Custom Style Creation

**Use this workflow to create your own WeChat style presets**

```
[HTML Template]
       ↓
[extracting-wechat-styles]  # Extract YAML style
       ↓
[converting-to-wechat with custom style]  # Use new style
```

**Steps:**
1. Export your article from mdnice or another platform as HTML
2. Use `extracting-wechat-styles` to create a YAML style file
3. Use the new style with `converting-to-wechat`

### Workflow 4: Regenerate Specific Images

**Use this workflow when you want to regenerate certain images**

```bash
# Regenerate a specific image
python3 skills/wechat-workflow/generating-article-images/scripts/generate_images.py \
    --input "article.md" \
    --filter "01-oracle-architecture.png"

# Regenerate multiple images matching pattern
python3 skills/wechat-workflow/generating-article-images/scripts/generate_images.py \
    --input "article.md" \
    --filter "01-*.png"
```

## Skill Dependency Diagram

```
                        ┌─────────────────────────┐
                        │  using-wechat-workflow  │
                        │    (This Overview)      │
                        └───────────┬─────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ↓                           ↓                           ↓
┌───────────────────┐    ┌───────────────────┐    ┌───────────────────┐
│ polishing-content │    │ extracting-wechat │    │ reviewing-tech-   │
│                   │    │     -styles       │    │ nical-accuracy    │
└─────────┬─────────┘    └─────────┬─────────┘    └─────────┬─────────┘
          │                       │                       │
          └───────────┬───────────┘                       │
                      ↓                                   │
          ┌───────────────────────┐                       │
          │ generating-article-   │                       │
          │     images            │                       │
          └───────────┬───────────┘                       │
                      ↓                                   │
          ┌───────────────────────┐    ┌───────────────────┐
          │ converting-to-wechat │←───│                   │
          └───────────────────────┘    └───────────────────┘
```

## Choosing the Right Skill

### When to use `polishing-content`:
- Your article feels dry or lacks engagement
- You want to add visual elements with image prompts
- You need to improve readability while maintaining technical accuracy
- You want alternative high-impact titles
- **Note**: Candidate titles are now inserted at the beginning of the article

### When to use `reviewing-technical-accuracy`:
- Publishing technical content with code, commands, or version-specific features
- You need to verify claims against official documentation
- You want to catch factual errors before publication

### When to use `generating-article-images`:
- Your article contains ` ```image-prompt ` code blocks from `polishing-content`
- You want to automatically generate images instead of manually creating them
- You need to regenerate specific images
- You want to keep a backup of all image prompts

### When to use `converting-to-wechat`:
- You have Markdown files ready for publication
- You need to process multiple articles efficiently
- You want automatic image upload to Aliyun OSS
- You prefer automated over manual formatting
- You need v3.0 professional styling (use `wechat-v3-professional.yaml` preset)

### When to use `extracting-wechat-styles`:
- You found a style on mdnice that you want to reuse
- You have HTML templates with custom styling
- You want to create a consistent style library

## Installation

Before using any skill in this package, install the required dependencies:

```bash
# For converting-to-wechat (includes most dependencies)
pip3 install -r skills/wechat-workflow/converting-to-wechat/scripts/requirements.txt

# For generating-article-images (new!)
pip3 install -r skills/wechat-workflow/generating-article-images/scripts/requirements.txt

# For extracting-wechat-styles (if not already installed)
pip3 install beautifulsoup4 pyyaml
```

## Configuration

### generating-article-images Configuration

The `generating-article-images` skill requires API configuration:

```bash
# Copy the example config
cd skills/wechat-workflow/generating-article-images/scripts
cp config.example.yaml config.yaml

# Edit config.yaml and add your Gemini API key
# apis.gemini.api_key: "YOUR_GEMINI_API_KEY"
```

**Supported APIs:**
- Google Gemini 3.1 Flash Image Preview (default)
- OpenAI DALL-E 3 (optional)
- Flux (optional)
- Stable Diffusion (optional)

### Default Configuration

The `converting-to-wechat` skill uses a default configuration file at:
```
skills/wechat-workflow/converting-to-wechat/convert.cfg
```

Edit this file to set your preferred:
- Default style preset
- OSS credentials location
- Default image upload behavior

### Aliyun OSS Setup

To enable automatic image upload, configure your OSS credentials:

```bash
# Copy the example config
cp skills/wechat-workflow/converting-to-wechat/config-example.yaml \
   skills/wechat-workflow/converting-to-wechat/config.yaml

# Edit with your credentials
# (This file is gitignored for security)
```

## Style Library

Pre-configured style presets are available in:
```
skills/wechat-workflow/converting-to-wechat/styles/
```

Available presets:
- `mdnice-test.yaml` - Warm orange, modern layout
- `wechat-professional-blue.yaml` - Professional WeChat brand blue
- `wechat-classic.yaml` - Classic deep blue-gray
- `wechat-ios-blue.yaml` - iOS system blue
- `wechat-minimal-dark.yaml` - Minimalist dark theme
- `wechat-v3-professional.yaml` - **v3.0 professional** (no emojis, solid colors, deep green + warm orange)

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Images not displaying | Ensure OSS credentials are configured and upload is enabled |
| Formatting looks wrong in WeChat editor | Copy the entire HTML content (Ctrl+A / Cmd+A) before pasting |
| Code blocks lose styling | The script uses `<section>` tags to preserve styles in WeChat |
| List punctuation breaks to new line | This is automatically fixed by the script |
| Image generation fails | Check your Gemini API key and quota in config.yaml |
| "未找到图片提示词" error | Ensure article was polished with `polishing-content` first |

## Related Skills

- **All skills in this package** are designed to work together as a complete workflow
- Skills can be used independently or in combination depending on your needs
- **New**: `generating-article-images` integrates seamlessly with `polishing-content` output

## Additional Resources

- For WeChat editor compatibility notes, see the `converting-to-wechat` skill documentation
- For image generation prompts format, see the `polishing-content` skill documentation
- For v3.0 styling specifications, use the `wechat-v3-professional.yaml` style preset
- For Gemini API documentation, see [Google AI Studio](https://ai.google.dev/gemini-api/docs)
