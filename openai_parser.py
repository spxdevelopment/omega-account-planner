import openai
import os
import fitz  # PyMuPDF

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_file(file_path):
    if file_path.endswith(".pdf"):
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    elif file_path.endswith(".docx"):
        import docx
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

def parse_input_to_schema(file_path):
    raw_text = extract_text_from_file(file_path)

    # Read your instruction prompt from file
    with open("instructions.txt", "r") as f:
        system_prompt = f.read()

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": raw_text}
        ],
        temperature=0.2
    )

    result_json = response['choices'][0]['message']['content']
    import json
    parsed = json.loads(result_json)
    name = parsed.get("account_overview", {}).get("account_name", None)
    return parsed, name

