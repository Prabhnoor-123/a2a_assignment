import os
import logging
import httpx
from config import settings
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message

logger = logging.getLogger(__name__)

class ResearchAgent:
    """Agent that uses Tavily API to perform research."""

    async def invoke(self, query: str) -> str:
        api_key = settings.TAVILY_API_KEY
        if not api_key:
            logger.error("TAVILY_API_KEY is not set.")
            return "Error: Tavily API key not configured."

        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {
            "query": query,
            "include_answer": True,
            "include_sources": True,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post("https://api.tavily.com/search", json=payload, headers=headers)
            if response.status_code != 200:
                logger.error(f"Tavily request failed: {response.text}")
                return "Error: Tavily request failed."

            result = response.json()
            print("result:",result)

        summary = result.get("answer", "No answer found.")
        sources = result.get("sources", [])
        source_text = "\n".join(f"- {s['url']}" for s in sources) if sources else "No sources found."

        return f"🔍 **Summary:**\n{summary}\n\n📚 **Sources:**\n{source_text}"


class ResearchAgentExecutor(AgentExecutor):
    """A2A AgentExecutor that performs web research using Tavily."""

    def __init__(self):
        self.agent = ResearchAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        
        query = context.get_user_input()
        print(query)
        logger.info(f"Received query: {query}")

        result = await self.agent.invoke(query)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise Exception('Cancel not supported.')
