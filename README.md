# 🤖 AI Agent Project

Welcome to the **AI Agent** repository — a sandbox for exploring how to build intelligent agents using Python and AI models. This project demonstrates various approaches to creating agents that can chat, handle files, and even generate code.

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/VandanaaJn/AI_agent.git
cd ai-agent
```

### 2. Set Up the Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variable

Create a `.env` file and add your API key:

```env
OPENAI_API_KEY=your_openai_key_here
```

### 4. Run an Agent

```bash
python file_agent_with_fn_calling_v2.py
```

## 🖼️ Screenshot

![sample Screenshot](https://github.com/VandanaJn/repo-common/blob/main/file_agent_output.png)

## 🛠️ Scripts Explained

| Script                             | Description                                               |
|-----------------------------------|-----------------------------------------------------------|
| `chat_agent.py`                   | A basic conversational agent using AI                     |
| `simple_file_agent.py`            | Handles file input/output without function calling        |
| `file_agent_with_fn_calling.py`   | Adds function calling to enhance file handling            |
| `file_agent_with_fn_calling_v2.py`| Improved version with more robust function calling        |
| `generate_python_code.py`         | Generates Python code from natural language prompts       |

## 📄 License

This project is licensed under the [MIT License](LICENSE).