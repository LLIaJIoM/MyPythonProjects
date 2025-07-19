# joke_generator.py
import os
import requests

# Конфигурация IO Intelligence API
IO_API_BASE_URL = "https://api.intelligence.io.solutions/api/v1"
IO_API_KEY = "io-v2-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvd25lciI6IjY3YzM5OGE5LTZkNzYtNDMyZS1iYTlhLTY5ODZiODVjMmRkOCIsImV4cCI6NDkwNjQ4MTUwOX0.m0CayY7WgNNksnxAj-QAhsEYUEJNKbpujJoSm7sFwEwFxOeCNrrQx3jGLAh-vCwKd7wAvvDvFg3MnNjj8FIEdg"

def get_headers():
    """Возвращает заголовки для API запросов"""
    return {
        "accept": "application/json",
        "Authorization": f"Bearer {IO_API_KEY}",
        "Content-Type": "application/json"
    }

def make_joke(news_text):
    """Генерирует острую саркастичную шутку на основе новости"""
    try:
        # Используем модель CohereForAI/c4ai-command-r-plus-08-2024 для лучших результатов
        url = f"{IO_API_BASE_URL}/chat/completions"
        
        messages = [
            {
                "role": "system",
                "content": "Ты сатирик. Создавай короткие острые шутки. Отвечай только шуткой, без лишнего текста."
            },
            {
                "role": "user",
                "content": f"Шутка про: {news_text}"
            }
        ]
        
        data = {
            "model": "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
            "messages": messages,
            "max_tokens": 60,
            "temperature": 0.8,
        }
        
        response = requests.post(url, headers=get_headers(), json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        joke = result["choices"][0]["message"]["content"].strip()
        
        # Убираем лишние кавычки и форматирование
        joke = joke.replace('"', '').replace('"', '').replace('"', '')
        
        return joke
        
    except Exception as e:
        print(f"❌ Ошибка генерации шутки: {e}")
        # Fallback шутка
        return f"🤡 А вот и новость: {news_text[:50]}... Классика!"

def make_joke_alternative(news_text):
    """Альтернативная функция с другой моделью"""
    try:
        url = f"{IO_API_BASE_URL}/chat/completions"
        
        messages = [
            {
                "role": "system",
                "content": "Ты комик-сатирик. Создавай короткие, острые и саркастичные шутки. Используй иронию и чёрный юмор. Отвечай только шуткой."
            },
            {
                "role": "user",
                "content": f"Новость: {news_text}. Сделай острую шутку."
            }
        ]
        
        data = {
            "model": "deepseek-ai/DeepSeek-R1-0528",
            "messages": messages,
            "max_tokens": 100,
            "temperature": 0.9,
        }
        
        response = requests.post(url, headers=get_headers(), json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        return result["choices"][0]["message"]["content"].strip()
        
    except Exception as e:
        print(f"❌ Ошибка альтернативной генерации: {e}")
        return make_joke(news_text)  # Fallback к основной функции

# Пример использования:
if __name__ == "__main__":
    test_news = "В Москве прошёл дождь."
    print("🎭 Тест генерации шутки:")
    print(f"Новость: {test_news}")
    print(f"Шутка: {make_joke(test_news)}")    