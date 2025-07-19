# Настройка Telegram бота

## 🔧 Пошаговая инструкция

### 1. Создание бота

1. **Найдите @BotFather в Telegram**
   - Откройте Telegram
   - Найдите пользователя `@BotFather`
   - Нажмите "Start"

2. **Создайте нового бота**
   - Отправьте команду `/newbot`
   - Введите имя бота (например: "News Joke Bot")
   - Введите username бота (например: `my_news_joke_bot`)
   - Получите токен бота

3. **Скопируйте токен**
   - BotFather отправит вам токен вида:
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```
   - Сохраните этот токен

### 2. Создание канала

1. **Создайте канал в Telegram**
   - Нажмите на меню (☰)
   - Выберите "Создать канал"
   - Введите название канала
   - Добавьте описание (опционально)

2. **Настройте канал**
   - Сделайте канал публичным или приватным
   - Запомните username канала (если публичный) или ID

3. **Добавьте бота как администратора**
   - Откройте канал
   - Нажмите на название канала
   - Выберите "Администраторы"
   - Нажмите "Добавить администратора"
   - Найдите вашего бота по username
   - Дайте права на отправку сообщений

### 3. Получение ID канала

#### Для публичного канала:
- ID = `@username_канала`
- Пример: `@my_news_channel`

#### Для приватного канала:
1. Отправьте сообщение в канал
2. Перешлите это сообщение боту @userinfobot
3. Получите ID канала (например: `-1001234567890`)

### 4. Настройка переменных окружения

#### Windows (PowerShell):
```powershell
$env:TELEGRAM_BOT_TOKEN="ваш_токен_бота"
$env:TELEGRAM_CHANNEL_ID="ID_канала"
```

#### Windows (Command Prompt):
```cmd
set TELEGRAM_BOT_TOKEN=ваш_токен_бота
set TELEGRAM_CHANNEL_ID=ID_канала
```

#### Linux/Mac:
```bash
export TELEGRAM_BOT_TOKEN="ваш_токен_бота"
export TELEGRAM_CHANNEL_ID="ID_канала"
```

### 5. Тестирование

1. **Запустите тест:**
```bash
python test_bot.py
```

2. **Проверьте подключение:**
```bash
python test_send.py
```

3. **Запустите бота:**
```bash
python main.py
```

## 🔍 Примеры токенов и ID

### Токен бота:
```
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

### ID канала:
- Публичный: `@my_news_channel`
- Приватный: `-1001234567890`

## ⚠️ Частые ошибки

### Ошибка "Not Found":
- Проверьте правильность токена
- Убедитесь, что бот создан через @BotFather

### Ошибка "Forbidden":
- Бот не добавлен как администратор канала
- У бота нет прав на отправку сообщений

### Ошибка "Chat not found":
- Неправильный ID канала
- Бот не добавлен в канал

## 🛠️ Диагностика

### Проверка токена:
```python
import requests
token = "ваш_токен"
url = f"https://api.telegram.org/bot{token}/getMe"
response = requests.get(url)
print(response.json())
```

### Проверка канала:
```python
import requests
token = "ваш_токен"
chat_id = "ID_канала"
url = f"https://api.telegram.org/bot{token}/sendMessage"
data = {"chat_id": chat_id, "text": "Тест"}
response = requests.post(url, json=data)
print(response.json())
```

## 📞 Поддержка

Если возникли проблемы:
1. Проверьте все шаги выше
2. Убедитесь, что бот добавлен в канал
3. Проверьте права бота
4. Запустите `test_bot.py` для диагностики 