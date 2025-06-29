# mcp_client.py

import asyncio, os

from urllib.parse import quote_plus
from fastmcp import Client
from dotenv import load_dotenv
from fastmcp.client.transports import StreamableHttpTransport
import google.generativeai as genai

load_dotenv()
# Configure Gemini
genai.configure(api_key=os.getenv('gemini_api_key'))


model = genai.GenerativeModel("gemini-1.5-flash")

transport = StreamableHttpTransport(url="http://localhost:8001/mcp")
mcp_client = Client(transport)

async def get_summary_from_mcp(query: str) -> str:
    encoded_query = quote_plus(query)

    async with mcp_client:
        tavily_result = await mcp_client.read_resource(
            f"resource://tavily/search/{encoded_query}"
        )

        response = await model.generate_content_async(
            f"Summarize this research result:\n{tavily_result}",
            generation_config=genai.types.GenerationConfig(temperature=0.3)
        )

        return response.text
