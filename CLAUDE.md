# Project-Specific Skills Convention

## Skill Location Policy

**ALL skills created for this project MUST be located within the project's `skills/` directory:**

```
/Users/huangchenning/个人/github/weixin-skills/skills/
```

## What This Means

When asked to create, modify, or work with skills for this weixin-skills project:

1. **DO** create project-specific skills in:
   - `/Users/huangchenning/个人/github/weixin-skills/skills/` for standalone skills
   - `/Users/huangchenning/个人/github/weixin-skills/skills/wechat-workflow/` for workflow-related skills

2. **DO NOT** create skills in the global Claude skills directory:
   - `~/.claude/skills/` - This is reserved for globally-installed, reusable skills only

## Skill Categories in This Project

### Workflow Skills (`skills/wechat-workflow/`)
- `converting-to-wechat` - Convert Markdown to WeChat format
- `extracting-wechat-styles` - Extract WeChat article styles
- `generating-article-images` - Generate images for articles using Gemini
- `polishing-content` - Polish article content
- `reviewing-technical-accuracy` - Review technical accuracy
- `using-wechat-workflow` - Main workflow orchestration

### Standalone Skills (`skills/`)
- `generating-articles-from-docs` - Generate articles from documents using NotebookLM

## Global vs Project Skills

| Aspect | Project Skills | Global Skills |
|--------|---------------|---------------|
| Location | `skills/` in project | `~/.claude/skills/` |
| Scope | Project-specific workflows | Reusable across projects |
| Examples | `generating-article-images` | `notebooklm`, `git-commit-message` |
| Installation | Run directly from project | Installed via Skill tool |

## When Working on This Project

If a user asks to create a "skill" for weixin-skills functionality:
1. Create it under the project's `skills/` directory
2. Do NOT install it globally unless explicitly requested
3. The skill can be invoked directly from its location in the project

## Exception

Only create skills in `~/.claude/skills/` when:
1. The user explicitly requests a "global skill"
2. The functionality is clearly cross-project and reusable
3. The user confirms they want it installed globally

---

## Git 同步策略

### 同步范围

**本仓库采用严格的白名单同步策略，只同步以下内容到远程仓库：**

1. **技能目录**
   - 路径：`/Users/huangchenning/个人/github/weixin-skills/skills/`
   - 内容：所有项目特定的技能文件
   - 排除：superpowers、planning-with-files、skill-creator、skills-discovery

2. **项目文档**
   - `README.md` - 项目说明文档
   - `CLAUDE.md` - 项目配置和规范文档
   - `.gitignore` - Git 忽略规则配置

### 不同步内容

以下文件和目录被排除在同步之外：

- **工作文档**：`findings.md`、`progress.md`、`task_plan.md`、`*_old.md`、`test-article.md`
- **文档目录**：`docs/` 目录及其内容
- **示例目录**：`example/` 目录及其内容
- **Oracle 相关**：`Oracle view/`、`oracle_11g_ppt_outline/` 目录
- **输出目录**：`output/` 目录
- **敏感配置**：所有 `config.yaml`、`.env`、`*.key`、`*.token` 等敏感文件
- **依赖环境**：Python 虚拟环境、`__pycache__`、构建产物等
- **IDE 配置**：`.vscode/`、`.idea/` 等编辑器配置
- **系统文件**：`.DS_Store` 等操作系统文件

### 同步命令

```bash
# 查看当前同步状态
git status

# 添加所有允许同步的文件
git add .

# 提交更改
git commit -m "描述更改内容"

# 推送到远程仓库
git push
```

### 清理已追踪但应排除的文件

如果之前已经追踪了现在需要排除的文件，执行以下命令：

```bash
# 从 Git 缓存中移除但保留本地文件
git rm -r --cached docs/
git rm --cached findings.md progress.md task_plan.md
git rm --cached *_old.md test-article.md
git rm -r --cached "Oracle view/"
git rm -r --cached oracle_11g_ppt_outline/
git rm -r --cached output/
git rm -r --cached example/

# 提交清理
git commit -m "chore: 排除不应同步的文件和目录"
```

### 注意事项

1. **敏感信息保护**：永远不要将包含敏感信息的配置文件提交到仓库
2. **技能目录管理**：新创建的技能默认会被同步，如需排除请在 `.gitignore` 中添加
3. **文档同步**：只有 `README.md` 和 `CLAUDE.md` 会被同步，其他文档请放在 `docs/` 目录（已排除）
4. **定期检查**：使用 `git status` 定期检查即将同步的文件，确保符合预期
