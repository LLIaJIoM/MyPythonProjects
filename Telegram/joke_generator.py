# joke_generator.py
import requests

OPENROUTER_API_KEY = "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"

def make_joke(news_text):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
        # Можно добавить: "HTTP-Referer": "localhost", "X-Title": "my-bot"
    }
    data = {
        "model": "deepseek/deepseek-chat-v3-0324:free",
        "messages": [
            {"role": "system", "content": "Ты — остроумный комик. Преврати новость в короткую шутку."},
            {"role": "user", "content": f"Сделай из этой новости шутку: {news_text}"}
        ],
        "stream": False,
        "temperature": 0.8,
        "max_tokens": 100
    }
    response = requests.post(url, headers=headers, json=data)
    try:
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        return "[Ошибка генерации шутки]"

# Пример использования:
# print(make_joke("В Москве прошёл дождь."))    