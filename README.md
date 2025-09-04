# 🤖 AI Agent Project

A modular framework for building intelligent agents using Python, natural language processing, and tool orchestration. Supports both CLI and Streamlit interfaces for interacting with agents that perform file operations, generate code, and summarize tasks.

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/VandanaJn/ai-agent.git
   cd ai-agent
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install the package and dependencies**
   ```bash
   pip install -e .
   pip install -r requirements.txt
   ```

4. **Configure your OpenAI API key**
   Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_openai_key_here
   ```

---

## 🗂️ Folder Structure

- `cli_agents/` — CLI-based agents for chat, file operations, code generation, and task summaries  
- `core/` — Agent framework: base classes, tool registration, and orchestration  
- `streamlit_apps/` — Web apps for interacting with agents via Streamlit

---

## 🧠 Key Scripts

- `chat_agent.py` — Conversational agent using LiteLLM  
- `file_agent_with_fn_calling_v2.py` — Enhanced file agent with robust function calling  
- `file_agent_using_framework.py` — Agent built on a reusable framework  
- `generate_python_code.py` — Generates Python code from natural language prompts  
- `task_summarizer_agent.py` — Summarizes tasks and content from files  
- `chat_app.py` — Streamlit web app for chatting with the AI assistant  
- `file_agent_app.py` — Streamlit web app for file-based agent interactions, it can generate readme and describe python files
- `agent_framework.py` — Implements an agent framework providing the base classes for actions, tools registration, and agent functionality.

---

## 🚀 Usage

### 🖥️ Run CLI agents
```bash
python cli_agents/file_agent_with_fn_calling_v2.py
```
## 🖼️ Screenshot

![sample Screenshot](https://github.com/VandanaJn/repo-common/blob/main/file_agent_output.png)

### 🌐 Launch Streamlit apps
```bash
streamlit run streamlit_apps/file_agent_app.py
```

## 🖼️ Screenshot

![sample Screenshot](https://github.com/VandanaJn/repo-common/blob/main/file_readme_agent_screenshot.png)



---

## 📋 Requirements

- Python 3.8+
- Streamlit
- LiteLLM
- python-dotenv

---

## 🧩 Extensibility

This framework is modular and extensible. You can:
- Add new tools and agents by subclassing the base framework
- Integrate additional APIs or models
- Deploy agents via CLI, Streamlit, or other interfaces

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).