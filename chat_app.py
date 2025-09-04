import streamlit as st
from chat_agent import ChatSession

def main():
    st.title("Chat Agent with LiteLLM")

    # 1️⃣ Initialize session state
    if 'chat' not in st.session_state:
        # Create ChatSession with system prompt
        st.session_state.chat = ChatSession(
            "You are a helpful assistant who explains things clearly and writes clean code succinctly."
        )

        # Add initial greeting message
        greeting = "Hello! How can I help you today?"
        st.session_state.history = [('assistant', greeting)]

    # 2️⃣ Display chat history
    for role, msg in st.session_state.history:
        if role == 'user':
            st.chat_message("user").write(msg)
        else:
            st.chat_message("assistant").write(msg)

    # 3️⃣ Input box for user messages
    user_input = st.chat_input("Your message:")

    # 4️⃣ Handle new user input
    if user_input:
        # Save user message
        st.session_state.history.append(('user', user_input))

        # Get agent’s reply
        with st.spinner("Thinking..."):
            st.session_state.chat.user_message(user_input)
            reply = st.session_state.chat.get_response()
            st.session_state.history.append(('assistant', reply))

        # Refresh UI to show new messages
        st.rerun()

if __name__ == "__main__":
    main()
