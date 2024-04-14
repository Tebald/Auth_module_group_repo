Репозиторий для командного проекта Auth API.

## Запуск prod версии сервиса

`make prod-up` - запускает все сервисы.

## Запуск тестов в контейнере

`make tests-up`



## Локальный запуск приложения

Для локального запуска необходимо в файл `.env.local` скопировать в `.env`
и запустить `docker compose -f docker-compose.local.yml up`. Далее запустить локально `main.py`

