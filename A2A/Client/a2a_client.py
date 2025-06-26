import streamlit as st
import httpx
import asyncio
from uuid import uuid4
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import SendMessageRequest, MessageSendParams

# --- Configuration ---
RESEARCH_AGENT_URL = "http://localhost:8000"
AGENT_CARD_PATH = "/.well-known/agent.json"  

# --- Streamlit App ---
st.set_page_config(page_title="AI Research Chatbot", layout="centered")
st.title("🧠 AI Research Chatbot")

# Store chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

# Input box for new message
if prompt := st.chat_input("Ask your research question..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "text": prompt})

    async def ask_research_agent(query: str) -> str:
        async with httpx.AsyncClient(timeout=30.0) as httpx_client:
            # Discover agent card
            resolver = A2ACardResolver(httpx_client=httpx_client, base_url=RESEARCH_AGENT_URL)
            agent_card = await resolver.get_agent_card(relative_card_path=AGENT_CARD_PATH)

            # Init client
            client = A2AClient(httpx_client=httpx_client, agent_card=agent_card)

            # Create request
            message_id = uuid4().hex
            request = SendMessageRequest(
                id=str(uuid4()),
                params=MessageSendParams(
                    message={
                        "role": "user",
                        "messageId": message_id,
                        "parts": [{"kind": "text", "text": query}],
                    }
                )
            )

            # Send and receive
            response = await client.send_message(request)
            print(response)
            parts = response.root.result.parts  
            return "\n".join([p.root.text for p in parts if p.root.kind == "text"])

    # Run async task and display response
    with st.chat_message("assistant"):
        response_text = asyncio.run(ask_research_agent(prompt))
        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "text": response_text})
