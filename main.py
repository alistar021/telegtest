import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# ======= تنظیمات =======
TOKEN = os.getenv("TELEGRAM_TOKEN")  # توکن ربات از Environment Variable
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # آیدی کانال از Environment Variable
REGISTER_LINK = os.getenv("REGISTER_LINK")  # لینک ثبت نهایی از Environment Variable
# ========================

def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! لطفاً نام و نام خانوادگی خود را ارسال کنید:")

def handle_text(update: Update, context: CallbackContext):
    user_data = context.user_data
    if "name" not in user_data:
        user_data["name"] = update.message.text
        update.message.reply_text("لطفاً شماره موبایل خود را ارسال کنید:")
    elif "phone" not in user_data:
        user_data["phone"] = update.message.text
        update.message.reply_text("لطفاً عکس کارت ملی خود را ارسال کنید:")
    else:
        update.message.reply_text("لطفاً عکس کارت ملی خود را ارسال کنید.")

def handle_photo(update: Update, context: CallbackContext):
    user_data = context.user_data
    photo_file = update.message.photo[-1].get_file()
    caption = f"نام: {user_data.get('name')}\nشماره: {user_data.get('phone')}"
    
    # فوروارد به کانال خصوصی
    photo_file.download("temp.jpg")
    context.bot.send_photo(chat_id=CHANNEL_ID, photo=open("temp.jpg", "rb"), caption=caption)
    
    # دکمه ثبت نهایی
    keyboard = [[InlineKeyboardButton("ثبت نهایی", url=REGISTER_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "اطلاعات شما ثبت شد! برای ثبت نهایی روی دکمه زیر کلیک کنید:", 
        reply_markup=reply_markup
    )
    
    # پاک کردن داده‌ها
    user_data.clear()

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
