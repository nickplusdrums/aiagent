import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import available_functions


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.user_prompt`
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents = messages,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt),
)
prompt_tc = response.usage_metadata.prompt_token_count
candidates_tc = response.usage_metadata.candidates_token_count
if response.function_calls == None:
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tc}")
        print(f"Response tokens: {candidates_tc}")
    print(response.text)
else:
    for i in response.function_calls:
        print(f"Calling function: {i.name}({i.args})")

def main():
  #  print("Hello from aiagent!")
    pass

if __name__ == "__main__":
    main()
