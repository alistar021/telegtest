from telegram import Update, Bot, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

# ==== تنظیمات ربات ====
TOKEN = "8476998300:AAHrIH5HMc9TtXIHd-I8hH5MnDOGAkwMSlI"
CHANNEL_ID = "@alialisend123"

# مراحل دریافت اطلاعات
NAME, PHONE, PHOTO = range(3)

# دیکشنری برای ذخیره موقت داده‌ها
user_data = {}

# --- دستور /start ---
def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id, "سلام به ربات ما خوش آمدید! لطفا نام و نام خانوادگی خود را وارد کنید:")
    return NAME

# --- دریافت نام ---
def get_name(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_data[chat_id] = {}
    user_data[chat_id]['name'] = update.message.text
    context.bot.send_message(chat_id, "لطفا شماره موبایل خود را وارد کنید:")
    return PHONE

# --- دریافت شماره موبایل ---
def get_phone(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_data[chat_id]['phone'] = update.message.text
    context.bot.send_message(chat_id, "لطفا یک عکس باکیفیت از انتخاب واحد خود ارسال کنید:")
    return PHOTO

# --- دریافت عکس ---
def get_photo(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        user_data[chat_id]['photo'] = file_id

        # پیام تشکر به کاربر
        context.bot.send_message(chat_id, "با تشکر از شما، تیم فنی پس از بررسی شما را اد می‌کند.")

        # ارسال به کانال
        name = user_data[chat_id]['name']
        phone = user_data[chat_id]['phone']
        context.bot.send_message(
            CHANNEL_ID,
            f"✅ درخواست جدید:\n\n👤 نام: {name}\n📞 شماره: {phone}"
        )
        context.bot.send_photo(CHANNEL_ID, file_id, caption=f"عکس انتخاب واحد از {name}")

        # پاک کردن داده‌های کاربر
        user_data.pop(chat_id, None)
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id, "لطفا یک عکس ارسال کنید.")
        return PHOTO

# --- لغو ---
def cancel(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_data.pop(chat_id, None)
    context.bot.send_message(chat_id, "عملیات لغو شد.")
    return ConversationHandler.END

# ==== اجرای ربات ====
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # ConversationHandler برای مدیریت مراحل
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
            PHONE: [MessageHandler(Filters.text & ~Filters.command, get_phone)],
            PHOTO: [MessageHandler(Filters.photo, get_photo)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    print("ربات در حال اجراست...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
