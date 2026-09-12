import os

from telegram import Update
from telegram.ext import ContextTypes


ADMIN_ID = os.getenv("ADMIN_ID")

OWNER_NAME = "Simon Tech"
OWNER_USERNAME = "@mrdarkdev"


def is_admin(user_id: int) -> bool:
    return ADMIN_ID and str(user_id) == ADMIN_ID


async def owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 BOT OWNER\n\n"
        f"👤 Name: {OWNER_NAME}\n"
        f"🔗 Username: {OWNER_USERNAME}\n\n"
        "🤖 SIMON AI HUB\n"
        "🛠 Developer & Owner"
    )


async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if not is_admin(user.id):
        await update.message.reply_text(
            "❌ You are not authorized to use the admin panel."
        )
        return

    await update.message.reply_text(
        "👑 SIMON AI HUB — ADMIN PANEL\n\n"
        "/owner - Bot owner\n"
        "/adminstats - Bot statistics\n"
        "/broadcast - Broadcast message\n"
        "/users - User management"
    )


async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if not is_admin(user.id):
        await update.message.reply_text("❌ Access denied.")
        return

    await update.message.reply_text(
        "📊 ADMIN STATISTICS\n\n"
        "👥 User statistics will be connected here."
    )
