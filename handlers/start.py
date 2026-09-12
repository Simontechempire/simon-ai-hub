from telegram import Update
from telegram.ext import ContextTypes

from database import add_user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    add_user(
        user.id,
        user.username,
        user.first_name
    )

    await update.message.reply_text(
        f"👋 Welcome {user.first_name}!\n\n"
        "🤖 SIMON AI HUB\n\n"
        "Your all-in-one Telegram assistant.\n\n"
        "🤖 AI Tools\n"
        "🎨 Creative Tools\n"
        "📚 Education\n"
        "🎮 Games\n"
        "🛠 Utilities\n"
        "👨‍💻 Developer Tools\n"
        "📁 File Tools\n"
        "⚙️ Settings\n\n"
        "🚀 More features to come!"
    )
