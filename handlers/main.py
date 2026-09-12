from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes


# ============================================================
# MAIN MENU
# ============================================================

def main_keyboard():
    keyboard = [
        ["🤖 AI", "⚙️ Settings"],
        ["👥 Social", "🎮 Games"],
        ["🛒 Shop", "🎉 Fun"],
        ["📰 News", "🌐 General"],
        ["👑 Empire", "🐾 Pet"],
        ["🪪 Identity", "🎌 Anime"],
        ["⚡ Pokemon", "🛡️ Mod Panel"],
        ["➕ Add SIMON AI HUB to Group"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        is_persistent=True,
    )


# ============================================================
# BACK BUTTON
# ============================================================

def back_keyboard():
    return ReplyKeyboardMarkup(
        [["⬅️ Back"]],
        resize_keyboard=True,
    )


# ============================================================
# MAIN MENU MESSAGE
# ============================================================

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    await update.message.reply_text(
        f"👋 Welcome {user.first_name}!\n\n"
        "╭━━━〔 🤖 SIMON AI HUB 〕━━━╮\n"
        "┃\n"
        "┃ 🚀 All-In-One Telegram Assistant\n"
        "┃\n"
        "┃ 🤖 AI • 🎮 Games • 👥 Social\n"
        "┃ 🛒 Shop • 🎉 Fun • 📰 News\n"
        "┃ 👑 Empire • 🐾 Pet • 🎌 Anime\n"
        "┃ ⚡ Pokemon • 🛡️ Moderation\n"
        "┃\n"
        "╰━━━━━━━━━━━━━━━━━━━━━━╯\n\n"
        "👇 Select a menu below:",
        reply_markup=main_keyboard(),
    )


# ============================================================
# AI MENU
# ============================================================

async def ai_menu(update, context):

    await update.message.reply_text(
        "🤖 AI MENU\n\n"
        "/ai - Chat with AI\n"
        "/ask - Ask AI\n"
        "/write - AI writing\n"
        "/code - Coding assistant\n"
        "/explain - Explain something\n"
        "/summarize - Summarize text\n"
        "/translate - Translate text\n"
        "/grammar - Fix grammar\n"
        "/story - Create a story\n"
        "/idea - Generate ideas",
        reply_markup=back_keyboard(),
    )


# ============================================================
# SETTINGS MENU
# ============================================================

async def settings_menu(update, context):

    await update.message.reply_text(
        "⚙️ SETTINGS\n\n"
        "/settings - Settings\n"
        "/language - Change language\n"
        "/notifications - Notifications\n"
        "/privacy - Privacy settings\n"
        "/reset - Reset settings",
        reply_markup=back_keyboard(),
    )


# ============================================================
# SOCIAL MENU
# ============================================================

async def social_menu(update, context):

    await update.message.reply_text(
        "👥 SOCIAL\n\n"
        "/profile - View profile\n"
        "/setbio - Set bio\n"
        "/setname - Change name\n"
        "/friends - Friends list\n"
        "/addfriend - Add friend\n"
        "/removefriend - Remove friend\n"
        "/rep - Give reputation\n"
        "/myrep - Your reputation\n"
        "/toprep - Reputation leaderboard\n"
        "/level - Your level\n"
        "/rank - Your rank\n"
        "/online - Online users\n"
        "/marry - Marry a user\n"
        "/divorce - Divorce\n"
        "/couple - View couple\n"
        "/gift - Send gift",
        reply_markup=back_keyboard(),
    )


# ============================================================
# GAMES MENU
# ============================================================

async def games_menu_button(update, context):

    await update.message.reply_text(
        "🎮 GAMES\n\n"
        "/games - Games menu\n"
        "/dice - Roll dice\n"
        "/dart - Throw dart\n"
        "/guess - Guess number\n"
        "/trivia - Trivia\n"
        "/riddle - Riddle\n"
        "/coinflip - Coin flip\n"
        "/rps - Rock Paper Scissors\n"
        "/ttt - Tic Tac Toe\n"
        "/8ball - Magic 8 Ball\n"
        "/slots - Slots\n"
        "/blackjack - Blackjack",
        reply_markup=back_keyboard(),
    )


# ============================================================
# SHOP MENU
# ============================================================

async def shop_menu(update, context):

    await update.message.reply_text(
        "🛒 SHOP\n\n"
        "/shop - Open shop\n"
        "/buy - Buy item\n"
        "/sell - Sell item\n"
        "/inventory - Your inventory\n"
        "/item - Item information\n"
        "/use - Use item\n"
        "/gift - Give gift\n"
        "/daily - Daily reward",
        reply_markup=back_keyboard(),
    )


# ============================================================
# FUN MENU
# ============================================================

async def fun_menu(update, context):

    await update.message.reply_text(
        "🎉 FUN\n\n"
        "/fun - Fun menu\n"
        "/joke - Random joke\n"
        "/meme - Random meme\n"
        "/quote - Random quote\n"
        "/fact - Random fact\n"
        "/roast - Roast a user\n"
        "/compliment - Compliment\n"
        "/pickup - Pickup line\n"
        "/rate - Rate something\n"
        "/truth - Truth\n"
        "/dare - Dare\n"
        "/wyr - Would You Rather",
        reply_markup=back_keyboard(),
    )


# ============================================================
# NEWS MENU
# ============================================================

async def news_menu(update, context):

    await update.message.reply_text(
        "📰 NEWS\n\n"
        "/news - Latest news\n"
        "/worldnews - World news\n"
        "/technews - Technology news\n"
        "/sportsnews - Sports news\n"
        "/entertainment - Entertainment news\n"
        "/trending - Trending topics",
        reply_markup=back_keyboard(),
    )


# ============================================================
# GENERAL MENU
# ============================================================

async def general_menu(update, context):

    await update.message.reply_text(
        "🌐 GENERAL\n\n"
        "/help - Help\n"
        "/start - Start bot\n"
        "/about - About bot\n"
        "/stats - Bot statistics\n"
        "/id - Get ID\n"
        "/ping - Check bot speed\n"
        "/time - Current time\n"
        "/weather - Weather\n"
        "/calculator - Calculator",
        reply_markup=back_keyboard(),
    )


# ============================================================
# EMPIRE MENU
# ============================================================

async def empire_menu(update, context):

    await update.message.reply_text(
        "👑 EMPIRE\n\n"
        "/empire - Your empire\n"
        "/territory - View territory\n"
        "/army - View army\n"
        "/attack - Attack\n"
        "/defend - Defend\n"
        "/leaderboard - Empire leaderboard\n"
        "/war - Start war\n"
        "/upgrade - Upgrade empire\n"
        "/resources - View resources\n"
        "/empirestats - Empire statistics",
        reply_markup=back_keyboard(),
    )


# ============================================================
# PET MENU
# ============================================================

async def pet_menu(update, context):

    await update.message.reply_text(
        "🐾 PET\n\n"
        "/pet - View your pet\n"
        "/adopt - Adopt pet\n"
        "/feed - Feed pet\n"
        "/play - Play with pet\n"
        "/train - Train pet\n"
        "/petstats - Pet statistics\n"
        "/petshop - Pet shop\n"
        "/petbattle - Pet battle\n"
        "/petname - Rename pet\n"
        "/release - Release pet",
        reply_markup=back_keyboard(),
    )


# ============================================================
# IDENTITY MENU
# ============================================================

async def identity_menu(update, context):

    await update.message.reply_text(
        "🪪 IDENTITY\n\n"
        "/identity - Identity card\n"
        "/title - Set title\n"
        "/badge - View badges\n"
        "/achievements - Achievements\n"
        "/level - Your level\n"
        "/xp - View XP\n"
        "/rank - Your rank\n"
        "/avatar - View avatar\n"
        "/card - Profile card",
        reply_markup=back_keyboard(),
    )


# ============================================================
# ANIME MENU
# ============================================================

async def anime_menu(update, context):

    await update.message.reply_text(
        "🎌 ANIME\n\n"
        "/anime - Anime menu\n"
        "/animeinfo - Anime information\n"
        "/character - Anime character\n"
        "/animequote - Anime quote\n"
        "/animequiz - Anime quiz\n"
        "/randomanime - Random anime\n"
        "/animewallpaper - Anime wallpaper",
        reply_markup=back_keyboard(),
    )


# ============================================================
# POKEMON MENU
# ============================================================

async def pokemon_menu(update, context):

    await update.message.reply_text(
        "⚡ POKEMON\n\n"
        "/pokemon - Pokemon menu\n"
        "/pokedex - Pokedex\n"
        "/catch - Catch Pokemon\n"
        "/train - Train Pokemon\n"
        "/battle - Pokemon battle\n"
        "/evolve - Evolve Pokemon\n"
        "/pokemonteam - Your team\n"
        "/pokebag - Your Pokebag\n"
        "/pokemonshop - Pokemon shop\n"
        "/pokemonrank - Pokemon ranking",
        reply_markup=back_keyboard(),
    )


# ============================================================
# ADD BOT TO GROUP
# ============================================================

async def add_to_group(update, context):

    bot_username = context.bot.username

    url = (
        f"https://t.me/{bot_username}"
        "?startgroup=true"
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "➕ Add SIMON AI HUB to Group",
                url=url
            )
        ]
    ])

    await update.message.reply_text(
        "➕ ADD SIMON AI HUB TO GROUP\n\n"
        "Add me to your Telegram group and "
        "unlock group features.",
        reply_markup=keyboard,
    )


# ============================================================
# BACK TO MAIN MENU
# ============================================================

async def back_to_main(update, context):

    await update.message.reply_text(
        "🏠 Main Menu",
        reply_markup=main_keyboard(),
    )


# ============================================================
# MENU ROUTER
# ============================================================

async def menu_router(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message or not update.message.text:
        return

    text = update.message.text

    if text == "🤖 AI":
        await ai_menu(update, context)

    elif text == "⚙️ Settings":
        await settings_menu(update, context)

    elif text == "👥 Social":
        await social_menu(update, context)

    elif text == "🎮 Games":
        await games_menu_button(update, context)

    elif text == "🛒 Shop":
        await shop_menu(update, context)

    elif text == "🎉 Fun":
        await fun_menu(update, context)

    elif text == "📰 News":
        await news_menu(update, context)

    elif text == "🌐 General":
        await general_menu(update, context)

    elif text == "👑 Empire":
        await empire_menu(update, context)

    elif text == "🐾 Pet":
        await pet_menu(update, context)

    elif text == "🪪 Identity":
        await identity_menu(update, context)

    elif text == "🎌 Anime":
        await anime_menu(update, context)

    elif text == "⚡ Pokemon":
        await pokemon_menu(update, context)

    elif text == "➕ Add SIMON AI HUB to Group":
        await add_to_group(update, context)

    elif text == "⬅️ Back":
        await back_to_main(update, context)
