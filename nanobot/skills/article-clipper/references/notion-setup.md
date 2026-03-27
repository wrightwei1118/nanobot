# Notion MCP Server 配置指南

## 1. 创建 Notion Integration

1. 打开 https://www.notion.so/my-integrations
2. 点击 **"+ New integration"**
3. 填写名称（如 "Article Clipper"），选择关联的 workspace
4. 在 **Capabilities** 中确保勾选：
   - Read content
   - Update content
   - Insert content
   - Search
5. 点击 **Submit** 后复制 **Internal Integration Secret**（以 `ntn_` 开头）

## 2. 分享页面给 Integration

在 Notion 中找到你想用作文章归类根页面的页面：

1. 点击页面右上角 **"..."** → **"Connections"**
2. 搜索并添加你创建的 Integration
3. 该页面及其所有子页面将对 Integration 可见

## 3. 配置 MCP Server

在你的 Claude Code 或 nanobot 配置中添加 Notion MCP server。

### 方式 A: Claude Code settings.json

编辑 `~/.claude/settings.json`（或项目级 `.claude/settings.json`）：

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "OPENAPI_MCP_HEADERS": "{\"Authorization\":\"Bearer ntn_YOUR_API_KEY\",\"Notion-Version\":\"2022-06-28\"}"
      }
    }
  }
}
```

### 方式 B: nanobot 配置

在 nanobot 的 MCP server 配置文件中添加：

```json
{
  "notion": {
    "command": "npx",
    "args": ["-y", "@notionhq/notion-mcp-server"],
    "env": {
      "OPENAPI_MCP_HEADERS": "{\"Authorization\":\"Bearer ntn_YOUR_API_KEY\",\"Notion-Version\":\"2022-06-28\"}"
    }
  }
}
```

> 将 `ntn_YOUR_API_KEY` 替换为你的实际 API Key。

## 4. 验证配置

配置完成后，在 Claude Code 中测试：

1. 检查 MCP 工具是否可用 — 应该能看到 `mcp__notion__search` 等工具
2. 尝试搜索一个已知页面：调用 `mcp__notion__search` 搜索你的根页面名称
3. 如果返回结果，说明配置成功

## 常见问题

- **工具不可用**：确认 `npx` 可用，且 `@notionhq/notion-mcp-server` 包能正常安装
- **权限错误**：确认页面已分享给 Integration，且 API Key 正确
- **搜索无结果**：Notion 搜索 API 有延迟，新页面可能需要几秒后才能被搜到
