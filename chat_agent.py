from litellm import completion
from typing import List, Dict

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"]=api_key

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