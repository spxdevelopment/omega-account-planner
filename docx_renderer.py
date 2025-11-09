import os
import json
from docxtpl import DocxTemplate


def get_default_schema():
    return {
        "account_overview": {
            "account_name": "Not Available",
            "current_segment": "Not Available",
            "two_year_potential_segment": "Not Available",
            "account_owner": "Not Available",
            "data_created": "Not Available",
            "date_last_updated": "Not Available",
            "omega_team": [{
                "name": "Not Available",
                "role_title": "Not Available",
                "location": "Not Available"
            }]
        },
        "omega_history": {
            "revenue_fy24": "Not Available",
            "projects_fy24": "Not Available",
            "business_impact_fy24": "Not Available",
            "revenue_fy25": "Not Available",
            "projects_fy25": "Not Available",
            "business_impact_fy25": "Not Available",
            "non_project_activities_fy25": "Not Available"
        },
        "customer_health": {
            "status": "Not Available",
            "nps_reference": "Not Available",
            "red_flags": "Not Available"
        },
        "fy26_path_to_plan_summary": {
            "existing_sold_ec": "Not Available",
            "qualified_opportunities": "Not Available",
            "total": "Not Available",
            "fy26_goal": "Not Available",
            "gap_to_goal": "Not Available",
            "white_space_with_signal": "Not Available",
            "white_space_without_signal": "Not Available"
        },
        "customer_business_objectives": {
            "primary_objectives": ["Not Available"],
            "secondary_objectives": ["Not Available"]
        },
        "account_landscape": {
            "areas_of_focus": [{
                "name": "Not Available",
                "evidence": {
                    "stated_objectives": "Not Available",
                    "need_external_help": "Not Available",
                    "relationships_exist": "Not Available"
                },
                "impact_fy26": "Not Available"
            }],
            "revenue_projection": [{
                "name": "Not Available",
                "category": "Not Available",
                "area_of_focus": "Not Available",
                "projected_close": "Not Available",
                "est_tcv": "Not Available",
                "fy26_revenue": "Not Available",
                "sf_opp_id": "Not Available"
            }]
        },
        "account_relationships": [{
            "customer_name_title": "Not Available",
            "area_of_focus": "Not Available",
            "current_status": "Not Available",
            "development_objective": "Not Available",
            "actions": "Not Available",
            "omega_point_person": "Not Available"
        }],
        "account_strategy": [{
            "action_item": "Not Available",
            "owner": "Not Available",
            "due_date": "Not Available",
            "completed_date": "Not Available"
        }],
        "opportunity_win_plans": [{
            "opportunity_name": "Not Available",
            "sfdc_id": "Not Available",
            "omega_sales_leader": "Not Available",
            "alignment_score": "Not Available",
            "alignment_questions": {
                "stated_objectives": "Not Available",
                "need_external_help": "Not Available",
                "relationships_exist": "Not Available"
            },
            "alignment_summary": "Not Available",
            "svs8": {
                "single_sales_objective_defined": "Not Available",
                "coach_identified": "Not Available",
                "insight_stories_selected": "Not Available",
                "why_change_now": "Not Available",
                "why_omega": "Not Available",
                "business_case_developed": "Not Available",
                "decision_process_understood": "Not Available",
                "red_flags_present": "Not Available"
            },
            "sso": "Not Available",
            "coach": {
                "name": "Not Available",
                "title_role": "Not Available",
                "influence": "Not Available",
                "notes": "Not Available"
            },
            "insight_stories": [{
                "story": "Not Available",
                "referenceable": "Not Available",
                "omega_contact": "Not Available",
                "notes": "Not Available"
            }],
            "why_change_now_detail": "Not Available",
            "why_omega_detail": "Not Available",
            "business_case": {
                "solution": "Not Available",
                "benefit": "Not Available"
            },
            "decision_process": {
                "buyers": {
                    "economic": "Not Available",
                    "coach": "Not Available",
                    "technical": "Not Available",
                    "user": "Not Available"
                },
                "process": "Not Available",
                "criteria": "Not Available"
            },
            "red_flags": [{
                "risk": "Not Available",
                "mitigation": "Not Available"
            }],
            "opportunity_action_plan": [{
                "item": "Not Available",
                "owner": "Not Available",
                "due_date": "Not Available",
                "completed_date": "Not Available"
            }]
        }]
    }


def fill_missing_fields(data, default):
    if isinstance(default, dict):
        if not isinstance(data, dict):
            return default

        for key, val in default.items():
            if key not in data:
                data[key] = val
            elif isinstance(val, dict):
                if not isinstance(data[key], dict):
                    data[key] = val  # Force replace with default dict
                else:
                    data[key] = fill_missing_fields(data[key], val)
            elif isinstance(val, list):
                if not isinstance(data[key], list) or len(data[key]) == 0:
                    data[key] = val
                else:
                    new_list = []
                    for item in data[key]:
                        if isinstance(val[0], dict):
                            # Ensure every list item conforms to the expected structure
                            if not isinstance(item, dict):
                                new_list.append(val[0])  # fallback
                            else:
                                new_list.append(fill_missing_fields(item, val[0]))
                        else:
                            new_list.append(item)
                    data[key] = new_list
    elif isinstance(default, list):
        if not isinstance(data, list) or len(data) == 0:
            return default
        return [fill_missing_fields(item, default[0]) for item in data]

    return data



def render_template_to_docx(template_path, json_data, output_path):
    try:
        schema = get_default_schema()
        cleaned_data = fill_missing_fields(json_data, schema)

        if not isinstance(cleaned_data.get("opportunity_win_plans"), list) or len(cleaned_data["opportunity_win_plans"]) == 0:
            cleaned_data["opportunity_win_plans"] = schema["opportunity_win_plans"]

        # ✅ Sanity fix for evidence blocks to prevent crashes
        for area in cleaned_data.get("account_landscape", {}).get("areas_of_focus", []):
            if not isinstance(area.get("evidence"), dict):
                area["evidence"] = {
                    "stated_objectives": "Not Available",
                    "need_external_help": "Not Available",
                    "relationships_exist": "Not Available"
                }

        # ✅ Now render the template
        tpl = DocxTemplate(template_path)
        tpl.render(cleaned_data)
        tpl.save(output_path)

    except Exception as e:
        raise RuntimeError(f"Failed to render template: {e}")



