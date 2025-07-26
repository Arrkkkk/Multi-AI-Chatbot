# 🧠 Multi‑AI Chatbot  
### *Agentic Chatbot with LangGraph, FastAPI & Streamlit*

![Build](https://img.shields.io/badge/build-passing-brightgreen)  
![License](https://img.shields.io/badge/license-MIT-blue)  
![Python](https://img.shields.io/badge/python-3.10%2B-yellow)  
![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-orange)

A modern, intelligent chatbot platform that supports **multi-agent conversations** using **LangGraph**, integrates **FastAPI** for backend communication, and delivers an interactive **Streamlit** frontend. Choose from multiple LLMs (Groq/OpenAI), define agent personas, and even enable real-time **web search** with Tavily!

---

## 🔥 Features

- 🧑‍🎓 **Custom AI Agents** — Create and select agents with task-specific instructions  
- 🤖 **Model Flexibility** — Choose between:
  - `gpt-4o-mini`
  - `llama-3-70b`
  - `mixtral-8x7b`
- 🔌 **Model Provider Support** — Works with both **Groq** and **OpenAI** APIs  
- 🌐 **Optional Web Search** — Integrate **Tavily** for real-time enhanced responses  
- 🎨 **Streamlit UI** — Clean, modern frontend powered by Streamlit  
- ⚙️ **FastAPI Backend** — Robust backend API for processing requests  

---

## 📸 Demo Screenshot

> *(Add a screenshot image at `assets/demo-ui.jpg`)*  
![Chatbot UI](assets/demo-ui.jpg)

---

## 📁 Project Structure

```
multi-ai-chatbot/
├── ai_agent.py        # LangGraph agent logic
├── backend.py         # FastAPI backend API
├── frontend.py        # Streamlit app
├── assets/            # Static assets (e.g., screenshots)
│   └── demo-ui.jpg
├── .env               # Secret API keys (excluded from version control)
├── requirements.txt   # Python dependencies
├── Dockerfile         # Optional Docker support
└── README.md          # You’re reading it!
```

---

## ⚙️ Environment Variables

Create a `.env` file at the root and fill in your credentials:

```
OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key  # Optional
```

✅ Be sure to add `.env` to your `.gitignore` file!

---

## 🛠️ Installation

### 1. Clone the Repository

```
git clone https://github.com/Arrkkkk/multi-ai-chatbot.git
cd multi-ai-chatbot
```

### 2. Create a Virtual Environment

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

## 🚀 Running the App Locally

### Start the FastAPI Backend

```
uvicorn backend:app --reload
```

### Launch the Streamlit Frontend

```
streamlit run frontend.py
```

Open `http://localhost:8501` in your browser to chat with the agents.

---

## 🌐 Deploying to Streamlit Cloud

1. Push the project to a public GitHub repo  
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) → New App  
3. Set **main file** to `chatbot_app.py`  
4. Add **secrets** for your `.env` values in Streamlit’s dashboard  

---

## 🐳 Docker Deployment (Optional)

### Build Docker Image

```
docker build -t multi-ai-chatbot .
```

### Run Docker Container

```
docker run -p 8501:8501 multi-ai-chatbot
```

---

## 🧠 How It Works

1. **Select Agent** — Each with a unique system prompt  
2. **Choose Model** — Switch between LLM providers  
3. **Enable Search** — Optional web-based retrieval with Tavily  
4. **Chat** — Multi-agent, real-time interactions

---

## ✨ Customization Tips

- Add new agent logic inside `chatbot_app.py`  
- Improve the frontend layout in `chatbot_app.py`  
- Swap models or APIs via `.env` and config logic

---

## 📦 Requirements

```
streamlit
fastapi
openai
groq
langgraph
tavily
uvicorn
python-dotenv
```

Install using:

```
pip install -r requirements.txt
```

---

## 📚 Acknowledgments

- [LangGraph](https://www.langgraph.dev/)  
- [Streamlit](https://streamlit.io/)  
- [FastAPI](https://fastapi.tiangolo.com/)  
- [Groq](https://groq.com/)  
- [OpenAI](https://openai.com/)  
- [Tavily](https://www.tavily.com/)
- [Gemini](https://gemini.google.com)

---

## 📄 License

Licensed under the **MIT License** — free to use and modify with attribution.
