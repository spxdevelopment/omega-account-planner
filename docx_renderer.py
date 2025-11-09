from docxtpl import DocxTemplate

def render_template_to_docx(template_path, json_data, output_path):
    tpl = DocxTemplate(template_path)

    def inject_missing(data, fallback="Not Available"):
        if isinstance(data, dict):
            return {k: inject_missing(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [inject_missing(i) for i in data]
        elif data is None or data == "":
            return fallback
        return data

    safe_data = inject_missing(json_data)

    # Add placeholder for ALL required keys to avoid template crash
    required_keys = [
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

    for key in required_keys:
        if key not in safe_data:
            safe_data[key] = "Not Available"

    tpl.render(safe_data)
    tpl.save(output_path)
