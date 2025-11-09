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
        "customer_business_objectives": "Not Available",
        "account_landscape": {
            "areas_of_focus": [],
            "revenue_projection": []
        },
        "account_relationships": [],
        "account_strategy": [],
        "opportunity_win_plans": []
    }

def fill_missing_fields(data, default):
    if isinstance(default, dict):
        for key, val in default.items():
            if key not in data:
                data[key] = val
            else:
                data[key] = fill_missing_fields(data[key], val)
    elif isinstance(default, list):
        if not isinstance(data, list) or len(data) == 0:
            return default
        else:
            filled_list = []
            for item in data:
                filled_list.append(fill_missing_fields(item, default[0]))
            return filled_list
    return data

def render_template_to_docx(template_path, json_data, output_path):
    # Load base structure
    schema = get_default_schema()

    # Validate and complete schema
    cleaned_data = fill_missing_fields(json_data, schema)

    # Load and render template
    tpl = DocxTemplate(template_path)
    tpl.render(cleaned_data)
    tpl.save(output_path)
