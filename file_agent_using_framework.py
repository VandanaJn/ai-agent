from core.agent_framework import (
    AgentFunctionCallingActionLanguage,
    Action,
    ActionRegistry,
    Agent,
    Goal,
    generate_response, AgentLanguage, Environment
)
from typing import List
import os

# Define the agent's goals
goals = [
    Goal(priority=1, name="Gather Information", description="Read each python file in the project"),
    Goal(priority=1, name="Terminate", description="Call the terminate call only when you have read all the python files "
                                                    "and generate the content of the README in the terminate message")
]

# Define the agent's language
agent_language = AgentFunctionCallingActionLanguage()

def read_project_file(name: str) -> str:
    with open(name, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

def list_project_files() -> List[str]:
    return sorted([file for file in os.listdir(".") if file.endswith("file_agent_using_framework.py") or file.endswith("chat_agent.py")])


# Define the action registry and register some actions
action_registry = ActionRegistry()
action_registry.register(Action(
    name="list_project_files",
    function=list_project_files,
    description="Lists all files in the project.",
    parameters={},
    terminal=False
))
action_registry.register(Action(
    name="read_project_file",
    function=read_project_file,
    description="Reads a file from the project.",
    parameters={
        "type": "object",
        "properties": {
            "name": {"type": "string"}
        },
        "required": ["name"]
    },
    terminal=False
))
action_registry.register(Action(
    name="terminate",
    function=lambda message: f"{message}\nTerminating...",
    description="Terminates the session and prints the message to the user.",
    parameters={
        "type": "object",
        "properties": {
            "message": {"type": "string"}
        },
        "required": []
    },
    terminal=True
))

# Define the environment
environment = Environment()

# Create an agent instance
agent = Agent(goals, agent_language, action_registry, generate_response, environment)

# Run the agent with user input
user_input = "Write a README.md for this project."
final_memory = agent.run(user_input)

# Print the final memory
# print(final_memory.get_memories())