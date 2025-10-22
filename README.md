# Knit Pattern MCP

一个用于设计棒针编织图案的 MCP 服务器，基于 Python MCP SDK 的快速实现（STDIO 运行）。

## 功能概览

- 工具 `translate_abbrev`：翻译棒针英文缩写为中文含义
- 工具 `generate_chart`：生成常见针法的 ASCII 图表（`garter`, `stockinette`, `rib1x1`, `rib2x2`, `seed`, `lace_mesh`）
- 工具 `gauge_calc`：根据密度（每 10cm 针目/行数）计算目标尺寸的起针与行数
- 工具 `export_markdown`：将图表和图例导出为 Markdown 文本
- 资源 `pattern://{name}`：内置示例图案（`scarf_seed`, `mesh_sw`, 其他默认为 `garter`）

## 安装依赖

建议使用虚拟环境，并安装 `pyproject.toml` 中的依赖：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

或使用 uv：

```bash
uv pip install -e .
```

## 运行 MCP 服务器（STDIO）

```bash
python server.py
# 或
uv run python server.py
```

### 配合 MCP Inspector（可选）

```bash
npx @modelcontextprotocol/inspector
# 选择 STDIO 并设置命令为: uv run python server.py
```

## 工具输入与返回示例

- `translate_abbrev`
  - 输入：`"K, P, YO, k2tog"` 或 `["K", "YO"]`
  - 返回：缩写到中文含义的映射

- `generate_chart`
  - 输入：`pattern="seed", width=30, height=20`
  - 返回：包含 `chart`（二维数组），`legend`，`pattern` 等信息

- `gauge_calc`
  - 输入：`sts_per_10cm=22, rows_per_10cm=30, target_width_cm=20, target_height_cm=150`
  - 返回：`cast_on`, `row_count` 等

- `export_markdown`
  - 输入：`chart_result=generate_chart(...)`, `title="..."`
  - 返回：Markdown 文本，可直接保存或展示

- 资源 `pattern://{name}`
  - `pattern://scarf_seed`：返回 30x20 的桂花针围巾图案 Markdown
  - `pattern://mesh_sw`：返回 24x16 的网眼样片 Markdown
  - 其他名称：返回 20x20 的起伏针示例 Markdown

## 备注

- ASCII 图表以“自下而上”显示行，导出时已反转以贴合编织阅读习惯。
- `lace_mesh` 为简化网眼示例，包含 `YO` 与 `K2tog` 的重复，适合样片与练习。
- 如需扩展复杂花样（麻花、扭花等），可在 `server.py` 中新增对应的行/列变换逻辑。