from docxtpl import DocxTemplate
import os

REQUIRED_FIELDS = [
    "account_overview",
    "omega_history",
    "customer_health",
    "fy26_path_to_plan_summary",
    "customer_business_objectives",
    "account_landscape",
    "account_relationships",
    "account_strategy",
    "opportunity_win_plans",
    "omega_team"
]

def render_template_to_docx(template_path, json_data, output_path):
    tpl = DocxTemplate(template_path)

    def fill_missing(data, fallback="Not Available"):
        if isinstance(data, dict):
            return {k: fill_missing(v, fallback) for k, v in data.items()}
        elif isinstance(data, list):
            return [fill_missing(i, fallback) for i in data]
        elif data is None or data == "":
            return fallback
        return data

    safe_data = fill_missing(json_data)

    # Top-level schema patch
    for key in REQUIRED_FIELDS:
        if key not in safe_data:
            safe_data[key] = "Not Available"

    tpl.render(safe_data)
    tpl.save(output_path)
