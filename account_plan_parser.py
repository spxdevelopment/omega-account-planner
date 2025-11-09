import fitz  # PyMuPDF
import docx
import os
import json

def extract_text(input_path):
    ext = os.path.splitext(input_path)[-1].lower()
    if ext == ".pdf":
        doc = fitz.open(input_path)
        return " ".join([page.get_text() for page in doc])
    elif ext == ".docx":
        doc = docx.Document(input_path)
        return "\n".join([p.text for p in doc.paragraphs])
    elif ext == ".txt":
        with open(input_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return ""

def parse_input(input_path):
    raw_text = extract_text(input_path)

    # 💡 Example dummy parser (replace with your logic/rules/LLM)
    parsed = {
        "account_overview": {
            "account_name": "St. Veronica Health System",
            "current_segment": "Enterprise",
            "two_year_potential_segment": "Strategic",
            "account_owner": "Jane Smith",
            "data_created": "2025-11-09",
            "date_last_updated": "2025-11-09",
            "omega_team": []
        },
        "omega_history": {
            "revenue_fy24": "$2,500,000",
            "projects_fy24": "Patient Flow Optimization",
            "business_impact_fy24": "17% decrease in ER wait times",
            "revenue_fy25": "$3,100,000",
            "projects_fy25": "Clinical Staff Scheduling",
            "business_impact_fy25": "22% improved efficiency",
            "non_project_activities_fy25": "Presented at HIMSS"
        },
        "customer_health": {
            "status": "Healthy",
            "nps_reference": "72",
            "red_flags": "None"
        },
        "fy26_path_to_plan_summary": {
            "existing_sold_ec": "$1,200,000",
            "qualified_opportunities": "$2,000,000",
            "total": "$3,200,000",
            "fy26_goal": "$4,000,000",
            "gap_to_goal": "$800,000",
            "white_space_with_signal": "AI patient monitoring",
            "white_space_without_signal": "Telepharmacy"
        },
        "customer_business_objectives": {
            "summary": "Improve patient throughput and staffing efficiency"
        },
        "account_landscape": {
            "areas_of_focus": []
        },
        "account_relationships": {},
        "account_strategy": {},
        "opportunity_win_plans": []
    }

    return parsed, "St_Veronica_Health_System"
