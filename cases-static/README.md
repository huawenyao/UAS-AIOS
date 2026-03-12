# cases-static · StaticMCP 部署

UAS-AIOS 案例展示内容，通过 StaticMCP 协议暴露为 MCP 资源。

## 资源列表

| 资源 | 说明 |
|------|------|
| `file://uas_aios_pitch.html` | UAS-AIOS 战略简报（Pitch Deck） |
| `file://aios_business_plan.html` | UAS-AIOS 商业计划书 |

## 部署到 MCP Server

### 1. 部署静态文件

将 `cases-static/` 目录部署到任意静态托管服务：

- **GitHub Pages**：将本目录作为站点根目录或子路径
- **Vercel / Netlify**：直接部署本目录
- **其他**：任何支持静态文件的 CDN

部署后获得 base URL，例如：`https://your-domain.com/cases-static/`

### 2. 配置 Cursor MCP

在 `.cursor/mcp.json` 中添加：

```json
{
  "mcpServers": {
    "cases-static": {
      "url": "https://bridge.staticmcp.com/sse?url=https://your-domain.com/cases-static"
    }
  }
}
```

将 `https://your-domain.com/cases-static` 替换为你的实际部署 URL。

### 3. 重新构建

修改源 HTML 后，运行：

```bash
python scripts/build_cases_static.py
```

重新生成 `resources/*.json` 并重新部署。
