from google import genai
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-flash-latest"


def generate_penalty_email(owner_name, vehicle_no, violation_type, fine):

    today = datetime.now().strftime("%d %B %Y")

    prompt = f"""
You are an official traffic police email notification system.

Write a professional, polite, clean and well-structured email.

STRICT RULES:
- Use proper spacing and line breaks
- Do NOT use placeholders like [Insert Date] or [Insert Location]
- Mention today's date as: {today}
- Keep official tone
- Generate a slightly different email each time
- Do NOT use markdown or bullet points
- Everything should be easy to read

Include these sections in order:

Subject line

Greeting with owner name

Short paragraph about violation detected

Violation details on separate lines:
Vehicle Number
Violation Type
Fine Amount

Payment instruction paragraph (7 days deadline)

Formal closing

Details:
Owner Name: {owner_name}
Vehicle Number: {vehicle_no}
Violation Type: {violation_type}
Fine Amount: ₹{fine}

Write ONLY the email content.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text.strip()
