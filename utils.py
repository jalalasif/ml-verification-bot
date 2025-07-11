import json
import os
from datetime import datetime, timedelta

ATTEMPT_FILE = "attempts.json"

def load_welcome_messages(path="messages.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)["welcome_messages"]

def can_attempt(user_id):
    if not os.path.exists(ATTEMPT_FILE):
        return True

    with open(ATTEMPT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    now = datetime.utcnow()
    attempts = data.get(str(user_id), [])
    recent = [datetime.fromisoformat(ts) for ts in attempts if now - datetime.fromisoformat(ts) < timedelta(hours=24)]

    return len(recent) < 4

def record_attempt(user_id):
    data = {}
    if os.path.exists(ATTEMPT_FILE):
        with open(ATTEMPT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

    now = datetime.utcnow().isoformat()
    data.setdefault(str(user_id), []).append(now)

    with open(ATTEMPT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)