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
    for key in REQUIRED_TOP_KEYS:
        if key not in data:
            data[key] = [] if key == "opportunity_win_plans" else {}

    if "omega_team" not in data.get("account_overview", {}):
        data["account_overview"]["omega_team"] = [{
            "name": "Not Available",
            "role_title": "Not Available",
            "location": "Not Available"
        }]

    for area in data.get("account_landscape", {}).get("areas_of_focus", []):
        if not isinstance(area.get("evidence"), dict):
            area["evidence"] = {
                "stated_objectives": "Not Available",
                "need_external_help": "Not Available",
                "relationships_exist": "Not Available"
            }

    if isinstance(data.get("customer_business_objectives"), str):
        data["customer_business_objectives"] = {
            "primary_objectives": ["Not Available"],
            "secondary_objectives": ["Not Available"]
        }

    return data


def parse_input_to_schema(input_path):
    raw_text = extract_text_from_file(input_path)
    if not raw_text or len(raw_text.strip()) < 10:
        raise ValueError("Input content is empty or too short.")

    with open("instructions.txt", "r", encoding="utf-8") as f:
        instructions = f.read()

    system_prompt = (
        instructions +
        "\n\nADDITIONAL MANDATES:\n"
        "- Never return repeated junk like 'NotAvailableNotAvailable' or 'OmegaOmega'.\n"
        "- Split multi-action or multi-owner items into separate objects.\n"
        "- Avoid hallucinations or fake data. Use 'Not Available' if nothing relevant exists.\n"
        "- Expand answers with full context. Never use 2–3 words when the source has more detail.\n"
        "- NEVER reduce business case, SSO, or insight stories to 2–3 words. Write 1–2 sentences using specific input phrasing.\n"
        "- Use actual metrics, names, quotes, or impacts when writing business_case, alignment_summary, coach notes. All these should come from the input details. The actions can come from the inputs but you can include a suggestions based on the input and specify that this is a suggestions of action\n"
        "- Always include:\n"
        "    • at least one coach or possible coach if it is not well defined\n"
        "    • at least one insight_story if applicable\n"
        "    • a full opportunity_action_plan with 2+ steps\n"
        "    • full red_flags list with matched mitigations\n"
        "- Treat the opportunity as a storyline: summarize what the client needs, what Omega offers, and how value is measured.\n"
        "- Do not invent. Use only what is stated or logically implied from source.\n"
        "- Lists (like actions, relationships, projections) should never be flattened into text blobs.\n"
        "- Think like a deal strategist. Your answers should tell the story of the pursuit, not just list generic terms.\n"
        "- Chain of thought must be reflected in field mapping, especially for insight stories, red flags, etc.\n"

    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": raw_text}
        ],
        temperature=0.2,
    )

    raw_output = response.choices[0].message.content.strip()

    json_start = raw_output.find("{")
    json_end = raw_output.rfind("}") + 1
    json_block = raw_output[json_start:json_end]

    try:
        parsed_json = json.loads(json_block)
    except Exception as e:
        raise ValueError(f"JSON parsing error:\n{json_block}\n\nError: {e}")

    parsed_json = walk_and_clean(parsed_json)
    parsed_json = inject_fallbacks(parsed_json)

    account_name = parsed_json.get("account_overview", {}).get("account_name", "Account_Plan_Output")

    return parsed_json, account_name
