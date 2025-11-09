import os
import json
from openai import OpenAI
from utils import extract_text_from_file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_input_to_schema(input_path):
    text = extract_text_from_file(input_path)

    if not text or len(text.strip()) < 10:
        raise ValueError("Input content is empty or too short.")

    # Load your long instruction file
    with open("instructions.txt", "r", encoding="utf-8") as f:
        base_instructions = f.read()

    system_prompt = (
        base_instructions
        + "\n\nIMPORTANT:\n"
        + "You must return ONLY a valid JSON object matching Omega_Account_Plan_Schema.json.\n"
        + "Do not include any natural language, explanation, or formatting outside the JSON.\n"
        + "Your response must begin with '{' and end with '}'."
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        temperature=0.2,
    )

    raw_output = response.choices[0].message.content.strip()

    # In case model wraps JSON in text, extract the JSON block
    start = raw_output.find("{")
    end = raw_output.rfind("}") + 1
    json_block = raw_output[start:end] if start != -1 and end != -1 else raw_output

    try:
        parsed_json = json.loads(result)
    except Exception as e:
        raise ValueError(f"Failed to parse JSON from model output:\n\n{raw_output}\n\nError: {e}")

    account_name = parsed_json.get("account_overview", {}).get("account_name", "Account_Plan_Output")
    return parsed_json, account_name
