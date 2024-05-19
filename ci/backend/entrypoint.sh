#!/usr/bin/env sh
set -e

dockerize -wait tcp://postgres:5432 -wait tcp://mq:5672 -wait tcp://redis:6379 -timeout 120s

# Миграция и синхронизация
./manage.py migrate --noinput
./manage.py collectstatic --noinput
./manage.py loaddata offers_categories

./manage.py runserver 0.0.0.0:8000
