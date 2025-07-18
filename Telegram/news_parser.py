# news_parser.py
import feedparser

def get_latest_news(rss_url, limit=5):
    feed = feedparser.parse(rss_url)
    
    if hasattr(feed, 'status') and feed.status != 200:
        return []
    
    if len(feed.entries) == 0:
        return []
    
    news = []
    for entry in feed.entries[:limit]:
        news.append({
            'title': entry.title,
            'summary': entry.summary,
            'link': entry.link
        })
    return news

# Пример использования:
if __name__ == "__main__":
    news = get_latest_news("https://lenta.ru/rss/news")
    for n in news:
        print(n['title'], n['link'])
