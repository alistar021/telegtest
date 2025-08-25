import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from flask import Flask

# ======= تنظیمات =======
TOKEN = "8476998300:AAGxngE2JYli7AACp4RqGDWOdBFBh1QgUsM"  # توکن ربات شما
CHANNEL_ID = "@alialisend123"  # آیدی کانال
REGISTER_LINK = "https://t.me/YourFinalRegisterLink"  # لینک ثبت نهایی
# ========================

# لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# دیتای کاربر
user_data_dict = {}

# ======= ربات تلگرام =======
def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_data_dict[chat_id] = {}
    update.message.reply_text("سلام! لطفاً نام و نام خانوادگی خود را ارسال کنید:")

def handle_text(update: Update, context: CallbackContext):
    c
