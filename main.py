from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging

# ======= تنظیمات =======
TOKEN = "8476998300:AAGY2UnyUcrhm29IBvg8BYyCXgRxy73GvVY"
CHANNEL_ID = "@alialisend123"
# لینک کانال نهایی که بعد از ثبت برای کاربر فرستاده میشه
FINAL_LINK = "https://t.me/azadborojerd"
# ========================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 سلام دوست عزیز!\n\nلطفاً *نام و نام خانوادگی* خودت رو برام بفرست 🙏",
        parse_mode="Markdown"
    )

def handle_text(update: Update, context: CallbackContext):
    user_data = context.user_data
    if "name" not in user_data:
        user_data["name"] = update.message.text
        # اسم کاربر در پیام شماره موبایل استفاده میشه
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
        keyboard = [[InlineKeyboardButton("✅ ثبت نهایی", callback_data="final_click")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "🎉 اطلاعات شما ثبت شد! برای ثبت نهایی روی دکمه زیر کلیک کنید:", 
            reply_markup=reply_markup
        )

    except Exception as e:
        logging.error(f"Error sending photo: {e}")
        update.message.reply_text("❌ مشکلی پیش آمد! لطفاً دوباره امتحان کنید.", parse_mode="Markdown")

# مدیریت کلیک روی دکمه شیشه‌ای
def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    # پیام بعدی با لینک کانال نهایی
    query.message.reply_text(
        f"🙏 ممنون از این که ما را در ارائه خدمات بهتر دانشجویی یاری می‌کنید.\n"
        f"💬 مارا در تریبون دانشگاه آزاد بروجرد دنبال کنید.\n\n"
        f"🎓 لینک کانال: {FINAL_LINK}"
    )
    # پاک کردن داده‌های کاربر
    context.user_data.clear()

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    dp.add_handler(MessageHandler(Filters.command, lambda u, c: None))  # جلوگیری از خطای دیگر دستورها
    
    # اضافه کردن CallbackQueryHandler برای دکمه شیشه‌ای
    from telegram.ext import CallbackQueryHandler
    dp.add_handler(CallbackQueryHandler(button_click))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
