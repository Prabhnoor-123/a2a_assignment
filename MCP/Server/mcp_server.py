from fastmcp import FastMCP
# from models.config import settings
import httpx
import os
from dotenv import load_dotenv
load_dotenv()

mcp = FastMCP("Tavily_MCP")
TAVILY_API_KEY= os.getenv("TAVILY_API_KEY")

@mcp.resource("resource://tavily/search/{query}")
def search_tavily(query: str) -> dict:
    """Fetch search results from Tavily for a given query."""
    if not TAVILY_API_KEY:
        return {"error": "Tavily API key not set."}

    url = "https://api.tavily.com/search"
    payload = {
        "api_key": TAVILY_API_KEY,
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