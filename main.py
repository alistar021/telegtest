import os

# Switch to pyTelegramBotAPI (telebot) to avoid missing 'telegram' module error
try:
    import telebot
except ModuleNotFoundError:
    print("The 'telebot' module is not installed. Please install it using 'pip install pyTelegramBotAPI'")
    # Instead of exiting, stop execution gracefully
    telebot = None

if telebot:
    TOKEN = "8476998300:AAHrIH5HMc9TtXIHd-I8hH5MnDOGAkwMSlI"
    CHANNEL_ID = "@alialisend123"

    bot = telebot.TeleBot(TOKEN)
    user_data = {}

    @bot.message_handler(commands=['start'])
    def start(message):
        chat_id = message.chat.id
        bot.send_message(chat_id, "سلام! به ربات ما خوش آمدید.\nلطفا نام و نام خانوادگی خود را بفرستید.")
        user_data[chat_id] = {}

    @bot.message_handler(func=lambda m: m.text and m.chat.id in user_data and 'name' not in user_data[m.chat.id])
    def get_name(message):
        chat_id = message.chat.id
        user_data[chat_id]['name'] = message.text
        bot.send_message(chat_id, "لطفا شماره موبایل خود را وارد کنید.")

    @bot.message_handler(func=lambda m: m.text and m.chat.id in user_data and 'name' in user_data[m.chat.id] and 'phone' not in user_data[m.chat.id])
    def get_phone(message):
        chat_id = message.chat.id
        user_data[chat_id]['phone'] = message.text
        bot.send_message(chat_id, "لطفا عکس با کیفیت از انتخاب واحد خود ارسال کنید.")

    @bot.message_handler(content_types=['photo'])
    def get_photo(message):
        chat_id = message.chat.id
        if chat_id in user_data:
            file_id = message.photo[-1].file_id
            user_data[chat_id]['photo'] = file_id
            bot.send_message(chat_id, "با تشکر از شما، تیم فنی پس از بررسی شما را اضافه می‌کند.")
            bot.send_message(CHANNEL_ID, f"نام: {user_data[chat_id]['name']}\nشماره: {user_data[chat_id]['phone']}\nعکس انتخاب واحد: {file_id}")
            del user_data[chat_id]

    bot.infinity_polling()
