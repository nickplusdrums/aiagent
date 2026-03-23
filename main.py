import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import *
    
def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)
    for _ in range(20):
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents = messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt),
        )
        if response.usage_metadata:
            prompt_tc = response.usage_metadata.prompt_token_count
            candidates_tc = response.usage_metadata.candidates_token_count

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        function_responses = []

        if not response.function_calls:
            print(response.text)
            return
        
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_tc}")
            print(f"Response tokens: {candidates_tc}")
        for i in response.function_calls:
            function_call_result = call_function(i, args.verbose)
            if function_call_result.parts == []:
                raise Exception("Empty Parts List")
            if function_call_result.parts[0].function_response is None:
                raise Exception("Function Response is None")
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("Function Response is None")
            function_responses.append(function_call_result.parts[0])
        messages.append(types.Content(role="user", parts=function_responses))
    else:
        print("Agent stopped: reached max iterations without a final response")

if __name__ == "__main__":
    main()
