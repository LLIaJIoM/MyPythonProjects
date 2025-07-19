#!/usr/bin/env python3
"""
Скрипт для удаления всех сообщений в Telegram канале
"""

import requests
import time
import os

# Конфигурация
BOT_TOKEN = "7638129033:AAEYmXQikS0qa-qJ-Roxp3Wg7HLEQH9f-ao"
CHANNEL_ID = "-1002719144496"

def get_channel_info():
    """Получает информацию о канале"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChat"
    params = {"chat_id": CHANNEL_ID}
    
    try:
        response = requests.get(url, params=params)
        result = response.json()
        
        if result.get("ok"):
            chat = result["result"]
            print(f"📱 Канал: {chat.get('title', 'Неизвестно')}")
            print(f"🆔 ID: {chat.get('id')}")
            print(f"👤 Тип: {chat.get('type')}")
            return True
        else:
            print(f"❌ Ошибка получения информации о канале: {result.get('description', 'Неизвестная ошибка')}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка получения информации о канале: {e}")
        return False

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

def clear_channel_messages():
    """Удаляет сообщения в канале"""
    print("🗑️ Удаление сообщений в канале")
    print("=" * 50)
    print(f"🤖 Бот: {BOT_TOKEN[:10]}...")
    print(f"📱 Канал: {CHANNEL_ID}")
    print("=" * 50)
    
    # Проверяем информацию о канале
    if not get_channel_info():
        print("❌ Не удалось получить информацию о канале")
        return False
    
    # Удаляем сообщения с ID от 1 до 200
    deleted = 0
    failed = 0
    
    print(f"\n🗑️ Удаляю сообщения с ID 1-200...")
    
    for message_id in range(1, 201):
        print(f"🗑️ Удаляю сообщение {message_id}...")
        
        if delete_message(message_id):
            deleted += 1
        else:
            failed += 1
        
        # Задержка между удалениями
        time.sleep(0.3)
    
    print("\n" + "=" * 50)
    print("📊 Результаты удаления:")
    print(f"✅ Удалено: {deleted}")
    print(f"❌ Ошибок: {failed}")
    print(f"📊 Всего обработано: {deleted + failed}")
    print("=" * 50)
    
    return True

def main():
    """Основная функция"""
    print("🗑️ Скрипт удаления сообщений в Telegram канале")
    print("=" * 50)
    
    # Подтверждение
    confirm = input("\n⚠️ ВНИМАНИЕ! Это удалит ВСЕ сообщения в канале!\nВведите 'YES' для подтверждения: ")
    
    if confirm != "YES":
        print("❌ Операция отменена")
        return
    
    print("\n🚀 Начинаю удаление...")
    
    if clear_channel_messages():
        print("\n✅ Удаление завершено!")
    else:
        print("\n❌ Удаление не удалось!")

if __name__ == "__main__":
    main() 