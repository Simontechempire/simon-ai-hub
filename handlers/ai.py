import os

from openai import OpenAI
from telegram import Update
from telegram.ext import ContextTypes


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    prompt = update.message.text

    try:
        response = client.responses.create(
            model="gpt-5",
            input=prompt
        )

        answer = response.output_text

        await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text(
            "❌ AI error. Please try again later."
        )
