# joke_generator.py
import os
from huggingface_hub import InferenceClient

def make_joke(news_text):
    client = InferenceClient(
        provider="hf-inference",
        token=os.environ["HF_TOKEN"],
    )

    prompt = (
        "Ты — острый сатирик и комик. Создавай провокационные, саркастичные и остроумные шутки на основе новостей. "
        "Используй чёрный юмор, иронию и сарказм. Шутки должны быть смелыми, но не оскорбительными.\n"
        f"Сделай из этой новости острую саркастичную шутку: {news_text}"
    )

    completion = client.chat.completions.create(
        model="tiiuae/falcon-7b-instruct",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    return completion.choices[0].message.content

# Пример использования:
# print(make_joke("В Москве прошёл дождь."))    