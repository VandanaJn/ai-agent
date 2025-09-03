"""
chat_agent.py

This module defines a simple conversational agent using the LiteLLM library to interact with OpenAI's GPT models.
It supports message history, user input, and assistant responses.

Classes:
    ChatSession:
        Encapsulates a chat session with a system prompt and message history.

        Attributes:
            messages (List[Dict]): Stores the conversation history.

        Methods:
            __init__(system_prompt: str): Initializes the session with a system message.
            user_message(content: str): Adds a user message to the history.
            get_response() -> str: Sends the message history to the model and appends the assistant's reply.
            show_history(): Prints the full conversation history.

Environment:
    Loads the OpenAI API key from `.env` using `dotenv` and sets it for LiteLLM usage.

Example:
    chat = ChatSession("You are a helpful assistant...")
    chat.user_message("What is a lambda function?")
    print(chat.get_response())
"""

from litellm import completion
from typing import List, Dict

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = api_key

class ChatSession:
    def __init__(self, system_prompt: str):
        self.messages: List[Dict] = [{"role": "system", "content": system_prompt}]

    def user_message(self, content: str):
        self.messages.append({"role": "user", "content": content})

    def get_response(self) -> str:
        response = completion(
            model="openai/gpt-3.5-turbo",
            messages=self.messages,
            max_tokens=500
        )
        assistant_reply = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_reply})
        return assistant_reply

    def show_history(self):
        for msg in self.messages:
            print(f"{msg['role'].upper()}: {msg['content']}\n")

chat = ChatSession("You are a helpful assistant who explains things clearly and write clean code don't describe too much.")

chat.user_message("What is a lambda function in Python?")
print(chat.get_response())

chat.user_message("Can you give me an example?")
print(chat.get_response())

import json

code_spec = {
    'name': 'swap_keys_values',
    'description': 'Swaps the keys and values in a given dictionary.',
    'params': {
        'd': 'A dictionary with unique values.'
    },
}
chat.user_message(f"Please implement: {json.dumps(code_spec)}")
print(chat.get_response())
# chat.show_history()  # Optional: see the full conversation
