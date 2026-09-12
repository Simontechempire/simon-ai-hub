from telegram import Update
from telegram.ext import ContextTypes

from plugins.ai_tools import ask_ai


async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    if not user_message:
        return

    await update.message.chat.send_action("typing")

    try:
        answer = ask_ai(user_message)

        await update.message.reply_text(answer)

    except Exception as error:
        print(f"AI Error: {error}")

        await update.message.reply_text(
            "❌ Sorry, I couldn't process your request right now."
        )
