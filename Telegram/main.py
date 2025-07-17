from news_parser import get_latest_news
from joke_generator import make_joke
from telegram_sender import send_message
import asyncio

def main():
    news_list = get_latest_news("https://meduza.io/rss/all", limit=3)
    for news in news_list:
        joke = make_joke(news['title'] + " " + news['summary'])
        asyncio.run(send_message(f"📰 {news['title']}\n\n{joke}\n\nПодробнее: {news['link']}"))

if __name__ == "__main__":
    main()