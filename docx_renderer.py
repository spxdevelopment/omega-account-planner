import os
import json
from docxtpl import DocxTemplate


def get_default_schema():
    """
    Provides a detailed contextual default schema with descriptive fallback explanations
    instead of plain 'Not Available' placeholders.
    """
    return {
        "account_overview": {
            "account_name": "Account name was not clearly identified in the input material.",
            "current_segment": "Current customer segmentation (e.g., Enterprise, Mid-Market) not stated in input.",
            "two_year_potential_segment": "Projected future segment within two years not mentioned.",
            "account_owner": "Account owner or Omega lead not specified in the provided data.",
            "data_created": "Date of account creation not found in the source.",
            "date_last_updated": "No last update date referenced in the input.",
            "omega_team": [{
                "name": "Team member name not listed.",
                "role_title": "Team member role title was not found.",
                "location": "Location for this team member was not provided."
            }]
        },

        "omega_history": {
            "revenue_fy24": "FY24 revenue not found. If the input includes financials, verify formatting.",
            "projects_fy24": "FY24 project details were not explicitly described.",
            "business_impact_fy24": "No quantitative or qualitative business impact for FY24 was referenced.",
            "revenue_fy25": "FY25 revenue or growth indicators were not extracted from the input.",
            "projects_fy25": "FY25 project activities not identified.",
            "business_impact_fy25": "Business results or impacts from FY25 were not located.",
            "non_project_activities_fy25": "Non-project initiatives were not detailed in the content."
        },

        "customer_health": {
            "status": "Customer health assessment (e.g., strong, neutral, at risk) not included in input.",
            "nps_reference": "No NPS score or client satisfaction reference found.",
            "red_flags": "No relationship risks or concerns explicitly identified in the source."
        },

        "fy26_path_to_plan_summary": {
            "existing_sold_ec": "Existing sold EC revenue for FY26 not outlined.",
            "qualified_opportunities": "Qualified opportunities were not quantified or listed.",
            "total": "Combined FY26 opportunity total could not be calculated.",
            "fy26_goal": "Revenue goal for FY26 was not clearly stated in the input.",
            "gap_to_goal": "Gap to FY26 goal could not be determined from provided figures.",
            "white_space_with_signal": "No mention of white space opportunities with buying intent.",
            "white_space_without_signal": "No white space opportunities without signals were found."
        },

        "customer_business_objectives": {
            "primary_objectives": [
                "Primary customer business objectives not documented or labeled in the input file."
            ],
            "secondary_objectives": [
                "Supporting or secondary objectives not mentioned or could not be inferred."
            ]
        },

        "account_landscape": {
            "areas_of_focus": [{
                "name": "No functional focus area specified (e.g., Revenue Cycle, IT Modernization).",
                "evidence": {
                    "stated_objectives": "Client objectives for this area were not outlined.",
                    "need_external_help": "No mention of whether external vendor assistance is required.",
                    "relationships_exist": "No relationships or partnerships were referenced."
                },
                "impact_fy26": "Impact on FY26 performance was not described."
            }],
            "revenue_projection": [{
                "name": "Opportunity or initiative name not specified.",
                "category": "Opportunity category (Sold, Qualified, WSI, WSN) not found.",
                "area_of_focus": "Area of focus connection missing.",
                "projected_close": "Projected close date not mentioned.",
                "est_tcv": "Total contract value (TCV) not stated.",
                "fy26_revenue": "FY26 revenue portion for this opportunity not found.",
                "sf_opp_id": "Salesforce Opportunity ID not listed."
            }]
        },

        "account_relationships": [{
            "customer_name_title": "Customer name and title not provided in the input.",
            "area_of_focus": "Area of focus for this relationship not mentioned.",
            "current_status": "Relationship strength or current engagement status missing.",
            "development_objective": "Relationship development plan not described.",
            "actions": "No planned actions specified for this relationship.",
            "omega_point_person": "Omega point person responsible not identified."
        }],

        "account_strategy": [{
            "action_item": "Strategic action or initiative was not listed.",
            "owner": "No owner assigned to this strategy item.",
            "due_date": "No due date or milestone found.",
            "completed_date": "Completion status or date not mentioned."
        }],

        "opportunity_win_plans": [{
            "opportunity_name": "Opportunity name was not specified.",
            "sfdc_id": "Salesforce ID not found.",
            "omega_sales_leader": "Omega sales leader for this opportunity not named.",
            "alignment_score": "No alignment score or narrative provided.",
            "alignment_questions": {
                "stated_objectives": "Customer’s stated objectives not defined in input.",
                "need_external_help": "No explicit reference to external help needs.",
                "relationships_exist": "Relationships influencing the opportunity not mentioned."
            },
            "alignment_summary": "Alignment summary missing. No detail on strategic alignment found.",
            "svs8": {
                "single_sales_objective_defined": "Single sales objective not documented or inferred.",
                "coach_identified": "No internal coach identified.",
                "insight_stories_selected": "No insight stories mentioned for this opportunity.",
                "why_change_now": "No urgency or trigger for change stated.",
                "why_omega": "No differentiators explaining 'Why Omega' provided.",
                "business_case_developed": "Business case development not referenced.",
                "decision_process_understood": "Decision process unclear or missing.",
                "red_flags_present": "No explicit red flags were documented."
            },
            "sso": "Sales objective statement not included in input.",
            "coach": {
                "name": "Coach name not mentioned in source material.",
                "title_role": "Coach’s role or title not specified.",
                "influence": "Coach influence level not assessed.",
                "notes": "Additional context on coaching relationship not found."
            },
            "insight_stories": [{
                "story": "No insight story or client reference provided.",
                "referenceable": "No confirmation if story is referenceable.",
                "omega_contact": "Omega contact for this story not stated.",
                "notes": "No extra details provided for this story."
            }],
            "why_change_now_detail": "No explanation for change urgency provided.",
            "why_omega_detail": "No detailed rationale for choosing Omega found.",
            "business_case": {
                "solution": "Solution not described in input material.",
                "benefit": "Expected benefits not quantified or listed."
            },
            "decision_process": {
                "buyers": {
                    "economic": "Economic buyer not named.",
                    "coach": "No coach role detailed.",
                    "technical": "Technical decision-maker not mentioned.",
                    "user": "End user or functional buyer not listed."
                },
                "process": "Decision-making process not outlined.",
                "criteria": "Selection criteria not discussed."
            },
            "red_flags": [{
                "risk": "No risks identified for this opportunity.",
                "mitigation": "No mitigation tactics specified."
            }],
            "opportunity_action_plan": [{
                "item": "No defined action for opportunity progression.",
                "owner": "Action owner not named.",
                "due_date": "Due date or milestone missing.",
                "completed_date": "Completion status not mentioned."
            }]
        }]
    }


def fill_missing_fields(data, default):
    """
    Recursively ensures missing fields are filled with context-aware fallbacks
    rather than blunt 'Not Available' markers.
    """
    if isinstance(default, dict):
        if not isinstance(data, dict):
            return default
        for key, val in default.items():
            if key not in data:
                data[key] = val
            elif isinstance(val, dict):
                if not isinstance(data[key], dict):
                    data[key] = val
                else:
                    data[key] = fill_missing_fields(data[key], val)
            elif isinstance(val, list):
                if not isinstance(data[key], list) or len(data[key]) == 0:
                    data[key] = val
                else:
                    merged_list = []
                    for item in data[key]:
                        if isinstance(val[0], dict):
                            if not isinstance(item, dict):
                                merged_list.append(val[0])
                            else:
                                merged_list.append(fill_missing_fields(item, val[0]))
                        else:
                            merged_list.append(item)
                    data[key] = merged_list
    elif isinstance(default, list):
        if not isinstance(data, list) or len(data) == 0:
            return default
        return [fill_missing_fields(item, default[0]) for item in data]
    return data


def render_template_to_docx(template_path, json_data, output_path):
    """
    Safely merges JSON data into the DOCX template with rich fallback narratives.
    Prevents blank fields and ensures context clarity.
    """
    try:
        schema = get_default_schema()
        cleaned_data = fill_missing_fields(json_data, schema)

        # Validate core structures
        if isinstance(cleaned_data.get("customer_business_objectives"), str):
            cleaned_data["customer_business_objectives"] = schema["customer_business_objectives"]

        if not isinstance(cleaned_data.get("account_landscape"), dict):
            cleaned_data["account_landscape"] = schema["account_landscape"]

        if not isinstance(cleaned_data["account_landscape"].get("areas_of_focus"), list):
            cleaned_data["account_landscape"]["areas_of_focus"] = schema["account_landscape"]["areas_of_focus"]

        for idx, area in enumerate(cleaned_data["account_landscape"]["areas_of_focus"]):
            if not isinstance(area, dict):
                cleaned_data["account_landscape"]["areas_of_focus"][idx] = schema["account_landscape"]["areas_of_focus"][0]
            elif not isinstance(area.get("evidence"), dict):
                area["evidence"] = schema["account_landscape"]["areas_of_focus"][0]["evidence"]

        # Guarantee at least one valid opportunity block
        if not isinstance(cleaned_data.get("opportunity_win_plans"), list) or len(cleaned_data["opportunity_win_plans"]) == 0:
            cleaned_data["opportunity_win_plans"] = schema["opportunity_win_plans"]

        # Render the Word template
        tpl = DocxTemplate(template_path)
        tpl.render(cleaned_data)
        tpl.save(output_path)

    except Exception as e:
        raise RuntimeError(f"Failed to render template: {e}")
