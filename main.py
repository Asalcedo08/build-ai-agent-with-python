import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions, call_function

#Get the api key
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

#Check if found and set key
if api_key == None:
    raise RuntimeError("gemini key not found")
client = genai.Client(api_key=api_key)

#Set up CLI prompt reader
parser = argparse.ArgumentParser(description="Gemini 2.5 flash chat")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

for _ in range(20):
    #Get response from gemini
    response = client.models.generate_content(model="gemini-2.5-flash", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
    
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    #Check if api request worked and print info
    if response.usage_metadata == None:
        raise RuntimeError("failed API request")
    #Checking if metadata should print
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls:
        function_results = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, args.verbose)

            if not function_call_result.parts:
                raise Exception()
            if function_call_result.parts[0].function_response == None:
                raise Exception()
            if function_call_result.parts[0].function_response.response == None:
                raise Exception()
            function_results.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

        messages.append(types.Content(role="user", parts=function_results))



    if not response.function_calls:
        print(response.text)
        break

else:
    print("max iterations reached")
    sys.exit(1)



