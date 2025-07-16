# quiz.py

import json
import random

# Loads quiz questions from a JSON file.
def load_quiz(path="quiz.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Randomizes the answer choices for each question while preserving their scores.
def shuffle_options(question):
    original_options = question["options"]
    option_values = list(original_options.values())
    random.shuffle(option_values)  # Shuffle the options and their associated scores

    fixed_letters = ["A", "B", "C", "D"]
    new_options = {
        letter: option_values[i] for i, letter in enumerate(fixed_letters)
    }

    return {
        "question": question["question"],
        "options": new_options
    }

# Public function to get all quiz questions with randomized options
def get_questions():
    raw = load_quiz()
    return [shuffle_options(q) for q in raw]
