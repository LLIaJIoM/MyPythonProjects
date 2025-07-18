#!/bin/bash

echo "🚀 Автоматическое развертывание Telegram бота..."

# Проверяем, что мы root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Запустите скрипт от имени root"
    exit 1
fi

# Обновляем систему
echo "📦 Обновление системы..."
apt update && apt upgrade -y

# Устанавливаем Docker
echo "🐳 Установка Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    usermod -aG docker $USER
fi

# Устанавливаем Docker Compose
echo "📦 Установка Docker Compose..."
apt install docker-compose -y

# Создаем директорию проекта
echo "📁 Создание директории проекта..."
mkdir -p /opt/telegram-bot
cd /opt/telegram-bot

# Создаем .env файл
echo "⚙️ Настройка переменных окружения..."
cat > .env << EOF
TELEGRAM_TOKEN=7638129033:AAEYmXQikS0qa-qJ-Roxp3Wg7HLEQH9f-ao
CHANNEL_ID=-1002719144496
GPT_API_URL=http://gpt-server:8080
EOF

# Создаем systemd сервис
echo "🔧 Настройка автозапуска..."
cat > /etc/systemd/system/telegram-bot.service << EOF
[Unit]
Description=Telegram Bot with GPT
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/telegram-bot
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

# Включаем автозапуск
systemctl daemon-reload
systemctl enable telegram-bot.service

echo "✅ Установка завершена!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Скопируйте файлы проекта в /opt/telegram-bot/"
echo "2. Запустите: docker-compose up -d"
echo "3. Проверьте логи: docker-compose logs -f"
echo ""
echo "🔧 Полезные команды:"
echo "- Остановка: docker-compose down"
echo "- Перезапуск: docker-compose restart"
echo "- Логи: docker-compose logs -f"
echo "- Статус: systemctl status telegram-bot" 