from docx_renderer import render_template
from account_plan_parser import parse_input
import uuid
import os

def run_agent(input_file=None, input_text=None):
    # Choose input source
    if input_file:
        input_path = input_file
    else:
        with open("temp_input.txt", "w", encoding="utf-8") as f:
            f.write(input_text)
        input_path = "temp_input.txt"

    # Parse to JSON structure
    parsed_json, account_name = parse_input(input_path)

    # Output file name
    output_filename = f"{account_name or 'Account_Plan_Output'}_Account_Plan_v1_locked.docx"
    output_path = os.path.join("output", output_filename)

    # Render .docx
    render_template(
        template_path="Omega_Account_Plan_Template_v1_locked.docx",
        json_data=parsed_json,
        output_path=output_path
    )

    return output_path
