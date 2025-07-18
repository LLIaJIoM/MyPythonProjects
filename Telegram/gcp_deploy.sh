#!/bin/bash

echo "🚀 Развертывание на Google Cloud Free Tier..."

# Google Cloud дает БЕСПЛАТНО:
# - 1 виртуальная машина (1GB RAM)
# - 30GB хранилище
# - На 12 месяцев бесплатно

echo "📋 Инструкция для Google Cloud:"
echo ""
echo "1. Зарегистрируйтесь на console.cloud.google.com"
echo "2. Создайте Compute Engine:"
echo "   - Ubuntu 22.04"
echo "   - e2-micro (бесплатный тариф)"
echo "   - 1GB RAM"
echo ""
echo "3. Подключитесь к серверу:"
echo "   gcloud compute ssh YOUR_INSTANCE_NAME"
echo ""
echo "4. Запустите установку:"
echo "   wget https://raw.githubusercontent.com/your-repo/deploy.sh"
echo "   chmod +x deploy.sh"
echo "   sudo ./deploy.sh"
echo ""
echo "5. Загрузите проект:"
echo "   ./upload_to_server.sh YOUR_SERVER_IP"
echo ""
echo "⚠️ Бесплатно только 12 месяцев!" 