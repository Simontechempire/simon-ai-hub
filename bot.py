import os
import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from database import init_db, add_user, get_user_count


BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is missing.")


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    add_user(
        user.id,
        user.username,
        user.first_name
    )

    message = (
        f"👋 Welcome {user.first_name}!\n\n"
        "🤖 *SIMON AI HUB*\n\n"
        "Your all-in-one Telegram assistant.\n\n"
        "🤖 AI Tools\n"
        "🎨 Creative Tools\n"
        "📚 Education\n"
        "🎮 Games\n"
        "🛠 Utilities\n"
        "👨‍💻 Developer Tools\n"
        "📁 File Tools\n"
        "⚙️ Settings\n\n"
        "🚀 More features coming soon!"
    )

    await update.message.reply_text(
        message,
        parse_mode="Markdown"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 *SIMON AI HUB HELP*\n\n"
        "/start - Start the bot\n"
        "/help - Show help\n"
        "/tools - Show available tools\n"
        "/stats - Show bot statistics\n"
        "/about - About the bot",
        parse_mode="Markdown",
    )


async def tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 *SIMON AI HUB TOOLS*\n\n"
        "🤖 AI Tools\n"
        "🎨 Creative Tools\n"
        "📚 Education Tools\n"
        "🎮 Games\n"
        "💰 Business Tools\n"
        "🔐 Developer Tools\n"
        "📁 File Tools\n\n"
        "More tools will be added soon 🚀",
        parse_mode="Markdown",
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    count = get_user_count()

    await update.message.reply_text(
        f"📊 *SIMON AI HUB STATISTICS*\n\n"
        f"👥 Total Users: `{count}`",
        parse_mode="Markdown",
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *SIMON AI HUB*\n\n"
        "An all-in-one Telegram bot created by Simon.\n\n"
        "Powered by Python and designed to provide "
        "AI, utility, education, developer and creative tools.",
        parse_mode="Markdown",
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(
        "Exception while handling an update:",
        exc_info=context.error
    )


def main():
    init_db()

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("tools", tools))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("about", about))

    application.add_error_handler(error_handler)

    logger.info("SIMON AI HUB is starting...")

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
