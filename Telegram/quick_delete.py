#!/usr/bin/env python3
"""
Быстрый скрипт для удаления последних сообщений в канале
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

def quick_delete():
    """Быстрое удаление последних сообщений"""
    print("🗑️ Быстрое удаление сообщений")
    print("=" * 40)
    print(f"🤖 Бот: {BOT_TOKEN[:10]}...")
    print(f"📱 Канал: {CHANNEL_ID}")
    print("=" * 40)
    
    # Удаляем последние 50 сообщений
    deleted = 0
    failed = 0
    
    for message_id in range(1, 51):
        if delete_message(message_id):
            deleted += 1
        else:
            failed += 1
        
        # Быстрая задержка
        time.sleep(0.2)
    
    print("\n" + "=" * 40)
    print("📊 Результаты:")
    print(f"✅ Удалено: {deleted}")
    print(f"❌ Ошибок: {failed}")
    print("=" * 40)

if __name__ == "__main__":
    # Простое подтверждение
    confirm = input("🗑️ Удалить последние 50 сообщений? (y/N): ")
    
    if confirm.lower() == 'y':
        quick_delete()
    else:
        print("❌ Отменено") 