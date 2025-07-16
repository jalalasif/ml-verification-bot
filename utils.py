# Utility functions for quiz bot
import json
import os
from datetime import datetime, timedelta

ATTEMPT_FILE = "attempts.json"
MAX_ATTEMPTS_PER_DAY = 6

# Ensure file exists
if not os.path.exists(ATTEMPT_FILE):
    with open(ATTEMPT_FILE, "w") as f:
        json.dump({}, f)

def get_role_names(member):
    """Return a list of lowercase role names the user has."""
    return [role.name.lower() for role in member.roles]

def is_user_verified(member, verified_role_name):
    """Check if user has the verified role."""
    return any(role.name.lower() == verified_role_name.lower() for role in member.roles)

def can_attempt_quiz(user_id):
    """Check if a user has remaining attempts today."""
    with open(ATTEMPT_FILE, "r") as f:
        data = json.load(f)

    user_id = str(user_id)
    now = datetime.utcnow()
    today = now.strftime("%Y-%m-%d")

    if user_id not in data:
        return True

    attempts = data[user_id].get(today, 0)
    return attempts < MAX_ATTEMPTS_PER_DAY

def record_attempt(user_id):
    """Record an attempt for the user."""
    with open(ATTEMPT_FILE, "r") as f:
        data = json.load(f)

    user_id = str(user_id)
    now = datetime.utcnow()
    today = now.strftime("%Y-%m-%d")

    if user_id not in data:
        data[user_id] = {}
    if today not in data[user_id]:
        data[user_id][today] = 0

    data[user_id][today] += 1

    with open(ATTEMPT_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_remaining_attempts(user_id):
    """Get number of remaining attempts for today."""
    with open(ATTEMPT_FILE, "r") as f:
        data = json.load(f)

    user_id = str(user_id)
    now = datetime.utcnow()
    today = now.strftime("%Y-%m-%d")

    if user_id not in data or today not in data[user_id]:
        return MAX_ATTEMPTS_PER_DAY

    return MAX_ATTEMPTS_PER_DAY - data[user_id][today]
