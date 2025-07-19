#!/usr/bin/env python3
"""
Улучшенный скрипт для удаления всех постов в Telegram канале
Использует правильный API для получения сообщений
"""

import os
import requests
import time
import json

# Конфигурация
BOT_TOKEN = "7638129033:AAEYmXQikS0qa-qJ-Roxp3Wg7HLEQH9f-ao"
CHANNEL_ID = "-1002719144496"

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
            error_desc = result.get('description', 'Неизвестная ошибка')
            if "message to delete not found" in error_desc.lower():
                print(f"⏭️ Сообщение {message_id} уже удалено")
                return True
            else:
                print(f"❌ Ошибка удаления сообщения {message_id}: {error_desc}")
                return False
            
    except Exception as e:
        print(f"❌ Ошибка удаления сообщения {message_id}: {e}")
        return False

def get_channel_messages():
    """Получает сообщения из канала через getUpdates"""
    print("🔍 Получаю сообщения из канала...")
    
    # Сначала получаем информацию о боте
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    try:
        response = requests.get(url)
        response.raise_for_status()
        bot_info = response.json()
        
        if not bot_info.get("ok"):
            print("❌ Не удалось получить информацию о боте")
            return []
            
        print(f"🤖 Бот: @{bot_info['result']['username']}")
        
    except Exception as e:
        print(f"❌ Ошибка получения информации о боте: {e}")
        return []
    
    # Получаем обновления (сообщения)
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {
        "limit": 100,
        "timeout": 1
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        result = response.json()
        
        if result.get("ok"):
            updates = result.get("result", [])
            messages = []
            
            for update in updates:
                if "channel_post" in update:
                    message = update["channel_post"]
                    if message.get("chat", {}).get("id") == int(CHANNEL_ID):
                        messages.append(message)
                elif "message" in update:
                    message = update["message"]
                    if message.get("chat", {}).get("id") == int(CHANNEL_ID):
                        messages.append(message)
            
            print(f"📊 Найдено {len(messages)} сообщений в канале")
            return messages
        else:
            print(f"❌ Ошибка получения сообщений: {result.get('description', 'Неизвестная ошибка')}")
            return []
            
    except Exception as e:
        print(f"❌ Ошибка получения сообщений: {e}")
        return []

def clear_channel_history():
    """Удаляет все сообщения в канале"""
    print("🧹 Начинаю очистку канала...")
    print("=" * 50)
    
    # Проверяем информацию о канале
    if not get_channel_info():
        print("❌ Не удалось получить информацию о канале")
        return False
    
    # Получаем сообщения
    messages = get_channel_messages()
    
    if not messages:
        print("📭 В канале нет сообщений для удаления")
        return True
    
    # Удаляем сообщения
    deleted_count = 0
    failed_count = 0
    
    print(f"\n🗑️ Удаляю {len(messages)} сообщений...")
    
    for i, message in enumerate(messages, 1):
        message_id = message.get("message_id")
        if message_id:
            print(f"📝 [{i}/{len(messages)}] Удаляю сообщение {message_id}...")
            
            if delete_message(message_id):
                deleted_count += 1
            else:
                failed_count += 1
            
            # Небольшая задержка между удалениями
            time.sleep(0.5)
    
    print("\n" + "=" * 50)
    print("📊 Результаты очистки:")
    print(f"✅ Удалено: {deleted_count}")
    print(f"❌ Ошибок: {failed_count}")
    print(f"📊 Всего обработано: {deleted_count + failed_count}")
    
    return True

def main():
    """Основная функция"""
    print("🗑️ Скрипт очистки Telegram канала v2")
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