import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

print("=" * 50)
print("GROQ API KEY CHECKER")
print("=" * 50)

if not GROQ_API_KEY:
    print("❌ No GROQ_API_KEY found in .env file!")
    print("\nPlease add your Groq API key to .env file:")
    print("GROQ_API_KEY=your_actual_key_here")
else:
    print(f"✅ API Key found: {GROQ_API_KEY[:10]}...")
    print("\nTesting API connection...")
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": "Say hello in 3 words"}
        ],
        "temperature": 0.1,
        "max_tokens": 10
    }
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ API Connection successful!")
            result = response.json()
            if 'choices' in result:
                print(f"Response: {result['choices'][0]['message']['content']}")
        else:
            print(f"❌ API Error: Status {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 401:
                print("\n⚠️  Invalid API key! Please check your Groq API key.")
            elif response.status_code == 429:
                print("\n⚠️  Rate limit exceeded. Wait a bit and try again.")
                
    except Exception as e:
        print(f"❌ Connection error: {e}")

print("\n" + "=" * 50)
print("Next steps:")
print("1. If API key is invalid, get a new one from: https://console.groq.com/keys")
print("2. Update your .env file with: GROQ_API_KEY=your_actual_key")
print("3. Run 'python app.py' to start the server")
print("=" * 50)