import os
import sys

print("=" * 50)
print("🚀 ЗАПУСК ПРОСТОГО ТЕЛЕГРАМ БОТА")
print("=" * 50)

# Настройки
TOKEN = "8323210618:AAHzr0pwt_5ed1EF38a6ZtSj4dYpVQuioEg"
SOURCE = -1001158045480
TARGET = -1003238172094

print(f"Токен: {TOKEN[:10]}...")
print(f"Канал-источник: {SOURCE}")
print(f"Целевой канал: {TARGET}")
print("=" * 50)

try:
    # Пробуем версию 13.x
    from telegram.ext import Updater, MessageHandler, Filters
    
    print("✅ Использую python-telegram-bot 13.x")
    
    def handle_message(update, context):
        if update.channel_post:
            post = update.channel_post
            if post.chat.id == SOURCE:
                print(f"📨 Получен пост ID: {post.message_id}")
                try:
                    # Копируем пост
                    post.copy(chat_id=TARGET)
                    print("✅ Пост скопирован в LA LIGA HUB")
                except Exception as e:
                    print(f"❌ Ошибка: {e}")
    
    # Запускаем бота
    updater = Updater(TOKEN, use_context=True)
    updater.dispatcher.add_handler(MessageHandler(Filters.chat_type.channel, handle_message))
    
    print("🤖 Бот запущен. Ожидаю сообщения...")
    updater.start_polling()
    updater.idle()
    
except ImportError:
    print("❌ Библиотека python-telegram-bot не установлена")
    print("Установите: pip install python-telegram-bot==13.15")
    sys.exit(1)
except Exception as e:
    print(f"💥 Ошибка: {e}")
    sys.exit(1)
