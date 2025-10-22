# Knit MCP Demo

一个使用 FastAPI 提供简单控制面与 Python MCP SDK 提供示例工具/资源的最小演示。

## 安装依赖

建议使用虚拟环境，并安装 `pyproject.toml` 中的依赖：

```bash
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
pip install -e .             # 或者: pip install -r <生成的锁文件>
```

或使用 uv：

```bash
uv pip install -e .
```

## 运行 FastAPI 服务

```bash
uvicorn main:app --reload
```

- 健康检查：`GET /health`
- 注册工具：`POST /register`
- 列出工具：`GET /tools`

示例注册请求：

```json
{
  "name": "DemoServer",
  "version": "0.1.0",
  "tools": [
    {
      "name": "echo",
      "description": "Echo a message",
      "input_schema": {"type": "object", "properties": {"message": {"type": "string"}}}
    },
    {
      "name": "add",
      "description": "Add two numbers",
      "input_schema": {
        "type": "object",
        "properties": {"a": {"type": "number"}, "b": {"type": "number"}}
      }
    }
  ]
}
```

## 运行与测试 MCP 服务器（示例）

本仓库提供 `server.py`，定义了两个工具与一个资源，基于 `mcp` 官方 Python SDK。

- 直接以 stdio 运行（便于 MCP Inspector 或客户端调试）：

```bash
python server.py
# 或
uv run python server.py
```

- 配合 MCP Inspector（需安装 npm 包 `@modelcontextprotocol/inspector`）：

```bash
npx @modelcontextprotocol/inspector
# 按提示选择 STDIO，命令行可设置为: uv run python server.py
```

## 运行测试

```bash
pytest
```

测试覆盖：
- `GET /health` 返回 200 与 `{status: "ok"}`
- `POST /register` 正常保存工具并返回注册数量
- `GET /tools` 返回已注册的工具列表