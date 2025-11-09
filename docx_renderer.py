from docxtpl import DocxTemplate, template
import re

def extract_placeholders(template_path):
    """
    Scan the .docx template and extract all Jinja placeholders
    like {{ field }}, {{ account_overview.name }}, etc.
    """
    tpl = DocxTemplate(template_path)
    placeholder_pattern = re.compile(r"\{\{\s*(.*?)\s*\}\}")
    found = set()

    for block, _ in tpl.get_undeclared_template_variables():
        found.add(block)

    # The older docxtpl versions may not expose get_undeclared_template_variables properly;
    # fall back to regex if needed.
    try:
        doc_xml = "\n".join([p.text for p in tpl.doc.paragraphs if p.text])
        for m in placeholder_pattern.findall(doc_xml):
            found.add(m.split("|")[0].strip())  # ignore Jinja filters
    except Exception:
        pass

    return list(found)

def safe_insert(path, target_dict, value="Not Available"):
    """
    Create nested dict structure for a dotted path like 'account_overview.omega_team[0].name'
    """
    import re
    parts = re.split(r"\.|\[|\]", path)
    parts = [p for p in parts if p]
    d = target_dict
    for i, part in enumerate(parts):
        last = i == len(parts) - 1
        if last:
            d[part] = value
        else:
            if part not in d or not isinstance(d[part], dict):
                d[part] = {}
            d = d[part]
    return target_dict

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

    # 1. Extract all placeholders from template
    placeholders = extract_placeholders(template_path)

    # 2. Build safe data dict covering all placeholders
    safe_data = json_data.copy()
    for ph in placeholders:
        try:
            safe_insert(ph, safe_data)
        except Exception:
            # silently skip any invalid Jinja expression
            continue

    # 3. Fill blanks
    safe_data = fill_not_available(safe_data)

    # 4. Render and save
    tpl.render(safe_data)
    tpl.save(output_path)
