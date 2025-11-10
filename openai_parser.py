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
    """Ensure required top-level schema keys are present and filled in."""
    if not isinstance(data, dict):
        raise ValueError("Expected parsed JSON to be a dictionary.")

    for key in REQUIRED_TOP_KEYS:
        if key not in data or not isinstance(data[key], (dict, list)):
            data[key] = [] if key == "opportunity_win_plans" else {}

    if "omega_team" not in data.get("account_overview", {}):
        data["account_overview"]["omega_team"] = [{
            "name": "Not Available",
            "role_title": "Not Available",
            "location": "Not Available"
        }]

    return data


def fix_common_malformed_blocks(parsed_json):
    """Fix frequent formatting issues in certain nested fields."""

    # Fix malformed evidence
    areas = parsed_json.get("account_landscape", {}).get("areas_of_focus", [])
    for area in areas:
        if not isinstance(area, dict):
            continue
        if not isinstance(area.get("evidence"), dict):
            area["evidence"] = {
                "stated_objectives": "Not Available",
                "need_external_help": "Not Available",
                "relationships_exist": "Not Available"
            }

    # Fix customer_business_objectives if it's a string
    if isinstance(parsed_json.get("customer_business_objectives"), str):
        parsed_json["customer_business_objectives"] = {
            "primary_objectives": ["Not Available"],
            "secondary_objectives": ["Not Available"]
        }

    return parsed_json


def load_system_prompt():
    """Loads the combined instructions and field guidance files."""

    with open("instructions.txt", "r", encoding="utf-8") as f:
        instructions = f.read()

    guidance_path = "field_level_guidance.txt"
    if os.path.exists(guidance_path):
        with open(guidance_path, "r", encoding="utf-8") as f:
            guidance = f.read()
    else:
        guidance = ""

    system_prompt = (
        instructions.strip()
        + "\n\n"
        + guidance.strip()
        + "\n\nIMPORTANT:\n"
        + "You must return ONLY a valid JSON object matching Omega_Account_Plan_Schema.json.\n"
        + "Do not include explanations, markdown, or comments.\n"
        + "Your response must begin with '{' and end with '}'."
    )
    return system_prompt


def parse_input_to_schema(input_path):
    """
    Extracts text from input file, sends it to OpenAI, and parses the response into a dict.
    Returns: (parsed_json, account_name)
    """
    text = extract_text_from_file(input_path)
    if not text or len(text.strip()) < 10:
        raise ValueError("Input content is empty or too short to process.")

    system_prompt = load_system_prompt()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        temperature=0.2,
    )

    raw_output = response.choices[0].message.content.strip()

    # Extract just the JSON portion
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

    # Apply structure patches
    parsed_json = fix_common_malformed_blocks(parsed_json)
    parsed_json = inject_fallbacks(parsed_json)

    # Extract account name
    account_name = parsed_json.get("account_overview", {}).get("account_name", "Account_Plan_Output")

    return parsed_json, account_name
