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
