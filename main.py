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

        # پیام تشکر نهایی + اطلاع‌رسانی رسمی
        update.message.reply_text(
            "🙏 ممنون از این که ما را در ارائه خدمات بهتر دانشجویی یاری می‌کنید.\n"
            "💬 مارا در تریبون دانشگاه آزاد بروجرد دنبال کنید.\n\n"
            "🎓 تیم فنی پس از بررسی اطلاعات شما، به صورت رسمی شما را وارد گروه خواهند کرد.",
            parse_mode="Markdown"
        )

        # پاک کردن داده‌ها
        user_data.clear()

    except Exception as e:
        logging.error(f"Error sending photo: {e}")
        update.message.reply_text("❌ مشکلی پیش آمد! لطفاً دوباره امتحان کنید.", parse_mode="Markdown")
