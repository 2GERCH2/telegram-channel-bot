import os
import logging
import sys
from threading import Thread

# === FLASK ДЛЯ ПОДДЕРЖАНИЯ АКТИВНОСТИ НА RENDER ===
from flask import Flask
app = Flask('')

@app.route('/')
def home():
    return "🤖 Telegram Bot is running!"

def run_flask():
    """Запускает Flask сервер в отдельном потоке"""
    app.run(host='0.0.0.0', port=8080)

# === НАСТРОЙКИ ТЕЛЕГРАМ БОТА ===
from telegram.ext import Application, MessageHandler, filters

# Получаем настройки из переменных окружения Render
BOT_TOKEN = os.getenv('8323210618:AAHzr0pwt_5ed1EF38a6ZtSj4dYpVQuioEg')
SOURCE_CHANNEL_ID = int(os.getenv('SOURCE_CHANNEL_ID', '-1001158045480'))
TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID', '-1003238172094'))

# === НАСТРОЙКА ЛОГИРОВАНИЯ ===
logging.basicConfig(
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# === ОБРАБОТЧИК ТЕЛЕГРАМ ===
async def handle_channel_post(update, context):
    """Обрабатывает посты из канала-источника"""
    if update.channel_post:
        post = update.channel_post
        
        # Проверяем, что это наш канал-источник
        if post.chat.id == SOURCE_CHANNEL_ID:
            logger.info(f"📨 Получен пост ID: {post.message_id}")
            
            try:
                # Создаем копию поста
                await post.copy(chat_id=TARGET_CHANNEL_ID)
                logger.info("✅ Пост успешно скопирован в LA LIGA HUB")
            except Exception as e:
                logger.error(f"❌ Ошибка: {e}")

# === ОСНОВНАЯ ФУНКЦИЯ ===
def main():
    """Запуск бота на Render"""
    logger.info("=" * 50)
    logger.info("🚀 ТЕЛЕГРАМ БОТ ЗАПУЩЕН НА RENDER")
    logger.info("🌐 Flask сервер запущен на порту 8080")
    logger.info(f"📡 Канал-источник: {SOURCE_CHANNEL_ID}")
    logger.info(f"🎯 Целевой канал: {TARGET_CHANNEL_ID}")
    logger.info("=" * 50)
    
    # Запускаем Flask в отдельном потоке
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("✅ Flask запущен в фоновом режиме")
    
    # Создаем и запускаем Telegram бота
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ChatType.CHANNEL, handle_channel_post))
    
    # Уменьшаем лишние логи
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("apscheduler").setLevel(logging.WARNING)
    
    # Запускаем Telegram бота
    logger.info("✅ Telegram бот запущен")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
