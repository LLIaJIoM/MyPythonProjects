#!/usr/bin/env python3
"""
Тестовый скрипт для проверки удаления сообщений
"""

import requests

# Конфигурация
BOT_TOKEN = "7638129033:AAEYmXQikS0qa-qJ-Roxp3Wg7HLEQH9f-ao"
CHANNEL_ID = "-1002719144496"

def test_bot_connection():
    """Тестирует подключение к боту"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    
    try:
        response = requests.get(url)
        result = response.json()
        
        if result.get("ok"):
            bot = result["result"]
            print(f"✅ Бот подключен: @{bot['username']}")
            return True
        else:
            print(f"❌ Ошибка бота: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

def test_channel_access():
    """Тестирует доступ к каналу"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChat"
    params = {"chat_id": CHANNEL_ID}
    
    try:
        response = requests.get(url, params=params)
        result = response.json()
        
        if result.get("ok"):
            chat = result["result"]
            print(f"✅ Доступ к каналу: {chat.get('title')}")
            return True
        else:
            print(f"❌ Ошибка канала: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка канала: {e}")
        return False

def test_delete_message(message_id=1):
    """Тестирует удаление сообщения"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "message_id": message_id
    }
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        
        if result.get("ok"):
            print(f"✅ Удаление работает: сообщение {message_id}")
            return True
        else:
            error = result.get('description', 'Неизвестная ошибка')
            print(f"❌ Ошибка удаления: {error}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка удаления: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Тест удаления сообщений")
    print("=" * 40)
    
    # Тестируем подключение к боту
    bot_ok = test_bot_connection()
    
    # Тестируем доступ к каналу
    channel_ok = test_channel_access()
    
    # Тестируем удаление
    if bot_ok and channel_ok:
        print("\n🗑️ Тестируем удаление сообщения...")
        delete_ok = test_delete_message(1)
        
        if delete_ok:
            print("\n✅ Все тесты пройдены! Можно удалять сообщения.")
        else:
            print("\n❌ Удаление не работает. Проверьте права бота.")
    else:
        print("\n❌ Проблемы с подключением.") 