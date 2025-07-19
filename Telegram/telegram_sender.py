import os
import asyncio
import aiohttp
import json

# Конфигурация Telegram
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID", "")

async def send_message(message_text, channel_id=None):
    """Отправляет сообщение в Telegram канал"""
    if not TELEGRAM_BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN не установлен")
        return False
    
    if not channel_id and not TELEGRAM_CHANNEL_ID:
        print("❌ TELEGRAM_CHANNEL_ID не установлен")
        return False
    
    target_channel = channel_id or TELEGRAM_CHANNEL_ID
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        
        data = {
            "chat_id": target_channel,
            "text": message_text,
            "parse_mode": "HTML",  # Поддержка HTML разметки
            "disable_web_page_preview": False
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get("ok"):
                        print(f"✅ Сообщение отправлено в канал {target_channel}")
                        return True
                    else:
                        print(f"❌ Ошибка отправки: {result.get('description', 'Unknown error')}")
                        return False
                else:
                    print(f"❌ HTTP ошибка: {response.status}")
                    return False
                    
    except Exception as e:
        print(f"❌ Ошибка отправки сообщения: {e}")
        return False

async def send_photo(photo_url, caption="", channel_id=None):
    """Отправляет фото в Telegram канал"""
    if not TELEGRAM_BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN не установлен")
        return False
    
    target_channel = channel_id or TELEGRAM_CHANNEL_ID
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        
        data = {
            "chat_id": target_channel,
            "photo": photo_url,
            "caption": caption,
            "parse_mode": "HTML"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get("ok"):
                        print(f"✅ Фото отправлено в канал {target_channel}")
                        return True
                    else:
                        print(f"❌ Ошибка отправки фото: {result.get('description', 'Unknown error')}")
                        return False
                else:
                    print(f"❌ HTTP ошибка: {response.status}")
                    return False
                    
    except Exception as e:
        print(f"❌ Ошибка отправки фото: {e}")
        return False

def test_telegram_connection():
    """Тестирует подключение к Telegram API"""
    if not TELEGRAM_BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN не установлен")
        return False
    
    try:
        import requests
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                bot_info = data.get("result", {})
                print(f"✅ Подключение к Telegram успешно!")
                print(f"  Бот: @{bot_info.get('username', 'Unknown')}")
                print(f"  Имя: {bot_info.get('first_name', 'Unknown')}")
                return True
            else:
                print(f"❌ Ошибка API: {data.get('description', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Тест Telegram отправки...")
    
    # Тестируем подключение
    if test_telegram_connection():
        # Тестируем отправку сообщения
        test_message = "🤖 Тестовое сообщение от бота с шутками!"
        asyncio.run(send_message(test_message))
    else:
        print("❌ Не удалось подключиться к Telegram API") 