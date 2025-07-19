import requests
import asyncio
import aiohttp

# Конфигурация
BOT_TOKEN = "7638129033:AAEYmXQikS0qa-qJ-Roxp3Wg7HLEQH9f-ao"
CHANNEL_ID = "-1002719144496"

async def test_send_message():
    """Тестирует отправку сообщения в Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    message = """🤖 <b>Тестовое сообщение от бота с шутками!</b>

🎭 <b>Тестовая шутка:</b>
Почему программисты путают Рождество и Хэллоуин? Потому что Oct 31 == Dec 25!

📊 <b>Статус:</b> Бот работает
🔗 <a href="https://t.me/your_channel">Канал</a>

#тест #бот #юмор"""
    
    data = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                print(f"Status: {response.status}")
                result = await response.json()
                print(f"Response: {result}")
                
                if result.get("ok"):
                    print("✅ Сообщение отправлено успешно!")
                else:
                    print(f"❌ Ошибка: {result.get('description', 'Unknown error')}")
                    
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")

def test_bot_info():
    """Тестирует информацию о боте"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    
    try:
        response = requests.get(url)
        print(f"Bot Info Status: {response.status_code}")
        print(f"Bot Info Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                bot_info = data.get("result", {})
                print(f"✅ Бот найден: @{bot_info.get('username', 'Unknown')}")
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
    print("🧪 Тестирование отправки в Telegram...")
    print(f"Token: {BOT_TOKEN[:10]}...")
    print(f"Channel: {CHANNEL_ID}")
    print("=" * 50)
    
    # Тестируем информацию о боте
    test_bot_info()
    
    # Тестируем отправку сообщения
    asyncio.run(test_send_message()) 