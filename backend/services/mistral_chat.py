import os
from dotenv import load_dotenv
# from mistralai import Mistral
from mistralai.client import Mistral

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def generate_mistral_response(question, analysis_report):
    prompt = f"""
You are DermaSense AI, an educational skin information assistant.

Important safety rules:
- Do not provide medical diagnosis.
- Do not prescribe medicine.
- Do not claim certainty.
- Always remind the user to consult a dermatologist.
- Keep the answer clear, supportive, and educational.

Analysis report:
Prediction: {analysis_report.get("prediction")}
Confidence: {analysis_report.get("confidence")}
Description: {analysis_report.get("description")}
Causes: {analysis_report.get("causes")}
Management: {analysis_report.get("management")}
Severity: {analysis_report.get("severity")}

User question:
{question}
"""

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=300
    )

    return response.choices[0].message.content

def generate_mistral_report(prediction, confidence, raw_results=None):
    raw_results_text = raw_results if raw_results else "No additional class scores available."

    prompt = f"""
You are DermaSense AI, an educational skin information assistant.

Task:
Generate a structured Natural Language Generation report based on the vision model output.

Vision model result:
Predicted condition: {prediction}
Confidence score: {confidence}%
All class scores: {raw_results_text}

Safety rules:
- Do not diagnose the user.
- Do not prescribe medicine.
- Do not mention cancer or emergency disease.
- Use careful wording such as "may suggest" or "could be consistent with".
- Always include an educational disclaimer.
- Keep the report concise and suitable for a university AI demo.

Return the report in this exact format:

Description:
Causes:
Management:
Severity:
Disclaimer:
"""

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=350
    )

    return response.choices[0].message.content