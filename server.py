from typing import List, Dict, Union, TypedDict
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Knit Pattern MCP")

# 英文缩写到中文含义映射（节选与扩展）
ABBREV_MAP: Dict[str, str] = {
    "alt": "alternate，每隔一段",
    "beg": "begin，开始",
    "BO": "bind off，收针",
    "CC": "contrasting color，对比色",
    "CO": "cast on，起针",
    "cont": "continue，继续",
    "dec": "decrease，减针",
    "inc": "increase，加针",
    "K": "knit，下针",
    "k1-b": "knit one in back loop，扭下针",
    "k1f&b": "同一针织下针与扭针（加针）",
    "k2tog": "knit two together，左下二并针",
    "M1": "make 1 stitch，加一针（挑针）",
    "MC": "main color，主色",
    "p": "purl，上针",
    "p2sso": "pass 2 slipped stitches over，一次套过两滑针",
    "p2tog": "purl two together，左上二并针",
    "p3tog": "purl three together，左上三并针",
    "pm": "place marker，放记号圈",
    "psso": "pass slipped stitch over，将滑针套过左侧针",
    "pu": "pick up and knit，挑针继续织",
    "rep": "repeat，重复",
    "RS": "right side，正面",
    "s2kp": "sl 2-k1-p2sso，滑2针织1针后套过",
    "SSK": "Slip, Slip, Knit，滑滑并减针（右上并）",
    "SKP": "Slip1, knit1, pass over，右上2并1",
    "SSP": "Slip, Slip, Purl，上针右上并针",
    "YO": "yarn over，绕线加一针",
}

# 图例符号说明（用于 ASCII 图表）
LEGEND: Dict[str, str] = {
    "K": "下针",
    "P": "上针",
    "YO": "绕线加针",
    "K2tog": "左下二并针",
}

class ChartResult(TypedDict):
    pattern: str
    width: int
    height: int
    chart: List[List[str]]
    legend: Dict[str, str]


def _empty_grid(width: int, height: int, fill: str = "K") -> List[List[str]]:
    return [[fill for _ in range(width)] for _ in range(height)]


def _garter(width: int, height: int) -> List[List[str]]:
    # 起伏针：每行下针
    return _empty_grid(width, height, "K")


def _stockinette(width: int, height: int) -> List[List[str]]:
    # 平针面：正面下针，反面上针
    grid = []
    for r in range(height):
        row = ["K" if r % 2 == 0 else "P" for _ in range(width)]
        grid.append(row)
    return grid


def _rib(width: int, height: int, k: int, p: int) -> List[List[str]]:
    # 罗纹：k 个下针 + p 个上针 按列重复
    grid = []
    repeat = ["K"] * k + ["P"] * p
    for _ in range(height):
        row = [repeat[i % len(repeat)] for i in range(width)]
        grid.append(row)
    return grid


def _seed(width: int, height: int) -> List[List[str]]:
    # 桂花（moss/seed）：每针 K/P 交替，每行偏移 1
    grid = []
    for r in range(height):
        row = ["K" if (c + r) % 2 == 0 else "P" for c in range(width)]
        grid.append(row)
    return grid


def _lace_mesh(width: int, height: int) -> List[List[str]]:
    # 简单网眼：第1行重复 YO, K2tog；第2行全下针，循环
    grid = []
    for r in range(height):
        row = []
        if r % 2 == 0:
            i = 0
            while i < width:
                row.append("YO")
                if i + 1 < width:
                    row.append("K2tog")
                i += 2
            # 若宽为奇数，最后一个用 K 补齐
            if len(row) < width:
                row.append("K")
            row = row[:width]
        else:
            row = ["K" for _ in range(width)]
        grid.append(row)
    return grid


@mcp.tool()
def translate_abbrev(items: Union[str, List[str]]) -> Dict[str, str]:
    """翻译棒针英文缩写为中文含义。
    - 接受字符串或字符串列表
    - 返回缩写到中文说明的映射，未知项标注为 "未知缩写"
    """
    if isinstance(items, str):
        keys = [i.strip() for i in items.split(",") if i.strip()]
    else:
        keys = items
    result = {}
    for k in keys:
        result[k] = ABBREV_MAP.get(k, "未知缩写")
    return result


@mcp.tool()
def generate_chart(pattern: str, width: int, height: int) -> ChartResult:
    """生成常见针法的 ASCII 图表。
    支持的 pattern: garter, stockinette, rib1x1, rib2x2, seed, lace_mesh
    返回: {pattern, width, height, chart, legend}
    """
    pattern = pattern.lower()
    if pattern == "garter":
        grid = _garter(width, height)
    elif pattern == "stockinette":
        grid = _stockinette(width, height)
    elif pattern == "rib1x1":
        grid = _rib(width, height, 1, 1)
    elif pattern == "rib2x2":
        grid = _rib(width, height, 2, 2)
    elif pattern == "seed":
        grid = _seed(width, height)
    elif pattern == "lace_mesh":
        grid = _lace_mesh(width, height)
    else:
        raise ValueError("不支持的图案类型")
    return {
        "pattern": pattern,
        "width": width,
        "height": height,
        "chart": grid,
        "legend": LEGEND,
    }


@mcp.tool()
def gauge_calc(sts_per_10cm: float, rows_per_10cm: float, target_width_cm: float, target_height_cm: float) -> Dict[str, Union[int, float]]:
    """根据 10cm 密度计算起针数与行数。
    输入每 10cm 的针目与行数，以及目标宽高（cm）。
    返回: cast_on, row_count, 横向密度, 纵向密度
    """
    sts_per_cm = sts_per_10cm / 10.0
    rows_per_cm = rows_per_10cm / 10.0
    cast_on = round(sts_per_cm * target_width_cm)
    row_count = round(rows_per_cm * target_height_cm)
    return {
        "cast_on": cast_on,
        "row_count": row_count,
        "sts_per_cm": sts_per_cm,
        "rows_per_cm": rows_per_cm,
    }


def _format_chart_md(chart: List[List[str]]) -> str:
    lines = []
    for r in chart:
        lines.append(" ".join(f"{c:>6}" for c in r))
    return "\n".join(lines)


@mcp.tool()
def export_markdown(chart_result: ChartResult, title: str = "Knitting Pattern") -> str:
    """将生成的图表导出为 Markdown 文本（含图例）。"""
    chart = chart_result["chart"]
    legend = chart_result["legend"]
    pattern = chart_result["pattern"]
    width = chart_result["width"]
    height = chart_result["height"]
    md = [
        f"# {title}",
        "",
        f"- 图案: `{pattern}`",
        f"- 尺寸: `{width} x {height}`",
        "",
        "## 图例",
    ]
    for k, v in legend.items():
        md.append(f"- `{k}`: {v}")
    md += ["", "## 图表（自下而上显示行）", "```", _format_chart_md(chart[::-1]), "```"]  # type: ignore
    return "\n".join(md)

@mcp.tool("basic-knowledge")
def basic_knowledge_resource() -> str:
    """内置示例资源：返回 knitting 基础知识的 Markdown 文本。"""
    return """# Knitting Basic Knowledge
| 符号     | 英文全称及含义                                         |
| ------ | ----------------------------------------------- |
| alt    | alternate，每隔一段                                  |
| beg    | begin，开始                                        |
| BO     | bind off，收针                                     |
| CC     | contrasting color，对比色                           |
| CO     | cast on，起针                                      |
| cont   | continue，继续                                     |
| dec    | decrease，减针                                     |
| inc    | increase，加针                                     |
| K      | knit，下针                                         |
| k1-b   | knit one stitch in back loop，扭下针                |
| k1f\&b | knit 1 front and back，在同一针织下针与扭针（一种加针方式）        |
| k2tog  | knit two stitches together，左下二并针                |
| M1     | make 1 stitch，加一针（从下方挑针的方式，可分从右侧或左侧）            |
| MC     | main color，主色                                   |
| p      | purl，上针                                         |
| patt   | pattern，花样                                      |
| p2sso  | pass 2 slipped stitches over together，将两滑针套过左侧针 |
| p2tog  | purl two stitches together，左上二并针                |
| p3tog  | purl three stitches together，左上三并针              |
| pm     | place marker，放记号圈                               |
| psso   | pass slipped stitch over，将滑针套过左侧针               |
| pu     | pick up and knit，挑针继续织                          |
| rep    | repeat，重复                                       |
| RS     | right side，正面                                   |
| s2kp   | sl 2-k1-p2sso，先滑2针，再织1针，最后将滑过去的2针一起套过           |
| SSK    | Slip,Slip,Purl，滑滑并减针                            |
| SKP    | Slip1,knit1,pass slipped stitch over，右上2针并1针    |
| SSP    | Slip,Slip,Purl，上针的右上2针并1针                       |
"""


@mcp.resource("pattern://{name}")
def pattern_resource(name: str) -> str:
    """内置示例资源：返回一个示例图案的 Markdown 文本。"""
    if name == "scarf_seed":
        chart = generate_chart("seed", 30, 20)
        return export_markdown(chart, title="Seed Stitch Scarf Pattern")
    elif name == "mesh_sw":
        chart = generate_chart("lace_mesh", 24, 16)
        return export_markdown(chart, title="Simple Mesh Swatch")
    else:
        chart = generate_chart("garter", 20, 20)
        return export_markdown(chart, title=f"Garter Sample: {name}")


if __name__ == "__main__":
    # 通过 stdio 运行，便于 MCP Inspector 或客户端调试
    mcp.run(transport="stdio")