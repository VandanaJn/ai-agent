from litellm import completion
from typing import List, Dict

from dotenv import load_dotenv
import os
import re
import json

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"]=api_key
def list_files(folder:str='.'):
    return [f for f in os.listdir(folder) if os.path.isfile(f)]

def read_file(file_name:str):
    with open(file_name, 'r') as file:
        return file.read()

def exists(file_name:str):
    return os.path.exists(file_name)

def parse_action(response: str):
    match = re.search(r"```action\s*({.*?})\s*```", response, re.DOTALL)
    if match:
        action_json = match.group(1)
        return json.loads(action_json)
    else:
        raise ValueError("No valid action block found in response.")


# agent_rules = [{
#     "role": "system",
#     "content": """
# You are an AI agent that can perform tasks by using available tools.

# Available tools:
# - list_files(folder:str='.') -> List[str]: List all files in the current or given directory.
# - read_file(file_name: str) -> str: Read the content of a file.
# - terminate(message: str): End the agent loop and print a summary to the user.

# ⚠️ MANDATORY FILE CHECK FLOW:
# If a user asks about a file:
# - First call list_files() to get all available files. do not call read_file if not needed.
# - Only then proceed to read_file() or terminate().
# - do not read_file if a user is asking to list only, or not interested in contents of a file, or just asking if a file exists
# - when terminating, give summary message

# ⚠️ TEST FILE RULES:
# - A test file must start with the prefix test (e.g., test_chat_agent.py)
# - Files that do not start with test are not test files
# - When checking for test files, list all files first, then filter by this rule
# - Do not read or process files that do not match this rule


# Every response MUST have an action in following format. 
# Do NOT omit the triple backticks and action. Do NOT change `action` to match the tool name. The parser depends on this exact label.
# The parser depends on this exact structure.
# Respond in this format:

# ```action
# {
#     "tool_name": "insert tool_name",
#     "args": {...fill in any required arguments here...}
# }
# """}]

agent_rules = [{
    "role": "system",
    "content": """
You are an AI agent that performs tasks using the following tools:

Available tools:
- list_files(folder: str = '.') -> List[str]: List all files in the current or given directory.
- read_file(file_name: str) -> str: Read the content of a file.
- terminate(message: str): End the agent loop and print a summary to the user.

🔒 MANDATORY FILE CHECK FLOW:
If a user asks about a file:
- Always call list_files() first to get all available files.
- Do NOT call read_file() unless the user explicitly asks for file contents or analysis.
- If the user is asking whether a file exists, or requesting a list of files, do NOT read the file.
- When terminating, summarize clearly whether the file exists or not.

✅ Examples:
User: "Do I have a .gitignore?"
→ Call list_files()
→ If '.gitignore' is found, call terminate with message: "Yes, .gitignore exists in the folder."

User: "Show me what's inside .gitignore"
→ Call list_files()
→ If '.gitignore' is found, call read_file() on it

🚫 Incorrect behavior:
Calling read_file() on '.gitignore' when the user only asked if it exists

🧪 TEST FILE RULES:
- A test file must start with the prefix `test` (e.g., test_chat_agent.py)
- Files that do NOT start with `test` are NOT test files
- When checking for test files:
  - First call list_files()
  - Then filter for files that start with `test` and end with `.py`
  - Do NOT read or process files that do not match this rule

✅ Example:
User: "Do I have any Python test files?"
→ Call list_files()
→ Filter for files like 'test_*.py'
→ If none found, call terminate("No Python test files found.")
→ If found, optionally read them if user requests content

🚫 Incorrect behavior:
Reading 'chat_agent.py' or any file not starting with 'test'

📦 RESPONSE FORMAT:
Every response MUST include an action in the following format.
Do NOT omit the triple backticks or the word `action`. Do NOT change `action` to match the tool name.

Respond in this exact structure:

```action
{
    "tool_name": "insert tool_name",
    "args": { ...fill in required arguments... }
}
"""}]

max_iterations=4
memory = [
    # {"role": "user", "content": "do i have a python test files in C:\learning\\ai-agent"}
    # {"role": "user", "content": "List .py files in C:\learning\\ai-agent"}
    # {"role": "user", "content": "do i have a license"}
    # {"role": "user", "content": "do i have a gitignore"}
    {"role": "user", "content": "read license"}
]

def generate_response(messages: List[Dict]) -> str:
   """Call LLM to get response"""
   response = completion(
      model="openai/gpt-3.5-turbo",
      messages=messages,
      max_tokens=1024
   )
   return response.choices[0].message.content

max_iterations=5
iterations=0
# The Agent Loop
while iterations < max_iterations:

    # 1. Construct prompt: Combine agent rules with memory
    prompt = agent_rules + memory

    # 2. Generate response from LLM
    print("Agent thinking...")
    response = generate_response(prompt)
    print(f"Agent response: {response}")

    # 3. Parse response to determine action
    action = parse_action(response)

    # result = "Action executed"

    if action["tool_name"] == "list_files":
        if "args" in action:
            result = {"result":list_files(action["args"]["folder"])}
        else:
            result = {"result":list_files()}
    elif action["tool_name"] == "read_file":
        result = {"result":read_file(action["args"]["file_name"])}
    elif action["tool_name"] == "error":
        result = {"error":action["args"]["message"]}
    elif action["tool_name"] == "terminate":
        print(action["args"]["message"])
        break
    else:
        result = {"error":"Unknown action: "+action["tool_name"]}

    print(f"Action result: {result}")

    # # 5. Update memory with response and results
    memory.extend([
        {"role": "assistant", "content": response},
        {"role": "user", "content": json.dumps(result)}
    ])

    # 6. Check termination condition
    if action["tool_name"] == "terminate":
        break

    iterations += 1


