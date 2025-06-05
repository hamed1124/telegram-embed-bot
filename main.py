import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters
)
from yt_dlp import YoutubeDL

logging.basicConfig(level=logging.INFO)

TOKEN = "2077511133:AAHYQVTRTFoiGdERfOpV0d7Sv2YO2e54T8k"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لینک اینستا/یوتیوب/توییتر بفرست تا به‌صورت پخش‌شونده ارسال کنم.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "forceurl": True,
            "noplaylist": True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get("url")
            title = info.get("title", "ویدیو")

            if info.get("ext") in ["mp4", "webm"]:
                await update.message.reply_video(video=video_url, caption=title)
            elif info.get("ext") in ["jpg", "png"]:
                await update.message.reply_photo(photo=video_url, caption=title)
            else:
                await update.message.reply_text(f"{title}\n{video_url}")
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
