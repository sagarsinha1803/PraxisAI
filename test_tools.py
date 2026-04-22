import requests
import json

def get_weather(city):
    return f"The wather in {city} is sunny with a high of 25°C."


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a given city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city."
                    }
                },
                "required": ["city"]
            }
        }
    }
]

tools_registry = {
    "get_weather": get_weather
}

def call_llm(messages):
    URL = "http://localhost:11434/api/chat"

    response = requests.post(
        URL,
        json={
            "model": "llama3.2",
            "messages": messages,
            "tools": tools,
            "stream": False
        }
    )
    return response.json()["message"]


def run_agent(user_message):
    message = [{"role": "user", "content": user_message}]
    while True:
        response = call_llm(message)
        tool_calls = response.get("tool_calls", None)

        if tool_calls and len(tool_calls) > 0:
            for each_tool in tool_calls:
                tool_name = each_tool.get("function").get("name")
                tool_args = each_tool.get("function").get("arguments")

                print(f"\nLLM wants to call tool: {tool_name} with args: {tool_args}\n")
                
                result = tools_registry[tool_name](**tool_args)

                print(f"-> Tool returned: {result}\n")

                message.append({
                    "role": "tool",
                    "content": result
                })
        else:
            print(f"LLM response: {response.get('content')}")
            break


# messages = [{"role": "user", "content": "What is the weather in Mumbai?"}]
# response = call_llm(messages)

# print("Raw response from LLM: ", response)
# print(json.dumps(response, indent=2))

run_agent("What is the weather in Mumbai?")
