from flask import Flask, request, send_file, jsonify
from account_plan_parser import parse_input
from docx_renderer import render_template
import os
import tempfile

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "Omega Planner is online"}), 200

@app.route("/generate", methods=["POST"])
def generate_docx():
    try:
        input_file = request.files.get("input_file")
        input_text = request.form.get("input_text")

        if not input_file and not input_text:
            return jsonify({"error": "Provide input_file or input_text"}), 400

        with tempfile.TemporaryDirectory() as tmpdir:
            if input_file:
                input_path = os.path.join(tmpdir, input_file.filename)
                input_file.save(input_path)
            else:
                input_path = os.path.join(tmpdir, "input.txt")
                with open(input_path, "w", encoding="utf-8") as f:
                    f.write(input_text)

            parsed_data, account_name = parse_input(input_path)
            account_name = account_name or "Account_Plan_Output"
            output_filename = f"{account_name}_Account_Plan_v1_locked.docx"
            output_path = os.path.join(tmpdir, output_filename)

            render_template(
                template_path="Omega_Account_Plan_Template_v1_locked.docx",
                json_data=parsed_data,
                output_path=output_path
            )

            return send_file(output_path, as_attachment=True, download_name=output_filename)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ⬇️ THIS IS WHAT YOU NEED TO ADD:
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
