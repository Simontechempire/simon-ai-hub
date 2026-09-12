from telegram import Update
from telegram.ext import ContextTypes


async def files_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📁 SIMON AI HUB — FILE TOOLS\n\n"
        "📄 Send me a document and I can process it.\n"
        "🖼 Send me an image for image tools.\n"
        "🎵 Send me an audio file for audio tools.\n"
        "🎬 Send me a video for video tools.\n\n"
        "More file features will be added."
    )


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document

    await update.message.reply_text(
        f"📁 File received!\n\n"
        f"📄 Name: {document.file_name}\n"
        f"📦 Size: {document.file_size} bytes\n\n"
        "✅ File detected successfully."
    )
