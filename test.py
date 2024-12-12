# Use: python test_llama.py
# Will output three .json files for the four models

import openai
import json

class_api_key = "cmsc-35360"
client_8b = openai.OpenAI(
    api_key=class_api_key,
    base_url="http://103.101.203.226:80/v1",
)
client_70b = openai.OpenAI(
    api_key=class_api_key,
    base_url="http://195.88.24.64:80/v1",
)
client_405b = openai.OpenAI(
    api_key=class_api_key,
    base_url="http://66.55.67.65:80/v1",
)
client_qwen = openai.OpenAI(
    api_key="lm-studio",
    base_url="http://localhost:1234/v1", 
)

models = [["meta-llama/Meta-Llama-3.1-8B-Instruct", client_8b, "l31_8b"],
          ["meta-llama/Meta-Llama-3.1-70B-Instruct", client_70b, "l31_70b"],
          ["llama31-405b-fp8", client_405b, "l31_405b"],
          ["qwen2.5-coder-32b-instruct", client_qwen, "qwen_32b"]]

def ask_model(model_name, model_client, prompt) -> str:
    chat_response = model_client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt},],
        temperature=0.0,
        max_tokens=2056,
    )
    response = chat_response.choices[0].message.content
    return response

def read_file_lines(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        lines = [line.rstrip('\n') for line in file]
    return lines

questions = read_file_lines("./questions.txt")

for model in models:
    model_name = model[0]
    model_client = model[1]
    model_nick = model[2]
    model_bank = {}
    print(model_name)
    for question in questions:
        print(f"Question: {question}")
        response = ask_model(model_name, model_client, question)
        print(f"Response:\n{response}")
        model_bank[question] = response
    model_file = f"{model_nick}.json"
    print(f"Writing into {model_file}")
    with open(model_file, "w") as f:
        json.dump(model_bank, f, indent = 4)

