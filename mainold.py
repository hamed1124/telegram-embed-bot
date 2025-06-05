import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters
)
from yt_dlp import YoutubeDL

logging.basicConfig(level=logging.INFO)

# توکن مستقیم اینجا قرار داده شده
TOKEN = "2077511133:AAHYQVTRTFoiGdERfOpV0d7Sv2YO2e54T8k"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! یک لینک اینستاگرام/یوتیوب/توییتر بفرست تا لینک مستقیمش رو به‌صورت embed دریافت کنی."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    try:
        with YoutubeDL({"quiet": True, "skip_download": True}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get("title", "لینک")
            webpage = info.get("webpage_url", url)
            await update.message.reply_text(
                f"[{title}]({webpage})",
                parse_mode="Markdown",
                disable_web_page_preview=False,
            )
    except Exception as e:
        logging.error(e)
        await update.message.reply_text("❌ نتوانستم لینک را پردازش کنم!")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
