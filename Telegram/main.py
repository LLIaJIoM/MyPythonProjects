import time
import json
import os
import asyncio
from news_parser import get_latest_news, get_combined_news
from joke_generator import make_joke, make_joke_alternative
from telegram_sender import send_message, test_telegram_connection

CHECK_INTERVAL = 300  # 5 минут между проверками
PROCESSED_FILE = "processed_news.json"

# Загрузка обработанных новостей
if os.path.exists(PROCESSED_FILE):
    with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
        processed_news = set(json.load(f))
else:
    processed_news = set()

def save_processed_news():
    """Сохраняет обработанные новости в файл"""
    with open(PROCESSED_FILE, "w", encoding="utf-8") as f:
        json.dump(list(processed_news), f, ensure_ascii=False)

def format_news_message(news, joke):
    """Форматирует сообщение с новостью и шуткой"""
    source = news.get('source', 'Новости')
    
    message = f"""📰 <b>{news['title']}</b>

🎭 <b>ЮМОР:</b>
{joke}

📊 <b>Источник:</b> {source}
🔗 <a href="{news['link']}">Подробнее</a>

#новости #юмор #сатира"""
    
    return message

async def process_news():
    """Обрабатывает новые новости и отправляет шутки"""
    print("🔍 Проверяю новые новости...")
    
    try:
        # Получаем новости из нескольких источников
        news_list = get_combined_news()
        
        if not news_list:
            print("⚠️ Новости не найдены")
            return
        
        for news in news_list:
            news_id = news['link']
            
            if news_id not in processed_news:
                print(f"📰 Обрабатываю новость: {news['title'][:50]}...")
                
                # Генерируем шутку
                try:
                    joke = make_joke(f"{news['title']} {news['summary']}")
                    
                    # Если шутка слишком короткая, пробуем альтернативную модель
                    if len(joke) < 20:
                        joke = make_joke_alternative(f"{news['title']} {news['summary']}")
                    
                    # Форматируем сообщение
                    message = format_news_message(news, joke)
                    
                    # Отправляем в Telegram
                    success = await send_message(message)
                    
                    if success:
                        processed_news.add(news_id)
                        save_processed_news()
                        print(f"✅ Новость отправлена: {news['title'][:30]}...")
                    else:
                        print(f"❌ Ошибка отправки новости: {news['title'][:30]}...")
                    
                    # Задержка между постами
                    await asyncio.sleep(10)
                    
                except Exception as e:
                    print(f"❌ Ошибка обработки новости: {e}")
                    continue
            else:
                print(f"⏭️ Новость уже обработана: {news['title'][:30]}...")
        
        print(f"✅ Обработка завершена. Ожидание {CHECK_INTERVAL} секунд...")
        
    except Exception as e:
        print(f"❌ Ошибка получения новостей: {e}")

async def main():
    """Основная функция бота"""
    print("🤖 Бот с шутками запущен!")
    print("=" * 50)
    
    # Проверяем подключение к Telegram
    if not test_telegram_connection():
        print("❌ Не удалось подключиться к Telegram. Проверьте TELEGRAM_BOT_TOKEN")
        return
    
    # Тестируем генерацию шутки
    print("🧪 Тестируем генерацию шутки...")
    try:
        test_joke = make_joke("В Москве прошёл дождь.")
        print(f"✅ Тест шутки: {test_joke}")
    except Exception as e:
        print(f"❌ Ошибка теста шутки: {e}")
    
    print("🚀 Бот готов к работе!")
    print("=" * 50)
    
    while True:
        try:
            await process_news()
            await asyncio.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("\n🛑 Бот остановлен пользователем")
            break
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")
            await asyncio.sleep(60)  # Ждем минуту перед повторной попыткой

if __name__ == "__main__":
    asyncio.run(main())