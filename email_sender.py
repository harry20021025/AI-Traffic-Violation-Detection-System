import smtplib
from email.message import EmailMessage
from gemini_ai import generate_penalty_email
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


def send_email(to_email, owner_name, vehicle_no, fine, violation_type):
    try:
        print("Generating email using Gemini...")

        email_body = generate_penalty_email(
            owner_name,
            vehicle_no,
            violation_type,
            fine
        )

        print("Gemini email generated")

    except Exception as e:
        print("Gemini unavailable, using fallback:", e)

        email_body = f"""
Dear {owner_name},

This is an official notification regarding a traffic violation recorded for your vehicle.

Vehicle Number: {vehicle_no}
Violation Type: {violation_type}
Fine Amount: ₹{fine}

You are requested to pay the fine within 7 days from the date of this notice.

Failure to comply may result in further legal action.

Regards,
Traffic Police Department
""".strip()

    msg = EmailMessage()
    msg.set_content(email_body)

    msg["Subject"] = "Official Traffic Violation Notice"
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

    print("Email sent successfully")
