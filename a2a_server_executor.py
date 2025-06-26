import logging
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from mcp_client import get_summary_from_mcp  
from urllib.parse import quote_plus
from config import settings
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message

logger = logging.getLogger(__name__)

class ResearchAgent:
    def __init__(self):
        self.mcp_client = Client(StreamableHttpTransport(url="http://localhost:8000/mcp"))

    async def invoke(self, query: str) -> str:
        try:
            summary = await get_summary_from_mcp(query)
            return f"🔍 **Summary:**\n{summary}"
        except Exception as e:
            logger.exception("Failed to get data from MCP.")
            return f"❌ Error: {str(e)}"
        
class ResearchAgentExecutor(AgentExecutor):
    def __init__(self):
        self.agent = ResearchAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        query = context.get_user_input()
        logger.info(f"Received query: {query}")

        result = await self.agent.invoke(query)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception("Cancel not supported.")
