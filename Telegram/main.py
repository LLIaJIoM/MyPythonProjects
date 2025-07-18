import time
import json
import os
from news_parser import get_latest_news
from joke_generator import make_joke
from telegram_sender import send_message
import asyncio

CHECK_INTERVAL = 60  # секунд между проверками
PROCESSED_FILE = "processed_news.json"

# Загрузка обработанных новостей
if os.path.exists(PROCESSED_FILE):
    with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
        processed_news = set(json.load(f))
else:
    processed_news = set()

def save_processed_news():
    with open(PROCESSED_FILE, "w", encoding="utf-8") as f:
        json.dump(list(processed_news), f, ensure_ascii=False)

def main():
    print("🤖 Бот запущен и работает...")
    
    while True:
        print("🔍 Проверяю новые новости...")
        
        for news in get_latest_news("https://lenta.ru/rss/news", limit=3):
            news_id = news['link']
            if news_id not in processed_news:
                joke = make_joke(f"{news['title']} {news['summary']}")
                
                # Форматируем сообщение с префиксом
                formatted_joke = f"🎭 ЮМОР:\n{joke}"
                message = f"📰 {news['title']}\n\n{formatted_joke}\n\nПодробнее: {news['link']}"
                
                asyncio.run(send_message(message))
                processed_news.add(news_id)
                save_processed_news()
                
                # Задержка 5 секунд между постами
                time.sleep(5)
        
        print(f"⏰ Ожидание {CHECK_INTERVAL} секунд до следующей проверки...")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()