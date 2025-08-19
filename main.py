import telebot

TOKEN = "8476998300:AAHrIH5HMc9TtXIHd-I8hH5MnDOGAkwMSlI"
CHANNEL_ID = "@alialisend123"
REGISTER_LINK = "https://t.me/azadborojerd"

bot = telebot.TeleBot(TOKEN)

# دیکشنری برای ذخیره موقت داده‌های کاربران
user_data = {}

# شروع ربات
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id, 
        f"سلام به ربات ما خوش آمدید! لطفا نام و نام خانوادگی خود را وارد کنید.\nبرای ثبت‌نام رسمی: {REGISTER_LINK}"
    )
    user_data[message.chat.id] = {}
    bot.register_next_step_handler(message, get_name)

# دریافت نام و نام خانوادگی
def get_name(message):
    user_data[message.chat.id]['name'] = message.text
    bot.send_message(message.chat.id, "لطفا شماره موبایل خود را وارد کنید:")
    bot.register_next_step_handler(message, get_phone)

# دریافت شماره موبایل
def get_phone(message):
    user_data[message.chat.id]['phone'] = message.text
    bot.send_message(message.chat.id, "لطفا یک عکس باکیفیت از انتخاب واحد خود ارسال کنید:")
    bot.register_next_step_handler(message, get_photo)

# دریافت عکس
def get_photo(message):
    if message.content_type == 'photo':
        file_id = message.photo[-1].file_id
        user_data[message.chat.id]['photo'] = file_id
        bot.send_message(message.chat.id, "با تشکر از شما، تیم فنی پس از بررسی شما را اد می‌کند.")
        
        # ارسال داده‌ها به کانال
        name = user_data[message.chat.id]['name']
        phone = user_data[message.chat.id]['phone']
        bot.send_message(CHANNEL_ID, f"✅ درخواست جدید از کاربر:\n\n👤 نام و نام خانوادگی: {name}\n📞 شماره موبایل: {phone}")
        bot.send_photo(CHANNEL_ID, file_id, caption=f"عکس انتخاب واحد از {name}")
        
        # پاک کردن داده‌های موقت
        user_data.pop(message.chat.id, None)
    else:
        bot.send_message(message.chat.id, "لطفا یک عکس ارسال کنید.")
        bot.register_next_step_handler(message, get_photo)

# اجرای ربات
bot.infinity_polling()
