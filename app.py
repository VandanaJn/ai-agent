import streamlit as st
from file_agent_using_framework import agent  # your existing agent

# Streamlit page configuration
st.set_page_config(page_title="AI Agent Web App", page_icon="🤖")
st.title("AI Agent Web Interface")
st.write("Interact with your Python AI agent in the browser!")

# Initialize session state for conversation history
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("Ask your agent:")

if user_input:
    try:
        # Run the agent
        final_memory, result = agent.run(user_input)

        # Extract the latest text from memory
    #     result_str = ""
    #     if hasattr(final_memory, "get_memories"):
    #         memories = final_memory.get_memories()
    #         if memories:
    #             last_content = memories[-1].get("content", [])
    #             if isinstance(last_content, list) and len(last_content) > 0:
    #                 # Extract the text string safely
    #                 text_obj = last_content[0]
    #                 if isinstance(text_obj, dict) and "text" in text_obj:
    #                     result_str = text_obj["text"]
    #     elif isinstance(final_memory, dict) and "result" in final_memory:
    #         result_str = final_memory["result"]
    #     else:
    #         result_str = str(final_memory)

    #     # Clean up redundant 'Terminating...' if present
    #     result_str = result_str.replace("Terminating...", "").strip()

    except Exception as e:
        result_str = f"Error: {e}"

    # Append user input and agent response
    st.session_state.history.append(("User", str(user_input)))
    
    st.session_state.history.append(("Agent", str(result["result"])))

# Display chat history
for sender, message in st.session_state.history:
    if sender == "User":
        st.markdown(f"**You:** {message}")
    else:
        # Render multi-line Markdown in an expander
        with st.expander("Agent response", expanded=True):
            st.markdown(message)
