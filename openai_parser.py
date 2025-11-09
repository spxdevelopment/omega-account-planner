import os
import json
from openai import OpenAI
from utils import extract_text_from_file

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_input_to_schema(input_path):
    """
    Extracts text from input file, sends it to OpenAI, and parses the response into a dict.
    Always returns (parsed_json, account_name).
    """

    # Step 1: Extract plain text
    text = extract_text_from_file(input_path)

    if not text or len(text.strip()) < 10:
        raise ValueError("Input content is empty or too short to process.")

    # Step 2: Load your system instruction prompt
    with open("instructions.txt", "r", encoding="utf-8") as f:
        base_instructions = f.read()

    system_prompt = (
        base_instructions
        + "\n\nIMPORTANT:\n"
        + "You must return ONLY a valid JSON object matching Omega_Account_Plan_Schema.json.\n"
        + "Do not include explanations, markdown, or comments.\n"
        + "Your response must begin with '{' and end with '}'."
    )

    # Step 3: Query GPT-4o
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        temperature=0.2,
    )

    # Step 4: Extract model response
    raw_output = response.choices[0].message.content.strip()

    # Step 5: Isolate the JSON block (sometimes model adds text or markdown fences)
    start = raw_output.find("{")
    end = raw_output.rfind("}") + 1
    json_block = raw_output[start:end] if start != -1 and end != -1 else raw_output

    # Step 6: Parse JSON safely
    try:
        parsed_json = json.loads(json_block)
    except Exception as e:
        raise ValueError(
            f"Failed to parse JSON from model output:\n\n"
            f"```json\n{json_block}\n```\n\nError: {e}"
        )

    # Step 7: Get account name safely
    account_name = parsed_json.get("account_overview", {}).get("account_name", "Account_Plan_Output")

    return parsed_json, account_name
