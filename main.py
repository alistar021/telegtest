from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# توکن ربات
BOT_TOKEN = "8476998300:AAGxngE2JYli7AACp4RqGDWOdBFBh1QgUsM"

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! ربات شما آماده به کار است ✅")

# دستور /id برای گرفتن آیدی کاربر
async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(f"آیدی تلگرام شما: {user_id}")

# دستور /help برای نمایش لیست دستورات
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📌 لیست دستورات ربات:\n\n"
        "/start - شروع ربات\n"
        "/id - دریافت آیدی عددی شما\n"
        "/help - نمایش این راهنما\n"
    )
    await update.message.reply_text(help_text)

if __name__ == "__main__":
    # ساخت اپلیکیشن
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # اضافه کردن دستورها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", get_id))
    app.add_handler(CommandHandler("help", help_command))

    # اجرای ربات
    print("ربات در حال اجراست...")
    app.run_polling()
