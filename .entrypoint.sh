#!/bin/bash

export PYTHONPATH=$(pwd)

uv run /home/prabhnoor/Desktop/A2A_Assignment/A2A/Server/a2a_server.py &
uv run /home/prabhnoor/Desktop/A2A_Assignment/MCP/Server/mcp_server.py &
streamlit run /home/prabhnoor/Desktop/A2A_Assignment/A2A/Client/a2a_client.py
wait