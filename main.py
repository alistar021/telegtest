import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# ======= تنظیمات =======
TOKEN = "8476998300:AAGxngE2JYli7AACp4RqGDWOdBFBh1QgUsM"
CHANNEL_ID = "@alialisend123"  # کانال عمومی
REGISTER_LINK = "https://t.me/YourFinalRegisterLink"  # لینک ثبت نهایی
GROUP_LINK = "https://t.me/azadborojerd"  # لینک گروه
# ========================

def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 سلام دوست عزیز!\n\nلطفاً *نام و نام خانوادگی* خودت رو برام بفرست 🙏",
                              parse_mode="Markdown")

def handle_text(update: Update, context: CallbackContext):
    user_data = context.user_data
    text = update.message.text

    if "name" not in user_data:
        user_data["name"] = text
        update.message.reply_text("📞 عالی! حالا لطفاً *شماره موبایل* خودت رو وارد کن:", parse_mode="Markdown")

    elif "phone" not in user_data:
        user_data["phone"] = text
        update.message.reply_text("🆔 خوبه! حالا *آی‌دی تلگرام*ت رو (با @) بفرست:", parse_mode="Markdown")

    elif "telegram_id" not in user_data:
        user_data["telegram_id"] = text
        update.message.reply_text("🖼️ لطفاً یک *عکس کارت ملی یا مدرک معتبر* بفرست:", parse_mode="Markdown")

    else:
        update.message.reply_text("⚠️ لطفاً عکس کارت ملی یا مدرک معتبر خود را ارسال کنید.")

def handle_photo(update: Update, context: CallbackContext):
    user_data = context.user_data
    photo_file = update.message.photo[-1].get_file()

    caption = (
        f"👤 نام: {user_data.get('name')}\n"
        f"📞 شماره: {user_data.get('phone')}\n"
        f"🆔 آی‌دی: {user_data.get('telegram_id')}"
    )

    # ارسال به کانال
    photo_file.download("temp.jpg")
    context.bot.send_photo(chat_id=CHANNEL_ID, photo=open("temp.jpg", "rb"), caption=caption)

    # دکمه ثبت نهایی
    keyboard = [[InlineKeyboardButton("✅ ثبت نهایی", callback_data="final_register")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("🎉 اطلاعاتت ثبت شد! برای تکمیل ثبت‌نام روی دکمه زیر بزن:",
                              reply_markup=reply_markup)

    # پاک کردن داده‌ها بعد از ارسال
    user_data.clear()

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "final_register":
        query.edit_message_text("✅ اطلاعات شما با موفقیت ثبت شد.")
        context.bot.send_message(chat_id=query.message.chat_id,
                                 text=f"📌 برای ادامه به این گروه بپیوندید:\n{GROUP_LINK}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    dp.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
