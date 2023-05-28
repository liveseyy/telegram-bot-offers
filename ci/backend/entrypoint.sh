#!/usr/bin/env sh
# @TODO: что это значит?
set -e

# Ожидаем запуска postgres
dockerize -wait tcp://${POSTGRES_HOST}:${POSTGRES_PORT}

# Миграция и синхронизация
./manage.py migrate --noinput
./manage.py collectstatic --noinput

# Запуск команды
./manage.py runserver 0.0.0.0:8000
