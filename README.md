
# SimRabbit Support (WhatsApp + Voice)

This repo contains two Flask apps:

- `app.py` → WhatsApp AI Assistant
- `ivr_app.py` → Voice IVR

## WhatsApp Bot
Deploy `app.py` with:
```
gunicorn app:app
```
Webhook for Twilio (Messaging → WhatsApp Sender):
```
https://yourapp.onrender.com/whatsapp
```

## Voice IVR
Deploy `ivr_app.py` with:
```
gunicorn ivr_app:app
```
Webhook for Twilio (Phone Numbers → Voice → A Call Comes In):
```
https://yourivr.onrender.com/voice
```

## Environment Variables
- `OPENAI_API_KEY` → optional, for AI answers
- `AGENT_NOTE` → text shown when escalating to human
- `AGENT_NUMBER` → phone number where calls are forwarded

## Knowledge Base
Edit `kb/faq.yaml` to change quick answers.
