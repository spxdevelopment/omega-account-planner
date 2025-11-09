from docxtpl import DocxTemplate

def render_template_to_docx(template_path, json_data, output_path):
    tpl = DocxTemplate(template_path)

    def fallback(obj):
        if isinstance(obj, dict):
            return {k: fallback(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [fallback(i) for i in obj]
        elif obj in ("", None):
            return "Not Available"
        return obj

    tpl.render(fallback(json_data))
    tpl.save(output_path)
