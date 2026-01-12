import os
import sys
import logging
from threading import Thread

# === ПЕРВЫМ ДЕЛОМ ПРОВЕРЯЕМ ТОКЕН ===
print("🔍 ПРОВЕРКА ПЕРЕМЕННЫХ ОКРУЖЕНИЯ...")

# Способ 1: Попробуем получить из окружения
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Способ 2: Если не получилось, проверим по-другому
if not BOT_TOKEN:
    print("❌ BOT_TOKEN не найден в os.environ")
    print("   Пробую получить через getenv...")
    BOT_TOKEN = os.getenv('BOT_TOKEN')

# Способ 3: Если все еще нет, выведем ВСЕ переменные
if not BOT_TOKEN:
    print("⚠️  BOT_TOKEN все еще не найден!")
    print("   Все доступные переменные окружения:")
    for key, value in os.environ.items():
        print(f"   {key}: {'***скрыто***' if 'TOKEN' in key or 'SECRET' in key else value}")
    
    # Пробуем жестко закодировать для теста
    print("\n🔄 Использую токен напрямую для теста...")
    BOT_TOKEN = "8323210618:AAHzr0pwt_5ed1EF38a6ZtSj4dYpVQuioEg"
    
    if BOT_TOKEN:
        print(f"✅ Токен установлен: {BOT_TOKEN[:15]}...")
    else:
        print("💥 Критическая ошибка: токен не задан!")
        sys.exit(1)
else:
    print(f"✅ BOT_TOKEN найден: {BOT_TOKEN[:15]}...")

# ID каналов
try:
    SOURCE_CHANNEL_ID = int(os.getenv('SOURCE_CHANNEL_ID', '-1001158045480'))
    TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID', '-1003238172094'))
    print(f"✅ SOURCE_CHANNEL_ID: {SOURCE_CHANNEL_ID}")
    print(f"✅ TARGET_CHANNEL_ID: {TARGET_CHANNEL_ID}")
except Exception as e:
    print(f"❌ Ошибка ID каналов: {e}")
    sys.exit(1)

print("✅ Все проверки пройдены!")

# === FLASK ДЛЯ UPTIME ===
from flask import Flask
flask_app = Flask('')

@flask_app.route('/')
def home():
    return "🤖 Telegram Bot is running!"

@flask_app.route('/health')
def health():
    return {"status": "ok", "service": "telegram-bot"}

def run_flask():
    flask_app.run(host='0.0.0.0', port=8080, debug=False)

# === ТЕЛЕГРАМ БОТ ===
from telegram.ext import Application, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    stream=sys.stdout
)

logger = logging.getLogger(__name__)

async def handle_channel_post(update, context):
    if update.channel_post:
        post = update.channel_post
        if post.chat.id == SOURCE_CHANNEL_ID:
            logger.info(f"📨 Пост из {post.chat.title}: {post.message_id}")
            try:
                await post.copy(chat_id=TARGET_CHANNEL_ID)
                logger.info("✅ Скопировано в LA LIGA HUB")
            except Exception as e:
                logger.error(f"❌ Ошибка: {e}")

def main():
    logger.info("=" * 50)
    logger.info("🚀 ЗАПУСК ТЕЛЕГРАМ БОТА")
    logger.info(f"Токен: {BOT_TOKEN[:10]}...")
    logger.info("=" * 50)
    
    # Запускаем Flask в фоне
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("🌐 Flask запущен на порту 8080")
    
    # Запускаем Telegram бота
    try:
        app = Application.builder().token(BOT_TOKEN).build()
        app.add_handler(MessageHandler(filters.ChatType.CHANNEL, handle_channel_post))
        
        logger.info("✅ Telegram бот инициализирован")
        app.run_polling(drop_pending_updates=True)
    except Exception as e:
        logger.error(f"💥 Ошибка запуска бота: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()