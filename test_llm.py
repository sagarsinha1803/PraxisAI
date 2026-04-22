import requests

def call_llm(messages):
    
    URL = "http://localhost:11434/api/chat"

    response = requests.post(URL, 
                            json = {
                                "model": "llama3.2",
                                "messages":messages,
                                "stream": False
                            })
    return response.json()["message"]["content"]

messages = []

messages.append({"role": "user", "content": "My name is sagar."})
response = call_llm(messages)
print("AI: ", {response})

messages.append({"role": "assistant", "content": response})


messages.append({"role": "user", "content": "What is my name?"})
response = call_llm(messages)
print("AI: ", {response})

# res = call_llm("What is the capital of France?")
# print(res)
