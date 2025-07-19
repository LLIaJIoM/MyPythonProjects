# IO Intelligence API Server

Полнофункциональный API сервер для работы с IO Intelligence API, предоставляющий совместимый с OpenAI интерфейс.

## 🚀 Запуск

```bash
cd Telegram
python io_intelligence_api.py
```

Сервер запустится на порту 8888 и автоматически подключится к IO Intelligence API.

## 📋 Доступные эндпоинты

### 1. Корневой эндпоинт
```
GET /
```
Возвращает информацию об API и доступные эндпоинты.

### 2. Список моделей
```
GET /v1/models
```
Возвращает список всех доступных моделей из IO Intelligence API.

### 3. Информация о модели
```
GET /v1/models/{model_id}
```
Возвращает информацию о конкретной модели.

### 4. Чат комплеты
```
POST /v1/chat/completions
```
Основной эндпоинт для генерации ответов в формате чата.

**Пример запроса:**
```json
{
  "model": "deepseek-ai/DeepSeek-R1-0528",
  "messages": [
    {"role": "system", "content": "Ты полезный ассистент."},
    {"role": "user", "content": "Привет! Как дела?"}
  ],
  "temperature": 0.7,
  "max_tokens": 1000
}
```

### 5. Простые комплеты (legacy)
```
POST /v1/completions
```
Эндпоинт для простых текстовых комплетов.

**Пример запроса:**
```json
{
  "model": "deepseek-ai/DeepSeek-R1-0528",
  "prompt": "Расскажи короткую шутку:",
  "temperature": 0.7,
  "max_tokens": 100
}
```

### 6. Проверка здоровья
```
GET /health
```
Возвращает статус сервера и статистику запросов.

### 7. Тест подключения к IO API
```
GET /test-io-api
```
Тестирует подключение к IO Intelligence API.

## 🤖 Доступные модели

Сервер автоматически получает список моделей из IO Intelligence API. Примеры доступных моделей:

- `deepseek-ai/DeepSeek-R1-0528` - DeepSeek R1
- `meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8` - Llama 4 Maverick
- `Qwen/Qwen3-235B-A22B-FP8` - Qwen 3
- `meta-llama/Llama-3.2-90B-Vision-Instruct` - Llama 3.2 Vision
- `google/gemma-3-27b-it` - Gemma 3
- `mistralai/Mistral-Large-Instruct-2411` - Mistral Large
- И многие другие...

## 🔧 Особенности

- **Автоматическое подключение**: Сервер автоматически подключается к IO Intelligence API
- **Совместимость с OpenAI**: Полная совместимость с форматом OpenAI API
- **Мониторинг**: Ведение статистики запросов и ошибок
- **Fallback**: Автоматическое переключение на резервные модели при ошибках
- **CORS поддержка**: Готов для веб-приложений

## 📊 Мониторинг

Сервер ведет статистику:
- Общее количество запросов
- Количество ошибок
- Процент успешных запросов
- Статус подключения к IO Intelligence API
- Последний сгенерированный ответ

## 🧪 Тестирование

### Быстрый тест
```bash
python quick_test.py
```

### Полный тест
```bash
python test_io_api.py
```

## 📝 Примеры использования

### Python
```python
import requests

# Чат комплеты
response = requests.post("http://localhost:8888/v1/chat/completions", json={
    "model": "deepseek-ai/DeepSeek-R1-0528",
    "messages": [
        {"role": "user", "content": "Привет!"}
    ]
})

print(response.json()["choices"][0]["message"]["content"])
```

### JavaScript
```javascript
// Чат комплеты
const response = await fetch("http://localhost:8888/v1/chat/completions", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        model: "deepseek-ai/DeepSeek-R1-0528",
        messages: [
            {role: "user", content: "Привет!"}
        ]
    })
});

const data = await response.json();
console.log(data.choices[0].message.content);
```

### cURL
```bash
# Получить список моделей
curl http://localhost:8888/v1/models

# Генерация ответа
curl -X POST http://localhost:8888/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-ai/DeepSeek-R1-0528",
    "messages": [
      {"role": "user", "content": "Привет!"}
    ]
  }'
```

## 🔒 Безопасность

- API ключ IO Intelligence встроен в сервер
- Все запросы логируются
- Обработка ошибок с информативными сообщениями
- CORS поддержка для веб-приложений

## 🚀 Развертывание

### Локально
```bash
python io_intelligence_api.py
```

### Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY io_intelligence_api.py .
EXPOSE 8888
CMD ["python", "io_intelligence_api.py"]
```

### Heroku
```bash
heroku create your-app-name
git push heroku main
```

## 📦 Зависимости

- Flask
- Flask-CORS
- requests

## 🔄 Обновления

API полностью совместим с форматом OpenAI API и автоматически получает актуальный список моделей из IO Intelligence API.

## 📞 Поддержка

При возникновении проблем:
1. Проверьте подключение к интернету
2. Убедитесь, что IO Intelligence API доступен
3. Проверьте логи сервера
4. Используйте эндпоинт `/test-io-api` для диагностики 