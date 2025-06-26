# main.py
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.types import AgentCard, AgentCapabilities, AgentSkill

agent_card = AgentCard(
    id="test_agent",
    name="Test Agent",
    description="A test A2A agent",
    url="http://localhost:8000/",
    version="1.0.0",
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    capabilities=AgentCapabilities(streaming=False),
    skills=[
        AgentSkill(
            id="test_skill",
            name="Skill",
            description="Does nothing",
            tags=["test"],
            examples=["test example"]
        )
    ]
)

app = A2AStarletteApplication(agent_card=agent_card)

if __name__ == "__main__":
    uvicorn.run(app.build(), host="0.0.0.0", port=8000)
