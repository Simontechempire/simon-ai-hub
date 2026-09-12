import random

from telegram import Update
from telegram.ext import ContextTypes


async def games_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 SIMON AI HUB — GAMES\n\n"
        "🎲 /dice - Roll the dice\n"
        "🎯 /dart - Throw a dart\n"
        "🧠 /quiz - Play a quiz\n"
        "🔢 /guess - Guess the number\n"
    )


async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = random.randint(1, 6)

    await update.message.reply_text(
        f"🎲 You rolled: {number}"
    )


async def dart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    score = random.randint(1, 60)

    await update.message.reply_text(
        f"🎯 Your dart score: {score}"
    )


async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = random.randint(1, 10)

    context.user_data["guess_number"] = number

    await update.message.reply_text(
        "🔢 I'm thinking of a number from 1 to 10.\n\n"
        "Send your guess!"
    )


async def guess_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "guess_number" not in context.user_data:
        return

    try:
        user_guess = int(update.message.text)
    except ValueError:
        return

    number = context.user_data["guess_number"]

    if user_guess == number:
        await update.message.reply_text(
            "🎉 CORRECT! You won! 🔥"
        )
        del context.user_data["guess_number"]

    elif user_guess < number:
        await update.message.reply_text(
            "📈 Too low! Try again."
        )

    else:
        await update.message.reply_text(
            "📉 Too high! Try again."
        )


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


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = random.choice(QUIZZES)

    context.user_data["quiz_answer"] = question["answer"]

    await update.message.reply_text(
        "🧠 QUIZ TIME!\n\n"
        + question["question"]
        + "\n\nSend your answer!"
    )


async def quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "quiz_answer" not in context.user_data:
        return

    answer = update.message.text.lower().strip()
    correct = context.user_data["quiz_answer"]

    if answer == correct:
        await update.message.reply_text(
            "🎉 Correct! 🔥"
        )
    else:
        await update.message.reply_text(
            f"❌ Wrong!\nThe correct answer was: {correct.title()}"
        )

    del context.user_data["quiz_answer"]
