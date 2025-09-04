"""
AI agent using LiteLLM with function calling support.  
Sends tool_calls explicitly in assistant messages based on the previous response.  
Supports list_files, read_file, and terminate while preserving conversation history.
"""
import json
import os
from typing import List
from dotenv import load_dotenv
from litellm import completion

# --- Setup ---
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = api_key


# --- Tool functions ---
def terminate(message: str) -> None:
    """Terminate the agent loop and provide a summary message."""
    print(f"Termination message: {message}")


def list_files() -> List[str]:
    """List files in the current directory."""
    return os.listdir(".")


def read_file(file_name: str) -> str:
    """Read a file's contents."""
    try:
        with open(file_name, "r") as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: {file_name} not found."
    except Exception as e:
        return f"Error: {str(e)}"


tool_functions = {
    "list_files": list_files,
    "read_file": read_file,
    "terminate": terminate,
}

# --- Tools schema (for the model) ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Returns a list of files in the directory.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of a specified file in the directory.",
            "parameters": {
                "type": "object",
                "properties": {"file_name": {"type": "string"}},
                "required": ["file_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "terminate",
            "description": "Terminates the conversation. No further actions or interactions are possible after this. Prints the provided message for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                },
                "required": ["message"]
            }
        }
    }
]

# --- Rules for the agent ---
agent_rules = [
    {
        "role": "system",
        "content": """
You are an AI agent that can perform tasks by using available tools.

If a user asks about files, documents, or content, first list the files before reading them.
If there is nothing to do, call terminate.
"""
    }
]

# --- Get user request ---
user_task = input("What would you like me to do? ")

memory = [{"role": "user", "content": user_task}]

# --- Agent loop ---
max_iterations = 5
iterations = 0

while iterations < max_iterations:
    messages = agent_rules + memory

    response = completion(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=tools,
        max_tokens=512,
    )

    assistant_message = response.choices[0].message

    if assistant_message.tool_calls:
        tool = assistant_message.tool_calls[0]
        tool_name = tool.function.name
        tool_args = json.loads(tool.function.arguments) if tool.function.arguments else {}

        result = tool_functions[tool_name](**tool_args)

        print(f"\n🔧 Tool Name: {tool_name}")
        print(f"📥 Tool Arguments: {tool_args}")
        print(f"📤 Result: {result}")

        # Store assistant’s tool call
        memory.append({
            "role": "assistant",
            "tool_calls": assistant_message.tool_calls,
            "content": None,
        })

        # Store tool result with proper tool role
        memory.append({
            "role": "tool",
            "tool_call_id": tool.id,   # ✅ this links result to the tool call
            "content": str(result),
        })

        if tool_name == "terminate":
            print("\n✅ Agent terminated.")
            break

    else:
        print("\n💬 Assistant:", assistant_message.content)
        memory.append({"role": "assistant", "content": assistant_message.content or ""})


    iterations += 1
