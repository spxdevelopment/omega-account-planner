import os
import json
from docxtpl import DocxTemplate

def get_default_schema():
    """
    Provides contextual schema with descriptive and business-relevant fallback explanations.
    Each missing field now includes reasoning for why the information matters and how it should be used.
    """
    return {
        "account_overview": {
            "account_name": "The official name of the customer or prospect organization was not clearly identified in the input materials. This information defines the entity to which all planning data applies and should be confirmed before sharing externally.",
            "current_segment": "The current customer segment (e.g., Enterprise, Mid-Market, Public Sector) was not specified. This determines engagement model, pricing, and strategic prioritization.",
            "two_year_potential_segment": "The projected market segment for this account within two years is not discussed. This projection helps Omega forecast account expansion and resource needs.",
            "account_owner": "The Omega account owner or primary relationship manager is missing. Identifying the accountable owner ensures governance and client accountability.",
            "data_created": "Date when this account plan was created is not found. It’s important to track plan recency for audit and planning cycles.",
            "date_last_updated": "No last update date was provided. Keeping this up to date ensures version control and accuracy for planning reviews.",
            "omega_team": [{
                "name": "No Omega team member names were captured. Team composition defines collaboration touchpoints.",
                "role_title": "The role of this Omega team member was not described. Clarifying responsibilities helps coordinate execution.",
                "location": "Location for this Omega team member was not specified. Knowing where team members are based can optimize client coverage."
            }]
        },

        "omega_history": {
            "revenue_fy24": "FY24 revenue figures are not provided. These define historical baseline performance and guide FY26 projections.",
            "projects_fy24": "No FY24 projects listed. Detailing these demonstrates Omega’s engagement history and credibility with the client.",
            "business_impact_fy24": "Business outcomes from FY24 were not stated. These typically include ROI improvements, operational gains, or cost savings achieved through Omega’s solutions.",
            "revenue_fy25": "FY25 revenue performance was not found. This is essential for identifying year-over-year trajectory.",
            "projects_fy25": "FY25 initiatives not detailed. Capture all engagements that influenced FY25 results, including in-progress projects.",
            "business_impact_fy25": "The FY25 impact was not recorded. Describe results such as efficiency, patient outcomes, cost reduction, or modernization.",
            "non_project_activities_fy25": "Non-project strategic or advisory contributions were not included. These can reflect thought leadership or strategic alignment efforts."
        },

        "customer_health": {
            "status": "Customer relationship health status (e.g., strong, stable, at-risk) is missing. This indicates how Omega’s value is perceived and where support is needed.",
            "nps_reference": "No client satisfaction (NPS or CSAT) reference identified. Such indicators strengthen renewal and cross-sell positioning.",
            "red_flags": [{
                "issue": "No risks or relationship threats were captured. Documenting known risks helps Omega proactively mitigate churn or reputational damage.",
                "mitigation": "Mitigation steps were not described. A plan should be outlined for each identified concern to demonstrate proactive account management."
            }]
        },

        "fy26_path_to_plan_summary": {
            "existing_sold_ec": "Existing sold or executed contracts for FY26 are not mentioned. These define the guaranteed revenue baseline.",
            "qualified_opportunities": "Qualified opportunities contributing to FY26 targets were not quantified. Capture all pipeline deals with confidence above 50%.",
            "total": "Total combined revenue value from sold and qualified sources could not be calculated. This figure drives the gap-to-goal assessment.",
            "fy26_goal": "The FY26 goal is not recorded. Define this to establish a clear target benchmark.",
            "gap_to_goal": "The shortfall between goal and identified pipeline is not calculated. Addressing this gap informs white space pursuits.",
            "white_space_with_signal": "White space with buying signals not identified. These are near-term expansion possibilities based on client intent.",
            "white_space_without_signal": "White space without signals not documented. These represent longer-term strategic bets requiring relationship development."
        },

        "customer_business_objectives": {
            "primary_objectives": [
                "Primary customer objectives were not documented. These typically include mission-critical goals such as cost optimization, modernization, or growth enablement."
            ],
            "secondary_objectives": [
                "Secondary objectives not captured. These support the primary goals, often around process improvement, data enablement, or efficiency gains."
            ]
        },

        "account_landscape": {
            "areas_of_focus": [{
                "name": "Functional area of focus (e.g., Revenue Cycle, Cloud Modernization) not listed. This defines Omega’s engagement pillars.",
                "evidence": {
                    "stated_objectives": "Client objectives for this business area were not outlined. Understanding them ensures alignment of Omega’s strategy.",
                    "need_external_help": "No external dependency or support needs identified. Clarify where Omega’s expertise can close internal capability gaps.",
                    "relationships_exist": "No internal or partner relationships identified. Mapping this helps navigate influence networks."
                },
                "impact_fy26": "The expected impact of this area on FY26 goals is not described. Quantify or narrate expected business outcomes."
            }],
            "revenue_projection": [{
                "name": "Opportunity name not included. Each projection should link to tangible deals or initiatives.",
                "category": "Category (Sold, Qualified, WSI, WSN) not defined. Classification shows maturity level of pipeline opportunities.",
                "area_of_focus": "Area of focus not tied to this opportunity. Helps link growth areas with revenue projections.",
                "projected_close": "Projected close date not found. This impacts forecast timing and risk weighting.",
                "est_tcv": "Total contract value not listed. Capture this to estimate revenue potential.",
                "fy26_revenue": "Expected FY26 revenue contribution not provided.",
                "sf_opp_id": "Salesforce ID missing. Required for traceability in CRM systems."
            }]
        },

        "account_relationships": [{
            "customer_name_title": "No customer contact listed. Every key stakeholder should be represented by name and title.",
            "area_of_focus": "Area of client responsibility missing. This supports targeted relationship planning.",
            "current_status": "Current engagement level or relationship quality not described.",
            "development_objective": "Development goal for this contact is not outlined. This clarifies desired evolution in the relationship.",
            "actions": "No actions to advance the relationship recorded. These should define next steps and expected outcomes.",
            "omega_point_person": "Omega relationship owner not identified. Assign internal accountability."
        }],

        "account_strategy": [{
            "action_item": "Strategic initiative not defined. Capture efforts that build long-term positioning or customer goodwill.",
            "owner": "No responsible owner assigned to this strategic action.",
            "due_date": "No expected completion timeframe documented.",
            "completed_date": "Completion status not indicated. Include to track execution accountability."
        }],

        "opportunity_win_plans": [{
            "opportunity_name": "Opportunity name not specified. Identify to establish linkage to pipeline tracking.",
            "sfdc_id": "Salesforce ID not available. Needed for CRM synchronization.",
            "omega_sales_leader": "Sales leader or pursuit manager not mentioned. Assign ownership for governance.",
            "alignment_score": "Alignment score or qualitative rating missing. This helps measure deal health.",
            "alignment_questions": {
                "stated_objectives": "Client’s specific objectives for this opportunity not detailed.",
                "need_external_help": "No reference to where Omega’s support or partnership is required.",
                "relationships_exist": "No relationship context identified for this pursuit."
            },
            "alignment_summary": "No description summarizing how Omega’s offering aligns with client needs was found.",
            "svs8": {
                "single_sales_objective_defined": "No clear sales objective documented.",
                "coach_identified": "No internal champion identified to support deal navigation.",
                "insight_stories_selected": "No relevant customer success stories selected for proof points.",
                "why_change_now": "No urgency factors captured (e.g., cost pressure, regulatory change).",
                "why_omega": "Omega’s differentiation not articulated in the input.",
                "business_case_developed": "Business case development progress not found.",
                "decision_process_understood": "Decision-making path unclear.",
                "red_flags_present": "Risks for this opportunity not highlighted."
            },
            "sso": "Single Sales Objective not described.",
            "coach": {
                "name": "Coach name missing.",
                "title_role": "Coach role or influence level not defined.",
                "influence": "Influence rating not provided.",
                "notes": "Additional context about the coaching relationship missing."
            },
            "insight_stories": [{
                "story": "Insight story not documented. Use stories to demonstrate proven success.",
                "referenceable": "Referenceable status not confirmed.",
                "omega_contact": "Omega contact for this story not provided.",
                "notes": "No notes describing the story’s relevance or context."
            }],
            "why_change_now_detail": "No narrative on the urgency or external triggers prompting this change.",
            "why_omega_detail": "No expanded rationale for Omega’s fit or competitive positioning.",
            "business_case": {
                "solution": "Solution not described. This section should link Omega’s capabilities to the client’s needs.",
                "benefit": "Benefits and ROI not listed. Explain how value will be realized."
            },
            "decision_process": {
                "buyers": {
                    "economic": "Economic buyer not named.",
                    "coach": "Coach-level buyer not identified.",
                    "technical": "Technical decision-maker not specified.",
                    "user": "End-user or operational buyer not referenced."
                },
                "process": "Decision process not detailed. Outline steps to award the opportunity.",
                "criteria": "No selection criteria documented."
            },
            "red_flags": [{
                "risk": "No deal risks outlined.",
                "mitigation": "No mitigation plans provided to address deal blockers."
            }],
            "opportunity_action_plan": [{
                "item": "Action item not described. Document steps needed to close the deal.",
                "owner": "Owner responsible for this task not defined.",
                "due_date": "Due date or milestone missing.",
                "completed_date": "Completion status not mentioned."
            }]
        }]
    }


def fill_missing_fields(data, default):
    """Recursively merges missing data with schema defaults."""
    if isinstance(default, dict):
        if not isinstance(data, dict):
            return default
        for key, val in default.items():
            if key not in data:
                data[key] = val
            elif isinstance(val, dict):
                data[key] = fill_missing_fields(data.get(key, {}), val)
            elif isinstance(val, list):
                if not isinstance(data[key], list) or not data[key]:
                    data[key] = val
                else:
                    data[key] = [fill_missing_fields(i, val[0]) if isinstance(i, dict) else i for i in data[key]]
    elif isinstance(default, list):
        return [fill_missing_fields(item, default[0]) for item in data] if isinstance(data, list) else default
    return data


def humanize_field(value):
    """
    Converts structured data into detailed, narrative sentences suitable for executive summaries.
    Produces natural language with explanatory framing for context.
    """
    if isinstance(value, list):
        output = []
        for item in value:
            if isinstance(item, dict):
                if "risk" in item and "mitigation" in item:
                    output.append(f"A key risk identified is '{item['risk']}', and the proposed mitigation strategy involves {item['mitigation']}. This ensures business continuity and reduces operational exposure.")
                elif "issue" in item and "mitigation" in item:
                    output.append(f"Issue observed: {item['issue']}. Recommended response: {item['mitigation']}. Addressing this will strengthen execution alignment and client confidence.")
                elif "item" in item and "owner" in item:
                    output.append(f"The team plans to execute '{item['item']}' under the ownership of {item['owner']}. The due date is {item.get('due_date', 'unspecified')} and the completion is tracked as {item.get('completed_date', 'pending')}.")
                elif "story" in item:
                    output.append(f"Insight Story: {item['story']}. This case illustrates Omega’s proven value in similar situations. It is referenceable: {item.get('referenceable', 'Unknown')}. Contact person: {item.get('omega_contact', 'Not listed')}. Additional context: {item.get('notes', 'No further notes provided')}.")
                else:
                    joined = ", ".join(f"{k}: {v}" for k, v in item.items())
                    output.append(f"Additional details: {joined}.")
            elif isinstance(item, str):
                output.append(item)
        return " ".join(output)

    elif isinstance(value, dict):
        joined = "; ".join(f"{k.replace('_', ' ').title()}: {v}" for k, v in value.items())
        return f"Details include: {joined}."

    elif isinstance(value, str):
        text = value.strip()
        if "not" in text.lower() or "available" in text.lower():
            return f"{text} This field is crucial for account completeness and should be revisited with additional data or client validation."
        return text
    return str(value)


def humanize_json(data):
    """Applies contextual storytelling across the full JSON structure."""
    if isinstance(data, dict):
        return {k: humanize_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [humanize_json(v) for v in data]
    else:
        return humanize_field(data)


def render_template_to_docx(template_path, json_data, output_path):
    """Renders the DOCX template with full-context, narrative-enhanced data."""
    try:
        schema = get_default_schema()
        merged_data = fill_missing_fields(json_data, schema)
        enriched_data = humanize_json(merged_data)

        tpl = DocxTemplate(template_path)
        tpl.render(enriched_data)
        tpl.save(output_path)

    except Exception as e:
        raise RuntimeError(f"Failed to render template: {e}")
