from flask import Flask, request, render_template, send_file
from openai_parser import parse_input_to_schema
from docx_renderer import render_template_to_docx
import os
import tempfile

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files.get("input_file")
        if not uploaded_file:
            return render_template("index.html", error="Please upload a file.")

        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, uploaded_file.filename)
            uploaded_file.save(input_path)

            # Call OpenAI + schema logic
            parsed_json, account_name = parse_input_to_schema(input_path)
            account_name = account_name or "Account_Plan_Output"
            output_filename = f"{account_name}_Account_Plan_v1_locked.docx"
            output_path = os.path.join(tmpdir, output_filename)

            render_template_to_docx(
                template_path="Omega_Account_Plan_Template_v1_locked.docx",
                json_data=parsed_json,
                output_path=output_path
            )

            return send_file(output_path, as_attachment=True, download_name=output_filename)

    return render_template("index.html")
