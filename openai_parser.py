import os
import json
from openai import OpenAI
from utils import extract_text_from_file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

REQUIRED_TOP_KEYS = [
    "account_overview",
    "omega_history",
    "customer_health",
    "fy26_path_to_plan_summary",
    "customer_business_objectives",
    "account_landscape",
    "account_relationships",
    "account_strategy",
    "opportunity_win_plans"
]


def inject_fallbacks(data):
    """
    Ensure all required top-level keys and nested expected lists exist.
    Only adds 'Not Available' when data is truly absent or malformed.
    """
    for key in REQUIRED_TOP_KEYS:
        if key not in data:
            data[key] = [] if key == "opportunity_win_plans" else {}

    # Ensure omega_team is structured correctly
    if "omega_team" not in data.get("account_overview", {}):
        data["account_overview"]["omega_team"] = [{
            "name": "Not Available",
            "role_title": "Not Available",
            "location": "Not Available"
        }]

    # Validate nested evidence structure
    areas = data.get("account_landscape", {}).get("areas_of_focus", [])
    if isinstance(areas, list):
        for area in areas:
            if not isinstance(area.get("evidence"), dict):
                area["evidence"] = {
                    "stated_objectives": "Not Available",
                    "need_external_help": "Not Available",
                    "relationships_exist": "Not Available"
                }

    # Ensure customer_business_objectives is a dict
    if isinstance(data.get("customer_business_objectives"), str):
        data["customer_business_objectives"] = {
            "primary_objectives": ["Not Available"],
            "secondary_objectives": ["Not Available"]
        }

    return data


def sanitize_model_output_fields(parsed_json):
    """
    Detect hallucinations or non-business filler content in string fields.
    Replace junk entries like 'OMEGAOMEGA', 'asdf', or obvious errors.
    """
    def clean_string(value):
        if not isinstance(value, str):
            return value
        junk = ["OMEGAOMEGA", "asdf", "lorem", "unknown", "???", "n/a", "test"]
        return value.strip() if value.strip().lower() not in junk else "Not Available"

    def walk(obj):
        if isinstance(obj, dict):
            return {k: walk(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [walk(i) for i in obj]
        elif isinstance(obj, str):
            return clean_string(obj)
        else:
            return obj

    return walk(parsed_json)


def parse_input_to_schema(input_path):
    """
    Extracts input text, sends to OpenAI for structured field mapping,
    sanitizes output, and returns cleaned schema-aligned JSON.
    """
    text = extract_text_from_file(input_path)
    if not text or len(text.strip()) < 10:
        raise ValueError("Input content is empty or too short to process.")

    with open("instructions.txt", "r", encoding="utf-8") as f:
        base_instructions = f.read()

    system_prompt = (
        base_instructions
        + "\n\nEXTRACTIONS MUST:\n"
        + "• Use real business values from the input\n"
        + "• Include field-by-field details based on context\n"
        + "• Avoid filler terms like 'omegaomega', 'asdf', or 'n/a'\n"
        + "• when writing the output use spaces between the words and correctly do the chain of thought and reasoning to write the output to each field\n"
        + "• If partial data is available (e.g. only the coach name), still include the full nested field\n"
        + "\nREMEMBER:\n"
        +  "•Avoid repeat terms in the same field like Not AvailableNot AvailableNot AvailableNot Available or even like OmegaOmegaOmegaOmega \n"
        + "You are not summarizing. You are converting source info into a JSON template structure."
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

    start = raw_output.find("{")
    end = raw_output.rfind("}") + 1
    json_block = raw_output[start:end] if start != -1 and end != -1 else raw_output

    try:
        parsed_json = json.loads(json_block)
    except Exception as e:
        raise ValueError(
            f"Failed to parse JSON from model output:\n\n"
            f"```json\n{json_block}\n```\n\nError: {e}"
        )

    # Cleanup any malformed or junked fields
    parsed_json = sanitize_model_output_fields(parsed_json)

    # Inject missing schema keys
    parsed_json = inject_fallbacks(parsed_json)

    # Extract account name for file naming
    account_name = parsed_json.get("account_overview", {}).get("account_name", "Account_Plan_Output")
    return parsed_json, account_name
