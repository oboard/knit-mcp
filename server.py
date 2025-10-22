from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Knit MCP Demo")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.tool()
def echo(message: str) -> str:
    """Echo a message back"""
    return message


@mcp.resource("greeting://{name}")
def greeting(name: str) -> str:
    """Return a greeting resource"""
    return f"Hello, {name}!"


if __name__ == "__main__":
    # 通过 stdio 运行，便于使用 MCP Inspector 或客户段调试
    mcp.run(transport="stdio")