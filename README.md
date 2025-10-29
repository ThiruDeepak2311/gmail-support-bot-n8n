# Gmail Support Bot - AI-Powered Email Automation System

An intelligent email support automation system built with n8n, Python Flask, and Groq AI that automatically categorizes, prioritizes, and responds to customer support emails.

## 🎯 Project Overview

This project demonstrates an automated support email processing system that:
- **Receives** emails via webhook/API endpoints
- **Analyzes** content using Groq AI (Llama 3.1)
- **Categorizes** emails (bug reports, billing, technical support, etc.)
- **Prioritizes** based on urgency (critical, high, medium, low)
- **Routes** high-priority issues for immediate attention
- **Suggests** AI-generated responses
- **Visualizes** data through a real-time dashboard

## 🏗️ Architecture

```
Email Input → n8n Webhook → Flask API → Groq AI Analysis → Smart Routing → Dashboard
                                                          ↓
                                                   High Priority → Alert
                                                   Low Priority → Log
```

## 🚀 Features

- **AI-Powered Analysis**: Uses Groq's Llama 3.1 for intelligent email understanding
- **Smart Categorization**: Automatically detects email type (billing, technical, feature request, etc.)
- **Priority Detection**: Identifies urgent issues requiring immediate attention
- **Sentiment Analysis**: Understands customer emotion (positive, neutral, negative)
- **Suggested Responses**: AI generates appropriate reply templates
- **Real-time Dashboard**: Visual analytics with Chart.js
- **n8n Automation**: Complete workflow automation with conditional routing
- **RESTful API**: Clean API architecture for easy integration

## 📁 Project Structure

```
gmail-support-bot/
├── app.py                 # Flask API server with AI integration
├── dashboard.html         # Real-time analytics dashboard
├── test_api.py           # API testing suite
├── send_test.py          # Webhook testing script
├── check_groq.py         # Groq API connection tester
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not in repo)
├── n8n_workflow.json     # n8n workflow export
└── README.md            # This file
```

## 🛠️ Tech Stack

- **Backend**: Python Flask
- **AI/ML**: Groq API (Llama 3.1-8B)
- **Automation**: n8n workflow automation
- **Frontend**: HTML5, JavaScript, Chart.js
- **APIs**: RESTful architecture with webhooks

## 📋 Prerequisites

- Python 3.8+
- Node.js 14+ (for n8n)
- Groq API key (free at [console.groq.com](https://console.groq.com))

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/gmail-support-bot.git
cd gmail-support-bot
```

### 2. Set up Python environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure environment variables
Create a `.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
PORT=5000
```

### 4. Install and start n8n
```bash
# Install n8n globally
npm install -g n8n

# Start n8n
n8n start
```

## 🚀 Running the Application

### 1. Start the Flask API server
```bash
python app.py
```
Server runs at: `http://localhost:5000`

### 2. Access the dashboard
Open browser: `http://localhost:5000/dashboard`

### 3. Open n8n
Navigate to: `http://localhost:5678`

### 4. Import the workflow
- In n8n, click "Import from File"
- Select `n8n_workflow.json`
- Activate the workflow

## 🧪 Testing

### Test the API endpoints
```bash
python test_api.py
```

### Send test emails to the system
```bash
python send_test.py
```

### Check Groq API connection
```bash
python check_groq.py
```

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API status and info |
| `/analyze` | POST | Analyze email text with AI |
| `/webhook/email` | POST | Receive and process emails |
| `/emails` | GET | Get all processed emails |
| `/stats` | GET | Get analytics statistics |
| `/dashboard` | GET | View analytics dashboard |

## 🔄 n8n Workflow

The n8n workflow consists of:

1. **Webhook Trigger**: Receives email data
2. **HTTP Request**: Sends to Flask API for AI analysis
3. **IF Node**: Routes based on priority (critical/high vs medium/low)
4. **Code Nodes**: Process and format responses
5. **Webhook Response**: Returns confirmation

### Workflow Activation
1. Open n8n at `http://localhost:5678`
2. Import the workflow from `n8n_workflow.json`
3. Toggle to "Active" in top-right
4. Webhook URL: `http://localhost:5678/webhook/gmail-support`

## 📈 Dashboard Features

- **Real-time Updates**: Auto-refreshes every 5 seconds
- **Email List**: Shows recent emails with AI analysis
- **Priority Metrics**: Tracks critical vs normal issues
- **Category Distribution**: Pie chart of email types
- **Sentiment Analysis**: Bar chart of customer emotions
- **Test Panel**: Send test emails directly from dashboard

## 🎯 Use Cases

- Customer support automation
- Ticket prioritization systems
- Email triage for support teams
- Automated response generation
- Support metrics and analytics

## 🔮 Future Enhancements

- [ ] Real Gmail integration via OAuth2
- [ ] Slack/Discord notifications for high priority
- [ ] Database persistence (PostgreSQL/MongoDB)
- [ ] Multi-language support
- [ ] Custom training for domain-specific responses
- [ ] Export reports to PDF/CSV
- [ ] Team collaboration features

## 📝 Sample Email Analysis

**Input Email:**
```
Subject: Payment not working - URGENT
Body: I tried to upgrade my subscription but my credit card keeps getting declined. This is really frustrating!
```

**AI Analysis Output:**
```json
{
  "category": "billing",
  "priority": "high",
  "sentiment": "negative",
  "summary": "Customer experiencing payment processing issues",
  "suggested_response": "I apologize for the payment issues you're experiencing. Let me help resolve this immediately...",
  "customer_mood": "frustrated"
}
```

## 🤝 Contributing

Feel free to fork this project and submit pull requests with improvements!

## 📄 License

MIT License - feel free to use this in your own projects!


## 🙏 Acknowledgments

- Groq for providing free AI API access
- n8n community for workflow automation
- Flask and Python community

---

**Built for demonstration purposes showcasing n8n automation, AI integration, and full-stack development skills.**
