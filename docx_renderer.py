from docxtpl import DocxTemplate

# Top-level fields that must always exist in the schema
REQUIRED_FIELDS = [
    "account_overview",
    "omega_history",
    "customer_health",
    "fy26_path_to_plan_summary",
    "customer_business_objectives",
    "account_landscape",
    "account_relationships",
    "account_strategy",
    "opportunity_win_plans"
]

# Default nested structures that must also exist
REQUIRED_STRUCTURE = {
    "account_overview": {
        "omega_team": [{
            "name": "Not Available",
            "role_title": "Not Available",
            "location": "Not Available"
        }]
    },
    "opportunity_win_plans": [{
        "opportunity": "Not Available",
        "description": "Not Available"
    }],
    "account_relationships": {
        "executive_sponsors": ["Not Available"],
        "decision_makers": ["Not Available"],
        "influencers": ["Not Available"]
    }
}

def fill_missing_fields(data, structure):
    """
    Recursively inject required nested fields.
    """
    for key, val in structure.items():
        if key not in data:
            data[key] = val
        elif isinstance(val, dict) and isinstance(data[key], dict):
            fill_missing_fields(data[key], val)
        elif isinstance(val, list) and not isinstance(data[key], list):
            data[key] = val
    return data

def fill_not_available(obj, fallback="Not Available"):
    """
    Recursively replace None, empty strings, or blanks with fallback.
    """
    if isinstance(obj, dict):
        return {k: fill_not_available(v, fallback) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [fill_not_available(i, fallback) for i in obj]
    elif obj in ("", None):
        return fallback
    return obj

def render_template_to_docx(template_path, json_data, output_path):
    tpl = DocxTemplate(template_path)

    # Step 1: Ensure all top-level fields are present
    for field in REQUIRED_FIELDS:
        if field not in json_data:
            json_data[field] = {}

    # Step 2: Fill required nested structures
    safe_data = fill_missing_fields(json_data.copy(), REQUIRED_STRUCTURE)

    # Step 3: Replace all blank/missing values
    safe_data = fill_not_available(safe_data)

    # Step 4: Inject into the template
    tpl.render(safe_data)
    tpl.save(output_path)
