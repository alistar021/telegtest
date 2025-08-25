from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging

# ======= تنظیمات =======
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"   # توکن ربات
CHANNEL_ID = "@alialisend123"       # آیدی کانال
REGISTER_LINK = "https://t.me/YourFinalRegisterLink"  # لینک ثبت نهایی
# ========================

# تنظیمات لاگ
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! لطفاً نام و نام خانوادگی خود را ارسال کنید:")

def handle_text(update: Update, context: CallbackContext):
    user_data = context.user_data
    if "name" not in user_data:
        user_data["name"] = update.message.text
        update.message.reply_text("لطفاً شماره موبایل خود را ارسال کنید:")
    elif "phone" not in user_data:
        user_data["phone"] = update.message.text
        update.message.reply_text("لطفاً عکس دانشجویی یا انتخاب واحد را ارسال کنید:")
    else:
        update.message.reply_text("لطفاً عکس دانشجویی یا انتخاب واحد را ارسال کنید.")

def handle_photo(update: Update, context: CallbackContext):
    user_data = context.user_data
    try:
        photo_file = update.message.photo[-1].get_file()
        caption = f"نام: {user_data.get('name')}\nشماره: {user_data.get('phone')}"
        
        photo_file.download("temp.jpg")
        context.bot.send_photo(chat_id=CHANNEL_ID, photo=open("temp.jpg", "rb"), caption=caption)

        keyboard = [[InlineKeyboardButton("ثبت نهایی", url=REGISTER_LINK)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text("اطلاعات شما ثبت شد ✅ برای ثبت نهایی روی دکمه کلیک کنید:", reply_markup=reply_markup)
