import json
import openai
from utils import extract_text_from_file
from openai import OpenAI

client = OpenAI()  # uses OPENAI_API_KEY from env

def parse_input_to_schema(file_path):
    raw_text = extract_text_from_file(file_path)

    with open("instructions.txt", "r") as f:
        system_prompt = f.read()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": raw_text}
        ],
        temperature=0.2
    )

    result = response.choices[0].message.content
    parsed_json = json.loads(result)
    account_name = parsed_json.get("account_overview", {}).get("account_name", "Account_Plan_Output")
    return parsed_json, account_name
