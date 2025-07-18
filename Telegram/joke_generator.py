# joke_generator.py
import requests
import uuid
import re

def make_joke(news_text):
    import os
    HF_API_TOKEN = os.getenv('HF_API_TOKEN', 'hf_ВАШ_ТОКЕН_СЮДА')
    HF_MODEL_ID = os.getenv('HF_MODEL_ID', 'gpt2')  # Можно указать свою модель
    API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL_ID}"
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

    prompt = f"Ты — острый сатирик и комик. Создавай провокационные, саркастичные и остроумные шутки на основе новостей. Используй чёрный юмор, иронию и сарказм. Шутки должны быть смелыми, но не оскорбительными.\nСделай из этой новости острую саркастичную шутку: {news_text}"
    data = {"inputs": prompt}

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            result = response.json()
            # HuggingFace может возвращать список или dict
            if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
                return result[0]['generated_text']
            elif isinstance(result, dict) and 'generated_text' in result:
                return result['generated_text']
            else:
                return str(result)
        else:
            print(f"Ошибка HuggingFace API: {response.status_code} {response.text}")
            return "[Ошибка генерации шутки]"
    except Exception as e:
        print(f"Ошибка запроса к HuggingFace API: {e}")
        return "[Ошибка генерации шутки]"

# Пример использования:
# print(make_joke("В Москве прошёл дождь."))    