import asyncio
from telegram import Bot
from telegram.error import TelegramError

TELEGRAM_TOKEN = "7638129033:AAEYmXQikS0qa-qJ-Roxp3Wg7HLEQH9f-ao"
CHANNEL_ID = "-1002719144496"

async def clear_channel_history():
    """Очищает всю историю сообщений в канале"""
    bot = Bot(token=TELEGRAM_TOKEN)
    
    try:
        print("🔍 Начинаю очистку канала...")
        
        # Получаем информацию о канале
        chat = await bot.get_chat(CHANNEL_ID)
        print(f"📢 Канал: {chat.title}")
        
        # Попробуем удалить сообщения по ID (начиная с последних)
        deleted_count = 0
        consecutive_not_found = 0  # Счетчик подряд не найденных сообщений
        max_consecutive_not_found = 50  # Если 50 сообщений подряд не найдено - завершаем
        
        msg_id = 1
        while msg_id <= 10000:  # Максимальный лимит
            try:
                await bot.delete_message(chat_id=CHANNEL_ID, message_id=msg_id)
                deleted_count += 1
                consecutive_not_found = 0  # Сбрасываем счетчик при успешном удалении
                
                if deleted_count % 10 == 0:
                    print(f"🗑️ Удалено {deleted_count} сообщений...")
                await asyncio.sleep(0.1)  # Небольшая задержка
                
            except TelegramError as e:
                # Если сообщение не найдено
                if "message to delete not found" in str(e).lower():
                    consecutive_not_found += 1
                    if consecutive_not_found >= max_consecutive_not_found:
                        print(f"✅ Больше сообщений не найдено после {consecutive_not_found} попыток")
                        break
                elif "message can't be deleted" in str(e).lower():
                    print(f"⚠️ Сообщение {msg_id} не может быть удалено (возможно, слишком старое)")
                    consecutive_not_found += 1
                    if consecutive_not_found >= max_consecutive_not_found:
                        print(f"✅ Больше сообщений не найдено после {consecutive_not_found} попыток")
                        break
                else:
                    print(f"❌ Ошибка при удалении сообщения {msg_id}: {e}")
                    break
            
            msg_id += 1
        
        print(f"✅ Успешно удалено {deleted_count} сообщений")
        
    except TelegramError as e:
        print(f"❌ Ошибка при очистке канала: {e}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")

if __name__ == "__main__":
    print("🚀 Начинаю очистку канала...")
    asyncio.run(clear_channel_history())
    print("🏁 Очистка завершена!") 