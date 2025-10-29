# Create test_final.py
import requests
import json

webhook_url = "http://localhost:5678/webhook/gmail-support"

test_emails = [
    {
        "subject": "URGENT: System is completely down!",
        "body": "Nothing is working! Our entire system crashed and we're losing money every minute!",
        "from": "ceo@company.com"
    },
    {
        "subject": "Question about features",
        "body": "Hi, I was wondering what features are included in the pro plan?",
        "from": "prospect@example.com"
    }
]

for email in test_emails:
    response = requests.post(webhook_url, json=email)
    print(f"Sent: {email['subject']}")
    print(f"Response: {response.status_code}")
    print(f"Body: {response.json()}\n")