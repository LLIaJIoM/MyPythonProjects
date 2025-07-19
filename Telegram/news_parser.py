import feedparser
import requests
from datetime import datetime, timedelta
import time

def get_latest_news(rss_url, limit=5):
    """Получает последние новости из RSS ленты"""
    try:
        # Парсим RSS ленту
        feed = feedparser.parse(rss_url)
        
        if feed.bozo:
            print(f"⚠️ Ошибка парсинга RSS: {feed.bozo_exception}")
            return []
        
        news_list = []
        
        for entry in feed.entries[:limit]:
            # Извлекаем данные новости
            title = entry.get('title', 'Без заголовка')
            summary = entry.get('summary', '')
            link = entry.get('link', '')
            
            # Очищаем текст от HTML тегов
            summary = clean_html(summary)
            
            # Проверяем, что новость не слишком старая (не старше 24 часов)
            if 'published_parsed' in entry:
                pub_date = datetime(*entry.published_parsed[:6])
                if datetime.now() - pub_date > timedelta(hours=24):
                    continue
            
            news_list.append({
                'title': title,
                'summary': summary,
                'link': link,
                'published': entry.get('published', '')
            })
        
        print(f"📰 Получено {len(news_list)} новостей из {rss_url}")
        return news_list
        
    except Exception as e:
        print(f"❌ Ошибка получения новостей: {e}")
        return []

def clean_html(text):
    """Очищает текст от HTML тегов"""
    import re
    # Удаляем HTML теги
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    # Удаляем лишние пробелы
    text = ' '.join(text.split())
    return text

def get_news_from_lenta():
    """Получает новости с Lenta.ru"""
    return get_latest_news("https://lenta.ru/rss/news", limit=3)

def get_news_from_ria():
    """Получает новости с РИА Новости"""
    return get_latest_news("https://ria.ru/export/rss2/archive/index.xml", limit=3)

def get_news_from_tass():
    """Получает новости с ТАСС"""
    return get_latest_news("https://tass.ru/rss/v2.xml", limit=3)

def get_combined_news():
    """Получает новости только с Лента.ру"""
    all_news = []
    
    # Получаем новости только с Лента.ру
    try:
        news = get_news_from_lenta()
        for item in news:
            item['source'] = "Lenta.ru"
        all_news.extend(news)
        print(f"✅ Получено {len(news)} новостей с Лента.ру")
    except Exception as e:
        print(f"❌ Ошибка получения новостей с Лента.ру: {e}")
    
    # Сортируем по дате публикации (если доступна)
    all_news.sort(key=lambda x: x.get('published', ''), reverse=True)
    
    return all_news[:5]  # Возвращаем топ-5 новостей

if __name__ == "__main__":
    print("🧪 Тест парсера новостей...")
    
    # Тестируем разные источники
    sources = [
        ("Lenta.ru", "https://lenta.ru/rss/news"),
        ("РИА Новости", "https://ria.ru/export/rss2/archive/index.xml"),
        ("ТАСС", "https://tass.ru/rss/v2.xml")
    ]
    
    for source_name, url in sources:
        print(f"\n📰 Тестируем {source_name}:")
        news = get_latest_news(url, limit=2)
        for i, item in enumerate(news, 1):
            print(f"  {i}. {item['title'][:50]}...")
            print(f"     {item['summary'][:100]}...") 