#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы бота с шутками
"""

import os
import asyncio
from joke_generator import make_joke, make_joke_alternative
from news_parser import get_combined_news
from telegram_sender import test_telegram_connection, send_message

def test_joke_generation():
    """Тестирует генерацию шуток"""
    print("🎭 Тестирование генерации шуток...")
    print("=" * 40)
    
    test_news = [
        "В Москве прошёл дождь.",
        "Цены на бензин выросли на 5%.",
        "Новый фильм собрал рекордную кассу.",
        "Учёные открыли новый вид животных."
    ]
    
    for i, news in enumerate(test_news, 1):
        print(f"\n📰 Тест {i}: {news}")
        try:
            joke = make_joke(news)
            print(f"🎭 Шутка: {joke}")
            
            # Тестируем альтернативную модель
            alt_joke = make_joke_alternative(news)
            print(f"🎭 Альтернативная: {alt_joke}")
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")

def test_news_parsing():
    """Тестирует парсинг новостей"""
    print("\n📰 Тестирование парсинга новостей...")
    print("=" * 40)
    
    try:
        news_list = get_combined_news()
        print(f"✅ Получено {len(news_list)} новостей")
        
        for i, news in enumerate(news_list[:3], 1):
            print(f"\n{i}. {news['title']}")
            print(f"   Источник: {news.get('source', 'Неизвестно')}")
            print(f"   Ссылка: {news['link']}")
            
    except Exception as e:
        print(f"❌ Ошибка парсинга новостей: {e}")

async def test_telegram_sending():
    """Тестирует отправку в Telegram"""
    print("\n📱 Тестирование отправки в Telegram...")
    print("=" * 40)
    
    # Проверяем подключение
    if not test_telegram_connection():
        print("❌ Не удалось подключиться к Telegram")
        return
    
    # Тестируем отправку сообщения
    test_message = """🤖 <b>Тестовое сообщение от бота с шутками!</b>

🎭 <b>Тестовая шутка:</b>
Почему программисты путают Рождество и Хэллоуин? Потому что Oct 31 == Dec 25!

📊 <b>Статус:</b> Бот работает
🔗 <a href="https://t.me/your_channel">Канал</a>

#тест #бот #юмор"""
    
    try:
        success = await send_message(test_message)
        if success:
            print("✅ Тестовое сообщение отправлено!")
        else:
            print("❌ Ошибка отправки тестового сообщения")
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")

def test_environment():
    """Проверяет переменные окружения"""
    print("🔧 Проверка переменных окружения...")
    print("=" * 40)
    
    required_vars = [
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHANNEL_ID"
    ]
    
    for var in required_vars:
        value = os.environ.get(var, "")
        if value:
            print(f"✅ {var}: {'*' * len(value)}")
        else:
            print(f"❌ {var}: НЕ УСТАНОВЛЕН")
    
    print("\n💡 Для установки переменных используйте:")
    print("export TELEGRAM_BOT_TOKEN='ваш_токен'")
    print("export TELEGRAM_CHANNEL_ID='@ваш_канал'")

async def main():
    """Основная функция тестирования"""
    print("🧪 Комплексное тестирование бота с шутками")
    print("=" * 50)
    
    # Проверяем переменные окружения
    test_environment()
    
    # Тестируем генерацию шуток
    test_joke_generation()
    
    # Тестируем парсинг новостей
    test_news_parsing()
    
    # Тестируем отправку в Telegram
    await test_telegram_sending()
    
    print("\n✅ Тестирование завершено!")

if __name__ == "__main__":
    asyncio.run(main()) 