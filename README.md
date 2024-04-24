Репозиторий для командного проекта Auth API.

## Запуск prod версии сервиса

`make prod-up` - запускает все сервисы.

После того, как все сервисы стартовали, API доступен по адресу http://127.0.0.1/api/
Спецификация http://127.0.0.1/api/openapi

## Запуск тестов в контейнере

`make tests-up`

## Локальный запуск сервиса

Для локального запуска необходимо в файл `.env.local` скопировать `.env`
и запустить `make local-up`.

Закомментировать `API_HOST`, `ES_HOST` и `REDIS_HOST` переменные в файле `.env`. 

Далее запустить `main.py`.

## Локальный запуск тестов

Для локального запуска тестов необходимо запустить `make tests-local-up`.

Затем локально в файлк `.env.test` установить значение `PG_HOST="127.0.0.1"`

Далее из папки `auth-service` запустить `pytest`.


