import streamlit as st
from file_agent_using_framework import Agent, generate_response, Goal, Environment
from core.agent_framework import (
    AgentFunctionCallingActionLanguage,
    Action,
    ActionRegistry,
    Agent,
    Goal,
    generate_response, AgentLanguage, Environment, register_tool,PythonActionRegistry
)
# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
    st.session_state.task_count = 0  # track number of tasks

    # Initial greeting from agent
    greeting = "Hi there! I'm here to help you understand and document the Python files in this project. What would you like to explore first?"
    st.session_state.history.append(('assistant', greeting))

# Display conversation history
for role, message in st.session_state.history:
    st.chat_message(role).write(message)

# User input for new task
if st.session_state.task_count == 0:
    placeholder_text = "Describe your first task..."
else:
    placeholder_text = "Enter the next task..."
user_input = st.chat_input(placeholder_text)
if user_input:
    # Append user input to history
    st.session_state.history.append(('user', user_input))

    # Define agent's goals
    goals = [
        Goal(priority=1, name="Gather Information", description="Read each file in the project to build a deep understanding."),
        Goal(priority=1, name="Terminate", description="Call terminate when done and provide a complete README for the asked project in the message parameter.")
    ]

    # Create agent instance
    agent = Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        # The ActionRegistry now automatically loads tools with these tags
        action_registry=PythonActionRegistry(tags=["file_operations", "system"]),
        generate_response=generate_response,
        environment=Environment()
    )

    # Run the agent with user input
    final_memory, result = agent.run(user_input)

    # Append agent's response to history
    
    if isinstance(result, dict):
        res_txt = result.get("result", result)
    else:
        res_txt = result

    st.session_state.history.append(('assistant', res_txt))
    
    st.session_state.task_count += 1

    # Refresh the page to display the new conversation
    st.rerun()
