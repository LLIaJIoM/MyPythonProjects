# joke_generator.py
import requests
import uuid
import re

def make_joke(news_text):
    # Используем переменную окружения для URL GPT сервера
    import os
    gpt_url = os.getenv('GPT_API_URL', 'https://mypythonprojects-production.up.railway.app:8888')
    url = f"{gpt_url}/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Ты — острый сатирик и комик. Создавай провокационные, саркастичные и остроумные шутки на основе новостей. Используй чёрный юмор, иронию и сарказм. Шутки должны быть смелыми, но не оскорбительными."},
            {"role": "user", "content": f"Сделай из этой новости острую саркастичную шутку: {news_text}"}
        ]
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    try:
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            print(f"Ошибка GPT сервера: {response.status_code}")
            return "[Ошибка генерации шутки]"
    except Exception as e:
        print(f"Ошибка запроса к GPT: {e}")
        return "[Ошибка генерации шутки]"

# Пример использования:
# print(make_joke("В Москве прошёл дождь."))    