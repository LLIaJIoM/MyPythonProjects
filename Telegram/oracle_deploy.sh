#!/bin/bash

echo "🚀 Развертывание на Oracle Cloud Free Tier..."

# Oracle Cloud дает БЕСПЛАТНО:
# - 2 AMD виртуальные машины (1GB RAM каждая)
# - 4 ARM виртуальные машины (24GB RAM общая)
# - 200GB хранилище
# - Навсегда бесплатно!

echo "📋 Инструкция для Oracle Cloud:"
echo ""
echo "1. Зарегистрируйтесь на cloud.oracle.com"
echo "2. Создайте виртуальную машину:"
echo "   - Ubuntu 22.04"
echo "   - ARM процессор (лучше для GPT)"
echo "   - 6GB RAM (достаточно для всего)"
echo ""
echo "3. Подключитесь к серверу:"
echo "   ssh ubuntu@YOUR_SERVER_IP"
echo ""
echo "4. Запустите установку:"
echo "   wget https://raw.githubusercontent.com/your-repo/deploy.sh"
echo "   chmod +x deploy.sh"
echo "   sudo ./deploy.sh"
echo ""
echo "5. Загрузите проект:"
echo "   ./upload_to_server.sh YOUR_SERVER_IP"
echo ""
echo "✅ Полностью бесплатно навсегда!" 