import subprocess
import threading
import time
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def health_check():
    return {
        "status": "healthy",
        "service": "Telegram News Bot",
        "version": "1.0.0"
    }

@app.route('/health')
def health():
    return {"status": "ok"}

def run_bot():
    """Запускает Telegram бота в отдельном потоке"""
    try:
        subprocess.run(["python", "Telegram/main.py"], check=True)
    except Exception as e:
        print(f"Ошибка запуска бота: {e}")

def run_web_server():
    """Запускает веб-сервер"""
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    print("🚀 Запуск Telegram бота с веб-сервером...")
    
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    print("🤖 Бот запущен в фоне")
    print("🌐 Веб-сервер запускается...")
    
    # Запускаем веб-сервер в основном потоке
    run_web_server() 