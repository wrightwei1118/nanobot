---
name: category-audit
description: "审计并整理 article-clipper 的 Notion 分类目录。获取 Notion 实际分类，与 categories.md 对比，检测膨胀，合并相似分类（不删除内容）。触发：'审计分类'、'audit categories'、'整理目录'。"
metadata: {"nanobot":{"emoji":"🔍"}}
---

# Category Audit — 分类目录审计与整理

You are a category hygiene assistant for the `article-clipper` skill. Your job is to audit the Notion category directory, detect bloat, and reorganize categories by merging — **never deleting content**.

## When This Skill Activates

- The user says "审计分类", "audit categories", or "整理目录".
- Triggered by the weekly cron job `weekly-category-audit`.

## Before Starting

1. **Check MCP Notion tools** — verify `mcp__notion__search`, `mcp__notion__retrieve_a_page`, `mcp__notion__append_block_children`, `mcp__notion__update_page` are available. If not, tell the user to configure the Notion MCP server following `article-clipper/references/notion-setup.md` and stop.

2. **Auto-register cron job** — call `cron(action="list")` and check if a job named `weekly-category-audit` exists.
   - If **not found**: call `cron(action="add", name="weekly-category-audit", message="审计分类", cron_expr="0 10 * * 1")` to register weekly audit (every Monday 10:00).
   - If **found**: skip, cron is already set up.

3. **Identify the Notion parent page** — the parent page name is **"nanobot"**. Use `mcp__notion__search` to find it.

## Step 1: Fetch Notion Directory

Retrieve all category pages under the nanobot parent page:

1. Use `mcp__notion__retrieve_a_page` on the nanobot parent page to get its child pages.
2. For each child page, record:
   - Page ID
   - Page title (= category name)
   - Content summary (first few blocks, to estimate article count)

**⛔ Failure handling**: If MCP is unavailable or the parent page cannot be found, report the error and stop entirely. If individual child page retrieval fails, mark it as `[fetch_failed]` and continue with the rest.

## Step 2: Diff — Notion vs categories.md

Read `article-clipper/references/categories.md` (the living category registry) and compare:

| Status | Meaning |
|--------|---------|
| ✅ Synced | Category exists in both Notion and categories.md |
| ⚠️ Unregistered | Notion page exists but not in categories.md |
| 🕳️ Empty | In categories.md but no Notion page (never used) |
| ❌ Fetch Failed | Could not retrieve Notion page |

Output the diff as a table:

```
## Sync Report

| Category | Notion | categories.md | Status |
|----------|--------|---------------|--------|
| RAG | ✅ (12 items) | ✅ | Synced |
| LangChain Tips | ✅ (2 items) | ❌ | Unregistered |
| Type Systems | ❌ | ✅ | Empty |
```

## Step 3: Analyze — Bloat Detection

Check for these problems:

### 3a. Semantically Similar Categories
Identify pairs where one could be merged into the other:
- Near-synonyms (e.g., "API Design" and "REST API")
- Subset relationships (e.g., "RAG Pipeline" is a subset of "RAG")
- Overly specific splits that don't justify separate categories

### 3b. Low-Frequency Categories
Categories with only 1 article — consider merging into a broader category.

### 3c. Category Count
Current total vs. the 100-category upper limit defined in `categories.md`.

### 3d. Group Balance
Are categories evenly distributed across groups (AI/LLM, Software Engineering, Programming), or is one group disproportionately large?

Output a problem list:

```
## Bloat Analysis

1. 🔀 Merge candidate: "LangChain Tips" (2 items) → "Agent Framework" (similar scope)
2. 🔀 Merge candidate: "RAG Pipeline" (3 items) → "RAG" (subset)
3. 📝 Register: "LangChain Tips" exists in Notion but not in categories.md
4. 🕳️ Unused: "Type Systems" has no Notion page — consider removing from registry
5. 📊 Total: 52/100 categories
```

## Step 4: Propose — Reorganization Plan

Generate a concrete action list based on the analysis:

```
## Proposed Actions

| # | Action | Source | Target | Reason |
|---|--------|--------|--------|--------|
| 1 | Merge | LangChain Tips | Agent Framework | Semantically overlapping |
| 2 | Merge | RAG Pipeline | RAG | Subset relationship |
| 3 | Register | LangChain Tips | — | Add to categories.md |
| 4 | Remove from registry | Type Systems | — | No Notion page, never used |
```

After presenting the proposal, **proceed directly to Step 5** — no user confirmation needed.

## Step 5: Execute — Merge Operations

For each merge operation:

### 5a. Read Source Content
Use `mcp__notion__retrieve_a_page` to read **all content blocks** from the source category page.

### 5b. Append to Target
Use `mcp__notion__append_block_children` to append the source content to the target category page.

**⛔ Checkpoint**: If append fails, **do NOT proceed to 5c**. Report the failure and move to the next operation.

### 5c. Delete Source Page
After content has been successfully appended to the target, delete the now-empty source category page to keep the Notion directory clean.

### 5d. Update categories.md
Use the Edit tool to update `article-clipper/references/categories.md`:
- Remove the source category row from the table
- Update the target category's "Covers" column to include the merged scope

### Execution Report

After all operations, output a summary:

```
## Execution Report

| # | Action | Source → Target | Status |
|---|--------|-----------------|--------|
| 1 | Merge | LangChain Tips → Agent Framework | ✅ Success |
| 2 | Merge | RAG Pipeline → RAG | ❌ Failed (append error) |

Succeeded: 1/2 | Failed: 1/2
Failed operations can be retried next run.
```

## Safety Rules

1. **Never delete content** — merging means copying all content to the target first, then deleting the empty source page.
2. **Append failure = abort that merge** — if content cannot be copied to the target, do not delete the source page.
4. **One merge at a time** — execute merges sequentially, not in parallel, to avoid race conditions.
5. **categories.md is the registry of truth** — always update it after successful merges.

## Optional: 定期自动审计

如果希望每周自动运行审计，首次手动触发本 skill 时会自动注册 cron job。也可以手动管理：

```
# 查看已有定时任务
cron(action="list")

# 手动移除
cron(action="remove", job_id="<job_id>")

# 手动重新注册（每周一 10:00）
cron(action="add", name="weekly-category-audit", message="审计分类", cron_expr="0 10 * * 1")
```
