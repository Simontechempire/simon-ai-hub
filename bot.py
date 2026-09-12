import os
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from database import init_db, add_user, get_user_count
from handlers.ai import ai_chat
from handlers.games import (
    games_menu,
    dice,
    dart,
    quiz,
    guess,
    guess_answer,
)
from handlers.admin import owner

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing from .env")


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

    await update.message.reply_text(
        f"👋 Welcome {user.first_name}!\n\n"
        "🤖 SIMON AI HUB\n\n"
        "Your all-in-one Telegram AI assistant.\n\n"
        "💬 Send me a message to chat with the AI.\n"
        "🎮 Use /games to play games.\n"
        "👑 Use /owner to see the bot owner.\n\n"
        "🚀 More tools coming soon!"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🆘 SIMON AI HUB HELP\n\n"
        "/start - Start the bot\n"
        "/help - Show help\n"
        "/stats - Bot statistics\n"
        "/about - About the bot\n"
        "/owner - Bot owner\n"
        "/games - Games\n"
        "/dice - Roll dice\n"
        "/dart - Throw dart\n"
        "/quiz - Play quiz\n"
        "/guess - Guess the number\n\n"
        "💬 Send a normal message to chat with the AI."
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    count = get_user_count()

    await update.message.reply_text(
        f"📊 SIMON AI HUB STATISTICS\n\n"
        f"👥 Total Users: {count}"
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 SIMON AI HUB\n\n"
        "An all-in-one Telegram AI bot created by Simon Tech.\n\n"
        "👨‍💻 Developer: @mrdarkdev\n"
        "🚀 Powered by Python + OpenAI."
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(
        "Exception while handling an update:",
        exc_info=context.error
    )


def main():
    init_db()

    application = Application.builder().token(BOT_TOKEN).build()

    # Main commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("owner", owner))

    # Games
    application.add_handler(CommandHandler("games", games_menu))
    application.add_handler(CommandHandler("dice", dice))
    application.add_handler(CommandHandler("dart", dart))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(CommandHandler("guess", guess))

    # Game answers
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            guess_answer
        )
    )

    # AI chat
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            ai_chat
        )
    )

    application.add_error_handler(error_handler)

    logger.info("SIMON AI HUB is starting...")

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
