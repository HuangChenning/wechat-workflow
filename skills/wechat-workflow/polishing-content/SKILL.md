---
name: polishing-content
description: Use when polishing technical articles for WeChat Official Accounts. Applies literary techniques (16 types including Jin Yong style, historical analogies, metaphors), generates image prompts for Midjourney/DALL-E 3/Flux (4K HD quality), optimizes language for readability while maintaining technical accuracy. Supports single-file and batch processing with configurable polish intensity (Light/Standard/Deep). Works with multiple technologies: Oracle, MySQL, PostgreSQL, Redis, MongoDB, Kubernetes, Docker, LLM, etc.
---

# Polishing Content

**Formerly known as**: `tech-article-polisher`

This skill enhances technical articles with engaging writing techniques and image generation prompts for IT professionals (DBAs, DevOps, developers, data engineers).

# Tech Article Polisher

## Target Audience

IT professionals (DBAs, DevOps engineers, developers, data engineers, system administrators)

## Core Principles

**Professional yet accessible**: Use professional terminology and business/psychological concepts, but explain them in plain language.

**Maintain structure**: Keep the original article structure intact while enhancing the language and flow.

**Technical accuracy first**: Never compromise technical correctness for literary effect.

**Technology-agnostic**: Support multiple technologies and domains without bias.

**Direct file modification**: ALWAYS modify the target file directly using tools (SearchReplace), NEVER describe the polish result in the response without actual file changes. Use TodoWrite to track progress.

**Image directory management**: Always check and create the `img` directory in the target article's directory before generating image prompts. All image placeholders must use relative paths like `./img/[文章序列号]-[图片名].png` (e.g., 01-oracle-memory-architecture.png).

## Quick Start

### Single File Polish

```
请润色 /path/to/article.md
```

**Note**: When polishing an article with image prompts, the skill will automatically check and create an `img` directory in the article's directory if it doesn't exist. All image placeholders will use relative paths like `./img/[文章序列号]-[图片名].png` (e.g., 01-oracle-memory-architecture.png).

### Batch Polish

```
请润色 /path/to/directory/ 目录下所有的 md 文件
```

**Note**: 批量优化时，技能会：
1. 为每篇文章生成图片提示词，图片名称包含文章序列号（如 01-xxx.png, 02-xxx.png）
2. 为所有文章创建一个统一的封面图片提示词，保存为 `title.md`
3. 封面图片尺寸为 900 * 383 px (2.25:1 比例)

### With Technical Validation

```
请润色 /path/to/article.md，并验证所有代码片段的技术准确性
```

### Specify Technology Domain

```
请润色 /path/to/article.md，这是一篇关于 MySQL 的文章
```

### Batch Validation

```
请验证 /path/to/directory/ 目录下所有文章的技术准确性
```

### Quality Control Analysis

```
请分析 /path/to/article.md 的文学手法和可读性评分
```

### With Image Prompt Generation

```
请润色 /path/to/article.md，并在适当位置添加图片生成提示词
```

**Important**: The skill will automatically check and create an `img` directory in the article's directory if it doesn't exist. All generated image placeholders will use relative paths like `./img/[文章序列号]-[图片名].png` (e.g., 01-oracle-memory-architecture.png). The image prompts will be formatted as code blocks (```image-prompt```) instead of HTML comments or blockquotes.

## Supported Technologies

### Databases
- Oracle (SQL, PL/SQL, Performance Views, RAC, Data Guard)
- MySQL (SQL, Performance Schema, InnoDB, Replication)
- PostgreSQL (SQL, PL/pgSQL, pg_stat views, Extensions)
- MongoDB (Aggregation, Indexes, Sharding)
- Redis (Data Structures, Persistence, Clustering)
- Elasticsearch (Queries, Aggregations, Indexing)

### DevOps & Infrastructure
- Kubernetes (Pods, Services, Deployments, Helm)
- Docker (Containers, Images, Compose)
- Terraform (Infrastructure as Code)
- Ansible (Configuration Management)
- Prometheus (Monitoring, Alerting)
- Grafana (Visualization)

### Data & AI
- LLM (Large Language Models, Prompt Engineering, RAG)
- Vector Databases (Embeddings, Similarity Search)
- Machine Learning (Training, Inference, MLOps)
- Data Engineering (ETL, Data Pipelines, Airflow)

### Visualization & Documentation
- Mermaid (Diagrams, Flowcharts, Sequence Diagrams)
- PlantUML (UML Diagrams)
- Architecture Diagrams

### Programming Languages
- Python (Django, Flask, FastAPI, Data Science)
- Java (Spring Boot, Microservices)
- Go (Microservices, Cloud Native)
- JavaScript/TypeScript (Node.js, React, Vue)
- Rust (Systems Programming)

## Workflow

### Step 1: Read and Analyze

Read the target file(s) from the specified directory. Understand:
- Current structure and flow
- Technology domain and technical content
- Areas that need enhancement
- Code snippets and their accuracy

### Step 2: Identify Technology Domain

Detect or specify the technology domain:
- Analyze code snippets, commands, and terminology
- Identify database type, programming language, or infrastructure tool
- Determine version-specific features if applicable

### Step 3: Polish Content

Enhance the article while maintaining its structure:
- Apply appropriate writing techniques from the list below
- Improve language flow and readability
- Ensure technical accuracy is preserved
- Add professional yet accessible explanations
- Use technology-appropriate examples and analogies

### Step 4: Validate Technical Accuracy

For all technical articles:
- Validate code syntax (SQL, Python, YAML, etc.)
- Check command correctness
- Verify API names and parameters
- Check version compatibility annotations
- Run validation script if requested

### Step 5: Prepare Image Directory

Check if the `img` directory exists in the target article's directory. If not, create it to store generated images:

**Image directory preparation:**
1. Get the directory path of the target article file
2. Check if `img` directory exists in that directory
3. If the `img` directory does not exist, create it using: `mkdir -p [article-directory]/img`
4. All image placeholders will use relative path: `./img/[generated-filename].png`

**Example:**
- Article path: `/Users/user/docs/01-oracle-architecture.md`
- Image directory: `/Users/user/docs/img/`
- Image placeholder: `./img/01-oracle-memory-architecture.png`
- 文章序列号: 01
- 图片名称: oracle-memory-architecture

### Step 6: Format for Publication

Add formatting suitable for publication platforms (e.g., WeChat Official Accounts):
- Use blockquotes for important notes
- Add bold text for emphasis
- Insert horizontal lines for section separation
- Ensure proper heading hierarchy
- Format code blocks with language tags

### Step 7: Generate Image Prompts

Identify positions where images would enhance the article and generate detailed prompts:

**When to add image prompts:**
- After introducing core concepts or complex architectures
- Before explaining technical workflows or processes
- When comparing technologies or approaches
- At key inflection points in the narrative
- When visualizing abstract concepts (e.g., data structures, system architecture)

**Image prompt generation guidelines:**
1. Read the surrounding content (5-10 lines before and after the target position)
2. Identify the core concept or technical element to visualize
3. Generate a detailed prompt following the standard format (see Image Prompt Template below)
4. Insert the prompt in a code block (```image-prompt```) immediately before the image markdown link
5. Ensure the prompt is relevant to the surrounding technical content
6. Use technology-appropriate colors and visual elements
7. Ensure the `img` directory exists in the article's directory (created in Step 5)

**Prompt insertion format:**
```markdown
```image-prompt
用途：[简短描述图片用途]
工具：Midjourney / DALL-E 3 / Flux（生成 4K HD 质量图片）
图片路径：./img/[文章序列号]-[图片名].png（例如：01-ai-skill-layered-architecture.png）

Prompt (英文):
Subject: [核心主体描述]
Details:
- [细节1]
- [细节2]
- [细节3]
Style: [风格描述]
Colors: [颜色方案]
Visual Flow: [视觉流向]
Key Elements: [关键元素强调]
Technical: [技术参数，包含 4K HD 质量，如 --ar 16:9 --v 6.0 --style raw --quality 2 --stylize 250]

中文释义：
[详细的中文释义，解释图片要展示的内容]
```

------

![图片描述](./img/[文章序列号]-[图片名].png)

------
```

**图片命名规则:**
- 从文章文件名中提取序列号（如 "01-xxx.md" 中的 "01"）
- 序列号与图片名用短横线连接：`[文章序列号]-[图片名].png`
- 示例：
  - 文件名: `01-拒绝当复读机！为什么你的 AI 需要"技能包"？.md`
  - 图片路径: `./img/01-ai-traditional-vs-skill-comparison.png`
  - 文件名: `02-像带实习生一样设计 AI：三层"渐进式"沟通法.md`
  - 图片路径: `./img/02-ai-skill-progressive-structure.png`

**批量优化时的图片命名规则:**
- 对于批量优化的系列文章，每篇文章使用其文件名中的序列号作为图片前缀
- 这确保了系列文章的图片文件具有唯一的标识符和良好的组织性
- 批量优化完成后，将根据所有文章内容生成一个封面图片提示词，保存为 `title.md`

**Technology-specific color schemes:**
- Oracle: Red (#C74634), Blue (#3498DB), Gold (#F1C40F)
- MySQL: Orange (#E67E22), Blue (#3498DB)
- PostgreSQL: Blue (#3498DB), Silver (#BDC3C7)
- Redis: Red (#E74C3C), Gray (#7F8C8D)
- Kubernetes: Blue (#3498DB), Green (#27AE60)
- Docker: Blue (#3498DB), Cyan (#1ABC9C)
- LLM/AI: Purple (#9B59B6), Gold (#F1C40F), Green (#27AE60)

**Visual style recommendations:**
- Technical diagrams: Modern infographic with clean lines, flat design
- Architecture diagrams: Hierarchical tree structures, layered components
- Process flows: Left-to-right or top-to-bottom flow with arrows
- Comparisons: Side-by-side layout with highlighted differences
- Abstract concepts: Metaphorical visual representations

### Step 8: Generate Titles

Create 5 alternative high-impact titles based on the polished content. Titles should:
- Be engaging and shareable
- Reflect the article's core value
- Use numbers, questions, or strong statements
- Appeal to the target audience
- Include technology keywords when relevant

**Insert titles at the beginning of the article** (after title generation):
```markdown
## 备选标题

1. [标题1]
2. [标题2]
3. [标题3]
4. [标题4]
5. [标题5]

---
```

### Step 9: Generate Cover Image Prompt

After polishing all articles in the specified directory, generate a cover image prompt and save it to `title.md` in the same directory.

**Cover image specifications:**
- 尺寸: 900 * 383 px (2.25:1 比例)
- 用途: 系列文章封面图
- 工具: Midjourney / DALL-E 3 / Flux

**Cover image prompt format (in title.md):**
```markdown
```image-prompt
用途：系列文章封面图
工具：Midjourney / DALL-E 3 / Flux
图片尺寸：900 * 383 px (2.25:1 比例)

Prompt (英文):
Subject: [系列文章的核心主题，如 AI Skills, Oracle Architecture, Kubernetes DevOps]
Details:
- [整体视觉风格描述]
- [核心元素1]
- [核心元素2]
- [核心元素3]
- [系列文章数量提示，如 "covering 5 core concepts"]
Style: [封面图风格，如 Modern tech illustration, Clean professional design, Vibrant tech art]
Colors: [主色调方案，参考文章技术栈颜色]
Visual Flow: [视觉流向，通常为左到右或中心发散]
Key Elements: [关键元素强调，如 "AI assistant icon", "Skill cards", "Progressive layers"]
Technical: --ar 2.25:1 --v 6.0 --style raw --quality 2 --stylize 250 --no photorealistic

中文释义：
[详细的中文释义，描述封面图要展示的系列文章整体概念和核心价值]
```
```

**Cover image generation guidelines:**
- 基于所有优化后的文章内容，提取共同主题和核心价值
- 突出系列文章的连贯性和系统性
- 使用技术栈相关的配色方案
- 封面图应能吸引目标读者，传达系列文章的价值主张
- 包含系列文章数量或章节概念的视觉暗示

**title.md 文件位置:**
- 与系列文章位于同一目录下
- 文件名固定为 `title.md`
- 每次批量优化时覆盖原有 `title.md` 文件

 

Apply these techniques where appropriate to make articles more engaging:

### 1. Jin Yong Style Narrative (金庸式笔触)

Use Jin Yong novel's narrative rhythm when describing workplace conflicts or project challenges.

**Example (Database):**
> 周五下午五点，生产数据库突然卡死，用户投诉电话此起彼伏。你打开监控面板，发现……

**Example (DevOps):**
> 部署窗口只剩十分钟，Kubernetes 集群突然告警。Pod 一个接一个崩溃，你看着日志，心跳加速……

### 2. Historical Analogies (借古喻今)

Use Chinese historical allusions, poetry, or military strategy to elevate technical or business logic.

**Example (General):**
> 兵法云："知己知彼，百战不殆。" 在系统优化中，了解你的对手（瓶颈）比了解自己更重要。

**Example (LLM):**
> 古人云："温故而知新。" 在大模型时代，RAG 技术正是这一智慧的现代演绎——让 AI 在历史知识中寻找答案。

### 3. Liejin Technique (列锦手法)

List multiple images or nouns in parallel without verbs or connectors, creating atmosphere through意象叠加.

**Example (Database):**
> 会话、进程、锁——三张网，一个困局。

**Example (Kubernetes):**
> Pod、Service、Ingress——三层架构，一个世界。

**Example (LLM):**
> Prompt、Context、Temperature——三个参数，无限可能。

### 4. Materialization Technique (物化手法)

Transform abstract concepts, emotions, or thoughts into concrete, perceptible objects.

**Example (Database):**
> 性能瓶颈像一道无形的墙，挡在用户和数据之间。

**Example (LLM):**
> 模型的知识边界像一张看不见的网，网住了已知，却漏掉了未知。

**Example (Kubernetes):**
> 容器就像一个个独立的房间，共享着同一栋大楼的基础设施。

### 5. Metaphors and Analogies (比喻与类比)

Connect complex technical concepts to everyday life.

**Example (Database):**
> Buffer Cache 就像图书馆的阅览室——热门书放在桌上（内存），冷门书要去书架（磁盘）找。

**Example (Redis):**
> Redis 就像你的办公桌——常用的东西伸手就能拿到，不常用的东西要起身去文件柜找。

**Example (LLM):**
> Prompt 就像给 AI 的指令书——写得越清楚，AI 执行得越准确。

**Example (Kubernetes):**
> Deployment 就像自动化的军队——指挥官发布命令，士兵自动执行，伤亡了自动补充。

### 6. Question and Answer (设问与自答)

Guide thinking through questions, then provide answers.

**Example (Database):**
> 为什么同一个 SQL，有时快如闪电，有时慢如蜗牛？答案藏在执行计划里。

**Example (LLM):**
> 为什么同一个 Prompt，有时回答精准，有时胡言乱语？答案藏在 Temperature 参数里。

**Example (Kubernetes):**
> 为什么 Pod 重启了，数据却还在？答案藏在 Volume 的持久化机制里。

### 7. Contrast and Antithesis (对比与反差)

Highlight differences through comparison to deepen understanding.

**Example (Database):**
> V$SESSION 是实时快照，一秒一变；DBA_HIST_ACTIVE_SESS_HISTORY 是历史档案，一小时一张。

**Example (MySQL):**
> InnoDB 支持事务，适合写多读少；MyISAM 不支持事务，适合读多写少。

**Example (LLM):**
> GPT-4 像一位博学的教授，知识渊博但有时过于谨慎；Claude 像一位聪明的助手，反应敏捷但有时不够深入。

**Example (Kubernetes):**
> Docker 是容器引擎，负责运行单个容器；Kubernetes 是容器编排，负责管理成千上万个容器。

### 8. Progressive Layering (层递与递进)

Deepen understanding through logical sequence.

**Example (Database):**
> 先看会话是谁，再看他在干什么，最后看他干了多久——三步定位问题会话。

**Example (LLM):**
> 先理解用户意图，再检索相关知识，最后生成回答——三步完成 RAG 流程。

**Example (Kubernetes):**
> 先定义 Pod，再创建 Service，最后配置 Ingress——三步暴露应用。

### 9. Scenario-Based Narrative (场景化叙事)

Place technical problems in specific scenarios.

**Required Elements:**
- **Time**: Specific time (e.g., "周一上午9点", "周三下午3点")
- **Characters**: Specific roles (e.g., "产品经理", "运维群", "开发")
- **Dialogue**: Direct quotes (e.g., "AI 助手怎么这么慢？")
- **Data**: Concrete numbers (e.g., "2秒→200ms", "95%使用率")
- **Action**: Specific steps taken (e.g., "调整SGA参数", "重构索引")

**Transformation Example:**
Before: "周一上午发现查询变慢了，调整参数后恢复正常。"
After: "周一上午9点，产品经理冲进办公室：'AI助手怎么这么慢？'你调整SGA参数，五分钟后响应从2秒降回200ms。"

**Example (Database):**
> 周五下午五点，生产系统突然卡死，用户投诉电话此起彼伏。你打开数据库，发现……（具体时间、角色、数据）

**Example (LLM):**
> 客户要求 AI 助手能回答公司内部文档的问题。你尝试了直接提问，效果很差。这时，你想起了 RAG 技术……（具体对话、数据对比）

**Example (Kubernetes):**
> 新版本上线后，流量突然激增，Pod 开始崩溃。你看着 HPA 自动扩容，但数据库连接数已经爆满……（具体时间、数据、操作步骤）

### 10. Quantified Expression (数字化表达)

Use numbers to enhance persuasiveness and readability.

**Format Rules:**
- Use Arabic numerals: "3个指标" not "三个指标"
- Use concise format: "3个指标，1行SQL，10秒出结果"
- Emphasize key numbers: Bold critical thresholds (e.g., **90% 红色警戒线**)
- Use comparison: "2秒→200ms", "100ms→500ms"

**Example (Database):**
> 三个视图、五步排查、十种等待——掌握这些，你就是性能专家。

**Example (LLM):**
> 三个参数、五步优化、十种技巧——掌握这些，你就是 Prompt 工程师。

**Example (Kubernetes):**
> 三个资源、五步部署、十种监控——掌握这些，你就是 K8s 专家。

**Transformation Example:**
Before: "查询速度提升了，响应时间变短了。"
After: "响应时间从2秒降至200ms，提升**90%**。"

### 11. Citations and Authority (引用与权威)

Quote official documentation or expert opinions to enhance credibility.

**Example (Database):**
> Oracle 官方文档明确指出："V$ACTIVE_SESSION_HISTORY 每秒采样一次……"

**Example (LLM):**
> OpenAI 官方文档建议："Temperature 设置在 0.7 左右时，模型在创造性和准确性之间达到最佳平衡。"

**Example (Kubernetes):**
> Kubernetes 官方文档强调："Pod 是 Kubernetes 中最小的可部署单元。"

### 12. Suspense and Foreshadowing (悬念与伏笔)

Set suspense at the beginning to guide readers to continue.

**Example (Database):**
> 一条 SQL 执行了 3 小时还没结束，但 CPU 使用率只有 5%。问题出在哪里？答案可能让你意外。

**Example (LLM):**
> 同一个 Prompt，在 GPT-4 上回答完美，在 Claude 上却答非所问。问题出在哪里？答案藏在模型训练数据里。

**Example (Kubernetes):**
> 你的应用在本地运行完美，部署到 Kubernetes 后却无法访问。问题出在哪里？答案可能让你意外。

### 13. Summary and Elevation (总结与升华)

Extract key points at the end to elevate article value.

**Example (Database):**
> 掌握了这些视图，你不再是被动救火的消防员，而是主动预防的架构师。

**Example (LLM):**
> 掌握了这些技巧，你不再是盲目试错的 Prompt 新手，而是精准调优的 AI 工程师。

**Example (Kubernetes):**
> 掌握了这些概念，你不再是手动部署的运维人员，而是自动化编排的云原生工程师。

### 14. Code and Text Interleaving (代码与文字穿插)

Support text explanations with code examples.

**Example (Database):**
> 理论说再多，不如看代码：
> ```sql
> SELECT * FROM v$session WHERE status = 'ACTIVE';
> ```

**Example (LLM):**
> 理论说再多，不如看代码：
> ```python
> response = client.chat.completions.create(
>     model="gpt-4",
>     messages=[{"role": "user", "content": prompt}],
>     temperature=0.7
> )
> ```

**Example (Kubernetes):**
> 理论说再多，不如看代码：
> ```yaml
> apiVersion: apps/v1
> kind: Deployment
> metadata:
>   name: my-app
> spec:
>   replicas: 3
> ```

### 15. Reverse Metaphor (逆喻)

Combine two seemingly contradictory or unreasonable words together, creating deeper and more accurate meaning through collision.

**Example (Database):**
> 生命是一袭华美的袍，爬满了蚤子。

**Example (LLM):**
> 模型是一座宏伟的图书馆，却锁住了所有的书。

**Example (Kubernetes):**
> 自动化是一把锋利的剑，却砍向了运维的双手。

### 16. Tail-Biting Sentences (咬尾句)

Sentences are strung together like a thread, the tail of the previous sentence biting the mouth of the next, one link biting another, inescapable.

**Example (Database):**
> 我划亮一根火柴，火柴烧到指尖，指尖一抖，抖落的火星没点燃以前。

**Example (LLM):**
> 我输入一个 Prompt，Prompt 唤醒模型，模型生成回答，回答引发思考，思考又催生新的 Prompt。

**Example (Kubernetes):**
> 我部署一个 Pod，Pod 启动容器，容器运行应用，应用暴露服务，服务接收流量，流量触发扩容，扩容又创建新的 Pod。

## Technology-Specific Guidelines

### Database Articles

**Validation:**
- SQL syntax correctness
- View/table/column names accuracy
- Version compatibility annotations
- Index usage and performance considerations

**Common Techniques:**
- Use database-specific analogies (Buffer Cache, WAL, MVCC)
- Reference official documentation
- Include performance tuning tips

### DevOps & Infrastructure Articles

**Validation:**
- YAML/JSON syntax correctness
- Command syntax and flags
- API names and parameters
- Best practices compliance

**Common Techniques:**
- Use infrastructure analogies (Pods, Services, Deployments)
- Reference official documentation
- Include troubleshooting steps

### LLM & AI Articles

**Validation:**
- API call syntax correctness
- Parameter names and ranges
- Model capabilities and limitations
- Best practices for prompt engineering

**Common Techniques:**
- Use AI-specific analogies (Temperature, Context, Embeddings)
- Reference model documentation
- Include prompt optimization tips

### Visualization & Documentation Articles

**Validation:**
- Diagram syntax correctness (Mermaid, PlantUML)
- Element relationships accuracy
- Best practices for diagram design

**Common Techniques:**
- Use visualization analogies (Flowcharts, Sequence Diagrams)
- Reference diagram syntax documentation
- Include design tips

## Polish Intensity Levels

### Light Polish (轻度润色)

- Use 2-3 literary techniques
- 3-5 applications per article
- Maintain original style
- Generate 3 alternative titles
- Add image prompts only if explicitly requested

### Standard Polish (标准润色)

- Use 5-7 literary techniques
- 8-12 applications per article
- Moderately enhance readability
- Generate 5 alternative titles
- Add 1-2 image prompts at key positions if article length > 800 words

### Deep Polish (深度润色)

- Use 8-10 literary techniques
- 15-20 applications per article
- Significantly enhance readability
- Generate 5 alternative titles
- Add 3-5 image prompts at strategic positions (concept introduction, workflow explanation, comparison)

## Technical Validation

### Version Compatibility Annotations

Always annotate code snippets with version compatibility when applicable:

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

### Validation Script

Use the validation script for technical accuracy:

```bash
python scripts/validate-technical-accuracy.py /path/to/article.md
```

**Validation checks:**
- Code syntax correctness (SQL, Python, YAML, etc.)
- Command syntax and flags
- API names and parameters
- Version compatibility annotations
- Technology-specific best practices

**Supported technologies:**
- Oracle (SQL, PL/SQL, Performance Views)
- MySQL (SQL, Performance Schema)
- PostgreSQL (SQL, pg_stat views)
- Kubernetes (YAML, K8s resources)
- LLM (Python, API calls)
- Mermaid (Diagram syntax)

### Batch Validation Script

Validate multiple articles in parallel with progress tracking:

```bash
python scripts/batch-validate.py /path/to/directory --tech Oracle --workers 4 --output report.json
```

**Features:**
- Parallel processing with configurable workers
- Progress tracking and resumption
- Detailed JSON report generation
- Error recovery and retry

**Options:**
- `--tech <technology>`: Specify technology for all files
- `--workers <n>`: Number of parallel workers (default: 4)
- `--resume`: Resume from previous progress
- `--output <file>`: Save report to JSON file
- `--recursive`: Search directory recursively (default: true)

### Quality Control Script

Analyze literary techniques and readability:

```bash
python scripts/quality-control.py /path/to/article.md --output report.json
```

**Analysis includes:**
- Literary technique detection (列锦、物化、金庸式笔触、比喻、拟人、排比、设问、反问)
- Readability metrics (sentence length, word length, vocabulary richness)
- Readability score (0-100) and grade level
- Improvement suggestions

**Output:**
- Console report with detailed metrics
- JSON report for further analysis
- Specific suggestions for improvement

## Output Format

### Single File Output

After modifying the file directly, provide a brief summary:

```markdown
✅ 润色完成

文件：/path/to/article.md
修改内容：
- 应用 [数量] 种文学手法
- 添加 [数量] 个图片生成提示词
- 验证 [数量] 个代码片段
- 生成 [数量] 个备选标题（已插入文章开头）
```

**Note**: Candidate titles are inserted at the beginning of the article for easy reference.

### Batch Processing Output

```markdown
## 润色进度

✅ 第 04 篇：[标题] - 已完成
✅ 第 05 篇：[标题] - 已完成
...
✅ 第 22 篇：[标题] - 已完成

## 总结

共润色 19 篇文章，所有文章已直接修改并保存到原目录。
```

## Error Handling

### File Read Errors

If file cannot be read:
1. Check file path correctness
2. Verify file existence
3. Check file permissions

### Technical Validation Errors

If technical issues are found:
1. List all issues with line numbers
2. Provide suggested fixes
3. Ask user whether to continue

### Technology Detection Errors

If technology domain cannot be detected:
1. Ask user to specify the technology
2. Analyze code snippets and terminology
3. Provide technology-specific guidance

## Quality Control

### Pre-Polish Checklist

- [ ] Read and understand original content
- [ ] Identify technology domain
- [ ] Note version-specific features
- [ ] Plan literary technique usage
- [ ] Verify code snippets accuracy

### Post-Polish Checklist

- [ ] Technical accuracy maintained
- [ ] Article structure preserved
- [ ] Readability enhanced
- [ ] Literary techniques natural
- [ ] Formatting consistent
- [ ] Titles high-quality
- [ ] Technology-specific guidelines followed
- [ ] Code snippets validated
- [ ] Version compatibility annotated
- [ ] Quality control analysis completed

## Scripts Directory

The `scripts/` directory contains utility scripts for validation and quality control:

### validate-technical-accuracy.py

Validates technical accuracy of code snippets in articles.

**Usage:**
```bash
python scripts/validate-technical-accuracy.py /path/to/article.md [options]
```

**Options:**
- `--tech <technology>`: Specify technology (Oracle, MySQL, PostgreSQL, Kubernetes, LLM, Mermaid)
- `--verbose`: Show detailed validation output

**Features:**
- Automatic technology detection
- Code syntax validation
- Version compatibility checking
- Technology-specific validation rules

### batch-validate.py

Validates multiple articles in parallel with progress tracking.

**Usage:**
```bash
python scripts/batch-validate.py <file_or_directory> [options]
```

**Options:**
- `--tech <technology>`: Specify technology for all files
- `--workers <n>`: Number of parallel workers (default: 4)
- `--resume`: Resume from previous progress
- `--output <file>`: Save report to JSON file
- `--recursive`: Search directory recursively (default: true)

**Features:**
- Parallel processing with configurable workers
- Progress tracking and resumption
- Detailed JSON report generation
- Error recovery and retry

### quality-control.py

Analyzes literary techniques and readability of articles.

**Usage:**
```bash
python scripts/quality-control.py /path/to/article.md [options]
```

**Options:**
- `--output <file>`: Save report to JSON file

**Features:**
- Literary technique detection (列锦、物化、金庸式笔触、比喻、拟人、排比、设问、反问)
- Readability metrics (sentence length, word length, vocabulary richness)
- Readability score (0-100) and grade level
- Improvement suggestions

## Reference Materials

### Detailed Examples

See [references/examples.md](references/examples.md) for:
- Single file polish examples
- Batch processing examples
- Advanced usage patterns
- Error handling examples
- Technology-specific examples

### Quality Control Standards

See [references/quality-control.md](references/quality-control.md) for:
- Technical accuracy validation
- Literary technique usage guidelines
- Structure integrity checks
- Title generation standards
- Technology-specific quality criteria

### Technology Guides

See [references/technology-guides.md](references/technology-guides.md) for:
- Database technology guides (Oracle, MySQL, PostgreSQL)
- DevOps technology guides (Kubernetes, Docker, Terraform)
- AI/LLM technology guides (Prompt Engineering, RAG)
- Visualization guides (Mermaid, PlantUML)
- Programming language guides (Python, Java, Go)

## Guidelines

- **Preserve technical accuracy**: Never compromise technical correctness for literary effect
- **Use techniques judiciously**: Not every section needs every technique—apply where natural
- **Maintain original structure**: Keep the article's logical flow and organization
- **Be concise**: Avoid over-polishing that makes content verbose
- **Know your audience**: IT professionals appreciate depth but value clarity
- **Validate technical content**: Always verify code snippets and technology-specific content
- **Annotate version compatibility**: Clearly mark version-specific features
- **Generate quality titles**: Create engaging, shareable titles that reflect core value
- **Adapt to technology**: Use technology-appropriate examples, analogies, and terminology
- **Stay current**: Keep up with technology updates and best practices

## Image Prompt Template

### Standard Prompt Structure

All image generation prompts must follow this structure:

```markdown
```image-prompt
用途：[简短描述图片用途，1-2句话]
工具：Midjourney / DALL-E 3 / Flux（生成 4K HD 质量图片）
图片路径：./img/[文章序列号]-[图片名].png（例如：01-oracle-memory-architecture.png）

Prompt (英文):
Subject: [核心主体描述]
Details:
- [细节1]
- [细节2]
- [细节3]
Style: [风格描述]
Colors: [颜色方案]
Visual Flow: [视觉流向]
Key Elements: [关键元素强调]
Technical: [技术参数，包含 4K HD 质量，如 --ar 16:9 --v 6.0 --style raw --quality 2 --stylize 250]

中文释义：
[详细的中文释义，解释图片要展示的内容，3-5句话]
```
```

### Example: Oracle Architecture Diagram

```markdown
```image-prompt
用途：Oracle 内存架构演进图
工具：Midjourney / DALL-E 3 / Flux（生成 4K HD 质量图片）
图片路径：./img/oracle-memory-architecture-evolution-01.png

Prompt (英文):
Subject: A technical diagram showing Oracle Memory Architecture evolution from 11g to 26ai.
Details:
- Left section (11g): Show SGA (System Global Area) with Buffer Cache, Shared Pool, Large Pool, Java Pool. Visual: Database cylinder labeled "SGA" with internal compartments.
- Middle section (19c): Show In-Memory Column Store (IMCS) added above SGA. Visual: Orange cylinder labeled "In-Memory Store" with column icons inside.
- Right section (26ai): Show Vector Memory Pool and AI-specific structures. Visual: Purple cylinder labeled "Vector Pool" with neural network icons and vector representations.
- Show evolution arrows between sections with labels "11g → 19c → 26ai"
- Bottom: Show PGA (Program Global Area) as foundation layer across all versions
Style: Modern technical infographic with clean lines and professional enterprise software aesthetic. Flat design with subtle gradients and depth. Similar to Oracle Cloud documentation graphics. Ultra high definition for 4K HD quality.
Colors: Oracle red (#C74634) for SGA components, orange (#E67E22) for In-Memory Store, purple (#9B59B6) for Vector Pool, blue (#3498DB) for PGA, gold (#F1C40F) for AI/intelligence features. Background: clean white/light gray (#ECF0F1).
Visual Flow: Left-to-right evolution. Use arrows and connecting lines to show architectural progression.
Key Elements: Emphasize the new components added in each version (IMCS in 19c, Vector Pool in 26ai). Show the foundational PGA layer consistently across all versions.
Technical: --ar 16:9 --v 6.0 --style raw --quality 2 --stylize 250 --no photorealistic

中文释义：
技术图，展示 Oracle 内存架构从 11g 到 26ai 的演进。
- 左侧部分（11g）：显示 SGA（系统全局区）及其组件（Buffer Cache、Shared Pool、Large Pool、Java Pool）。视觉：标记为"SGA"的数据库圆柱体，内部有多个隔间。
- 中间部分（19c）：显示在 SGA 之上添加的内存列存储（IMCS）。视觉：标记为"In-Memory Store"的橙色圆柱体，内部有列图标。
- 右侧部分（26ai）：显示向量内存池和 AI 专用结构。视觉：标记为"Vector Pool"的紫色圆柱体，内部有神经网络图标和向量表示。
- 显示各部分之间的演进箭头，标签为"11g → 19c → 26ai"
- 底部：显示 PGA（程序全局区）作为所有版本的基础层
风格：现代技术信息图，干净的线条，专业的企业软件美学。扁平设计，微妙的渐变和深度。类似于 Oracle Cloud 文档图形。
颜色：Oracle 红色用于 SGA 组件，橙色用于内存列存储，紫色用于向量池，蓝色用于 PGA，金色用于 AI/智能功能。背景：干净的白色/浅灰色。
视觉流向：从左到右的演进。使用箭头和连接线显示架构演进。
关键元素：强调每个版本中添加的新组件（19c 中的 IMCS，26ai 中的 Vector Pool）。显示 PGA 基础层在所有版本中的一致性。
```
```

### Example: Kubernetes Deployment Flow

```markdown
```image-prompt
用途：Kubernetes 部署流程图
工具：Midjourney / DALL-E 3 / Flux（生成 4K HD 质量图片）
图片路径：./img/kubernetes-deployment-workflow-01.png

Prompt (英文):
Subject: A process flow diagram showing Kubernetes deployment workflow from YAML to running Pods.
Details:
- Step 1 (YAML Input): Show a code editor icon with YAML code snippet. Label: "Deployment YAML"
- Step 2 (API Server): Show Kubernetes API server as a gateway icon. Arrow from YAML to API Server labeled "kubectl apply"
- Step 3 (Controller): Show Deployment Controller as a gear icon. Arrow from API Server to Controller labeled "Validate"
- Step 4 (Scheduler): Show Scheduler as a clock icon. Arrow from Controller to Scheduler labeled "Assign Node"
- Step 5 (Kubelet): Show Kubelet as a worker icon on a Node box. Arrow from Scheduler to Kubelet labeled "Pull Image & Start"
- Step 6 (Pod Running): Show 3 running Pods as rounded rectangles with application icons inside. Arrow from Kubelet to Pods labeled "Running"
- Bottom: Show cluster diagram with 3 Nodes, each containing multiple Pods
Style: Modern technical flowchart with clean icons and arrows. Professional cloud-native documentation style. Similar to Kubernetes documentation. Ultra high definition for 4K HD quality.
Colors: Kubernetes blue (#326CE5) for core components, green (#00C853) for successful states, gray (#607D8B) for infrastructure, orange (#FF9800) for actions. Background: clean white (#FFFFFF).
Visual Flow: Top-to-bottom workflow with numbered steps. Use arrows and labels to show data flow.
Key Elements: Emphasize the transformation from YAML configuration to running Pods. Show the numbered steps clearly. Highlight the role of each component (API Server, Controller, Scheduler, Kubelet).
Technical: --ar 16:9 --v 6.0 --style raw --quality 2 --stylize 250 --no photorealistic

中文释义：
流程图，展示 Kubernetes 部署工作流程，从 YAML 到运行中的 Pod。
- 步骤 1（YAML 输入）：显示带有 YAML 代码片段的代码编辑器图标。标签："Deployment YAML"
- 步骤 2（API Server）：显示 Kubernetes API Server 作为网关图标。从 YAML 到 API Server 的箭头标记为"kubectl apply"
- 步骤 3（Controller）：显示 Deployment Controller 作为齿轮图标。从 API Server 到 Controller 的箭头标记为"Validate"
- 步骤 4（Scheduler）：显示 Scheduler 作为时钟图标。从 Controller 到 Scheduler 的箭头标记为"Assign Node"
- 步骤 5（Kubelet）：显示 Kubelet 作为节点框上的工人图标。从 Scheduler 到 Kubelet 的箭头标记为"Pull Image & Start"
- 步骤 6（Pod 运行）：显示 3 个运行的 Pod，作为带有应用图标的圆角矩形。从 Kubelet 到 Pod 的箭头标记为"Running"
- 底部：显示集群图，包含 3 个节点，每个节点包含多个 Pod
风格：现代技术流程图，干净的图标和箭头。专业的云原生文档风格。类似于 Kubernetes 文档。
颜色：Kubernetes 蓝色用于核心组件，绿色用于成功状态，灰色用于基础设施，橙色用于操作。背景：干净的白色。
视觉流向：从上到下的工作流程，带有编号步骤。使用箭头和标签显示数据流。
关键元素：强调从 YAML 配置到运行 Pod 的转换。清晰显示编号步骤。突出每个组件的角色（API Server、Controller、Scheduler、Kubelet）。
```
```
```

### Example: LLM RAG Architecture

```markdown
```image-prompt
用途：LLM RAG 架构图
工具：Midjourney / DALL-E 3 / Flux（生成 4K HD 质量图片）
图片路径：./img/llm-rag-architecture-01.png

Prompt (英文):
Subject: A conceptual architecture diagram showing RAG (Retrieval Augmented Generation) workflow for LLM applications.
Details:
- Left Section (User Query): Show a user icon with a speech bubble containing "Query about company documents". Arrow pointing to the Embedding Model.
- Middle Top Section (Embedding Model): Show a neural network icon labeled "Embedding Model". Two inputs: User Query (arrow from left) and Document Database (arrow from bottom). Output: Vector representation as a vertical bar chart with values [0.1, 0.9, 0.3, 0.7...].
- Middle Bottom Section (Vector Database): Show a database cylinder labeled "Vector Store" with multiple vector representations inside. Show similarity search icon (magnifying glass with vectors) finding the top-k similar vectors.
- Right Section (LLM Generation): Show a large AI brain icon labeled "LLM". Two inputs: Original User Query (dotted arrow from left) and Retrieved Context (arrow from Vector Database). Output: Generated Response in a text bubble.
- Visual flow: Left-to-right. Use arrows and connecting lines to show the complete RAG pipeline.
- Key elements: Emphasize the two-step process: (1) Retrieval from Vector Database, (2) Augmented Generation by LLM.
Style: Modern technical diagram with clean lines and professional AI/ML documentation aesthetic. Flat design with subtle gradients. Similar to OpenAI or Anthropic documentation graphics. Ultra high definition for 4K HD quality.
Colors: Purple (#9B59B6) for neural network/AI components, blue (#3498DB) for database/vector storage, green (#27AE60) for successful retrieval, gold (#F1C40F) for LLM generation, gray (#7F8C8D) for user inputs. Background: clean white/light gray (#ECF0F1).
Visual Flow: Left-to-right pipeline. Use arrows and labels to show data transformation.
Key Elements: Emphasize the embedding transformation (text → vectors), the vector similarity search, and the context-augmented LLM generation. Show the separation between retrieval and generation phases.
Technical: --ar 16:9 --v 6.0 --style raw --quality 2 --stylize 250 --no photorealistic

中文释义：
概念架构图，展示 RAG（检索增强生成）用于 LLM 应用的完整工作流程。
- 左侧部分（用户查询）：显示用户图标，带有包含"Query about company documents"的对话气泡。箭头指向嵌入模型。
- 中上部分（嵌入模型）：显示标记为"Embedding Model"的神经网络图标。两个输入：用户查询（来自左侧的箭头）和文档数据库（来自底部的箭头）。输出：向量表示为垂直条形图，值为 [0.1, 0.9, 0.3, 0.7...]。
- 中下部分（向量数据库）：显示标记为"Vector Store"的数据库圆柱体，内部有多个向量表示。显示相似度搜索图标（带有向量的放大镜）找到前 k 个相似向量。
- 右侧部分（LLM 生成）：显示标记为"LLM"的大型 AI 大脑图标。两个输入：原始用户查询（来自左侧的虚线箭头）和检索到的上下文（来自向量数据库的箭头）。输出：文本气泡中的生成响应。
- 视觉流向：从左到右。使用箭头和连接线显示完整的 RAG 管道。
- 关键元素：强调两步流程：(1) 从向量数据库检索，(2) 由 LLM 进行增强生成。
风格：现代技术图，干净的线条，专业的 AI/ML 文档美学。扁平设计，微妙的渐变。类似于 OpenAI 或 Anthropic 文档图形。
颜色：紫色用于神经网络/AI 组件，蓝色用于数据库/向量存储，绿色用于成功检索，金色用于 LLM 生成，灰色用于用户输入。背景：干净的白色/浅灰色。
视觉流向：从左到右的管道。使用箭头和标签显示数据转换。
关键元素：强调嵌入转换（文本 → 向量）、向量相似度搜索和上下文增强的 LLM 生成。显示检索和生成阶段之间的分离。
```
```

## Prompt Generation Best Practices

### 1. Context Awareness
- Read 5-10 lines before and after the target position
- Understand the technical concept being explained
- Identify the audience level (beginner, intermediate, advanced)

### 2. Visual Clarity
- Use simple, clean visual elements
- Avoid overcrowding the diagram
- Maintain consistent iconography throughout the article

### 3. Color Consistency
- Use technology-specific color schemes
- Maintain consistent color usage across multiple images in the same article
- Ensure high contrast for accessibility

### 4. Technical Accuracy
- Ensure visual representation matches the technical description
- Verify all labels and terminology are correct
- Cross-reference with official documentation when applicable

### 5. Narrative Flow
- Position images at natural breakpoints in the narrative
- Use images to support, not replace, textual explanations
- Ensure the image enhances understanding of the surrounding content

### 6. Prompt Quality
- Be specific about visual elements (icons, shapes, colors)
- Include style references (e.g., "similar to Oracle Cloud documentation")
- Specify technical parameters (aspect ratio, version, style settings, 4K HD quality)
- Always include quality parameters: `--quality 2 --stylize 250` for 4K HD output
- Add "Ultra high definition for 4K HD quality" to style descriptions
- Provide detailed Chinese translation for all elements

### 7. Standardization
- Follow the standard prompt structure consistently
- Use the same format for all image prompts in the same article
- Maintain code block wrapper (```image-prompt``` ...) for all prompts
- Include horizontal lines (------) before and after image markdown
- Always include image placeholder path (./img/[文章序列号]-[图片名].png)
- 从文章文件名中提取序列号（如 "01-xxx.md" 中的 "01"），作为图片路径的前缀

## Common Image Types and Prompt Templates

### Architecture Diagram
Use for: System architecture, component relationships, infrastructure design

**Key elements:**
- Component boxes with labels
- Connection arrows with labels
- Hierarchical or layered structure
- Data flow indicators

### Process Flow
Use for: Workflow steps, deployment pipelines, data transformation

**Key elements:**
- Numbered steps
- Directional arrows
- Input/output indicators
- Decision points (if applicable)

### Comparison Diagram
Use for: Technology comparisons, before/after scenarios, pros/cons

**Key elements:**
- Side-by-side layout
- Highlighted differences
- Comparison labels
- Color coding for different options

### Concept Visualization
Use for: Abstract concepts, mental models, metaphors

**Key elements:**
- Metaphorical visual representation
- Simplified abstract elements
- Clear labeling
- Contextual indicators

### Timeline/Evolution
Use for: Technology evolution, version history, growth stages

**Key elements:**
- Timeline axis
- Version labels
- Feature highlights
- Progression arrows

## Related Skills

- **`wechat-workflow:reviewing-technical-accuracy`** - Use after polishing to perform comprehensive technical audit and validate claims
- **`wechat-workflow:generating-article-images`** - Use after polishing to generate images from the image prompts created by this skill
- **`wechat-workflow:converting-to-wechat`** - Use to convert polished Markdown articles to WeChat HTML format (includes v3.0 professional style preset)
