# weixin-skills

微信公众号内容创作技能包 - 从文档到发布的完整工作流。

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/downloads/)

## 📖 项目简介

本项目包含一套完整的微信公众号内容创作工具链，涵盖从**文档收集**、**内容润色**、**图片生成**到**格式转换**的全流程。

### ⭐ 核心特性

- 📚 **智能知识管理**：集成 NotebookLM 进行文档分析和内容规划
- ✍️ **文章润色**：16 种文学技巧，将技术文档转化为生动文章
- 🎨 **自动配图**：使用 Gemini 3.1 Flash API 生成高质量文章配图
- 🔄 **批量转换**：一键将 Markdown 转换为微信公众号 HTML
- 🎯 **样式定制**：6 种内置样式，支持自定义样式提取

### 🔥 最重要的改进

**`polishing-content` 是工作流中不可或缺的核心步骤！**

它将普通的技术文档转化为：
- 📖 生动有趣的文学性文章（16 种文学技巧）
- 🎨 自动生成的图片提示词（Midjourney/DALL-E/Flux）
- 🏷️ 5 个吸引人的备选标题
- ✅ 可验证的技术准确性

详见 [WORKFLOW_GUIDE.md](docs/WORKFLOW_GUIDE.md) 了解完整工作流程。

---

## 🎯 技能概览

### 核心技能组：wechat-workflow

| 技能 | 功能 | 适用场景 |
|------|------|----------|
| `polishing-content` | **文章润色**，添加16种文学技法和图片提示词 | ⭐ **所有文章都必须经过此步骤** |
| `generating-article-images` | 使用 Gemini 3.1 Flash 生成图片 | 自动生成文章配图（带重试机制） |
| `converting-to-wechat` | Markdown 转 HTML，支持6种样式 | 转换文章为微信格式 |
| `reviewing-technical-accuracy` | 技术审核，验证代码和版本兼容性 | 发布包含代码/命令的技术内容 |
| `extracting-wechat-styles` | 从 HTML 提取样式为 YAML | 创建自定义样式预设 |
| `using-wechat-workflow` | 完整工作流概览和指南 | 开始任何微信内容创作任务 |

### 扩展技能

| 技能 | 功能 | 适用场景 |
|------|------|----------|
| `notebooklm` | NotebookLM 集成，支持文档查询和管理 | 从文档中获取知识、内容分析 |
| `generating-articles-from-docs` | 从文档自动生成系列文章 | 批量内容生产、知识库转化 |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装核心转换技能
pip3 install -r skills/wechat-workflow/converting-to-wechat/scripts/requirements.txt

# 安装图片生成技能
pip3 install -r skills/wechat-workflow/generating-article-images/scripts/requirements.txt
```

### 2. 配置 API

```bash
# 图片生成配置（必需）
cd skills/wechat-workflow/generating-article-images/scripts
cp config.example.yaml config.yaml
# 编辑 config.yaml，填入 Gemini API Key

# OSS 上传配置（可选，用于图片托管）
cd ../../converting-to-wechat/
cp config.example.yaml config.yaml
# 编辑 config.yaml，填入阿里云 OSS 凭据
```

### 3. 完整工作流程（推荐）

```bash
# 步骤 1: 使用 polishing-content 润色文章 ⭐ 核心步骤
# 在 Claude Code 中执行：
请润色 /path/to/article.md

# 步骤 2: 生成图片
python3 skills/wechat-workflow/generating-article-images/scripts/generate_images.py \
    --input "/path/to/article.md"

# 步骤 3: 转换为 HTML
python3 skills/wechat-workflow/converting-to-wechat/scripts/convert.py \
    --input "/path/to/articles/" \
    --output "output/html/"
```

### 4. 发布到微信

在浏览器中打开生成的 HTML 文件，全选（Cmd+A）→ 复制 → 粘贴到微信公众号编辑器。

---

## 🔄 完整工作流

### 标准工作流（推荐）

```
┌─────────────────────────────────────────────────────────────────┐
│  步骤 1️⃣: 创建草稿文章                                          │
│  - 手动撰写草稿                                                │
│  - 或从其他工具生成（如 NotebookLM、ChatGPT）                    │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│  步骤 2️⃣: 使用 polishing-content 润色 ⭐⭐⭐ 核心步骤        │
│                                                                  │
│  🌟 文学技巧润色（16种）                                      │
│     • 金庸式笔触：武侠风格，生动描述                            │
│     • 借古喻今：历史典故类比现代技术                            │
│     • 列锦手法：意象罗列，增强画面感                            │
│     • 物化手法：抽象概念具体化                                  │
│     • 比喻类比：用熟悉事物解释抽象                              │
│     • ...还有11种技巧                                          │
│                                                                  │
│  🎨 自动生成图片提示词                                          │
│     • 根据文章内容自动选择插入位置                              │
│     • 生成 Midjourney/DALL-E/Flux 提示词                          │
│     • 包含详细参数：Subject, Details, Style, Colors              │
│     • 中英文双语说明                                            │
│                                                                  │
│  🏷️ 生成5个备选标题                                            │
│                                                                  │
│  使用方式：请润色 /path/to/article.md                          │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│  步骤 3️⃣: 生成图片                                              │
│                                                                  │
│  • 自动解析图片提示词代码块                                     │
│  • 调用 Gemini 3.1 Flash Image Preview API                      │
│  • 重试机制：失败自动重试3次（可配置）                         │
│  • 部分成功也会替换成功的图片                                  │
│  • 并发生成，提高效率                                          │
│                                                                  │
│  python3 generate_images.py --input article.md                 │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│  步骤 4️⃣: 转换为微信 HTML                                        │
│                                                                  │
│  • 批量转换 Markdown 文件                                       │
│  • 上传图片到阿里云 OSS                                         │
│  • 应用样式预设（6种内置样式）                                │
│  • 微信编辑器兼容优化                                          │
│                                                                  │
│  python3 convert.py --input articles/ --output html/           │
└────────────────┬────────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│  步骤 5️⃣: 发布到微信                                            │
│                                                                  │
│  • 在浏览器中打开 HTML 文件                                    │
│  • 全选 (Cmd+A) → 复制                                         │
│  • 粘贴到微信公众号编辑器                                     │
│                                                                  │
│  完成！🎉                                                       │
└─────────────────────────────────────────────────────────────────┘
```

### 从文档生成文章工作流

```
[上传文档到 NotebookLM]
       ↓
[generating-articles-from-docs] # 自动分析、规划、生成文章
       ↓
[polishing-content]            # ⭐ 润色内容 + 生成图片提示词
       ↓
[generating-article-images]     # 生成配图
       ↓
[converting-to-wechat]          # 转换为微信 HTML
       ↓
[发布到微信]
```

---

## 📊 效果对比

### 使用 polishing-content vs 不使用

| 指标 | 不使用 | 使用 |
|------|--------|------|
| 📖 文学性 | ⭐⭐⭐ 专业但干瘪 | ⭐⭐⭐⭐⭐ 生动有趣，有故事性 |
| 🎨 图片覆盖率 | ⭐⭐ 很多文章没有图片 | ⭐⭐⭐⭐⭐ 每篇文章4-6张图片 |
| 🏷️ 标题吸引力 | ⭐⭐⭐ 单一标题 | ⭐⭐⭐⭐⭐ 5个备选标题 |
| 👁️ 视觉效果 | ⭐⭐⭐ 一般 | ⭐⭐⭐⭐⭐ 专业美观 |
| 📱 可读性 | ⭐⭐⭐ 需要反复阅读 | ⭐⭐⭐⭐⭐ 一遍就能理解 |
| 🎯 点击率 | ⭐⭐⭐ 一般 | ⭐⭐⭐⭐⭐ 大幅提升 |

### 示例对比

**原文（无润色）**：
> NotebookLM 是 Google 推出的知识管理工具。它可以帮助用户整理文档，回答问题。

**润色后（金庸式笔触 + 列锦手法）**：
> 想象一下，在江湖中，若有一位绝世高手，能够过目不忘，将天下武学秘籍尽收脑海，并能举一反三，发现不同武学之间的关联。这便是 Google 推出的 NotebookLM，一位当世的知识管理"大宗师"。

它深谙"书山有路勤为径"的道理，能助你：
- 📚 整理文档，如同管理藏经阁
- 🤔 回答问题，如同指点武功
- 🔗 发现关联，如同融会贯通

---

## 📁 项目结构

```
weixin-skills/
├── skills/
│   ├── wechat-workflow/              # 微信工作流技能组
│   │   ├── converting-to-wechat/     # Markdown → HTML 转换
│   │   │   ├── scripts/
│   │   │   │   ├── convert.py        # 主转换脚本
│   │   │   │   ├── config.example.yaml
│   │   │   │   └── requirements.txt
│   │   │   └── styles/               # 6种内置样式
│   │   ├── generating-article-images/ # 图片生成
│   │   │   ├── scripts/
│   │   │   │   ├── generate_images.py # 主图片生成脚本
│   │   │   │   ├── config.example.yaml
│   │   │   │   └── requirements.txt
│   │   ├── polishing-content/        # ⭐ 文章润色（核心）
│   │   ├── reviewing-technical-accuracy/ # 技术审核
│   │   ├── extracting-wechat-styles/ # 样式提取
│   │   └── using-wechat-workflow/    # 工作流概览
│   ├── notebooklm/                   # NotebookLM 集成
│   │   ├── scripts/                  # 核心脚本
│   │   ├── data/                     # 认证数据（gitignore）
│   │   └── requirements.txt
│   └── generating-articles-from-docs/ # 文档生成文章
│       ├── scripts/
│       ├── config.example.yaml
│       └── requirements.txt
├── output/                            # 测试输出目录
│   ├── articles/                     # Markdown 文章
│   ├── html/                         # 微信 HTML
│   └── img/                          # 生成的图片
├── docs/                              # 文档
│   └── WORKFLOW_GUIDE.md             # ⭐ 完整工作流程指南
├── .gitignore                         # Git 忽略规则
├── CLAUDE.md                          # 技能边界定义
└── README.md                          # 本文件
```

---

## ⚙️ 配置说明

### 图片生成配置

编辑 `skills/wechat-workflow/generating-article-images/scripts/config.yaml`：

```yaml
default_api: gemini

apis:
  gemini:
    enabled: true
    api_key: "YOUR_GEMINI_API_KEY"  # 替换为您的 API Key
    model: "gemini-3.1-flash-image-preview"  # 使用最新模型
    timeout: 120
    concurrent_limit: 3
    max_retries: 3  # 失败重试次数（可选）
    retry_delay: 2  # 重试延迟（秒，可选）

image:
  default_aspect_ratio: "16:9"  # 默认图片宽高比
  output_dir: "img"             # 图片输出目录
```

### OSS 图片上传配置（可选）

编辑 `skills/wechat-workflow/converting-to-wechat/config.yaml`：

```yaml
image:
  upload_to_oss: true
  oss_access_key_id: "YOUR_KEY_ID"
  oss_access_key_secret: "YOUR_SECRET"
  oss_bucket: "your-bucket"
  oss_region: "oss-cn-shanghai"
  oss_endpoint: "oss-cn-shanghai.aliyuncs.com"
```

**注意**：`config.yaml` 文件已加入 `.gitignore`，不会提交到 Git。

---

## 🎨 内置样式

| 样式名称 | 风格 | 适用场景 |
|---------|------|----------|
| `mdnice-test.yaml` | 暖橙色，现代排版 | 技术博客 |
| `wechat-professional-blue.yaml` | 专业微信蓝 | 企业号 |
| `wechat-classic.yaml` | 经典深蓝灰 | 传统媒体 |
| `wechat-ios-blue.yaml` | iOS 系统蓝 | 科技产品 |
| `wechat-minimal-dark.yaml` | 极简深色 | 设计类内容 |
| `wechat-v3-professional.yaml` | v3.0 专业（无emoji） | 正式文章 |

---

## 📊 输出示例

### 完整测试结果

```
============================================================
✅ 步骤 1/3: 文章润色（polishing-content）
============================================================
  处理文章: 3 篇
  ✓ 01-ai-skills-notebooklm.md
    • 生成 5 个备选标题
    • 应用 16 种文学技巧
    • 生成 6 个图片提示词
  ✓ 02-ai-skills-trends-2025.md
    • 生成 5 个备选标题
    • 应用 12 种文学技巧
    • 生成 4 个图片提示词
  ✓ 03-ai-skills-knowledge-system.md
    • 生成 5 个备选标题
    • 应用 14 种文学技巧
    • 生成 5 个图片提示词

============================================================
✅ 步骤 2/3: 生成图片
============================================================
  文章: 01-ai-skills-notebooklm-polished.md
  生成图片: 6/6 (100%)
  ✓ 01-notebooklm-hero.png (1.7 MB)
  ✓ 01-information-overload.png (1.9 MB)
  ✓ 01-ai-knowledge-manager.png (2.0 MB)
  ✓ 01-knowledge-graph.png (1.8 MB)
  ✓ 01-research-efficiency.png (1.4 MB)
  ✓ 01-gemini-architecture.png (1.3 MB)

  文章: 02-ai-skills-trends-2025-polished.md
  生成图片: 3/4 (75%)
  ✓ 02-ai-trends-hero.png (1.8 MB)
  ✓ 02-ai-cost-reduction.png (1.4 MB)
  ✓ 02-ai-business-applications.png (1.8 MB)
  ⚠️  02-ai-frontier-applications.png (重试3次后失败)

  文章: 03-ai-skills-knowledge-system-polished.md
  生成图片: 5/5 (100%)
  ✓ 03-knowledge-system-hero.png (1.8 MB)
  ✓ 03-information-overload-solution.png (1.7 MB)
  ✓ 03-knowledge-taxonomy.png (1.5 MB)
  ✓ 03-smart-retrieval-scenarios.png (1.6 MB)
  ✓ 03-learning-cycle.png (1.5 MB)

============================================================
✅ 步骤 3/3: 转换为微信 HTML
============================================================
  转换文件数: 12 篇
  图片上传: 25 张成功
  输出文件:
    ✓ 01-ai-skills-notebooklm-polished.html (33.6 KB)
    ✓ 02-ai-skills-trends-2025-polished.html (39.4 KB)
    ✓ 03-ai-skills-knowledge-system-polished.html (65.4 KB)
```

---

## 🛠 故障排除

| 问题 | 解决方法 |
|------|----------|
| 图片不显示 | 确保 OSS 凭据配置正确且上传已启用 |
| 图片生成失败 | 检查 Gemini API Key 和配额，已启用自动重试机制 |
| 排版显示错误 | 粘贴前全选整个 HTML 内容（Cmd+A） |
| 代码块样式丢失 | 脚本使用 `<section>` 标签保留样式 |
| "未找到图片提示词" | ⭐ 确保文章已通过 `polishing-content` 润色 |
| 文章干瘪无吸引力 | ⭐ 使用 `polishing-content` 技能润色内容 |
| 缺少图片 | ⭐ 使用 `polishing-content` 自动生成图片提示词 |

---

## 🔒 安全说明

- ✅ 所有 `config.yaml` 文件已加入 `.gitignore`
- ✅ 只提交 `config.example.yaml` 示例文件
- ✅ API 密钥、OSS 凭据等敏感信息不会被提交
- ✅ 认证数据存储在 `skills/notebooklm/data/`（已排除）

---

## 📚 详细文档

- [WORKFLOW_GUIDE.md](docs/WORKFLOW_GUIDE.md) - 完整工作流程指南，深入理解 polishing-content
- [CLAUDE.md](CLAUDE.md) - 技能边界定义和项目约定

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**最后更新**: 2026-03-04
**版本**: 2.0.0
