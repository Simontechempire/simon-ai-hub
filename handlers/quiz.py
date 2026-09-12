import os
import json
import asyncio
import logging

from dotenv import load_dotenv
from openai import AsyncOpenAI

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
)

load_dotenv()

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing from .env")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


# ============================================================
# SUBJECTS
# ============================================================

SUBJECTS = [
    "English Studies",
    "Mathematics",
    "CRS",
    "Home Economics",
    "Marketing",
    "Computer Science",
    "Agricultural Science",
    "Chemistry",
    "Biology",
    "Financial Accounting",
    "Physics",
    "Government",
    "Sports",
    "General Discussion",
    "General Knowledge",
    "Civic Education",
    "Literature in English",
    "Commerce",
    "Economics",
    "Geography",
    "History",
    "Basic Science",
    "Social Studies",
    "Health Education",
    "Further Mathematics",
    "Technical Drawing",
    "Data Processing",
    "ICT",
    "Entrepreneurship",
    "Business Studies",
    "French",
]


DIFFICULTIES = {
    "easy": "Easy",
    "medium": "Medium",
    "hard": "Hard",
}


QUIZ_TIME = 10 * 60


# ============================================================
# START QUIZ
# ============================================================

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Open the subject selection menu."""

    keyboard = []

    row = []

    for subject in SUBJECTS:
        button = InlineKeyboardButton(
            subject,
            callback_data=f"quiz_subject:{subject}"
        )

        row.append(button)

        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    keyboard.append([
        InlineKeyboardButton(
            "❌ Close",
            callback_data="quiz_close"
        )
    ])

    await update.message.reply_text(
        "🧠 SIMON AI HUB QUIZ\n\n"
        "📚 Choose a subject:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ============================================================
# SUBJECT SELECTION
# ============================================================

async def quiz_subject(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    subject = query.data.split(":", 1)[1]

    context.user_data["quiz_subject"] = subject

    keyboard = [
        [
            InlineKeyboardButton(
                "🟢 Easy",
                callback_data="quiz_difficulty:easy"
            ),
            InlineKeyboardButton(
                "🟡 Medium",
                callback_data="quiz_difficulty:medium"
            ),
        ],
        [
            InlineKeyboardButton(
                "🔴 Hard",
                callback_data="quiz_difficulty:hard"
            ),
        ],
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="quiz_back_subjects"
            )
        ],
    ]

    await query.edit_message_text(
        f"📚 Subject: {subject}\n\n"
        "🎯 Choose difficulty:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ============================================================
# DIFFICULTY SELECTION
# ============================================================

async def quiz_difficulty(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    difficulty_key = query.data.split(":", 1)[1]

    subject = context.user_data.get("quiz_subject")

    if not subject:
        await query.edit_message_text(
            "❌ Quiz session expired.\n\n"
            "Use /quiz to start again."
        )
        return

    difficulty = DIFFICULTIES.get(
        difficulty_key,
        "Medium"
    )

    context.user_data["quiz_difficulty"] = difficulty
    context.user_data["quiz_score"] = 0
    context.user_data["quiz_question_number"] = 0
    context.user_data["quiz_active"] = True

    await query.edit_message_text(
        f"📚 Subject: {subject}\n"
        f"🎯 Difficulty: {difficulty}\n\n"
        "🤖 Generating your first question..."
    )

    await send_question(
        chat_id=query.message.chat_id,
        context=context,
    )


# ============================================================
# AI QUESTION GENERATOR
# ============================================================

async def generate_question(
    subject: str,
    difficulty: str,
):
    prompt = f"""
You are a professional educational quiz generator.

Create ONE high-quality multiple-choice question.

Subject:
{subject}

Difficulty:
{difficulty}

The question must have exactly SIX answer options:
A, B, C, D, E, F.

Only ONE answer may be correct.

Return ONLY valid JSON in this exact structure:

{{
  "question": "Question text",
  "options": [
    "Option A",
    "Option B",
    "Option C",
    "Option D",
    "Option E",
    "Option F"
  ],
  "correct_option": 0,
  "explanation": "Short explanation of the correct answer."
}}

Rules:

- correct_option must be a number from 0 to 5.
- Make the question appropriate for the selected subject.
- Match the requested difficulty.
- Do not put A., B., C., etc. inside the option text.
- Do not create trick questions.
- Make sure exactly one option is correct.
"""

    response = await client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You generate accurate educational "
                    "multiple-choice questions."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.7,
        response_format={
            "type": "json_object"
        },
    )

    content = response.choices[0].message.content

    data = json.loads(content)

    question = data["question"]
    options = data["options"]
    correct_option = int(data["correct_option"])
    explanation = data.get(
        "explanation",
        "No explanation provided."
    )

    if len(options) != 6:
        raise ValueError(
            "AI did not return exactly 6 options."
        )

    if correct_option < 0 or correct_option > 5:
        raise ValueError(
            "Invalid correct option."
        )

    return {
        "question": question,
        "options": options,
        "correct_option": correct_option,
        "explanation": explanation,
    }


# ============================================================
# SEND QUESTION
# ============================================================

async def send_question(
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE,
):
    subject = context.user_data.get("quiz_subject")
    difficulty = context.user_data.get(
        "quiz_difficulty"
    )

    if not subject or not difficulty:
        return

    if not context.user_data.get(
        "quiz_active",
        False
    ):
        return

    # Cancel previous timer
    old_task = context.user_data.get(
        "quiz_timer_task"
    )

    if old_task:
        old_task.cancel()

    question_number = (
        context.user_data.get(
            "quiz_question_number",
            0
        ) + 1
    )

    context.user_data[
        "quiz_question_number"
    ] = question_number

    try:
        question_data = await generate_question(
            subject,
            difficulty,
        )
    except Exception as error:
        logger.exception(
            "Quiz question generation failed: %s",
            error
        )

        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                "❌ I couldn't generate the question.\n\n"
                "Please try again."
            ),
        )
        return

    context.user_data[
        "current_quiz_question"
    ] = question_data

    context.user_data[
        "current_quiz_poll_id"
    ] = None

    # Send quiz poll
    message = await context.bot.send_poll(
        chat_id=chat_id,
        question=(
            f"🧠 {subject}\n\n"
            f"Question {question_number}\n"
            f"🎯 Difficulty: {difficulty}\n\n"
            f"{question_data['question']}"
        ),
        options=question_data["options"],
        type="quiz",
        correct_option_id=question_data[
            "correct_option"
        ],
        is_anonymous=False,
        explanation=question_data[
            "explanation"
        ],
    )

    context.user_data[
        "current_quiz_poll_id"
    ] = message.poll.id

    # Navigation menu
    keyboard = [
        [
            InlineKeyboardButton(
                "⛔ Stop Quiz",
                callback_data="quiz_stop"
            ),
            InlineKeyboardButton(
                "➡️ Next",
                callback_data="quiz_next"
            ),
        ]
    ]

    timer_message = await context.bot.send_message(
        chat_id=chat_id,
        text=(
            "⏱️ Time: 10:00\n\n"
            "Choose an answer in the poll above.\n"
            "The next question will appear when the timer expires."
        ),
        reply_markup=InlineKeyboardMarkup(
            keyboard
        ),
    )

    context.user_data[
        "quiz_timer_message_id"
    ] = timer_message.message_id

    # Start 10-minute timer
    task = asyncio.create_task(
        quiz_timer(
            chat_id,
            context,
            timer_message.message_id,
        )
    )

    context.user_data[
        "quiz_timer_task"
    ] = task


# ============================================================
# 10-MINUTE TIMER
# ============================================================

async def quiz_timer(
    chat_id: int,
    context: ContextTypes.DEFAULT_TYPE,
    timer_message_id: int,
):
    try:
        remaining = QUIZ_TIME

        while remaining > 0:

            if not context.user_data.get(
                "quiz_active",
                False
            ):
                return

            minutes = remaining // 60
            seconds = remaining % 60

            # Update every 10 seconds at first,
            # then every minute to avoid Telegram API spam.
            if (
                remaining == QUIZ_TIME
                or remaining <= 60
                or remaining % 60 == 0
            ):
                try:
                    await context.bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=timer_message_id,
                        text=(
                            f"⏱️ Time remaining: "
                            f"{minutes:02d}:{seconds:02d}\n\n"
                            "Answer the poll above."
                        ),
                        reply_markup=InlineKeyboardMarkup([
                            [
                                InlineKeyboardButton(
                                    "⛔ Stop Quiz",
                                    callback_data="quiz_stop"
                                ),
                                InlineKeyboardButton(
                                    "➡️ Next",
                                    callback_data="quiz_next"
                                ),
                            ]
                        ]),
                    )
                except Exception:
                    pass

            await asyncio.sleep(1)
            remaining -= 1

        # Time expired
        if not context.user_data.get(
            "quiz_active",
            False
        ):
            return

        try:
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=timer_message_id,
                text=(
                    "⏰ TIME EXPIRED!\n\n"
                    "➡️ Loading the next question..."
                ),
            )
        except Exception:
            pass

        await asyncio.sleep(2)

        await send_question(
            chat_id=chat_id,
            context=context,
        )

    except asyncio.CancelledError:
        return

    except Exception as error:
        logger.exception(
            "Quiz timer error: %s",
            error
        )


# ============================================================
# POLL ANSWER
# ============================================================

async def quiz_answer(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    answer = update.poll_answer

    if not answer:
        return

    user_id = answer.user.id

    # This implementation stores quiz state in the
    # user's context. Only process if the user is active.
    active_user = context.application.user_data.get(
        user_id
    )

    if not active_user:
        return


# ============================================================
# NEXT QUESTION
# ============================================================

async def quiz_next(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    if not context.user_data.get(
        "quiz_active",
        False
    ):
        await query.message.reply_text(
            "❌ No active quiz.\n\n"
            "Use /quiz to start one."
        )
        return

    task = context.user_data.get(
        "quiz_timer_task"
    )

    if task:
        task.cancel()

    try:
        await query.message.delete()
    except Exception:
        pass

    await send_question(
        chat_id=query.message.chat_id,
        context=context,
    )


# ============================================================
# STOP QUIZ
# ============================================================

async def quiz_stop(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    task = context.user_data.get(
        "quiz_timer_task"
    )

    if task:
        task.cancel()

    score = context.user_data.get(
        "quiz_score",
        0
    )

    questions = context.user_data.get(
        "quiz_question_number",
        0
    )

    subject = context.user_data.get(
        "quiz_subject",
        "Unknown"
    )

    difficulty = context.user_data.get(
        "quiz_difficulty",
        "Unknown"
    )

    context.user_data[
        "quiz_active"
    ] = False

    await query.edit_message_text(
        "🏆 QUIZ STOPPED\n\n"
        f"📚 Subject: {subject}\n"
        f"🎯 Difficulty: {difficulty}\n\n"
        f"📝 Questions: {questions}\n"
        f"✅ Correct: {score}\n\n"
        f"🏆 Score: {score}/{questions}\n\n"
        "Use /quiz to play again."
    )


# ============================================================
# CLOSE QUIZ MENU
# ============================================================

async def quiz_close(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "❌ Quiz menu closed.\n\n"
        "Use /quiz whenever you want to play."
    )


# ============================================================
# BACK TO SUBJECTS
# ============================================================

async def quiz_back_subjects(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    keyboard = []

    row = []

    for subject in SUBJECTS:
        row.append(
            InlineKeyboardButton(
                subject,
                callback_data=f"quiz_subject:{subject}"
            )
        )

        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    await query.edit_message_text(
        "📚 Choose a subject:",
        reply_markup=InlineKeyboardMarkup(
            keyboard
        ),
    )
