#!/usr/bin/env python3
"""
Демо-версия бота с шутками (без Telegram)
"""

import time
import json
import os
from news_parser import get_combined_news
from joke_generator import make_joke, make_joke_alternative

def format_news_message(news, joke):
    """Форматирует сообщение с новостью и шуткой"""
    source = news.get('source', 'Новости')
    
    message = f"""📰 {news['title']}

🎭 ЮМОР:
{joke}

📊 Источник: {source}
🔗 Подробнее: {news['link']}

#новости #юмор #сатира"""
    
    return message

def demo_bot():
    """Демо-версия бота"""
    print("🤖 Демо-версия бота с шутками")
    print("=" * 50)
    
    # Тестируем генерацию шутки
    print("🧪 Тестируем генерацию шутки...")
    try:
        test_joke = make_joke("В Москве прошёл дождь.")
        print(f"✅ Тест шутки: {test_joke}")
    except Exception as e:
        print(f"❌ Ошибка теста шутки: {e}")
    
    print("\n📰 Получаем новости...")
    
    try:
        # Получаем новости
        news_list = get_combined_news()
        
        if not news_list:
            print("⚠️ Новости не найдены")
            return
        
        print(f"✅ Получено {len(news_list)} новостей")
        
        # Обрабатываем первые 3 новости
        for i, news in enumerate(news_list[:3], 1):
            print(f"\n{'='*60}")
            print(f"📰 Новость {i}: {news['title']}")
            print(f"📊 Источник: {news.get('source', 'Неизвестно')}")
            
            # Генерируем шутку
            try:
                joke = make_joke(f"{news['title']} {news['summary']}")
                
                # Если шутка слишком короткая, пробуем альтернативную модель
                if len(joke) < 20:
                    joke = make_joke_alternative(f"{news['title']} {news['summary']}")
                
                # Форматируем сообщение
                message = format_news_message(news, joke)
                
                print(f"\n🎭 Шутка: {joke}")
                print(f"\n📱 Сообщение для Telegram:")
                print("-" * 40)
                print(message)
                print("-" * 40)
                
                # Имитируем отправку
                print("✅ Сообщение отправлено (демо)")
                
                # Задержка между постами
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Ошибка обработки новости: {e}")
                continue
        
        print(f"\n{'='*60}")
        print("🎉 Демо завершено!")
        print("💡 Для полной работы настройте Telegram бота:")
        print("1. Создайте бота через @BotFather")
        print("2. Установите переменные окружения:")
        print("   TELEGRAM_BOT_TOKEN=ваш_токен")
        print("   TELEGRAM_CHANNEL_ID=@ваш_канал")
        print("3. Запустите: python main.py")
        
    except Exception as e:
        print(f"❌ Ошибка получения новостей: {e}")

if __name__ == "__main__":
    demo_bot() 