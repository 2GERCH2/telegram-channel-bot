import os
import sys
import logging

# Добавим путь для поиска библиотек
sys.path.append('/opt/render/project/src/.venv/lib/python3.9/site-packages')
sys.path.append('/opt/render/project/.venv/lib/python3.9/site-packages')

print("=" * 60)
print("🚀 ЗАПУСК ТЕЛЕГРАМ БОТА НА RENDER")
print("=" * 60)

# Проверяем Python и пути
print(f"Python версия: {sys.version}")
print(f"Python путь: {sys.executable}")
print(f"Пути поиска: {sys.path[:3]}...")

# Проверяем установленные библиотеки
try:
    import pkg_resources
    installed = [pkg.key for pkg in pkg_resources.working_set]
    print(f"Установленные библиотеки: {len(installed)}")
    if 'python-telegram-bot' in installed:
        print("✅ python-telegram-bot установлен")
    else:
        print("❌ python-telegram-bot НЕ установлен")
except:
    pass

# === НАСТРОЙКИ ===
TOKEN = "8323210618:AAHzr0pwt_5ed1EF38a6ZtSj4dYpVQuioEg"
SOURCE = -1001158045480
TARGET = -1003238172094

print(f"\n📋 КОНФИГУРАЦИЯ:")
print(f"   Токен: {TOKEN[:10]}...")
print(f"   Источник: {SOURCE}")
print(f"   Цель: {TARGET}")
print("=" * 60)

# === ПРОВЕРЯЕМ БИБЛИОТЕКУ ===
try:
    print("\n🔍 Проверяю библиотеку telegram...")
    from telegram.ext import Updater, MessageHandler, Filters
    print("✅ Библиотека telegram импортирована успешно!")
    
    # Проверяем версию
    import telegram
    print(f"   Версия: {telegram.__version__}")
    
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("\n📦 Пробую установить библиотеку через pip...")
    
    # Пробуем установить
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot==13.15"])
        print("✅ Установка завершена!")
        
        # Перезагружаем модули
        import importlib
        importlib.invalidate_caches()
        
        # Пробуем снова
        from telegram.ext import Updater, MessageHandler, Filters
        print("✅ Теперь библиотека загружается!")
        
    except Exception as install_error:
        print(f"💥 Ошибка установки: {install_error}")
        print("\n❌ Не могу продолжить. Проверьте файл requirements.txt")
        sys.exit(1)

# === ОСНОВНОЙ КОД ===
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def handle_channel_post(update, context):
    """Обрабатывает посты из канала"""
    if update.channel_post:
        post = update.channel_post
        if post.chat.id == SOURCE:
            logger.info(f"📨 Получен пост ID: {post.message_id}")
            try:
                # Копируем пост
                post.copy(chat_id=TARGET)
                logger.info("✅ Пост скопирован в LA LIGA HUB")
            except Exception as e:
                logger.error(f"❌ Ошибка копирования: {e}")

def main():
    """Запуск бота"""
    logger.info("🤖 Инициализирую бота...")
    
    try:
        # Создаем бота
        updater = Updater(token=TOKEN, use_context=True)
        dispatcher = updater.dispatcher
        
        # Добавляем обработчик
        dispatcher.add_handler(MessageHandler(Filters.chat_type.channel, handle_channel_post))
        
        logger.info("✅ Бот настроен. Запускаю polling...")
        
        # Запускаем
        updater.start_polling()
        logger.info("🎉 Бот запущен и работает!")
        logger.info("📡 Ожидаю сообщения из канала...")
        
        # Работаем до остановки
        updater.idle()
        
    except Exception as e:
        logger.error(f"💥 Критическая ошибка запуска: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
