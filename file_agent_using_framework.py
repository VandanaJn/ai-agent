from core.agent_framework import (
    AgentFunctionCallingActionLanguage,
    Action,
    ActionRegistry,
    Agent,
    Goal,
    generate_response, AgentLanguage, Environment, register_tool,PythonActionRegistry
)
from typing import List
import os

# First, we'll define our tools using decorators
@register_tool(tags=["file_operations", "read"])
def read_project_file(path: str) -> str:
    """Reads and returns the content of a specified project file.

    Opens the file in read mode and returns its entire contents as a string.
    Raises FileNotFoundError if the file doesn't exist.

    Args:
        path: The name of the file with path to read

    Returns:
        The contents of the file as a string
    """
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

@register_tool(tags=["file_operations", "list"])
def list_project_files(path: str='.') -> List[str]:
    """Lists all Python files in the current project directory or given path.
    
    Args:
        path (str, optional): The folder to scan. Defaults to the current directory ('.').

    Scans the path and returns a sorted list of all files
    that end with '.py'.

    Returns:
        A sorted list of Python filenames
    """
    return sorted([file for file in os.listdir(path) if os.path.isfile(file) and not file.endswith(".md") and not file.endswith("LICENSE")
                    ])

@register_tool(tags=["system"], terminal=True)
def terminate(message: str) -> str:
    """Terminates the agent's execution with a final message.

    Args:
        message: The final message to return before terminating

    Returns:
        The message with a termination note appended
    """
    return f"{message}"




if __name__ == "__main__":
    # Define the agent's goals
    goals = [
        Goal(priority=1,
                name="Gather Information",
                description="Read each file in the project in order to build a deep understanding of the given project in order to write a README or description"),
        Goal(priority=1,
                name="Terminate",
                description="Call terminate when done and provide a complete README for the asked project in the message parameter")
    ]

    # Create an agent instance with tag-filtered actions
    agent = Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        # The ActionRegistry now automatically loads tools with these tags
        action_registry=PythonActionRegistry(tags=["file_operations", "system"]),
        generate_response=generate_response,
        environment=Environment()
    )
    # Run the agent with user input
    user_input = "Write a README for project C:\learning\hugging-face-app."
    final_memory, result = agent.run(user_input)
    # print(final_memory.get_memories())