import requests
import json

# Базовый URL API
BASE_URL = "http://localhost:8888"

def test_io_connection():
    """Тестирует подключение к IO Intelligence API"""
    print("🔍 Тестирование подключения к IO Intelligence API...")
    
    try:
        response = requests.get(f"{BASE_URL}/test-io-api")
        if response.status_code == 200:
            data = response.json()
            print("✅ Подключение к IO Intelligence API:")
            print(f"  Статус: {data['status']}")
            print(f"  Количество моделей: {data['models_count']}")
            print(f"  Модели: {', '.join(data['models'])}")
        else:
            print(f"❌ Ошибка: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

def test_models_endpoint():
    """Тестирует эндпоинт /v1/models"""
    print("\n🔍 Тестирование эндпоинта /v1/models...")
    
    try:
        response = requests.get(f"{BASE_URL}/v1/models")
        if response.status_code == 200:
            data = response.json()
            print("✅ Успешно получен список моделей:")
            for model in data.get('data', []):
                print(f"  - {model['id']}")
        else:
            print(f"❌ Ошибка: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

def test_chat_completions():
    """Тестирует эндпоинт /v1/chat/completions"""
    print("\n🔍 Тестирование эндпоинта /v1/chat/completions...")
    
    payload = {
        "model": "deepseek-ai/DeepSeek-R1",
        "messages": [
            {"role": "system", "content": "Ты полезный ассистент."},
            {"role": "user", "content": "Привет! Как дела?"}
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/v1/chat/completions",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Успешно получен ответ:")
            print(f"  Модель: {data['model']}")
            print(f"  Ответ: {data['choices'][0]['message']['content']}")
            print(f"  Использовано токенов: {data['usage']['total_tokens']}")
        else:
            print(f"❌ Ошибка: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

def test_completions():
    """Тестирует эндпоинт /v1/completions"""
    print("\n🔍 Тестирование эндпоинта /v1/completions...")
    
    payload = {
        "model": "deepseek-ai/DeepSeek-R1",
        "prompt": "Расскажи короткую шутку:",
        "temperature": 0.7,
        "max_tokens": 50
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/v1/completions",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Успешно получен ответ:")
            print(f"  Модель: {data['model']}")
            print(f"  Ответ: {data['choices'][0]['text']}")
            print(f"  Использовано токенов: {data['usage']['total_tokens']}")
        else:
            print(f"❌ Ошибка: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

def test_health():
    """Тестирует эндпоинт /health"""
    print("\n🔍 Тестирование эндпоинта /health...")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Статус сервера:")
            print(f"  Статус: {data['status']}")
            print(f"  Время: {data['timestamp']}")
            print(f"  Всего запросов: {data['stats']['total_requests']}")
            print(f"  Ошибок: {data['stats']['error_count']}")
            print(f"  Успешность: {data['stats']['success_rate']:.1f}%")
            print(f"  IO API статус: {data['io_api_status']}")
        else:
            print(f"❌ Ошибка: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

def test_root():
    """Тестирует корневой эндпоинт"""
    print("\n🔍 Тестирование корневого эндпоинта...")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print("✅ Информация об API:")
            print(f"  Сообщение: {data['message']}")
            print(f"  Версия: {data['version']}")
            print(f"  Провайдер: {data['api_provider']}")
            print(f"  Доступные модели: {', '.join(data['available_models'])}")
        else:
            print(f"❌ Ошибка: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

def test_direct_io_api():
    """Тестирует прямое подключение к IO Intelligence API"""
    print("\n🔍 Тестирование прямого подключения к IO Intelligence API...")
    
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer io-v2-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvd25lciI6IjY3YzM5OGE5LTZkNzYtNDMyZS1iYTlhLTY5ODZiODVjMmRkOCIsImV4cCI6NDkwNjQ4MTUwOX0.m0CayY7WgNNksnxAj-QAhsEYUEJNKbpujJoSm7sFwEwFxOeCNrrQx3jGLAh-vCwKd7wAvvDvFg3MnNjj8FIEdg"
    }
    
    try:
        response = requests.get("https://api.intelligence.io.solutions/api/v1/models", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("✅ Прямое подключение к IO Intelligence API:")
            print(f"  Статус: {response.status_code}")
            print(f"  Количество моделей: {len(data.get('data', []))}")
            for model in data.get('data', [])[:3]:  # Показываем первые 3 модели
                print(f"  - {model.get('id', 'Unknown')}")
        else:
            print(f"❌ Ошибка прямого подключения: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Ошибка прямого подключения: {e}")

if __name__ == "__main__":
    print("🚀 Запуск тестов IO Intelligence API...")
    print(f"📍 Тестируем API по адресу: {BASE_URL}")
    
    test_direct_io_api()
    test_root()
    test_io_connection()
    test_models_endpoint()
    test_chat_completions()
    test_completions()
    test_health()
    
    print("\n✅ Тестирование завершено!") 