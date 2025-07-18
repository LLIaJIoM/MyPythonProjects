import asyncio
from telegram import Bot
from datetime import datetime

TELEGRAM_TOKEN = "7638129033:AAEYmXQikS0qa-qJ-Roxp3Wg7HLEQH9f-ao"
CHANNEL_ID = "-1002719144496"

async def check_channel_status():
    """Проверяет статус канала и последние сообщения"""
    bot = Bot(token=TELEGRAM_TOKEN)
    
    try:
        # Получаем информацию о канале
        chat = await bot.get_chat(CHANNEL_ID)
        print(f"📢 Канал: {chat.title}")
        print(f"👥 Участников: {chat.member_count if hasattr(chat, 'member_count') else 'Неизвестно'}")
        
        # Проверяем последние сообщения
        print("\n🔍 Проверяем последние сообщения...")
        
        # Пытаемся получить последние сообщения
        try:
            # Отправляем тестовое сообщение
            test_msg = await bot.send_message(
                chat_id=CHANNEL_ID, 
                text=f"🤖 Тест работы сервера\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            print(f"✅ Тестовое сообщение отправлено (ID: {test_msg.message_id})")
            
            # Удаляем тестовое сообщение
            await bot.delete_message(chat_id=CHANNEL_ID, message_id=test_msg.message_id)
            print("🗑️ Тестовое сообщение удалено")
            
        except Exception as e:
            print(f"❌ Ошибка при работе с сообщениями: {e}")
        
        print("\n✅ Канал работает нормально!")
        
    except Exception as e:
        print(f"❌ Ошибка при проверке канала: {e}")

if __name__ == "__main__":
    print("🔍 Проверка статуса канала...")
    asyncio.run(check_channel_status()) 