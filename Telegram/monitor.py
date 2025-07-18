import asyncio
from telegram import Bot
from datetime import datetime
import time

TELEGRAM_TOKEN = "7638129033:AAEYmXQikS0qa-qJ-Roxp3Wg7HLEQH9f-ao"
CHANNEL_ID = "-1002719144496"

# ID вашего личного чата для уведомлений (замените на свой)
ADMIN_CHAT_ID = None  # Замените на ваш ID

async def send_admin_notification(message):
    """Отправляет уведомление администратору"""
    if ADMIN_CHAT_ID:
        try:
            bot = Bot(token=TELEGRAM_TOKEN)
            await bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=f"🤖 Мониторинг сервера\n{message}"
            )
        except Exception as e:
            print(f"❌ Ошибка отправки уведомления: {e}")

async def check_server_health():
    """Проверяет здоровье сервера"""
    bot = Bot(token=TELEGRAM_TOKEN)
    
    try:
        # Проверяем подключение к каналу
        chat = await bot.get_chat(CHANNEL_ID)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        status_msg = f"✅ Сервер работает\n📢 Канал: {chat.title}\n⏰ {current_time}"
        print(status_msg)
        
        # Отправляем уведомление администратору
        await send_admin_notification(status_msg)
        
        return True
        
    except Exception as e:
        error_msg = f"❌ Ошибка сервера: {e}\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        print(error_msg)
        
        # Отправляем уведомление об ошибке
        await send_admin_notification(error_msg)
        
        return False

async def monitor_forever():
    """Бесконечный мониторинг"""
    print("🔍 Запуск мониторинга сервера...")
    print("💡 Проверка каждые 30 минут")
    
    while True:
        try:
            is_healthy = await check_server_health()
            
            if is_healthy:
                print("✅ Сервер работает нормально")
            else:
                print("⚠️ Обнаружены проблемы с сервером")
            
            # Ждем 30 минут до следующей проверки
            print("😴 Ожидание 30 минут...")
            await asyncio.sleep(1800)  # 30 минут
            
        except Exception as e:
            print(f"❌ Критическая ошибка мониторинга: {e}")
            await asyncio.sleep(300)  # Ждем 5 минут при ошибке

if __name__ == "__main__":
    print("🚀 Запуск мониторинга...")
    asyncio.run(monitor_forever()) 