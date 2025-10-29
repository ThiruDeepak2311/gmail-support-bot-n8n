import requests
import json

# Test the API
BASE_URL = "http://localhost:5000"

def test_groq_connection():
    """Test if Groq API is working"""
    print("Testing Groq API connection...")
    response = requests.get(f"{BASE_URL}/test-groq")
    result = response.json()
    
    if result.get('status_code') == 200:
        print("✅ Groq API is working!")
    else:
        print("❌ Groq API issue detected:")
        print(json.dumps(result, indent=2))
    return result.get('status_code') == 200

def test_analyze():
    """Test the analyze endpoint"""
    
    test_emails = [
        {
            "text": "Hi, I'm having trouble logging into my account. It says invalid password but I'm sure it's correct. This is urgent as I need to access my files for a meeting in 2 hours. Please help!",
            "subject": "Urgent: Login Issue"
        },
        {
            "text": "I love your product! It has made my workflow so much easier. Just wanted to say thanks!",
            "subject": "Thank you!"
        },
        {
            "text": "The app keeps crashing whenever I try to upload files. This is a critical bug that needs immediate attention.",
            "subject": "Critical Bug Report"
        }
    ]
    
    for i, test_email in enumerate(test_emails, 1):
        print(f"\nTest Email #{i}: {test_email['subject']}")
        print("-" * 40)
        response = requests.post(f"{BASE_URL}/analyze", json=test_email)
        result = response.json()
        
        if 'analysis' in result:
            analysis = result['analysis']
            print(f"Category: {analysis.get('category', 'N/A')}")
            print(f"Priority: {analysis.get('priority', 'N/A')}")
            print(f"Sentiment: {analysis.get('sentiment', 'N/A')}")
            print(f"Summary: {analysis.get('summary', 'N/A')}")
            print(f"AI Mode: {'Real AI' if not analysis.get('ai_status') else 'Mock Mode'}")
        else:
            print("Error:", result)

def test_webhook():
    """Test the webhook endpoint"""
    
    test_email_data = {
        "subject": "Payment not going through",
        "body": "I've been trying to upgrade my subscription but my credit card keeps getting declined. I've checked with my bank and everything is fine on their end. This is really frustrating!",
        "from": "customer@example.com",
        "date": "2024-01-10"
    }
    
    response = requests.post(f"{BASE_URL}/webhook/email", json=test_email_data)
    print("\nWebhook Test:")
    print("-" * 40)
    result = response.json()
    
    if result.get('success'):
        print("✅ Webhook successful!")
        print(f"Email ID: {result['data']['id']}")
        print(f"Category: {result['data']['analysis']['category']}")
        print(f"Priority: {result['data']['analysis']['priority']}")
    else:
        print("❌ Webhook failed:", result)

def test_stats():
    """Test the stats endpoint"""
    response = requests.get(f"{BASE_URL}/stats")
    print("\nStatistics:")
    print("-" * 40)
    stats = response.json()
    print(f"Total emails: {stats['total_emails']}")
    print(f"Categories: {stats['categories']}")
    print(f"Priorities: {stats['priorities']}")
    print(f"Sentiment: {stats['sentiment']}")

def test_get_emails():
    """Test getting all emails"""
    response = requests.get(f"{BASE_URL}/emails")
    emails = response.json()
    print(f"\n📧 Total emails in system: {len(emails)}")
    
if __name__ == "__main__":
    print("=" * 50)
    print("EMAIL SUPPORT BOT - API TESTER")
    print("=" * 50)
    
    # First check if server is running
    try:
        response = requests.get(BASE_URL)
        print("✅ Server is running!")
    except:
        print("❌ Server is not running. Please run 'python app.py' first!")
        exit(1)
    
    # Test Groq connection
    groq_working = test_groq_connection()
    
    if not groq_working:
        print("\n⚠️  Using MOCK mode for analysis (no AI)")
        print("To use real AI, please:")
        print("1. Get API key from https://console.groq.com/keys")
        print("2. Add to .env file: GROQ_API_KEY=your_key")
    
    # Test analyze endpoint with multiple examples
    test_analyze()
    
    # Test webhook endpoint
    test_webhook()
    
    # Get stats
    test_stats()
    
    # Get all emails
    test_get_emails()
    
    print("\n" + "=" * 50)
    print("✅ All tests complete!")
    print("=" * 50)