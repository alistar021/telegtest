from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging

# ======= تنظیمات =======
TOKEN = "8476998300:AAGY2UnyUcrhm29IBvg8BYyCXgRxy73GvVY"  # توکن ربات شما
CHANNEL_ID = "@alialisend123"  # آیدی کانال عمومی
REGISTER_LINK = "https://t.me/YourFinalRegisterLink"  # لینک ثبت نهایی
# ========================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 سلام دوست عزیز!\n\nلطفاً *نام و نام خانوادگی* خودت رو برام بفرست 🙏",
                              parse_mode="Markdown")

def handle_text(update: Update, context: CallbackContext):
    user_data = context.user_data
    if "name" not in user_data:
        user_data["name"] = update.message.text
        update.message.reply_text("📞 عالی! حالا لطفاً *شماره موبایل* خودت رو وارد کن:", parse_mode="Markdown")
    elif "phone" not in user_data:
        user_data["phone"] = update.message.text
        update.message.reply_text("🖼️ خوبه! حالا لطفاً عکس دانشجویی یا انتخاب واحد خودت رو بفرست:", parse_mode="Markdown")
    else:
        update.message.reply_text("⚠️ لطفاً عکس دانشجویی یا انتخاب واحد خود را ارسال کنید.", parse_mode="Markdown")

def handle_photo(update: Update, context: CallbackContext):
    user_data = context.user_data
    try:
        photo_file = update.message.photo[-1].get_file()
        caption = f"👤 نام: {user_data.get('name')}\n📞 شماره: {user_data.get('phone')}"
        
        # فوروارد به کانال
        photo_file.download("temp.jpg")
        context.bot.send_photo(chat_id=CHANNEL_ID, photo=open("temp.jpg", "rb"), caption=caption)
        
        # دکمه ثبت نهایی
        keyboard = [[InlineKeyboardButton("✅ ثبت نهایی", url=REGISTER_LINK)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "🎉 اطلاعات شما ثبت شد! برای ثبت نهایی روی دکمه زیر کلیک کنید:", 
            reply_markup=reply_markup
        )

        update.message.reply_text(
            "🙏 ممنون از این که ما را در ارائه خدمات بهتر دانشجویی یاری می‌کنید.\n"
            "💬 مارا در تریبون دانشگاه آزاد بروجرد دنبال کنید.\n\n"
            "🎓 تیم فنی پس از بررسی اطلاعات شما، به صورت رسمی شما را وارد گروه خواهند کرد.",
            parse_mode="Markdown"
        )

        user_data.clear()

    except Exception as e:
        logging.error(f"Error sending photo: {e}")
        update.message.reply_text("❌ مشکلی پیش آمد! لطفاً دوباره امتحان کنید.", parse_mode="Markdown")

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
