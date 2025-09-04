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


def extract_markdown_block_old(text: str, block_type: str) -> str:
    """
    Extracts a fenced markdown code block of the given type from the text.
    For example, if block_type is "action", it looks for ```action ... ``` blocks.
    """
    pattern = rf"```{block_type}\n(.*?)\n```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        raise ValueError(f"No markdown block of type '{block_type}' found.")
    
def extract_markdown_block(response: str, block_type: str = "action") -> str:
    """Extract code block from response"""

    if not '```' in response:
        return response

    code_block = response.split('```')[1].strip()

    if code_block.startswith(block_type):
        code_block = code_block[len(block_type):].strip()

    return code_block

def parse_action(response: str) -> Dict:
    """Parse the LLM response into a structured action dictionary."""
    try:
        response = extract_markdown_block(response, "action")
        response_json = json.loads(response)
        if "tool_name" in response_json and "args" in response_json:
            return response_json
        else:
            return {"tool_name": "error", "args": {"message": "You must respond with a JSON tool invocation."}}
    except json.JSONDecodeError:
        return {"tool_name": "error", "args": {"message": "Invalid JSON response. You must respond with a JSON tool invocation."}}
    except ValueError:
        return {"tool_name": "error", "args": {"message": "Invalid response. You must respond with action and a JSON tool invocation."}}


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
    {"role": "user", "content": "do i have a license"}
    # {"role": "user", "content": "do i have a gitignore"}
    # {"role": "user", "content": "read license"}
    # {"role": "user", "content": "how is the weather"}
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


