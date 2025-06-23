from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
import subprocess

load_dotenv()

client = OpenAI()

# ✅ write_file tool
def write_file(file_path: str, content: str):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ File created at {file_path}"
    except Exception as e:
        return f"❌ Error writing file: {str(e)}"

# ✅ Fixed run_command tool
def run_command(cmd: str):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip() if result.stdout else result.stderr.strip()
    except Exception as e:
        return f"❌ Error running command: {str(e)}"

# ✅ get_weather tool
def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text.strip()}."
    return "Something went wrong"

# ✅ Available tools
available_tools = {
    "get_weather": get_weather,
    "run_command": run_command,
    "write_file": write_file,
}

# ✅ System prompt (unchanged)
SYSTEM_PROMPT = f"""
You are a helpful AI Assistant who is specialized in resolving user query.
You work on start, plan, action, observe mode.

For the given user query and available tools, plan the step-by-step execution.
Then select the relevant tool from the available tool.

Wait for the observation and based on that, resolve the query.

Rules:
- Follow the output JSON Format.
- Always perform one step at a time and wait for next input.
- Carefully analyze the user query.

Output JSON Format: {{
      "step": "string",
      "content": "string",
      "function": "The name of function if the step is action",
      "input": "The input parameter for the function"
}}

Available Tools:
- "get_weather": Takes a city name as an input and returns the current weather.
- "run_command": Executes Linux shell command.
- "write_file": Takes 'file_path' and 'content' to write a file.

Example:
User Query: What is the weather of New York?
output: {{"step": "plan", "content": "User wants weather for New York."}}
output: {{"step": "plan", "content": "I will call get_weather"}}
output: {{"step": "action", "function": "get_weather", "input": "New York"}}
output: {{"step": "observe", "output": "Partly Cloudy 25°C"}}
output: {{"step": "output", "content": "The weather for New York is Partly Cloudy 25°C"}}
"""

# ✅ Initial message setup
messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

query = input("> ")
messages.append({"role": "user", "content": query})

# ✅ Main loop
while True:
    response = client.chat.completions.create(
        model="gpt-4.1",
        response_format={"type": "json_object"},
        messages=messages
    )

    ai_message = response.choices[0].message.content
    messages.append({"role": "assistant", "content": ai_message})
    parsed_response = json.loads(ai_message)

    step = parsed_response.get("step")

    if step == "plan":
        print(f"🧠: {parsed_response.get('content')}")
        continue

    elif step == "action":
        tool_name = parsed_response.get("function")
        tool_input = parsed_response.get("input")

        print(f"🔩🔩: Calling Tool: {tool_name} with input {tool_input}")

        if tool_name in available_tools:
            if isinstance(tool_input, dict):
                output = available_tools[tool_name](**tool_input)
            else:
                output = available_tools[tool_name](tool_input)

            messages.append({
                "role": "user",
                "content": json.dumps({"step": "observe", "output": output})
            })
        continue

    elif step == "output":
        print(f"🤖: {parsed_response.get('content')}")
        break
