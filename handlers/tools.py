from telegram import Update
from telegram.ext import ContextTypes


async def tools_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 SIMON AI HUB — TOOLS\n\n"
        "🤖 AI Tools\n"
        "🎨 Creative Tools\n"
        "📚 Education Tools\n"
        "🎮 Games\n"
        "📁 File Tools\n"
        "👨‍💻 Developer Tools\n"
        "📱 Telegram Tools\n"
        "⚙️ Utilities\n\n"
        "Select a tool from the menu to get started."
    )
