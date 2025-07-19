#!/usr/bin/env python3
"""
Тестовый скрипт для проверки healthcheck
"""

import requests
import time

def test_healthcheck():
    """Тестирует healthcheck endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Тестирование healthcheck...")
    
    try:
        # Тест корневого endpoint
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"✅ / - Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Тест health endpoint
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"✅ /health - Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Не удалось подключиться к серверу")
        return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Запуск теста healthcheck...")
    
    # Ждем немного для запуска сервера
    time.sleep(3)
    
    success = test_healthcheck()
    
    if success:
        print("✅ Healthcheck работает!")
    else:
        print("❌ Healthcheck не работает!") 