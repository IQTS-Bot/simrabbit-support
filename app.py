
#!/usr/bin/env python3
"""
SimRabbit WhatsApp AI Assistant (Twilio + Flask)
"""
import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import yaml

try:
    import openai
except ImportError:
    openai = None

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AGENT_NOTE = os.getenv("AGENT_NOTE", "An agent will join shortly.")
if openai and OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY
    USE_AI = True
else:
    USE_AI = False

app = Flask(__name__)

def load_kb():
    path = os.path.join(os.path.dirname(__file__), "kb", "faq.yaml")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}

KB = load_kb()

def rules_based_answer(text: str):
    t = text.lower()
    if "agent" in t or "human" in t or "support" in t:
        return AGENT_NOTE
    if "install" in t:
        return KB.get("install", "Install: Settings > Cellular > Add eSIM > Scan QR.")
    if "device" in t or "compatible" in t:
        return KB.get("devices", "Compatible: iPhone 11+, Samsung/Pixel with eSIM.")
    if "no data" in t or "apn" in t:
        return KB.get("troubleshoot", "Toggle airplane mode, enable Data Roaming, APN: internet.")
    if "price" in t or "plan" in t:
        return KB.get("prices", "Check plans at simrabbit.com/plans")
    return None

AI_SYSTEM = (
    "You are SimRabbit's support bot. "
    "Answer only about eSIM setup, devices, prices, troubleshooting. "
    "For complex issues, say: 'Type agent to talk to a person.'"
)

def ai_answer(user_text: str):
    if not USE_AI:
        return None
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": AI_SYSTEM + "\nKB:\n" + str(KB)},
                {"role": "user", "content": user_text},
            ],
            temperature=0.2,
            max_tokens=300,
        )
        return resp.choices[0].message["content"].strip()
    except Exception:
        return None

@app.post("/whatsapp")
def whatsapp():
    msg = request.values.get("Body", "").strip()
    answer = rules_based_answer(msg) or ai_answer(msg) or (
        "Hi! I'm SimRabbit 🐇\n"
        "Try: install, devices, prices, no data.\n"
        "Type 'agent' for a human."
    )
    tw = MessagingResponse()
    tw.message(answer)
    return str(tw)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
