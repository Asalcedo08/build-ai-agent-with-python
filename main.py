import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

#Get response from gemini
response = client.models.generate_content(model="gemini-2.5-flash", contents=messages)

#Check if api request worked and print info
if response.usage_metadata == None:
    raise RuntimeError("failed API request")
#Checking if metadata should print
if args.verbose:
    print(f"User prompt: {args.user_prompt}\nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
print(response.text)

