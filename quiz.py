import json
import random

def load_quiz(path="quiz.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def shuffle_options(question):
    # Extract and shuffle the values (answer text + score)
    shuffled_values = list(question["options"].values())
    random.shuffle(shuffled_values)

    # Assign shuffled values back to fixed letter keys
    fixed_letters = ["A", "B", "C", "D"]
    new_options = {letter: shuffled_values[i] for i, letter in enumerate(fixed_letters)}

    return {**question, "options": new_options}