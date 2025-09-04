'''This code generates python code and unit test based on description and 
borrowed and improved based on a course by Vanderbilt University in Coursera
'''
from litellm import completion
from typing import List, Dict

from dotenv import load_dotenv
import os
import sys
import re

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"]=api_key



def generate_response(messages: List[Dict]) -> str:
   """Call LLM to get response"""
   response = completion(
      model="openai/gpt-3.5-turbo",
      messages=messages,
      max_tokens=1024
   )
   return response.choices[0].message.content

def extract_code_block(response: str) -> str:
    """Extract the first Python code block from a Markdown-formatted string."""
    match = re.search(r"```(?:python)?\n(.*?)```", response, re.DOTALL)
    return match.group(1).strip() if match else response.strip()


def extract_code_block2(response: str) -> str:
   """Extract code block from response"""

   if not '```' in response:
      return response

   code_block = response.split('```')[1].strip()
   # Check for "python" at the start and remove

   if code_block.startswith("python"):
      code_block = code_block[6:]

   return code_block

def develop_custom_function():
   # Get user input for function description
   print("\nWhat kind of function would you like to create?")
   print("Example: 'A function that calculates the factorial of a number'")
   print("Your description: ", end='')
   function_description = input().strip()

   # Initialize conversation with system prompt
   messages = [
      {"role": "system", "content": "You are a Python expert helping to develop a function."}
   ]

   # First prompt - Basic function
   messages.append({
      "role": "user",
      "content": f"Write a Python function that {function_description}. Output the function in a ```python code block```."
   })
   initial_function = generate_response(messages)

   # Parse the response to get the function code
   initial_function = extract_code_block(initial_function)

   print("\n=== Initial Function ===")
   print(initial_function)

   # Add assistant's response to conversation
   # Notice that I am purposely causing it to forget its commentary and just see the code so that
   # it appears that is always outputting just code.
   messages.append({"role": "assistant", "content": "\`\`\`python\n\n"+initial_function+"\n\n\`\`\`"})

   # Second prompt - Add documentation
   messages.append({
      "role": "user",
      "content": "Add comprehensive documentation to this function, including description, parameters, "
                 "return value, examples, and edge cases. Output the function in a ```python code block```."
   })
   documented_function = generate_response(messages)
   documented_function = extract_code_block(documented_function)
   print("\n=== Documented Function ===")
   print(documented_function)

   # Add documentation response to conversation
   messages.append({"role": "assistant", "content": "\`\`\`python\n\n"+documented_function+"\n\n\`\`\`"})

   # Third prompt - Add test cases
   messages.append({
      "role": "user",
      "content": "Add unittest test cases for this function, including tests for basic functionality, "
                 "edge cases, error cases, and various input scenarios. Output the code in a \`\`\`python code block\`\`\`."
   })
   test_cases = generate_response(messages)
   # We will likely run into random problems here depending on if it outputs JUST the test cases or the
   # test cases AND the code. This is the type of issue we will learn to work through with agents in the course.
   test_cases = extract_code_block(test_cases)
   print("\n=== Test Cases ===")
   print(test_cases)

   # Generate filename from function description
   filename = function_description.lower()
   filename = ''.join(c for c in filename if c.isalnum() or c.isspace())
   filename = filename.replace(' ', '_')[:30] + '.py'

   # Save final version
   with open(filename, 'w') as f:
      f.write(documented_function + '\n\n' + test_cases)

   return documented_function, test_cases, filename

if __name__ == "__main__":


   function_code, tests, filename = develop_custom_function()
   print(f"\nFinal code has been saved to {filename}")

