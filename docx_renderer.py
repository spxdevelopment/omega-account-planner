from docxtpl import DocxTemplate

def render_template_to_docx(template_path, json_data, output_path):
    tpl = DocxTemplate(template_path)

    def inject_missing_keys(data, fallback="Not Available"):
        if isinstance(data, dict):
            return {k: inject_missing_keys(v, fallback) for k, v in data.items()}
        elif isinstance(data, list):
            return [inject_missing_keys(item, fallback) for item in data]
        elif data in (None, ""):
            return fallback
        return data

    safe_data = inject_missing_keys(json_data)

    # Add any known missing sections
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
