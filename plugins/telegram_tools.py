from telegram import Bot
import os


async def get_bot_info():
    token = os.getenv("BOT_TOKEN")

    if not token:
        return "❌ BOT_TOKEN is missing."

    bot = Bot(token=token)

    me = await bot.get_me()

    return (
        f"🤖 Bot Information\n\n"
        f"Name: {me.first_name}\n"
        f"Username: @{me.username}\n"
        f"ID: {me.id}"
    )
