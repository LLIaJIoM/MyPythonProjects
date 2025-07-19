#!/usr/bin/env python3
"""
Простой скрипт для удаления сообщений в Telegram канале
"""

import requests
import time

# Конфигурация
BOT_TOKEN = "7638129033:AAEYmXQikS0qa-qJ-Roxp3Wg7HLEQH9f-ao"
CHANNEL_ID = "-1002719144496"

def delete_message(message_id):
    """Удаляет сообщение по ID"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "message_id": message_id
    }
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        
        if result.get("ok"):
            print(f"✅ Удалено сообщение {message_id}")
            return True
        else:
            error = result.get('description', 'Неизвестная ошибка')
            if "message to delete not found" in error.lower():
                print(f"⏭️ Сообщение {message_id} уже удалено")
                return True
            else:
                print(f"❌ Ошибка удаления {message_id}: {error}")
                return False
                
    except Exception as e:
        print(f"❌ Ошибка удаления {message_id}: {e}")
        return False

def clear_recent_messages():
    """Удаляет последние сообщения в канале"""
    print("🗑️ Удаление сообщений в канале")
    print("=" * 40)
    print(f"🤖 Бот: {BOT_TOKEN[:10]}...")
    print(f"📱 Канал: {CHANNEL_ID}")
    print("=" * 40)
    
    # Удаляем сообщения с ID от 1 до 100
    deleted = 0
    failed = 0
    
    for message_id in range(1, 101):
        print(f"🗑️ Удаляю сообщение {message_id}...")
        
        if delete_message(message_id):
            deleted += 1
        else:
            failed += 1
        
        # Задержка между удалениями
        time.sleep(0.3)
    
    print("\n" + "=" * 40)
    print("📊 Результаты:")
    print(f"✅ Удалено: {deleted}")
    print(f"❌ Ошибок: {failed}")
    print("=" * 40)

if __name__ == "__main__":
    # Подтверждение
    confirm = input("⚠️ Удалить последние 100 сообщений? (y/N): ")
    
    if confirm.lower() == 'y':
        clear_recent_messages()
    else:
        print("❌ Отменено") 