#!/usr/bin/env python3
"""
Быстрый тест всех компонентов
"""

import os
import sys
import requests

def test_environment():
    """Тестирует переменные окружения"""
    print("🔧 Проверка переменных окружения...")
    
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    channel = os.environ.get('TELEGRAM_CHANNEL_ID')
    
    if token:
        print(f"✅ TELEGRAM_BOT_TOKEN: {token[:10]}...")
    else:
        print("❌ TELEGRAM_BOT_TOKEN не установлен")
    
    if channel:
        print(f"✅ TELEGRAM_CHANNEL_ID: {channel}")
    else:
        print("❌ TELEGRAM_CHANNEL_ID не установлен")
    
    return bool(token and channel)

def test_telegram():
    """Тестирует подключение к Telegram"""
    print("\n📱 Проверка подключения к Telegram...")
    
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not token:
        print("❌ Токен не установлен")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{token}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Бот найден: @{data['result']['username']}")
            return True
        else:
            print(f"❌ Ошибка Telegram API: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

def test_web_server():
    """Тестирует веб-сервер"""
    print("\n🌐 Проверка веб-сервера...")
    
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Веб-сервер работает")
            return True
        else:
            print(f"❌ Веб-сервер вернул статус: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Веб-сервер не отвечает")
        return False
    except Exception as e:
        print(f"❌ Ошибка веб-сервера: {e}")
        return False

if __name__ == '__main__':
    print("🧪 Быстрый тест компонентов")
    print("=" * 40)
    
    env_ok = test_environment()
    telegram_ok = test_telegram()
    web_ok = test_web_server()
    
    print("\n" + "=" * 40)
    print("📊 Результаты тестов:")
    print(f"🔧 Переменные окружения: {'✅' if env_ok else '❌'}")
    print(f"📱 Telegram API: {'✅' if telegram_ok else '❌'}")
    print(f"🌐 Веб-сервер: {'✅' if web_ok else '❌'}")
    
    if all([env_ok, telegram_ok, web_ok]):
        print("\n🎉 Все тесты пройдены!")
    else:
        print("\n⚠️ Некоторые тесты не пройдены") 