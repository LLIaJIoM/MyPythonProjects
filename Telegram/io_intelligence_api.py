from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import time
import uuid
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Конфигурация IO Intelligence API
IO_API_BASE_URL = "https://api.intelligence.io.solutions/api/v1"
IO_API_KEY = "io-v2-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvd25lciI6IjY3YzM5OGE5LTZkNzYtNDMyZS1iYTlhLTY5ODZiODVjMmRkOCIsImV4cCI6NDkwNjQ4MTUwOX0.m0CayY7WgNNksnxAj-QAhsEYUEJNKbpujJoSm7sFwEwFxOeCNrrQx3jGLAh-vCwKd7wAvvDvFg3MnNjj8FIEdg"

# Глобальные переменные для мониторинга
last_response = ""
request_count = 0
error_count = 0

# Заголовки для API запросов
def get_headers():
    return {
        "accept": "application/json",
        "Authorization": f"Bearer {IO_API_KEY}",
        "Content-Type": "application/json"
    }

# Доступные модели (получаем из API)
AVAILABLE_MODELS = {}

def fetch_models():
    """Получает список доступных моделей из IO Intelligence API"""
    global AVAILABLE_MODELS
    try:
        response = requests.get(f"{IO_API_BASE_URL}/models", headers=get_headers())
        if response.status_code == 200:
            data = response.json()
            models = {}
            for model in data.get('data', []):
                model_id = model.get('id', '')
                if model_id:
                    models[model_id] = {
                        "id": model_id,
                        "object": "model",
                        "created": model.get('created', int(time.time())),
                        "owned_by": model.get('owned_by', 'io-intelligence'),
                        "permission": model.get('permission', [])
                    }
            AVAILABLE_MODELS = models
            print(f"✅ Загружено {len(models)} моделей из IO Intelligence API")
        else:
            print(f"❌ Ошибка получения моделей: {response.status_code}")
            # Fallback модели
            AVAILABLE_MODELS = {
                "deepseek-ai/DeepSeek-R1": {
                    "id": "deepseek-ai/DeepSeek-R1",
                    "object": "model",
                    "created": int(time.time()),
                    "owned_by": "io-intelligence"
                }
            }
    except Exception as e:
        print(f"❌ Ошибка подключения к IO Intelligence API: {e}")
        # Fallback модели
        AVAILABLE_MODELS = {
            "deepseek-ai/DeepSeek-R1": {
                "id": "deepseek-ai/DeepSeek-R1",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "io-intelligence"
            }
        }

@app.route('/v1/models', methods=['GET'])
def list_models():
    """Список доступных моделей"""
    models = []
    for model_id, model_data in AVAILABLE_MODELS.items():
        models.append({
            "id": model_id,
            "object": "model",
            "created": model_data.get('created', int(time.time())),
            "owned_by": model_data.get('owned_by', 'io-intelligence'),
            "permission": model_data.get('permission', [{
                "id": f"modelperm-{uuid.uuid4().hex[:24]}",
                "object": "model_permission",
                "created": int(time.time()),
                "allow_create_engine": False,
                "allow_sampling": True,
                "allow_logprobs": True,
                "allow_search_indices": False,
                "allow_view": True,
                "allow_fine_tuning": False,
                "organization": "*",
                "group": None,
                "is_blocking": False
            }]),
            "root": None,
            "parent": None,
            "max_model_len": None
        })
    
    return jsonify({
        "object": "list",
        "data": models
    })

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    """Основной эндпоинт для генерации чат-комплетов"""
    global last_response, request_count, error_count
    
    request_count += 1
    
    try:
        data = request.get_json()
        messages = data.get('messages', [])
        model = data.get('model', 'deepseek-ai/DeepSeek-R1')
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 1000)
        stream = data.get('stream', False)
        
        if not messages:
            return jsonify({"error": "No messages provided"}), 400
        
        # Формируем запрос к IO Intelligence API
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        # Отправляем запрос к IO Intelligence API
        response = requests.post(
            f"{IO_API_BASE_URL}/chat/completions",
            json=payload,
            headers=get_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            last_response = data.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            # Возвращаем ответ в том же формате
            return jsonify(data)
        else:
            error_count += 1
            return jsonify({"error": f"IO Intelligence API error: {response.status_code}", "details": response.text}), response.status_code
        
    except Exception as e:
        error_count += 1
        return jsonify({"error": str(e)}), 500

@app.route('/v1/completions', methods=['POST'])
def completions():
    """Эндпоинт для простых комплетов (legacy)"""
    global request_count, error_count
    
    request_count += 1
    
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        model = data.get('model', 'deepseek-ai/DeepSeek-R1')
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 1000)
        
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400
        
        # Формируем запрос к IO Intelligence API
        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        # Отправляем запрос к IO Intelligence API
        response = requests.post(
            f"{IO_API_BASE_URL}/completions",
            json=payload,
            headers=get_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            error_count += 1
            return jsonify({"error": f"IO Intelligence API error: {response.status_code}", "details": response.text}), response.status_code
        
    except Exception as e:
        error_count += 1
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Эндпоинт для проверки здоровья сервера"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "last_response": last_response[:100] + "..." if len(last_response) > 100 else last_response,
        "stats": {
            "total_requests": request_count,
            "error_count": error_count,
            "success_rate": ((request_count - error_count) / request_count * 100) if request_count > 0 else 100
        },
        "io_api_status": "connected" if AVAILABLE_MODELS else "disconnected"
    })

@app.route('/v1/models/<model_id>', methods=['GET'])
def get_model(model_id):
    """Получить информацию о конкретной модели"""
    if model_id not in AVAILABLE_MODELS:
        return jsonify({"error": "Model not found"}), 404
    
    model_data = AVAILABLE_MODELS[model_id]
    return jsonify({
        "id": model_id,
        "object": "model",
        "created": model_data.get('created', int(time.time())),
        "owned_by": model_data.get('owned_by', 'io-intelligence'),
        "permission": model_data.get('permission', [{
            "id": f"modelperm-{uuid.uuid4().hex[:24]}",
            "object": "model_permission",
            "created": int(time.time()),
            "allow_create_engine": False,
            "allow_sampling": True,
            "allow_logprobs": True,
            "allow_search_indices": False,
            "allow_view": True,
            "allow_fine_tuning": False,
            "organization": "*",
            "group": None,
            "is_blocking": False
        }]),
        "root": None,
        "parent": None,
        "max_model_len": None
    })

@app.route('/', methods=['GET'])
def root():
    """Корневой эндпоинт с информацией об API"""
    return jsonify({
        "message": "IO Intelligence API Server",
        "version": "1.0.0",
        "endpoints": {
            "models": "/v1/models",
            "chat_completions": "/v1/chat/completions",
            "completions": "/v1/completions",
            "health": "/health"
        },
        "available_models": list(AVAILABLE_MODELS.keys()),
        "api_provider": "IO Intelligence"
    })

@app.route('/test-io-api', methods=['GET'])
def test_io_api():
    """Тестирует подключение к IO Intelligence API"""
    try:
        response = requests.get(f"{IO_API_BASE_URL}/models", headers=get_headers())
        if response.status_code == 200:
            data = response.json()
            return jsonify({
                "status": "connected",
                "models_count": len(data.get('data', [])),
                "models": [model.get('id') for model in data.get('data', [])]
            })
        else:
            return jsonify({
                "status": "error",
                "status_code": response.status_code,
                "error": response.text
            })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8888))
    print(f"🚀 Запуск IO Intelligence API сервера на порту {port}...")
    
    # Загружаем модели при запуске
    fetch_models()
    
    print(f"📊 Доступные модели: {list(AVAILABLE_MODELS.keys())}")
    print(f"🔗 API доступен по адресу: http://localhost:{port}")
    print(f"🔗 Тест подключения: http://localhost:{port}/test-io-api")
    
    app.run(host='0.0.0.0', port=port, debug=False) 