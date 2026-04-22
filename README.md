# harmony-doc-search-mcp

一个基于 FastMCP 的鸿蒙开发文档搜索 MCP 服务。调用华为开发者社区搜索接口查询：

- HarmonyOS NEXT 官方 API 文档
- ArkTS 语法资料
- ArkUI 组件与用法文档

## 功能

- 提供 `search_harmonyos_api` MCP 工具
- 支持 `query / offset / length` 分页参数
- 支持代理（`HTTPS_PROXY` / `HTTP_PROXY`）

## MCP 客户端配置示例

```json
{
  "mcpServers": {
    "harmony-doc-search": {
      "command": "uvx",
      "args": [
        "git+https://github.com/john-walks-slow/harmony-doc-search-mcp@main"
      ]
    }
  }
}
```

## 可用环境变量

| 变量名 | 默认值 | 说明 |
|---|---:|---|
| `HARMONY_DOC_LANGUAGE` | `zh` | 接口语言 |
| `HARMONY_DOC_COUNTRY` | `CN` | 国家/地区 |
| `HARMONY_DOC_DEVICE_ID` | `ESN` | 请求参数中的 deviceId |
| `HARMONY_DOC_DEVICE_TYPE` | `1` | 请求参数中的 deviceType |
| `HARMONY_DOC_VERIFY_SSL` | `true` | 是否校验证书 |
| `LOG_LEVEL` | `INFO` | 日志级别 |
| `HTTPS_PROXY` / `HTTP_PROXY` | 空 | HTTP 代理 |

## 开发

```bash
uv sync --dev
uv run ruff check .
```
