import subprocess
import time
import sys
import os
from datetime import datetime

def run_forever():
    """Запускает скрипт очистки канала в бесконечном цикле"""
    
    print("🌙 Запуск скрипта очистки канала в режиме 'спать и работать'")
    print("💡 Для остановки нажмите Ctrl+C")
    print("=" * 50)
    
    while True:
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n🕐 [{current_time}] Запуск бота новостей...")
            
            # Запускаем основной бот из папки Telegram
            result = subprocess.run([sys.executable, "Telegram/main.py"], 
                                  capture_output=True, text=True)
            
            # Выводим результат
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(f"⚠️ Ошибки: {result.stderr}")
            
            print(f"✅ Бот завершил работу с кодом: {result.returncode}")
            
            # Ждем 1 минуту перед перезапуском (если бот упал)
            print("😴 Ожидание 1 минуты перед перезапуском...")
            time.sleep(60)  # 1 минута
            
        except KeyboardInterrupt:
            print("\n🛑 Остановка скрипта по запросу пользователя")
            break
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")
            print("🔄 Перезапуск через 1 минуту...")
            time.sleep(60)

if __name__ == "__main__":
    run_forever() 