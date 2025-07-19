#!/usr/bin/env python3
"""
Тест получения новостей только с Лента.ру
"""

from news_parser import get_combined_news

def test_lenta_only():
    """Тестирует получение новостей только с Лента.ру"""
    print("🧪 Тест получения новостей только с Лента.ру")
    print("=" * 50)
    
    # Получаем новости
    news = get_combined_news()
    
    print(f"\n📊 Получено {len(news)} новостей:")
    print("=" * 50)
    
    for i, item in enumerate(news, 1):
        print(f"\n{i}. {item['title']}")
        print(f"   📰 Источник: {item['source']}")
        print(f"   🔗 Ссылка: {item['link']}")
        print(f"   📝 Краткое описание: {item['summary'][:100]}...")
        print("-" * 50)
    
    # Проверяем, что все новости с Лента.ру
    all_from_lenta = all(item['source'] == 'Lenta.ru' for item in news)
    
    if all_from_lenta:
        print("\n✅ ВСЕ новости получены с Лента.ру!")
    else:
        print("\n❌ Некоторые новости не с Лента.ру!")
        
        for item in news:
            if item['source'] != 'Lenta.ru':
                print(f"   ❌ {item['title']} - {item['source']}")

if __name__ == "__main__":
    test_lenta_only() 