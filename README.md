# 🧠 AI Research Chatbot (A2A-Powered)

An intelligent research assistant that answers your questions by performing live web research using the [Tavily API](https://www.tavily.com/). It is built using the [A2A Protocol](https://github.com/a2a-protocol), and consists of:

- ✅ A frontend Streamlit chatbot UI
- ✅ A backend A2A-compatible Research Agent
- ✅ Integration with Tavily for real-time web summaries and citations

---

## 📦 Project Structure

```
ai-research-chatbot/
├── agent_executor.py          # Logic to call Tavily API
├── run_agent_server.py        # A2A Research Agent server
├── streamlit_chatbot.py       # Streamlit-based frontend chat
├── config.py                  # Stores API keys and settings
├── requirements.txt
└── README.md
```

---

## 🚀 Features

- 🔍 Real-time research using Tavily
- 💬 Conversational UI with memory (chat history)
- 🔗 Cites sources in response
- ⚡ Built using A2A protocol

---

## 🛠️ Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/your-username/ai-research-chatbot.git
cd ai-research-chatbot
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a file `config.py`:

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    TAVILY_API_KEY: str = "your_tavily_api_key"

settings = Settings()
```

> 🔑 Replace `"your_tavily_api_key"` with your actual [Tavily API key](https://app.tavily.com/).

---

## 🚦 How to Run

### ▶️ Start the Research Agent Server

```bash
python run_agent_server.py
```

Runs the agent at:  
```
http://localhost:8000
```

---

### 💬 Start the Streamlit Chatbot UI

```bash
streamlit run streamlit_chatbot.py
```

Opens in your browser at:  
```
http://localhost:8501
```

---

## 🧪 Example Questions to Try

- "What is the latest in quantum computing?"
- "Recent breakthroughs in AI safety?"
- "Top articles about climate change in 2024"

---

## 📖 A2A Agent Card

Accessible at:
```
http://localhost:8000/.well-known/agent.json
```

Used by the frontend to dynamically discover and interact with the agent.

---

## 🧰 Technologies Used

- [Streamlit](https://streamlit.io/) - frontend UI
- [httpx](https://www.python-httpx.org/) - async HTTP client
- [Tavily API](https://www.tavily.com/) - web search + summarization
- [A2A Protocol](https://github.com/a2a-protocol) - communication standard
