# 🚀 Развертывание Telegram бота на VPS

## Шаг 1: Создание VPS на DigitalOcean

1. **Зарегистрируйтесь** на [digitalocean.com](https://digitalocean.com)
2. **Создайте Droplet**:
   - Выберите Ubuntu 22.04 LTS
   - Размер: Basic ($6/месяц) - достаточно для бота
   - Регион: Amsterdam (ближе к России)
   - Аутентификация: SSH ключ (рекомендуется)

## Шаг 2: Подключение к серверу

```bash
# Подключитесь к серверу
ssh root@YOUR_SERVER_IP

# Обновите систему
apt update && apt upgrade -y

# Установите Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Установите Docker Compose
apt install docker-compose -y

# Добавьте пользователя в группу docker
usermod -aG docker $USER
```

## Шаг 3: Загрузка проекта

```bash
# Создайте директорию для проекта
mkdir -p /opt/telegram-bot
cd /opt/telegram-bot

# Клонируйте ваш репозиторий (если есть)
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git .

# Или загрузите файлы через SCP
# scp -r ./Telegram/* root@YOUR_SERVER_IP:/opt/telegram-bot/
```

## Шаг 4: Настройка переменных окружения

```bash
# Создайте файл с переменными
cat > .env << EOF
TELEGRAM_TOKEN=7638129033:AAEYmXQikS0qa-qJ-Roxp3Wg7HLEQH9f-ao
CHANNEL_ID=-1002719144496
GPT_API_URL=http://gpt-server:8080
EOF
```

## Шаг 5: Запуск проекта

```bash
# Запустите контейнеры
docker-compose up -d

# Проверьте статус
docker-compose ps

# Посмотрите логи
docker-compose logs -f
```

## Шаг 6: Настройка автозапуска

```bash
# Создайте systemd сервис
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

# Включите автозапуск
systemctl enable telegram-bot.service
systemctl start telegram-bot.service
```

## Шаг 7: Мониторинг

```bash
# Проверка статуса
systemctl status telegram-bot

# Просмотр логов
docker-compose logs -f telegram-bot

# Проверка GPT сервера
curl http://localhost:8080/health
```

## 🔧 Управление

### Остановка:
```bash
docker-compose down
```

### Перезапуск:
```bash
docker-compose restart
```

### Обновление:
```bash
cd /opt/telegram-bot
git pull
docker-compose down
docker-compose up -d --build
```

## 💰 Стоимость

- **DigitalOcean**: $6/месяц (1GB RAM, 1 CPU)
- **Vultr**: $5/месяц (1GB RAM, 1 CPU)
- **Linode**: $5/месяц (1GB RAM, 1 CPU)

## 🛡️ Безопасность

```bash
# Настройте firewall
ufw allow ssh
ufw allow 80
ufw allow 443
ufw enable

# Обновите SSH конфигурацию
nano /etc/ssh/sshd_config
# Измените порт и отключите root доступ
```

## 📊 Мониторинг ресурсов

```bash
# Установите htop для мониторинга
apt install htop -y
htop

# Проверка диска
df -h

# Проверка памяти
free -h
``` 