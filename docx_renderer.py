import os
import json
from docxtpl import DocxTemplate

# Adds all missing nested structures
def enforce_schema_structure(data):
    if not isinstance(data, dict):
        return {}

    if not isinstance(data.get("account_overview"), dict):
        data["account_overview"] = {}

    if "omega_team" not in data["account_overview"] or not isinstance(data["account_overview"].get("omega_team"), list):
        data["account_overview"]["omega_team"] = [{
            "name": "Not Available",
            "role_title": "Not Available",
            "location": "Not Available"
        }]

    if "account_relationships" not in data:
        data["account_relationships"] = {"executive_sponsors": [], "influencers": []}

    if not isinstance(data.get("opportunity_win_plans"), list):
        data["opportunity_win_plans"] = []

    for opp in data["opportunity_win_plans"]:
        if not isinstance(opp, dict):
            continue

        opp.setdefault("alignment_questions", {
            "stated_objectives": "Not Available",
            "need_external_help": "Not Available",
            "relationships_exist": "Not Available"
        })

        opp.setdefault("svs8", {
            "single_sales_objective_defined": "Not Available",
            "coach_identified": "Not Available",
            "insight_stories_selected": "Not Available",
            "why_change_now": "Not Available",
            "why_omega": "Not Available",
            "business_case_developed": "Not Available",
            "decision_process_understood": "Not Available",
            "red_flags_present": "Not Available"
        })

        opp.setdefault("coach", {
            "name": "Not Available",
            "title_role": "Not Available",
            "influence": "Not Available",
            "notes": "Not Available"
        })

        opp.setdefault("insight_stories", [{
            "story": "Not Available",
            "referenceable": "Not Available",
            "omega_contact": "Not Available",
            "notes": "Not Available"
        }])

        opp.setdefault("business_case", {
            "solution": "Not Available",
            "benefit": "Not Available"
        })

        opp.setdefault("decision_process", {
            "buyers": {
                "economic": "Not Available",
                "coach": "Not Available",
                "technical": "Not Available",
                "user": "Not Available"
            },
            "process": "Not Available",
            "criteria": "Not Available"
        })

        opp.setdefault("red_flags", [{"risk": "Not Available", "mitigation": "Not Available"}])

        opp.setdefault("opportunity_action_plan", [{
            "item": "Not Available",
            "owner": "Not Available",
            "due_date": "Not Available",
            "completed_date": "Not Available"
        }])

    return data


# ✅ FINAL FUNCTION — use this in app.py
def render_template_to_docx(template_path, json_data, output_path):
    cleaned_data = enforce_schema_structure(json_data)
    tpl = DocxTemplate(template_path)
    tpl.render(cleaned_data)
    tpl.save(output_path)
