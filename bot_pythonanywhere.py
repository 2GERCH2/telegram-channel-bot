import os
import logging
import sys
from telegram.ext import Application, MessageHandler, filters

# === НАСТРОЙКИ ИЗ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ ===
BOT_TOKEN = os.getenv('8323210618:AAHzr0pwt_5ed1EF38a6ZtSj4dYpVQuioEg')
SOURCE_CHANNEL_ID = int(os.getenv('SOURCE_CHANNEL_ID', '-1001158045480'))
TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID', '-1003238172094'))

# === НАСТРОЙКА ЛОГИРОВАНИЯ ДЛЯ RENDER ===
logging.basicConfig(
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

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

def main():
    """Запуск бота на Render"""
    logger.info("=" * 50)
    logger.info("🚀 ТЕЛЕГРАМ БОТ ЗАПУЩЕН НА RENDER")
    logger.info(f"📡 Канал-источник: {SOURCE_CHANNEL_ID}")
    logger.info(f"🎯 Целевой канал: {TARGET_CHANNEL_ID}")
    logger.info(f"🆔 ID процесса: {os.getpid()}")
    logger.info("=" * 50)
    
    # Создаем приложение
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчик
    app.add_handler(MessageHandler(filters.ChatType.CHANNEL, handle_channel_post))
    
    # Уменьшаем лишние логи
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("apscheduler").setLevel(logging.WARNING)
    
    # Запускаем бота
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
