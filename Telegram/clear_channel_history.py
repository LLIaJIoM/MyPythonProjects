#!/usr/bin/env python3
"""
Скрипт для удаления всех постов в Telegram канале
"""

import os
import requests
import time
import json

# Конфигурация
BOT_TOKEN = "7638129033:AAEYmXQikS0qa-qJ-Roxp3Wg7HLEQH9f-ao"
CHANNEL_ID = "-1002719144496"

def get_channel_messages(offset=0, limit=100):
    """Получает сообщения из канала"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {
        "chat_id": CHANNEL_ID,
        "offset": offset,
        "limit": limit
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Ошибка получения сообщений: {e}")
        return None

def delete_message(message_id):
    """Удаляет конкретное сообщение"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "message_id": message_id
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        
        if result.get("ok"):
            print(f"✅ Удалено сообщение {message_id}")
            return True
        else:
            print(f"❌ Ошибка удаления сообщения {message_id}: {result.get('description', 'Неизвестная ошибка')}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка удаления сообщения {message_id}: {e}")
        return False

def get_channel_info():
    """Получает информацию о канале"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChat"
    params = {"chat_id": CHANNEL_ID}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
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

def clear_channel_history():
    """Удаляет все сообщения в канале"""
    print("🧹 Начинаю очистку канала...")
    print("=" * 50)
    
    # Проверяем информацию о канале
    if not get_channel_info():
        print("❌ Не удалось получить информацию о канале")
        return False
    
    print("\n🔍 Получаю сообщения из канала...")
    
    # Получаем сообщения
    messages_data = get_channel_messages()
    if not messages_data or not messages_data.get("ok"):
        print("❌ Не удалось получить сообщения")
        return False
    
    messages = messages_data.get("result", [])
    if not messages:
        print("📭 В канале нет сообщений для удаления")
        return True
    
    print(f"📊 Найдено {len(messages)} сообщений")
    
    # Удаляем сообщения
    deleted_count = 0
    failed_count = 0
    
    for message in messages:
        message_id = message.get("message", {}).get("message_id")
        if message_id:
            if delete_message(message_id):
                deleted_count += 1
            else:
                failed_count += 1
            
            # Небольшая задержка между удалениями
            time.sleep(0.1)
    
    print("\n" + "=" * 50)
    print("📊 Результаты очистки:")
    print(f"✅ Удалено: {deleted_count}")
    print(f"❌ Ошибок: {failed_count}")
    print(f"📊 Всего обработано: {deleted_count + failed_count}")
    
    return True

def main():
    """Основная функция"""
    print("🗑️ Скрипт очистки Telegram канала")
    print("=" * 50)
    print(f"🤖 Бот: {BOT_TOKEN[:10]}...")
    print(f"📱 Канал: {CHANNEL_ID}")
    print("=" * 50)
    
    # Подтверждение
    confirm = input("\n⚠️ ВНИМАНИЕ! Это удалит ВСЕ сообщения в канале!\nВведите 'YES' для подтверждения: ")
    
    if confirm != "YES":
        print("❌ Операция отменена")
        return
    
    print("\n🚀 Начинаю очистку...")
    
    if clear_channel_history():
        print("\n✅ Очистка завершена!")
    else:
        print("\n❌ Очистка не удалась!")

if __name__ == "__main__":
    main() 