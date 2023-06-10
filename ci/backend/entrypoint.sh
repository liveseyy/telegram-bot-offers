#!/usr/bin/env sh
# @TODO: что это значит?
set -e

dockerize -wait tcp://psql:5432 -wait tcp://mq:5672 -wait tcp://redis:6379 -timeout 120s

# Миграция и синхронизация
./manage.py migrate --noinput
./manage.py collectstatic --noinput

# Запуск команды
./manage.py runserver 0.0.0.0:8000
