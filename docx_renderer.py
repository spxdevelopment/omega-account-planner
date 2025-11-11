import os
import json
from docxtpl import DocxTemplate

def get_default_schema():
    return {
        "account_overview": {
            "account_name": "Account name not identified.",
            "current_segment": "Current segment not stated.",
            "two_year_potential_segment": "Growth segment not projected.",
            "account_owner": "Account owner missing.",
            "data_created": "Creation date not available.",
            "date_last_updated": "Last update date missing.",
            "omega_team": [{
                "name": "Unspecified",
                "role_title": "Unspecified",
                "location": "Unspecified"
            }]
        },
        "omega_history": {
            "revenue_fy24": "FY24 revenue not available.",
            "projects_fy24": "FY24 project details missing.",
            "business_impact_fy24": "No FY24 impact described.",
            "revenue_fy25": "FY25 revenue not available.",
            "projects_fy25": "FY25 project info missing.",
            "business_impact_fy25": "No FY25 business impact found.",
            "non_project_activities_fy25": "Non-project activities not listed."
        },
        "customer_health": {
            "status": "No customer health assessment found.",
            "nps_reference": "No NPS or reference quote available.",
            "red_flags": "No red flags documented."
        },
        "fy26_path_to_plan_summary": {
            "existing_sold_ec": "Existing sold EC not provided.",
            "qualified_opportunities": "Qualified opportunities not listed.",
            "total": "Total not calculated.",
            "fy26_goal": "FY26 revenue goal missing.",
            "gap_to_goal": "Gap to goal not determined.",
            "white_space_with_signal": "No whitespace with signal identified.",
            "white_space_without_signal": "No whitespace without signal documented."
        },
        "customer_business_objectives": {
            "primary_objectives": ["Primary objectives not stated."],
            "secondary_objectives": ["Secondary objectives missing."]
        },
        "account_landscape": {
            "areas_of_focus": [{
                "name": "Focus area unspecified.",
                "evidence": {
                    "stated_objectives": "Objectives not found.",
                    "need_external_help": "Need for external help not mentioned.",
                    "relationships_exist": "Relationships not detailed."
                },
                "impact_fy26": "FY26 impact not described."
            }],
            "revenue_projection": [{
                "name": "Opportunity name missing.",
                "category": "Category not stated.",
                "area_of_focus": "Area of focus not given.",
                "projected_close": "Close date not included.",
                "est_tcv": "Estimated TCV not available.",
                "fy26_revenue": "FY26 revenue portion not shown.",
                "sf_opp_id": "Salesforce ID not listed."
            }]
        },
        "account_relationships": [{
            "customer_name_title": "Customer name/title not listed.",
            "area_of_focus": "Focus area not identified.",
            "current_status": "Relationship status unclear.",
            "development_objective": "Development objective missing.",
            "actions": "Actions not described.",
            "omega_point_person": "Omega point person not assigned."
        }],
        "account_strategy": [{
            "action_item": "Action item not outlined.",
            "owner": "Owner not specified.",
            "due_date": "Due date not assigned.",
            "completed_date": "Completion status unknown."
        }],
        "opportunity_win_plans": [{
            "opportunity_name": "Opportunity name missing.",
            "sfdc_id": "SFDC ID not listed.",
            "omega_sales_leader": "Sales leader not named.",
            "alignment_score": "Alignment score not available.",
            "alignment_questions": {
                "stated_objectives": "Stated objectives not found.",
                "need_external_help": "External help need unclear.",
                "relationships_exist": "Relevant relationships not detailed."
            },
            "alignment_summary": "No summary of strategic alignment provided.",
            "svs8": {
                "single_sales_objective_defined": "SSO not defined.",
                "coach_identified": "No coach identified.",
                "insight_stories_selected": "No insight stories selected.",
                "why_change_now": "Change urgency not described.",
                "why_omega": "Why Omega not articulated.",
                "business_case_developed": "Business case not developed.",
                "decision_process_understood": "Decision process unclear.",
                "red_flags_present": "Red flags not outlined."
            },
            "sso": "SSO statement missing.",
            "coach": {
                "name": "Name not provided.",
                "title_role": "Role/title missing.",
                "influence": "Influence level not assessed.",
                "notes": "No notes available."
            },
            "insight_stories": [{
                "story": "No story given.",
                "referenceable": "Referenceability not known.",
                "omega_contact": "Omega contact missing.",
                "notes": "Story notes not provided."
            }],
            "why_change_now_detail": "Change rationale not found.",
            "why_omega_detail": "Omega differentiation not explained.",
            "business_case": {
                "solution": "Solution details missing.",
                "benefit": "Business benefit not stated."
            },
            "decision_process": {
                "buyers": {
                    "economic": "Economic buyer not listed.",
                    "coach": "Coach buyer not identified.",
                    "technical": "Technical buyer missing.",
                    "user": "User buyer not referenced."
                },
                "process": "Buying process not outlined.",
                "criteria": "Decision criteria not provided."
            },
            "red_flags": [{
                "risk": "Risk not identified.",
                "mitigation": "Mitigation tactic not specified."
            }],
            "opportunity_action_plan": [{
                "item": "Action step not listed.",
                "owner": "Owner not assigned.",
                "due_date": "Due date missing.",
                "completed_date": "Completion date not recorded."
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
                data[key] = fill_missing_fields(data.get(key, {}), val)
            elif isinstance(val, list):
                if not isinstance(data.get(key), list) or not data[key]:
                    data[key] = val
                else:
                    data[key] = [fill_missing_fields(item, val[0]) if isinstance(item, dict) else item for item in data[key]]
    elif isinstance(default, list):
        if not isinstance(data, list) or not data:
            return default
        return [fill_missing_fields(item, default[0]) for item in data]
    return data

def render_template_to_docx(template_path, json_data, output_path):
    try:
        schema = get_default_schema()
        cleaned_data = fill_missing_fields(json_data, schema)

        tpl = DocxTemplate(template_path)
        tpl.render(cleaned_data)
        tpl.save(output_path)

    except Exception as e:
        raise RuntimeError(f"Failed to render template: {e}")
