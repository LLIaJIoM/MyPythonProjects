# Telegram Бот с Шутками

Автоматический бот для генерации острых саркастичных шуток на основе новостей с использованием IO Intelligence API.

## 🚀 Возможности

- 📰 **Автоматический парсинг новостей** из нескольких источников (Lenta.ru, РИА Новости, ТАСС)
- 🎭 **Генерация острых шуток** с помощью IO Intelligence API
- 🤖 **Автоматическая отправка** в Telegram канал
- 🔄 **Отслеживание обработанных новостей** для избежания дублирования
- ⚡ **Асинхронная работа** для высокой производительности

## 📋 Установка

1. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

2. **Настройте переменные окружения:**
```bash
export TELEGRAM_BOT_TOKEN="ваш_токен_бота"
export TELEGRAM_CHANNEL_ID="@ваш_канал"
```

## 🔧 Настройка

### 1. Создание Telegram бота

1. Найдите @BotFather в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен

### 2. Настройка канала

1. Создайте канал в Telegram
2. Добавьте бота как администратора канала
3. Скопируйте ID канала (например: `@my_channel`)

### 3. Установка переменных окружения

**Windows:**
```cmd
set TELEGRAM_BOT_TOKEN=ваш_токен
set TELEGRAM_CHANNEL_ID=@ваш_канал
```

**Linux/Mac:**
```bash
export TELEGRAM_BOT_TOKEN="ваш_токен"
export TELEGRAM_CHANNEL_ID="@ваш_канал"
```

## 🚀 Запуск

### Основной запуск
```bash
cd Telegram
python main.py
```

### Тестирование
```bash
python test_bot.py
```

## 📁 Структура проекта

```
Telegram/
├── main.py                 # Основной файл бота
├── joke_generator.py       # Генератор шуток (IO Intelligence API)
├── news_parser.py          # Парсер новостей
├── telegram_sender.py      # Отправка в Telegram
├── test_bot.py            # Тестовый скрипт
├── README_BOT.md          # Документация
└── processed_news.json    # Файл с обработанными новостями
```

## 🎭 Генерация шуток

Бот использует две модели IO Intelligence API:

1. **CohereForAI/c4ai-command-r-plus-08-2024** - основная модель
2. **deepseek-ai/DeepSeek-R1-0528** - альтернативная модель

### Настройки генерации:
- **Temperature**: 0.8 (креативность)
- **Max tokens**: 150 (длина шутки)
- **Top_p**: 0.9 (разнообразие)

## 📰 Источники новостей

Бот автоматически получает новости из:
- **Lenta.ru** - https://lenta.ru/rss/news
- **РИА Новости** - https://ria.ru/export/rss2/archive/index.xml
- **ТАСС** - https://tass.ru/rss/v2.xml

## ⚙️ Настройки

### Интервалы проверки
```python
CHECK_INTERVAL = 300  # 5 минут между проверками
```

### Формат сообщений
```python
message = f"""📰 <b>{news['title']}</b>

🎭 <b>ЮМОР:</b>
{joke}

📊 <b>Источник:</b> {source}
🔗 <a href="{news['link']}">Подробнее</a>

#новости #юмор #сатира"""
```

## 🧪 Тестирование

### Комплексный тест
```bash
python test_bot.py
```

Тест проверяет:
- ✅ Подключение к IO Intelligence API
- ✅ Генерацию шуток
- ✅ Парсинг новостей
- ✅ Подключение к Telegram
- ✅ Отправку сообщений

### Тест генерации шуток
```bash
python joke_generator.py
```

## 🔍 Мониторинг

Бот выводит подробные логи:
- 📰 Обработка новостей
- 🎭 Генерация шуток
- ✅ Успешная отправка
- ❌ Ошибки и их причины

## 🛠️ Устранение неполадок

### Ошибка подключения к Telegram
```
❌ TELEGRAM_BOT_TOKEN не установлен
```
**Решение:** Проверьте переменную окружения `TELEGRAM_BOT_TOKEN`

### Ошибка отправки сообщений
```
❌ TELEGRAM_CHANNEL_ID не установлен
```
**Решение:** Проверьте переменную окружения `TELEGRAM_CHANNEL_ID`

### Ошибка генерации шуток
```
❌ Ошибка генерации шутки: ...
```
**Решение:** Проверьте подключение к интернету и доступность IO Intelligence API

### Новости не найдены
```
⚠️ Новости не найдены
```
**Решение:** Проверьте доступность RSS лент новостных сайтов

## 🔄 Автоматический запуск

### Systemd (Linux)
```bash
sudo nano /etc/systemd/system/news-joke-bot.service
```

```ini
[Unit]
Description=News Joke Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/your/project
Environment=TELEGRAM_BOT_TOKEN=your_token
Environment=TELEGRAM_CHANNEL_ID=@your_channel
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

## 📊 Статистика

Бот ведет статистику:
- Количество обработанных новостей
- Успешные отправки
- Ошибки генерации
- Время работы

## 🔒 Безопасность

- API ключи хранятся в переменных окружения
- Обработка ошибок и fallback механизмы
- Логирование всех операций
- Защита от дублирования новостей

## 📞 Поддержка

При возникновении проблем:
1. Проверьте переменные окружения
2. Запустите `test_bot.py` для диагностики
3. Проверьте логи бота
4. Убедитесь в доступности API и RSS лент 