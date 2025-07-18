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
            print(f"\n🕐 [{current_time}] Запуск очистки канала...")
            
            # Запускаем скрипт очистки из папки Telegram
            result = subprocess.run([sys.executable, "Telegram/clear_channel_history.py"], 
                                  capture_output=True, text=True)
            
            # Выводим результат
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(f"⚠️ Ошибки: {result.stderr}")
            
            print(f"✅ Очистка завершена с кодом: {result.returncode}")
            
            # Ждем 5 минут перед следующей очисткой
            print("😴 Ожидание 5 минут перед следующей очисткой...")
            time.sleep(300)  # 5 минут
            
        except KeyboardInterrupt:
            print("\n🛑 Остановка скрипта по запросу пользователя")
            break
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")
            print("🔄 Перезапуск через 1 минуту...")
            time.sleep(60)

if __name__ == "__main__":
    run_forever() 