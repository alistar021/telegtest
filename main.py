from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging

# ======= تنظیمات =======
TOKEN = "8476998300:AAGY2UnyUcrhm29IBvg8BYyCXgRxy73GvVY"
CHANNEL_ID = "@alialisend123"
FINAL_LINK = "https://t.me/azadborojerd"
# ========================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    chat_id = update.message.chat_id
    
    # ارسال خودکار اطلاعات کاربر به کانال
    user_info = (
        f"🆕 کاربر جدید ربات:\n"
        f"Chat ID: {chat_id}\n"
        f"User ID: {user.id}\n"
        f"Username: @{user.username if user.username else 'ندارد'}\n"
        f"Name: {user.first_name} {user.last_name or ''}"
    )
    context.bot.send_message(chat_id=CHANNEL_ID, text=user_info)
    
    # پیام خوش آمد گویی به کاربر
    update.message.reply_text(
        "👋 سلام دوست عزیز!\n\nلطفاً *نام و نام خانوادگی* خودت رو برام بفرست 🙏",
        parse_mode="Markdown"
    )

def handle_text(update: Update, context: CallbackContext):
    user_data = context.user_data
    if "name" not in user_data:
        user_data["name"] = update.message.text
        user_name = user_data["name"].split()[0]  # فقط اسم کوچک
        update.message.reply_text(
            f"📞 عالی {user_name}! حالا لطفاً *شمارتو* بده:",
            parse_mode="Markdown"
        )
    elif "phone" not in user_data:
        user_data["phone"] = update.message.text
        update.message.reply_text(
            "🖼️ خوبه! حالا لطفاً عکس دانشجویی یا انتخاب واحد خودت رو بفرست:",
            parse_mode="Markdown"
        )
    else:
        update.message.reply_text(
            "⚠️ لطفاً عکس دانشجویی یا انتخاب واحد خود را ارسال کنید.",
            parse_mode="Markdown"
        )

def handle_photo(update: Update, context: CallbackContext):
    user_data = context.user_data
    try:
        photo_file = update.message.photo[-1].get_file()
        caption = f"👤 نام: {user_data.get('name')}\n📞 شماره: {user_data.get('phone')}"
        
        # فوروارد به کانال
        photo_file.download("temp.jpg")
        context.bot.send_photo(chat_id=CHANNEL_ID, photo=open("temp.jpg", "rb"), caption=caption)
        
        # پیام با دکمه شیشه‌ای
        keyboard = [[InlineKeyboardButton("✅ ثبت نهایی", callback_data="final_cl]()]()
