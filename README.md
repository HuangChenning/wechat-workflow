# weixin-skills

微信公众号内容创作技能包。

## 包：wechat-workflow

本仓库包含 `wechat-workflow` 包 - 一套用于创建专业微信公众号内容的完整技能集合。

---

## 📋 可用技能概览

| 技能 | 描述 | 使用场景 |
|-------|-------------|----------|
| `polishing-content` | 用16种文学技法和AI图片提示词润色技术文章 | 文章内容枯燥、缺乏吸引力 |
| `reviewing-technical-accuracy` | 使用 WebSearch 进行全面技术审核 | 发布包含代码/命令的技术内容 |
| `generating-article-images` | 使用 Gemini 3.1 Flash API 从提示词生成图片 | 自动生成文章配图 |
| `converting-to-wechat` | 将 Markdown 转换为可配置样式的微信 HTML | 转换 Markdown 文件为微信格式 |
| `extracting-wechat-styles` | 从 HTML 模板提取样式（如 mdnice） | 创建自定义样式预设 |
| `using-wechat-workflow` | 包概览和工作流指南 | 开始任何微信内容创作任务 |

---

## 🚀 快速开始

### 1. 安装依赖

安装核心转换技能的依赖：

```bash
pip3 install -r skills/wechat-workflow/converting-to-wechat/scripts/requirements.txt
```

### 2. 基础使用

最简单的命令使用 `convert.cfg` 中的默认配置：

```bash
# 转换单篇文章
python3 skills/wechat-workflow/converting-to-wechat/scripts/convert.py --input "my-series/article.md"

# 转换整个目录
python3 skills/wechat-workflow/converting-to-wechat/scripts/convert.py --input "my-series/"
```

### 3. 自定义样式

临时使用不同的样式预设：

```bash
python3 skills/wechat-workflow/converting-to-wechat/scripts/convert.py \
    --input "my-series/article.md" \
    --style skills/wechat-workflow/converting-to-wechat/styles/wechat-professional-blue.yaml
```

### 4. 禁用图片上传

本次转换不上传图片：

```bash
python3 skills/wechat-workflow/converting-to-wechat/scripts/convert.py \
    --input "my-series/article.md" \
    --no-upload
```

> [!TIP]
> 转换脚本会在文章文件夹中自动创建 `output/` 目录。在浏览器中打开生成的 HTML，**全选（Cmd+A）→ 复制 → 粘贴**到微信公众号编辑器即可。

---

## 📖 详细技能指南

### 1. polishing-content（文章润色）

**功能特性：**
- 应用16种文学技法（金庸式笔触、历史典故、比喻、悬念等）
- 生成 AI 图片提示词，支持 Midjourney/DALL-E 3/Flux（4K HD 质量）
- 在保持技术准确性的同时优化语言可读性
- 创建 5 个备选的高吸引力标题（插入文章开头）
- 支持单文件和批量处理
- 可配置的润色强度（轻度/标准/深度）

**支持的技术：**
- **数据库**：Oracle、MySQL、PostgreSQL、MongoDB、Redis、Elasticsearch
- **DevOps**：Kubernetes、Docker、Terraform、Ansible、Prometheus
- **AI/LLM**：大语言模型、RAG、向量数据库
- **编程语言**：Python、Java、Go、JavaScript/TypeScript、Rust

**使用示例：**
```
# 单文件润色
请润色 /path/to/article.md

# 批量润色
请润色 /path/to/directory/ 目录下所有的 md 文件

# 带技术验证
请润色 /path/to/article.md，并验证所有代码片段的技术准确性

# 指定技术领域
请润色 /path/to/article.md，这是一篇关于 MySQL 的文章

# 添加图片提示词
请润色 /path/to/article.md，并在适当位置添加图片生成提示词
```

**输出内容：**
- 直接修改文章文件
- 在代码块中生成图片提示词
- 创建 `img/` 目录存放图片
- 生成 5 个备选标题（插入文章开头）
- 批量处理时：生成 `title.md` 封面图片提示词

---

### 2. reviewing-technical-accuracy（技术审核）

**功能特性：**
- 使用 WebSearch 进行全面技术审核
- 验证产品版本和功能可用性
- 检查版本兼容性和废弃功能
- 验证代码语法和命令正确性
- 确保术语使用准确
- 生成结构化报告，包含错误、警告和建议

**审核目标：**
- **概念完整性**（理论正确性）
- **技术准确性**（命令/代码按描述工作）
- **术语准确性**（正确使用标准术语）
- **语言和语义**（拼写、语法、逻辑）

**使用示例：**
```
# 审核单个文件
请审查 /path/to/article.md 的技术准确性

# 批量审核
请验证 /path/to/directory/ 目录下所有文章的技术准确性

# 指定技术
请审查 /path/to/article.md，这是一篇 Oracle 相关的技术文章
```

**输出格式：**
```
## 报告：[文件名]

### 🔴 严重错误（事实/技术）
| 位置 | 错误描述 | 正确事实 | 参考/来源 |

### 🟡 警告（语言/清晰度）
- 第15行：拼写错误 "Oracel" -> "Oracle"

### 🟢 建议
- 考虑为此概念添加图表
```

---

### 3. generating-article-images（图片生成）

**功能特性：**
- 解析文章中的 ````image-prompt` 代码块
- 调用 Google Gemini 3.1 Flash Image Preview API 生成图片
- 并发生成多张图片（可配置）
- 自动替换文章中的提示词为图片链接
- 保留原始提示词到 `image-prompts.md`
- 支持按文件名过滤重新生成

**支持的 API：**
- **Google Gemini 3.1 Flash** (默认)
- OpenAI DALL-E 3 (可选)
- Flux (可选)
- Stable Diffusion (可选)

**使用方法：**
```bash
# 安装依赖
pip3 install -r skills/wechat-workflow/generating-article-images/scripts/requirements.txt

# 配置 API Key
cd skills/wechat-workflow/generating-article-images/scripts
cp config.example.yaml config.yaml
# 编辑 config.yaml，填入 Gemini API Key

# 生成所有图片
python3 skills/wechat-workflow/generating-article-images/scripts/generate_images.py \
    --input "/path/to/article.md"

# 重新生成特定图片
python3 skills/wechat-workflow/generating-article-images/scripts/generate_images.py \
    --input "/path/to/article.md" \
    --filter "01-oracle-architecture.png"
```

**输出内容：**
- 图片保存到 `img/` 文件夹
- 文章中的提示词被替换为图片链接
- `image-prompts.md` 备份所有原始提示词

---

### 4. converting-to-wechat（Markdown转换）

**功能特性：**
- 将 Markdown 转换为微信兼容的 HTML
- 可配置的 YAML 样式（6个内置预设）
- 阿里云 OSS 自动图片上传
- macOS 风格代码块渲染
- 微信编辑器兼容性（使用 `<section>` 替代 `<div>`）
- 支持单文件和批量目录模式
- 默认配置系统（convert.cfg）

**命令行参数：**
| 参数 | 缩写 | 描述 |
|-----------|-------|-------------|
| `--input` | `-i` | **（必选）** 输入的 MD 文件或目录路径 |
| `--style` | `-s` | 视觉样式预设文件路径 |
| `--config` | `-c` | 本地覆盖配置文件（含 OSS 凭据） |
| `--upload-images` | | 启用 OSS 图片上传 |
| `--no-upload` | | 禁用图片上传（覆盖默认设置） |
| `--output` | `-o` | 输出目录（默认：输入目录/output/） |

**使用示例：**
```bash
# 基础转换
python3 skills/wechat-workflow/converting-to-wechat/scripts/convert.py \
    --input "Oracle view/第01篇.md"

# 批量转换
python3 skills/wechat-workflow/converting-to-wechat/scripts/convert.py \
    --input "my-series/"

# 自定义样式
python3 skills/wechat-workflow/converting-to-wechat/scripts/convert.py \
    --input "article.md" \
    --style skills/wechat-workflow/converting-to-wechat/styles/wechat-professional-blue.yaml

# 使用 v3.0 专业样式（无表情符号、纯色设计）
python3 skills/wechat-workflow/converting-to-wechat/scripts/convert.py \
    --input "article.md" \
    --style skills/wechat-workflow/converting-to-wechat/styles/wechat-v3-professional.yaml

# 不上传图片
python3 skills/wechat-workflow/converting-to-wechat/scripts/convert.py \
    --input "article.md" \
    --no-upload
```

**内置样式预设：**
- `mdnice-test.yaml` - 暖橙色，现代排版
- `wechat-professional-blue.yaml` - 专业微信蓝
- `wechat-classic.yaml` - 经典深蓝灰
- `wechat-ios-blue.yaml` - iOS 系统蓝
- `wechat-minimal-dark.yaml` - 极简深色主题
- `wechat-v3-professional.yaml` - **v3.0 专业样式**（无表情符号、纯色设计、深绿+暖橙配色）

---

### 5. extracting-wechat-styles（样式提取）

**功能特性：**
- 解析 HTML 文件并提取 CSS 样式
- 转换为与 converting-to-wechat 兼容的 YAML 格式
- 支持 mdnice 和其他微信编辑器导出
- 提取 8 类样式：基础、段落、标题、引用、列表、表格、代码、分隔线

**使用方法：**
```bash
# 安装依赖
pip3 install beautifulsoup4 pyyaml

# 从 HTML 提取样式
python3 skills/wechat-workflow/extracting-wechat-styles/scripts/generate_style.py \
    --input "example/test.html" \
    --name "my-cool-style"

# 自定义输出目录
python3 skills/wechat-workflow/extracting-wechat-styles/scripts/generate_style.py \
    --input "exported.html" \
    --name "custom-style" \
    --output-dir "/path/to/output"
```

**输出内容：**
- YAML 文件保存到 `converting-to-wechat/styles/<name>.yaml`
- 可立即通过 `--style` 参数使用

---

### 6. using-wechat-workflow（包概览）

**功能特性：**
- 完整的包概览和所有可用技能
- 不同使用场景的快速入门指南
- 常见工作流示例
- 技能依赖关系图
- 故障排除指南
- 选择合适技能的指南

**使用方法：**
```
# 开始任何微信内容任务时使用此技能
wechat-workflow:using-wechat-workflow
```

---

## 🔄 常见工作流

### 工作流 1：技术文章发布（推荐）

**适用于技术博客、教程或文档**

```
[草稿文章]
       ↓
[polishing-content]     # 用文学技法增强内容 + 生成图片提示词
       ↓
[reviewing-technical-accuracy]  # 验证技术声明
       ↓
[generating-article-images]     # ✨ 生成图片
       ↓
[converting-to-wechat]  # 转换为微信 HTML
       ↓
[发布到微信]
```

**详细步骤：**
```bash
# 1. 润色文章（使用 AI 技能）
请润色 my-article.md

# 2. 审核技术准确性（使用 AI 技能）
请审查 my-article.md 的技术准确性

# 3. 生成图片
python3 skills/wechat-workflow/generating-article-images/scripts/generate_images.py \
    --input "my-article.md"

# 4. 转换为微信 HTML
python3 skills/wechat-workflow/converting-to-wechat/scripts/convert.py \
    --input "my-article.md"
```

---

### 工作流 2：批量文章转换

**一次转换多篇文章**

```bash
# 生成所有文章的图片
for file in /path/to/articles/*.md; do
    python3 skills/wechat-workflow/generating-article-images/scripts/generate_images.py \
        --input "$file"
done

# 转换目录中的所有 Markdown 文件
python3 skills/wechat-workflow/converting-to-wechat/scripts/convert.py \
    --input "/path/to/articles/"
```

---

### 工作流 3：自定义样式创建

**创建自己的微信样式预设**

```
[来自 mdnice 的 HTML 模板]
       ↓
[extracting-wechat-styles]  # 提取 YAML 样式
       ↓
[converting-to-wechat 使用自定义样式]  # 使用新样式
```

**详细步骤：**
```bash
# 1. 从 HTML 提取样式
python3 skills/wechat-workflow/extracting-wechat-styles/scripts/generate_style.py \
    --input "mdnice-export.html" \
    --name "my-brand-style"

# 2. 使用新样式
python3 skills/wechat-workflow/converting-to-wechat/scripts/convert.py \
    --input "article.md" \
    --style skills/wechat-workflow/converting-to-wechat/styles/my-brand-style.yaml
```

---

### 工作流 4：重新生成特定图片

**重新生成不满意的图片**

```bash
# 重新生成单张图片
python3 skills/wechat-workflow/generating-article-images/scripts/generate_images.py \
    --input "article.md" \
    --filter "01-oracle-architecture.png"

# 重新生成多张图片
python3 skills/wechat-workflow/generating-article-images/scripts/generate_images.py \
    --input "article.md" \
    --filter "01-*.png"
```

---

## 📁 配置说明

### 文件结构

```
weixin-skills/
└── skills/wechat-workflow/
    ├── converting-to-wechat/          # 核心转换技能
    │   ├── config.yaml                  # 默认 OSS 凭据（已 gitignore）
    │   ├── config-example.yaml          # 配置模板
    │   ├── convert.cfg                  # 默认参数配置
    │   ├── styles/                      # 视觉样式预设库
    │   │   ├── mdnice-test.yaml         # 暖橙色，mdnice 风格
    │   │   ├── wechat-professional-blue.yaml  # 专业蓝
    │   │   ├── wechat-classic.yaml      # 经典深蓝灰
    │   │   ├── wechat-ios-blue.yaml     # iOS 蓝
    │   │   ├── wechat-minimal-dark.yaml # 极简深色
    │   │   └── wechat-v3-professional.yaml  # v3.0 专业样式
    │   └── scripts/
    │       └── convert.py               # 转换脚本
    ├── polishing-content/              # 文章润色技能
    │   ├── scripts/                     # 验证和质量控制脚本
    │   └── references/                  # 示例和技术指南
    ├── reviewing-technical-accuracy/   # 技术审核技能
    ├── generating-article-images/     # 图片生成技能 ✨
    │   └── scripts/
    │       ├── config.example.yaml       # 配置模板
    │       ├── generate_images.py        # 生成脚本
    │       └── requirements.txt          # Python 依赖
    ├── extracting-wechat-styles/      # 样式提取技能
    │   └── scripts/
    │       └── generate_style.py       # 样式提取脚本
    └── using-wechat-workflow/         # 包概览和导航

系列文件夹/（如 "Oracle view/"）
├── 文章.md
├── config.yaml                         # 系列级配置覆盖（可选）
├── img/                                # 本地图片
├── image-prompts.md                    # 图片提示词备份（可选）
└── output/                             # 生成的 HTML（自动创建）
```

### 默认配置：`convert.cfg`

编辑 `skills/wechat-workflow/converting-to-wechat/convert.cfg` 修改默认参数：

```ini
[defaults]
# 默认视觉样式预设
style = skills/wechat-workflow/converting-to-wechat/styles/mdnice-test.yaml

# 默认本地覆盖配置（含 OSS 凭据）
config = skills/wechat-workflow/converting-to-wechat/config.yaml

# 默认启用图片上传（true/false）
upload_images = true
```

### 图片生成配置：`config.yaml`

**首次使用需要配置：**

```bash
cd skills/wechat-workflow/generating-article-images/scripts
cp config.example.yaml config.yaml

# 编辑 config.yaml，填入您的 Gemini API Key
```

**配置示例：**
```yaml
default_api: gemini

apis:
  gemini:
    enabled: true
    api_key: "YOUR_GEMINI_API_KEY"  # 替换为您的 API Key
    model: "gemini-3.1-flash-image-preview"
    timeout: 120
    concurrent_limit: 3
```

### OSS 凭据：`config.yaml`

OSS 凭据存储在 `skills/wechat-workflow/converting-to-wechat/config.yaml`。**此文件已加入 .gitignore，不会提交到 Git。**

为特定文章系列配置不同的 OSS 凭据：

```bash
cp skills/wechat-workflow/converting-to-wechat/config-example.yaml "Oracle view/config.yaml"
```

```yaml
image:
  upload_to_oss: true
  oss_access_key_id: "YOUR_KEY_ID"
  oss_access_key_secret: "YOUR_SECRET"
  oss_bucket: "your-bucket"
  oss_region: "oss-cn-shanghai"
  oss_endpoint: "oss-cn-shanghai.aliyuncs.com"
```

---

## 🔧 微信编辑器兼容性说明

微信公众号后台编辑器在粘贴 HTML 时会进行严格的"标准化"过滤。本工具针对这些问题做了特定适配：

1. **标签过滤**：编辑器会剔除几乎所有的 `<div>` 标签。
   - **解决方案**：使用 `<section>` 作为容器标签以保留背景色。

2. **布局属性删除**：`display: flex` 等属性会被删除。
   - **解决方案**：代码块装饰栏使用 `display: inline-block` + `vertical-align`。

3. **列表换行陷阱**：微信会强制将文本包裹在 `<p>` 中，可能分离标点符号。
   - **解决方案**：`convert.py` 会主动将文本包裹在 `<section>` 中以防止分离。

4. **CSS 冗余**：背景色多重定义以确保复制粘贴的可靠性。

---

## 📚 完整技能参考

| 技能名称 | 中文名称 | 用途 |
|------------|--------------|---------|
| `wechat-workflow:polishing-content` | 文章润色 | 技术文章润色，添加文学技法和图片提示词 |
| `wechat-workflow:reviewing-technical-accuracy` | 技术审核 | 技术内容审核，验证版本兼容性和代码准确性 |
| `wechat-workflow:generating-article-images` | 图片生成 | 从提示词自动生成文章配图 |
| `wechat-workflow:converting-to-wechat` | Markdown转换 | Markdown → 微信公众号 HTML（核心技能） |
| `wechat-workflow:extracting-wechat-styles` | 样式提取 | 从 HTML 模板提取样式 YAML |
| `wechat-workflow:using-wechat-workflow` | 包概览 | 包概览、快速开始指南和工作流 |

---

## 🛠 故障排除

| 问题 | 解决方法 |
|---------|----------|
| 图片不显示 | 确保 OSS 凭据配置正确且上传已启用 |
| 排版显示错误 | 粘贴前全选整个 HTML 内容（Ctrl+A / Cmd+A） |
| 代码块样式丢失 | 脚本使用 `<section>` 标签保留样式 |
| 列表标点换行 | 脚本已自动修复此问题 |
| 样式未加载 | 检查 `convert.cfg` 中的样式路径或使用绝对路径 |
| 图片生成失败 | 检查 `generating-article-images/config.yaml` 中的 API Key 配置 |
| "未找到图片提示词" | 确保文章已通过 `polishing-content` 润色 |
| Gemini API 配额不足 | 检查 Google Cloud Console 中的 API 使用量和配额 |

---

## 🔗 参考项目

- https://github.com/DavidLam-oss/obsidian-wechat-converter
- https://md.qikqiak.com/
- https://github.com/cnych/markdown-weixin
