from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Добавляем путь к G4F
sys.path.append('/app/g4f')

from g4f import ChatCompletion, Provider
import asyncio
import json

app = Flask(__name__)
CORS(app)

# Глобальная переменная для хранения последнего ответа
last_response = ""

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    global last_response
    
    try:
        data = request.get_json()
        messages = data.get('messages', [])
        model = data.get('model', 'gpt-3.5-turbo')
        
        # Формируем промпт из сообщений
        prompt = ""
        for message in messages:
            role = message.get('role', 'user')
            content = message.get('content', '')
            if role == 'user':
                prompt += f"User: {content}\n"
            elif role == 'assistant':
                prompt += f"Assistant: {content}\n"
            elif role == 'system':
                prompt += f"System: {content}\n"
        
        # Убираем последний перенос строки
        prompt = prompt.strip()
        
        # Генерируем ответ через G4F
        response = asyncio.run(generate_response(prompt))
        
        # Сохраняем последний ответ
        last_response = response
        
        # Формируем ответ в формате OpenAI
        return jsonify({
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1677652288,
            "model": model,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": len(prompt.split()),
                "completion_tokens": len(response.split()),
                "total_tokens": len(prompt.split()) + len(response.split())
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

async def generate_response(prompt):
    """Генерирует ответ через G4F"""
    try:
        # Пробуем разные провайдеры
        providers = [
            Provider.DeepInfra,
            Provider.DeepSeek,
            Provider.Gemini,
            Provider.GeminiPro
        ]
        
        for provider in providers:
            try:
                response = await ChatCompletion.create_async(
                    model="gpt-3.5-turbo",
                    provider=provider,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response
            except Exception as e:
                print(f"Ошибка с провайдером {provider}: {e}")
                continue
        
        # Если все провайдеры не работают, возвращаем заглушку
        return "Извините, не удалось сгенерировать ответ. Попробуйте позже."
        
    except Exception as e:
        return f"Ошибка генерации: {str(e)}"

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "last_response": last_response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8888))
    print(f"🚀 Запуск G4F сервера на порту {port}...")
    app.run(host='0.0.0.0', port=port, debug=False) 