from docxtpl import DocxTemplate

def render_template(template_path, json_data, output_path):
    tpl = DocxTemplate(template_path)

    def fill_blanks(obj):
        if isinstance(obj, dict):
            return {k: fill_blanks(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [fill_blanks(i) for i in obj]
        elif obj in ("", None):
            return "Not Available"
        return obj

    tpl.render(fill_blanks(json_data))
    tpl.save(output_path)
