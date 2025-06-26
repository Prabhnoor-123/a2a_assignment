from fastmcp import FastMCP
from config import settings
import httpx

mcp = FastMCP("Tavily_MCP")


@mcp.resource("resource://tavily/search/{query}")
def search_tavily(query: str) -> dict:
    """Fetch search results from Tavily for a given query."""
    if not settings.TAVILY_API_KEY:
        return {"error": "Tavily API key not set."}

    url = "https://api.tavily.com/search"
    payload = {
        "api_key": settings.TAVILY_API_KEY,
        "query": query,
        "include_answers": True,
        "include_sources": True,
    }

    try:
        response = httpx.post(url, json=payload)
        response.raise_for_status()
        return response.json()  # This will be auto-serialized by FastMCP
    except httpx.HTTPError as e:
        return {"error": str(e)}
    

if __name__ == "__main__":
    mcp.run(transport="streamable-http",port=8001)    