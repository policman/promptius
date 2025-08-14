#!/bin/bash

set -e

echo "🛑 Остановка всех локальных PostgreSQL (brew)..."
brew services list | grep postgresql | awk '{print $1}' | while read service; do
  echo "→ Остановка $service"
  brew services stop "$service" || true
done

echo "🔄 Перезапуск Docker PostgreSQL..."
docker compose down -v
docker compose up -d

echo "⏳ Ожидаем запуск базы данных..."
until docker exec -it promptius-db-1 pg_isready -U postgres > /dev/null 2>&1; do
  sleep 1
done

echo "✅ База данных в контейнере готова!"

echo "🧬 Запуск миграций Alembic..."
alembic upgrade head

echo "🎉 Готово! Всё успешно выполнено."
