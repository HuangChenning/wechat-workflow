---
name: converting-to-wechat
description: Use when converting Markdown files to WeChat Official Account HTML articles. Supports YAML-configurable styles (5 presets), Aliyun OSS image upload, macOS-style code blocks, and WeChat editor compatibility (using `<section>` instead of `<div>`). Features default config system (convert.cfg) and style preset library. Single file and batch directory modes supported.
---

# Converting to WeChat

**Formerly known as**: `markdown-to-wechat`

将 Markdown 文件转换为微信公众号原生的 HTML 格式，支持全自动样式内联、代码块 macOS 风格渲染以及阿里云 OSS 图片自动上传。

将 Markdown 文件转换为微信公众号原生的 HTML 格式，支持全自动样式内联、代码块 macOS 风格渲染以及阿里云 OSS 图片自动上传。

## 快速开始

### 1. 安装依赖
```bash
pip install -r skills/wechat-workflow/converting-to-wechat/scripts/requirements.txt
```

### 2. 基础使用
脚本会自动读取 `convert.cfg` 中的默认配置，通常只需指定输入文件：
```bash
python3 skills/wechat-workflow/converting-to-wechat/scripts/convert.py --input "Oracle view/第01篇.md"
```

### 3. 命令行参数

| 参数              | 缩写 | 描述                                                      |
| ----------------- | ---- | --------------------------------------------------------- |
| `--input`         | `-i` | **(必选)** 输入的 MD 文件或目录路径                       |
| `--style`         | `-s` | 视觉样式预设文件路径（默认取自 convert.cfg）              |
| `--config`        | `-c` | 本地覆盖配置文件（通常含 OSS 凭据，默认取自 convert.cfg） |
| `--upload-images` |      | 是否上传图片到 OSS（可在 convert.cfg 默认开启）           |
| `--no-upload`     |      | 强制禁用上传（覆盖默认开启状态）                          |
| `--output`        | `-o` | 输出目录（默认为输入目录下的 output/）                    |

---

## 配置体系 (Configuration System)

### 1. 默认参数表：`convert.cfg`
位于 `skills/wechat-workflow/converting-to-wechat/convert.cfg`，定义了不带参数运行时的行为：
```ini
[defaults]
style = skills/wechat-workflow/converting-to-wechat/styles/mdnice-test.yaml
config = skills/wechat-workflow/converting-to-wechat/config.yaml
upload_images = true
```

### 2. 视觉样式库：`styles/`
内置了多种风格预设，可在 `convert.cfg` 或通过 `--style` 切换：
- `mdnice-test.yaml`: 暖橙色，现代排版。
- `wechat-professional-blue.yaml`: 专业微信蓝。
- `wechat-classic.yaml`: 经典深蓝灰。
- `wechat-ios-blue.yaml`: iOS 系统蓝。
- `wechat-minimal-dark.yaml`: 极简深色。

### 3. 本地覆盖与凭据：`config.yaml`
默认配置位于 `skills/wechat-workflow/converting-to-wechat/config.yaml`，用于存放 OSS 凭据等私密信息。
**重要：此文件已加入 .gitignore，不会被提交到 Git。**

如需为特定文章系列配置不同的凭据，可将 `config-example.yaml` 复制到系列目录并重命名：
```bash
cp skills/wechat-workflow/converting-to-wechat/config-example.yaml "Oracle view/config.yaml"
```

```yaml
image:
  upload_to_oss: true
  oss_access_key_id: "..."
  oss_access_key_secret: "..."
  # ... 其他 OSS 配置
```

---

## 核心功能说明

### 代码块渲染
- **macOS 风格**：自动在代码块顶部添加红黄绿圆点装饰栏。
- **语言标签**：自动识别并显示代码语言（如 SQL, Python）。
- **同步背景**：装饰栏颜色与代码块背景色自动同步，视觉统一。

### 图片处理 (OSS Upload)
- **自动检测**：识别 MD 中的本地相对路径图片。
- **幂等上传**：使用 MD5 哈希校验，已上传过的图片会自动跳过，不浪费流量。
- **路径替换**：生成 HTML 时自动将本地路径替换为 OSS 公网 URL。

### 微信兼容性适配 (Compatibility Hacks)
- **标签降级**：优先使用 `<section>` 替代 `<div>`，确保背景色不丢失（编辑器会剔除 `div`）。
- **布局降级**：弃用 `flex`，改用 `inline-block` + `vertical-align` 实现装饰栏对齐。
- **主动包裹**：对列表项（`li`）开头的文字自动包裹 `<section>`，防止编辑器强行拆分导致标点符号（如冒号 `：`）换行。
- **样式冗余**：背景色多重定义（Section/Pre/Code），提升全选复制时的渲染可靠性。

---

## AI 协作流程

当用户请求转换文章时：
1. **检查输入**：确认 MD 文件路径。
2. **确认配置**：默认使用 `skills/wechat-workflow/converting-to-wechat/config.yaml` 和 `convert.cfg` 预设。
3. **执行转换**：
   ```bash
   python3 skills/wechat-workflow/converting-to-wechat/scripts/convert.py --input “<path>”
   ```
4. **交付结果**：告知生成的 HTML 路径，并提醒用户”全选→复制→粘贴”的操作步骤。

---

## 故障排除

| 问题                | 原因                   | 解决方法                                        |
| ------------------- | ---------------------- | ----------------------------------------------- |
| 图片不显示          | 未开启 OSS 上传        | 确保 `upload_images=true` 且凭据有效。          |
| 标点符号掉到下一行  | 微信强行拆分 `li` 内容 | 脚本已实现自动包裹 `section` 解决。             |
| 背景色丢失          | 使用了 `div` 标签      | 检查 YAML 配置，确保主要容器使用 `section`。    |
| 装饰栏错位          | `flex` 被编辑器抹除    | 脚本已改用 `inline-block` 适配。                |
| 无法加载 config.yaml | 路径错误               | 检查 `convert.cfg` 中的 `config` 路径是否正确。 |

## Related Skills

- **`wechat-workflow:extracting-wechat-styles`** - Use to create new style presets from existing HTML templates (e.g., mdnice exports). Output styles are saved to `converting-to-wechat/styles/` directory.
- **`wechat-workflow:polishing-content`** - Use before conversion to enhance articles with literary techniques and image prompts
- **`wechat-workflow:reviewing-technical-accuracy`** - Use before conversion to validate technical claims and accuracy
- **`wechat-workflow:generating-article-images`** - Use before conversion to generate images from image prompts (if article contains prompts)
