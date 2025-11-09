import os
import json
import openai
from utils import extract_text_from_file

# Load API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load the instructions (schema + rules)
with open("instructions.txt", "r", encoding="utf-8") as f:
    SYSTEM_INSTRUCTIONS = f.read()

def parse_input_to_schema(input_path):
    text = extract_text_from_file(input_path)

    if not text or len(text.strip()) < 10:
        raise ValueError("Input content is too short or empty.")

    messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTIONS},
        {"role": "user", "content": text}
    ]

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.2
        )
    except Exception as e:
        raise RuntimeError(f"OpenAI API call failed: {str(e)}")

    result = response.choices[0].message.content.strip()

    if not result:
        raise ValueError("OpenAI returned an empty response.")

    try:
        parsed_json = json.loads(result)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON from OpenAI: {str(e)}\n\nResponse was:\n{result}")

    # Optional: Extract account name from schema
    account_name = parsed_json.get("account_overview", {}).get("account_name", "")

    return parsed_json, account_name
