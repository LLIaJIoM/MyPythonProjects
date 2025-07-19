import requests
import json

def test_api():
    """Быстрый тест API"""
    base_url = "http://localhost:8888"
    
    print("🚀 Быстрый тест IO Intelligence API")
    print("=" * 40)
    
    # Тест 1: Корневой эндпоинт
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print("✅ API работает!")
            print(f"  Провайдер: {data['api_provider']}")
            print(f"  Модели: {len(data['available_models'])} доступно")
        else:
            print(f"❌ Ошибка API: {response.status_code}")
    except Exception as e:
        print(f"❌ Не удалось подключиться к API: {e}")
        return
    
    # Тест 2: Список моделей
    try:
        response = requests.get(f"{base_url}/v1/models")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Список моделей получен: {len(data['data'])} моделей")
            for model in data['data'][:3]:  # Показываем первые 3
                print(f"  - {model['id']}")
        else:
            print(f"❌ Ошибка получения моделей: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # Тест 3: Чат комплеты
    try:
        payload = {
            "model": "deepseek-ai/DeepSeek-R1-0528",
            "messages": [
                {"role": "user", "content": "Привет! Как дела?"}
            ],
            "temperature": 0.7,
            "max_tokens": 50
        }
        
        response = requests.post(
            f"{base_url}/v1/chat/completions",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Чат комплеты работают!")
            print(f"  Ответ: {data['choices'][0]['message']['content']}")
        else:
            print(f"❌ Ошибка чат комплетов: {response.status_code}")
            print(f"  Детали: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка чат комплетов: {e}")
    
    # Тест 4: Статус сервера
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Статус сервера:")
            print(f"  Запросов: {data['stats']['total_requests']}")
            print(f"  Ошибок: {data['stats']['error_count']}")
            print(f"  IO API: {data['io_api_status']}")
        else:
            print(f"❌ Ошибка статуса: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка статуса: {e}")

if __name__ == "__main__":
    test_api() 