#!/bin/bash

# Проверяем аргументы
if [ $# -eq 0 ]; then
    echo "❌ Укажите IP сервера"
    echo "Использование: ./upload_to_server.sh YOUR_SERVER_IP"
    exit 1
fi

SERVER_IP=$1

echo "🚀 Загрузка файлов на сервер $SERVER_IP..."

# Создаем архив с файлами проекта
echo "📦 Создание архива..."
tar -czf telegram-bot.tar.gz \
    docker-compose.yml \
    bot_dockerfile \
    gpt_dockerfile \
    requirements.txt \
    run_forever.py \
    railway.json \
    Procfile \
    Telegram/

# Загружаем архив на сервер
echo "📤 Загрузка на сервер..."
scp telegram-bot.tar.gz root@$SERVER_IP:/opt/telegram-bot/

# Выполняем команды на сервере
echo "🔧 Настройка на сервере..."
ssh root@$SERVER_IP << 'EOF'
cd /opt/telegram-bot
tar -xzf telegram-bot.tar.gz
rm telegram-bot.tar.gz

# Запускаем проект
docker-compose up -d

# Проверяем статус
docker-compose ps
EOF

echo "✅ Загрузка завершена!"
echo "🔍 Проверьте логи: ssh root@$SERVER_IP 'docker-compose logs -f'" 