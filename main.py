import os
import requests
from flask import Flask, request, jsonify

TOKEN = os.getenv('TELEGRAM_TOKEN', 'YOUR_TOKEN_HERE')
CHANNEL_ID = os.getenv('CHANNEL_ID', '@yourchannel')

user_data = {}

app = Flask(__name__)

TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    url = f"{TELEGRAM_API}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(url, data=payload)

@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    update = request.get_json()

    if 'message' in update:
        chat_id = update['message']['chat']['id']

        # دریافت متن پیام
        if 'text' in update['message']:
            text = update['message']['text']

            if text == '/start':
                send_message(chat_id, "سلام! به ربات ما خوش آمدید.\nلطفا نام و نام خانوادگی خود را بفرستید.")
                user_data[chat_id] = {}
            elif chat_id in user_data and 'name' not in user_data[chat_id]:
                user_data[chat_id]['name'] = text
                send_message(chat_id, "لطفا شماره موبایل خود را وارد کنید.")
            elif chat_id in user_data and 'name' in user_data[chat_id] and 'phone' not in user_data[chat_id]:
                user_data[chat_id]['phone'] = text
                send_message(chat_id, "لطفا عکس با کیفیت از انتخاب واحد خود ارسال کنید.")

        # دریافت عکس
        elif 'photo' in update['message']:
            if chat_id in user_data:
                file_id = update['message']['photo'][-1]['file_id']
                user_data[chat_id]['photo'] = file_id

                send_message(chat_id, "با تشکر از شما، تیم فنی پس از بررسی شما را اضافه می‌کند.")
                # ارسال اطلاعات به کانال
                send_message(CHANNEL_ID,
                             f"📌 نام: {user_data[chat_id]['name']}\n"
                             f"📱 شماره: {user_data[chat_id]['phone']}\n"
                             f"🖼️ عکس انتخاب واحد: {file_id}")

                del user_data[chat_id]

    return jsonify({"ok": True})

if __name__ == "__main__":
    # روی Railway پورت را از ENV می‌گیرد
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)
