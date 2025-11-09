import os
import tempfile
from flask import Flask, request, render_template, send_file
from openai_parser import parse_input_to_schema
from docx_renderer import render_template_to_docx

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Retrieve uploaded file and/or text input
            uploaded_file = request.files.get("input_file")
            text_input = request.form.get("text_input")

            if not uploaded_file and (not text_input or text_input.strip() == ""):
                return render_template("index.html", error="Please provide either a file or brief text.")

            with tempfile.TemporaryDirectory() as tmpdir:
                if uploaded_file and uploaded_file.filename != "":
                    input_path = os.path.join(tmpdir, uploaded_file.filename)
                    uploaded_file.save(input_path)
                else:
                    input_path = os.path.join(tmpdir, "text_input.txt")
                    with open(input_path, "w", encoding="utf-8") as f:
                        f.write(text_input.strip())

                # Parse input to Omega schema
                parsed_json, account_name = parse_input_to_schema(input_path)

                # Ensure fallback if no account name found
                account_name = account_name or "Account_Plan_Output"
                output_filename = f"{account_name}_Account_Plan_v1_locked.docx"
                output_path = os.path.join(tmpdir, output_filename)

                # Render template
                render_template_to_docx(
                    template_path="Omega_Account_Plan_Template_v1_locked.docx",
                    json_data=parsed_json,
                    output_path=output_path
                )

                return send_file(output_path, as_attachment=True, download_name=output_filename)

        except Exception as e:
            return f"""
                <h2 style='color:red;'>Something went wrong.</h2>
                <pre>{str(e)}</pre>
                <br><a href='/'>Go Back</a>
            """

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
