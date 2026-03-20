import os
import requests
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

# Try getting from Streamlit Secrets first, fallback to os.environ (local)
try:
    SENDGRID_API_KEY = st.secrets["SENDGRID_API_KEY"]
    SENDER_EMAIL = st.secrets["SENDER_EMAIL"]
except Exception:
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")

def send_otp_email(receiver_email, otp):
    if not SENDGRID_API_KEY or not SENDER_EMAIL:
        raise Exception("API Keys are missing from Streamlit Secrets!")
        
    url = "https://api.sendgrid.com/v3/mail/send"

    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "personalizations": [{
            "to": [{"email": receiver_email}]
        }],
        "from": {"email": SENDER_EMAIL},
        "subject": "Your FitPlan AI OTP",
        "content": [{
            "type": "text/plain",
            "value": f"Your OTP is: {otp}"
        }]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 202:
        raise Exception(f"Failed to send email. Status: {response.status_code}, Msg: {response.text}")