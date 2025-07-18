# joke_generator.py
import os
import requests

def make_joke(news_text):
    api_key = os.environ["TOGETHER_API_KEY"]
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    messages = [
        {
            "role": "system",
            "content": "Ты — острый сатирик и комик. Создавай провокационные, саркастичные и остроумные шутки на основе новостей. Используй чёрный юмор, иронию и сарказм. Шутки должны быть смелыми, но не оскорбительными."
        },
        {
            "role": "user",
            "content": f"Сделай из этой новости острую саркастичную шутку: {news_text}"
        }
    ]
    data = {
        "model": "meta-llama/Llama-2-70b-chat-hf",
        "messages": messages,
        "max_tokens": 100,
        "temperature": 0.7,
        "top_p": 0.9,
    }
    response = requests.post(url, headers=headers, json=data, timeout=60)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"].strip()

# Пример использования:
# print(make_joke("В Москве прошёл дождь."))    