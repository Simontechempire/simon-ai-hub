import os
import logging

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    PollAnswerHandler,
    ContextTypes,
    filters,
)

from database import init_db, add_user, get_user_count

from handlers.ai import ai_chat

from handlers.games import (
    games_menu,
    dice,
    dart,
    guess,
    guess_answer,
)

from handlers.admin import owner

from handlers.quiz import (
    quiz,
    quiz_subject,
    quiz_difficulty,
    quiz_next,
    quiz_stop,
    quiz_close,
    quiz_back_subjects,
    quiz_answer,
)

from handlers.moderator import (
    moderator_panel,
    modhelp,
    ban,
    unban,
    kick,
    mute,
    unmute,
    warn,
    unwarn,
    warnings,
    clearwarns,
    softban,
    delete_message,
    purge,
    purgeuser,
    clear,
    pin,
    unpin,
    antispam,
    spam,
    flood,
    antiflood,
    lock,
    unlock,
    lockall,
    unlockall,
    lockmedia,
    unlockmedia,
    locklinks,
    unlocklinks,
    locksticker,
    unlocksticker,
    antilink,
    allowlink,
    blocklink,
    whitelist,
    unwhitelist,
    domains,
    adddomain,
    deldomain,
    cleardomains,
    userinfo,
    user_id,
    admins,
    mods,
    modlist,
    addmod,
    delmod,
    promote,
    demote,
    checkmod,
    warnlist,
    reason,
    setwarnlimit,
    warnlimit,
    resetwarn,
    warning,
    warningset,
    warnmode,
    autoban,
    autokick,
    antibot,
    botcheck,
    botmode,
    captcha,
    verify,
    unverify,
    raidmode,
    raid,
    unraid,
    joinprotect,
    announce,
    notice,
    rules,
    setrules,
    modnote,
    note,
    notes,
    report,
    reports,
    reportslist,
    modstats,
    log,
    logs,
    modlog,
    setlog,
    chatstats,
    userstats,
    activity,
    topmods,
    actionlog,
    slowmode,
    unslowmode,
    setslowmode,
    approval,
    approve,
    disapprove,
    blacklist,
    unblacklist,
)


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is missing from .env"
    )


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    format=(
        "%(asctime)s - %(name)s - "
        "%(levelname)s - %(message)s"
    ),
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# ============================================================
# START
# ============================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
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
        "🎮 Use /games for games.\n"
        "🧠 Use /quiz for the AI quiz.\n"
        "👑 Use /owner for the bot owner.\n"
        "🛡️ Use /modhelp for moderator commands.\n\n"
        "🚀 More tools coming soon!"
    )


# ============================================================
# HELP
# ============================================================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "🆘 SIMON AI HUB HELP\n\n"

        "🤖 GENERAL\n"
        "/start - Start the bot\n"
        "/help - Show help\n"
        "/stats - Bot statistics\n"
        "/about - About the bot\n"
        "/owner - Bot owner\n\n"

        "🎮 GAMES\n"
        "/games - Games menu\n"
        "/dice - Roll dice\n"
        "/dart - Throw dart\n"
        "/guess - Guess the number\n\n"

        "🧠 AI QUIZ\n"
        "/quiz - Start AI quiz\n\n"

        "🛡️ MODERATION\n"
        "/modhelp - Moderator commands\n"
        "/modpanel - Moderator panel\n\n"

        "💬 Send a normal message to chat with the AI."
    )


# ============================================================
# STATS
# ============================================================

async def stats(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    count = get_user_count()

    await update.message.reply_text(
        "📊 SIMON AI HUB STATISTICS\n\n"
        f"👥 Total Users: {count}"
    )


# ============================================================
# ABOUT
# ============================================================

async def about(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "🤖 SIMON AI HUB\n\n"
        "An all-in-one Telegram AI bot "
        "created by Simon Tech.\n\n"
        "👨‍💻 Developer: @mrdarkdev\n"
        "🚀 Powered by Python + OpenAI."
    )


# ============================================================
# ERROR HANDLER
# ============================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):
    logger.error(
        "Exception while handling an update:",
        exc_info=context.error
    )


# ============================================================
# MAIN
# ============================================================

def main():

    init_db()

    application = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )

    # ========================================================
    # MAIN COMMANDS
    # ========================================================

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    application.add_handler(
        CommandHandler("stats", stats)
    )

    application.add_handler(
        CommandHandler("about", about)
    )

    application.add_handler(
        CommandHandler("owner", owner)
    )

    # ========================================================
    # GAMES
    # ========================================================

    application.add_handler(
        CommandHandler("games", games_menu)
    )

    application.add_handler(
        CommandHandler("dice", dice)
    )

    application.add_handler(
        CommandHandler("dart", dart)
    )

    application.add_handler(
        CommandHandler("guess", guess)
    )

    # ========================================================
    # NEW AI QUIZ
    # ========================================================

    application.add_handler(
        CommandHandler("quiz", quiz)
    )

    # Subject buttons
    application.add_handler(
        CallbackQueryHandler(
            quiz_subject,
            pattern=r"^quiz_subject:"
        )
    )

    # Difficulty buttons
    application.add_handler(
        CallbackQueryHandler(
            quiz_difficulty,
            pattern=r"^quiz_difficulty:"
        )
    )

    # Next question
    application.add_handler(
        CallbackQueryHandler(
            quiz_next,
            pattern=r"^quiz_next$"
        )
    )

    # Stop quiz
    application.add_handler(
        CallbackQueryHandler(
            quiz_stop,
            pattern=r"^quiz_stop$"
        )
    )

    # Close quiz
    application.add_handler(
        CallbackQueryHandler(
            quiz_close,
            pattern=r"^quiz_close$"
        )
    )

    # Back to subjects
    application.add_handler(
        CallbackQueryHandler(
            quiz_back_subjects,
            pattern=r"^quiz_back_subjects$"
        )
    )

    # Telegram poll answers
    application.add_handler(
        PollAnswerHandler(quiz_answer)
    )

    # ========================================================
    # MODERATOR COMMANDS
    # ========================================================

    moderator_commands = {

        "modhelp": modhelp,
        "modpanel": moderator_panel,

        "ban": ban,
        "unban": unban,
        "kick": kick,
        "mute": mute,
        "unmute": unmute,
        "warn": warn,
        "unwarn": unwarn,
        "warnings": warnings,
        "clearwarns": clearwarns,
        "softban": softban,

        "del": delete_message,
        "purge": purge,
        "purgeuser": purgeuser,
        "clear": clear,
        "pin": pin,
        "unpin": unpin,
        "antispam": antispam,
        "spam": spam,
        "flood": flood,
        "antiflood": antiflood,

        "lock": lock,
        "unlock": unlock,
        "lockall": lockall,
        "unlockall": unlockall,
        "lockmedia": lockmedia,
        "unlockmedia": unlockmedia,
        "locklinks": locklinks,
        "unlocklinks": unlocklinks,
        "locksticker": locksticker,
        "unlocksticker": unlocksticker,

        "antilink": antilink,
        "allowlink": allowlink,
        "blocklink": blocklink,
        "whitelist": whitelist,
        "unwhitelist": unwhitelist,
        "domains": domains,
        "adddomain": adddomain,
        "deldomain": deldomain,
        "cleardomains": cleardomains,

        "userinfo": userinfo,
        "id": user_id,
        "admins": admins,
        "mods": mods,
        "modlist": modlist,
        "addmod": addmod,
        "delmod": delmod,
        "promote": promote,
        "demote": demote,
        "checkmod": checkmod,

        "warnlist": warnlist,
        "reason": reason,
        "setwarnlimit": setwarnlimit,
        "warnlimit": warnlimit,
        "resetwarn": resetwarn,
        "warning": warning,
        "warningset": warningset,
        "warnmode": warnmode,
        "autoban": autoban,
        "autokick": autokick,

        "antibot": antibot,
        "botcheck": botcheck,
        "botmode": botmode,
        "captcha": captcha,
        "verify": verify,
        "unverify": unverify,
        "raidmode": raidmode,
        "raid": raid,
        "unraid": unraid,
        "joinprotect": joinprotect,

        "announce": announce,
        "notice": notice,
        "rules": rules,
        "setrules": setrules,
        "modnote": modnote,
        "note": note,
        "notes": notes,
        "report": report,
        "reports": reports,
        "reportslist": reportslist,

        "modstats": modstats,
        "log": log,
        "logs": logs,
        "modlog": modlog,
        "setlog": setlog,
        "chatstats": chatstats,
        "userstats": userstats,
        "activity": activity,
        "topmods": topmods,
        "actionlog": actionlog,

        "slowmode": slowmode,
        "unslowmode": unslowmode,
        "setslowmode": setslowmode,
        "approval": approval,
        "approve": approve,
        "disapprove": disapprove,
        "blacklist": blacklist,
        "unblacklist": unblacklist,
    }

    for command, handler in moderator_commands.items():
        application.add_handler(
            CommandHandler(
                command,
                handler
            )
        )

    # ========================================================
    # GUESS GAME ANSWERS
    # ========================================================

    application.add_handler(
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND,
            guess_answer
        )
    )

    # ========================================================
    # AI CHAT
    # ========================================================

    application.add_handler(
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND,
            ai_chat
        )
    )

    # ========================================================
    # ERROR HANDLER
    # ========================================================

    application.add_error_handler(
        error_handler
    )

    logger.info(
        "SIMON AI HUB is starting..."
    )

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
