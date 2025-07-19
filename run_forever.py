import threading
import time
import os
import asyncio
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
        # Импортируем и запускаем бота напрямую
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Telegram'))
        
        from main import main as bot_main
        asyncio.run(bot_main())
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