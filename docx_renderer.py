import os
import json
from docxtpl import DocxTemplate

# Helper: fallback for missing nested fields
def enforce_schema_structure(data):
    if not isinstance(data.get("account_overview"), dict):
        data["account_overview"] = {}

    if "omega_team" not in data["account_overview"] or not isinstance(data["account_overview"].get("omega_team"), list):
        data["account_overview"]["omega_team"] = [{
            "name": "Not Available",
            "role_title": "Not Available",
            "location": "Not Available"
        }]

    if not isinstance(data.get("opportunity_win_plans"), list):
        data["opportunity_win_plans"] = []

    # Ensure nested fields in opportunity_win_plans
    for opp in data["opportunity_win_plans"]:
        if "alignment_questions" not in opp or not isinstance(opp["alignment_questions"], dict):
            opp["alignment_questions"] = {
                "stated_objectives": "Not Available",
                "need_external_help": "Not Available",
                "relationships_exist": "Not Available"
            }

        if "svs8" not in opp or not isinstance(opp["svs8"], dict):
            opp["svs8"] = {
                "single_sales_objective_defined": "Not Available",
                "coach_identified": "Not Available",
                "insight_stories_selected": "Not Available",
                "why_change_now": "Not Available",
                "why_omega": "Not Available",
                "business_case_developed": "Not Available",
                "decision_process_understood": "Not Available",
                "red_flags_present": "Not Available"
            }

        if "coach" not in opp or not isinstance(opp["coach"], dict):
            opp["coach"] = {
                "name": "Not Available",
                "title_role": "Not Available",
                "influence": "Not Available",
                "notes": "Not Available"
            }

        if "insight_stories" not in opp or not isinstance(opp["insight_stories"], list):
            opp["insight_stories"] = [{
                "story": "Not Available",
                "referenceable": "Not Available",
                "omega_contact": "Not Available",
                "notes": "Not Available"
            }]

        if "business_case" not in opp or not isinstance(opp["business_case"], dict):
            opp["business_case"] = {
                "solution": "Not Available",
                "benefit": "Not Available"
            }

        if "decision_process" not in opp or not isinstance(opp["decision_process"], dict):
            opp["decision_process"] = {
                "buyers": {
                    "economic": "Not Available",
                    "coach": "Not Available",
                    "technical": "Not Available",
                    "user": "Not Available"
                },
                "process": "Not Available",
                "criteria": "Not Available"
            }

        if "red_flags" not in opp or not isinstance(opp["red_flags"], list):
            opp["red_flags"] = [{"risk": "Not Available", "mitigation": "Not Available"}]

        if "opportunity_action_plan" not in opp or not isinstance(opp["opportunity_action_plan"], list):
            opp["opportunity_action_plan"] = [{
                "item": "Not Available",
                "owner": "Not Available",
                "due_date": "Not Available",
                "completed_date": "Not Available"
            }]

    return data

# Core renderer
def render_template(schema_json_path, template_path, output_path):
    with open(schema_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Inject safe fallbacks
    cleaned_data = enforce_schema_structure(data)

    tpl = DocxTemplate(template_path)
    tpl.render(cleaned_data)
    tpl.save(output_path)
