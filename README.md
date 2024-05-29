# Telegram-бот для поиска новых объявлений о продаже автомобилей
## Запуск приложения

```shell
# Скопировать .env.dist в файл .env
cp ci/.env.dist ci/.env
# Зайти в папку `cd ci/dev`
cd ci
# заполнить переменные TG_BOT_TOKEN и TG_BOT_USERNAME
nano .env
# Запустить приложение
sudo docker compose up --build
```
