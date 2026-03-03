# Tech Article Polisher

一个用于润色和增强技术文章的技能，专为 IT 专业人士（DBA、运维人员、开发人员、数据工程师）设计。支持多种技术领域，包括数据库、DevOps、AI/LLM、可视化等。

## 功能特性

- ✅ 应用文学手法（比喻、类比、叙事元素）使技术内容更生动
- ✅ 优化语言流畅度和可读性，同时保持技术准确性
- ✅ 添加适合微信公众号等发布平台的格式
- ✅ 生成高传播率的备选标题
- ✅ 验证代码片段和技术内容的技术准确性
- ✅ 支持单文件和批量处理
- ✅ 可配置的润色强度
- ✅ 支持多种技术领域（Oracle、MySQL、PostgreSQL、Kubernetes、Docker、LLM、Mermaid 等）

## 支持的技术领域

### 数据库
- Oracle (SQL, PL/SQL, Performance Views, RAC, Data Guard)
- MySQL (SQL, Performance Schema, InnoDB, Replication)
- PostgreSQL (SQL, PL/pgSQL, pg_stat views, Extensions)
- MongoDB (Aggregation, Indexes, Sharding)
- Redis (Data Structures, Persistence, Clustering)
- Elasticsearch (Queries, Aggregations, Indexing)

### DevOps 与基础设施
- Kubernetes (Pods, Services, Deployments, Helm)
- Docker (Containers, Images, Compose)
- Terraform (Infrastructure as Code)
- Ansible (Configuration Management)
- Prometheus (Monitoring, Alerting)
- Grafana (Visualization)

### 数据与 AI
- LLM (Large Language Models, Prompt Engineering, RAG)
- Vector Databases (Embeddings, Similarity Search)
- Machine Learning (Training, Inference, MLOps)
- Data Engineering (ETL, Data Pipelines, Airflow)

### 可视化与文档
- Mermaid (Diagrams, Flowcharts, Sequence Diagrams)
- PlantUML (UML Diagrams)
- Architecture Diagrams

### 编程语言
- Python (Django, Flask, FastAPI, Data Science)
- Java (Spring Boot, Microservices)
- Go (Microservices, Cloud Native)
- JavaScript/TypeScript (Node.js, React, Vue)
- Rust (Systems Programming)

## 快速开始

### 单文件润色

```
请润色 /path/to/article.md
```

### 批量润色

```
请润色 /path/to/directory/ 目录下所有的 md 文件，除了第 01 篇、第 02 篇、第 03 篇
```

### 指定技术领域

```
请润色 /path/to/article.md，这是一篇关于 MySQL 的文章
```

### 带技术验证的润色

```
请润色 /path/to/article.md，并验证所有代码片段的技术准确性
```

## 润色强度

### 轻度润色

- 使用 2-3 种文学手法
- 每篇文章 3-5 处应用
- 保持原文风格
- 生成 3 个备选标题

### 标准润色

- 使用 5-7 种文学手法
- 每篇文章 8-12 处应用
- 适度增强可读性
- 生成 5 个备选标题

### 深度润色

- 使用 8-10 种文学手法
- 每篇文章 15-20 处应用
- 显著提升可读性
- 生成 5 个备选标题

## 文学手法

技能支持以下文学手法：

1. **金庸式笔触** - 模仿金庸小说的叙事节奏
2. **借古喻今** - 引用历史典故、古诗词、兵法
3. **列锦手法** - 并列排列多个意象或名词
4. **物化手法** - 将抽象概念转化为具体物象
5. **比喻与类比** - 将复杂概念与日常生活联系
6. **设问与自答** - 通过提问引导思考
7. **对比与反差** - 通过对比突出差异
8. **层递与递进** - 按照逻辑顺序层层深入
9. **场景化叙事** - 将技术问题放入具体场景
10. **数字化表达** - 用数字增强说服力
11. **引用与权威** - 引用官方文档或专家观点
12. **悬念与伏笔** - 在开头设置悬念
13. **总结与升华** - 在结尾提炼要点
14. **代码与文字穿插** - 用代码示例支撑文字说明

## 技术验证

### 版本兼容性标注

所有代码片段都应标注版本兼容性：

```sql
-- 适用版本：Oracle 11g / 12c / 19c / 26ai
-- 适用版本：MySQL 5.7 / 8.0
-- 适用版本：PostgreSQL 12 / 13 / 14 / 15
```

```python
# 适用版本：Python 3.8+
# 适用版本：OpenAI API v1.0+
```

```yaml
# 适用版本：Kubernetes 1.20+
# 适用版本：Docker Compose v2
```

### 验证脚本

#### 单文件验证

使用验证脚本检查技术准确性：

```bash
python scripts/validate-technical-accuracy.py /path/to/article.md
```

**验证内容：**
- 代码语法正确性（SQL、Python、YAML 等）
- 命令语法和参数
- API 名称和参数
- 版本兼容性标注
- 技术特定的最佳实践

#### 批量验证

使用批量验证脚本处理多个文件：

```bash
python scripts/batch-validate.py /path/to/directory --technology oracle
python scripts/batch-validate.py /path/to/directory --auto-detect
python scripts/batch-validate.py /path/to/directory --resume
```

**批量验证特性：**
- 并行处理多个文件（可配置工作线程数）
- 自动技术检测（基于关键词）
- 进度跟踪和断点续传
- 错误恢复和详细报告
- 支持 Oracle、MySQL、PostgreSQL、Kubernetes、LLM、Mermaid 等多种技术

#### 质量控制

使用质量控制脚本分析文学手法和可读性：

```bash
python scripts/quality-control.py /path/to/article.md
python scripts/quality-control.py /path/to/article.md --output report.json
python scripts/quality-control.py /path/to/directory --batch
```

**质量控制分析：**
- 文学手法统计（列锦、物化、金庸式笔触等）
- 可读性评分（0-100 分）
- 句子长度分析
- 词汇丰富度评估
- 改进建议

## 目录结构

```
tech-article-polisher/
├── SKILL.md                          # 主技能文件
├── README.md                         # 使用说明
├── references/                       # 参考资料
│   ├── examples.md                   # 详细使用示例
│   ├── quality-control.md            # 质量控制标准
│   ├── oracle-versions.md            # Oracle 版本兼容性指南
│   └── technology-guides.md          # 技术指南（多技术领域）
└── scripts/                          # 脚本工具
    ├── validate-technical-accuracy.py  # 技术准确性验证脚本（单文件）
    ├── batch-validate.py              # 批量技术验证脚本（并行处理）
    └── quality-control.py             # 质量控制脚本（文学手法和可读性分析）
```

## 参考资料

### 详细使用示例

参见 [references/examples.md](references/examples.md) 了解：
- 单文件润色示例
- 批量处理示例
- 高级用法模式
- 错误处理示例
- 技术特定示例

### 质量控制标准

参见 [references/quality-control.md](references/quality-control.md) 了解：
- 技术准确性验证
- 文学手法使用指南
- 结构完整性检查
- 标题生成标准
- 技术特定质量标准

### 技术指南

参见 [references/technology-guides.md](references/technology-guides.md) 了解：
- 数据库技术指南（Oracle、MySQL、PostgreSQL）
- DevOps 技术指南（Kubernetes、Docker、Terraform）
- AI/LLM 技术指南（Prompt Engineering、RAG）
- 可视化指南（Mermaid、PlantUML）
- 编程语言指南（Python、Java、Go）

### Oracle 版本兼容性

参见 [references/oracle-versions.md](references/oracle-versions.md) 了解：
- 版本概览和支持状态
- 视图版本兼容性
- 特性版本兼容性
- 版本差异处理
- 常见兼容性问题

## 核心原则

- **技术准确性优先** - 永不为了文学效果而牺牲技术正确性
- **适度使用手法** - 不是每个部分都需要每种手法，在自然的地方应用
- **保持原有结构** - 保持文章的逻辑流程和组织结构
- **简洁明了** - 避免过度润色导致内容冗长
- **了解受众** - IT 专业人士重视深度但更看重清晰度
- **验证技术内容** - 始终验证代码片段和技术特定内容
- **标注版本兼容性** - 清晰标记版本特定特性
- **生成高质量标题** - 创建引人入胜、易于分享的标题
- **适应技术领域** - 使用技术特定的示例、类比和术语
- **保持更新** - 跟上技术更新和最佳实践

## 使用场景

1. **技术博客润色** - 提升技术博客的可读性和传播率
2. **微信公众号文章** - 添加适合微信公众号的格式和标题
3. **技术文档优化** - 使技术文档更易于理解
4. **批量文章处理** - 批量润色系列文章
5. **技术内容验证** - 验证代码片段和技术特定内容的技术准确性
6. **多技术领域支持** - 支持数据库、DevOps、AI/LLM、可视化等多种技术领域

## 注意事项

- 技能会保持文章的主体结构不变
- 技能会优先保证技术准确性
- 技能会根据文章内容选择合适的文学手法
- 技能会生成多个备选标题供选择
- 技能支持自定义润色强度
- 技能支持指定技术领域以获得更精准的润色效果

## 许可证

本技能为开源项目，可自由使用和修改。
