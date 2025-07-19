#!/usr/bin/env python3
"""
Финальная версия приложения для Railway
Запускает Telegram бота + веб-сервер для healthcheck
"""

import os
import sys
import asyncio
import threading
import time
from flask import Flask

# Устанавливаем переменные окружения если они не установлены
if not os.environ.get('TELEGRAM_BOT_TOKEN'):
    os.environ['TELEGRAM_BOT_TOKEN'] = '7638129033:AAEYmXQikS0qa-qJ-Roxp3Wg7HLEQH9f-ao'

if not os.environ.get('TELEGRAM_CHANNEL_ID'):
    os.environ['TELEGRAM_CHANNEL_ID'] = '-1002719144496'

# Создаем Flask приложение
app = Flask(__name__)

@app.route('/')
def health_check():
    return {
        "status": "healthy",
        "service": "Telegram News Bot",
        "version": "1.0.0",
        "bot": "running",
        "timestamp": time.time()
    }

@app.route('/health')
def health():
    return {"status": "ok", "timestamp": time.time()}

@app.route('/status')
def status():
    return {
        "bot_token": os.environ.get('TELEGRAM_BOT_TOKEN', 'НЕ УСТАНОВЛЕН')[:10] + "...",
        "channel_id": os.environ.get('TELEGRAM_CHANNEL_ID', 'НЕ УСТАНОВЛЕН'),
        "uptime": time.time()
    }

def run_bot():
    """Запускает Telegram бота в отдельном потоке"""
    try:
        print("🤖 Запуск Telegram бота...")
        
        # Добавляем путь к модулям Telegram
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Telegram'))
        
        # Запускаем бота через subprocess
        import subprocess
        subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'Telegram', 'main.py')], check=True)
        
    except Exception as e:
        print(f"❌ Ошибка запуска бота: {e}")

def run_web_server():
    """Запускает веб-сервер"""
    port = int(os.environ.get('PORT', 5000))
    print(f"🌐 Запуск веб-сервера на порту {port}...")
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)

if __name__ == '__main__':
    print("🚀 Запуск Telegram бота с веб-сервером для Railway...")
    print(f"Token: {os.environ.get('TELEGRAM_BOT_TOKEN', 'НЕ УСТАНОВЛЕН')[:10]}...")
    print(f"Channel: {os.environ.get('TELEGRAM_CHANNEL_ID', 'НЕ УСТАНОВЛЕН')}")
    
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    print("🤖 Бот запущен в фоне")
    print("🌐 Веб-сервер запускается...")
    
    # Запускаем веб-сервер в основном потоке
    run_web_server() 