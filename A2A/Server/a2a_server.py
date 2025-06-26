import uvicorn
import logging
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from A2A.Server.a2a_server_executor import ResearchAgentExecutor  

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    skill = AgentSkill(
        id='web_research',
        name='Research Query Resolver',
        description='Performs research on the web and returns summaries, references, and articles.',
        tags=['research', 'summary', 'references'],
        examples=['what is the latest in quantum computing?', 'AI safety research papers'],
    )

    public_agent_card = AgentCard(
        id='research_agent',
        name='Research AI Agent',
        description='Performs live research using Tavily and returns summarized data and references.',
        url='http://localhost:8000',
        version='1.0.0',
        defaultInputModes=['text'],
        defaultOutputModes=['text'],
        capabilities=AgentCapabilities(streaming=False),
        skills=[skill],
        supportsAuthenticatedExtendedCard=False,
    )

    request_handler = DefaultRequestHandler(
        agent_executor=ResearchAgentExecutor(),  # Uses Tavily under the hood
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=public_agent_card,
        http_handler=request_handler,
    )

    uvicorn.run(server.build(), host='0.0.0.0', port=8000)
