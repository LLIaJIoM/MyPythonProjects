#!/usr/bin/env python3
"""
Скрипт для запуска Telegram бота с веб-сервером для Railway healthcheck
"""

import os
import sys
import asyncio
import threading
from flask import Flask

# Устанавливаем переменные окружения если они не установлены
if not os.environ.get('TELEGRAM_BOT_TOKEN'):
    os.environ['TELEGRAM_BOT_TOKEN'] = '7638129033:AAEYmXQikS0qa-qJ-Roxp3Wg7HLEQH9f-ao'

if not os.environ.get('TELEGRAM_CHANNEL_ID'):
    os.environ['TELEGRAM_CHANNEL_ID'] = '-1002719144496'

# Создаем Flask приложение для healthcheck
app = Flask(__name__)

@app.route('/')
def health_check():
    return {
        "status": "healthy",
        "service": "Telegram News Bot",
        "version": "1.0.0",
        "bot": "running"
    }

@app.route('/health')
def health():
    return {"status": "ok"}

def run_bot():
    """Запускает Telegram бота в отдельном потоке"""
    try:
        # Добавляем путь к модулям Telegram
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Telegram'))
        
        # Импортируем и запускаем бота
        from main import main as bot_main
        asyncio.run(bot_main())
    except Exception as e:
        print(f"❌ Ошибка запуска бота: {e}")

def run_web_server():
    """Запускает веб-сервер"""
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    print("🚀 Запуск Telegram бота с веб-сервером...")
    print(f"Token: {os.environ.get('TELEGRAM_BOT_TOKEN', 'НЕ УСТАНОВЛЕН')[:10]}...")
    print(f"Channel: {os.environ.get('TELEGRAM_CHANNEL_ID', 'НЕ УСТАНОВЛЕН')}")
    
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    print("🤖 Бот запущен в фоне")
    print("🌐 Веб-сервер запускается...")
    
    # Запускаем веб-сервер в основном потоке
    run_web_server() 