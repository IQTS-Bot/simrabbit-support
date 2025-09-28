
#!/usr/bin/env python3
"""
SimRabbit Voice IVR (Twilio + Flask)
"""
import os
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
from dotenv import load_dotenv

load_dotenv()
AGENT_NUMBER = os.getenv("AGENT_NUMBER", "+12065551234")
app = Flask(__name__)

@app.post("/voice")
def voice():
    resp = VoiceResponse()
    gather = Gather(num_digits=1, action="/handle-key", method="POST")
    gather.say("Welcome to SimRabbit support. "
               "Press 1 for installation guide. "
               "Press 2 for device compatibility. "
               "Press 3 for troubleshooting. "
               "Press 0 to speak with an agent.")
    resp.append(gather)
    resp.redirect("/voice")
    return str(resp)

@app.post("/handle-key")
def handle_key():
    digit_pressed = request.values.get("Digits", "")
    resp = VoiceResponse()
    if digit_pressed == "1":
        resp.say("To install your eSIM, go to settings, cellular, add cellular plan, scan the QR code provided.")
    elif digit_pressed == "2":
        resp.say("SimRabbit works on iPhone eleven and newer, recent Samsung Galaxy, and Google Pixel models.")
    elif digit_pressed == "3":
        resp.say("If your data is not working, toggle airplane mode for ten seconds, enable data roaming, and set the APN to internet.")
    elif digit_pressed == "0":
        resp.say("Please hold while we connect you to an agent.")
        resp.dial(AGENT_NUMBER)
    else:
        resp.say("Sorry, I did not understand your choice.")
        resp.redirect("/voice")
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
