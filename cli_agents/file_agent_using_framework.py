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

@register_tool(tags=["file_operations", "list_files"])
def list_project_files(path: str='.') -> List[str]:
    """Lists all Python files in the current project directory or given path.
    
    Args:
        path (str, optional): The folder to scan. Defaults to the current directory ('.').

    Scans the path and returns a sorted list of all files
    that end with '.py'.

    Returns:
        A sorted list of filenames
    """
    return sorted([
        file for file in os.listdir(path)
        if os.path.isfile(os.path.join(path, file))
        # and file.endswith(".py")  
        # and not file.endswith("_v2.py")  
        # and not file.endswith("simple_file_agent.py")  
        and not file.__eq__("__init__.py")  
    ])

    
@register_tool(tags=["file_operations", "list_dir"])
def list_project_folders(path: str='.') -> List[str]:
    """Lists all directories in the current project directory or given path.
    
    Args:
        path (str, optional): The folder to scan. Defaults to the current directory ('.').

    Scans the path and returns a sorted list of all dir
    that end with '.py'.

    Returns:
        A sorted list of directory names
    """
    return sorted([file for file in os.listdir(path) 
                   if os.path.isdir(os.path.join(path, file))
                   and not file.startswith(".") 
                #    and not file.startswith("core") 
                   and not file.__eq__("files") 
                   and not file.endswith("egg-info") 
                   and not file.endswith("__pycache__") 
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
    # print(list_project_files("c://learning//ai-agent//cli_agents"))
    # Define the agent's goals
    goals = [
        Goal(priority=1,
                name="Gather Information",
                description="List and read each file in the project in all the directories in order to build a deep understanding of the given project in order to write a README or description"),
        Goal(priority=1,
                name="Terminate",
                description="Call terminate after reading all needed files and provide a complete README for the asked project in the message parameter")
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
    user_input = "Write a README for c:\learning\ai-agent\cli_agents."
    # user_input = "Write a README for C:\learning\hugging-face-app."
    final_memory, result = agent.run(user_input)