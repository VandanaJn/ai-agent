from core.agent_framework import (Agent, Goal, Environment, PythonActionRegistry, 
                                  AgentFunctionCallingActionLanguage, register_tool, generate_response)

# First, we'll define our tools using decorators
@register_tool(tags=["file_operations", "read"])
def read_project_file(name: str) -> str:
    """Reads and returns the content of a specified project file.

    Opens the file in read mode and returns its entire contents as a string.
    Raises FileNotFoundError if the file doesn't exist.

    Args:
        name: The name of the file to read

    Returns:
        The contents of the file as a string
    """
    with open(name, "r") as f:
        return f.read()
    
@register_tool(tags=["system"], terminal=True)
def terminate(message: str) -> str:
    """Terminates the agent's execution with a final message.

    Args:
        message: The final message to return before terminating

    Returns:
        The message with a termination note appended
    """
    return f"{message}\nTerminating..."

# Define goals
goals = [
    Goal(priority=1,
         name="Gather Information",
         description="Read tasks.txt to understand all the tasks listed."),
    Goal(priority=2,
         name="Summarize",
         description="Group tasks into categories (Work, Personal, Other)."),
    Goal(priority=3,
         name="Terminate",
         description="Call terminate when done and provide a categorized summary in the message parameter.")
]

# Create agent
agent = Agent(
    goals=goals,
    agent_language=AgentFunctionCallingActionLanguage(),
    action_registry=PythonActionRegistry(tags=["file_operations", "system"]),
    generate_response=generate_response, 
    environment=Environment()
)

# Run loop
user_input = "Summarize my tasks from tasks.txt into categories."
final_memory, result = agent.run(user_input)

# print("=== Final Agent Memory ===")
# print(final_memory.get_memories())