# ask_model.py
# Sends a question to Gemini with the tool declarations and prints the tool call the model requests.

import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from tool_schemas import TOOL_DECLARATIONS
from dispatch import run_tool_call

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"), http_options=types.HttpOptions(timeout=20000))

MODEL = "gemini-3.5-flash-lite"

question = " ".join(sys.argv[1:]) or "What is the average score for student S001?"

tools = types.Tool(function_declarations=[
    types.FunctionDeclaration(
        name=d["name"],
        description=d["description"],
        parameters_json_schema=d["parameters"],
    )
    for d in TOOL_DECLARATIONS
])

response = client.models.generate_content(
    model=MODEL,
    contents=question,
    config=types.GenerateContentConfig(tools=[tools], temperature=0),
)

calls = response.function_calls or []
if not calls:
    print("No tool requested.")
    print(response.text)
for call in calls:
    print(run_tool_call(call.name, dict(call.args)))