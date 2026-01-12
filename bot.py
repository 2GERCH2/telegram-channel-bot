import os
import sys
import logging
from threading import Thread

# === НАСТРОЙКА ЛОГИРОВАНИЯ ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

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

# Запускаем Flask в отдельном потоке
flask_thread = Thread(target=run_flask, daemon=True)
flask_thread.start()
print("🌐 Flask запущен на порту 8080")

# === ТЕЛЕГРАМ БОТ (python-telegram-bot 13.x) ===
try:
    from telegram.ext import Updater, MessageHandler, Filters
    
    print("✅ Использую python-telegram-bot 13.x")
    
    def handle_message(update, context):
        logger.info(f"Получено обновление: {update}")
        
        if update.channel_post:
            post = update.channel_post
            logger.info(f"Пост из канала {post.chat.id}: {post.message_id}")
            
            if post.chat.id == SOURCE_CHANNEL_ID:
                print(f"📨 Пост из канала-источника: {post.message_id}")
                try:
                    # Пробуем скопировать пост
                    post.copy(chat_id=TARGET_CHANNEL_ID)
                    print("✅ Пост скопирован в целевой канал")
                except Exception as e:
                    print(f"❌ Ошибка при копировании: {e}")
                    logger.error(f"Ошибка при копировании: {e}")
            else:
                print(f"📭 Пост из другого канала (не источник): {post.chat.id}")
    
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.chat_type.channel, handle_message))
    
    print("🚀 Запускаю бота...")
    updater.start_polling(drop_pending_updates=True)
    print("✅ Бот запущен, ожидаю сообщения...")
    updater.idle()
    
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    sys.exit(1)
except Exception as e:
    print(f"💥 Критическая ошибка: {e}")
    sys.exit(1)
