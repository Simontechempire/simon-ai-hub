import random


def roll_dice():
    return random.randint(1, 6)


def throw_dart():
    return random.randint(1, 60)


def generate_number():
    return random.randint(1, 10)


QUIZZES = [
    {
        "question": "🌍 What is the capital of Nigeria?",
        "answer": "abuja",
    },
    {
        "question": "🪐 Which planet is known as the Red Planet?",
        "answer": "mars",
    },
    {
        "question": "🐘 What is the largest land animal?",
        "answer": "elephant",
    },
]


def get_quiz():
    return random.choice(QUIZZES)
