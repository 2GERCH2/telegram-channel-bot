import os
import sys
import logging
from threading import Thread

# === ПРОВЕРКА ПЕРЕМЕННЫХ ===
print("🔍 ПРОВЕРКА ПЕРЕМЕННЫХ...")

BOT_TOKEN = os.getenv('BOT_TOKEN', "8323210618:AAHzr0pwt_5ed1EF38a6ZtSj4dYpVQuioEg")
SOURCE_CHANNEL_ID = int(os.getenv('SOURCE_CHANNEL_ID', '-1001158045480'))
TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID', '-1003238172094'))

print(f"✅ Токен: {BOT_TOKEN[:15]}...")
print(f"✅ Источник: {SOURCE_CHANNEL_ID}")
print(f"✅ Цель: {TARGET_CHANNEL_ID}")

# === FLASK ДЛЯ ПИНГОВ ===
from flask import Flask
flask_app = Flask('')

@flask_app.route('/')
def home():
    return "🤖 Telegram Bot Active"

@flask_app.route('/ping')
def ping():
    return "pong"

def run_flask():
    flask_app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)

# Запускаем Flask сразу в отдельном потоке
flask_thread = Thread(target=run_flask, daemon=True)
flask_thread.start()
print("🌐 Flask запущен на порту 8080")

# === ТЕЛЕГРАМ БОТ (СОВМЕСТИМАЯ ВЕРСИЯ) ===
try:
    # Попробуем импорт для python-telegram-bot 20.x
    from telegram.ext import Application, MessageHandler, filters
    from telegram import Update
    from telegram.ext import ContextTypes
    
    print("✅ Использую python-telegram-bot 20.x")
    
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.channel_post:
            post = update.channel_post
            if post.chat.id == SOURCE_CHANNEL_ID:
                print(f"📨 Пост из канала: {post.message_id}")
                try:
                    await post.copy(chat_id=TARGET_CHANNEL_ID)
                    print("✅ Пост скопирован в LA LIGA HUB")
                except Exception as e:
                    print(f"❌ Ошибка: {e}")
    
    async def main():
        print("🚀 Запускаю Telegram бота...")
        
        application = Application.builder().token(BOT_TOKEN).build()
        application.add_handler(MessageHandler(filters.ChatType.CHANNEL, handle_message))
        
        print("✅ Бот запущен, ожидаю сообщения...")
        await application.run_polling(drop_pending_updates=True)
    
    import asyncio
    asyncio.run(main())
    
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("Пробую старую версию...")
    
    try:
        # Для python-telegram-bot 13.x
        from telegram.ext import Updater, MessageHandler, Filters
        
        print("✅ Использую python-telegram-bot 13.x")
        
        def handle_message(update, context):
            if update.channel_post:
                post = update.channel_post
                if post.chat.id == SOURCE_CHANNEL_ID:
                    print(f"📨 Пост из канала: {post.message_id}")
                    try:
                        post.copy(chat_id=TARGET_CHANNEL_ID)
                        print("✅ Пост скопирован в LA LIGA HUB")
                    except Exception as e:
                        print(f"❌ Ошибка: {e}")
        
        updater = Updater(BOT_TOKEN, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(MessageHandler(Filters.chat_type.channel, handle_message))
        
        print("🚀 Запускаю бота...")
        updater.start_polling(drop_pending_updates=True)
        updater.idle()
        
    except Exception as e2:
        print(f"💥 Критическая ошибка: {e2}")
        sys.exit(1)