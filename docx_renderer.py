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

JUNK_STRINGS = {
    "omegaomega", "asdf", "test", "unknown", "n/a", "none", "null",
    "lorem", "???", "not sure", "demo", "test123", "n.a.", "--"
}

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
        instructions
        + "\n\n🧠 ENHANCED REQUIREMENTS:\n"
        + "- Expand answers into full business-ready sentences when the source contains supporting context.\n"
        + "- Do NOT condense insights to one-liners like 'Reduce AR'. YOU MUST Provide reasoning, value, and metrics.\n"
        + "- Be narrative-oriented: explain the strategic importance of fields like opportunity_alignment, red_flags, and sso.\n"
        + "- If data is missing but logic allows, infer structure (e.g. explain missing decision process by noting it's TBD).\n"
        + "- Leverage all relevant business metrics, pain points, financials, or buyer motivations in your output.\n"
        + "- Use bullet points only when the field requires lists. Otherwise, prefer coherent paragraph form.\n"
        + "- Think like a deal strategist. Your answers should tell the story of the pursuit, not just list generic terms.\n"
        + "- Expand answers where contextual details AS MUCH AS POSSIBLE WHEN are available. Do NOT truncate to short phrases.\n"
        + "- NEVER skip fields, and NEVER use shallow phrases like 'Not Available' alone—explain what is missing, e.g., 'Buyer roles not confirmed yet'.\n"
        + "- Each section (e.g. svs8, alignment_summary) must provide deal context, progress blockers, and value realization potential.\n"
        + "- When multiple values are embedded in a paragraph, split them correctly across lists/objects.\n"
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
