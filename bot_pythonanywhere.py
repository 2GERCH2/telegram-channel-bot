import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
from telegram.constants import ParseMode

# === НАСТРОЙКИ ===
SOURCE_CHANNEL_ID = -1001158045480  # Яндекс проекты
TARGET_CHANNEL_ID = -1003238172094  # LA LIGA HUB
BOT_TOKEN = "8323210618:AAHzr0pwt_5ed1EF38a6ZtSj4dYpVQuioEg"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def copy_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Создает копию поста в целевом канале"""
    if update.channel_post:
        post = update.channel_post
        
        # Проверяем, что это наш канал-источник
        if post.chat.id != SOURCE_CHANNEL_ID:
            return
        
        logger.info(f"📨 Получен пост из Яндекс проекты (ID: {post.message_id})")
        
        try:
            # В зависимости от типа контента создаем копию
            
            # 1. Текстовое сообщение
            if post.text:
                await context.bot.send_message(
                    chat_id=TARGET_CHANNEL_ID,
                    text=post.text,
                    entities=post.entities,
                    parse_mode=ParseMode.HTML if post.text_html else None
                )
                logger.info("✅ Создана копия текстового поста")
            
            # 2. Фото с подписью или без
            elif post.photo:
                await context.bot.send_photo(
                    chat_id=TARGET_CHANNEL_ID,
                    photo=post.photo[-1].file_id,  # Берем самую большую версию фото
                    caption=post.caption,
                    caption_entities=post.caption_entities,
                    parse_mode=ParseMode.HTML if post.caption_html else None
                )
                logger.info("✅ Создана копия фото")
            
            # 3. Видео
            elif post.video:
                await context.bot.send_video(
                    chat_id=TARGET_CHANNEL_ID,
                    video=post.video.file_id,
                    caption=post.caption,
                    caption_entities=post.caption_entities,
                    parse_mode=ParseMode.HTML if post.caption_html else None
                )
                logger.info("✅ Создана копия видео")
            
            # 4. Документы
            elif post.document:
                await context.bot.send_document(
                    chat_id=TARGET_CHANNEL_ID,
                    document=post.document.file_id,
                    caption=post.caption,
                    caption_entities=post.caption_entities,
                    parse_mode=ParseMode.HTML if post.caption_html else None
                )
                logger.info("✅ Создана копия документа")
            
            # 5. Группы медиа (альбомы)
            elif post.media_group_id:
                logger.info("⏭️ Пропускаем медиагруппу (альбом)")
                # Для альбомов нужна отдельная логика
            
            # 6. Стикеры
            elif post.sticker:
                await context.bot.send_sticker(
                    chat_id=TARGET_CHANNEL_ID,
                    sticker=post.sticker.file_id
                )
                logger.info("✅ Создана копия стикера")
            
            # 7. Голосовые сообщения
            elif post.voice:
                await context.bot.send_voice(
                    chat_id=TARGET_CHANNEL_ID,
                    voice=post.voice.file_id,
                    caption=post.caption
                )
                logger.info("✅ Создана копия голосового сообщения")
            
            # 8. Аудио
            elif post.audio:
                await context.bot.send_audio(
                    chat_id=TARGET_CHANNEL_ID,
                    audio=post.audio.file_id,
                    caption=post.caption,
                    caption_entities=post.caption_entities
                )
                logger.info("✅ Создана копия аудио")
            
            else:
                logger.warning(f"⚠️ Неподдерживаемый тип контента: {post}")
                
        except Exception as e:
            logger.error(f"❌ Ошибка при создании копии: {type(e).__name__}: {e}")

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Тестовая команда"""
    await update.message.reply_text(
        "🤖 Бот для копирования постов работает!\n"
        "Создайте пост в 'Яндекс проекты' и он появится в 'LA LIGA HUB'"
    )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Проверка статуса"""
    try:
        # Проверяем доступ к каналам
        source_chat = await context.bot.get_chat(SOURCE_CHANNEL_ID)
        target_chat = await context.bot.get_chat(TARGET_CHANNEL_ID)
        
        await update.message.reply_text(
            f"📊 Статус бота:\n\n"
            f"✅ Канал-источник: {source_chat.title}\n"
            f"✅ Целевой канал: {target_chat.title}\n"
            f"🤖 Бот готов к работе!"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"💥 Ошибка: {context.error}")

def main():
    """Запуск бота"""
    logger.info("🚀 Запускаю бота для КОПИРОВАНИЯ постов...")
    logger.info(f"   Источник: {SOURCE_CHANNEL_ID}")
    logger.info(f"   Цель: {TARGET_CHANNEL_ID}")
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Обработчик сообщений из каналов
    app.add_handler(MessageHandler(filters.ChatType.CHANNEL, copy_channel_post))
    
    # Команды
    app.add_handler(CommandHandler("start", test_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("test", test_command))
    
    # Обработчик ошибок
    app.add_error_handler(error_handler)
    
    # Уменьшаем логирование httpx
    logging.getLogger("httpx").setLevel(logging.WARNING)
    
    logger.info("✅ Бот запущен. Создайте пост в 'Яндекс проекты'...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
