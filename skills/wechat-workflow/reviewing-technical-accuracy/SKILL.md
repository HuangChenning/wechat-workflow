---
name: reviewing-technical-accuracy
description: Use when reviewing technical content for WeChat Official Account publication. Performs comprehensive technical audit using WebSearch to verify claims, check version compatibility, validate code syntax, and ensure terminology accuracy. Supports: Oracle, MySQL, PostgreSQL, MongoDB, Redis, Elasticsearch, Kubernetes, Docker, LLM, and more. Generates structured reports with critical errors, warnings, and suggestions.
---

# Reviewing Technical Accuracy

**Formerly known as**: `tech-content-reviewer`

This skill guides the AI to perform a rigorous technical review of technical documents. It mimics the role of a Senior Technical Editor and QA Engineer.

This skill guides the AI to perform a rigorous technical review of technical documents. It mimics the role of a Senior Technical Editor and QA Engineer.

## Workflow

Follow this process for every review request:

### 1. Discovery
- **Action**: Locate all files to be reviewed in the specified target directory or file path.
- **Tool**: Use `Glob` or `LS` to build the file list based on the user's requirements (may include markdown, text, or other file types).

### 2. Review Process (Per File)
For each identified file, perform the following steps sequentially:

#### Step A: Content Analysis
- Read the full content of the file.
- Identify **Key Technical Claims**, including:
  - Product versions (e.g., "Oracle 19c", "PostgreSQL 16", "GPT-4o")
  - Feature availability (e.g., "Vector Search was introduced in Oracle 23ai", "JSON support in MySQL 5.7")
  - Deprecations/Removals (e.g., "mysql_native_password removed in MySQL 8.4")
  - Model capabilities (e.g., "Context window size", "Multimodal support")
  - Code snippets and commands
  - Configuration parameters
  - Technical concepts and terminology

#### Step B: Verification (Crucial)
- **Action**: Verify *every* major technical claim using `WebSearch`.
- **Search Strategy**:
  - Use specific queries: `"<Product> <Version> <Feature> documentation"`, `"<Command> syntax error"`, `"<Feature> deprecated version"`.
  - **Source Priority**: Prefer official documentation (e.g., docs.oracle.com, dev.mysql.com, postgresql.org/docs, platform.openai.com) over forums, but use forums (StackOverflow) for common error patterns.
- **Verification Targets**:
  - **Conceptual Integrity**: Is the explanation theoretically correct?
  - **Technical Accuracy**: Do the commands/code work as described? Are the versions correct?
  - **Terminology**: Are standard terms used correctly? (e.g., "Parameter" vs "Argument")

#### Step C: Language & Semantics
- Check for:
  - Spelling and Typos (especially technical terms)
  - Grammar and Sentence Structure
  - Semantic Logic (Does the paragraph make logical sense?)
  - formatting issues (Broken links, malformed tables)

### 3. Reporting
Output a structured report for each file. Use the following format:

## Report: [Filename]

### 🔴 Critical Errors (Factual/Technical)
| Location | Error Description | Correct Fact | Reference/Source |
|----------|-------------------|--------------|------------------|
| Line 42  | Claimed V$XYZ is new in 19c | V$XYZ was introduced in 12c | [Oracle Docs Link](...) |
| Line 88  | JSON_TABLE not supported in PG | PostgreSQL 12+ supports json_to_recordset | [PostgreSQL Docs](...) |

### 🟡 Warnings (Language/Clarity)
- **Line 15**: Typo "Oracel" -> "Oracle".
- **Line 20**: Ambiguous phrasing. Suggested rewrite: "..."

### 🟢 Suggestions
- Consider adding a diagram for this concept.
- Code snippet on Line 50 lacks error handling.

---

## Guidelines for the Agent
1. **Be Pedantic**: Technical accuracy is paramount. If a feature was introduced in 18c but the text says 19c, flag it.
2. **Citation Required**: Never flag a technical error without providing a URL to a credible source (Official Docs preferred).
3. **Context Matters**: Consider the publication date if mentioned. "Currently" in a 2020 article means 2020, not today.
4. **Code Review**: Visually scan code snippets for obvious syntax errors or anti-patterns.

## Related Skills

- **`wechat-workflow:polishing-content`** - Use before reviewing to enhance articles with literary techniques and improve readability
- **`wechat-workflow:generating-article-images`** - Use after review to generate images from the image prompts
- **`wechat-workflow:converting-to-wechat`** - Use after review (and image generation) to convert validated Markdown to WeChat HTML format
