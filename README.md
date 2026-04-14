# Customer Service Call Flow Application

A minimal Python application demonstrating best practices for customer service call flows using FastAPI and Vonage APIs.

## Features

### Best Practices Implemented

- **Effective IVR System**: Self-service menu options with escape routes for complex calls
- **Voice Quality & NLP**: Text-to-speech using Vonage Voice API with natural prompts
- **CRM Integration**: Customer lookup and personalized greetings based on phone number
- **Skills-Based Routing**: DTMF input routes calls to appropriate departments
- **Error Handling**: Graceful fallbacks and callback options when agents are unavailable
- **Interaction Logging**: All calls and messages recorded in SQLite database
- **Agent Dashboard Ready**: Endpoints for agents to access customer history

## Prerequisites

- Python 3.9+
- Vonage API credentials (API key, secret, app ID, private key)
- A Vonage virtual number configured for voice

## Installation

1. **Clone and setup**:
```bash
cd customer\_service\_app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
