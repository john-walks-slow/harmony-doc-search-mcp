# harmony-doc-search-mcp

一个基于 **FastMCP** 的 HarmonyOS 官方文档搜索 MCP 服务。

它会调用华为开发者社区搜索接口，查询：

- HarmonyOS NEXT 官方 API 文档
- ArkTS 语法资料
- ArkUI 组件与用法文档

## 功能

- 提供 `search_harmonyos_api` MCP 工具
- 支持 `query / offset / length` 分页参数
- 自动读取环境变量代理（`HTTPS_PROXY` / `HTTP_PROXY`）
- 支持通过环境变量控制 SSL 校验
- 可直接用 `uv` 运行与管理依赖

## 项目结构

```text
.
├── pyproject.toml
├── README.md
├── .gitignore
├── src/
│   └── harmony_doc_search_mcp/
│       ├── __init__.py
│       └── server.py
└── examples/
    └── mcp-config.json
```

## 环境要求

- Python 3.10+
- [uv](https://github.com/astral-sh/uv)

## 安装

```bash
uv sync
```

## 启动

```bash
uv run harmony-doc-search-mcp
```

## MCP 客户端配置示例

`examples/mcp-config.json`

```json
{
  "mcpServers": {
    "harmony-doc-search": {
      "command": "uv",
      "args": [
        "run",
        "harmony-doc-search-mcp"
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

## MCP Tool

### `search_harmonyos_api(query: str, offset: int = 0, length: int = 15)`

用于搜索鸿蒙官方文档，返回标题、摘要与链接。

示例：

- `search_harmonyos_api("Navigation")`
- `search_harmonyos_api("ArkTS 状态管理", 0, 10)`

## 开发

```bash
uv sync --dev
uv run ruff check .
```

## 说明

原始版本中使用了 `verify=False`。当前版本改为默认校验证书，如确实需要关闭，可设置：

```bash
export HARMONY_DOC_VERIFY_SSL=false
```
