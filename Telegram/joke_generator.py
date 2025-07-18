# joke_generator.py
import requests
import uuid
import re

def make_joke(news_text):
    url = "http://localhost:8080/backend-api/v2/conversation"
    headers = {"Content-Type": "application/json"}
    
    # Генерируем уникальные ID
    request_id = str(int(uuid.uuid4().int % 10**18))
    conversation_id = str(uuid.uuid4())
    
    data = {
        "id": request_id,
        "conversation_id": conversation_id,
        "action": "next",
        "api_key": None,
        "aspect_ratio": "16:9",
        "conversation": None,
        "download_media": True,
        "ignored": ["Anthropic", "Blackbox", "BlackboxPro", "CablyAI", "Cerebras"],
        "messages": [
            {"role": "system", "content": "Ты — острый сатирик и комик. Создавай провокационные, саркастичные и остроумные шутки на основе новостей. Используй чёрный юмор, иронию и сарказм. Шутки должны быть смелыми, но не оскорбительными."},
            {"role": "user", "content": f"Сделай из этой новости острую саркастичную шутку: {news_text}"}
        ],
        "model": "openai",
        "provider": "PollinationsAI",
        "web_search": False
    }
    
    response = requests.post(url, json=data, headers=headers, stream=True)
    
    try:
        full_response = ""
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                
                # Проверяем, что это JSON строка
                if line.strip().startswith('{'):
                    try:
                        import json
                        json_data = json.loads(line)
                        
                        # Извлекаем текст только из строк с type: "content"
                        if json_data.get("type") == "content" and "content" in json_data:
                            content = json_data["content"]
                            full_response += content
                            
                        # Проверяем на завершение
                        elif json_data.get("type") == "finish":
                            break
                            
                    except json.JSONDecodeError:
                        pass
        
        return full_response.strip() if full_response else "[Ошибка генерации шутки]"
    except Exception as e:
        return "[Ошибка генерации шутки]"

# Пример использования:
# print(make_joke("В Москве прошёл дождь."))    