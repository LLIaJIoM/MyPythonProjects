#!/usr/bin/env python3
"""
Скрипт для запуска Telegram бота с правильными переменными окружения
"""

import os
import sys
import asyncio

# Устанавливаем переменные окружения если они не установлены
if not os.environ.get('TELEGRAM_BOT_TOKEN'):
    os.environ['TELEGRAM_BOT_TOKEN'] = '7638129033:AAEYmXQikS0qa-qJ-Roxp3Wg7HLEQH9f-ao'

if not os.environ.get('TELEGRAM_CHANNEL_ID'):
    os.environ['TELEGRAM_CHANNEL_ID'] = '-1002719144496'

# Добавляем путь к модулям Telegram
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Telegram'))

# Импортируем и запускаем бота
from main import main

if __name__ == '__main__':
    print("🤖 Запуск Telegram бота...")
    print(f"Token: {os.environ.get('TELEGRAM_BOT_TOKEN', 'НЕ УСТАНОВЛЕН')[:10]}...")
    print(f"Channel: {os.environ.get('TELEGRAM_CHANNEL_ID', 'НЕ УСТАНОВЛЕН')}")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен")
    except Exception as e:
        print(f"❌ Ошибка запуска бота: {e}") 