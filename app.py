from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests
import json
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

# Get Groq API key
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# In-memory storage (for demo - in production use database)
processed_emails = []

@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "message": "Gmail Support Bot API",
        "dashboard": "http://localhost:5000/dashboard",
        "endpoints": [
            "/webhook/email",
            "/analyze",
            "/emails",
            "/stats",
            "/test-groq"
        ]
    })

@app.route('/dashboard')
def dashboard():
    """Serve the dashboard HTML"""
    return send_from_directory('.', 'dashboard.html')

@app.route('/test-groq', methods=['GET'])
def test_groq():
    """Test Groq API connection"""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.1-8b-instant",  # Using smaller, faster model
        "messages": [
            {"role": "user", "content": "Say 'API Working' in JSON format"}
        ],
        "temperature": 0.1,
        "max_tokens": 50
    }
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        # Return full response for debugging
        return jsonify({
            "status_code": response.status_code,
            "response": response.json() if response.status_code == 200 else response.text
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/webhook/email', methods=['POST'])
def receive_email():
    """Webhook endpoint for n8n to send email data"""
    try:
        email_data = request.json
        
        # Process with AI
        analysis = analyze_email_with_ai(email_data)
        
        # Store the result
        processed_email = {
            "id": len(processed_emails) + 1,
            "timestamp": datetime.now().isoformat(),
            "original": email_data,
            "analysis": analysis
        }
        processed_emails.append(processed_email)
        
        return jsonify({
            "success": True,
            "data": processed_email
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze_email():
    """Direct endpoint to analyze any text with AI"""
    try:
        data = request.json
        text = data.get('text', '')
        subject = data.get('subject', '')
        
        analysis = analyze_email_with_ai({"body": text, "subject": subject})
        
        return jsonify({
            "success": True,
            "analysis": analysis
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/emails', methods=['GET'])
def get_emails():
    """Get all processed emails"""
    return jsonify(processed_emails)

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get statistics about processed emails"""
    stats = {
        "total_emails": len(processed_emails),
        "categories": {},
        "priorities": {},
        "sentiment": {"positive": 0, "neutral": 0, "negative": 0}
    }
    
    for email in processed_emails:
        # Count categories
        cat = email['analysis'].get('category', 'unknown')
        stats['categories'][cat] = stats['categories'].get(cat, 0) + 1
        
        # Count priorities  
        pri = email['analysis'].get('priority', 'medium')
        stats['priorities'][pri] = stats['priorities'].get(pri, 0) + 1
        
        # Count sentiment
        sent = email['analysis'].get('sentiment', 'neutral')
        if sent in stats['sentiment']:
            stats['sentiment'][sent] += 1
    
    return jsonify(stats)

def analyze_email_with_ai(email_data):
    """Use Groq AI to analyze email via direct API call"""
    try:
        email_body = email_data.get('body', email_data.get('text', ''))
        email_subject = email_data.get('subject', '')
        
        # Check if API key exists
        if not GROQ_API_KEY:
            print("WARNING: No GROQ_API_KEY found! Using mock data.")
            return get_mock_analysis(email_subject, email_body)
        
        prompt = f"""Analyze this customer support email and return a JSON response:

Subject: {email_subject}
Body: {email_body}

Return ONLY valid JSON with these fields:
{{
    "category": "bug_report|feature_request|billing|general|technical_support",
    "priority": "critical|high|medium|low",
    "sentiment": "positive|neutral|negative",
    "summary": "one line summary",
    "key_points": ["point1", "point2"],
    "suggested_response": "a helpful response to the customer",
    "needs_human": true/false,
    "detected_issues": ["issue1", "issue2"],
    "customer_mood": "angry|frustrated|neutral|happy|urgent"
}}"""

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama-3.1-8b-instant",  # Using smaller model for faster response
            "messages": [
                {"role": "system", "content": "You are a support email analyzer. Always return valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 500
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )
        
        # Check if request was successful
        if response.status_code != 200:
            print(f"Groq API Error: Status {response.status_code}")
            print(f"Response: {response.text}")
            return get_mock_analysis(email_subject, email_body)
        
        # Parse the response
        response_json = response.json()
        
        # Check if response has expected structure
        if 'choices' not in response_json or len(response_json['choices']) == 0:
            print(f"Unexpected Groq response format: {response_json}")
            return get_mock_analysis(email_subject, email_body)
        
        ai_response = response_json['choices'][0]['message']['content']
        
        # Try to extract JSON from response
        try:
            # Clean the response
            ai_response = ai_response.strip()
            if ai_response.startswith('```json'):
                ai_response = ai_response[7:]
            if ai_response.startswith('```'):
                ai_response = ai_response[3:]
            if ai_response.endswith('```'):
                ai_response = ai_response[:-3]
            
            analysis = json.loads(ai_response)
            
            # Validate that all required fields are present
            required_fields = ['category', 'priority', 'sentiment', 'summary']
            for field in required_fields:
                if field not in analysis:
                    analysis[field] = get_mock_analysis(email_subject, email_body)[field]
            
            return analysis
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return get_mock_analysis(email_subject, email_body)
        
    except requests.exceptions.Timeout:
        print("Groq API timeout")
        return get_mock_analysis(email_subject, email_body)
    except Exception as e:
        print(f"AI Analysis Error: {e}")
        return get_mock_analysis(email_subject, email_body)

def get_mock_analysis(subject, body):
    """Provide mock analysis when AI is not available"""
    # Simple keyword-based analysis for demo
    text = (subject + " " + body).lower()
    
    # Determine category
    if any(word in text for word in ['bug', 'error', 'crash', 'broken', 'fix']):
        category = "bug_report"
    elif any(word in text for word in ['feature', 'add', 'request', 'want', 'need']):
        category = "feature_request"
    elif any(word in text for word in ['payment', 'billing', 'charge', 'subscription', 'refund']):
        category = "billing"
    elif any(word in text for word in ['technical', 'install', 'setup', 'config']):
        category = "technical_support"
    else:
        category = "general"
    
    # Determine priority
    if any(word in text for word in ['urgent', 'asap', 'critical', 'emergency']):
        priority = "high"
    elif any(word in text for word in ['important', 'soon']):
        priority = "medium"
    else:
        priority = "low"
    
    # Determine sentiment
    if any(word in text for word in ['frustrated', 'angry', 'annoyed', 'terrible']):
        sentiment = "negative"
        mood = "frustrated"
    elif any(word in text for word in ['happy', 'great', 'thank', 'appreciate']):
        sentiment = "positive"
        mood = "happy"
    else:
        sentiment = "neutral"
        mood = "neutral"
    
    return {
        "category": category,
        "priority": priority,
        "sentiment": sentiment,
        "summary": f"Customer inquiry about {category.replace('_', ' ')}",
        "key_points": [
            f"Category: {category.replace('_', ' ')}",
            f"Priority: {priority}"
        ],
        "suggested_response": f"Thank you for contacting our support team. We understand your concern regarding {category.replace('_', ' ')}. Our team will review your request and get back to you within 24 hours.",
        "needs_human": priority in ["high", "critical"],
        "detected_issues": [category],
        "customer_mood": mood,
        "ai_status": "mock_mode"  # Indicator that this is mock data
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"🚀 Server starting on http://localhost:{port}")
    print(f"📊 Dashboard: http://localhost:{port}/dashboard")
    print(f"🔌 n8n webhook: http://localhost:{port}/webhook/email")
    print(f"🔑 Groq API Key: {'Found' if GROQ_API_KEY else 'NOT FOUND - Using mock mode'}")
    print(f"🧪 Test Groq API: http://localhost:{port}/test-groq")
    app.run(debug=True, port=port, host='0.0.0.0')