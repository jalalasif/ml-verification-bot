import json
import random

def load_quiz(path="quiz.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def shuffle_options(question):
    options = list(question["options"].items())
    random.shuffle(options)
    shuffled = {k: v for k, v in options}
    return {**question, "options": shuffled}