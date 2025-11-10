import os
import json
import re
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

JUNK_STRINGS = {"omegaomega", "asdf", "test", "unknown", "n/a", "none", "lorem", "???", "not sure"}


def clean_string(s):
    if not isinstance(s, str):
        return s
    s = s.strip()
    if not s or s.lower() in JUNK_STRINGS:
        return "Not Available"
    # Remove repeated junk (e.g. "OmegaOmegaOmega")
    s = re.sub(r"(Not Available)+", "Not Available", s, flags=re.I)
    s = re.sub(r"(Omega)+", "Omega", s)
    return s


def walk_and_clean(obj):
    if isinstance(obj, dict):
        return {k: walk_and_clean(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [walk_and_clean(i) for i in obj]
    elif isinstance(obj, str):
        return clean_string(obj)
    return obj


def inject_fallbacks(data):
    """Ensure all schema-required fields are present."""
    for key in REQUIRED_TOP_KEYS:
        if key not in data:
            data[key] = [] if key == "opportunity_win_plans" else {}

    # Fix omega_team structure
    if "omega_team" not in data.get("account_overview", {}):
        data["account_overview"]["omega_team"] = [{
            "name": "Not Available",
            "role_title": "Not Available",
            "location": "Not Available"
        }]

    # Fix malformed 'evidence'
    for area in data.get("account_landscape", {}).get("areas_of_focus", []):
        if not isinstance(area.get("evidence"), dict):
            area["evidence"] = {
                "stated_objectives": "Not Available",
                "need_external_help": "Not Available",
                "relationships_exist": "Not Available"
            }

    # Fix malformed business objectives
    if isinstance(data.get("customer_business_objectives"), str):
        data["customer_business_objectives"] = {
            "primary_objectives": ["Not Available"],
            "secondary_objectives": ["Not Available"]
        }

    return data


def parse_input_to_schema(input_path):
    """Extract raw input, send to GPT, return cleaned + validated JSON output."""
    raw_text = extract_text_from_file(input_path)
    if not raw_text or len(raw_text.strip()) < 10:
        raise ValueError("Input content is empty or too short.")

    with open("instructions.txt", "r", encoding="utf-8") as f:
        instructions = f.read()

    system_prompt = (
        instructions
        + "\n\nADDITIONAL MANDATES:\n"
        + "- Never return repeated words like 'NotAvailableNotAvailable' or 'OmegaOmega'.\n"
        + "- Split multi-action or multi-owner items into separate objects.\n"
        + "- Avoid hallucinations or fake data. If unsure, use 'Not Available'.\n"
        + "- Ensure all fields in schema are filled, even if some values are placeholders.\n"
        + "- When extracting nested lists (e.g. opportunity_action_plan), split based on action boundaries.\n"
        + "- Return real values and phrases from the input, not guesses.\n"
        + "- Chain of thought must be reflected in field mapping, especially for insight stories, red flags, etc.\n"
    )

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": raw_text}
        ],
        temperature=0.2,
    )

    raw_output = response.choices[0].message.content.strip()

    # Extract JSON portion
    json_start = raw_output.find("{")
    json_end = raw_output.rfind("}") + 1
    json_block = raw_output[json_start:json_end]

    try:
        parsed_json = json.loads(json_block)
    except Exception as e:
        raise ValueError(f"JSON parsing error:\n{json_block}\n\nError: {e}")

    # Clean and validate
    parsed_json = walk_and_clean(parsed_json)
    parsed_json = inject_fallbacks(parsed_json)

    # Extract file naming info
    account_name = parsed_json.get("account_overview", {}).get("account_name", "Account_Plan_Output")

    return parsed_json, account_name
