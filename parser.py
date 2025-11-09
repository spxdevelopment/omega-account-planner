import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_brief_and_extract_schema(text):
    system_prompt = "Extract data from the following input and return a JSON object matching Omega_Account_Plan_Schema.json ..."
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        temperature=0.2
    )
    return json.loads(response['choices'][0]['message']['content'])
